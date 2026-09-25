"""
E5: DOES A MECHANISM CHOSEN ON 8 PUBLIC GAMES TRANSFER TO THE OTHER 17?  No game is run.

Specified in docs/TOG_PLAN_v2.md Section 4 before this script was first run; the script
implements that specification and nothing chosen after looking at its output.

Reads two ablation matrices already under runs/ (rows in the ablate format: game, mode, seed,
score, levels, level_log, actions, state, seconds):

    PRIMARY      runs/ablate_lenovo_6x4.json    6 mechanisms x 4 seeds x 25 games, 20,000 actions
    EXPLORATORY  runs/ablate_kaggle_20x1.json  20 mechanisms x 1 seed  x 25 games, 10,000 actions
                 (half the primary's budget: a sensitivity check, never mixed with the primary)

Cell value: for game g and mechanism m, the mean over seeds of the recorded scorecard "score".
Nothing is recomputed from level_log.

For each matrix, 10,000 random 8/17 splits of the 25 games (draw k uses
numpy.random.default_rng([20260925, k]); the draw does not depend on --workers).  Per split:
    pick          argmax over mechanisms of the unweighted train-game mean (ties: every outcome is
                  averaged over the tied mechanisms)
    best_hit      pick is the held-out-best mechanism by held-out mean (ties count as best)
    pergame_hits  held-out games on which the pick attains that game's maximum
    alltie_games  held-out games on which every mechanism scores the same (carry no information)
    pick_ho, best_ho, oracle_ho, regret_best = best_ho - pick_ho, regret_oracle = oracle_ho - pick_ho
    rank          pick's rank on the held-out mean (1 = best; ties share the better rank)
    tau           Kendall tau-b between train means and held-out means over mechanisms
    chance_*      the same quantities for a uniformly random mechanism
Secondary (fixed in the plan): S1 "pinned" splits keep the three source-informed games (tu93, dc22,
ls20) in train and draw 5 more from the other 22 (seed [20260926, k]); S2 a cross-fitted per-game
oracle for matrices with an even number >= 2 of seeds (choose each game's best on half the seeds,
score it on the other half, all balanced halves, both directions).  And the author's fixed split
(train tu93 ls20 vc33 m0r0 ft09 lp85 lf52 dc22), with a per-game table; * marks source-informed.

TIME-TRUNCATED RUNS: a run that did not end in WIN and used fewer actions than the matrix's budget
(its largest action count) stopped on the wall clock, not on the action budget.  A mechanism with
any such run is excluded from the main analysis of its matrix; the analysis with every mechanism
is also printed, labelled as including truncated runs.  (Measured before this script existed:
the primary has none; the exploratory has 47 - reset_in_graph 25, object_state 17, coarse_state 3,
seek 2 - so its main analysis has 16 mechanisms.)

SELF-CHECKS (the script stops if one fails):
  - every (game, mechanism, seed) cell present exactly once; 25 games = 8 train + 17 held-out;
  - on the fixed split, the primary matrix's hash_state held-out mean prints as 0.3329
    (docs/HANDOFF_GNAV.md, CLAUDE.md).  If it does not, the loader is wrong and no number below
    it may be used.

RESUMABLE: the whole analysis is deterministic and takes seconds, so there is nothing to resume
inside a run; the output is written atomically (temp file, then rename) and an existing output is
never overwritten without --force (runs/ is never edited).

Commands (PowerShell, from D:\\Research\\arc3\\repo):

    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\g_split_transfer.py --workers 8

    other options: --splits 10000  --out runs\\split_transfer.json  --force

EXPECTED OUTPUT (shape; the numbers do not exist until the author runs it):

    loaded 600 rows from runs\\ablate_lenovo_6x4.json: 25 games, 6 mechanisms, seeds [1000..1003],
        budget 20000, time-truncated runs: none
    loaded 500 rows from runs\\ablate_kaggle_20x1.json: 25 games, 20 mechanisms, seeds [1000],
        budget 10000, time-truncated runs: coarse_state 3, object_state 17, reset_in_graph 25, seek 2
    === primary (6 mechanisms, 4 seeds) ===
    fixed split: train means ..., pick ..., held-out means ..., per-game table (* source-informed)
    SELF-CHECK hash_state held-out mean on the fixed split = 0.3329 ... PASS
    old plan's one-split numbers (matrix and selection rule not recorded), checked one by one:
        per-game oracle 0.3632           -> this matrix's oracle, and whether it matches
        "selected" 0.3329                -> which mechanism(s) have that held-out mean, their
                                            train-mean rank, and whether the train pick has it
        pick best on 3 of 17 games       -> for that mechanism: games where it is best, all / not
                                            counting games where every mechanism ties
    random splits (10000, D distinct): best_hit F  (chance C) ...  percentile table ...
    pinned splits ...  cross-fitted oracle ...
    === exploratory (16 mechanisms, 1 seed, 10,000 actions) ===  ... same blocks
    === exploratory, all 20 mechanisms (INCLUDES TIME-TRUNCATED RUNS) === ... same blocks
    wrote runs\\split_transfer.json

LIMITS (say them where the numbers are used): the splits are splits of the same 25 authored public
games; they share games and are strongly dependent, so a fraction over splits describes this set,
not a population of games, and carries no p-value.  Seeds are nested within games.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import sys
import time
from collections import Counter, defaultdict
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TRAIN = ["tu93", "ls20", "vc33", "m0r0", "ft09", "lp85", "lf52", "dc22"]
HELD_OUT = ["ar25", "bp35", "cd82", "cn04", "g50t", "ka59", "r11l", "re86", "s5i5",
            "sb26", "sc25", "sk48", "sp80", "su15", "tn36", "tr87", "wa30"]
SOURCE_INFORMED = ["tu93", "dc22", "ls20"]
N_TRAIN = 8
SPLIT_SEED = 20260925
PINNED_SEED = 20260926
EPS = 1e-12
CHUNK = 500
PCTS = [5, 25, 50, 75, 95]
OLD_PLAN = {"pergame_hits": 3, "oracle": 0.3632, "selected": 0.3329}


# ---------------------------------------------------------------- loading

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load_matrix(path):
    """Cube score[g, m, s] from an ablate JSON; stops on a missing or duplicate cell."""
    rows = json.load(open(path))
    games = sorted({r["game"] for r in rows})
    mechs = sorted({r["mode"] for r in rows})
    seeds = sorted({int(r["seed"]) for r in rows})
    if sorted(games) != sorted(TRAIN + HELD_OUT):
        sys.exit(f"STOP {path}: games {games} are not the 8 train + 17 held-out games")
    budget = max(int(r["actions"]) for r in rows)
    cube = np.full((len(games), len(mechs), len(seeds)), np.nan)
    seen = Counter()
    truncated = Counter()
    for r in rows:
        if "error" in r:
            sys.exit(f"STOP {path}: run {r['game']} {r['mode']} {r['seed']} has an error field")
        key = (r["game"], r["mode"], int(r["seed"]))
        seen[key] += 1
        cube[games.index(r["game"]), mechs.index(r["mode"]), seeds.index(int(r["seed"]))] = \
            float(r["score"])
        if r.get("state") != "WIN" and int(r["actions"]) < budget:
            truncated[r["mode"]] += 1
    dups = [k for k, v in seen.items() if v > 1]
    if dups:
        sys.exit(f"STOP {path}: {len(dups)} duplicate cells, e.g. {dups[:3]}")
    if np.isnan(cube).any():
        miss = [(games[g], mechs[m], seeds[s]) for g, m, s in zip(*np.where(np.isnan(cube)))]
        sys.exit(f"STOP {path}: {len(miss)} missing cells, e.g. {miss[:3]}")
    trunc_txt = ", ".join(f"{m} {truncated[m]}" for m in sorted(truncated)) or "none"
    print(f"loaded {len(rows)} rows from {path}: {len(games)} games, "
          f"{len(mechs)} mechanisms, seeds {seeds}, budget {budget}, "
          f"time-truncated runs: {trunc_txt}")
    return dict(path=os.path.basename(path), sha256=sha256(path), rows=len(rows),
                games=games, mechs=mechs, seeds=seeds, budget=budget, cube=cube,
                truncated=dict(truncated))


# ---------------------------------------------------------------- one split

def tau_b(x, y):
    """Kendall tau-b with ties to EPS; nan if either vector is constant."""
    n = len(x)
    c = d = tx = ty = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = x[i] - x[j], y[i] - y[j]
            zx, zy = abs(dx) <= EPS, abs(dy) <= EPS
            if zx:
                tx += 1
            if zy:
                ty += 1
            if zx or zy:
                continue
            if (dx > 0) == (dy > 0):
                c += 1
            else:
                d += 1
    n0 = n * (n - 1) / 2
    den = math.sqrt((n0 - tx) * (n0 - ty))
    return (c - d) / den if den > 0 else float("nan")


def evaluate(cell, train_idx, xoracle=None):
    """All outcomes for one split.  cell[g, m] = seed-mean score."""
    G, M = cell.shape
    tr = np.zeros(G, bool)
    tr[train_idx] = True
    ho_idx = np.where(~tr)[0]
    train_mean = cell[tr].mean(axis=0)
    ho_mean = cell[~tr].mean(axis=0)
    picks = np.where(train_mean >= train_mean.max() - EPS)[0]
    w = 1.0 / len(picks)

    best_ho = ho_mean.max()
    best_set = ho_mean >= best_ho - EPS
    ho_cells = cell[~tr]
    game_max = ho_cells.max(axis=1)
    game_best = ho_cells >= game_max[:, None] - EPS            # [held-out game, mechanism]
    alltie = (ho_cells.max(axis=1) - ho_cells.min(axis=1)) <= EPS
    ranks = np.array([1 + int((ho_mean > ho_mean[m] + EPS).sum()) for m in range(M)])

    pick_ho = float(ho_mean[picks].mean())
    oracle_ho = float(game_max.mean())
    out = dict(
        train=[int(i) for i in train_idx],
        picks=[int(p) for p in picks],
        best_hit=float(best_set[picks].mean()),
        pergame_hits=float(game_best[:, picks].mean(axis=1).sum()),
        pergame_hits_informative=float(game_best[~alltie][:, picks].mean(axis=1).sum()),
        alltie_games=int(alltie.sum()),
        pick_ho=pick_ho,
        best_ho=float(best_ho),
        oracle_ho=oracle_ho,
        regret_best=float(best_ho) - pick_ho,
        regret_oracle=oracle_ho - pick_ho,
        rank=float(ranks[picks].mean()),
        tau=tau_b(train_mean, ho_mean),
        chance_best_hit=float(best_set.mean()),
        chance_pergame_hits=float(game_best.mean(axis=1).sum()),
        chance_ho=float(ho_mean.mean()),
        pick_weights={int(p): w for p in picks},
    )
    if xoracle is not None:
        out["xoracle_ho"] = float(xoracle[ho_idx].mean())
        out["regret_xoracle"] = out["xoracle_ho"] - pick_ho
    return out


def draw_split(kind, k, n_games, pinned_idx):
    if kind == "random":
        rng = np.random.default_rng([SPLIT_SEED, k])
        return np.sort(rng.choice(n_games, N_TRAIN, replace=False))
    rng = np.random.default_rng([PINNED_SEED, k])
    rest = np.array([i for i in range(n_games) if i not in pinned_idx])
    more = rng.choice(rest, N_TRAIN - len(pinned_idx), replace=False)
    return np.sort(np.concatenate([np.array(pinned_idx), more]))


_W = {}


def _init(cell, xoracle, pinned_idx):
    _W.update(cell=cell, xoracle=xoracle, pinned_idx=pinned_idx)


def _chunk(job):
    kind, lo, hi = job
    cell, xo, pin = _W["cell"], _W["xoracle"], _W["pinned_idx"]
    return [evaluate(cell, draw_split(kind, k, cell.shape[0], pin), xo) for k in range(lo, hi)]


# ---------------------------------------------------------------- summaries

def cross_fitted_oracle(cube):
    """Per game: pick the best mechanism on one balanced half of the seeds, score it on the other
    half; average over all balanced halves and both directions.  None if seeds are not even >= 2."""
    S = cube.shape[2]
    if S < 2 or S % 2:
        return None
    halves = [c for c in itertools.combinations(range(S), S // 2) if 0 in c]
    vals = np.zeros(cube.shape[0])
    n = 0
    for a in halves:
        b = tuple(s for s in range(S) if s not in a)
        for sel, ev in ((a, b), (b, a)):
            ms = cube[:, :, list(sel)].mean(axis=2)
            me = cube[:, :, list(ev)].mean(axis=2)
            best = ms >= ms.max(axis=1, keepdims=True) - EPS
            vals += (me * best).sum(axis=1) / best.sum(axis=1)
            n += 1
    return vals / n


def summarise(results, mechs):
    num = ["best_hit", "pergame_hits", "pergame_hits_informative", "alltie_games", "pick_ho",
           "best_ho", "oracle_ho", "regret_best", "regret_oracle", "rank", "tau",
           "chance_best_hit", "chance_pergame_hits", "chance_ho", "xoracle_ho", "regret_xoracle"]
    out = {"splits": len(results), "distinct_splits": len({tuple(r["train"]) for r in results})}
    for k in num:
        if k not in results[0]:
            continue
        v = np.array([r[k] for r in results], float)
        v = v[~np.isnan(v)]
        out[k] = dict(mean=float(v.mean()), n=int(len(v)),
                      **{f"p{p}": float(np.percentile(v, p)) for p in PCTS})
    freq = defaultdict(float)
    for r in results:
        for p, w in r["pick_weights"].items():
            freq[mechs[int(p)]] += w
    out["pick_frequency"] = {m: freq[m] / len(results) for m in mechs}
    return out


def print_summary(title, s):
    print(f"\n  {title}: {s['splits']} splits ({s['distinct_splits']} distinct)")
    print(f"    {'outcome':26} {'mean':>8} " + " ".join(f"{'p' + str(p):>8}" for p in PCTS))
    for k in ["best_hit", "chance_best_hit", "pergame_hits", "chance_pergame_hits",
              "pergame_hits_informative", "alltie_games", "pick_ho", "chance_ho", "best_ho",
              "oracle_ho", "xoracle_ho", "regret_best", "regret_oracle", "regret_xoracle",
              "rank", "tau"]:
        if k in s:
            v = s[k]
            print(f"    {k:26} {v['mean']:8.4f} " + " ".join(f"{v['p' + str(p)]:8.4f}" for p in PCTS)
                  + ("" if v["n"] == s["splits"] else f"   (defined on {v['n']} splits)"))
    print("    pick frequency: " + ", ".join(f"{m} {f:.3f}" for m, f in
                                             sorted(s["pick_frequency"].items(), key=lambda x: -x[1])))


def fixed_split(mat, cell, mech_idx, xoracle):
    games = mat["games"]
    mechs = [mat["mechs"][i] for i in mech_idx]
    tr_idx = [games.index(g) for g in TRAIN]
    r = evaluate(cell, tr_idx, xoracle)
    tr = np.zeros(len(games), bool)
    tr[tr_idx] = True
    train_mean, ho_mean = cell[tr].mean(axis=0), cell[~tr].mean(axis=0)
    picks = [mechs[p] for p in r["picks"]]
    w = max(len(m) for m in mechs) + 1
    print(f"\n  fixed split (train {' '.join(TRAIN)})")
    print(f"    {'mechanism':{w}} {'train':>8} {'held-out':>9}")
    for i, m in enumerate(mechs):
        print(f"    {m:{w}} {train_mean[i]:8.4f} {ho_mean[i]:9.4f}" + ("   <- pick" if m in picks else ""))
    print(f"    per game (held-out best marked +; * = source-informed):")
    print(f"      {'game':6} " + " ".join(f"{m[:10]:>10}" for m in mechs))
    per_game = {}
    for gi, g in enumerate(games):
        mx = cell[gi].max()
        tag = ("*" if g in SOURCE_INFORMED else " ") + ("T" if g in TRAIN else "H")
        print(f"      {g:4}{tag} " + " ".join(
            f"{cell[gi, i]:9.4f}{'+' if cell[gi, i] >= mx - EPS and g in HELD_OUT else ' '}"
            for i in range(len(mechs))))
        per_game[g] = {m: float(cell[gi, i]) for i, m in enumerate(mechs)}
    print(f"    pick {picks}: held-out best on {r['pergame_hits']:.2f} of 17 games "
          f"({r['alltie_games']} games where all mechanisms tie); "
          f"held-out mean {r['pick_ho']:.4f}, best mechanism {r['best_ho']:.4f}, "
          f"per-game oracle {r['oracle_ho']:.4f}"
          + (f", cross-fitted oracle {r['xoracle_ho']:.4f}" if "xoracle_ho" in r else ""))
    # the old plan's one-split numbers, checked one by one (its matrix and rule were not recorded)
    print(f"    old plan, per-game oracle {OLD_PLAN['oracle']}: this matrix {r['oracle_ho']:.4f} "
          + ("MATCH" if f"{r['oracle_ho']:.4f}" == f"{OLD_PLAN['oracle']:.4f}" else "no match"))
    order = sorted(range(len(mechs)), key=lambda i: -train_mean[i])
    ho_cells = cell[~tr]
    alltie = (ho_cells.max(axis=1) - ho_cells.min(axis=1)) <= EPS
    hits_old = {}
    for i, m in enumerate(mechs):
        if f"{ho_mean[i]:.4f}" != f"{OLD_PLAN['selected']:.4f}":
            continue
        best = ho_cells[:, i] >= ho_cells.max(axis=1) - EPS
        hits_old[m] = dict(train_rank=order.index(i) + 1, games_best=int(best.sum()),
                           games_best_informative=int((best & ~alltie).sum()),
                           is_train_pick=m in picks)
        print(f"    old plan, selected {OLD_PLAN['selected']}: held-out mean of {m}, train-mean rank "
              f"{order.index(i) + 1} of {len(mechs)} ({'IS' if m in picks else 'is NOT'} the train "
              f"pick); best on {int(best.sum())} of 17 held-out games, "
              f"{int((best & ~alltie).sum())} not counting all-tie games "
              f"(old plan: {OLD_PLAN['pergame_hits']})")
    if not hits_old:
        print(f"    old plan, selected {OLD_PLAN['selected']}: no mechanism in this matrix has that "
              f"held-out mean")
    r["old_plan_check"] = dict(oracle_match=f"{r['oracle_ho']:.4f}" == f"{OLD_PLAN['oracle']:.4f}",
                               mechanisms_with_selected_value=hits_old)
    r.update(train_means={m: float(train_mean[i]) for i, m in enumerate(mechs)},
             heldout_means={m: float(ho_mean[i]) for i, m in enumerate(mechs)},
             pick_names=picks, per_game=per_game)
    return r


def analyse(label, mat, mech_idx, splits, workers):
    mechs = [mat["mechs"][i] for i in mech_idx]
    cube = mat["cube"][:, mech_idx, :]
    cell = cube.mean(axis=2)
    xo = cross_fitted_oracle(cube)
    print(f"\n=== {label} ({len(mechs)} mechanisms, {len(mat['seeds'])} seed(s), "
          f"{mat['budget']} actions) ===")
    res = dict(mechanisms=mechs, seeds=mat["seeds"], budget=mat["budget"])
    res["fixed_split"] = fixed_split(mat, cell, mech_idx, xo)
    pin = [mat["games"].index(g) for g in SOURCE_INFORMED]
    for kind, seed in (("random", SPLIT_SEED), ("pinned", PINNED_SEED)):
        jobs = [(kind, lo, min(lo + CHUNK, splits)) for lo in range(0, splits, CHUNK)]
        if workers > 1:
            with Pool(workers, initializer=_init, initargs=(cell, xo, pin)) as pool:
                out = [r for chunk in pool.map(_chunk, jobs) for r in chunk]
        else:
            _init(cell, xo, pin)
            out = [r for j in jobs for r in _chunk(j)]
        s = summarise(out, mechs)
        s["rng_seed"] = seed
        print_summary(f"{kind} splits" + (" (tu93 dc22 ls20 always train)" if kind == "pinned" else ""), s)
        # per-split columns (train sets are not stored: split k is regenerated by draw_split)
        cols = {k: [round(r[k], 5) if isinstance(r[k], float) else r[k] for r in out]
                for k in out[0] if k not in ("pick_weights", "train")}
        res[kind] = dict(summary=s, per_split=cols)
    return res


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--primary", default=os.path.join(REPO, "runs", "ablate_lenovo_6x4.json"))
    ap.add_argument("--exploratory", default=os.path.join(REPO, "runs", "ablate_kaggle_20x1.json"))
    ap.add_argument("--splits", type=int, default=10000)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default=os.path.join(REPO, "runs", "split_transfer.json"))
    ap.add_argument("--force", action="store_true", help="overwrite an existing output")
    args = ap.parse_args()
    if os.path.exists(args.out) and not args.force:
        sys.exit(f"{args.out} exists; runs/ is never overwritten silently (use --force)")
    t0 = time.time()

    prim = load_matrix(args.primary)
    expl = load_matrix(args.exploratory)

    out = dict(script="scripts/g_split_transfer.py", plan="docs/TOG_PLAN_v2.md Section 4",
               created=time.strftime("%Y-%m-%d %H:%M:%S"), splits=args.splits,
               split_seed=SPLIT_SEED, pinned_seed=PINNED_SEED, n_train=N_TRAIN, eps=EPS,
               train_games=TRAIN, heldout_games=HELD_OUT, source_informed=SOURCE_INFORMED,
               inputs={k: {f: m[f] for f in ("path", "sha256", "rows", "mechs", "seeds", "budget",
                                             "truncated")}
                       for k, m in (("primary", prim), ("exploratory", expl))},
               games_order=prim["games"])

    ok = [i for i, m in enumerate(prim["mechs"]) if m not in prim["truncated"]]
    if len(ok) != len(prim["mechs"]):
        print(f"NOTE: primary has time-truncated mechanisms {sorted(prim['truncated'])}; excluded")
    out["primary"] = analyse("primary", prim, ok, args.splits, args.workers)
    hs = out["primary"]["fixed_split"]["heldout_means"].get("hash_state")
    passed = hs is not None and f"{hs:.4f}" == "0.3329"
    print(f"\nSELF-CHECK hash_state held-out mean on the fixed split = "
          f"{'missing' if hs is None else f'{hs:.4f}'} (expected 0.3329) ... {'PASS' if passed else 'FAIL'}")
    out["self_check_hash_state_0.3329"] = passed
    if not passed:
        sys.exit("STOP: the primary matrix does not reproduce 0.3329; nothing is written")

    ok = [i for i, m in enumerate(expl["mechs"]) if m not in expl["truncated"]]
    out["exploratory"] = analyse(f"exploratory, untruncated mechanisms only", expl, ok,
                                 args.splits, args.workers)
    out["exploratory_all20_includes_truncated"] = analyse(
        "exploratory, ALL mechanisms (INCLUDES TIME-TRUNCATED RUNS)", expl,
        list(range(len(expl["mechs"]))), args.splits, args.workers)

    tmp = args.out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    os.replace(tmp, args.out)
    print(f"\nwrote {args.out} in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
