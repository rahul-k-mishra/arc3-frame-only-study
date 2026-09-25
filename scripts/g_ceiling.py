"""
E4: THE SCORE CEILING OF AN AGENT THAT WINS THE FIRST k LEVELS AT r TIMES THE HUMAN COST.
No game is run.  Specified in docs/TOG_PLAN_v2.md Section 5.

THE RULE, as implemented in arc_agi/scorecard.py (arc-agi 0.9.8), not as printed in the technical
report (whose displayed equations use a fixed n = 5):
    level i (1-based) of a game with N levels, human baseline h_i, agent actions a_i
    completed level, a_i > 0:  s_i = min(115, 100 (h_i / a_i)^2)
    completed level, a_i = 0:  s_i = 0            uncompleted level: s_i = 0
    weights w_i = i;  W_N = N(N+1)/2
    A = sum_i i s_i / W_N                          weighted mean
    M = 100 * sum_{i: s_i > 0} i / W_N             environment cap
    E = min(A, M)                                  environment score
    several plays of one game in a card: the maximum E;  scorecard score: mean E over games

THE CEILING for P(k, r) = "complete levels 1..k, a_i = r h_i on each":
    for i <= k, s_i = min(115, 100/r^2) > 0  (h_i cancels), so
    A = min(115, 100/r^2) W_k/W_N,  M = 100 W_k/W_N,
    E = (W_k/W_N) min(115, 100/r^2, 100) = 100 k(k+1)/(N(N+1)) min(1, 1/r^2)  =: S(k, r, N).
    Under a constant ratio the 115 cap never binds and r < 1 is worth nothing beyond r = 1.
    Any play that completes exactly k levels has E <= 100 k(k+1)/(N(N+1)).
Actions are whole numbers; the "whole-action" columns use a_i = max(1, floor(r h_i)) (ratio at
most r) and are computed through the scorecard's own EnvironmentScoreCalculator.

VALIDATION (before any table is produced; any mismatch > 1e-9 prints the case and exits non-zero
without writing the output).  An independent implementation of E = min(A, M) is compared with
(a) EnvironmentScoreCalculator.add_level / to_score and (b) EnvironmentScorecard.from_scorecard on
a constructed Card + EnvironmentInfo, on:
    V1  S(k, r, N): N = 1..10, k = 0..N, r in {0.5, 0.9, 1, 1.5, 2, 5, 30}, h_i = 20 i (r h_i whole)
    V2  environment cap binds: all levels at h/2 (mean 115 -> 100); N = 3, level 1 at r = 0.5,
        level 2 at r = 1 (A = 52.5, M = 50, E = 50)
    V3  a completed level with 0 actions (s = 0, weight left out of M)
    V4  k = 0; an unfinished run with actions spent on level k+1 (no effect on E)
    V5  two plays of one game in one card (score = the larger)
    V6  a reset inside a level adds one action to that level (Card.inc_reset_count)
    V7  more completed levels than baselines (scorecard gives 0, "size mismatch")
    V8  2,000 random cases (numpy default_rng(20260925)): N 1-12, k 0-N, h 1-200, a 0-10h

WHAT IT READS FROM environment_files: ONLY the "baseline_actions" list of each
<env-dir>/<game>/<version>/metadata.json.  It globs for files named metadata.json and never lists,
opens or imports a game's .py file.  The game name is the directory name.

RESUMABLE: deterministic and takes seconds, so there is nothing to resume inside a run; the output
is written atomically and an existing output is never overwritten without --force.  --workers runs
the V8 cases and the per-game tables in a Pool.

Commands (PowerShell, from D:\\Research\\arc3\\repo):

    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\g_ceiling.py --workers 8

    other options: --env-dir D:\\Research\\arc3\\brutus\\environment_files  --out runs\\ceiling.json  --force

EXPECTED OUTPUT (shape; the table numbers do not exist until the author runs it):

    scorer: ...\\arc_agi\\scorecard.py  sha256 <64 hex>  arc-agi 0.9.8  arcengine 0.9.3
    baselines: 25 games from metadata.json (baseline_actions only)
    VALIDATION  V1 455 cases ... PASS  (max |diff| ...)   ... V8 2000 cases ... PASS
    VALIDATION: all N cases agree with the scorecard to 1e-9
    tu93 worked example: level 1 at 356 vs h_1 = 19 -> level score 0.2848, game score 0.0063
        (the old plan's "0.3 of 100" was the level score)
    per game: N, W_N, S(1, r, N) for r = 1 2 5 10 30 100 150, then k = 2, 3   (* source-informed)
    means over 25 / held-out 17 / train 8, closed form and whole-action
    wrote runs\\ceiling.json
If a validation case fails, the derivation or the implementation reading is wrong; nothing from
this script may be used until it passes.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import importlib.metadata as md
import json
import math
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DEFAULT_ENV = r"D:\Research\arc3\brutus\environment_files"
TRAIN = ["tu93", "ls20", "vc33", "m0r0", "ft09", "lp85", "lf52", "dc22"]
HELD_OUT = ["ar25", "bp35", "cd82", "cn04", "g50t", "ka59", "r11l", "re86", "s5i5",
            "sb26", "sc25", "sk48", "sp80", "su15", "tn36", "tr87", "wa30"]
SOURCE_INFORMED = ["tu93", "dc22", "ls20"]
RATIOS = [1, 2, 5, 10, 30, 100, 150]
KS = [1, 2, 3]
TOL = 1e-9
LEVEL_CAP = 115.0
RNG_SEED = 20260925
N_RANDOM = 2000


# ---------------------------------------------------------------- the rule, written independently

def level_score(h, a):
    return min(LEVEL_CAP, 100.0 * (h / a) ** 2) if a > 0 else 0.0


def env_score(h, won_actions):
    """E = min(A, M) for a play that completed levels 1..len(won_actions) with those action counts.
    Written from the rule above, without calling the scorecard."""
    N = len(h)
    WN = N * (N + 1) / 2
    s = [level_score(h[i], won_actions[i]) for i in range(len(won_actions))]
    A = sum((i + 1) * s[i] for i in range(len(s))) / WN
    M = 100.0 * sum(i + 1 for i in range(len(s)) if s[i] > 0) / WN
    return min(A, M)


def S(k, r, N):
    """Closed form for P(k, r)."""
    return 100.0 * k * (k + 1) / (N * (N + 1)) * min(1.0, 1.0 / r ** 2)


# ---------------------------------------------------------------- the scorecard's two paths

def sc_calculator(h, won_actions, extra=0):
    """Path (a): EnvironmentScoreCalculator, one add_level per level as _calculate_score does."""
    from arc_agi.scorecard import EnvironmentScoreCalculator
    c = EnvironmentScoreCalculator()
    k = len(won_actions)
    for i in range(len(h)):
        if i < k:
            c.add_level(level_index=i + 1, completed=True, actions_taken=won_actions[i],
                        baseline_actions=h[i])
        else:
            c.add_level(level_index=i + 1, completed=False,
                        actions_taken=extra if i == k else 0, baseline_actions=h[i])
    return c.to_score().score


def make_card(game_id, plays):
    """A Card with one play per entry of `plays`; each play is (won_actions, extra_actions).
    Actions are added to the card's counter directly (the same counter inc_action_count adds 1
    to); level completions go through Card.set_levels_completed, as update_scorecard does."""
    from arc_agi.scorecard import Card
    from arcengine import GameState
    card = Card.model_validate({"game_id": game_id})
    for p, (won, extra, n_levels) in enumerate(plays):
        guid = f"play{p}"
        card.inc_play_count(guid)
        idx = card.index_of_guid(guid)
        for i, a in enumerate(won):
            card.actions[idx] += a
            card.set_levels_completed(guid, i + 1)
        card.actions[idx] += extra
        if len(won) == n_levels:
            card.set_state(guid, GameState.WIN)
    return card


def sc_from_scorecard(h, plays, game_id="toy"):
    """Path (b): EnvironmentScorecard.from_scorecard on a constructed Card and EnvironmentInfo.
    Returns (environment score, EnvironmentScoreList)."""
    from arc_agi.models import EnvironmentInfo
    from arc_agi.scorecard import EnvironmentScorecard, Scorecard
    card = make_card(game_id, plays)
    sc = Scorecard(cards={game_id: card})
    env = EnvironmentScorecard.from_scorecard(
        sc, [EnvironmentInfo(game_id=game_id, baseline_actions=list(h))])
    return env.environments[0].score, env.environments[0]


# ---------------------------------------------------------------- validation cases

def v1_cases():
    out = []
    for N in range(1, 11):
        h = [20 * (i + 1) for i in range(N)]
        for k in range(0, N + 1):
            for r in [0.5, 0.9, 1, 1.5, 2, 5, 30]:
                won = [int(round(r * h[i])) for i in range(k)]
                assert all(abs(won[i] - r * h[i]) < 1e-9 for i in range(k))
                out.append(dict(tag="V1", h=h, won=won, extra=0, expect=S(k, r, N) if k else 0.0))
    return out


def v2_to_v4_cases():
    return [
        dict(tag="V2 all levels at h/2 (cap binds, 100)", h=[10, 20, 30], won=[5, 10, 15], extra=0,
             expect=100.0),
        dict(tag="V2 N=3, r=0.5 then r=1 (A=52.5, M=50)", h=[10, 20, 30], won=[5, 20], extra=7,
             expect=50.0),
        dict(tag="V3 completed level with 0 actions", h=[10, 20, 30], won=[10, 0], extra=0,
             expect=100.0 / 6),
        dict(tag="V4 k=0", h=[10, 20, 30], won=[], extra=500, expect=0.0),
        dict(tag="V4 unfinished level k+1 has no effect", h=[10, 20, 30], won=[20], extra=9999,
             expect=25.0 / 6),
    ]


def v8_chunk(args):
    lo, hi = args
    out = []
    for j in range(lo, hi):
        rng = np.random.default_rng([RNG_SEED, j])
        N = int(rng.integers(1, 13))
        h = [int(x) for x in rng.integers(1, 201, N)]
        k = int(rng.integers(0, N + 1))
        won = []
        for i in range(k):
            won.append(0 if rng.random() < 0.03 else int(rng.integers(1, 10 * h[i] + 1)))
        extra = 0 if k == N else int(rng.integers(0, 1000))
        out.append(check(dict(tag="V8", h=h, won=won, extra=extra, expect=None)))
    return out


def check(case):
    """Compare the independent formula (and the expected value, if any) with both scorecard paths."""
    h, won, extra = case["h"], case["won"], case["extra"]
    mine = env_score(h, won)
    a = sc_calculator(h, won, extra)
    b, _ = sc_from_scorecard(h, [(won, extra, len(h))])
    vals = dict(formula=mine, calculator=a, from_scorecard=b)
    if case.get("expect") is not None:
        vals["expected"] = case["expect"]
    diff = max(abs(x - y) for x in vals.values() for y in vals.values())
    return dict(tag=case["tag"], h=h, won=won, extra=extra, values=vals, diff=diff, ok=diff <= TOL)


def special_checks():
    """V5 best of two plays, V6 reset counts as an action, V7 baseline size mismatch."""
    from arc_agi.scorecard import Card, EnvironmentScorecard, Scorecard
    from arc_agi.models import EnvironmentInfo
    res = []
    h = [10, 20, 30]
    # V5: play 0 wins 2 levels slowly, play 1 wins 1 level at the human count
    e0, e1 = env_score(h, [40, 80]), env_score(h, [10])
    got, lst = sc_from_scorecard(h, [([40, 80], 3, 3), ([10], 3, 3)])
    res.append(dict(tag="V5 two plays: score is the larger", values=dict(
        expected=max(e0, e1), from_scorecard=got), diff=abs(got - max(e0, e1)),
        ok=abs(got - max(e0, e1)) <= TOL, note=f"play scores {e0:.6f}, {e1:.6f}"))
    # V6: 3 actions, a reset, 2 actions, level 1 done -> level 1 cost 6 actions
    card = Card.model_validate({"game_id": "toy"})
    card.inc_play_count("g")
    card.actions[0] += 3
    card.inc_reset_count("g")
    card.actions[0] += 2
    card.set_levels_completed("g", 1)
    env = EnvironmentScorecard.from_scorecard(
        Scorecard(cards={"toy": card}), [EnvironmentInfo(game_id="toy", baseline_actions=h)])
    la = env.environments[0].runs[0].level_actions[0]
    res.append(dict(tag="V6 reset adds one action to its level", values=dict(
        expected=6, level_actions=la), diff=abs(la - 6), ok=la == 6))
    # V7: three levels completed, two baselines
    got, lst = sc_from_scorecard([10, 20], [([10, 20, 30], 0, 3)])
    msg = lst.runs[0].message
    res.append(dict(tag="V7 more levels than baselines scores 0", values=dict(
        expected=0.0, from_scorecard=got), diff=abs(got), ok=got == 0.0, note=msg))
    return res


def validate(workers):
    report = {}
    groups = [("V1", v1_cases()), ("V2-V4", v2_to_v4_cases())]
    all_ok = True
    for name, cases in groups:
        rs = [check(c) for c in cases]
        report[name] = rs
    report["V5-V7"] = special_checks()
    jobs = [(lo, min(lo + 250, N_RANDOM)) for lo in range(0, N_RANDOM, 250)]
    if workers > 1:
        with Pool(workers) as pool:
            report["V8"] = [r for chunk in pool.map(v8_chunk, jobs) for r in chunk]
    else:
        report["V8"] = [r for j in jobs for r in v8_chunk(j)]
    n = 0
    for name, rs in report.items():
        bad = [r for r in rs if not r["ok"]]
        n += len(rs)
        worst = max(r["diff"] for r in rs)
        print(f"VALIDATION  {name:6} {len(rs):5} cases ... {'PASS' if not bad else 'FAIL'}"
              f"  (max |diff| {worst:.2e})")
        if name in ("V2-V4", "V5-V7"):
            for r in rs:
                print(f"            {r['tag']:42} " + "  ".join(
                    f"{k} {v:.6f}" for k, v in r["values"].items())
                      + (f"   [{r['note']}]" if r.get("note") else ""))
        for r in bad[:5]:
            print(f"    FAIL {r}")
        all_ok &= not bad
    return all_ok, n, report


# ---------------------------------------------------------------- the public set

def baselines(env_dir):
    """{game: (version, [h_i])} from metadata.json only; stops if a game has two versions."""
    out = {}
    for meta in sorted(glob.glob(os.path.join(env_dir, "*", "*", "metadata.json"))):
        version = os.path.basename(os.path.dirname(meta))
        game = os.path.basename(os.path.dirname(os.path.dirname(meta)))
        with open(meta) as f:
            b = json.load(f).get("baseline_actions")
        if not b:
            sys.exit(f"STOP: {game} has no baseline_actions in its metadata.json")
        if game in out:
            sys.exit(f"STOP: {game} has more than one version directory; which one was run?")
        out[game] = (version, [int(x) for x in b])
    return out


def game_row(args):
    game, version, h = args
    N = len(h)
    row = dict(game=game, version=version, N=N, W_N=N * (N + 1) // 2, baseline_actions=h,
               split="train" if game in TRAIN else "heldout",
               source_informed=game in SOURCE_INFORMED, closed={}, whole={}, k_clamped={})
    for k in KS:
        kk = min(k, N)
        row["k_clamped"][str(k)] = kk
        for r in RATIOS:
            won = [max(1, math.floor(r * h[i])) for i in range(kk)]
            row["closed"][f"{k},{r}"] = S(kk, r, N)
            row["whole"][f"{k},{r}"] = sc_calculator(h, won)
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--env-dir", default=DEFAULT_ENV)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default=os.path.join(REPO, "runs", "ceiling.json"))
    ap.add_argument("--force", action="store_true", help="overwrite an existing output")
    args = ap.parse_args()
    if os.path.exists(args.out) and not args.force:
        sys.exit(f"{args.out} exists; runs/ is never overwritten silently (use --force)")
    t0 = time.time()

    import arc_agi.scorecard as scm
    with open(scm.__file__, "rb") as f:
        sc_sha = hashlib.sha256(f.read()).hexdigest()
    versions = {p: md.version(p) for p in ("arc-agi", "arcengine")}
    print(f"scorer: {scm.__file__}  sha256 {sc_sha}  arc-agi {versions['arc-agi']}  "
          f"arcengine {versions['arcengine']}")
    if versions["arc-agi"] != "0.9.8":
        print(f"WARNING: arc-agi {versions['arc-agi']} is not the 0.9.8 the runs used")

    ok, n_cases, report = validate(args.workers)
    if not ok:
        sys.exit("VALIDATION FAILED: the derivation or the reading of scorecard.py is wrong; "
                 "nothing is written")
    print(f"VALIDATION: all {n_cases} cases agree with the scorecard to {TOL:g}\n")

    base = baselines(args.env_dir)
    games = sorted(base)
    if sorted(games) != sorted(TRAIN + HELD_OUT):
        sys.exit(f"STOP: games found {games} are not the 8 train + 17 held-out games")
    print(f"baselines: {len(games)} games from metadata.json (baseline_actions only)")

    # the old plan's worked example: tu93 level 1 at 356 actions against the human 19
    h_tu = base["tu93"][1]
    lv = level_score(h_tu[0], 356)
    gs = sc_calculator(h_tu, [356])
    print(f"tu93 worked example: level 1 at 356 vs h_1 = {h_tu[0]} -> level score {lv:.4f}, "
          f"game score {gs:.4f} (N = {len(h_tu)}, W_N = {len(h_tu) * (len(h_tu) + 1) // 2}); "
          f"the old plan's \"0.3 of 100\" was the level score\n")

    jobs = [(g, base[g][0], base[g][1]) for g in games]
    if args.workers > 1:
        with Pool(args.workers) as pool:
            rows = pool.map(game_row, jobs)
    else:
        rows = [game_row(j) for j in jobs]

    for k in KS:
        print(f"S({k}, r, N): closed form (whole-action value in brackets when it differs by "
              f">= 0.00005); * = source-informed, T/H = train/held-out, ^ = N < k (all levels)")
        print(f"  {'game':7} {'N':>2} " + " ".join(f"{'r=' + str(r):>16}" for r in RATIOS))
        for row in rows:
            tag = ("*" if row["source_informed"] else " ") + ("T" if row["split"] == "train" else "H")
            cells = []
            for r in RATIOS:
                c, w = row["closed"][f"{k},{r}"], row["whole"][f"{k},{r}"]
                cells.append(f"{c:7.4f}" + (f" [{w:7.4f}]" if abs(c - w) >= 5e-5 else " " * 10))
            print(f"  {row['game']:4}{tag} {row['N']:3}" + ("^" if row["N"] < k else " ")
                  + " ".join(f"{c:>16}" for c in cells))
        print()

    means = {}
    for label, sel in (("all25", games), ("heldout17", HELD_OUT), ("train8", TRAIN)):
        means[label] = {}
        for kind in ("closed", "whole"):
            means[label][kind] = {key: float(np.mean([r[kind][key] for r in rows if r["game"] in sel]))
                                  for key in rows[0][kind]}
    print("means over games of S(k, r, N) (closed form / whole-action):")
    print(f"  {'set':10} {'k':>2} " + " ".join(f"{'r=' + str(r):>17}" for r in RATIOS))
    for label in means:
        for k in KS:
            print(f"  {label:10} {k:2} " + " ".join(
                f"{means[label]['closed'][f'{k},{r}']:8.4f}/{means[label]['whole'][f'{k},{r}']:<8.4f}"
                for r in RATIOS))

    out = dict(script="scripts/g_ceiling.py", plan="docs/TOG_PLAN_v2.md Section 5",
               created=time.strftime("%Y-%m-%d %H:%M:%S"),
               scorer=dict(path=scm.__file__, sha256=sc_sha, **versions),
               formula="S(k,r,N) = 100 k(k+1)/(N(N+1)) min(1, 1/r^2)",
               whole_action_rule="a_i = max(1, floor(r h_i)), scored by EnvironmentScoreCalculator",
               ratios=RATIOS, ks=KS, env_dir=args.env_dir,
               reads="baseline_actions from <env-dir>/<game>/<version>/metadata.json only",
               source_informed=SOURCE_INFORMED, train_games=TRAIN, heldout_games=HELD_OUT,
               validation=dict(passed=True, cases=n_cases, tol=TOL,
                               groups={k: dict(cases=len(v), max_diff=max(r["diff"] for r in v))
                                       for k, v in report.items()},
                               named_cases=report["V2-V4"] + report["V5-V7"]),
               tu93_example=dict(h1=h_tu[0], a1=356, level_score=lv, game_score=gs, N=len(h_tu)),
               games=rows, means=means)
    tmp = args.out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=1)
    os.replace(tmp, args.out)
    print(f"\nwrote {args.out} in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
