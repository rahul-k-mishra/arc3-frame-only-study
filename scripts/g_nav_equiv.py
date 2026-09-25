"""
Does the modified g_agent.py (hook points added) play EXACTLY like the original when no hook is
given?  Runs both on the same games and seeds, worker pool, and compares score, levels, actions
and the per-level action counts.  Any difference is printed; the verdict is IDENTICAL or NOT.

    python g_nav_equiv.py --games train --seeds 2 --budget 3000 --workers 8

g_agent_ref.py is the original file from brutus_g_handoff.zip (byte-identical copy).
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict
from multiprocessing import Pool

import g_control_probe as M1

HERE = os.path.dirname(os.path.abspath(__file__))


def one(job):
    game, cfg_d, seconds, env_dir, which = job
    import logging
    logging.disable(logging.CRITICAL)
    mod = __import__("g_agent_ref" if which == "ref" else "g_agent")
    try:
        r = mod.play(game, mod.Config(**cfg_d), env_dir, seconds=seconds)
        out = dict(score=r.get("score"), levels=r.get("levels"), actions=r.get("actions"),
                   level_log=[(L.get("level"), L.get("actions")) for L in r.get("level_log", [])])
    except Exception as e:
        out = dict(error=repr(e)[:200])
    return game, cfg_d["seed"], which, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", default="train")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--budget", type=int, default=3000)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--game-seconds", type=float, default=900)
    ap.add_argument("--env-dir", default=os.path.join(HERE, "environment_files"))
    args = ap.parse_args()
    games = (M1.TRAIN if args.games == "train" else M1.HELD_OUT if args.games == "heldout"
             else args.games.split(","))
    jobs = []
    for s in range(args.seeds):
        for g in games:
            cfg = dict(max_actions=args.budget, seed=1000 + s, mode="hash")
            jobs.append((g, cfg, args.game_seconds, args.env_dir, "ref"))
            jobs.append((g, cfg, args.game_seconds, args.env_dir, "new"))
    res = {}
    with Pool(args.workers) as pool:
        for game, seed, which, out in pool.imap_unordered(one, jobs):
            res[(game, seed, which)] = out
            print(f"{game} seed {seed} {which}: {out}", flush=True)
    diffs = 0
    for s in range(args.seeds):
        for g in games:
            a, b = res.get((g, 1000 + s, "ref")), res.get((g, 1000 + s, "new"))
            if a != b:
                diffs += 1
                print(f"DIFFERENT {g} seed {1000 + s}:\n   ref {a}\n   new {b}")
    print(f"\n{len(games) * args.seeds} pairs compared, {diffs} different -> "
          f"{'IDENTICAL' if diffs == 0 else 'NOT IDENTICAL - do not use g_agent.py'}")
    json.dump({f"{k[0]}/{k[1]}/{k[2]}": v for k, v in res.items()},
              open(os.path.join(HERE, "equiv_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
