#!/usr/bin/env python3
"""
Stitch the Vesper conversation sessions into one faithful, readable history.

Reads the raw Claude Code session transcripts (.jsonl) listed in SESSIONS straight
from disk, merges all events by timestamp, dedups by uuid, and emits:
  - conversation-transcript.md  (readable: user verbatim, assistant text verbatim,
                                 one-line tool-call + tool-result summaries, numbered
                                 user exchanges, session-boundary markers)
  - raw-transcript.jsonl        (lossless: the merged+deduped+sorted raw events)

FAITHFULNESS: user words and assistant text are copied verbatim from disk — never
paraphrased. Only structural wrappers (<system-reminder>, <command-*>, local-command
caveats) are stripped from user turns so the actual words read clean.

NOTE ON REASONING: Claude Code stores only an *encrypted signature* for assistant
`thinking`, not the text (verified: 632 thinking blocks in the main session, all empty).
So the model's internal reasoning is NOT in the log and cannot be in this transcript;
the loops / course-corrections behind it are distilled by hand in `iteration-log.md`.

Re-run:  python3 build_transcript.py
"""
import json
import os
import re

SRC_DIR = "/Users/a0000/.claude/projects/-Users-a0000-Desktop-Desktop-Archive-Backup-story-gen-story-gen-web-app-story-gen-django"
# The Vesper chain. 8e47ba21 is the main arc ("lets author a new game" -> now);
# 3013838e is a short "continue authoring vesper" side-session. Other games
# (e.g. 0353c3d6 incest) and the skill-redesign precursors are excluded.
SESSIONS = [
    "8e47ba21-c47f-46e7-a2e1-a1aabdceb1d8.jsonl",
    "3013838e-5df5-4913-b8bd-41d7d44f809e.jsonl",
]
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPT_MD = os.path.join(OUT_DIR, "conversation-transcript.md")
RAW_JSONL = os.path.join(OUT_DIR, "raw-transcript.jsonl")

WRAP_RE = re.compile(
    r"<system-reminder>.*?</system-reminder>"
    r"|<command-name>.*?</command-name>"
    r"|<command-message>.*?</command-message>"
    r"|<command-args>.*?</command-args>"
    r"|<local-command-stdout>.*?</local-command-stdout>"
    r"|<local-command-caveat>.*?</local-command-caveat>",
    re.DOTALL,
)


def clean_user(text):
    return WRAP_RE.sub("", text or "").strip()


def short(s, n=160):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n] + "…"


def user_text(content):
    if isinstance(content, str):
        return clean_user(content)
    if isinstance(content, list):
        return clean_user(" ".join(
            b.get("text", "") for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        ).strip())
    return ""


def has_tool_result(content):
    return isinstance(content, list) and any(
        isinstance(b, dict) and b.get("type") == "tool_result" for b in content
    )


def summarize_tool_use(b):
    name = b.get("name", "tool")
    inp = b.get("input", {}) or {}
    if name in ("Edit", "Write", "Read", "NotebookEdit"):
        p = inp.get("file_path", "")
        return f"[{name}] {os.path.basename(p) or p}"
    if name == "Bash":
        return f"[Bash] {short(inp.get('description') or inp.get('command', ''), 100)}"
    if name in ("Agent",):
        return f"[Agent:{inp.get('subagent_type', '?')}] {short(inp.get('description', ''), 90)}"
    if name == "Workflow":
        m = re.search(r"name:\s*'([^']+)'", str(inp.get("script", "")))
        return f"[Workflow] {m.group(1) if m else (inp.get('name') or 'inline')}"
    if name == "Skill":
        return f"[Skill] {inp.get('skill', '')}"
    if name == "ToolSearch":
        return f"[ToolSearch] {short(inp.get('query', ''), 70)}"
    if name == "AskUserQuestion":
        qs = inp.get("questions") or []
        return f"[AskUserQuestion] {short(' / '.join(q.get('header', '?') for q in qs if isinstance(q, dict)), 90)}"
    if name in ("TaskCreate", "TaskUpdate"):
        return f"[{name}] {short(inp.get('subject') or inp.get('taskId', ''), 70)}"
    if name == "ExitPlanMode":
        return "[ExitPlanMode]"
    if name in ("Glob", "Grep"):
        return f"[{name}] {short(inp.get('pattern', ''), 70)}"
    return f"[{name}] {short(json.dumps(inp, ensure_ascii=False), 70)}"


def summarize_tool_result(content):
    for b in content:
        if isinstance(b, dict) and b.get("type") == "tool_result":
            c = b.get("content")
            if isinstance(c, list):
                c = " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
            tag = "⚠️ " if b.get("is_error") else ""
            return f"_{tag}↳ {short(c, 170)}_"
    return "_↳ (result)_"


# ---- load + merge ---------------------------------------------------------------------
events, seen, per_session = [], set(), {}
for si, fn in enumerate(SESSIONS):
    sid = fn[:36]
    n = 0
    with open(os.path.join(SRC_DIR, fn), encoding="utf-8", errors="replace") as fh:
        for ln, line in enumerate(fh):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            uid = ev.get("uuid")
            if uid and uid in seen:
                continue
            if uid:
                seen.add(uid)
            ev["_src"], ev["_order"], ev["_raw"] = sid, (si, ln), line
            events.append(ev)
            n += 1
    per_session[sid] = n

events.sort(key=lambda e: (e.get("timestamp") or "", e["_order"]))

with open(RAW_JSONL, "w", encoding="utf-8") as out:
    for ev in events:
        out.write(ev["_raw"] + "\n")

# ---- readable transcript --------------------------------------------------------------
exchange = n_asst = n_tool = 0
cur_session = None
first_ts = last_ts = None
body = []

for ev in events:
    typ, ts = ev.get("type"), ev.get("timestamp")
    if ts:
        first_ts = first_ts or ts
        last_ts = ts
    if ev.get("isSidechain"):
        continue  # subagent/workflow internals -> stay in raw only
    msg = ev.get("message") or {}
    content = msg.get("content")

    if ev.get("_src") != cur_session and typ in ("user", "assistant"):
        cur_session = ev.get("_src")
        body.append(f"\n\n---\n\n> ⟦ session `{cur_session}` — {str(ts)[:19]} ⟧\n")

    if typ == "user":
        if has_tool_result(content) and not user_text(content):
            body.append(summarize_tool_result(content) + "\n")
            continue
        txt = user_text(content)
        if not txt:
            continue
        exchange += 1
        body.append(f"\n\n---\n\n## ▶ [{exchange}] LO\n\n{txt}\n")
    elif typ == "assistant":
        if not isinstance(content, list):
            continue
        for b in content:
            if not isinstance(b, dict):
                continue
            bt = b.get("type")
            if bt == "text":
                t = b.get("text", "").strip()
                if t:
                    n_asst += 1
                    body.append(f"\n**ENI:** {t}\n")
            elif bt == "tool_use":
                n_tool += 1
                body.append(f"&nbsp;&nbsp;`{summarize_tool_use(b)}`  \n")

header = f"""# Vesper — Stitched Conversation History

Faithful, turn-by-turn record of the Vesper authoring conversation, stitched from the
raw Claude Code session transcripts on disk by `build_transcript.py` — the source of
truth, NOT a reconstruction from memory. User words and assistant replies are verbatim;
only structural wrappers (system-reminders / command tags) were stripped from user turns.

**Sessions stitched (newest content first in time):** {', '.join('`'+s[:8]+'`' for s in SESSIONS)}
**Span:** {first_ts} → {last_ts}
**Counts:** {exchange} user exchanges · {n_asst} assistant replies · {n_tool} tool calls
**Per-session events (deduped):** {', '.join(f'{k[:8]}={v}' for k,v in per_session.items())}

> **The model's reasoning is NOT in this transcript.** Claude Code stores only an
> encrypted signature for assistant `thinking`, so the plaintext is empty in the log.
> The loops, dead-ends, and course-corrections — the part worth studying — are distilled
> by hand in **`iteration-log.md`**. Subagent/workflow internals (sidechains) are kept
> out of this readable thread but remain in `raw-transcript.jsonl`.

---
"""

with open(TRANSCRIPT_MD, "w", encoding="utf-8") as out:
    out.write(header)
    out.write("".join(body))
    out.write("\n")

print(f"events merged (deduped): {len(events)}")
print(f"per-session: {per_session}")
print(f"user exchanges: {exchange}  asst replies: {n_asst}  tool calls: {n_tool}")
print(f"span: {first_ts} .. {last_ts}")
print(f"wrote {TRANSCRIPT_MD}")
print(f"wrote {RAW_JSONL}")
