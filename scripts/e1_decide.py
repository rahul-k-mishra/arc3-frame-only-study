"""
E1 DECISION: applies docs/TOG_PLAN_v2.md Section 3 (3.2 measures, 3.3 rule) to one external agent.
No game is run.  Written 25 Sep 2026 before any phase-2 result or E2 output was read.

    --agent      rows of the external agent (ablate format), e.g. runs/e1_rudakov_lenovo_25x10_20k.json
    --reference  rows of our explorer at 10 seeds (E2), e.g. runs/navrun_e2_hash_25x10.json;
                 only rows of --reference-mode (default hash_state) are used

MEASURES (3.2), held-out games only (17), games the unit, seeds nested within games:
    M1  mean over games of the seed-mean recorded scorecard "score"
    M2  AT HUMAN: the same runs with every won level at exactly the human count, same won levels,
        no extra level; mean over games of seed means; and M2/M1 ("M1 = 0" if M1 is 0)
    M3  number of held-out (game, seed) runs that won level 3 or later (levels >= 3)
    M4  sum over the 17 games of the seed-mean levels completed
AT HUMAN is computed from each row's card_baseline (the scorecard's human counts) with the
scorecard rule (arc_agi/scorecard.py; derived in TOG_PLAN_v2 Section 5): a run that completed the
first k of N levels at the human count scores 100 * k(k+1) / (N(N+1)).  Levels are completed in
order, so "levels" = k identifies the won levels.

RULE (3.3, verbatim):
    REPRODUCES if all of: (i) M1 < 0.5; (ii) M2 / M1 > 5; (iii) M3 = 0.
    BREAKS if any of: (iv) M1 >= 1.0 (three times our 0.3329, rounded up);
        (v) level 3 or later won on at least 2 held-out games, each in at least half of that
            agent's seeds;
        (vi) M4 at least twice our E2 value of M4.
    INCONCLUSIVE otherwise (for example M1 = 0.6, or a single lucky lv3 win), or if the agent
    could not produce per-level scorecard counts.
PRECEDENCE (plan 3.3, added 25 Sep 2026, decided before any phase-2 result was read): BREAKS
takes precedence over REPRODUCES.  If any of (iv)-(vi) holds, the label is BREAKS even when
(i)-(iii) also hold; the output then lists both condition sets with their values.  The rule's
last clause (no per-level scorecard counts -> INCONCLUSIVE) is checked first (plan 3.3).  No
threshold is changed.

The decision uses the point values.  The 95% intervals are hierarchical bootstrap percentiles
(resample the 17 games with replacement, then seeds within each resampled game; 10,000 draws,
numpy default_rng(20260925)); they describe variation within this set of games and do not enter
the rule.  The 8 train games are reported beside (tu93, dc22, ls20 marked source-informed) and do
not enter the rule.  Games where ACTION7 is unavailable to the E1a agent are marked (docs/
E1_phase2_protocol.md 2.2).

CHECKS (the script stops, and writes nothing, if one fails):
    every held-out game has the same set of seeds in the agent file, and in the reference file;
    no duplicate (game, seed); no error rows among the used rows;
    every used row ran the full budget (--budget, default 20000) or won the game;
    the seed count is reported, and a result from fewer than 10 seeds is labelled as such.
If any agent row lacks card_levels / card_baseline, the outcome is INCONCLUSIVE by the rule's last
clause.

No --workers: the bootstrap takes seconds.  Output written atomically; an existing output is not
overwritten without --force.

Command (PowerShell, from D:\\Research\\arc3\\repo):

    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\e1_decide.py --agent runs\\e1_rudakov_lenovo_25x10_20k.json --reference runs\\navrun_e2_hash_25x10.json

EXPECTED OUTPUT (shape): the files and seed counts; a per-game table (agent and reference seed
means of score and levels, seeds with level >= 3); M1-M4 side by side with 95% intervals; each
condition (i)-(vi) with its values and TRUE/FALSE; one line
    DECISION: REPRODUCES | BREAKS | INCONCLUSIVE  -  decided by <conditions>
and "wrote runs\\e1_decision.json".
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TRAIN = ["tu93", "ls20", "vc33", "m0r0", "ft09", "lp85", "lf52", "dc22"]
HELD_OUT = ["ar25", "bp35", "cd82", "cn04", "g50t", "ka59", "r11l", "re86", "s5i5",
            "sb26", "sc25", "sk48", "sp80", "su15", "tn36", "tr87", "wa30"]
SOURCE_INFORMED = ["tu93", "dc22", "ls20"]
NO_ACTION7 = ["ar25", "bp35", "sb26", "sk48", "su15", "lf52"]
BOOT, BOOT_SEED = 10000, 20260925
RULE_TEXT = {
    "i": "M1 < 0.5", "ii": "M2 / M1 > 5", "iii": "M3 = 0",
    "iv": "M1 >= 1.0 (three times our 0.3329, rounded up)",
    "v": "level 3 or later won on at least 2 held-out games, each in at least half of that agent's seeds",
    "vi": "M4 at least twice our E2 value of M4",
}


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def at_human(k, n):
    """Scorecard score of a run that completed the first k of n levels at the human count."""
    return 100.0 * k * (k + 1) / (n * (n + 1)) if n else 0.0


def load(path, mode, budget, games, label):
    rows = [r for r in json.load(open(path)) if r.get("mode") == mode and r.get("game") in games]
    if not rows:
        sys.exit(f"STOP {label}: no rows of mode {mode!r} for these games in {path}")
    errs = [r for r in rows if r.get("error")]
    if errs:
        sys.exit(f"STOP {label}: {len(errs)} error rows, e.g. {errs[0]['game']} seed {errs[0]['seed']}")
    cells = defaultdict(dict)
    for r in rows:
        k = (r["game"], int(r["seed"]))
        if k[1] in cells[k[0]]:
            sys.exit(f"STOP {label}: duplicate row {k}")
        full = int(r.get("budget", budget)) == budget and (
            int(r.get("actions", -1)) == budget or r.get("state") == "WIN")
        if not full:
            sys.exit(f"STOP {label}: {k} did not run the {budget}-action budget "
                     f"(actions {r.get('actions')}, state {r.get('state')}, budget {r.get('budget')})")
        cells[k[0]][k[1]] = r
    missing = [g for g in games if g not in cells]
    if missing:
        sys.exit(f"STOP {label}: no rows for {missing}")
    seedsets = {g: tuple(sorted(cells[g])) for g in games}
    if len(set(seedsets.values())) != 1:
        sys.exit(f"STOP {label}: games have different seed sets: "
                 + ", ".join(f"{g} {s}" for g, s in seedsets.items() if s != seedsets[games[0]]))
    return cells, list(seedsets[games[0]])


def arrays(cells, games, seeds):
    """score[g, s], levels[g, s], athuman[g, s], card_ok"""
    G, S = len(games), len(seeds)
    sc, lv, ah = np.zeros((G, S)), np.zeros((G, S)), np.zeros((G, S))
    card_ok = True
    for i, g in enumerate(games):
        for j, s in enumerate(seeds):
            r = cells[g][s]
            sc[i, j] = float(r.get("score", 0.0))
            lv[i, j] = int(r.get("levels", 0))
            base = r.get("card_baseline")
            if not r.get("card_levels") or not base:
                card_ok = False
                ah[i, j] = np.nan
            else:
                ah[i, j] = at_human(int(lv[i, j]), len(base))
    return sc, lv, ah, card_ok


def measures(sc, lv, ah):
    m1 = float(sc.mean(axis=1).mean())
    m2 = float(np.nanmean(ah, axis=1).mean()) if not np.isnan(ah).all() else float("nan")
    m3 = int((lv >= 3).sum())
    m4 = float(lv.mean(axis=1).sum())
    ratio = m2 / m1 if m1 > 0 else float("nan")
    return dict(M1=m1, M2=m2, M2_over_M1=ratio, M3=m3, M4=m4)


def bootstrap(sc, lv, ah):
    rng = np.random.default_rng(BOOT_SEED)
    G, S = sc.shape
    out = defaultdict(list)
    for _ in range(BOOT):
        gi = rng.integers(0, G, G)
        si = rng.integers(0, S, (G, S))
        rows = np.arange(G)[:, None]
        m = measures(sc[gi][rows, si], lv[gi][rows, si], ah[gi][rows, si])
        for k, v in m.items():
            out[k].append(v)
    ci = {}
    for k, v in out.items():
        a = np.array(v, float)
        a = a[~np.isnan(a)]
        ci[k] = [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))] if len(a) else None
    return ci


def fmt(v, ci=None, d=4):
    if isinstance(v, float) and np.isnan(v):
        s = "undefined"
    else:
        s = f"{v:.{d}f}" if isinstance(v, float) else str(v)
    if ci:
        s += f" [{ci[0]:.{d}f}, {ci[1]:.{d}f}]"
    return s


def main():
    ap = argparse.ArgumentParser(description="E1 decision rule (TOG_PLAN_v2 Section 3)")
    ap.add_argument("--agent", required=True)
    ap.add_argument("--reference", required=True)
    ap.add_argument("--agent-mode", default="rudakov")
    ap.add_argument("--reference-mode", default="hash_state")
    ap.add_argument("--budget", type=int, default=20000)
    ap.add_argument("--out", default=os.path.join(REPO, "runs", "e1_decision.json"))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    if os.path.exists(args.out) and not args.force:
        sys.exit(f"{args.out} exists; not overwritten without --force")

    a_cells, a_seeds = load(args.agent, args.agent_mode, args.budget, HELD_OUT, "agent")
    r_cells, r_seeds = load(args.reference, args.reference_mode, args.budget, HELD_OUT, "reference")
    print(f"agent     {args.agent} mode {args.agent_mode}: 17 held-out games x {len(a_seeds)} seeds {a_seeds}")
    print(f"reference {args.reference} mode {args.reference_mode}: 17 held-out games x {len(r_seeds)} seeds {r_seeds}")
    for lab, s in (("agent", a_seeds), ("reference", r_seeds)):
        if len(s) < 10:
            print(f"NOTE: {lab} has {len(s)} seeds; the registered protocol is 10 - every number below is "
                  f"labelled '{len(s)} seeds'")

    a_sc, a_lv, a_ah, a_card = arrays(a_cells, HELD_OUT, a_seeds)
    r_sc, r_lv, r_ah, r_card = arrays(r_cells, HELD_OUT, r_seeds)
    A, R = measures(a_sc, a_lv, a_ah), measures(r_sc, r_lv, r_ah)
    Aci, Rci = bootstrap(a_sc, a_lv, a_ah), bootstrap(r_sc, r_lv, r_ah)

    # per-game table
    print(f"\n{'game':6} {'agent score':>11} {'levels':>6} {'lv3+ seeds':>10}   {'ref score':>9} {'levels':>6} "
          f"{'lv3+ seeds':>10}  notes")
    per_game = {}
    for i, g in enumerate(HELD_OUT):
        a3, r3 = int((a_lv[i] >= 3).sum()), int((r_lv[i] >= 3).sum())
        note = "ACTION7 unavailable to E1a agent" if g in NO_ACTION7 else ""
        print(f"{g:6} {a_sc[i].mean():11.4f} {a_lv[i].mean():6.2f} {a3:6}/{len(a_seeds):<3}   "
              f"{r_sc[i].mean():9.4f} {r_lv[i].mean():6.2f} {r3:6}/{len(r_seeds):<3}  {note}")
        per_game[g] = dict(agent_score=float(a_sc[i].mean()), agent_levels=float(a_lv[i].mean()),
                           agent_lv3_seeds=a3, ref_score=float(r_sc[i].mean()),
                           ref_levels=float(r_lv[i].mean()), ref_lv3_seeds=r3,
                           action7_unavailable=g in NO_ACTION7)

    print(f"\n{'measure':10} {'agent (95% interval over games, seeds nested)':>48}   {'reference (E2)':>40}")
    for k in ("M1", "M2", "M2_over_M1", "M3", "M4"):
        print(f"{k:10} {fmt(A[k], Aci.get(k)):>48}   {fmt(R[k], Rci.get(k)):>40}")

    # the rule, verbatim, on point values
    half = len(a_seeds) / 2
    v_games = [g for i, g in enumerate(HELD_OUT) if (a_lv[i] >= 3).sum() >= half]
    cond = {
        "i": A["M1"] < 0.5,
        "ii": (A["M1"] > 0) and (A["M2"] / A["M1"] > 5),
        "iii": A["M3"] == 0,
        "iv": A["M1"] >= 1.0,
        "v": len(v_games) >= 2,
        "vi": A["M4"] >= 2 * R["M4"],
    }
    vals = {
        "i": f"M1 = {A['M1']:.4f}",
        "ii": "M1 = 0" if A["M1"] == 0 else f"M2 / M1 = {A['M2']:.4f} / {A['M1']:.4f} = {A['M2'] / A['M1']:.2f}",
        "iii": f"M3 = {A['M3']}",
        "iv": f"M1 = {A['M1']:.4f}",
        "v": f"games with level >= 3 in >= half ({half:g}) of the seeds: {v_games or 'none'}",
        "vi": f"M4 = {A['M4']:.2f} vs 2 x E2 M4 = 2 x {R['M4']:.2f} = {2 * R['M4']:.2f}",
    }
    print()
    for c in ("i", "ii", "iii", "iv", "v", "vi"):
        print(f"({c:3}) {RULE_TEXT[c]:95} {vals[c]:60} {'TRUE' if cond[c] else 'FALSE'}")

    reproduces = cond["i"] and cond["ii"] and cond["iii"]
    breaks = [c for c in ("iv", "v", "vi") if cond[c]]
    if not a_card:
        decision, by = "INCONCLUSIVE", "the agent could not produce per-level scorecard counts (rows without card_levels / card_baseline)"
    elif breaks:
        # precedence (TOG_PLAN_v2 3.3, added 25 Sep 2026 before any phase-2 result was read):
        # any BREAKS condition decides, even when (i)-(iii) also hold
        by = "BREAKS (" + "; ".join(f"{c}: {vals[c]}" for c in breaks) + ")"
        if reproduces:
            by += (" - the REPRODUCES conditions also hold (" + "; ".join(f"{c}: {vals[c]}" for c in
                                                                    ("i", "ii", "iii"))
                   + "); BREAKS takes precedence (plan 3.3)")
        decision = "BREAKS"
    elif reproduces:
        decision, by = "REPRODUCES", "(i), (ii) and (iii) all true"
    else:
        missed = [c for c in ("i", "ii", "iii") if not cond[c]]
        decision, by = "INCONCLUSIVE", f"REPRODUCES fails on ({', '.join(missed)}); no BREAKS condition holds"
    label = "" if len(a_seeds) >= 10 else f" [{len(a_seeds)} seeds, below the registered 10]"
    print(f"\nDECISION: {decision}{label}  -  decided by {by}")
    print("(point values decide; intervals are descriptive.  Train games do not enter the rule.)")

    # train games beside, not in the rule
    train = {}
    for lab, path, mode, cells in (("agent", args.agent, args.agent_mode, None),
                                   ("reference", args.reference, args.reference_mode, None)):
        try:
            c, s = load(path, mode, args.budget, TRAIN, lab + " (train)")
            sc, lv, ah, _ = arrays(c, TRAIN, s)
            train[lab] = dict(seeds=s, measures=measures(sc, lv, ah),
                              per_game={g: dict(score=float(sc[i].mean()), levels=float(lv[i].mean()),
                                                source_informed=g in SOURCE_INFORMED)
                                        for i, g in enumerate(TRAIN)})
        except SystemExit as e:
            train[lab] = dict(unavailable=str(e))
    print("\ntrain games (beside, not in the rule; * source-informed):")
    for lab, t in train.items():
        if "unavailable" in t:
            print(f"  {lab}: {t['unavailable']}")
            continue
        print(f"  {lab:9} M1 {t['measures']['M1']:.4f}  M4 {t['measures']['M4']:.2f}  "
              + " ".join(f"{g}{'*' if v['source_informed'] else ''} {v['score']:.3f}/{v['levels']:.1f}"
                         for g, v in t["per_game"].items()))

    out = dict(script="scripts/e1_decide.py", plan="docs/TOG_PLAN_v2.md Section 3",
               created=time.strftime("%Y-%m-%d %H:%M:%S"),
               agent=dict(path=args.agent, sha256=sha256(args.agent), mode=args.agent_mode, seeds=a_seeds),
               reference=dict(path=args.reference, sha256=sha256(args.reference), mode=args.reference_mode,
                              seeds=r_seeds),
               budget=args.budget, bootstrap=dict(draws=BOOT, seed=BOOT_SEED, method="games, then seeds within game"),
               measures=dict(agent=A, reference=R), intervals95=dict(agent=Aci, reference=Rci),
               conditions={c: dict(text=RULE_TEXT[c], value=vals[c], holds=bool(cond[c])) for c in cond},
               decision=decision, decided_by=by, seeds_below_registered=len(a_seeds) < 10,
               reproduces_conditions_hold=bool(reproduces), breaks_conditions_hold=breaks,
               precedence="BREAKS over REPRODUCES (TOG_PLAN_v2 3.3, 25 Sep 2026)",
               per_game_heldout=per_game, train_beside=train,
               action7_unavailable=NO_ACTION7, source_informed=SOURCE_INFORMED)
    tmp = args.out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=1)
    os.replace(tmp, args.out)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
