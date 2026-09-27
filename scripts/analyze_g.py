"""
G — goal-identification cost (docs/PREREG.md v1, Sections 6 and 10).  Registered analysis; frozen at
the tag.  G is reported, not tested: there is no threshold.

Reads the rows written by scripts/g_goal_cost.py (agent "G"), each with a field
    G = {"defined": bool, "G_end_place": int|null, "G_end_feat": int|null, "G_act": float|null}
"defined" is false where A2 fails (no controlled object): such rows count as undefined and are
excluded.  For a defined row, G_end_* null means infinity (h0 verdict or budget ended first), and
G_act null means no level end within the budget.
Per (suite, condition, game): seeds, undefined seeds, lower median of G_end_place and G_end_feat with
infinity sorted last, the number of infinite values, and the lower median of G_act over the seeds
where it is not null.  Per (suite, condition): the lower median over games of the per-game values.
Lower median = element at index floor((n-1)/2) of the sorted list (defined with infinity).
Confirmatory games only on suites B and C; all ARC games present.

Command (PowerShell, from D:\\Research\\arc3\\repo):

    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\analyze_g.py --runs "runs\\prereg_g_*.json"

EXPECTED OUTPUT (shape): one line per (suite, condition, game), then one summary line per suite:
    procgen center_off maze seeds=10 undefined=0 G_end_place=... inf=... G_end_feat=... inf=... G_act=...
    suite procgen center_off: games=14 G_end_place=... G_end_feat=... G_act=...
    wrote docs\\tables\\g.md, docs\\tables\\g.json
"""
from __future__ import annotations

import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analyze_common as C  # noqa: E402

INF = math.inf


def g_rows(rows, truth_by_suite):
    per = {}
    for r in rows:
        if r.get("agent") != "G" or not isinstance(r.get("G"), dict):
            continue
        per.setdefault((r.get("suite"), r.get("condition"), r["game"]), []).append(r["G"])
    games_table, suite_table = [], []
    by_suite = {}
    for (suite, cond, game), gs in sorted(per.items()):
        if suite != "arc":
            truth = truth_by_suite.get(suite)
            if truth is None or game not in C.confirmatory(suite, truth):
                continue
        defined = [g for g in gs if g.get("defined")]
        ep = [INF if g.get("G_end_place") is None else g["G_end_place"] for g in defined]
        ef = [INF if g.get("G_end_feat") is None else g["G_end_feat"] for g in defined]
        ga = [g["G_act"] for g in defined if g.get("G_act") is not None]
        row = [suite, cond, game, len(gs), len(gs) - len(defined), C.lower_median(ep), sum(v == INF for v in ep),
               C.lower_median(ef), sum(v == INF for v in ef), C.lower_median(ga)]
        games_table.append(row)
        by_suite.setdefault((suite, cond), []).append(row)
    for (suite, cond), rs in sorted(by_suite.items()):
        suite_table.append([suite, cond, len(rs),
                            C.lower_median([r[5] for r in rs if r[5] is not None]),
                            C.lower_median([r[7] for r in rs if r[7] is not None]),
                            C.lower_median([r[9] for r in rs if r[9] is not None])])
    return games_table, suite_table


def main(argv=None):
    ap = argparse.ArgumentParser(description="G goal-identification cost (reported)")
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--truth-minigrid", default=os.path.join(REPO, "docs", "GROUND_TRUTH_minigrid.md"))
    ap.add_argument("--truth-procgen", default=os.path.join(REPO, "docs", "GROUND_TRUTH_procgen.md"))
    ap.add_argument("--out", default=os.path.join(REPO, "docs", "tables"))
    args = ap.parse_args(argv)

    rows = C.load_rows(args.runs)
    truth = {"minigrid": C.parse_truth_minigrid(args.truth_minigrid),
             "procgen": C.parse_truth_procgen(args.truth_procgen)}
    games_table, suite_table = g_rows(rows, truth)
    for r in games_table:
        print(f"{r[0]} {r[1]} {r[2]} seeds={r[3]} undefined={r[4]} G_end_place={r[5]} inf={r[6]} "
              f"G_end_feat={r[7]} inf={r[8]} G_act={r[9]}")
    for s in suite_table:
        print(f"suite {s[0]} {s[1]}: games={s[2]} G_end_place={s[3]} G_end_feat={s[4]} G_act={s[5]}")
    C.write_table(args.out, "g", ["suite", "condition", "game", "seeds", "undefined", "G_end_place", "inf_place",
                                  "G_end_feat", "inf_feat", "G_act"], games_table,
                  dict(note="G per docs/PREREG.md v1 Sections 6 and 10; reported, not tested.",
                       suite_summary=suite_table, runs=args.runs))
    print(f"wrote {os.path.join(args.out, 'g.md')}, {os.path.join(args.out, 'g.json')}")
    return games_table, suite_table


if __name__ == "__main__":
    main()
