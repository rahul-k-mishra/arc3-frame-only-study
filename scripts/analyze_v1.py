"""
V1 — instrument validity (docs/PREREG.md v1, Section 10).  Registered analysis; frozen at the tag.

For every (suite, condition) present in the run rows, the census verdict of each confirmatory game
is the seed-majority of the N rows' census (analyze_common.majority), compared with the source-
derived truth (docs/GROUND_TRUTH_minigrid.md, docs/GROUND_TRUTH_procgen.md), per assumption A1-A5:
    agreement  share of games where census == truth (undetermined never agrees)
    kappa      Cohen's kappa, only if both truth values have >= 3 games (constant-column rule)
    verdict    PASS if agreement >= 0.90 and (kappa >= 0.70 or kappa not defined);
               FAIL if agreement < 0.75; otherwise neither
Suite C is reported on all 14 confirmatory games and again on the in-range subset (Section 4).
Suite B uses A3-raw truth for condition "raw" and A3-macro truth for "macro".  ARC V1 (8 train games,
development) is computed only if --truth-arc names a table; none exists at v1.

Reads no game.  Writes docs/tables/v1.md and docs/tables/v1.json (or --out).

Command (PowerShell, from D:\\Research\\arc3\\repo):

    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\analyze_v1.py --runs "runs\\prereg_*.json"

EXPECTED OUTPUT (shape): one line per (suite, condition, subset, assumption):
    minigrid macro all A2 n=161 truth_holds=161 agreement=... kappa=None verdict=...
    ...
    wrote docs\\tables\\v1.md, docs\\tables\\v1.json
"""
from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analyze_common as C  # noqa: E402


def v1_rows(rows, truth_by_suite):
    out = []
    conds = sorted({(r.get("suite"), r.get("condition")) for r in rows if r.get("agent") == "N"})
    for suite, cond in conds:
        truth = truth_by_suite.get(suite)
        if truth is None:
            continue
        census = C.census_by_game(rows, suite, cond)
        games = [g for g in C.confirmatory(suite, truth) if g in census] if suite != "arc" \
            else [g for g in C.ARC_TRAIN if g in census and g in truth]
        subsets = [("all", games)]
        if suite == "procgen":
            subsets.append(("in_range", [g for g in games if g in C.IN_RANGE_C]))
        for name, gs in subsets:
            for a in C.ASSUMPTIONS:
                t = [C.truth_for(suite, cond, truth[g], a) for g in gs]
                p = [census[g][a] for g in gs]
                agree, kappa = C.agreement_kappa(t, p)
                out.append([suite, cond, name, a, len(gs), sum(x == C.HOLDS for x in t), agree, kappa,
                            C.v1_verdict(agree, kappa)])
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="V1 instrument validity")
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--truth-minigrid", default=os.path.join(REPO, "docs", "GROUND_TRUTH_minigrid.md"))
    ap.add_argument("--truth-procgen", default=os.path.join(REPO, "docs", "GROUND_TRUTH_procgen.md"))
    ap.add_argument("--truth-arc", default=None)
    ap.add_argument("--out", default=os.path.join(REPO, "docs", "tables"))
    args = ap.parse_args(argv)

    rows = C.load_rows(args.runs)
    truth = {"minigrid": C.parse_truth_minigrid(args.truth_minigrid),
             "procgen": C.parse_truth_procgen(args.truth_procgen)}
    if args.truth_arc:
        truth["arc"] = C.parse_truth_procgen(args.truth_arc)
    table = v1_rows(rows, truth)
    for r in table:
        print(f"{r[0]} {r[1]} {r[2]} {r[3]} n={r[4]} truth_holds={r[5]} agreement="
              f"{'None' if r[6] is None else f'{r[6]:.4f}'} kappa={'None' if r[7] is None else f'{r[7]:.4f}'} "
              f"verdict={r[8]}")
    C.write_table(args.out, "v1", ["suite", "condition", "subset", "assumption", "n", "truth_holds",
                                   "agreement", "kappa", "verdict"], table,
                  dict(note="V1 per docs/PREREG.md v1 Section 10; kappa only where both truth values have >= 3 games.",
                       runs=args.runs))
    print(f"wrote {os.path.join(args.out, 'v1.md')}, {os.path.join(args.out, 'v1.json')}")
    return table


if __name__ == "__main__":
    main()
