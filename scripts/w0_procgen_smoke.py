"""
W0 check C1/C2 (docs/W0_CHECKS.md): Procgen install and smoke test.  Infrastructure facts only;
no census, no agent, no score.  Nothing from this script enters the manuscript.

Per game (all 16 Procgen games), with distribution_mode easy, use_backgrounds off,
use_monochrome_assets on, one fixed start level (num_levels 1), and 1,000 actions drawn once from a
seeded RNG over the game's own action space:
    obs shape and dtype            of the RGB observation the adapter would receive
    action count                   size of the game's action space
    level-complete key             which info-dict key(s) contain "level_complete", and how often
                                   each was true in the 1,000 steps
    distinct RGB colours           over the 1,001 frames (reset frame + 1,000 steps)
    steps per second               act + observe + get_info, first run only
    determinism                    the same (start level, seed, actions) run twice; the two frame
                                   sequences compared byte for byte (scripts/w0_common.py)
The constructor keywords are checked against the INSTALLED procgen (inspect.signature of
ProcgenGym3Env) before use; a missing keyword is recorded as status "keyword_missing" and that game
is not run.  The keyword names used here were written from memory of procgen 0.10.x and are
confirmed only by this check.

One JSON per game: runs/w0_checks/procgen/<game>.json (fields game, mode "w0_smoke", seed, plus the
facts above).  Resume-safe: a game whose JSON exists is skipped unless --force.  Environments are
created inside the worker (spawn-safe on Windows).  Deterministic given --seed and --start-level.

Command (PowerShell, from D:\\Research\\arc3\\repo; see docs/W0_CHECKS.md for the venv):

    D:\\Research\\arc3\\brutus\\.venv_procgen\\Scripts\\python.exe scripts\\w0_procgen_smoke.py --workers 8

EXPECTED OUTPUT (shape; values are what the check measures, none is known in advance):
    procgen <version>; ProcgenGym3Env keywords confirmed: distribution_mode, use_backgrounds, ...
    16 games, 16 to run (0 already done), 8 workers
    done bigfish ... (one line per game as it finishes)
    table: game  status  obs_shape  dtype  n_actions  level_complete_keys  colours  steps_per_s  determinism
    summary: 16 ok, 0 error; determinism PASS on N of 16
"""
from __future__ import annotations

import argparse
import inspect
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import w0_common as C  # noqa: E402

GAMES_FALLBACK = ["bigfish", "bossfight", "caveflyer", "chaser", "climber", "coinrun", "dodgeball",
                  "fruitbot", "heist", "jumper", "leaper", "maze", "miner", "ninja", "plunder",
                  "starpilot"]
REQUIRED_KW = ["distribution_mode", "use_backgrounds", "use_monochrome_assets", "start_level",
               "num_levels", "rand_seed"]


def game_list():
    try:
        from procgen.env import ENV_NAMES
        return list(ENV_NAMES), "procgen.env.ENV_NAMES"
    except Exception:
        return list(GAMES_FALLBACK), "fallback list in this script"


def signature_check():
    from procgen import ProcgenGym3Env
    params = list(inspect.signature(ProcgenGym3Env.__init__).parameters)
    missing = [k for k in REQUIRED_KW if k not in params]
    return params, missing


def play_once(game, start_level, seed, actions, params):
    from procgen import ProcgenGym3Env
    kw = dict(num=1, env_name=game, distribution_mode="easy", use_backgrounds=False,
              use_monochrome_assets=True, start_level=start_level, num_levels=1, rand_seed=seed)
    if "num_threads" in params:
        kw["num_threads"] = 1              # one environment per worker process
    env = ProcgenGym3Env(**kw)
    ac = env.ac_space
    n_actions = getattr(ac, "eval_n", None) or getattr(ac, "n", None)
    frames, info_keys, lc_true, firsts = [], set(), {}, 0
    _rew, obs, _first = env.observe()
    frames.append(np.array(obs["rgb"][0], copy=True))
    t0 = time.perf_counter()
    for a in actions:
        env.act(np.array([a], dtype=np.int32))
        _rew, obs, first = env.observe()
        frames.append(np.array(obs["rgb"][0], copy=True))
        info = env.get_info()[0]
        info_keys.update(info.keys())
        for k, v in info.items():
            if "level_complete" in k:
                lc_true[k] = lc_true.get(k, 0) + int(bool(v))
        firsts += int(bool(first[0]))
    secs = time.perf_counter() - t0
    try:
        env.close()
    except Exception:
        pass
    return frames, n_actions, sorted(info_keys), lc_true, firsts, secs


def one(job):
    game, out_dir, seed, start_level, steps, params = job
    rec = dict(game=game, mode="w0_smoke", seed=seed, suite="procgen", start_level=start_level,
               steps=steps, distribution_mode="easy", use_backgrounds=False,
               use_monochrome_assets=True, num_levels=1)
    try:
        # the action space size comes from the environment itself, so the RNG draw needs it first
        _f, n_actions, *_ = play_once(game, start_level, seed, [], params)
        rng = np.random.default_rng([seed, start_level])
        actions = rng.integers(0, n_actions, size=steps).tolist()
        f1, n1, keys1, lc1, firsts1, secs1 = play_once(game, start_level, seed, actions, params)
        f2, _n2, _k2, lc2, firsts2, _s2 = play_once(game, start_level, seed, actions, params)
        det = C.compare_frames(f1, f2)
        rec.update(status="ok", obs_shape=list(f1[0].shape), obs_dtype=str(f1[0].dtype),
                   n_actions=int(n1), info_keys=keys1,
                   level_complete_keys=sorted(lc1), level_complete_true_counts=lc1,
                   episode_starts=firsts1, distinct_rgb_colours=C.distinct_colours(f1),
                   steps_per_second=round(steps / secs1, 1) if secs1 > 0 else None,
                   determinism=det, determinism_flags_equal=(lc1 == lc2 and firsts1 == firsts2))
    except Exception as e:                       # recorded, never hidden
        rec.update(status="error", error=f"{type(e).__name__}: {e}")
    C.write_json_atomic(C.out_path(out_dir, game), rec)
    return game, rec["status"]


def main():
    ap = argparse.ArgumentParser(description="W0 C2: Procgen smoke test (infrastructure facts only)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--start-level", type=int, default=0)
    ap.add_argument("--steps", type=int, default=1000)
    ap.add_argument("--out", default=os.path.join(REPO, "runs", "w0_checks", "procgen"))
    ap.add_argument("--force", action="store_true", help="rerun games whose JSON exists")
    args = ap.parse_args()

    import procgen
    params, missing = signature_check()
    print(f"procgen {getattr(procgen, '__version__', '?')}; ProcgenGym3Env keywords "
          + ("confirmed: " + ", ".join(REQUIRED_KW) if not missing else f"MISSING: {missing}"))
    games, src = game_list()
    todo = C.pending(games, args.out, args.force)
    print(f"{len(games)} games (from {src}), {len(todo)} to run ({len(games) - len(todo)} already done), "
          f"{args.workers} workers")
    if missing:
        for g in todo:
            C.write_json_atomic(C.out_path(args.out, g), dict(
                game=g, mode="w0_smoke", seed=args.seed, suite="procgen", status="keyword_missing",
                missing_keywords=missing, signature=params))
        todo = []
    jobs = [(g, args.out, args.seed, args.start_level, args.steps, params) for g in todo]
    if jobs:
        with Pool(args.workers) as pool:
            for g, st in pool.imap_unordered(one, jobs):
                print(f"done {g}: {st}", flush=True)

    rows = C.load_all(games, args.out)
    C.print_table(rows, [
        ("game", lambda r: r["game"]), ("status", lambda r: r["status"]),
        ("obs_shape", lambda r: "x".join(map(str, r.get("obs_shape", []))) or None),
        ("dtype", lambda r: r.get("obs_dtype")), ("n_actions", lambda r: r.get("n_actions")),
        ("level_complete_keys", lambda r: ",".join(r.get("level_complete_keys", [])) or "-"),
        ("colours", lambda r: r.get("distinct_rgb_colours")),
        ("steps_per_s", lambda r: r.get("steps_per_second")),
        ("determinism", lambda r: ("PASS" if r["determinism"]["pass_"] else
                                   f"FAIL@{r['determinism']['first_diff_step']}") if "determinism" in r else None),
    ])
    ok = sum(r["status"] == "ok" for r in rows)
    det = sum(bool(r.get("determinism", {}).get("pass_")) for r in rows)
    print(f"summary: {ok} ok, {len(rows) - ok} not ok, {len(games) - len(rows)} missing; "
          f"determinism PASS on {det} of {len(games)}")


if __name__ == "__main__":
    main()
