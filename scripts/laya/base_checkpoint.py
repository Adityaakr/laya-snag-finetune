"""Locates (or downloads, pinned) the base Laya checkpoint that every experiment starts from.

Base: convaiinnovations/laya, typed-decisions subfolder, revision 55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851 (Apache-2.0).
The download goes to <repo>/.laya/hf, the same place the Snag repository uses, so both layouts work.
"""

from __future__ import annotations

import os

REPO = "convaiinnovations/laya"
REVISION = "55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851"
SUBFOLDER = "typed-decisions"


def base_dir(root: str) -> str:
    cache = os.path.join(root, ".laya", "hf", "hub")
    local = os.path.join(cache, "models--convaiinnovations--laya", "snapshots", REVISION, SUBFOLDER)
    if os.path.exists(os.path.join(local, "model.safetensors")):
        return local
    from huggingface_hub import snapshot_download

    snap = snapshot_download(REPO, revision=REVISION, allow_patterns=[f"{SUBFOLDER}/*"], cache_dir=cache)
    return os.path.join(snap, SUBFOLDER)
