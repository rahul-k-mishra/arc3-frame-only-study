"""
E3: THE hash_state BUDGET CURVE, as registered in docs/TOG_PLAN_v2.md Section 7 (E3).
No game is run.  Written 26 Sep 2026 before any E3 output existed.

Inputs (defaults), all mode hash_state, all 25 games, seeds 1000-1003:
      3,000 actions   runs/navrun_e3_hash_25x4_3k.json
     20,000 actions   runs/navrun_e2_hash_25x10.json, seeds 1000-1003 only (E2 is not re-run, so
                      all four budgets share games and seeds)
     50,000 actions   runs/navrun_e3_hash_25x4_50k.json
    100,000 actions   runs/navrun_e3_hash_25x4_100k.json

CHECKS (registered; if any fails the script prints every violation, writes nothing and exits 1):
  C0  each budget has exactly one row per (game, seed) for the 25 games x 4 seeds, no error rows;
  C1  every row used its full budget or won (actions == budget, or state WIN with actions <= budget);
  C2  nesting, for each (game, seed) and each pair of budgets b < B:
        levels completed at b <= levels completed at B, and
        card_levels[i] identical at b and at B for every level i completed at b.
      In hash_state mode the budget is only a stop condition and runs are deterministic given the
      seed, so the run at b must be the prefix of the run at B.  A violation means non-determinism
      or a harness difference; no curve is reported from such rows.

REPORT (registered): on the 17 held-out games, games the unit, seeds nested (TOG_PLAN_v2 3.2):
    M1(B)  mean over games of the seed-mean recorded score
    M3(B)  held-out runs that won level 3 or later
    M4(B)  sum over games of the seed-mean levels completed
with hierarchical bootstrap 95% intervals (resample games, then seeds within each game; 10,000
draws; numpy default_rng(20260925)) and paired differences M(B) - M(20,000): the same resampled
games and seeds are used at every budget in each draw, which the shared seeds allow.  A per-game
table per budget; the 8 train games beside, never pooled (tu93, dc22, ls20 source-informed).
The 20,000 point here is the 4-seed subset of E2, so its values are not E2's 10-seed reference
values (0.3274, 10.50); this is stated in the output.

Allowed wording (plan): "for hash_state on the 17 held-out public games, seeds 1000-1003, raising
the budget from 20,000 to B actions changed M1 by x [interval] and M4 by y [interval]".  The
intervals describe variation within this set of games, not a population.

No --workers: the bootstrap takes seconds.  Output written atomically; an existing output is not
overwritten without --force.

Command (PowerShell, from D:\\Research\\arc3\\repo):

    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\e3_curve.py

EXPECTED OUTPUT (shape): the four files with row counts; "C0 ... PASS", "C1 ... PASS",
"C2 nesting ... PASS (n pairs checked)"; a per-game held-out table (seed-mean score and levels
per budget); M1, M3, M4 per budget with 95% intervals; paired differences against 20,000 with
95% intervals; the train games beside; "wrote runs\\e3_curve.json".  If a check fails:
"STOP: <check> failed" with every violation listed, and nothing written.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TRAIN = ["tu93", "ls20", "vc33", "m0r0", "ft09", "lp85", "lf52", "dc22"]
HELD_OUT = ["ar25", "bp35", "cd82", "cn04", "g50t", "ka59", "r11l", "re86", "s5i5",
            "sb26", "sc25", "sk48", "sp80", "su15", "tn36", "tr87", "wa30"]
SOURCE_INFORMED = ["tu93", "dc22", "ls20"]
SEEDS = [1000, 1001, 1002, 1003]
MODE = "hash_state"
REF_BUDGET = 20000
BOOT, BOOT_SEED = 10000, 20260925


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load(path, budget):
    """{(game, seed): row} for mode hash_state, seeds 1000-1003; C0 and C1 problems as lists."""
    rows = [r for r in json.load(open(path)) if r.get("mode") == MODE and int(r.get("seed", -1)) in SEEDS]
    c0, c1, cells = [], [], {}
    for r in rows:
        k = (r["game"], int(r["seed"]))
        if r.get("error"):
            c0.append(f"{budget}: {k} is an error row ({r['error'][:80]})")
            continue
        if k in cells:
            c0.append(f"{budget}: duplicate row {k}")
            continue
        cells[k] = r
        acts = int(r.get("actions", -1))
        if not (acts == budget or (r.get("state") == "WIN" and acts <= budget)):
            c1.append(f"{budget}: {k} used {acts} actions, state {r.get('state')} (budget {budget})")
    for g in TRAIN + HELD_OUT:
        for s in SEEDS:
            if (g, s) not in cells:
                c0.append(f"{budget}: missing row {(g, s)}")
    return cells, c0, c1


def nesting(data, budgets):
    """C2: levels never decrease and completed levels' card_levels agree, for every b < B."""
    bad, n = [], 0
    for b, B in itertools.combinations(budgets, 2):
        for g in TRAIN + HELD_OUT:
            for s in SEEDS:
                rb, rB = data[b][(g, s)], data[B][(g, s)]
                n += 1
                lb, lB = int(rb["levels"]), int(rB["levels"])
                if lb > lB:
                    bad.append(f"{g} seed {s}: {lb} levels at {b} but {lB} at {B}")
                    continue
                cb, cB = rb.get("card_levels"), rB.get("card_levels")
                if not cb or not cB:
                    bad.append(f"{g} seed {s}: card_levels missing at {b if not cb else B}")
                    continue
                if cb[:lb] != cB[:lb]:
                    bad.append(f"{g} seed {s}: card_levels of the {lb} completed levels differ, "
                               f"{cb[:lb]} at {b} vs {cB[:lb]} at {B}")
    return bad, n


def arrays(cells, games):
    sc = np.array([[float(cells[(g, s)].get("score", 0.0)) for s in SEEDS] for g in games])
    lv = np.array([[int(cells[(g, s)].get("levels", 0)) for s in SEEDS] for g in games])
    return sc, lv


def measures(sc, lv):
    return dict(M1=float(sc.mean(axis=1).mean()), M3=int((lv >= 3).sum()),
                M4=float(lv.mean(axis=1).sum()))


def main():
    ap = argparse.ArgumentParser(description="E3 budget curve (TOG_PLAN_v2 Section 7)")
    ap.add_argument("--b3k", default=os.path.join(REPO, "runs", "navrun_e3_hash_25x4_3k.json"))
    ap.add_argument("--b20k", default=os.path.join(REPO, "runs", "navrun_e2_hash_25x10.json"))
    ap.add_argument("--b50k", default=os.path.join(REPO, "runs", "navrun_e3_hash_25x4_50k.json"))
    ap.add_argument("--b100k", default=os.path.join(REPO, "runs", "navrun_e3_hash_25x4_100k.json"))
    ap.add_argument("--out", default=os.path.join(REPO, "runs", "e3_curve.json"))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    if os.path.exists(args.out) and not args.force:
        sys.exit(f"{args.out} exists; not overwritten without --force")
    files = {3000: args.b3k, 20000: args.b20k, 50000: args.b50k, 100000: args.b100k}
    budgets = sorted(files)
    missing = [p for p in files.values() if not os.path.exists(p)]
    if missing:
        sys.exit(f"STOP: input files not found: {missing}")

    data, c0, c1 = {}, [], []
    for b in budgets:
        cells, e0, e1 = load(files[b], b)
        data[b] = cells
        c0 += e0
        c1 += e1
        print(f"{b:>7} actions: {files[b]}  ({len(cells)} rows, mode {MODE}, seeds {SEEDS})")
    for name, errs in (("C0 complete rows", c0), ("C1 full budget or win", c1)):
        if errs:
            print(f"\nSTOP: {name} failed ({len(errs)}):")
            for e in errs:
                print("   " + e)
            sys.exit(1)
        print(f"{name} ... PASS")
    bad, n = nesting(data, budgets)
    if bad:
        print(f"\nSTOP: C2 nesting failed ({len(bad)} of {n} (game, seed, budget pair) checks):")
        for e in bad:
            print("   " + e)
        print("A run at a smaller budget is not the prefix of the run at a larger one: "
              "non-determinism or a harness difference. No curve is reported.")
        sys.exit(1)
    print(f"C2 nesting ... PASS ({n} (game, seed, budget pair) checks)")

    # arrays [budget][game, seed]
    H = {b: arrays(data[b], HELD_OUT) for b in budgets}
    T = {b: arrays(data[b], TRAIN) for b in budgets}
    point = {b: measures(*H[b]) for b in budgets}

    rng = np.random.default_rng(BOOT_SEED)
    G, S = len(HELD_OUT), len(SEEDS)
    draws = {b: {k: [] for k in ("M1", "M3", "M4")} for b in budgets}
    diffs = {b: {k: [] for k in ("M1", "M3", "M4")} for b in budgets if b != REF_BUDGET}
    rows_idx = np.arange(G)[:, None]
    for _ in range(BOOT):
        gi = rng.integers(0, G, G)
        si = rng.integers(0, S, (G, S))
        m = {}
        for b in budgets:
            sc, lv = H[b]
            m[b] = measures(sc[gi][rows_idx, si], lv[gi][rows_idx, si])
            for k in m[b]:
                draws[b][k].append(m[b][k])
        for b in diffs:
            for k in m[b]:
                diffs[b][k].append(m[b][k] - m[REF_BUDGET][k])
    ci = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    intervals = {b: {k: ci(v) for k, v in draws[b].items()} for b in budgets}
    diff_point = {b: {k: point[b][k] - point[REF_BUDGET][k] for k in point[b]} for b in diffs}
    diff_ci = {b: {k: ci(v) for k, v in diffs[b].items()} for b in diffs}

    # per-game table
    print(f"\nheld-out, seed-mean score / levels per budget (seeds {SEEDS}):")
    print(f"  {'game':6} " + " ".join(f"{b:>16}" for b in budgets))
    per_game = {}
    for i, g in enumerate(HELD_OUT):
        cells = [f"{H[b][0][i].mean():8.4f}/{H[b][1][i].mean():5.2f}" for b in budgets]
        print(f"  {g:6} " + " ".join(f"{c:>16}" for c in cells))
        per_game[g] = {str(b): dict(score=float(H[b][0][i].mean()), levels=float(H[b][1][i].mean()))
                       for b in budgets}

    fmt = lambda v, c, d: f"{v:.{d}f} [{c[0]:.{d}f}, {c[1]:.{d}f}]"
    print(f"\nheld-out measures (games the unit, seeds nested; 95% hierarchical bootstrap intervals):")
    print(f"  {'budget':>7} {'M1':>28} {'M3':>18} {'M4':>24}")
    for b in budgets:
        p, c = point[b], intervals[b]
        print(f"  {b:>7} {fmt(p['M1'], c['M1'], 4):>28} {fmt(p['M3'], c['M3'], 0):>18} "
              f"{fmt(p['M4'], c['M4'], 2):>24}")
    print(f"\npaired differences against {REF_BUDGET} actions (same resampled games and seeds):")
    print(f"  {'budget':>7} {'M1(B) - M1(20k)':>30} {'M3(B) - M3(20k)':>22} {'M4(B) - M4(20k)':>26}")
    for b in diffs:
        p, c = diff_point[b], diff_ci[b]
        print(f"  {b:>7} {fmt(p['M1'], c['M1'], 4):>30} {fmt(p['M3'], c['M3'], 0):>22} "
              f"{fmt(p['M4'], c['M4'], 2):>26}")
    print(f"\nnote: the {REF_BUDGET}-action point is seeds {SEEDS} of E2, not E2's 10-seed reference "
          f"values (M1 0.3274, M4 10.50).")

    train = {str(b): dict(measures=measures(*T[b]),
                          per_game={g: dict(score=float(T[b][0][i].mean()),
                                            levels=float(T[b][1][i].mean()),
                                            source_informed=g in SOURCE_INFORMED)
                                    for i, g in enumerate(TRAIN)}) for b in budgets}
    print("\ntrain games beside (not pooled; * source-informed): M1 / M4 per budget")
    for b in budgets:
        t = train[str(b)]
        print(f"  {b:>7} M1 {t['measures']['M1']:.4f} M4 {t['measures']['M4']:.2f}  "
              + " ".join(f"{g}{'*' if v['source_informed'] else ''} {v['score']:.3f}/{v['levels']:.1f}"
                         for g, v in t["per_game"].items()))

    out = dict(script="scripts/e3_curve.py", plan="docs/TOG_PLAN_v2.md Section 7 (E3)",
               created=time.strftime("%Y-%m-%d %H:%M:%S"), mode=MODE, seeds=SEEDS,
               inputs={str(b): dict(path=files[b], sha256=sha256(files[b])) for b in budgets},
               checks=dict(C0="PASS", C1="PASS", C2=f"PASS ({n} checks)"),
               bootstrap=dict(draws=BOOT, seed=BOOT_SEED, method="games, then seeds within game; paired across budgets"),
               heldout=dict(point={str(b): point[b] for b in budgets},
                            intervals95={str(b): intervals[b] for b in budgets},
                            diff_vs_20000={str(b): diff_point[b] for b in diffs},
                            diff_intervals95={str(b): diff_ci[b] for b in diffs},
                            per_game=per_game),
               train_beside=train,
               note_20000=f"seeds {SEEDS} of runs/navrun_e2_hash_25x10.json; not E2's 10-seed values")
    tmp = args.out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=1)
    os.replace(tmp, args.out)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
