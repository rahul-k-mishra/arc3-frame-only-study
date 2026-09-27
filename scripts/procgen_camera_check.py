#!/usr/bin/env python
"""
procgen_camera_check.py -- does the center_agent option change the frame, game by game?

Infrastructure check in the same class as fidelity_check.py: no census, no agent, no decision.
For each of the 16 Procgen games it builds two environments that differ only in center_agent
(False, then True), drives both with the same fixed 400-action sequence, and compares the 64x64
RGB frame byte for byte at every step (401 comparisons including the initial frame).

Verdict per game:
  identical -- every frame identical, so center_agent has no effect on this game under these options
  differs   -- at least one frame differs; the first differing step is recorded

Writes runs/pilot_checks/procgen_camera_check.json with the constructor kwargs, the procgen version,
and the per-game counts. Run it in the procgen venv from the repo root:
  (procgen venv) python scripts/procgen_camera_check.py
"""
import argparse
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

GAMES = ["bigfish", "bossfight", "caveflyer", "chaser", "climber", "coinrun", "dodgeball", "fruitbot",
         "heist", "jumper", "leaper", "maze", "miner", "ninja", "plunder", "starpilot"]

BASE_KWARGS = dict(num=1, use_sequential_levels=True, num_levels=0, start_level=1000, rand_seed=1000,
                   distribution_mode="easy", use_backgrounds=False, use_monochrome_assets=True)


def frame_bytes(env):
    _rew, obs, _first = env.observe()
    return obs["rgb"][0].tobytes()


def check_game(job):
    game, n_actions, action_seed = job
    import numpy as np
    from procgen import ProcgenGym3Env
    actions = np.random.RandomState(action_seed).randint(0, 15, size=n_actions)
    envs = [ProcgenGym3Env(env_name=game, center_agent=c, **BASE_KWARGS) for c in (False, True)]
    n_same = 0
    first_diff = None
    n_first = [0, 0]
    for step in range(n_actions + 1):
        frames = [frame_bytes(e) for e in envs]
        if frames[0] == frames[1]:
            n_same += 1
        elif first_diff is None:
            first_diff = step
        if step == n_actions:
            break
        a = np.asarray([actions[step]], dtype=np.int32)
        for i, e in enumerate(envs):
            e.act(a)
            _r, _o, first = e.observe()
            if bool(first[0]):
                n_first[i] += 1
    return {"game": game, "steps_compared": n_actions + 1, "identical_frames": n_same, "first_differing_step": first_diff,
            "verdict": "identical" if first_diff is None else "differs", "episode_starts_seen": n_first}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--actions", type=int, default=400)
    ap.add_argument("--action-seed", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default="runs/pilot_checks/procgen_camera_check.json")
    args = ap.parse_args()
    try:
        import procgen
        version = str(getattr(procgen, "__version__", "unknown")).strip()
    except Exception as e:
        print(f"procgen import failed: {e}")
        sys.exit(1)
    jobs = [(g, args.actions, args.action_seed) for g in GAMES]
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        results = list(ex.map(check_game, jobs))
    print(f"procgen {version}; kwargs {BASE_KWARGS}; {args.actions} actions from RandomState({args.action_seed}).randint(0, 15)")
    print(f"{'game':10s} {'compared':>8s} {'identical':>9s} {'first diff':>10s}  verdict   episode starts (off, on)")
    for r in results:
        fd = "-" if r["first_differing_step"] is None else str(r["first_differing_step"])
        print(f"{r['game']:10s} {r['steps_compared']:8d} {r['identical_frames']:9d} {fd:>10s}  {r['verdict']:9s} {r['episode_starts_seen']}")
    ident = [r["game"] for r in results if r["verdict"] == "identical"]
    diff = [r["game"] for r in results if r["verdict"] == "differs"]
    print(f"\ncenter_agent has no effect on {len(ident)} games: {ident}")
    print(f"center_agent changes the frame on {len(diff)} games: {diff}")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"procgen_version": version, "kwargs": BASE_KWARGS, "actions": args.actions, "action_seed": args.action_seed,
                   "results": results, "identical": ident, "differs": diff}, f, indent=1)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
