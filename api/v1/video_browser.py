"""
Video Browser — dev tool for browsing video collections and managing clips.

No authentication, no database. Pure filesystem operations.

Directory structure:
    games/
    └── jacks_world/              ← "game"
        └── videos/
            └── angela_white/     ← "collection"
                ├── video1.mp4
                └── clips/
                    └── video1/
                        ├── clip_001.mp4
                        ├── clips.json
                        └── posters/
"""

import json
import shutil
import subprocess
import threading
import time
from pathlib import Path
from urllib.parse import quote

import tomli

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from apps.assets.management.commands.split_video import process_single_video
from apps.assets.services.video_file_utils import extract_frame, probe_metadata

GAMES_ROOT = Path(settings.BASE_DIR) / "games"
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"}
FFMPEG_PATHS = ["ffmpeg", "/usr/local/bin/ffmpeg", "/opt/homebrew/bin/ffmpeg", "/usr/bin/ffmpeg"]


# =============================================================================
# Utilities
# =============================================================================

def find_ffmpeg() -> str | None:
    for p in FFMPEG_PATHS:
        try:
            result = subprocess.run([p, "-version"], capture_output=True, timeout=5)
            if result.returncode == 0:
                return p
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    return None


def validate_path(base: Path, *parts: str) -> Path:
    """Join parts under base and verify result doesn't escape it."""
    target = base.joinpath(*parts).resolve()
    if not str(target).startswith(str(base.resolve())):
        raise ValueError("Path escapes base directory")
    return target


def renumber_clips(clips_dir: Path) -> list[dict]:
    """Renumber all clip_*.mp4 files sequentially. Returns new clip metadata list."""
    clips = sorted(clips_dir.glob("clip_*.mp4"))
    posters_dir = clips_dir / "posters"

    # First pass: rename to temp names to avoid collisions
    temp_mapping = []
    for i, clip in enumerate(clips):
        temp_name = clips_dir / f"__temp_{i:03d}.mp4"
        clip.rename(temp_name)
        poster = posters_dir / clip.with_suffix(".jpg").name
        temp_poster = posters_dir / f"__temp_{i:03d}.jpg"
        if poster.exists():
            poster.rename(temp_poster)
        temp_mapping.append((temp_name, temp_poster if temp_poster.exists() else None))

    # Second pass: rename to final sequential names and build metadata
    clips_data = []
    for i, (temp_clip, temp_poster) in enumerate(temp_mapping):
        final_name = f"clip_{i + 1:03d}.mp4"
        final_clip = clips_dir / final_name
        temp_clip.rename(final_clip)

        if temp_poster and temp_poster.exists():
            final_poster = posters_dir / f"clip_{i + 1:03d}.jpg"
            temp_poster.rename(final_poster)

        try:
            _, _, dur = probe_metadata(str(final_clip))
        except Exception:
            dur = 0.0

        clips_data.append({
            "filename": final_name,
            "index": i + 1,
            "duration_sec": round(dur, 3),
        })

    return clips_data


def rebuild_clips_json(clips_dir: Path, clips_data: list[dict], source_video: str = ""):
    """Write a new clips.json from the given clip metadata."""
    has_posters = (clips_dir / "posters").exists()
    for clip in clips_data:
        if has_posters:
            clip["poster"] = f"posters/{clip['filename'].replace('.mp4', '.jpg')}"

    summary = {
        "source_video": source_video,
        "clips": clips_data,
    }

    with open(clips_dir / "clips.json", "w") as f:
        json.dump(summary, f, indent=2)


def _parse_body(request):
    """Parse JSON body from a POST request."""
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return {}


def _get_used_video_paths(game_name: str) -> set[str]:
    """Parse 6_final_game.toml and return set of video file paths used in game."""
    toml_path = GAMES_ROOT / game_name / "toml_phases" / "6_final_game.toml"
    if not toml_path.exists():
        return set()
    try:
        with open(toml_path, "rb") as f:
            data = tomli.load(f)
        paths = set()
        for canvas in data.get("canvases", []):
            for node in canvas.get("nodes", []):
                for block in node.get("blocks", []):
                    if block.get("type") == "video":
                        fp = block.get("props", {}).get("file", "")
                        if fp:
                            paths.add(fp)
        return paths
    except Exception:
        return set()


# =============================================================================
# Views
# =============================================================================

@require_GET
def scan(request):
    """Scan games directory and return JSON tree: games → collections → videos → clips."""
    cache_bust = int(time.time())
    if not GAMES_ROOT.exists():
        return JsonResponse({"games": []})

    games = []
    for game_dir in sorted(GAMES_ROOT.iterdir()):
        if not game_dir.is_dir():
            continue
        game_name = game_dir.name
        videos_root = game_dir / "videos"
        if not videos_root.exists() or not videos_root.is_dir():
            continue

        used_paths = _get_used_video_paths(game_name)
        collections = []
        for coll_dir in sorted(videos_root.iterdir()):
            if not coll_dir.is_dir():
                continue
            coll_name = coll_dir.name
            real_dir = coll_dir.resolve()

            videos = []
            for f in sorted(real_dir.iterdir()):
                if not f.is_file() or f.suffix.lower() not in VIDEO_EXTENSIONS:
                    continue

                video_data = {
                    "filename": f.name,
                    "stem": f.stem,
                    "url": f"/games/{quote(game_name)}/videos/{quote(coll_name)}/{quote(f.name)}",
                    "source_deleted": False,
                    "clips": [],
                }

                clips_dir_path = real_dir / "clips" / f.stem
                clips_json_path = clips_dir_path / "clips.json"
                if clips_json_path.exists():
                    try:
                        with open(clips_json_path) as jf:
                            meta = json.load(jf)

                        status = meta.get("status")
                        if status:
                            video_data["clip_status"] = status
                            video_data["clip_error"] = meta.get("error", "")
                        else:
                            video_data["duration"] = meta.get("total_duration_sec")
                            video_data["resolution"] = meta.get("resolution")
                            video_data["fps"] = meta.get("fps")

                            # Load descriptions if available
                            descriptions = {}
                            desc_file = clips_dir_path / "descriptions.json"
                            if desc_file.exists():
                                try:
                                    with open(desc_file) as df:
                                        desc_data = json.load(df)
                                    descriptions = desc_data.get("results", {})
                                except (json.JSONDecodeError, KeyError):
                                    pass

                            # Load description generation status
                            desc_status_file = clips_dir_path / "desc_status.json"
                            if desc_status_file.exists():
                                try:
                                    with open(desc_status_file) as sf:
                                        desc_status = json.load(sf)
                                    video_data["desc_status"] = desc_status.get("status", "")
                                    video_data["desc_progress"] = desc_status.get("progress", "")
                                except (json.JSONDecodeError, KeyError):
                                    pass

                            if descriptions and not video_data.get("desc_status"):
                                video_data["desc_status"] = "done"
                            video_data["desc_count"] = len(descriptions)

                            for clip in meta.get("clips", []):
                                clip_filename = clip["filename"]
                                clip_stem = clip_filename.replace(".mp4", "")
                                clip_entry = {
                                    "filename": clip_filename,
                                    "url": f"/games/{quote(game_name)}/videos/{quote(coll_name)}/clips/{quote(f.stem)}/{quote(clip_filename)}?v={cache_bust}",
                                    "poster_url": f"/games/{quote(game_name)}/videos/{quote(coll_name)}/clips/{quote(f.stem)}/posters/{quote(clip_stem)}.jpg?v={cache_bust}",
                                    "start_sec": clip.get("start_sec", 0),
                                    "end_sec": clip.get("end_sec", 0),
                                    "duration_sec": clip.get("duration_sec", 0),
                                    "index": clip.get("index", 0),
                                }
                                # Attach description preview if available
                                clip_desc = descriptions.get(clip_filename)
                                if clip_desc:
                                    clip_entry["has_description"] = True
                                    desc_text = clip_desc.get("description", "")
                                    clip_entry["description_preview"] = desc_text[:150] + ("..." if len(desc_text) > 150 else "")
                                else:
                                    clip_entry["has_description"] = False
                                # Check if clip is used in game TOML
                                video_path = f"{coll_name}/clips/{f.stem}/{clip_filename}"
                                clip_entry["used_in_game"] = video_path in used_paths
                                video_data["clips"].append(clip_entry)
                            video_data["used_clip_count"] = sum(
                                1 for c in video_data["clips"] if c.get("used_in_game")
                            )
                    except (json.JSONDecodeError, KeyError):
                        pass

                videos.append(video_data)

            # Discover orphaned clip directories (source video deleted)
            clips_root = real_dir / "clips"
            if clips_root.exists() and clips_root.is_dir():
                discovered_stems = {v["stem"] for v in videos}
                for clip_dir in sorted(clips_root.iterdir()):
                    if not clip_dir.is_dir() or clip_dir.name in discovered_stems:
                        continue
                    clips_json_path = clip_dir / "clips.json"
                    if not clips_json_path.exists():
                        continue
                    try:
                        with open(clips_json_path) as jf:
                            meta = json.load(jf)
                    except (json.JSONDecodeError, KeyError):
                        continue
                    if meta.get("status"):
                        continue  # Skip processing/error with no real clips

                    source_filename = meta.get("source_video", clip_dir.name + ".mp4")
                    orphan = {
                        "filename": source_filename,
                        "stem": clip_dir.name,
                        "url": "",
                        "source_deleted": True,
                        "clips": [],
                        "duration": meta.get("total_duration_sec"),
                        "resolution": meta.get("resolution"),
                        "fps": meta.get("fps"),
                    }

                    # Load descriptions
                    descriptions = {}
                    desc_file = clip_dir / "descriptions.json"
                    if desc_file.exists():
                        try:
                            with open(desc_file) as df:
                                desc_data = json.load(df)
                            descriptions = desc_data.get("results", {})
                        except (json.JSONDecodeError, KeyError):
                            pass

                    desc_status_file = clip_dir / "desc_status.json"
                    if desc_status_file.exists():
                        try:
                            with open(desc_status_file) as sf:
                                desc_status = json.load(sf)
                            orphan["desc_status"] = desc_status.get("status", "")
                            orphan["desc_progress"] = desc_status.get("progress", "")
                        except (json.JSONDecodeError, KeyError):
                            pass

                    if descriptions and not orphan.get("desc_status"):
                        orphan["desc_status"] = "done"
                    orphan["desc_count"] = len(descriptions)

                    for clip in meta.get("clips", []):
                        clip_filename = clip["filename"]
                        clip_stem = clip_filename.replace(".mp4", "")
                        clip_entry = {
                            "filename": clip_filename,
                            "url": f"/games/{quote(game_name)}/videos/{quote(coll_name)}/clips/{quote(clip_dir.name)}/{quote(clip_filename)}?v={cache_bust}",
                            "poster_url": f"/games/{quote(game_name)}/videos/{quote(coll_name)}/clips/{quote(clip_dir.name)}/posters/{quote(clip_stem)}.jpg?v={cache_bust}",
                            "start_sec": clip.get("start_sec", 0),
                            "end_sec": clip.get("end_sec", 0),
                            "duration_sec": clip.get("duration_sec", 0),
                            "index": clip.get("index", 0),
                        }
                        clip_desc = descriptions.get(clip_filename)
                        if clip_desc:
                            clip_entry["has_description"] = True
                            desc_text = clip_desc.get("description", "")
                            clip_entry["description_preview"] = desc_text[:150] + ("..." if len(desc_text) > 150 else "")
                        else:
                            clip_entry["has_description"] = False
                        video_path = f"{coll_name}/clips/{clip_dir.name}/{clip_filename}"
                        clip_entry["used_in_game"] = video_path in used_paths
                        orphan["clips"].append(clip_entry)

                    orphan["used_clip_count"] = sum(
                        1 for c in orphan["clips"] if c.get("used_in_game")
                    )
                    videos.append(orphan)

            if videos:
                collections.append({"name": coll_name, "videos": videos})

        if collections:
            games.append({"name": game_name, "collections": collections})

    return JsonResponse({"games": games})


@csrf_exempt
@require_POST
def delete_clip(request):
    """Delete a clip file, its poster, and update clips.json."""
    body = _parse_body(request)
    game = body.get("game", "")
    collection = body.get("collection", "")
    video_stem = body.get("video_stem", "")
    clip_filename = body.get("clip_filename", "")

    if not all([game, collection, video_stem, clip_filename]):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    try:
        clips_dir = validate_path(GAMES_ROOT, game, "videos", collection, "clips", video_stem)
        clip_path = validate_path(GAMES_ROOT, game, "videos", collection, "clips", video_stem, clip_filename)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    if not clip_path.exists():
        return JsonResponse({"error": "Clip not found"}, status=404)

    clip_path.unlink()

    poster_name = clip_filename.replace(".mp4", ".jpg")
    poster_path = clips_dir / "posters" / poster_name
    if poster_path.exists():
        poster_path.unlink()

    source_video = ""
    existing_json = clips_dir / "clips.json"
    if existing_json.exists():
        try:
            with open(existing_json) as f:
                source_video = json.load(f).get("source_video", "")
        except Exception:
            pass

    clips_data = renumber_clips(clips_dir)
    rebuild_clips_json(clips_dir, clips_data, source_video)

    return JsonResponse({"success": True, "clips_remaining": len(clips_data)})


@csrf_exempt
@require_POST
def split_clip(request):
    """Split a clip into 2-3 parts at the given start/end times."""
    body = _parse_body(request)
    game = body.get("game", "")
    collection = body.get("collection", "")
    video_stem = body.get("video_stem", "")
    clip_filename = body.get("clip_filename", "")
    start_time = body.get("start_time")
    end_time = body.get("end_time")

    if not all([game, collection, video_stem, clip_filename]):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    try:
        start_time = float(start_time)
        end_time = float(end_time)
    except (TypeError, ValueError):
        return JsonResponse({"error": "start_time and end_time must be numbers"}, status=400)

    if start_time < 0 or start_time >= end_time:
        return JsonResponse({"error": "Invalid time range"}, status=400)

    try:
        clips_dir = validate_path(GAMES_ROOT, game, "videos", collection, "clips", video_stem)
        clip_path = validate_path(GAMES_ROOT, game, "videos", collection, "clips", video_stem, clip_filename)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    if not clip_path.exists():
        return JsonResponse({"error": "Clip not found"}, status=404)

    ffmpeg_cmd = find_ffmpeg()
    if not ffmpeg_cmd:
        return JsonResponse({"error": "FFmpeg not found"}, status=500)

    try:
        _, _, duration = probe_metadata(str(clip_path))
    except Exception as e:
        return JsonResponse({"error": f"Failed to read clip: {e}"}, status=500)

    if end_time > duration:
        end_time = duration

    segments = []
    if start_time > 0.1:
        segments.append((0.0, start_time))
    segments.append((start_time, end_time))
    if (duration - end_time) > 0.1:
        segments.append((end_time, duration))

    if len(segments) < 2:
        return JsonResponse({"error": "No split needed (covers full clip)"}, status=400)

    temp_files = []
    try:
        for i, (seg_start, seg_end) in enumerate(segments):
            temp_path = clips_dir / f"__split_temp_{i:03d}.mp4"
            seg_duration = seg_end - seg_start
            cmd = [
                ffmpeg_cmd, "-y",
                "-i", str(clip_path),
                "-ss", str(seg_start),
                "-t", str(seg_duration),
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "18",
                "-c:a", "aac",
                "-b:a", "128k",
                str(temp_path),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                for tf in temp_files:
                    if tf.exists():
                        tf.unlink()
                return JsonResponse(
                    {"error": f"FFmpeg failed: {result.stderr[:300]}"},
                    status=500,
                )
            temp_files.append(temp_path)

    except subprocess.TimeoutExpired:
        for tf in temp_files:
            if tf.exists():
                tf.unlink()
        return JsonResponse({"error": "FFmpeg timed out"}, status=500)

    clip_path.unlink()
    poster_name = clip_filename.replace(".mp4", ".jpg")
    poster_path = clips_dir / "posters" / poster_name
    if poster_path.exists():
        poster_path.unlink()

    base_index = clip_filename.replace("clip_", "").replace(".mp4", "")
    for i, temp_path in enumerate(temp_files):
        insert_name = f"clip_{base_index}_{chr(97 + i)}.mp4"
        temp_path.rename(clips_dir / insert_name)

    source_video = ""
    existing_json = clips_dir / "clips.json"
    if existing_json.exists():
        try:
            with open(existing_json) as f:
                source_video = json.load(f).get("source_video", "")
        except Exception:
            pass

    clips_data = renumber_clips(clips_dir)

    posters_dir = clips_dir / "posters"
    posters_dir.mkdir(exist_ok=True)
    for clip in clips_data:
        poster_path = posters_dir / clip["filename"].replace(".mp4", ".jpg")
        if not poster_path.exists():
            clip_file = clips_dir / clip["filename"]
            extract_frame(str(clip_file), 0.1, poster_path)

    rebuild_clips_json(clips_dir, clips_data, source_video)

    return JsonResponse({"success": True, "segments_created": len(segments), "total_clips": len(clips_data)})


@csrf_exempt
@require_POST
def remove_audio(request):
    """Remove the audio track from a clip, keeping video intact (no re-encode)."""
    body = _parse_body(request)
    game = body.get("game", "")
    collection = body.get("collection", "")
    video_stem = body.get("video_stem", "")
    clip_filename = body.get("clip_filename", "")

    if not all([game, collection, video_stem, clip_filename]):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    try:
        clips_dir = validate_path(GAMES_ROOT, game, "videos", collection, "clips", video_stem)
        clip_path = validate_path(GAMES_ROOT, game, "videos", collection, "clips", video_stem, clip_filename)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    if not clip_path.exists():
        return JsonResponse({"error": "Clip not found"}, status=404)

    ffmpeg_cmd = find_ffmpeg()
    if not ffmpeg_cmd:
        return JsonResponse({"error": "FFmpeg not found"}, status=500)

    temp_path = clips_dir / "__temp_noaudio.mp4"
    try:
        cmd = [
            ffmpeg_cmd, "-y",
            "-i", str(clip_path),
            "-c:v", "copy",
            "-an",
            str(temp_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            if temp_path.exists():
                temp_path.unlink()
            return JsonResponse({"error": f"FFmpeg failed: {result.stderr[:300]}"}, status=500)

        temp_path.rename(clip_path)
        return JsonResponse({"success": True})

    except subprocess.TimeoutExpired:
        if temp_path.exists():
            temp_path.unlink()
        return JsonResponse({"error": "FFmpeg timed out"}, status=500)


def _run_generate(video_path: Path, output_dir: Path):
    """Background thread target: run scene detection + clip splitting."""
    try:
        process_single_video(
            video_path=video_path,
            output_dir=output_dir,
            posters=True,
            stdout=None,
        )
    except Exception as e:
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_dir / "clips.json", "w") as f:
            json.dump({"status": "error", "error": str(e)}, f, indent=2)


@csrf_exempt
@require_POST
def generate_clips(request):
    """Force (re)generate clips for a video using scene detection. Runs async."""
    body = _parse_body(request)
    game = body.get("game", "")
    collection = body.get("collection", "")
    video_stem = body.get("video_stem", "")

    if not all([game, collection, video_stem]):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    try:
        coll_dir = validate_path(GAMES_ROOT, game, "videos", collection)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    # Find the video file (try each extension)
    video_path = None
    for ext in VIDEO_EXTENSIONS:
        candidate = coll_dir / f"{video_stem}{ext}"
        if candidate.exists():
            video_path = candidate
            break
    if not video_path:
        return JsonResponse({"error": f"Video file not found for stem: {video_stem}"}, status=404)

    output_dir = coll_dir / "clips" / video_stem

    # Check if already processing
    clips_json = output_dir / "clips.json"
    if clips_json.exists():
        try:
            with open(clips_json) as f:
                meta = json.load(f)
            if meta.get("status") == "processing":
                return JsonResponse({"error": "Already processing"}, status=409)
        except (json.JSONDecodeError, KeyError):
            pass

    # Delete existing clips folder
    if output_dir.exists():
        shutil.rmtree(output_dir)

    # Write processing status
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(clips_json, "w") as f:
        json.dump({"status": "processing", "started_at": int(time.time())}, f, indent=2)

    # Spawn background thread
    thread = threading.Thread(target=_run_generate, args=(video_path, output_dir), daemon=True)
    thread.start()

    return JsonResponse({"success": True, "status": "processing"})


# =============================================================================
# AI Description Generation (via Modal Qwen-VL)
# =============================================================================

MODEL_ID_FALLBACK = "huihui-ai/Huihui-Qwen3-VL-8B-Instruct-abliterated"


MODAL_APP_NAME = "qwen-vl-video-captioner"


def _stop_modal_app():
    """Stop the Modal app via CLI (no Python API available)."""
    try:
        result = subprocess.run(
            ["modal", "app", "stop", MODAL_APP_NAME],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            print(f"[Describe] Modal app stopped", flush=True)
        else:
            print(f"[Describe] Modal app stop warning: {result.stderr.strip()}", flush=True)
    except Exception as e:
        print(f"[Describe] Failed to stop Modal app: {e}", flush=True)


def _run_describe(clips_dir: Path, chunk_size: int = 5):
    """Background thread: generate AI descriptions for all clips using Modal Qwen-VL."""
    status_file = clips_dir / "desc_status.json"
    desc_file = clips_dir / "descriptions.json"
    deployed_by_us = False

    try:
        # Collect clip files
        clip_files = sorted(clips_dir.glob("clip_*.mp4"))
        total = len(clip_files)
        if total == 0:
            with open(status_file, "w") as f:
                json.dump({"status": "error", "error": "No clip files found"}, f, indent=2)
            return

        # Write initial status
        with open(status_file, "w") as f:
            json.dump({
                "status": "describing",
                "progress": f"0/{total}",
                "started_at": int(time.time()),
            }, f, indent=2)

        # Auto-deploy Modal app if not already running
        import modal
        from modal_qwen_vl.app import app as modal_app, QwenVLCaptioner

        try:
            modal.App.lookup(MODAL_APP_NAME)
            print(f"[Describe] Modal app already deployed", flush=True)
        except modal.exception.NotFoundError:
            print(f"[Describe] Deploying Modal app...", flush=True)
            with open(status_file, "w") as f:
                json.dump({
                    "status": "describing",
                    "progress": "deploying...",
                    "started_at": int(time.time()),
                }, f, indent=2)
            modal_app.deploy()
            deployed_by_us = True
            print(f"[Describe] Modal app deployed", flush=True)

        captioner = QwenVLCaptioner()

        all_results = []
        total_chunks = (total + chunk_size - 1) // chunk_size

        for chunk_start in range(0, total, chunk_size):
            chunk_files = clip_files[chunk_start:chunk_start + chunk_size]
            chunk_num = chunk_start // chunk_size + 1

            print(f"[Describe] Chunk {chunk_num}/{total_chunks}: Reading {len(chunk_files)} clips...", flush=True)

            # Read chunk bytes
            chunk_videos = []
            for cf in chunk_files:
                chunk_videos.append((cf.name, cf.read_bytes()))

            print(f"[Describe] Sending chunk {chunk_num} to Modal...", flush=True)
            results = captioner.caption_batch.remote(chunk_videos)
            all_results.extend(results)

            # Incremental save (crash-safe)
            output_data = {
                "total_videos": len(all_results),
                "model": all_results[0]["model"] if all_results else MODEL_ID_FALLBACK,
                "results": {r["filename"]: r for r in all_results},
            }
            with open(desc_file, "w") as f:
                json.dump(output_data, f, indent=2)

            # Update progress
            with open(status_file, "w") as f:
                json.dump({
                    "status": "describing",
                    "progress": f"{len(all_results)}/{total}",
                    "started_at": int(time.time()),
                }, f, indent=2)

            print(f"[Describe] Chunk {chunk_num} done ({len(all_results)}/{total} total)", flush=True)

        # Done
        total_in = sum(r.get("input_tokens", 0) for r in all_results)
        total_out = sum(r.get("output_tokens", 0) for r in all_results)
        with open(status_file, "w") as f:
            json.dump({
                "status": "done",
                "total": total,
                "input_tokens": total_in,
                "output_tokens": total_out,
            }, f, indent=2)
        print(f"[Describe] Done! {total} clips, {total_in} in / {total_out} out tokens", flush=True)

        # Stop Modal app if we deployed it (save GPU costs)
        if deployed_by_us:
            _stop_modal_app()

    except Exception as e:
        print(f"[Describe] Error: {e}", flush=True)
        with open(status_file, "w") as f:
            json.dump({"status": "error", "error": str(e)}, f, indent=2)
        # Stop Modal app on error too, if we deployed it
        if deployed_by_us:
            _stop_modal_app()


@csrf_exempt
@require_POST
def generate_descriptions(request):
    """Generate AI descriptions for all clips of a video. Runs async via Modal."""
    body = _parse_body(request)
    game = body.get("game", "")
    collection = body.get("collection", "")
    video_stem = body.get("video_stem", "")

    if not all([game, collection, video_stem]):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    try:
        clips_dir = validate_path(GAMES_ROOT, game, "videos", collection, "clips", video_stem)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    if not clips_dir.exists():
        return JsonResponse({"error": "Clips directory not found"}, status=404)

    # Check if already describing
    status_file = clips_dir / "desc_status.json"
    if status_file.exists():
        try:
            with open(status_file) as f:
                status_data = json.load(f)
            if status_data.get("status") == "describing":
                return JsonResponse({"error": "Already describing", "progress": status_data.get("progress", "")}, status=409)
        except (json.JSONDecodeError, KeyError):
            pass

    # Spawn background thread
    thread = threading.Thread(target=_run_describe, args=(clips_dir,), daemon=True)
    thread.start()

    return JsonResponse({"success": True, "status": "describing"})


@require_GET
def get_description(request):
    """Get full description for a single clip."""
    game = request.GET.get("game", "")
    collection = request.GET.get("collection", "")
    video_stem = request.GET.get("video_stem", "")
    clip_filename = request.GET.get("clip_filename", "")

    if not all([game, collection, video_stem, clip_filename]):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    try:
        clips_dir = validate_path(GAMES_ROOT, game, "videos", collection, "clips", video_stem)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    desc_file = clips_dir / "descriptions.json"
    if not desc_file.exists():
        return JsonResponse({"error": "No descriptions file found"}, status=404)

    try:
        with open(desc_file) as f:
            data = json.load(f)
        result = data.get("results", {}).get(clip_filename)
        if not result:
            return JsonResponse({"error": "No description for this clip"}, status=404)
        return JsonResponse(result)
    except (json.JSONDecodeError, KeyError) as e:
        return JsonResponse({"error": f"Failed to read descriptions: {e}"}, status=500)


@csrf_exempt
@require_POST
def cleanup_source(request):
    """Delete the original source video after clips and descriptions are done."""
    body = _parse_body(request)
    game = body.get("game", "")
    collection = body.get("collection", "")
    video_stem = body.get("video_stem", "")

    if not all([game, collection, video_stem]):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    try:
        coll_dir = validate_path(GAMES_ROOT, game, "videos", collection)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    # Find the video file
    video_path = None
    for ext in VIDEO_EXTENSIONS:
        candidate = coll_dir / f"{video_stem}{ext}"
        if candidate.exists():
            video_path = candidate
            break
    if not video_path:
        return JsonResponse({"error": f"Source video not found for stem: {video_stem}"}, status=404)

    # Safety: require descriptions to be done before allowing cleanup
    clips_dir = coll_dir / "clips" / video_stem
    desc_status_file = clips_dir / "desc_status.json"
    if not desc_status_file.exists():
        return JsonResponse({"error": "Descriptions not yet generated"}, status=400)

    try:
        with open(desc_status_file) as f:
            desc_status = json.load(f)
        if desc_status.get("status") != "done":
            return JsonResponse({"error": f"Descriptions not complete (status: {desc_status.get('status')})"}, status=400)
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({"error": "Cannot read description status"}, status=500)

    file_size_mb = video_path.stat().st_size / (1024 * 1024)

    try:
        video_path.unlink()
    except OSError as e:
        return JsonResponse({"error": f"Failed to delete: {e}"}, status=500)

    return JsonResponse({
        "success": True,
        "deleted": video_path.name,
        "freed_mb": round(file_size_mb, 1),
    })


# =============================================================================
# HTML Page
# =============================================================================

def page(request):
    """Serve the video browser HTML page."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Video Browser</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f0f0f; color: #e0e0e0; display: flex; height: 100vh; overflow: hidden; }

/* Sidebar */
#sidebar { width: 240px; background: #1a1a1a; border-right: 1px solid #333; overflow-y: auto; flex-shrink: 0; }
#sidebar h2 { padding: 16px; font-size: 14px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
.game-item { padding: 8px 16px; cursor: pointer; border-left: 3px solid transparent; transition: all 0.15s; font-size: 14px; font-weight: 600; color: #ccc; }
.game-item:hover { background: #252525; }
.game-item.active { background: #252525; border-left-color: #e44; color: #fff; }
.game-count { color: #666; font-size: 12px; margin-left: 4px; font-weight: 400; }
.coll-list { padding-left: 12px; display: none; }
.coll-list.open { display: block; }
.coll-item { padding: 6px 16px; cursor: pointer; border-left: 3px solid transparent; transition: all 0.15s; font-size: 13px; color: #aaa; }
.coll-item:hover { background: #252525; color: #ddd; }
.coll-item.active { background: #2a2225; border-left-color: #e88; color: #fff; }
.coll-count { color: #666; font-size: 11px; margin-left: 4px; }

/* Main */
#main { flex: 1; overflow-y: auto; padding: 20px; }
#main h1 { font-size: 20px; margin-bottom: 16px; color: #fff; }
.loading { color: #666; padding: 40px; text-align: center; }
.breadcrumb { font-size: 13px; color: #666; margin-bottom: 12px; }
.breadcrumb span { color: #aaa; cursor: pointer; }
.breadcrumb span:hover { color: #fff; }

/* Video card */
.video-card { background: #1a1a1a; border-radius: 8px; margin-bottom: 16px; overflow: hidden; }
.video-header { padding: 12px 16px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #252525; }
.video-header:hover { background: #222; }
.video-title { font-size: 14px; font-weight: 600; }
.video-meta { font-size: 12px; color: #888; }
.video-body { display: none; padding: 16px; }
.video-body.open { display: block; }
.source-player { width: 100%; max-width: 640px; border-radius: 4px; background: #000; }

/* Clips grid */
.clips-label { font-size: 13px; color: #888; margin: 16px 0 8px; text-transform: uppercase; letter-spacing: 0.5px; }
.clips-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }

/* Clip card */
.clip-card { background: #222; border-radius: 6px; overflow: hidden; position: relative; }
.clip-top { display: flex; justify-content: space-between; align-items: center; padding: 6px 10px; background: #2a2a2a; font-size: 12px; }
.clip-duration { color: #aaa; }
.btn-del { background: none; border: none; color: #e44; cursor: pointer; font-size: 13px; padding: 2px 6px; border-radius: 3px; }
.btn-del:hover { background: #e4433020; }
.clip-video { width: 100%; display: block; background: #000; }
.clip-controls { padding: 8px 10px; display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
.clip-controls label { font-size: 11px; color: #888; min-width: 32px; }
.clip-controls input[type=number] { width: 70px; background: #1a1a1a; border: 1px solid #444; color: #e0e0e0; padding: 3px 6px; border-radius: 3px; font-size: 12px; font-family: monospace; }
.btn-set { background: #333; border: 1px solid #555; color: #ccc; cursor: pointer; padding: 3px 8px; border-radius: 3px; font-size: 11px; }
.btn-set:hover { background: #444; }
.btn-split { background: #e44; border: none; color: #fff; cursor: pointer; padding: 5px 14px; border-radius: 4px; font-size: 12px; font-weight: 600; margin-top: 4px; width: 100%; }
.btn-split:hover { background: #c33; }
.btn-split:disabled { background: #555; color: #888; cursor: not-allowed; }
.btn-generate { background: #2563eb; border: none; color: #fff; cursor: pointer; padding: 4px 12px; border-radius: 4px; font-size: 12px; margin-left: 8px; }
.btn-generate:hover { background: #1d4ed8; }
.btn-generate:disabled { background: #555; color: #888; cursor: not-allowed; }
.processing-msg { padding: 20px; text-align: center; color: #888; font-size: 14px; }
.processing-msg .spinner { display: inline-block; width: 16px; height: 16px; border: 2px solid #555; border-top-color: #2563eb; border-radius: 50%; animation: spin 0.8s linear infinite; margin-right: 8px; vertical-align: middle; }
@keyframes spin { to { transform: rotate(360deg); } }
.error-msg { padding: 12px 16px; background: #2a1a1a; border: 1px solid #e44; border-radius: 6px; color: #e88; font-size: 13px; margin: 8px 0; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 10000; display: flex; align-items: center; justify-content: center; }
.modal-box { background: #1a1a1a; border: 1px solid #333; border-radius: 10px; padding: 24px; max-width: 400px; width: 90%; }
.modal-box h3 { font-size: 16px; color: #fff; margin-bottom: 8px; }
.modal-box p { font-size: 13px; color: #aaa; margin-bottom: 20px; line-height: 1.5; }
.modal-box .modal-warn { color: #e44; font-weight: 600; }
.modal-actions { display: flex; gap: 10px; justify-content: flex-end; }
.modal-actions button { padding: 8px 20px; border-radius: 6px; border: none; cursor: pointer; font-size: 13px; font-weight: 600; }
.modal-cancel { background: #333; color: #ccc; }
.modal-cancel:hover { background: #444; }
.modal-confirm { background: #e44; color: #fff; }
.modal-confirm:hover { background: #c33; }

/* Description UI */
.btn-describe { background: #0d9488; border: none; color: #fff; cursor: pointer; padding: 4px 12px; border-radius: 4px; font-size: 12px; margin-left: 6px; }
.btn-describe:hover { background: #0f766e; }
.btn-describe:disabled { background: #555; color: #888; cursor: not-allowed; }
.btn-cleanup { background: #dc2626; border: none; color: #fff; cursor: pointer; padding: 4px 12px; border-radius: 4px; font-size: 12px; margin-left: 6px; }
.btn-cleanup:hover { background: #b91c1c; }
.btn-cleanup:disabled { background: #555; color: #888; cursor: not-allowed; }
.source-deleted-msg { padding: 12px 16px; background: #1a1a2a; border: 1px solid #4a4a6a; border-radius: 6px; color: #8888cc; font-size: 13px; margin-bottom: 12px; }
.desc-section { padding: 6px 10px 8px; border-top: 1px solid #2a2a2a; }
.desc-badge { display: inline-block; background: #16a34a; color: #fff; font-size: 10px; padding: 1px 6px; border-radius: 8px; margin-right: 6px; vertical-align: middle; }
.used-badge { display: inline-block; background: #22c55e; color: #fff; font-size: 9px; padding: 1px 5px; border-radius: 8px; margin-left: 4px; vertical-align: middle; }
.unused-badge { display: inline-block; background: #555; color: #999; font-size: 9px; padding: 1px 5px; border-radius: 8px; margin-left: 4px; vertical-align: middle; }
.video-usage { font-size: 12px; margin-left: 8px; }
.video-usage.all-used { color: #4ade80; }
.video-usage.partial-used { color: #fbbf24; }
.video-usage.none-used { color: #888; }
.desc-preview { font-size: 11px; color: #888; font-style: italic; line-height: 1.4; cursor: pointer; margin-top: 4px; }
.desc-preview:hover { color: #bbb; }
.modal-desc { max-width: 700px; max-height: 80vh; display: flex; flex-direction: column; }
.modal-desc h3 { font-size: 15px; color: #fff; margin-bottom: 12px; }
.modal-desc-body { font-size: 13px; color: #ccc; line-height: 1.7; overflow-y: auto; max-height: 60vh; white-space: pre-wrap; margin-bottom: 16px; }
.modal-desc-footer { font-size: 11px; color: #666; border-top: 1px solid #333; padding-top: 8px; }
.describing-msg { padding: 8px 10px; font-size: 12px; color: #0d9488; }
.describing-msg .spinner { display: inline-block; width: 12px; height: 12px; border: 2px solid #555; border-top-color: #0d9488; border-radius: 50%; animation: spin 0.8s linear infinite; margin-right: 6px; vertical-align: middle; }

/* Toast */
.toast { position: fixed; bottom: 20px; right: 20px; padding: 10px 16px; border-radius: 6px; color: #fff; font-size: 13px; z-index: 9999; animation: slideIn 0.3s; }
.toast.success { background: #16a34a; }
.toast.error { background: #dc2626; }
@keyframes slideIn { from { transform: translateX(100px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }

/* Mute toggle */
#sidebar h2 { display: flex; justify-content: space-between; align-items: center; }
.mute-toggle { background: none; border: 1px solid #444; color: #aaa; cursor: pointer; padding: 2px 8px; border-radius: 4px; font-size: 16px; line-height: 1; }
.mute-toggle:hover { background: #333; color: #fff; }
.mute-toggle.muted { color: #e44; border-color: #e44; }
</style>
</head>
<body>

<div id="sidebar">
  <h2>Games <button class="mute-toggle" id="mute-btn" onclick="toggleMute()" title="Toggle audio"></button></h2>
  <div id="game-list"><div class="loading">Loading...</div></div>
  <div style="padding:12px 16px;border-top:1px solid #333;margin-top:8px"><a href="/api/v1/dev/game-review/" style="color:#6b8afd;font-size:12px;text-decoration:none">Game Review &rarr;</a></div>
</div>

<div id="main">
  <div class="loading">Select a game</div>
</div>

<script>
const API = '/api/v1/dev/video-browser';
let DATA = null;
let CUR_GAME = null;
let CUR_COLL = null;
let AUDIO_MUTED = localStorage.getItem('videoMuted') === 'true';

function toggleMute() {
  AUDIO_MUTED = !AUDIO_MUTED;
  localStorage.setItem('videoMuted', AUDIO_MUTED);
  document.querySelectorAll('video').forEach(v => v.muted = AUDIO_MUTED);
  updateMuteBtn();
}

function updateMuteBtn() {
  const btn = document.getElementById('mute-btn');
  if (!btn) return;
  btn.textContent = AUDIO_MUTED ? '\\u{1F507}' : '\\u{1F50A}';
  btn.classList.toggle('muted', AUDIO_MUTED);
  btn.title = AUDIO_MUTED ? 'Unmute audio' : 'Mute audio';
}


async function loadData() {
  const res = await fetch(API + '/scan');
  DATA = await res.json();
  renderSidebar();
  if (DATA.games.length === 1) {
    selectGame(DATA.games[0].name);
    if (DATA.games[0].collections.length === 1) {
      selectCollection(DATA.games[0].name, DATA.games[0].collections[0].name);
    }
  }
}

function renderSidebar() {
  const el = document.getElementById('game-list');
  el.innerHTML = DATA.games.map(g => {
    const totalColls = g.collections.length;
    const collsHtml = g.collections.map(c => {
      const totalClips = c.videos.reduce((s, v) => s + v.clips.length, 0);
      const usedClips = c.videos.reduce((s, v) => s + (v.used_clip_count || 0), 0);
      const usageTxt = totalClips > 0 ? ' \u2014 ' + usedClips + ' used' : '';
      return '<div class="coll-item" data-game="' + esc(g.name) + '" data-name="' + esc(c.name) + '" onclick="selectCollection(\\'' + esc(g.name) + '\\',\\'' + esc(c.name) + '\\')">' + esc(c.name) + '<span class="coll-count">(' + totalClips + usageTxt + ')</span></div>';
    }).join('');
    return '<div class="game-item" data-name="' + esc(g.name) + '" onclick="selectGame(\\'' + esc(g.name) + '\\')">' + esc(g.name) + '<span class="game-count">(' + totalColls + ')</span></div><div class="coll-list" data-game="' + esc(g.name) + '">' + collsHtml + '</div>';
  }).join('');
}

function selectGame(name) {
  CUR_GAME = name;
  CUR_COLL = null;
  document.querySelectorAll('.game-item').forEach(el => {
    el.classList.toggle('active', el.dataset.name === name);
  });
  document.querySelectorAll('.coll-list').forEach(el => {
    el.classList.toggle('open', el.dataset.game === name);
  });
  document.querySelectorAll('.coll-item').forEach(el => {
    el.classList.remove('active');
  });
  const game = DATA.games.find(g => g.name === name);
  if (!game) return;
  const main = document.getElementById('main');
  let html = '<h1>' + esc(name) + '</h1>';
  html += '<p style="color:#888;margin-bottom:16px">' + game.collections.length + ' collection(s). Select one from the sidebar.</p>';
  game.collections.forEach(c => {
    const totalClips = c.videos.reduce((s, v) => s + v.clips.length, 0);
    html += '<div style="background:#1a1a1a;padding:12px 16px;border-radius:6px;margin-bottom:8px;cursor:pointer" onclick="selectCollection(\\'' + esc(name) + '\\',\\'' + esc(c.name) + '\\')">';
    html += '<span style="font-weight:600">' + esc(c.name) + '</span>';
    html += '<span style="color:#888;margin-left:8px;font-size:13px">' + c.videos.length + ' videos, ' + totalClips + ' clips</span>';
    html += '</div>';
  });
  main.innerHTML = html;
}

function selectCollection(gameName, collName) {
  CUR_GAME = gameName;
  CUR_COLL = collName;
  document.querySelectorAll('.game-item').forEach(el => {
    el.classList.toggle('active', el.dataset.name === gameName);
  });
  document.querySelectorAll('.coll-list').forEach(el => {
    el.classList.toggle('open', el.dataset.game === gameName);
  });
  document.querySelectorAll('.coll-item').forEach(el => {
    el.classList.toggle('active', el.dataset.game === gameName && el.dataset.name === collName);
  });
  const game = DATA.games.find(g => g.name === gameName);
  if (!game) return;
  const coll = game.collections.find(c => c.name === collName);
  if (!coll) return;
  renderMain(gameName, coll);
}

function renderMain(gameName, coll) {
  const main = document.getElementById('main');
  const totalClips = coll.videos.reduce((s, v) => s + v.clips.length, 0);
  const totalUsed = coll.videos.reduce((s, v) => s + (v.used_clip_count || 0), 0);
  let html = '<div class="breadcrumb"><span onclick="selectGame(\\'' + esc(gameName) + '\\')">' + esc(gameName) + '</span> / ' + esc(coll.name) + '</div>';
  html += '<h1>' + esc(coll.name) + ' <span style="color:#888;font-size:14px">' + coll.videos.length + ' videos, ' + totalClips + ' clips (' + totalUsed + ' used in game)</span></h1>';

  coll.videos.forEach((video, vi) => {
    const metaParts = [];
    if (video.duration) metaParts.push(fmtTime(video.duration));
    if (video.resolution) metaParts.push(video.resolution.width + 'x' + video.resolution.height);
    metaParts.push(video.clips.length + ' clips');
    const usedCount = video.used_clip_count || 0;
    const totalCount = video.clips.length;
    if (totalCount > 0) {
      const usageCls = usedCount === totalCount ? 'all-used' : (usedCount > 0 ? 'partial-used' : 'none-used');
      metaParts.push('<span class="video-usage ' + usageCls + '">' + usedCount + '/' + totalCount + ' used</span>');
    }

    html += '<div class="video-card">';
    const isProcessing = video.clip_status === 'processing';
    const isError = video.clip_status === 'error';
    const isDescribing = video.desc_status === 'describing';
    const hasDescriptions = video.desc_status === 'done';
    const sourceDeleted = !!video.source_deleted;
    const genBtnDisabled = (isProcessing || hasDescriptions || sourceDeleted) ? ' disabled' : '';
    const genBtnText = isProcessing ? 'Processing...' : 'Force Generate';
    const descBtnDisabled = (isDescribing || isProcessing || video.clips.length === 0 || hasDescriptions) ? ' disabled' : '';
    const descBtnText = isDescribing ? 'Describing ' + (video.desc_progress || '') + '...' : (video.desc_count > 0 ? 'Re-Describe All' : 'Describe All');

    html += '<div class="video-header">';
    html += '<span class="video-title" style="cursor:pointer" onclick="toggleVideo(' + vi + ')">' + esc(video.filename) + (sourceDeleted ? ' <span style="color:#888;font-size:11px">(source deleted)</span>' : '') + '</span>';
    html += '<span>';
    html += '<span class="video-meta" style="cursor:pointer" onclick="toggleVideo(' + vi + ')">' + metaParts.join(' | ') + '</span>';
    html += '<button class="btn-generate"' + genBtnDisabled + ' onclick="event.stopPropagation();generateClips(\\'' + esc(gameName) + '\\',\\'' + esc(coll.name) + '\\',\\'' + esc(video.stem) + '\\',this)">' + genBtnText + '</button>';
    html += '<button class="btn-describe"' + descBtnDisabled + ' onclick="event.stopPropagation();describeClips(\\'' + esc(gameName) + '\\',\\'' + esc(coll.name) + '\\',\\'' + esc(video.stem) + '\\',this)">' + descBtnText + '</button>';
    if (hasDescriptions && !sourceDeleted) {
      html += '<button class="btn-cleanup" onclick="event.stopPropagation();cleanupSource(\\'' + esc(gameName) + '\\',\\'' + esc(coll.name) + '\\',\\'' + esc(video.stem) + '\\',this)">Cleanup Source</button>';
    }
    html += '</span>';
    html += '</div>';
    html += '<div class="video-body" id="vbody-' + vi + '">';
    if (sourceDeleted) {
      html += '<div class="source-deleted-msg">Source video deleted. ' + video.clips.length + ' clips preserved.</div>';
    } else {
      html += '<video class="source-player" controls preload="none" src="' + video.url + '"' + (AUDIO_MUTED ? ' muted' : '') + '></video>';
    }

    if (isProcessing) {
      html += '<div class="processing-msg"><span class="spinner"></span>Generating clips... This may take a minute.</div>';
      if (!pollTimer) startPolling();
    } else if (isError) {
      html += '<div class="error-msg">Generation failed: ' + esc(video.clip_error || 'Unknown error') + '</div>';
      html += '<div class="clips-label">Clips (' + video.clips.length + ')</div>';
      html += '<div class="clips-grid">';
      html += '</div>';
    } else {
      if (isDescribing) {
        html += '<div class="describing-msg"><span class="spinner"></span>Generating AI descriptions... ' + (video.desc_progress || '') + '</div>';
        if (!pollTimer) startPolling();
      }
      html += '<div class="clips-label">Clips (' + video.clips.length + ')' + (video.desc_count > 0 ? ' &mdash; ' + video.desc_count + ' described' : '') + '</div>';
      html += '<div class="clips-grid" id="clips-' + vi + '">';
      video.clips.forEach((clip, ci) => {
        const cid = vi + '-' + ci;
        html += renderClipCard(clip, cid, gameName, coll.name, video.stem, hasDescriptions);
      });
      html += '</div>';
    }

    html += '</div></div>';
  });

  main.innerHTML = html;
}

function renderClipCard(clip, cid, game, collection, videoStem, locked) {
  const splitDisabled = locked ? ' disabled' : '';
  let html = '<div class="clip-card" id="card-' + cid + '">' +
    '<div class="clip-top">' +
    '<span>' + esc(clip.filename) + ' <span class="clip-duration">(' + clip.duration_sec.toFixed(1) + 's)</span>' +
    (clip.has_description ? '<span class="desc-badge">AI</span>' : '') +
    (clip.used_in_game ? '<span class="used-badge">Used</span>' : '<span class="unused-badge">Unused</span>') +
    '</span>' +
    '<button class="btn-del" onclick="removeAudio(\\'' + esc(game) + '\\',\\'' + esc(collection) + '\\',\\'' + esc(videoStem) + '\\',\\'' + esc(clip.filename) + '\\')" title="Remove audio">NoAud</button>' +
    '<button class="btn-del"' + splitDisabled + ' onclick="deleteClip(\\'' + esc(game) + '\\',\\'' + esc(collection) + '\\',\\'' + esc(videoStem) + '\\',\\'' + esc(clip.filename) + '\\')" title="Delete clip">Del</button>' +
    '</div>' +
    '<video class="clip-video" id="video-' + cid + '" controls preload="none" poster="' + clip.poster_url + '" src="' + clip.url + '"' + (AUDIO_MUTED ? ' muted' : '') + '></video>' +
    '<div class="clip-controls">' +
    '<label>Start</label>' +
    '<input type="number" id="start-' + cid + '" value="0" step="0.1" min="0">' +
    '<button class="btn-set" onclick="setTime(\\'start-' + cid + '\\',\\'video-' + cid + '\\')">Set</button>' +
    '<label>End</label>' +
    '<input type="number" id="end-' + cid + '" value="' + clip.duration_sec.toFixed(2) + '" step="0.1" min="0">' +
    '<button class="btn-set" onclick="setTime(\\'end-' + cid + '\\',\\'video-' + cid + '\\')">Set</button>' +
    '<button class="btn-split"' + splitDisabled + ' onclick="splitClip(\\'' + esc(game) + '\\',\\'' + esc(collection) + '\\',\\'' + esc(videoStem) + '\\',\\'' + esc(clip.filename) + '\\',\\'start-' + cid + '\\',\\'end-' + cid + '\\',this)">Split</button>' +
    '</div>';
  if (clip.has_description) {
    html += '<div class="desc-section">' +
      '<div class="desc-preview" onclick="showDescriptionModal(\\'' + esc(game) + '\\',\\'' + esc(collection) + '\\',\\'' + esc(videoStem) + '\\',\\'' + esc(clip.filename) + '\\')">' +
      esc(clip.description_preview || '') +
      '</div></div>';
  }
  html += '</div>';
  return html;
}

function toggleVideo(vi) {
  document.getElementById('vbody-' + vi).classList.toggle('open');
}

function setTime(inputId, videoId) {
  const video = document.getElementById(videoId);
  const input = document.getElementById(inputId);
  if (video && input) {
    input.value = video.currentTime.toFixed(2);
  }
}

async function deleteClip(game, collection, videoStem, clipFilename) {
  if (!confirm('Delete ' + clipFilename + '?')) return;
  try {
    const res = await fetch(API + '/delete-clip', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({game, collection, video_stem: videoStem, clip_filename: clipFilename}),
    });
    const data = await res.json();
    if (data.success) {
      toast('Deleted. ' + data.clips_remaining + ' clips remaining.', 'success');
      await refresh();
    } else {
      toast(data.error || 'Delete failed', 'error');
    }
  } catch (e) {
    toast('Request failed: ' + e.message, 'error');
  }
}

async function removeAudio(game, collection, videoStem, clipFilename) {
  if (!confirm('Remove audio from ' + clipFilename + '?')) return;
  try {
    const res = await fetch(API + '/remove-audio', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({game, collection, video_stem: videoStem, clip_filename: clipFilename}),
    });
    const data = await res.json();
    if (data.success) {
      toast('Audio removed from ' + clipFilename, 'success');
      await refresh();
    } else {
      toast(data.error || 'Remove audio failed', 'error');
    }
  } catch (e) {
    toast('Request failed: ' + e.message, 'error');
  }
}

async function splitClip(game, collection, videoStem, clipFilename, startId, endId, btn) {
  const startTime = parseFloat(document.getElementById(startId).value);
  const endTime = parseFloat(document.getElementById(endId).value);

  if (isNaN(startTime) || isNaN(endTime) || startTime >= endTime) {
    toast('Invalid time range', 'error');
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Splitting...';

  try {
    const res = await fetch(API + '/split-clip', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({game, collection, video_stem: videoStem, clip_filename: clipFilename, start_time: startTime, end_time: endTime}),
    });
    const data = await res.json();
    if (data.success) {
      toast('Split into ' + data.segments_created + ' parts. ' + data.total_clips + ' total clips.', 'success');
      await refresh();
    } else {
      toast(data.error || 'Split failed', 'error');
      btn.disabled = false;
      btn.textContent = 'Split';
    }
  } catch (e) {
    toast('Request failed: ' + e.message, 'error');
    btn.disabled = false;
    btn.textContent = 'Split';
  }
}

function generateClips(game, collection, videoStem, btn) {
  showModal(
    'Force Generate Clips',
    'This will <span class="modal-warn">delete all existing clips</span> for this video and regenerate them using scene detection. This cannot be undone.',
    async () => {
      btn.disabled = true;
      btn.textContent = 'Starting...';
      try {
        const res = await fetch(API + '/generate-clips', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({game, collection, video_stem: videoStem}),
        });
        const data = await res.json();
        if (data.success) {
          toast('Clip generation started...', 'success');
          await refresh();
        } else {
          toast(data.error || 'Generate failed', 'error');
          btn.disabled = false;
          btn.textContent = 'Force Generate';
        }
      } catch (e) {
        toast('Request failed: ' + e.message, 'error');
        btn.disabled = false;
        btn.textContent = 'Force Generate';
      }
    }
  );
}

function describeClips(game, collection, videoStem, btn) {
  showModal(
    'Generate AI Descriptions',
    'This will send all clips to <strong>Modal Qwen-VL</strong> for AI description generation. Existing descriptions will be overwritten. This may take several minutes.',
    async () => {
      btn.disabled = true;
      btn.textContent = 'Starting...';
      try {
        const res = await fetch(API + '/generate-descriptions', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({game, collection, video_stem: videoStem}),
        });
        const data = await res.json();
        if (data.success) {
          toast('Description generation started...', 'success');
          await refresh();
        } else {
          toast(data.error || 'Describe failed', 'error');
          btn.disabled = false;
          btn.textContent = 'Describe All';
        }
      } catch (e) {
        toast('Request failed: ' + e.message, 'error');
        btn.disabled = false;
        btn.textContent = 'Describe All';
      }
    }
  );
}

function cleanupSource(game, collection, videoStem, btn) {
  showModal(
    'Delete Source Video',
    'This will <span class="modal-warn">permanently delete the original source video</span> for <strong>' + esc(videoStem) + '</strong>. All clips and descriptions will be preserved. This cannot be undone.',
    async () => {
      btn.disabled = true;
      btn.textContent = 'Deleting...';
      try {
        const res = await fetch(API + '/cleanup-source', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({game, collection, video_stem: videoStem}),
        });
        const data = await res.json();
        if (data.success) {
          toast('Deleted ' + data.deleted + ' (' + data.freed_mb + ' MB freed)', 'success');
          await refresh();
        } else {
          toast(data.error || 'Cleanup failed', 'error');
          btn.disabled = false;
          btn.textContent = 'Cleanup Source';
        }
      } catch (e) {
        toast('Request failed: ' + e.message, 'error');
        btn.disabled = false;
        btn.textContent = 'Cleanup Source';
      }
    }
  );
}

async function showDescriptionModal(game, collection, videoStem, clipFilename) {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = '<div class="modal-box modal-desc">' +
    '<h3>' + esc(clipFilename) + '</h3>' +
    '<div class="modal-desc-body">Loading...</div>' +
    '<div class="modal-desc-footer"></div>' +
    '<div class="modal-actions"><button class="modal-cancel">Close</button></div>' +
    '</div>';
  overlay.querySelector('.modal-cancel').onclick = () => overlay.remove();
  overlay.onclick = (e) => { if (e.target === overlay) overlay.remove(); };
  document.body.appendChild(overlay);

  try {
    const params = new URLSearchParams({game, collection, video_stem: videoStem, clip_filename: clipFilename});
    const res = await fetch(API + '/get-description?' + params);
    const data = await res.json();
    if (data.error) {
      overlay.querySelector('.modal-desc-body').textContent = 'Error: ' + data.error;
    } else {
      overlay.querySelector('.modal-desc-body').textContent = data.description || 'No description';
      const tokens = [];
      if (data.input_tokens) tokens.push(data.input_tokens + ' input tokens');
      if (data.output_tokens) tokens.push(data.output_tokens + ' output tokens');
      if (data.model) tokens.push(data.model);
      overlay.querySelector('.modal-desc-footer').textContent = tokens.join(' | ');
    }
  } catch (e) {
    overlay.querySelector('.modal-desc-body').textContent = 'Failed to load: ' + e.message;
  }
}

function showModal(title, bodyHtml, onConfirm) {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = '<div class="modal-box">' +
    '<h3>' + title + '</h3>' +
    '<p>' + bodyHtml + '</p>' +
    '<div class="modal-actions">' +
    '<button class="modal-cancel">Cancel</button>' +
    '<button class="modal-confirm">Confirm</button>' +
    '</div></div>';
  overlay.querySelector('.modal-cancel').onclick = () => overlay.remove();
  overlay.querySelector('.modal-confirm').onclick = () => { overlay.remove(); onConfirm(); };
  overlay.onclick = (e) => { if (e.target === overlay) overlay.remove(); };
  document.body.appendChild(overlay);
}

let pollTimer = null;
function startPolling() {
  if (pollTimer) return;
  pollTimer = setInterval(async () => {
    await refresh();
    const anyBusy = DATA.games.some(g =>
      g.collections.some(c => c.videos.some(v =>
        v.clip_status === 'processing' || v.desc_status === 'describing'
      ))
    );
    if (!anyBusy) {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  }, 3000);
}

async function refresh() {
  const res = await fetch(API + '/scan');
  DATA = await res.json();
  renderSidebar();
  if (CUR_GAME && CUR_COLL) {
    selectCollection(CUR_GAME, CUR_COLL);
  } else if (CUR_GAME) {
    selectGame(CUR_GAME);
  }
}

function toast(msg, type) {
  const el = document.createElement('div');
  el.className = 'toast ' + type;
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 4000);
}

function fmtTime(s) {
  const m = Math.floor(s / 60);
  const sec = Math.floor(s % 60);
  return m + ':' + String(sec).padStart(2, '0');
}

function esc(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML.replace(/'/g, "\\\\'");
}

updateMuteBtn();
loadData();
</script>
</body>
</html>"""
    return HttpResponse(html, content_type="text/html")


# =============================================================================
# URL Patterns
# =============================================================================

urlpatterns = [
    path("", page, name="video_browser_page"),
    path("scan", scan, name="video_browser_scan"),
    path("delete-clip", delete_clip, name="video_browser_delete_clip"),
    path("split-clip", split_clip, name="video_browser_split_clip"),
    path("remove-audio", remove_audio, name="video_browser_remove_audio"),
    path("generate-clips", generate_clips, name="video_browser_generate_clips"),
    path("generate-descriptions", generate_descriptions, name="video_browser_generate_descriptions"),
    path("get-description", get_description, name="video_browser_get_description"),
    path("cleanup-source", cleanup_source, name="video_browser_cleanup_source"),
]
