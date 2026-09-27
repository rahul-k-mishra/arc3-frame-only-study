"""
Fidelity check, docs/PREREG.md v1 Sections 2.1 and 9: every game of a suite is played twice through
its adapter with the same seed and the same 200 actions; the two grid sequences (and the level_end
and game_end flags) must be byte-identical.  It runs the adapters themselves, so it also shows the
adapters are deterministic.  No census, no agent: actions are drawn once from
numpy.random.default_rng([seed, index of the condition]) over the adapter's action list.

    --suite minigrid   run in .venv_games;  games = the 167 non-excluded ids of
                       docs/GROUND_TRUTH_minigrid.md (confirmatory and pilot); conditions raw, macro
    --suite procgen    run in .venv_procgen; games = the 16 Procgen games; conditions center_off,
                       center_on

One JSON per (game, condition): runs/fidelity/<suite>/<game>__<condition>.json with
    game, suite, condition, seed, steps, status ("ok" | "error"), identical, first_diff_step,
    flags_equal, n_actions, grid, n_colours, level_ends, game_ends, steps_per_second, adapter record
Resume-safe: a JSON whose status is "ok" is skipped unless --force; "error" is run again.
Worker pool (spawn-safe: adapters are built inside the worker).  A console table at the end.

Commands: docs/W2_COMMANDS.md.

EXPECTED OUTPUT (shape; values are what the check measures):
    fidelity minigrid: 334 jobs (167 games x 2 conditions), N to run, 8 workers
    done <game> <condition>: ok identical
    table: game  condition  status  identical  flags  grid  colours  n_actions  level_ends  game_ends  steps_per_s
    summary: N ok, N error; identical on N of N
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

CONDITIONS = {"minigrid": ["raw", "macro"], "procgen": ["center_off", "center_on"]}


def games_for(suite):
    if suite == "procgen":
        from adapter_procgen import GAMES
        return list(GAMES)
    import analyze_common as C
    t = C.parse_truth_minigrid(os.path.join(REPO, "docs", "GROUND_TRUTH_minigrid.md"))
    return sorted(g for g, r in t.items() if not r["status"].startswith("excluded"))


def make(suite, game, condition):
    if suite == "procgen":
        from adapter_procgen import ProcgenAdapter
        return ProcgenAdapter(game, condition)
    from adapter_minigrid import MinigridAdapter
    return MinigridAdapter(game, condition)


def play(suite, game, condition, seed, actions):
    a = make(suite, game, condition)
    grids, flags = [a.reset(seed).tobytes()], []
    t0 = time.perf_counter()
    for i in actions:
        g, le, ge = a.step(int(i))
        grids.append(np.asarray(g).tobytes())
        flags.append((bool(le), bool(ge)))
    secs = time.perf_counter() - t0
    rec = a.record()
    shape = rec.get("grid")
    a.close()
    return grids, flags, secs, rec, shape


def out_path(out, suite, game, condition):
    return os.path.join(out, suite, f"{game}__{condition}.json")


def one(job):
    suite, game, condition, seed, steps, out = job
    row = dict(game=game, suite=suite, condition=condition, seed=seed, steps=steps)
    try:
        probe = make(suite, game, condition)
        n_actions = len(probe.actions)
        probe.close()
        rng = np.random.default_rng([seed, CONDITIONS[suite].index(condition)])
        acts = rng.integers(0, n_actions, size=steps).tolist()
        g1, f1, secs, rec, shape = play(suite, game, condition, seed, acts)
        g2, f2, _s, _r, _sh = play(suite, game, condition, seed, acts)
        diff = next((k for k, (x, y) in enumerate(zip(g1, g2)) if x != y), None)
        if diff is None and len(g1) != len(g2):
            diff = min(len(g1), len(g2))
        row.update(status="ok", identical=diff is None, first_diff_step=diff, flags_equal=f1 == f2,
                   n_actions=n_actions, grid=shape, n_colours=rec.get("n_colours"),
                   level_ends=sum(le for le, _ in f1), game_ends=sum(ge for _, ge in f1),
                   steps_per_second=round(steps / secs, 1) if secs > 0 else None, adapter=rec)
    except Exception as e:                       # recorded, never hidden
        row.update(status="error", error=f"{type(e).__name__}: {e}")
    p = out_path(out, suite, game, condition)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(row, f, indent=1)
    os.replace(tmp, p)
    return game, condition, row["status"], row.get("identical")


def main():
    ap = argparse.ArgumentParser(description="Adapter fidelity check (PREREG.md Section 2.1)")
    ap.add_argument("--suite", required=True, choices=sorted(CONDITIONS))
    ap.add_argument("--conditions", default="")
    ap.add_argument("--games", default="", help="comma list; default: every registered game of the suite")
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default=os.path.join(REPO, "runs", "fidelity"))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    conds = [c for c in args.conditions.split(",") if c] or CONDITIONS[args.suite]
    games = [g for g in args.games.split(",") if g] or games_for(args.suite)
    jobs = []
    for g in games:
        for c in conds:
            p = out_path(args.out, args.suite, g, c)
            if not args.force and os.path.exists(p):
                with open(p, encoding="utf-8") as f:
                    if json.load(f).get("status") == "ok":
                        continue
            jobs.append((args.suite, g, c, args.seed, args.steps, args.out))
    total = len(games) * len(conds)
    print(f"fidelity {args.suite}: {total} jobs ({len(games)} games x {len(conds)} conditions), "
          f"{len(jobs)} to run, {args.workers} workers", flush=True)
    if jobs:
        with Pool(args.workers) as pool:
            for g, c, st, ident in pool.imap_unordered(one, jobs):
                print(f"done {g} {c}: {st}" + ("" if st != "ok" else (" identical" if ident else " DIFFERS")),
                      flush=True)

    rows = []
    for g in games:
        for c in conds:
            p = out_path(args.out, args.suite, g, c)
            if os.path.exists(p):
                with open(p, encoding="utf-8") as f:
                    rows.append(json.load(f))
    head = ["game", "condition", "status", "identical", "flags", "grid", "colours", "n_actions",
            "level_ends", "game_ends", "steps_per_s"]
    cells = [[str(r["game"]), r["condition"], r["status"], str(r.get("identical")), str(r.get("flags_equal")),
              "x".join(map(str, r.get("grid") or [])), str(r.get("n_colours")), str(r.get("n_actions")),
              str(r.get("level_ends")), str(r.get("game_ends")), str(r.get("steps_per_second"))] for r in rows]
    w = [max([len(h)] + [len(c[i]) for c in cells]) for i, h in enumerate(head)]
    print("  ".join(h.ljust(w[i]) for i, h in enumerate(head)))
    for c in cells:
        print("  ".join(c[i].ljust(w[i]) for i in range(len(head))))
    ok = sum(r["status"] == "ok" for r in rows)
    ident = sum(bool(r.get("identical")) and bool(r.get("flags_equal")) for r in rows)
    print(f"summary: {ok} ok, {len(rows) - ok} error, {total - len(rows)} missing; identical on {ident} of {total}")
    for r in rows:
        if r["status"] != "ok":
            print(f"  error {r['game']} {r['condition']}: {r.get('error')}")


if __name__ == "__main__":
    main()
