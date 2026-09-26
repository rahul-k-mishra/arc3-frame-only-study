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
The constructor keywords are checked against the INSTALLED procgen by walking ProcgenGym3Env's method
resolution order: in procgen 0.10.7, start_level, num_levels, rand_seed and num_threads are
parameters of BaseProcgenEnv.__init__ and reach it through ProcgenGym3Env.__init__(**kwargs)
(procgen/env.py lines 71-84, 207-246).  (The first version checked the child's signature only and
reported those keywords missing; corrected 27 Sep 2026, docs/W0_CHECKS.md amendment.)  Then one
environment (bigfish, the registered settings) is constructed before the pool starts, as the
decisive test; if that raises, the traceback is printed and the script stops.  A game whose JSON
says "keyword_missing" or "error" is not counted as done and is run again.  The action count is
read from ac_space.eltype.n (gym3 TensorType of Discrete); the construction test reads it too, so
a failure there stops the script before the pool.

One JSON per game: runs/w0_checks/procgen/<game>.json (fields game, mode "w0_smoke", seed, plus the
facts above).  Resume-safe: a game whose JSON exists is skipped unless --force.  Environments are
created inside the worker (spawn-safe on Windows).  Deterministic given --seed and --start-level.

Command (PowerShell, from D:\\Research\\arc3\\repo; see docs/W0_CHECKS.md for the venv):

    D:\\Research\\arc3\\brutus\\.venv_procgen\\Scripts\\python.exe scripts\\w0_procgen_smoke.py --workers 8

EXPECTED OUTPUT (shape; values are what the check measures, none is known in advance):
    procgen <version>; ProcgenGym3Env keywords confirmed: distribution_mode (ProcgenGym3Env), ...,
        start_level (BaseProcgenEnv), num_levels (BaseProcgenEnv), rand_seed (BaseProcgenEnv)
    construction test: bigfish built with the registered settings, obs['rgb'] <shape>, <n> actions
    16 games (from procgen.env.ENV_NAMES), 16 to run (0 already done), 8 workers
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


def action_count(ac):
    """Size of a procgen gym3 action space.  ProcgenGym3Env.ac_space is a gym3 TensorType with
    shape () whose .eltype is Discrete(n) (gym3/types.py lines 63-64, 95-97, 126); neither the
    TensorType nor the env has .n or .eval_n.  Reading those (the first version) gave None, and
    rng.integers(0, None) raised "ValueError: high <= 0" in every worker (27 Sep 2026)."""
    el = getattr(ac, "eltype", ac)
    n = getattr(el, "n", None)
    if not isinstance(n, int) or n <= 0:
        raise ValueError(f"cannot read a positive action count from ac_space {ac!r}")
    return n


def signature_check():
    """Keywords accepted by ProcgenGym3Env, found by walking its method resolution order.

    In procgen 0.10.7 (procgen/env.py) start_level, num_levels, rand_seed and num_threads are
    parameters of BaseProcgenEnv.__init__; ProcgenGym3Env.__init__ takes **kwargs and forwards them
    with super().__init__(num, env_name, options, **kwargs).  A keyword defined on a parent class
    counts only if every class below it in the MRO forwards **kwargs.  Returns (params, missing,
    defined_by), defined_by mapping each accepted keyword to the class that defines it."""
    from procgen import ProcgenGym3Env
    defined_by, forwarding = {}, True
    for cls in ProcgenGym3Env.__mro__:
        init = cls.__dict__.get("__init__")
        if init is None:
            continue
        try:
            sig = inspect.signature(init)
        except (TypeError, ValueError):
            break                                # a C-level __init__: nothing more to read
        if forwarding:
            for name, p in sig.parameters.items():
                if name != "self" and p.kind not in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
                    defined_by.setdefault(name, cls.__name__)
        forwarding = forwarding and any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values())
    missing = [k for k in REQUIRED_KW if k not in defined_by]
    return sorted(defined_by), missing, defined_by


def construction_test(params, seed, start_level):
    """The decisive test: build one environment (bigfish, the registered settings) and observe it
    once.  Raises whatever the constructor raises."""
    from procgen import ProcgenGym3Env
    kw = dict(num=1, env_name="bigfish", distribution_mode="easy", use_backgrounds=False,
              use_monochrome_assets=True, start_level=start_level, num_levels=1, rand_seed=seed)
    if "num_threads" in params:
        kw["num_threads"] = 1
    env = ProcgenGym3Env(**kw)
    _rew, obs, _first = env.observe()
    shape = tuple(obs["rgb"].shape)
    n_actions = action_count(env.ac_space)
    try:
        env.close()
    except Exception:
        pass
    return shape, n_actions


def play_once(game, start_level, seed, actions, params):
    from procgen import ProcgenGym3Env
    kw = dict(num=1, env_name=game, distribution_mode="easy", use_backgrounds=False,
              use_monochrome_assets=True, start_level=start_level, num_levels=1, rand_seed=seed)
    if "num_threads" in params:
        kw["num_threads"] = 1              # one environment per worker process
    env = ProcgenGym3Env(**kw)
    ac = env.ac_space
    n_actions = action_count(ac)
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
    import traceback
    params, missing, defined_by = signature_check()
    print(f"procgen {getattr(procgen, '__version__', '?')}; ProcgenGym3Env keywords "
          + ("confirmed: " + ", ".join(f"{k} ({defined_by[k]})" for k in REQUIRED_KW)
             if not missing else f"MISSING: {missing}"))
    try:
        shape, n_act = construction_test(params, args.seed, args.start_level)
        print(f"construction test: bigfish built with the registered settings, obs['rgb'] {shape}, "
              f"{n_act} actions")
    except Exception:
        print("construction test FAILED: bigfish could not be built with the registered settings")
        traceback.print_exc()
        sys.exit(1)
    games, src = game_list()
    todo = C.pending(games, args.out, args.force)
    # a game recorded as keyword_missing or error was never played to the end (the pre-fix check
    # stopped it, or the worker raised), so it is not done: run it again without --force
    for r in C.load_all(games, args.out):
        if r.get("status") in ("keyword_missing", "error") and r["game"] not in todo:
            todo.append(r["game"])
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
