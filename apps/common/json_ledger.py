"""Concurrency-safe read-modify-write for the small JSON ledgers under `.find-media/`.

The find-media ledgers (`media_options.json`, `media_reviews.json`) are plain files
that every mutation rewrites whole: read the dict, change one key, write it back.
That is fine while exactly one thing writes at a time — which is how every run to
date has worked — and silently destructive the moment two do.

**Measured, 2026-07-31**, 40 concurrent adds to one shelf over the real HTTP path:

    HTTP:   25 x 200      15 x 500
    shelf:  16 landed     24 LOST

Two separate defects produced that:

1. **Lost updates.** Read-modify-write with no lock. Two writers both read state S,
   both write S+their own change, and the second one wins. The loser's caller still
   gets ``200 {"ok": true}`` — nine of those 25 successes had already been discarded.
2. **A shared tmp filename.** Every writer staged through the *same* `<name>.tmp`,
   so writer A's `os.replace` moved the file out from under writer B, whose own
   `os.replace` then raised `FileNotFoundError` — the 15 500s.

Both readers also swallow parse errors and return an empty dict, so a torn ledger
reads back as *no options at all* rather than as an error. That is what turns a
race into total shelf loss with nothing in the logs.

This module is the one place that knows how to mutate those files safely. It lives
in `apps/common/` for the same reason `media_blocks.py` does: the callers are in two
different modules (`api/v1/media_finder.py`, `api/v1/media_review.py`) and one of
them mutates the other's ledger, so a fix that lived in either would drift.

Usage — hold the lock across the WHOLE read-modify-write, not just the write::

    with ledger_lock(path):
        data = _read(path)
        data["options"].setdefault(key, []).append(entry)
        write_json_atomic(path, data)

POSIX only (`fcntl`). Both supported targets — macOS dev and the Linux containers in
`docker-compose` — provide it.
"""
import fcntl
import json
import os
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any


@contextmanager
def ledger_lock(path: Path):
    """Hold an exclusive lock on `path`'s sidecar for the duration of the block.

    The lock is taken on a separate `<name>.lock` file, never on the ledger itself.
    That is deliberate: `write_json_atomic` replaces the ledger via `os.replace`,
    which swaps in a **new inode**. A lock held on the old inode would still be held
    on a file nobody can reach any more, so the next writer would sail straight
    through. The sidecar is never replaced, so it stays a stable thing to lock.

    `flock` is associated with the open file description, and each `open()` here
    creates a new one — so this serialises threads within one process (Django's
    dev server is threaded by default) exactly as it does separate processes.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_name(path.name + ".lock")
    with lock_path.open("a") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def write_json_atomic(path: Path, data: Any) -> None:
    """Replace `path` with `data` as JSON, via a tmp file unique to this writer.

    The tmp name carries pid + thread id so two concurrent writers can never stage
    through the same path. Without that, one writer's `os.replace` steals the other's
    tmp file and the loser raises `FileNotFoundError` — 15 of 40 requests, measured.

    Callers should already hold `ledger_lock`; this function is atomic on its own
    (readers see either the old file or the new one, never a partial write) but it
    cannot prevent a lost update, because the read happened before it was called.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    try:
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
