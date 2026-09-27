"""
e6_summary.py -- the STATE.md amendment (e) table, recomputed from the E6 run file after the re-run.

Infrastructure (a read-only summary): plays no game, changes no file, writes nothing.  Standard
library only.  Reads runs/navrun_prereg_e6_arc_25x10.json (25 games x {hash_state, nav} x 10 seeds x
20,000 actions; the eight nav rows cut at 900 s were replaced in commit b3509de).

What amendment (e) reported, and how each quantity is defined here (the definitions of
docs/archive/TOG_PLAN_v2.md Section 3.2, games as the unit, seeds nested; they are also what
scripts/g_nav_run.py's closing TRAIN / HELD-OUT line prints when every game has all its seeds):
    M1                mean over the games of the split of the seed-mean scorecard score
                      (row field "score")
    levels per seed   sum over the games of the split of the seed-mean levels completed (field
                      "levels"); TOG_PLAN_v2's M4
    goal_confirmed    the games where the nav counter goal_confirmed (row nav.counters) is >= 1 in
                      at least one seed
per mode (hash_state, nav) and split: train (8 games; tu93, dc22, ls20 source-informed) and held-out
(17 games).  It also prints the g_nav_run.py forms (mean over rows; total levels / 10 seeds) and says
whether they equal the per-game forms, and the checks behind the numbers: rows per (game, mode),
seeds, rows with actions < 20,000 that did not win.

Amendment (e)'s values, for comparison (hash_state rows are unchanged by the re-run, so its two
hash_state lines must reproduce exactly; the nav lines are the ones the re-run can change):
    hash_state  train M1 0.1901, levels per seed 11.1; held-out M1 0.3274, levels per seed 10.5
    nav         train M1 0.2035, levels per seed 10.8; held-out M1 0.2612, levels per seed 11.1
                (provisional: computed with the eight cut rows)
    goal_confirmed fired on tu93 only; on no held-out game.

Command (PowerShell, from D:\\Research\\arc3\\repo; the ARC venv, or any Python 3):

    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\e6_summary.py

EXPECTED OUTPUT (shape):
    read 500 rows from runs\\navrun_prereg_e6_arc_25x10.json
    checks: 25 games x 2 modes, 10 seeds each (1000-1009): OK; rows with actions < 20000 and not WIN: 0
    split     mode        games  M1      levels/seed  (g_nav_run form: mean ..., levels .../seed; same)
    train     hash_state  8      0.1901  11.10
    train     nav         8      ...     ...
    held-out  hash_state  17     0.3274  10.50
    held-out  nav         17     ...     ...
    goal_confirmed >= 1 in some seed (nav): train [...]; held-out [...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict

# CLAUDE.md and docs/HELDOUT.md; scripts/g_control_probe.py TRAIN / HELD_OUT
TRAIN = ("tu93", "ls20", "vc33", "m0r0", "ft09", "lp85", "lf52", "dc22")
HELD_OUT = ("ar25", "bp35", "cd82", "cn04", "g50t", "ka59", "r11l", "re86", "s5i5", "sb26", "sc25",
            "sk48", "sp80", "su15", "tn36", "tr87", "wa30")
MODES = ("hash_state", "nav")
SEEDS = tuple(range(1000, 1010))
BUDGET = 20000


def main(argv=None):
    ap = argparse.ArgumentParser(description="STATE.md amendment (e) table from the E6 run file")
    ap.add_argument("--runs", default=os.path.join("runs", "navrun_prereg_e6_arc_25x10.json"))
    args = ap.parse_args(argv)
    with open(args.runs, encoding="utf-8") as f:
        rows = json.load(f)
    print(f"read {len(rows)} rows from {args.runs}")

    by = defaultdict(list)
    for r in rows:
        by[(r["game"], r["mode"])].append(r)
    problems = []
    for g in TRAIN + HELD_OUT:
        for m in MODES:
            seeds = sorted(r["seed"] for r in by.get((g, m), []))
            if tuple(seeds) != SEEDS:
                problems.append(f"{g} {m}: seeds {seeds}")
    extra = sorted({k for k in by if k[0] not in TRAIN + HELD_OUT or k[1] not in MODES})
    if extra:
        problems.append(f"unexpected (game, mode): {extra}")
    errors = [f"{r['game']} {r['mode']} {r['seed']}" for r in rows if r.get("error")]
    cut = [f"{r['game']} {r['mode']} {r['seed']} ({r.get('actions')})" for r in rows
           if int(r.get("actions", -1)) < BUDGET and r.get("state") != "WIN"]
    print(f"checks: 25 games x 2 modes, 10 seeds each (1000-1009): {'OK' if not problems else 'PROBLEMS'}; "
          f"rows with an error: {len(errors)}; rows with actions < {BUDGET} and not WIN: {len(cut)}")
    for p in problems + errors + cut:
        print(f"    {p}")

    print(f"\n{'split':9} {'mode':11} {'games':>5}  {'M1':>6}  {'levels/seed':>11}   g_nav_run form")
    for split, games in (("train", TRAIN), ("held-out", HELD_OUT)):
        for m in MODES:
            per = [by[(g, m)] for g in games if by.get((g, m))]
            if not per:
                continue
            m1 = sum(sum(r["score"] for r in v) / len(v) for v in per) / len(per)
            lv = sum(sum(r["levels"] for r in v) / len(v) for v in per)
            flat = [r for v in per for r in v]
            m1_rows = sum(r["score"] for r in flat) / len(flat)
            lv_rows = sum(r["levels"] for r in flat) / len(SEEDS)
            same = abs(m1 - m1_rows) < 1e-12 and abs(lv - lv_rows) < 1e-9
            print(f"{split:9} {m:11} {len(per):5d}  {m1:.4f}  {lv:11.2f}   mean {m1_rows:.4f}, levels "
                  f"{lv_rows:.1f}/seed; {'same' if same else 'DIFFERENT'}")

    for split, games in (("train", TRAIN), ("held-out", HELD_OUT)):
        fired = [g for g in games if any(((r.get("nav") or {}).get("counters") or {}).get("goal_confirmed", 0) >= 1
                                          for r in by.get((g, "nav"), []))]
        print(f"goal_confirmed >= 1 in some seed (nav), {split}: {fired or 'none'}")
    return 0 if not (problems or errors) else 1


if __name__ == "__main__":
    sys.exit(main())
