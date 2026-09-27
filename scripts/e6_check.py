"""
E6 identity checks (docs/PREREG.md Sections 5.4, 9.1; v1.1 draft D12).  Reads three run files,
plays nothing:
    E6   runs/navrun_prereg_e6_arc_25x10.json   (tag prereg-v1; hash_state + nav, 25 x 10 x 20,000)
    E2   runs/navrun_e2_hash_25x10.json         (hash_state, 25 x 10 x 20,000, before the repository tag)
    v2   runs/navrun_v2_heldout.json            (the census v2 input: hash_state + nav, 17 held-out
                                                 games, seeds 1000-1003)
(a) hash_state rows of E6 against E2, matched by (game, seed): identical in every field except
    `seconds`?  Count and every differing row with its differing fields.
(b) nav rows of E6 for seeds 1000-1003 against the nav rows of v2 for the same (game, seed) (v2 has the
    17 held-out games only): identical except `seconds`?  Count, and the first differing field per row.
(c) every E6 row with actions < 20000: game, mode, seed, actions, seconds.
Fields are compared leaf by leaf, recursively (lists by position, dicts by key).

Command (PowerShell, from D:\\Research\\arc3\\repo):

    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\e6_check.py
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
IGNORE = {"seconds"}
BUDGET = 20000


def diffs(a, b, path=""):
    """Paths of leaves that differ between a and b (the top-level fields in IGNORE are skipped)."""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b), key=str):
            if not path and k in IGNORE:
                continue
            p = f"{path}.{k}" if path else str(k)
            if k not in a or k not in b:
                out.append(p + (" (missing in E6)" if k not in a else " (missing in the reference)"))
            else:
                out += diffs(a[k], b[k], p)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(f"{path} (length {len(a)} vs {len(b)})")
        for i, (x, y) in enumerate(zip(a, b)):
            out += diffs(x, y, f"{path}[{i}]")
    elif a != b:
        out.append(path)
    return out


def load(name):
    with open(os.path.join(REPO, "runs", name), encoding="utf-8") as f:
        return json.load(f)


def main():
    e6 = load("navrun_prereg_e6_arc_25x10.json")
    e2 = load("navrun_e2_hash_25x10.json")
    v2 = load("navrun_v2_heldout.json")
    print(f"E6 rows {len(e6)}; E2 rows {len(e2)}; v2 rows {len(v2)}")

    # (a)
    ref = {(r["game"], r["seed"]): r for r in e2 if r.get("mode") == "hash_state"}
    hs = [r for r in e6 if r.get("mode") == "hash_state"]
    same, bad, missing = 0, [], []
    for r in hs:
        k = (r["game"], r["seed"])
        if k not in ref:
            missing.append(k)
            continue
        d = diffs(r, ref[k])
        if d:
            bad.append((k, d))
        else:
            same += 1
    print(f"\n(a) E6 hash_state vs E2: {same} of {len(hs)} rows identical in every field except seconds"
          + (f"; {len(missing)} E6 rows without an E2 row: {missing}" if missing else ""))
    for k, d in bad:
        print(f"    differs {k[0]} seed {k[1]}: {len(d)} field(s): {d[:8]}{' ...' if len(d) > 8 else ''}")

    # (b)
    ref = {(r["game"], r["seed"]): r for r in v2 if r.get("mode") == "nav"}
    nav = [r for r in e6 if r.get("mode") == "nav" and 1000 <= r["seed"] <= 1003 and (r["game"], r["seed"]) in ref]
    same, bad = 0, []
    for r in nav:
        d = diffs(r, ref[(r["game"], r["seed"])])
        if d:
            bad.append(((r["game"], r["seed"]), d))
        else:
            same += 1
    print(f"\n(b) E6 nav (seeds 1000-1003) vs census-v2 nav rows (runs/navrun_v2_heldout.json, 17 held-out games): "
          f"{same} of {len(nav)} rows identical in every field except seconds; {len(bad)} differ")
    for k, d in bad:
        print(f"    differs {k[0]} seed {k[1]}: first field {d[0]}; {len(d)} differing field(s)")

    # (c)
    cut = [r for r in e6 if int(r.get("actions", 0)) < BUDGET]
    print(f"\n(c) E6 rows with actions < {BUDGET}: {len(cut)}")
    for r in sorted(cut, key=lambda r: (r["game"], r["mode"], r["seed"])):
        print(f"    {r['game']} {r['mode']} seed {r['seed']} actions {r['actions']} seconds {r.get('seconds')} "
              f"state {r.get('state')} levels {r.get('levels')}")


if __name__ == "__main__":
    main()
