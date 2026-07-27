#!/usr/bin/env python3
"""Fetch + contact-sheet harness for the media_lab query study.

Ranks the stocked options for one slot by how much its URL slug says about the
beat, downloads the top N, applies fetch sanity, and tiles one representative
frame per survivor into a single contact sheet we Read once.
"""
import json, os, re, subprocess, sys, urllib.request, pathlib, shutil

ROOT = pathlib.Path("games/media_lab/.find-media")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

def rank(url, want, avoid):
    slug = url.rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()
    words = re.split(r"[-_]+", slug)
    descriptive = sum(1 for w in words if len(w) > 2 and not w.isdigit()) >= 2
    s = 0
    for kw in want:
        if kw in slug:
            s += 10
    for kw in avoid:
        if kw in slug or kw in url.lower():   # avoid can name a host, e.g. shutterstock
            s -= 25
    if descriptive:
        s += 3
    # hover-preview mp4s are sampled from a full video, not authored loops
    if "preview" in slug and url.endswith(".mp4"):
        s -= 4
    return s

def fetch(url, dest):
    # Referer = the URL's OWN origin, exactly what the backend's _fetch_headers does.
    # A google.com Referer trips hotlink protection: measured 403 on sexxxgif,
    # nsfwgify, porngif.co, xgifer and hardcoregify; 200 on all of them without it.
    from urllib.parse import urlparse
    p_ = urlparse(url)
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Referer": f"{p_.scheme}://{p_.hostname}/"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            ct = (r.headers.get("Content-Type") or "").lower()
            data = r.read()
    except Exception as e:
        return None, f"ERR {type(e).__name__}"
    if len(data) < 1024:
        return None, f"TINY {len(data)}"
    if "text/html" in ct or data[:15].lstrip().lower().startswith(b"<!doctype") or data[:6].lower() == b"<html>":
        return None, "HTML"
    dest.write_bytes(data)
    return len(data), "ok"

def main():
    slot = sys.argv[1]                     # e.g. scenes/lab_eyecontact_t5.webm
    n = int(sys.argv[2])
    want = [w for w in sys.argv[3].split(",") if w]
    avoid = [w for w in sys.argv[4].split(",") if w] if len(sys.argv) > 4 else []

    item = pathlib.PurePosixPath(slot).stem
    opts = json.load(open(ROOT / "media_options.json"))["options"][slot]
    urls = [o["url"] for o in opts]
    urls.sort(key=lambda u: -rank(u, want, avoid))

    work = pathlib.Path(f"/tmp/fm/{item}")
    if work.exists():
        shutil.rmtree(work)
    (work / "rep").mkdir(parents=True)

    kept, dead = [], []
    i = 0
    for u in urls:
        if len(kept) >= n:
            break
        i += 1
        low = u.lower()
        ext = next((e for e in (".mp4", ".webm", ".jpg", ".jpeg", ".png", ".webp") if low.endswith(e)), ".gif")
        dest = work / f"{len(kept):02d}{ext}"
        size, why = fetch(u, dest)
        if size:
            kept.append((dest.name, u, size))
        else:
            dead.append((u, why))

    print(f"=== {item}: fetched {len(kept)}/{i} tried, {len(dead)} dead")
    for name, u, size in kept:
        print(f"  {name}  {size//1024:5d}KB  {u}")
    if dead:
        print("  -- dead --")
        for u, why in dead[:12]:
            print(f"     {why:12s} {u}")
    json.dump([{"name": n_, "url": u, "bytes": s} for n_, u, s in kept],
              open(work / "manifest.json", "w"), indent=1)

if __name__ == "__main__":
    main()
