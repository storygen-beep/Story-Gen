#!/usr/bin/env python3
"""
Build a readable markdown transcript of the Vesper authoring session from the
raw Claude Code session .jsonl (the faithful source — NOT a reconstruction).

Usage:
    python3 build_transcript.py [raw-transcript.jsonl] [conversation-transcript.md]

Renders, in file (chronological) order:
  - USER turns verbatim (system-reminder / command wrappers stripped, words kept)
  - ASSISTANT text replies verbatim
  - ASSISTANT thinking blocks (foldable <details>, so they don't drown the dialogue)
  - tool calls summarized to one line; tool results summarized to one line
Metadata-only events are skipped.
"""
import json, sys, re, os

INCLUDE_THINKING = True
SRC = sys.argv[1] if len(sys.argv) > 1 else "raw-transcript.jsonl"
OUT = sys.argv[2] if len(sys.argv) > 2 else "conversation-transcript.md"

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
    """Strip harness wrappers, keep the user's real words."""
    t = WRAP_RE.sub("", text)
    return t.strip()

def short(s, n=160):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n] + "…"

def summarize_tool_use(b):
    name = b.get("name", "tool")
    inp = b.get("input", {}) or {}
    if name in ("Edit", "Write", "Read", "NotebookEdit"):
        p = inp.get("file_path", "")
        return f"`[{name}]` {os.path.basename(p) or p}"
    if name == "Bash":
        return f"`[Bash]` {short(inp.get('description') or inp.get('command',''), 100)}"
    if name == "Agent":
        return f"`[Agent:{inp.get('subagent_type','?')}]` {short(inp.get('description',''), 100)}"
    if name == "Skill":
        return f"`[Skill]` {inp.get('skill','')}"
    if name == "ToolSearch":
        return f"`[ToolSearch]` {short(inp.get('query',''), 80)}"
    if name == "AskUserQuestion":
        qs = inp.get("questions") or []
        heads = " / ".join(q.get("header", "?") for q in qs if isinstance(q, dict))
        return f"`[AskUserQuestion]` {short(heads, 100)}"
    if name == "ExitPlanMode":
        return "`[ExitPlanMode]`"
    if name == "Glob" or name == "Grep":
        return f"`[{name}]` {short(inp.get('pattern',''), 80)}"
    return f"`[{name}]` {short(json.dumps(inp, ensure_ascii=False), 80)}"

def summarize_tool_result(b):
    c = b.get("content")
    if isinstance(c, list):
        txt = " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
    else:
        txt = str(c) if c is not None else ""
    err = b.get("is_error")
    tag = "⚠️ " if err else ""
    return f"_{tag}↳ result: {short(txt, 180)}_"

def main():
    out = []
    user_n = 0
    asst_n = 0
    sess = None
    first_ts = last_ts = None
    with open(SRC, encoding="utf-8") as fh:
        lines = [l for l in fh if l.strip()]

    # header placeholder (filled after we know counts/dates)
    body = []
    for line in lines:
        try:
            o = json.loads(line)
        except Exception:
            continue
        t = o.get("type")
        sess = sess or o.get("sessionId")
        ts = o.get("timestamp")
        if ts:
            first_ts = first_ts or ts
            last_ts = ts
        msg = o.get("message") or {}

        if t == "user":
            c = msg.get("content")
            if isinstance(c, str):
                txt = clean_user(c)
                if txt:
                    user_n += 1
                    body.append(f"\n\n---\n\n## ▶ USER #{user_n}\n\n{txt}\n")
            elif isinstance(c, list):
                texts = [b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text"]
                tres = [b for b in c if isinstance(b, dict) and b.get("type") == "tool_result"]
                joined = clean_user(" ".join(texts).strip())
                if joined:
                    user_n += 1
                    body.append(f"\n\n---\n\n## ▶ USER #{user_n}\n\n{joined}\n")
                for b in tres:
                    body.append(summarize_tool_result(b) + "\n")

        elif t == "assistant":
            c = msg.get("content")
            if not isinstance(c, list):
                continue
            opened = False
            for b in c:
                if not isinstance(b, dict):
                    continue
                bt = b.get("type")
                if bt == "thinking" and INCLUDE_THINKING:
                    th = b.get("thinking", "").strip()
                    if th:
                        body.append(
                            "\n<details><summary>🧠 thinking</summary>\n\n"
                            + th + "\n\n</details>\n"
                        )
                elif bt == "text":
                    txt = b.get("text", "").strip()
                    if txt:
                        if not opened:
                            asst_n += 1
                            opened = True
                        body.append(f"\n**🤖 ASSISTANT:**\n\n{txt}\n")
                elif bt == "tool_use":
                    body.append(summarize_tool_use(b) + "\n")

    header = [
        "# Vesper — full authoring conversation (faithful transcript)\n",
        "> Converted verbatim from the raw Claude Code session log "
        "(`raw-transcript.jsonl`) by `build_transcript.py`. Source of truth, "
        "not a reconstruction.\n",
        f"> **Session:** `{sess}`  \n",
        f"> **Span:** {first_ts} → {last_ts}  \n",
        f"> **Your turns:** {user_n}  ·  **My replies:** {asst_n}\n",
        "\n> This is the visible dialogue + one-line tool-call summaries. NOTE: Claude Code stores only an "
        "*encrypted signature* for assistant reasoning (the `thinking` text is empty in the log), so my "
        "internal reasoning is **not** in here — the loops and course-corrections behind it are distilled "
        "in `iteration-log.md` instead.\n",
    ]
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("".join(header))
        fh.write("".join(body))
        fh.write("\n")
    print(f"WROTE {OUT}: {user_n} user turns, {asst_n} assistant replies")

if __name__ == "__main__":
    main()
