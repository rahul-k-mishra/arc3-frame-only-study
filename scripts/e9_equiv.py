"""
E9 gate G2 (docs/E9_protocol.md Section 2): with the oracle off, the E9 code plays EXACTLY like
today's nav mode.

For each (game, seed) three plays are compared:
    REF  scripts/g_nav.py as committed before E9 (loaded from git, --ref-commit), mode nav
    NAV  the current scripts/g_nav.py with oracle=None                      (mode nav after E9)
    OFF  the current scripts/g_nav.py with a ColourOracle(off=True): every E9 code path runs (the
         environment hand-over, the level-start call) but no colour is ever handed
The whole result row (every field except wall-clock "seconds") and the full action sequence sent
to the environment must be identical across the three.  The action sequence is recorded by
wrapping env.step in all three plays alike; the wrapper only records.

Verdict: "IDENTICAL" or "NOT IDENTICAL" with every difference printed.  Exit status 1 if not.
No game outcome is read beyond the equality test.  Train games only (tu93, dc22, ls20 for E9);
a held-out game is refused.

Commands (PowerShell):

    cd D:\\Research\\arc3\\repo\\scripts
    $py = "D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe"
    & $py e9_equiv.py --games tu93,dc22,ls20 --seeds 2 --budget 3000 --env-dir D:\\Research\\arc3\\brutus\\environment_files

EXPECTED OUTPUT: one line per play ("tu93 seed 1000 REF: score ... levels ... actions ... n_act ..."),
then "compared 6 (game, seed): 0 different -> IDENTICAL", and the JSON written to
e9_equiv_<games>_<seeds>x<budget>.json next to this script (or --out).  Resumable in the sense
that it is deterministic and takes minutes; nothing to resume.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import asdict
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import g_control_probe as M1  # noqa: E402

REF_COMMIT = "378345f"          # last commit of scripts/g_nav.py before E9


def load_ref(commit):
    """today's g_nav.py from git, as module g_nav_ref (imports g_agent etc. from scripts/)"""
    src = subprocess.run(["git", "show", f"{commit}:scripts/g_nav.py"], cwd=REPO, capture_output=True,
                         text=True, check=True).stdout
    d = tempfile.mkdtemp(prefix="e9_ref_")
    path = os.path.join(d, "g_nav_ref.py")
    open(path, "w", encoding="utf-8").write(src)
    spec = importlib.util.spec_from_file_location("g_nav_ref", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def play_recorded(module, game, cfg, env_dir, seconds, oracle):
    """play with env.step wrapped to record (action id, data); identical wrapper for every arm"""
    import arc_agi
    log = []
    orig = arc_agi.Arcade.make

    def make(self, *a, **k):
        env = orig(self, *a, **k)
        step = env.step

        def rec(action, *sa, **sk):
            data = sk.get("data")
            log.append([int(getattr(action, "value", action)), dict(data) if data else None])
            return step(action, *sa, **sk)
        env.step = rec
        return env
    arc_agi.Arcade.make = make
    try:
        if oracle is None:
            r = module.play(game, cfg, env_dir, seconds=seconds)
        else:
            r = module.play(game, cfg, env_dir, seconds=seconds, oracle=oracle)
    finally:
        arc_agi.Arcade.make = orig
    return r, log


def one(job):
    game, cfg_d, seconds, env_dir, arm, ref_commit = job
    import logging
    logging.disable(logging.CRITICAL)
    import g_agent as A
    try:
        if arm == "REF":
            mod, oracle = load_ref(ref_commit), None
        else:
            import g_nav as mod
            oracle = mod.ColourOracle(game, off=True) if arm == "OFF" else None
        r, log = play_recorded(mod, game, A.Config(**cfg_d), env_dir, seconds, oracle)
        r = {k: v for k, v in r.items() if k != "seconds"}
    except Exception as e:
        import traceback
        r, log = dict(error=repr(e)[:300], trace=traceback.format_exc()[-1500:]), []
    return game, cfg_d["seed"], arm, r, log


def main():
    ap = argparse.ArgumentParser(description="E9 gate G2: oracle off == today's nav")
    ap.add_argument("--games", default="tu93,dc22,ls20")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--budget", type=int, default=3000)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--game-seconds", type=float, default=3600)
    ap.add_argument("--env-dir", default=os.path.join(HERE, "environment_files"))
    ap.add_argument("--ref-commit", default=REF_COMMIT)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    games = args.games.split(",")
    bad = [g for g in games if g in M1.HELD_OUT]
    if bad:
        sys.exit(f"STOP: held-out games {bad} refused (E9 uses tu93, dc22, ls20 only)")
    jobs = [(g, dict(max_actions=args.budget, seed=1000 + s, mode="hash"), args.game_seconds,
             args.env_dir, arm, args.ref_commit)
            for s in range(args.seeds) for g in games for arm in ("REF", "NAV", "OFF")]
    res = {}
    with Pool(args.workers) as pool:
        for game, seed, arm, r, log in pool.imap_unordered(one, jobs):
            res[(game, seed, arm)] = (r, log)
            print(f"{game} seed {seed} {arm}: score {r.get('score')} levels {r.get('levels')} "
                  f"actions {r.get('actions')} n_act {len(log)}"
                  + (f" ERROR {r['error']}" if r.get("error") else ""), flush=True)
    diffs = []
    for s in range(args.seeds):
        for g in games:
            ref = res.get((g, 1000 + s, "REF"))
            for arm in ("NAV", "OFF"):
                other = res.get((g, 1000 + s, arm))
                if ref is None or other is None or ref[0].get("error") or other[0].get("error"):
                    diffs.append(f"{g} seed {1000 + s} {arm}: missing or error")
                    continue
                if json.dumps(ref[0], sort_keys=True, default=str) != json.dumps(other[0], sort_keys=True, default=str):
                    keys = sorted(k for k in set(ref[0]) | set(other[0]) if ref[0].get(k) != other[0].get(k))
                    diffs.append(f"{g} seed {1000 + s} {arm}: row differs in {keys}")
                if ref[1] != other[1]:
                    i = next((i for i, (a, b) in enumerate(zip(ref[1], other[1])) if a != b),
                             min(len(ref[1]), len(other[1])))
                    diffs.append(f"{g} seed {1000 + s} {arm}: action sequence differs at action {i} "
                                 f"(lengths {len(ref[1])}, {len(other[1])})")
    n = len(games) * args.seeds
    for d in diffs:
        print("DIFFERENT " + d)
    verdict = "IDENTICAL" if not diffs else "NOT IDENTICAL"
    print(f"\ncompared {n} (game, seed) x 2 arms against REF ({args.ref_commit}): "
          f"{len(diffs)} different -> {verdict}")
    out = args.out or os.path.join(HERE, f"e9_equiv_{'-'.join(games)}_{args.seeds}x{args.budget}.json")
    json.dump(dict(verdict=verdict, ref_commit=args.ref_commit, games=games, seeds=args.seeds,
                   budget=args.budget, differences=diffs,
                   plays={f"{k[0]}/{k[1]}/{k[2]}": dict(row=v[0], n_actions=len(v[1])) for k, v in res.items()}),
              open(out, "w"), indent=1, default=str)
    print(f"wrote {out}")
    sys.exit(0 if not diffs else 1)


if __name__ == "__main__":
    main()
