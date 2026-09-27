"""
determinism_check.py -- center_on must equal center_off on the nine identical-frame Procgen games.

Infrastructure check in the class of scripts/fidelity_check.py and scripts/pilot_check.py (docs/PREREG.md
v1.1 draft D8 and D13): no census, no agent decision, no V1/V2/G number.  Plays no game; reads rows
written by scripts/run_suite.py; changes no file under runs/suites.

Why: at procgen 0.10.7 nine confirmatory games set center_agent false inside their own game_reset
(PREREG v1.1 D13), so the two camera conditions draw the same frames and the runs are deterministic
given the seed.  Every center_on row must therefore equal the center_off row of the same (game, mode,
seed) in every field, except
    the seven timing fields dropped by scripts/pilot_check.py:
        agent_seconds, env_sec_per_action, game_seconds, play_seconds, sec_per_action, seconds, seconds_cap
    (a flattened field is dropped when its last name component is one of these), and
    the three condition labels: condition, adapter.condition, adapter.camera.center_agent (exact paths).
Rows are flattened: dict keys joined with ".", list items indexed ("level_log.0.actions").

Reads   runs/suites/procgen/<condition>/<mode>/<game>__<seed>.json   (one-element lists)
Writes  runs/checks/determinism_check.json
Prints  per game: pairs compared, pairs identical, and every differing field name; then a total line.
Exit    0 if every pair is present and identical; 1 if any pair differs; 2 if a row is missing or
        unreadable (and no pair differs).

Standard library only.  A worker pool loads and compares the pairs (--workers).

Command (PowerShell; ARC venv; from the repository root, or from the tag worktree with --suites
pointing at the main repository's rows; docs/W2_COMMANDS.md block D7):

    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\determinism_check.py --suites D:\\Research\\arc3\\repo\\runs\\suites --out D:\\Research\\arc3\\repo\\runs\\checks\\determinism_check.json

EXPECTED OUTPUT (after block D4; 9 games x 3 modes x 10 seeds = 270 pairs):
    bossfight  pairs 30  identical 30
    ...                                      (one line per game, nine lines)
    total: 270 pairs compared, 270 identical, 0 differing, 0 missing -> PASS
    wrote D:\\Research\\arc3\\repo\\runs\\checks\\determinism_check.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from multiprocessing import Pool

# PREREG v1.1 draft D13: the nine confirmatory games that set center_agent false in game_reset.
# Equal to analyze_common.IN_RANGE_C (checked by scripts/test_determinism_check.py); copied here so
# that this script needs only the standard library.
NINE = ("bossfight", "chaser", "dodgeball", "heist", "leaper", "maze", "miner", "plunder", "starpilot")
MODES = ("hash_state", "nav", "i1")
TIMING = ("agent_seconds", "env_sec_per_action", "game_seconds", "play_seconds", "sec_per_action",
          "seconds", "seconds_cap")
LABELS = ("condition", "adapter.condition", "adapter.camera.center_agent")


def flatten(obj, prefix=""):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(obj, list):
        if not obj:
            out[prefix] = "[]"
        for i, v in enumerate(obj):
            out.update(flatten(v, f"{prefix}.{i}" if prefix else str(i)))
    else:
        out[prefix] = obj
    return out


def comparable(row):
    return {k: v for k, v in flatten(row).items()
            if k not in LABELS and k.split(".")[-1] not in TIMING}


def load(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d[0] if isinstance(d, list) else d


def compare(job):
    suites, game, mode, seed = job
    paths = [os.path.join(suites, "procgen", c, mode, f"{game}__{seed}.json") for c in ("center_off", "center_on")]
    try:
        off, on = (comparable(load(p)) for p in paths)
    except (OSError, ValueError, IndexError) as e:
        return dict(game=game, mode=mode, seed=seed, status="missing", error=f"{type(e).__name__}: {e}"[:300])
    diff = sorted(k for k in set(off) | set(on) if off.get(k, "<absent>") != on.get(k, "<absent>"))
    return dict(game=game, mode=mode, seed=seed, status="identical" if not diff else "differs", fields=diff)


def main(argv=None):
    ap = argparse.ArgumentParser(description="center_on = center_off on the nine identical-frame games")
    ap.add_argument("--suites", default=os.path.join("runs", "suites"))
    ap.add_argument("--out", default=os.path.join("runs", "checks", "determinism_check.json"))
    ap.add_argument("--games", default=",".join(NINE))
    ap.add_argument("--modes", default=",".join(MODES))
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args(argv)

    games = [g for g in args.games.split(",") if g]
    bad = [g for g in games if g not in NINE]
    if bad:
        sys.exit(f"STOP: {bad} are not among the nine identical-frame games {NINE}")
    modes = [m for m in args.modes.split(",") if m]
    jobs = [(args.suites, g, m, 1000 + s) for g in games for m in modes for s in range(args.seeds)]
    if args.workers > 1:
        with Pool(args.workers) as pool:
            res = pool.map(compare, jobs, chunksize=8)
    else:
        res = [compare(j) for j in jobs]

    per_game = {}
    for r in res:
        g = per_game.setdefault(r["game"], dict(compared=0, identical=0, missing=0, differing_fields=[], differing_pairs=[]))
        if r["status"] == "missing":
            g["missing"] += 1
            continue
        g["compared"] += 1
        if r["status"] == "identical":
            g["identical"] += 1
        else:
            g["differing_pairs"].append(dict(mode=r["mode"], seed=r["seed"], fields=r["fields"]))
            g["differing_fields"] = sorted(set(g["differing_fields"]) | set(r["fields"]))
    for game in games:
        g = per_game[game]
        line = f"{game:10s} pairs {g['compared']:3d}  identical {g['identical']:3d}"
        if g["missing"]:
            line += f"  missing {g['missing']}"
        if g["differing_fields"]:
            line += f"  DIFFERING FIELDS {g['differing_fields']}"
        print(line)
        for p in g["differing_pairs"]:
            print(f"    {p['mode']} seed {p['seed']}: {p['fields']}")
    n = sum(g["compared"] for g in per_game.values())
    same = sum(g["identical"] for g in per_game.values())
    miss = sum(g["missing"] for g in per_game.values())
    code = 1 if same < n else (2 if miss else 0)
    verdict = {0: "PASS", 1: "FAIL (a pair differs)", 2: "INCOMPLETE (rows missing)"}[code]
    print(f"total: {n} pairs compared, {same} identical, {n - same} differing, {miss} missing -> {verdict}")

    out = dict(script="scripts/determinism_check.py", games=games, modes=modes, seeds=args.seeds,
               timing_fields_dropped=list(TIMING), label_fields_dropped=list(LABELS),
               pairs_compared=n, pairs_identical=same, pairs_missing=miss, verdict=verdict,
               per_game=per_game, missing=[r for r in res if r["status"] == "missing"])
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    tmp = args.out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    os.replace(tmp, args.out)
    print(f"wrote {args.out}")
    return code


if __name__ == "__main__":
    sys.exit(main())
