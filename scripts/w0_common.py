"""
Shared helpers for the W0 infrastructure checks (docs/W0_CHECKS.md): the byte-for-byte determinism
comparison, the distinct-colour count, atomic JSON writing, resume and the summary table.

Nothing here plays a game.  Imported by scripts/w0_procgen_smoke.py and scripts/w0_minigrid_smoke.py;
it needs only numpy and the standard library, so it runs in both .venv_procgen and .venv_games.
"""
from __future__ import annotations

import json
import os

import numpy as np


def compare_frames(a, b):
    """Byte-for-byte comparison of two frame sequences (lists of numpy arrays).

    Returns dict(pass_, n_a, n_b, first_diff_step, reason).  pass_ is True only if both sequences
    have the same length and every pair of frames has the same shape, the same dtype and identical
    bytes.  first_diff_step is the 0-based index of the first differing frame, or None."""
    out = dict(pass_=False, n_a=len(a), n_b=len(b), first_diff_step=None, reason="")
    for i, (x, y) in enumerate(zip(a, b)):
        if x.shape != y.shape or x.dtype != y.dtype:
            out.update(first_diff_step=i, reason=f"shape/dtype {x.shape} {x.dtype} vs {y.shape} {y.dtype}")
            return out
        if x.tobytes() != y.tobytes():
            out.update(first_diff_step=i, reason="bytes differ")
            return out
    if len(a) != len(b):
        out.update(first_diff_step=min(len(a), len(b)), reason="lengths differ")
        return out
    out.update(pass_=True, reason="identical")
    return out


def distinct_colours(frames):
    """Number of distinct RGB triples over all frames (H x W x 3, uint8).  Each pixel is packed as
    r<<16 | g<<8 | b and the packed values are collected in one set."""
    seen = set()
    for f in frames:
        f = np.asarray(f)
        if f.ndim != 3 or f.shape[-1] != 3:
            raise ValueError(f"expected H x W x 3, got {f.shape}")
        p = f.reshape(-1, 3).astype(np.uint32)
        packed = (p[:, 0] << 16) | (p[:, 1] << 8) | p[:, 2]
        seen.update(np.unique(packed).tolist())
    return len(seen)


def safe_name(game):
    """A file name for an environment id (ids contain only letters, digits, '-', '_' and '.')."""
    return "".join(c if (c.isalnum() or c in "-_.") else "_" for c in game)


def out_path(out_dir, game):
    return os.path.join(out_dir, safe_name(game) + ".json")


def write_json_atomic(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1)
    os.replace(tmp, path)


def pending(games, out_dir, force):
    """Games still to run: all of them with --force, else those without a JSON (resume)."""
    if force:
        return list(games)
    return [g for g in games if not os.path.exists(out_path(out_dir, g))]


def load_all(games, out_dir):
    rows = []
    for g in games:
        p = out_path(out_dir, g)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                rows.append(json.load(f))
    return rows


def print_table(rows, cols):
    """cols: list of (header, function row -> value).  One line per row, in the given order."""
    heads = [h for h, _ in cols]
    cells = [[("" if v is None else str(v)) for v in (fn(r) for _, fn in cols)] for r in rows]
    w = [max([len(h)] + [len(c[i]) for c in cells]) for i, h in enumerate(heads)]
    print("  ".join(h.ljust(w[i]) for i, h in enumerate(heads)))
    for c in cells:
        print("  ".join(c[i].ljust(w[i]) for i in range(len(heads))))
