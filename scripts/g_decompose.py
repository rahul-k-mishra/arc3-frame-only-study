"""
WHERE DOES THE SCORE COME FROM?  Efficiency or coverage - decided from runs you already have.

Reads the result JSONs written by g_ablate.py / g_diag.py / g_seeds.py (any file whose rows
carry game, score, levels, level_log) and, for every mechanism found in them, splits the
HELD-OUT score into what it is made of:

    level index      how much of the score comes from level-1 wins, level-2 wins, level 3+
    efficiency       for every level won, agent actions / human baseline actions, and the
                     level's score out of 100 (= min(115, 100 * (human/agent)^2))
    the two prizes   what the SAME runs would have scored if
                        (a) every won level had cost exactly the human count  (efficiency at cap)
                        (b) every won level had cost 2x / 5x the human count
                     against what they actually scored - no extra level crossed in any of them

If prize (a) is many times the recorded number, the score is in efficiency and a planner is the
build.  If prize (a) is close to the recorded number, the score is in coverage (more levels) and
a planner is the wrong build.  This script builds nothing and runs no game.

SELF-CHECK: the game score is recomputed from level_log + human baselines and compared with
the score the scorecard actually recorded for that run.  level_log undercounts by a few actions
(probe presses and resets are not counted per level), so the recomputed number should be
SLIGHTLY HIGHER than the recorded one, never lower.  The largest disagreement is printed;
a large one means level_log and the scorecard disagree about what was won, and the
decomposition is not to be trusted for that game.

WHAT IT READS FROM environment_files: ONLY the "baseline_actions" list in each game's
metadata.json - the human action count per level, the same numbers the scorecard prints after
every run (EnvironmentScore.level_baseline_actions).  It never opens a game's .py file.

    python g_decompose.py --files ablate_stage2.json
    python g_decompose.py --files ablate_stage2.json,seeds_results.json --env-dir environment_files
    python g_decompose.py --files ablate_stage2.json --games train      (train games instead)

JSON RECORD: everything printed is also written to runs/decompose_<tag>.json (--tag; default
<games>_<file stems>): the inputs, the per-mechanism table, the DISAGREEMENT lines, the largest
recorded/recomputed disagreement per mechanism, the >25% list, and the per-run won levels.  The
numbers in the JSON are the unrounded values behind the printed ones; nothing printed changes.
An existing JSON is never overwritten without --force (runs/ is never edited).

    python g_decompose.py --files ..unsblate_lenovo_6x4.json --env-dir <env> --tag lenovo_6x4_heldout
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(os.path.dirname(HERE), "runs")
HELD_OUT = ["ar25", "bp35", "cd82", "cn04", "g50t", "ka59", "r11l", "re86", "s5i5",
            "sb26", "sc25", "sk48", "sp80", "su15", "tn36", "tr87", "wa30"]
TRAIN = ["tu93", "ls20", "vc33", "m0r0", "ft09", "lp85", "lf52", "dc22"]
CAP = 115.0


def baselines(env_dir):
    """{game: [human actions per level]} from metadata.json ONLY (never the game source)."""
    out = {}
    for meta in glob.glob(os.path.join(env_dir, "*", "*", "metadata.json")):
        game = os.path.basename(os.path.dirname(os.path.dirname(meta)))
        try:
            d = json.load(open(meta))
            b = d.get("baseline_actions")
            if b:
                out[game] = [int(x) for x in b]
        except Exception as e:
            print(f"  metadata unreadable for {game}: {e!r}")
    return out


def level_score(human, agent):
    if agent <= 0:
        return 0.0
    return min(CAP, 100.0 * (human / agent) ** 2)


def game_score(level_actions, human):
    """The scorecard formula: sum(i * s_i) / sum(i) over ALL levels; a cap at the share of
    weight that was completed (both from arc_agi/scorecard.py)."""
    n = len(human)
    tot, wsum, wdone = 0.0, 0, 0
    for i in range(n):
        w = i + 1
        wsum += w
        if i < len(level_actions):
            s = level_score(human[i], level_actions[i])
            tot += w * s
            if s > 0:
                wdone += w
    sc = tot / wsum if wsum else 0.0
    return min(sc, 100.0 * wdone / wsum) if wsum else 0.0


def load_rows(files):
    rows = []
    paths = []
    for pat in files:
        hits = sorted(glob.glob(pat, recursive=True))
        if not hits and os.path.exists(pat):
            hits = [pat]
        paths.extend(hits)
    if not paths:
        print(f"NO RESULT FILES MATCH: {files}")
        print("  the JSONs are written next to the g_*.py that ran (ablate_<tag>.json, "
              "diag_<tag>.json, seeds_results.json), or to /kaggle/working on a Kaggle lab kernel")
        return rows
    for f in paths:
        try:
            data = json.load(open(f))
        except Exception as e:
            print(f"  unreadable {f}: {e!r}")
            continue
        n0 = len(rows)
        if isinstance(data, dict):            # g_seeds.py writes a dict of lists
            flat = []
            for k, v in data.items():
                if isinstance(v, list):
                    for r in v:
                        if isinstance(r, dict) and "game" in r:
                            r.setdefault("mode", str(k))
                            flat.append(r)
            data = flat
        for r in data:
            if not isinstance(r, dict) or "game" not in r:
                continue
            r.setdefault("mode", "all")
            r["_file"] = os.path.basename(f)
            rows.append(r)
        print(f"loaded {len(rows) - n0:5} runs from {f}")
    # MEASURED (lenovo, 24 Sep): the Kaggle kernel output is saved twice (top level and lab/), and
    # its seed-1000 runs are byte-identical to the lenovo's seed-1000 runs because the agent is
    # deterministic - so seed 1000 was counted three times and hash_state showed 0.4578 instead
    # of the 0.3329 of four equal seeds.  Identical runs are counted once.
    seen, uniq = set(), []
    for r in rows:
        key = (r["game"], r["mode"], str(r.get("seed")), round(float(r.get("score", 0.0)), 6),
               tuple((L.get("level"), L.get("actions"), L.get("ended")) for L in r.get("level_log", [])))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(r)
    if len(uniq) != len(rows):
        print(f"dropped {len(rows) - len(uniq)} duplicate runs (same game, mechanism, seed, score and level_log)")
    return uniq


def won_levels(r):
    """[(level_index_1based, agent_actions)] for the levels this run won, from level_log."""
    out = []
    for L in r.get("level_log", []):
        # older JSONs log the last level of a WON game as "WIN" (the loop broke before marking
        # it "won"); it is a won level
        if L.get("ended") in ("won", "WIN"):
            out.append((int(L.get("level", len(out))) + 1, int(L.get("actions", 0))))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", required=True, help="comma separated result JSONs")
    ap.add_argument("--env-dir", default=os.path.join(HERE, "environment_files"))
    ap.add_argument("--games", default="heldout", help="heldout | train | comma list")
    ap.add_argument("--tag", default=None,
                    help="writes runs/decompose_<tag>.json (default: <games>_<file stems>)")
    ap.add_argument("--out-dir", default=RUNS)
    ap.add_argument("--force", action="store_true", help="overwrite an existing JSON")
    args = ap.parse_args()
    tag = args.tag or "_".join([args.games.replace(",", "-")] + [
        os.path.splitext(os.path.basename(f))[0] for f in args.files.split(",")])
    out_path = os.path.join(args.out_dir, f"decompose_{tag}.json")
    if os.path.exists(out_path) and not args.force:
        print(f"{out_path} exists; runs/ is never overwritten silently (use --force)")
        return

    games = (HELD_OUT if args.games == "heldout" else TRAIN if args.games == "train"
             else args.games.split(","))
    human = baselines(args.env_dir)
    missing = [g for g in games if g not in human]
    if missing:
        print(f"NO BASELINES FOUND for {missing} under {args.env_dir} - those games are skipped")
        games = [g for g in games if g in human]
    rows = [r for r in load_rows(args.files.split(",")) if r["game"] in games]
    if not rows:
        print("no rows for these games in these files")
        return
    print(f"{len(rows)} runs over {len(games)} games "
          f"({'held-out' if args.games == 'heldout' else args.games}), "
          f"{len(set(r['mode'] for r in rows))} mechanisms\n")

    by_mode = defaultdict(list)
    for r in rows:
        by_mode[r["mode"]].append(r)
    rec_json = dict(script="scripts/g_decompose.py", created=time.strftime("%Y-%m-%d %H:%M:%S"),
                    tag=tag, files=args.files.split(","), env_dir=args.env_dir, games_arg=args.games,
                    games=games, runs=len(rows),
                    runs_per_file={f: sum(1 for r in rows if r["_file"] == f)
                                   for f in sorted({r["_file"] for r in rows})},
                    mechanisms={}, disagreements=[], largest_disagreement={},
                    level_log_vs_recorded_over_25pct=[], per_run=[])

    hdr = (f"{'mechanism':14} {'runs':>4} {'recorded':>9} {'recomputed':>10} {'maxdiff':>8} "
           f"{'lv1':>4} {'lv2':>4} {'lv3+':>4} {'from lv1':>9} {'AT HUMAN':>9} {'at 2x':>7} "
           f"{'at 5x':>7} {'med ratio':>9}")
    print(hdr)
    print("-" * len(hdr))
    for mode in sorted(by_mode):
        v = by_mode[mode]
        rec = sum(float(r.get("score", 0.0)) for r in v) / len(v)
        recomp, at_cap, at_2x, at_5x, from_lv1 = 0.0, 0.0, 0.0, 0.0, 0.0
        maxdiff, maxdiff_game = 0.0, "-"
        idx = defaultdict(int)
        ratios = []
        for r in v:
            h = human[r["game"]]
            wl = won_levels(r)
            # the run's levels_completed must agree with level_log's count of 'won' entries
            if int(r.get("levels", len(wl))) != len(wl):
                print(f"  DISAGREEMENT {r['game']} seed {r.get('seed')} {mode}: levels_completed="
                      f"{r.get('levels')} but level_log has {len(wl)} won entries")
                rec_json["disagreements"].append(dict(
                    game=r["game"], seed=r.get("seed"), mode=mode, file=r["_file"],
                    levels_completed=r.get("levels"), level_log_won=len(wl)))
            acts = [a for _i, a in wl]
            s = game_score(acts, h)
            recomp += s
            d = s - float(r.get("score", 0.0))
            if abs(d) > abs(maxdiff):
                maxdiff, maxdiff_game = d, f"{r['game']}/{r.get('seed')}"
            at_cap += game_score([h[i] for i in range(len(acts))], h)
            at_2x += game_score([2 * h[i] for i in range(len(acts))], h)
            at_5x += game_score([5 * h[i] for i in range(len(acts))], h)
            # share of the recomputed score contributed by level-1 wins alone
            if acts:
                from_lv1 += game_score(acts[:1], h)
            for i, a in wl:
                idx[1 if i == 1 else 2 if i == 2 else 3] += 1
                ratios.append(a / max(1, h[i - 1]))
        n = len(v)
        ratios.sort()
        med = ratios[len(ratios) // 2] if ratios else float("nan")
        print(f"{mode:14} {n:4} {rec:9.4f} {recomp / n:10.4f} {maxdiff:+8.3f} "
              f"{idx[1]:4} {idx[2]:4} {idx[3]:4} {from_lv1 / n:9.4f} {at_cap / n:9.4f} "
              f"{at_2x / n:7.4f} {at_5x / n:7.4f} {med:9.1f}")
        rec_json["mechanisms"][mode] = dict(
            runs=n, recorded=rec, recomputed=recomp / n, maxdiff=maxdiff, maxdiff_run=maxdiff_game,
            lv1=idx[1], lv2=idx[2], lv3plus=idx[3], from_lv1=from_lv1 / n, at_human=at_cap / n,
            at_2x=at_2x / n, at_5x=at_5x / n, median_ratio=None if med != med else med,
            ratios=ratios)
        if abs(maxdiff) > 0.5:
            print(f"    largest recorded/recomputed disagreement is on {maxdiff_game}: {maxdiff:+.3f} "
                  f"- level_log and the scorecard do not agree there")
            rec_json["largest_disagreement"][mode] = dict(run=maxdiff_game, diff=maxdiff)
    # every run where the two counters disagree by more than a quarter.  MEASURED in the build
    # sandbox on ft09: recorded 0.1156 implies ~276 actions on level 1, level_log says 152 - the
    # click scan's presses (and probe presses and resets) are stepped outside the per-level
    # counter.  So level_log FLATTERS efficiency; the true agent/human ratio is never better than
    # the one printed here, and AT HUMAN is exact because it does not use the agent's count.
    print("\nruns where level_log and the recorded score disagree by more than 25% "
          "(level_log misses scan/probe/reset presses; the true ratio is worse than shown):")
    n_bad = 0
    for mode in sorted(by_mode):
        for r in by_mode[mode]:
            wl = won_levels(r)
            if not wl:
                continue
            s = game_score([a for _i, a in wl], human[r["game"]])
            rec_r = float(r.get("score", 0.0))
            if rec_r > 0 and abs(s - rec_r) > 0.25 * rec_r:
                n_bad += 1
                print(f"   {r['game']:6} {mode:14} seed {str(r.get('seed')):>5} recorded {rec_r:8.4f} "
                      f"from level_log {s:8.4f}  levels {len(wl)}")
                rec_json["level_log_vs_recorded_over_25pct"].append(dict(
                    game=r["game"], mode=mode, seed=r.get("seed"), file=r["_file"],
                    recorded=rec_r, from_level_log=s, levels=len(wl)))
    if not n_bad:
        print("   none")
    print("\nrecorded    = mean of the scores the scorecard wrote (what the leaderboard would see)")
    print("recomputed  = the same from level_log + human baselines (self-check; a few % high is normal)")
    print("lv1/lv2/lv3+ = won levels by index, summed over runs")
    print("from lv1    = the recomputed mean if only the level-1 wins counted")
    print("AT HUMAN    = the SAME won levels at the human action count, nothing else changed")
    print("at 2x / 5x  = the same won levels at 2x / 5x the human count")
    print("med ratio   = median of agent/human actions over the won levels")

    # per game: won levels with their ratios, best mechanism aside
    print(f"\n{'game':6} {'mech':14} {'seed':>5} {'won levels  (index: agent/human -> level score)'}")
    for mode in sorted(by_mode):
        for r in sorted(by_mode[mode], key=lambda x: (x["game"], str(x.get("seed")))):
            wl = won_levels(r)
            if not wl:
                continue
            h = human[r["game"]]
            parts = [f"L{i}: {a}/{h[i - 1]} -> {level_score(h[i - 1], a):.2f}" for i, a in wl]
            print(f"{r['game']:6} {mode:14} {str(r.get('seed')):>5} {'; '.join(parts)}")

    # per-run rows (every run, including those with no won level, which the listing above skips)
    for mode in sorted(by_mode):
        for r in sorted(by_mode[mode], key=lambda x: (x["game"], str(x.get("seed")))):
            h = human[r["game"]]
            wl = won_levels(r)
            rec_json["per_run"].append(dict(
                game=r["game"], mode=mode, seed=r.get("seed"), file=r["_file"],
                recorded=float(r.get("score", 0.0)), levels_completed=r.get("levels"),
                recomputed=game_score([a for _i, a in wl], h),
                won_levels=[dict(level=i, agent=a, human=h[i - 1],
                                 level_score=level_score(h[i - 1], a)) for i, a in wl],
                card_levels=r.get("card_levels"), card_baseline=r.get("card_baseline")))

    os.makedirs(args.out_dir, exist_ok=True)
    tmp = out_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(rec_json, f, indent=1)
    os.replace(tmp, out_path)
    print()
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
