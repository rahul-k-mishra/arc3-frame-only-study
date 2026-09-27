"""
V2 — predictive validity (docs/PREREG.md v1, Section 10).  Registered analysis; frozen at the tag.

For every (suite, condition, agent) present in the run rows, over the confirmatory games of that
suite (and, for suite C, again over the in-range subset):
    S     census score: number of A1-A5 whose seed-majority census verdict is "holds" (N rows, same
          suite and condition); A5 "undetermined" counts as not holding
    P     prediction: A2, A3, A4 and A5 all hold
    Y     game outcome: the agent completed level 1 in at least half of its seeds
    precondition   share of games with Y = 1 in [0.10, 0.90]; outside it the test is VOID
    AUROC(S -> Y), percentile 95% CI from 2,000 bootstrap resamples of games (seed 20260927,
          worker pool), balanced accuracy of P, AUROC of the nuisance baseline B (logistic
          regression on grid area, action count, colour count; analyze_common.logistic_fit_predict)
    verdict  VOID; PASS if AUROC >= 0.80 and CI low > 0.60 and BA >= 0.80 and AUROC - AUROC_B >= 0.10;
             FAIL if AUROC <= 0.65; otherwise neither
Evidence agents are R and I1; N's rows are labelled "instrument check" (circular: N uses A1-A5).
Suite-level FAIL: both R and I1 non-void with AUROC <= 0.65.  ARC held-out rows are reported, not
tested (the script labels suite "arc" as "reported").

Reads no game.  Writes docs/tables/v2.md and docs/tables/v2.json (or --out).

Command (PowerShell, from D:\\Research\\arc3\\repo):

    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\analyze_v2.py --runs "runs\\prereg_*.json" --workers 8

EXPECTED OUTPUT (shape): one line per (suite, condition, subset, agent), then one suite line each:
    minigrid macro all R n=161 pos=... auroc=... ci=[..., ...] ba=... auroc_B=... verdict=...
    suite minigrid macro all: R ..., I1 ... -> suite FAIL / not failed
    wrote docs\\tables\\v2.md, docs\\tables\\v2.json
"""
from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analyze_common as C  # noqa: E402


def game_table(rows, suite, cond, agent, games, census):
    """Per game: (S, P, Y, features) for games with both census and agent rows."""
    by = {}
    for r in rows:
        if r.get("suite") == suite and r.get("condition") == cond and r.get("agent") == agent and r["game"] in games:
            by.setdefault(r["game"], []).append(r)
    out = []
    for g in games:
        if g not in by or g not in census:
            continue
        rs = by[g]
        cv = census[g]
        S = sum(cv[a] == C.HOLDS for a in C.ASSUMPTIONS)
        P = all(cv[a] == C.HOLDS for a in ("A2", "A3", "A4", "A5"))
        Y = 2 * sum(bool(r.get("level1_completed")) for r in rs) >= len(rs)
        ad = [r.get("adapter") or {} for r in rs]
        feats = [sum((a.get("grid") or [0, 0])[0] * (a.get("grid") or [0, 0])[1] for a in ad) / len(ad),
                 sum(len(a.get("action_list") or []) for a in ad) / len(ad),
                 sum(a.get("n_colours") or 0 for a in ad) / len(ad)]
        out.append((g, S, P, Y, feats))
    return out


def v2_stats(gt, n_resamples=2000, seed=20260927, workers=8):
    S = [x[1] for x in gt]
    P = [x[2] for x in gt]
    Y = [x[3] for x in gt]
    n = len(gt)
    pos = sum(Y)
    share = pos / n if n else None
    void = (n == 0) or not (0.10 <= share <= 0.90)
    a = C.auroc(S, Y)
    lo, hi, skipped = (None, None, None) if void or a is None else C.bootstrap_auroc_ci(S, Y, n_resamples, seed, workers)
    ba = C.balanced_accuracy(P, Y)
    pb = C.logistic_fit_predict([x[4] for x in gt], [int(y) for y in Y]) if n else []
    ab = C.auroc(list(pb), Y) if n else None
    if void:
        verdict = "VOID"
    elif a is not None and a >= 0.80 and lo is not None and lo > 0.60 and ba is not None and ba >= 0.80 \
            and ab is not None and a - ab >= 0.10:
        verdict = "PASS"
    elif a is not None and a <= 0.65:
        verdict = "FAIL"
    else:
        verdict = "neither"
    return dict(n=n, pos=pos, share=share, auroc=a, ci_low=lo, ci_high=hi, skipped=skipped, ba=ba,
                auroc_B=ab, verdict=verdict)


def v2_rows(rows, truth_by_suite, n_resamples=2000, seed=20260927, workers=8):
    table, suite_lines = [], []
    keys = sorted({(r.get("suite"), r.get("condition"), r.get("agent")) for r in rows if r.get("agent")})
    for suite, cond in sorted({(k[0], k[1]) for k in keys}):
        census = C.census_by_game(rows, suite, cond)
        if suite == "arc":
            games = sorted(census)
        else:
            truth = truth_by_suite.get(suite)
            if truth is None:
                continue
            games = C.confirmatory(suite, truth)
        subsets = [("all", games)]
        if suite == "procgen":
            subsets.append(("in_range", [g for g in games if g in C.IN_RANGE_C]))
        for name, gs in subsets:
            per_agent = {}
            for agent in sorted(k[2] for k in keys if k[0] == suite and k[1] == cond):
                gt = game_table(rows, suite, cond, agent, gs, census)
                st = v2_stats(gt, n_resamples, seed, workers)
                role = "reported" if suite == "arc" else ("evidence" if agent in ("R", "I1") else "instrument check")
                per_agent[agent] = st
                table.append([suite, cond, name, agent, role, st["n"], st["pos"], st["auroc"], st["ci_low"],
                              st["ci_high"], st["ba"], st["auroc_B"], st["verdict"]])
            r, i1 = per_agent.get("R"), per_agent.get("I1")
            if suite == "arc":
                sv = "reported, not tested"
            elif r and i1 and r["verdict"] != "VOID" and i1["verdict"] != "VOID" \
                    and r["auroc"] is not None and i1["auroc"] is not None and r["auroc"] <= 0.65 and i1["auroc"] <= 0.65:
                sv = "suite FAIL"
            elif i1 is None:
                sv = "not failed (I1 absent: the suite-level FAIL rule needs both R and I1)"
            else:
                sv = "not failed"
            suite_lines.append([suite, cond, name, sv])
    return table, suite_lines


def main(argv=None):
    ap = argparse.ArgumentParser(description="V2 predictive validity")
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--truth-minigrid", default=os.path.join(REPO, "docs", "GROUND_TRUTH_minigrid.md"))
    ap.add_argument("--truth-procgen", default=os.path.join(REPO, "docs", "GROUND_TRUTH_procgen.md"))
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--resamples", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20260927)
    ap.add_argument("--out", default=os.path.join(REPO, "docs", "tables"))
    args = ap.parse_args(argv)

    rows = C.load_rows(args.runs)
    truth = {"minigrid": C.parse_truth_minigrid(args.truth_minigrid),
             "procgen": C.parse_truth_procgen(args.truth_procgen)}
    table, suite_lines = v2_rows(rows, truth, args.resamples, args.seed, args.workers)
    f = lambda v: "None" if v is None else f"{v:.4f}"  # noqa: E731
    for r in table:
        print(f"{r[0]} {r[1]} {r[2]} {r[3]} ({r[4]}) n={r[5]} pos={r[6]} auroc={f(r[7])} ci=[{f(r[8])}, {f(r[9])}] "
              f"ba={f(r[10])} auroc_B={f(r[11])} verdict={r[12]}")
    for s in suite_lines:
        print(f"suite {s[0]} {s[1]} {s[2]}: {s[3]}")
    C.write_table(args.out, "v2", ["suite", "condition", "subset", "agent", "role", "n", "positives", "auroc",
                                   "ci_low", "ci_high", "balanced_acc", "auroc_B", "verdict"], table,
                  dict(note="V2 per docs/PREREG.md v1 Section 10.", suite_lines=suite_lines, runs=args.runs,
                       resamples=args.resamples, seed=args.seed))
    print(f"wrote {os.path.join(args.out, 'v2.md')}, {os.path.join(args.out, 'v2.json')}")
    return table, suite_lines


if __name__ == "__main__":
    main()
