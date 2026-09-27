"""
The confirmatory wall-clock cap per suite (docs/PREREG.md v1.1 draft, D5): three times the longest
pilot run's wall time in that suite, over all modes and conditions, rounded up to a whole minute.

Reads runs/suites/<suite>/**/*.json (rows written by scripts/run_suite.py; each file a one-element
list), keeps the registered pilot games of the suite (analyze_common.PILOTS_B / PILOTS_C) and rows
without an error, and uses the row field `seconds` (run_suite.py's wall time for the whole run).
Plays no game.  Prints, per suite: rows read, rows with an error (excluded), the longest run
(game, condition, mode, seed, seconds) and the cap in seconds.

Command (PowerShell, from D:\\Research\\arc3\\repo; any venv with numpy):

    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\pilot_cap.py

EXPECTED OUTPUT (shape):
    minigrid: 360 pilot rows, 0 with an error; longest <game> <condition> <mode> seed <s> <t> s -> cap <c> s
    procgen:  120 pilot rows, 0 with an error; longest ... -> cap <c> s
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analyze_common as C  # noqa: E402

PILOTS = {"minigrid": C.PILOTS_B, "procgen": C.PILOTS_C}


def cap_for(rows):
    """(longest row, cap in seconds) over rows with a numeric `seconds`; (None, None) if none."""
    rs = [r for r in rows if isinstance(r.get("seconds"), (int, float))]
    if not rs:
        return None, None
    top = max(rs, key=lambda r: r["seconds"])
    return top, int(math.ceil(3 * top["seconds"] / 60.0) * 60)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Confirmatory cap from the pilot rows (PREREG v1.1 D5)")
    ap.add_argument("--root", default=os.path.join(REPO, "runs", "suites"))
    args = ap.parse_args(argv)
    out = {}
    for suite, pilots in PILOTS.items():
        rows = []
        for p in glob.glob(os.path.join(args.root, suite, "**", "*.json"), recursive=True):
            with open(p, encoding="utf-8") as f:
                d = json.load(f)
            rows.extend(d if isinstance(d, list) else [d])
        rows = [r for r in rows if r.get("game") in pilots]
        errs = [r for r in rows if r.get("error")]
        ok = [r for r in rows if not r.get("error")]
        top, cap = cap_for(ok)
        if top is None:
            print(f"{suite}: {len(rows)} pilot rows, {len(errs)} with an error; no timed row - no cap")
        else:
            print(f"{suite}: {len(rows)} pilot rows, {len(errs)} with an error; longest {top['game']} "
                  f"{top.get('condition')} {top.get('mode')} seed {top.get('seed')} {top['seconds']} s -> cap {cap} s")
        out[suite] = dict(rows=len(rows), errors=len(errs), longest=None if top is None else
                          dict(game=top["game"], condition=top.get("condition"), mode=top.get("mode"),
                               seed=top.get("seed"), seconds=top["seconds"]), cap_seconds=cap)
    return out


if __name__ == "__main__":
    main()
