"""
W0 check C3 (docs/W0_CHECKS.md): MiniGrid and BabyAI smoke test in .venv_games.  Infrastructure
facts only; no census, no agent, no score.  Nothing from this script enters the manuscript.

Every registered gymnasium id starting with "MiniGrid-" or "BabyAI-" is constructed with

    gymnasium.make(env_id, render_mode="rgb_array", highlight=False, tile_size=8, agent_pov=False)

Keyword names confirmed from the installed source, minigrid 3.1.0,
minigrid/minigrid_env.py lines 43-47 (render_mode, highlight, tile_size, agent_pov); with
agent_pov False, render() returns the full-grid frame (get_frame -> get_full_render, lines
736-742).  It is reset with a fixed seed, then 200 actions, drawn once from a seeded RNG over the
primitive action space, are taken; after an episode ends, the env is reset without a seed (its RNG
continues from the first seeded reset, so the run stays deterministic).  Per env:
    frame shape and dtype          of render() - the full-grid RGB frame the adapter would receive
    observation image shape        of obs["image"] (the partial view MiniGrid returns), for reference
    action count                   primitive action space size
    level-complete key             info-dict keys containing "level_complete" (and all info keys seen);
                                   episodes ended with reward > 0 counted as successes
    distinct RGB colours           over the 201 frames
    steps per second               step + render, first run only
    determinism                    the same (seed, actions) run twice; frame sequences compared byte
                                   for byte (scripts/w0_common.py)

One JSON per env: runs/w0_checks/minigrid/<env_id>.json (fields game, mode "w0_smoke", seed, plus the
facts above).  Resume-safe: an env whose JSON exists is skipped unless --force.  With --only id1,id2
exactly the listed ids are run, even if their JSON exists (overwritten atomically), and nothing
else; an unregistered id stops the script.  Environments are
created inside the worker (spawn-safe on Windows).  An env whose constructor rejects a keyword is
recorded as status "error" with the message, never skipped silently.

Command (PowerShell, from D:\\Research\\arc3\\repo):

    D:\\Research\\arc3\\brutus\\.venv_games\\Scripts\\python.exe scripts\\w0_minigrid_smoke.py --workers 8

EXPECTED OUTPUT (shape; values are what the check measures, none is known in advance):
    minigrid <version>, gymnasium <version>; N env ids (M MiniGrid-, K BabyAI-), N to run, 8 workers
    done <env_id>: ok (one line per env as it finishes)
    table: env  status  frame_shape  dtype  n_actions  level_complete_keys  successes  colours  steps_per_s  determinism
    summary: N ok, 0 not ok; determinism PASS on N of N
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import w0_common as C  # noqa: E402

MAKE_KW = dict(render_mode="rgb_array", highlight=False, tile_size=8, agent_pov=False)


def env_ids():
    import gymnasium
    import minigrid  # noqa: F401  (registers the MiniGrid and BabyAI ids)
    return sorted(k for k in gymnasium.envs.registry if k.startswith(("MiniGrid-", "BabyAI-")))


def play_once(env_id, seed, actions):
    import gymnasium
    import minigrid  # noqa: F401
    env = gymnasium.make(env_id, **MAKE_KW)
    obs, info = env.reset(seed=seed)
    frames = [np.array(env.render(), copy=True)]
    img_shape = list(np.asarray(obs["image"]).shape) if isinstance(obs, dict) and "image" in obs else None
    info_keys, lc_true, ends, successes = set(info.keys()), {}, [], 0
    t0 = time.perf_counter()
    for a in actions:
        obs, rew, term, trunc, info = env.step(int(a))
        frames.append(np.array(env.render(), copy=True))
        info_keys.update(info.keys())
        for k, v in info.items():
            if "level_complete" in k:
                lc_true[k] = lc_true.get(k, 0) + int(bool(v))
        if term or trunc:
            ends.append(len(frames) - 1)
            successes += int(bool(term) and rew > 0)
            env.reset()
            frames.append(np.array(env.render(), copy=True))
    secs = time.perf_counter() - t0
    n_actions = int(env.action_space.n)
    env.close()
    return frames, n_actions, img_shape, sorted(info_keys), lc_true, ends, successes, secs


def one(job):
    env_id, out_dir, seed, steps = job
    rec = dict(game=env_id, mode="w0_smoke", seed=seed, suite="minigrid", steps=steps,
               make_kwargs=MAKE_KW)
    try:
        import gymnasium
        import minigrid  # noqa: F401
        e = gymnasium.make(env_id, **MAKE_KW)
        n_actions = int(e.action_space.n)
        e.close()
        rng = np.random.default_rng(seed)
        actions = rng.integers(0, n_actions, size=steps).tolist()
        f1, n1, img, keys, lc1, ends1, succ1, secs1 = play_once(env_id, seed, actions)
        f2, _n2, _i2, _k2, lc2, ends2, succ2, _s2 = play_once(env_id, seed, actions)
        det = C.compare_frames(f1, f2)
        rec.update(status="ok", frame_shape=list(f1[0].shape), frame_dtype=str(f1[0].dtype),
                   obs_image_shape=img, n_actions=n1, primitive_action_count=n1, info_keys=keys,
                   level_complete_keys=sorted(lc1), level_complete_true_counts=lc1,
                   episode_end_steps=ends1, successes_reward_gt_0=succ1,
                   distinct_rgb_colours=C.distinct_colours(f1),
                   steps_per_second=round(steps / secs1, 1) if secs1 > 0 else None,
                   determinism=det,
                   determinism_flags_equal=(lc1 == lc2 and ends1 == ends2 and succ1 == succ2))
    except Exception as e:                       # recorded, never hidden
        rec.update(status="error", error=f"{type(e).__name__}: {e}")
    C.write_json_atomic(C.out_path(out_dir, env_id), rec)
    return env_id, rec["status"]


def main():
    ap = argparse.ArgumentParser(description="W0 C3: MiniGrid/BabyAI smoke test (infrastructure facts only)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--out", default=os.path.join(REPO, "runs", "w0_checks", "minigrid"))
    ap.add_argument("--force", action="store_true", help="rerun envs whose JSON exists")
    ap.add_argument("--only", default="",
                    help="comma-separated env ids: run exactly these (overwriting their JSON) and nothing else")
    args = ap.parse_args()

    import gymnasium
    import minigrid
    ids = env_ids()
    if args.only:
        only = [i.strip() for i in args.only.split(",") if i.strip()]
        unknown = [i for i in only if i not in ids]
        if unknown:
            sys.exit(f"STOP: --only names ids that are not registered: {unknown}")
        todo = only
    else:
        todo = C.pending(ids, args.out, args.force)
    n_bab = sum(i.startswith("BabyAI-") for i in ids)
    print(f"minigrid {getattr(minigrid, '__version__', '?')}, gymnasium {gymnasium.__version__}; "
          f"{len(ids)} env ids ({len(ids) - n_bab} MiniGrid-, {n_bab} BabyAI-), {len(todo)} to run, "
          f"{args.workers} workers")
    jobs = [(i, args.out, args.seed, args.steps) for i in todo]
    if jobs:
        with Pool(args.workers) as pool:
            for i, st in pool.imap_unordered(one, jobs):
                print(f"done {i}: {st}", flush=True)

    rows = C.load_all(ids, args.out)
    C.print_table(rows, [
        ("env", lambda r: r["game"]), ("status", lambda r: r["status"]),
        ("frame_shape", lambda r: "x".join(map(str, r.get("frame_shape", []))) or None),
        ("dtype", lambda r: r.get("frame_dtype")), ("n_actions", lambda r: r.get("n_actions")),
        ("level_complete_keys", lambda r: ",".join(r.get("level_complete_keys", [])) or "-"),
        ("successes", lambda r: r.get("successes_reward_gt_0")),
        ("colours", lambda r: r.get("distinct_rgb_colours")),
        ("steps_per_s", lambda r: r.get("steps_per_second")),
        ("determinism", lambda r: ("PASS" if r["determinism"]["pass_"] else
                                   f"FAIL@{r['determinism']['first_diff_step']}") if "determinism" in r else None),
    ])
    ok = sum(r["status"] == "ok" for r in rows)
    det = sum(bool(r.get("determinism", {}).get("pass_")) for r in rows)
    print(f"summary: {ok} ok, {len(rows) - ok} not ok, {len(ids) - len(rows)} missing; "
          f"determinism PASS on {det} of {len(ids)}")


if __name__ == "__main__":
    main()
