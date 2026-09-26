"""
E9 REPORT (gate G3): applies docs/E9_protocol.md Sections 4-5 to the E9 rows.  No game is run.

    --e9  rows of the E9 run: modes hash_state (arm F), nav (arm N), nav_oracle (arm O), e.g.
          runs/navrun_e9_oracle_3x10.json
    --e2  the E2 file, e.g. runs/navrun_e2_hash_25x10.json (for check V1)

CHECKS (registered; the report refuses, prints every failure and writes nothing if V1-V4 or V6
fails; V5 is reported, never passed or failed):
  C0 every (game, arm, seed) present exactly once, no error rows
  V1 arm F rows equal E2's rows for these games and seeds (every field except "seconds")
  V2 (decision D1, docs/E9_protocol.md Section 8) on each testable game, over the levels won by
     arm O on which the oracle handed colours:
       oracle_confirmed == False  the level ended on a position without an oracle colour: FAILS V2
                                  and blocks the report
       missing or None            the planner could not read the ending (a click, the click scan,
                                  or no position after a fallback): "ending not seen" - NOT a
                                  failure; counted per game and per level for arm O, excluded from
                                  V2's denominator, and printed beside every result it affects
                                  (the V2 line, the per-level table, the classification line)
  V3 tu93: arm O's seed-mean levels completed is not below arm N's by 0.5 or more
  V4 every row used its full budget or won
  V5 per testable level: oracle-colour cells outside the target, and their components, from the
     level's first planner frame (reported per seed, min-max)
  V6 ls20 (NOT TESTABLE): arm O rows equal arm N rows (every field except "seconds")

MEASURES (Section 4), per game, arm and level; games are the unit, seeds nested, no pooling:
levels completed (seed mean); seeds winning the level; scorecard actions / human count over the
seeds that won it (median, range); level score (seed mean, unwon = 0); game score (seed mean).

PREDICTIONS (Section 5), per testable game, arms N and O:
  dL = O's seed-mean levels completed minus N's (whole game)
  eligible level  = a level on which arm O used an oracle colour (oracle_targets > 0) in at
                    least one seed; only eligible levels enter "shared" and "newly won"
  shared level    = eligible, won by both arms in >= 5 of 10 seeds (half the seeds, rounded up)
  newly won level = eligible, won by O in >= half the seeds and by N in fewer than half
  BINDING     dL >= 1.0, or a newly won level, or rO <= rN / 2 on a shared level
  NOT BINDING |dL| < 0.5, no newly won level, and rO > 0.75 rN on every shared level
  MIXED       otherwise;  NOT TESTABLE  no eligible level
  verdict over tu93 and dc22: both BINDING -> binding; both NOT BINDING -> not binding;
  otherwise inconclusive.  ls20 is reported as NOT TESTABLE, a finding (docs/E9_goals.md).

Commands (PowerShell, from D:\\Research\\arc3\\repo):

    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\e9_report.py --e9 runs\\navrun_e9_oracle_3x10.json --e2 runs\\navrun_e2_hash_25x10.json

EXPECTED OUTPUT: "C0 ... PASS", "V1 ... PASS", "V2 ... PASS", "V3 ... PASS", "V4 ... PASS",
"V6 ... PASS"; per game a per-level table for arms F, N, O with V5 beside arm O; per game the
classification with dL, shared and newly won levels; the verdict line; "wrote runs\\e9_report.json".
On a failed check: "STOP: <check> failed" with every failure, and nothing written.
Deterministic; takes seconds; an existing output is not overwritten without --force.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import statistics as st
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ARMS = {"F": "hash_state", "N": "nav", "O": "nav_oracle"}
TESTABLE = ["tu93", "dc22"]          # docs/E9_goals.md
NOT_TESTABLE = ["ls20"]
SOURCE_INFORMED = ["tu93", "dc22", "ls20"]


def sha256(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def strip(r):
    return json.dumps({k: v for k, v in r.items() if k != "seconds"}, sort_keys=True, default=str)


def load(path, games, seeds, modes):
    cells, errs = {}, []
    for r in json.load(open(path)):
        if r.get("game") not in games or r.get("mode") not in modes or r.get("seed") not in seeds:
            continue
        k = (r["game"], r["mode"], r["seed"])
        if r.get("error"):
            errs.append(f"{k} error row: {r['error'][:100]}")
        if k in cells:
            errs.append(f"{k} duplicate")
        cells[k] = r
    return cells, errs


def won(r, i):
    return int(r.get("levels", 0)) > i


def nav_levels(r):
    return {int(L["level"]): L for L in (r.get("nav") or {}).get("levels", [])}


def main():
    ap = argparse.ArgumentParser(description="E9 report (docs/E9_protocol.md Sections 4-5)")
    ap.add_argument("--e9", required=True)
    ap.add_argument("--e2", required=True)
    ap.add_argument("--games", default="tu93,dc22,ls20")
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--budget", type=int, default=20000)
    ap.add_argument("--out", default=os.path.join(REPO, "runs", "e9_report.json"))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    if os.path.exists(args.out) and not args.force:
        sys.exit(f"{args.out} exists; not overwritten without --force")
    games = args.games.split(",")
    seeds = list(range(1000, 1000 + args.seeds))
    half = math.ceil(len(seeds) / 2)
    testable = [g for g in games if g in TESTABLE]

    E9, e0 = load(args.e9, games, seeds, set(ARMS.values()))
    E2, _ = load(args.e2, games, seeds, {"hash_state"})
    fails = {}
    # C0
    c0 = list(e0)
    for g in games:
        for a, m in ARMS.items():
            for s in seeds:
                if (g, m, s) not in E9:
                    c0.append(f"missing {(g, m, s)}")
    fails["C0 complete rows"] = c0
    if c0:
        report_and_stop(fails)
    # V1
    fails["V1 arm F equals E2"] = [f"{g} seed {s}: differs from E2" if (g, "hash_state", s) in E2 else
                                   f"{g} seed {s}: not in E2"
                                   for g in games for s in seeds
                                   if (g, "hash_state", s) not in E2
                                   or strip(E9[(g, "hash_state", s)]) != strip(E2[(g, "hash_state", s)])]
    # V2 (decision D1): only a False blocks; an ending not seen is counted and excluded
    v2 = []
    not_seen = {g: {} for g in testable}            # game -> {level (1-based): [seeds]}
    v2_counts = {g: dict(wins_with_oracle=0, confirmed=0, not_seen=0) for g in testable}
    for g in testable:
        for s in seeds:
            r = E9[(g, "nav_oracle", s)]
            lv = nav_levels(r)
            for i in range(int(r.get("levels", 0))):
                L = lv.get(i, {})
                if not L.get("oracle_colours"):
                    continue                        # the oracle handed nothing on this level
                v2_counts[g]["wins_with_oracle"] += 1
                ok = L.get("oracle_confirmed", None)
                if ok is False:
                    v2.append(f"{g} seed {s} level {i + 1}: won on a position WITHOUT an oracle colour")
                elif ok is True:
                    v2_counts[g]["confirmed"] += 1
                else:
                    v2_counts[g]["not_seen"] += 1
                    not_seen[g].setdefault(i + 1, []).append(s)
    fails["V2 level ends on an oracle colour"] = v2
    # V3
    v3 = []
    if "tu93" in games:
        mN = st.mean(int(E9[("tu93", "nav", s)]["levels"]) for s in seeds)
        mO = st.mean(int(E9[("tu93", "nav_oracle", s)]["levels"]) for s in seeds)
        if mO <= mN - 0.5:
            v3.append(f"tu93: arm O levels {mO:.2f} vs arm N {mN:.2f} (positive control failed)")
    if "tu93" in games:
        fails["V3 positive control tu93"] = v3
    # V4
    fails["V4 full budget or win"] = [f"{k}: {r.get('actions')} actions, state {r.get('state')}"
                                      for k, r in E9.items()
                                      if not (int(r.get("actions", -1)) == args.budget or r.get("state") == "WIN")]
    # V6
    if "ls20" in games:
        fails["V6 ls20 arm O equals arm N"] = [f"ls20 seed {s}: arm O row differs from arm N" for s in seeds
                                               if strip(E9[("ls20", "nav_oracle", s)]) != strip(E9[("ls20", "nav", s)])]
    if any(v for v in fails.values()):
        report_and_stop(fails)
    for k in fails:
        print(f"{k} ... PASS")
        if k.startswith("V2"):
            for g in testable:
                c = v2_counts[g]
                print(f"    {g}: {c['confirmed']} of {c['wins_with_oracle'] - c['not_seen']} seen endings on an "
                      f"oracle colour; {c['not_seen']} ending(s) not seen, excluded from V2"
                      + (f" (levels: {', '.join(f'{lv} x{len(v)}' for lv, v in sorted(not_seen[g].items()))})"
                         if c['not_seen'] else ""))
    for k, g in (("V3 positive control tu93", "tu93"), ("V6 ls20 arm O equals arm N", "ls20")):
        if g not in games:
            print(f"{k} ... not applicable ({g} not in --games)")

    out = dict(script="scripts/e9_report.py", protocol="docs/E9_protocol.md", goals="docs/E9_goals.md",
               created=time.strftime("%Y-%m-%d %H:%M:%S"),
               inputs=dict(e9=dict(path=args.e9, sha256=sha256(args.e9)), e2=dict(path=args.e2, sha256=sha256(args.e2))),
               seeds=seeds, budget=args.budget, source_informed=SOURCE_INFORMED,
               checks={k: "PASS" for k in fails},
               v2=dict(decision="D1 (docs/E9_protocol.md Section 8)", counts=v2_counts,
                       ending_not_seen={g: {str(k): v for k, v in d.items()} for g, d in not_seen.items()}),
               games={})
    for g in games:
        base = E9[(g, "hash_state", seeds[0])].get("card_baseline") or []
        nlev = len(base)
        rows = {a: [E9[(g, m, s)] for s in seeds] for a, m in ARMS.items()}
        gm = dict(n_levels=nlev, arms={}, per_level=[])
        print(f"\n=== {g}{' (source-informed)' if g in SOURCE_INFORMED else ''}"
              f"{'  NOT TESTABLE (finding: predicate not a place, docs/E9_goals.md)' if g in NOT_TESTABLE else ''}")
        for a in ARMS:
            gm["arms"][a] = dict(levels_mean=st.mean(int(r["levels"]) for r in rows[a]),
                                 score_mean=st.mean(float(r.get("score", 0.0)) for r in rows[a]))
            print(f"  arm {a} ({ARMS[a]:10}) levels completed {gm['arms'][a]['levels_mean']:.2f}  "
                  f"game score {gm['arms'][a]['score_mean']:.4f}")
        print(f"  {'lvl':>3} {'human':>5} | " + " | ".join(f"arm {a}: won  ratio med [range]  lvscore" for a in ARMS)
              + " | O oracle_targets seeds  V5 cells/comps  O ending not seen (excluded from V2)")
        for i in range(nlev):
            h = base[i]
            row = dict(level=i + 1, human=h, arms={})
            parts = []
            for a in ARMS:
                wins = [r for r in rows[a] if won(r, i)]
                ratios = [r["card_levels"][i] / h for r in wins if r.get("card_levels") and h]
                lsc = st.mean((r.get("card_scores") or [0] * nlev)[i] if won(r, i) else 0.0 for r in rows[a])
                row["arms"][a] = dict(won=len(wins), ratio_median=st.median(ratios) if ratios else None,
                                      ratio_min=min(ratios) if ratios else None,
                                      ratio_max=max(ratios) if ratios else None, level_score_mean=lsc)
                rtxt = (f"{st.median(ratios):6.1f} [{min(ratios):.1f}-{max(ratios):.1f}]" if ratios else "     -")
                parts.append(f"{len(wins):2}/{len(seeds)} {rtxt:>18} {lsc:7.3f}")
            used = [s for s, r in zip(seeds, rows["O"]) if nav_levels(r).get(i, {}).get("oracle_targets", 0) > 0]
            v5 = [nav_levels(r).get(i, {}).get("oracle_ambiguity") for r in rows["O"]]
            v5 = [x for x in v5 if x]
            row["oracle_targets_seeds"] = len(used)
            ns = not_seen.get(g, {}).get(i + 1, [])
            row["ending_not_seen_seeds"] = ns
            row["v5"] = (dict(cells_min=min(x["cells"] for x in v5), cells_max=max(x["cells"] for x in v5),
                              components_min=min(x["components"] for x in v5),
                              components_max=max(x["components"] for x in v5), seeds=len(v5)) if v5 else None)
            v5txt = (f"{row['v5']['cells_min']}-{row['v5']['cells_max']} / "
                     f"{row['v5']['components_min']}-{row['v5']['components_max']}" if v5 else "-")
            print(f"  {i + 1:>3} {h:>5} | " + " | ".join(parts) + f" | {len(used):2}/{len(seeds)}  {v5txt}"
                  + (f"  {len(ns)} seed(s) {ns}" if ns else ""))
            gm["per_level"].append(row)
        # classification (Section 5)
        if g in testable:
            dL = gm["arms"]["O"]["levels_mean"] - gm["arms"]["N"]["levels_mean"]
            elig = [row for row in gm["per_level"] if row["oracle_targets_seeds"] > 0]
            shared = [row for row in elig if row["arms"]["N"]["won"] >= half and row["arms"]["O"]["won"] >= half]
            newly = [row for row in elig if row["arms"]["O"]["won"] >= half and row["arms"]["N"]["won"] < half]
            halved = [row for row in shared if row["arms"]["O"]["ratio_median"] <= row["arms"]["N"]["ratio_median"] / 2]
            small = all(row["arms"]["O"]["ratio_median"] > 0.75 * row["arms"]["N"]["ratio_median"] for row in shared)
            if not elig:
                cls = "NOT TESTABLE"
            elif dL >= 1.0 or newly or halved:
                cls = "BINDING"
            elif abs(dL) < 0.5 and not newly and small:
                cls = "NOT BINDING"
            else:
                cls = "MIXED"
            gm["classification"] = dict(result=cls, dL=dL, eligible_levels=[r["level"] for r in elig],
                                        shared_levels=[r["level"] for r in shared],
                                        newly_won_levels=[r["level"] for r in newly],
                                        halved_levels=[r["level"] for r in halved],
                                        v2_endings_not_seen=v2_counts[g]["not_seen"])
            print(f"  -> {cls}: dL = {dL:+.2f}; eligible levels {[r['level'] for r in elig]}; shared "
                  f"{[r['level'] for r in shared]}; newly won {[r['level'] for r in newly]}; "
                  f"actions halved on {[r['level'] for r in halved]}"
                  f"; V2: {v2_counts[g]['not_seen']} arm-O ending(s) not seen, excluded")
        else:
            gm["classification"] = dict(result="NOT TESTABLE (finding)")
        out["games"][g] = gm
    cl = [out["games"][g]["classification"]["result"] for g in TESTABLE if g in out["games"]]
    if len(cl) == 2 and all(c == "BINDING" for c in cl):
        verdict = "BINDING: goal identification is the binding constraint for this instrument on tu93 and dc22"
    elif len(cl) == 2 and all(c == "NOT BINDING" for c in cl):
        verdict = "NOT BINDING: goal identification is not the binding constraint for this instrument on tu93 and dc22"
    else:
        verdict = f"INCONCLUSIVE ({dict(zip([g for g in TESTABLE if g in out['games']], cl))})"
    out["verdict"] = verdict
    print(f"\nVERDICT: {verdict}")
    print("(two source-informed train games; no general claim - docs/E9_protocol.md Section 6)")
    tmp = args.out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=1)
    os.replace(tmp, args.out)
    print(f"wrote {args.out}")


def report_and_stop(fails):
    for k, v in fails.items():
        print(f"{k} ... {'PASS' if not v else 'FAIL'}")
    for k, v in fails.items():
        if v:
            print(f"\nSTOP: {k} failed ({len(v)}):")
            for x in v:
                print("   " + x)
    print("\nNothing written.")
    sys.exit(1)


if __name__ == "__main__":
    main()
