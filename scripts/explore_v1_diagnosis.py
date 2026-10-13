"""
EXPLORATORY -- explore_v1_diagnosis.py: why V1 failed, and the ARC V2 reported line on the 17
held-out games.  Written after gate G3 (docs/STATE.md amendment (k), outcome REFUTE).

EXPLORATORY.  Nothing this script prints or writes enters a claim, changes a registered file, or
alters the G3 outcome.  It changes no file under runs/suites and no registered script: it imports
scripts/analyze_common.py (census_from_report, majority, truth tables, confirmatory sets) and
scripts/analyze_v2.py (game_table, v2_stats) and uses them unchanged, so the census and V2 rules are
the registered ones, not a re-implementation.

Reads   runs/suites/<suite>/<condition>/nav/<game>__<seed>.json   (N rows; confirmatory games only)
        docs/GROUND_TRUTH_minigrid.md, docs/GROUND_TRUTH_procgen.md
        runs/navrun_prereg_e6_arc_25x10.json                        (Part 2 only)
Writes  runs/exploratory/v1_diagnosis.json
Plays no game.  Worker pool (--workers) for loading the rows, as scripts/pilot_check.py does.

PART 1 -- V1 diagnosis.  The subsets are those of analyze_v1.py: suite B raw and macro, "all" (161);
suite C center_off "all" (14) and "in_range" (9); suite C center_on "camera_distinct" (5).
  1a  per (suite, condition, subset, assumption): the confusion table of the seed-majority census
      verdict (analyze_common.majority) against the truth (A3-raw / A3-macro truth for suite B):
      rows truth holds / fails, columns census holds / fails / undetermined.
  1b  the disagreeing environments (census != truth; "undetermined" always disagrees), grouped by
      family.  Family = the id without its "MiniGrid-"/"BabyAI-" prefix kept as a prefix, its version,
      and its size/variant tokens (e.g. MiniGrid-LavaCrossingS9N2-v0 -> MiniGrid-LavaCrossing,
      BabyAI-GoToLocalS8N3-v0 -> BabyAI-GoToLocal); the mapping is written to the JSON.  Procgen:
      the game.
  1c  for each disagreeing family and assumption, the per-seed values that produced the per-seed
      verdict (analyze_common.census_from_report), summarised on the console (categorical values
      counted; numeric values min / median / max over the family's seeds) and kept per seed in the
      JSON:
        A1  learned shift per key (learn[k].shift)
        A2  learn[k].decided per key, counters.avatar_found
        A3  learn[k].agree / decided / shift, the level-1 fallback (levels[0].fallback), and A2
        A4  counters.wall_contradicted, walls, and A3 (A4 requires A3)
        A5  counters.goal_confirmed, goal_recorded, goal_reached_no_end; goal_targets summed over
            levels and on level 1
  1d  per (game, assumption): the number of seeds whose per-seed verdict differs from the game's
      majority verdict; console: per (suite, condition, assumption) how many games have any such
      seed, and the largest count.
  1e  a consistency check: the stored per-row census field against census_from_report(nav)
      recomputed here; the number of mismatches is printed (expected 0).

PART 2 -- the ARC V2 reported line on the 17 held-out games (PREREG.md Section 8).  The frozen
analyze_v2.py took all 25 public games with a census and printed a per-agent verdict on a line that
PREREG says is "reported, not tested" (STATE.md amendment (k)).  Here the same functions are applied:
(i) to all 25, as a check that the frozen table is reproduced (expected: N n=25 pos=14 auroc 0.4188;
R n=25 pos=15 auroc 0.4100; docs/tables/v2.md); (ii) to the 17 held-out games, labelled exploratory.
The verdict field is replaced by "EXPLORATORY, not tested".  ARC rows carry no adapter field, so the
nuisance features are constant and AUROC_B is 0.5, as in the frozen table.

Command (PowerShell, ARC venv, from the main checkout):

    cd D:\\Research\\arc3\\repo
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\explore_v1_diagnosis.py --workers 8

EXPECTED OUTPUT (shape):
    EXPLORATORY -- V1 diagnosis (not a registered analysis; enters no claim)
    loaded N rows: minigrid raw 1610, minigrid macro 1610, procgen center_off 140, procgen center_on 140
    census field vs census_from_report: 0 mismatches
    == EXPLORATORY 1a/1b/1c minigrid macro all A3 (n=161) ...   confusion table, families, counters
    ...
    == EXPLORATORY 1d seeds disagreeing with the game's majority ...
    == EXPLORATORY Part 2: ARC V2 reported line
    all 25 (check against docs/tables/v2.md): N n=25 pos=14 auroc=0.4188 ... ; R n=25 pos=15 auroc=0.4100 ...
    held-out 17: N n=17 pos=... auroc=... ci=[..., ...] ba=... auroc_B=0.5000 EXPLORATORY, not tested
    wrote runs\\exploratory\\v1_diagnosis.json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analyze_common as C  # noqa: E402
import analyze_v2 as V2  # noqa: E402

TAG = "EXPLORATORY"
ARC_HELD_OUT = ("ar25", "bp35", "cd82", "cn04", "g50t", "ka59", "r11l", "re86", "s5i5", "sb26", "sc25",
                "sk48", "sp80", "su15", "tn36", "tr87", "wa30")      # PREREG.md Section 8; CLAUDE.md
SUBSETS = {("minigrid", "raw"): [("all", None)], ("minigrid", "macro"): [("all", None)],
           ("procgen", "center_off"): [("all", None), ("in_range", C.IN_RANGE_C)],
           ("procgen", "center_on"): [("camera_distinct", C.CAMERA_DISTINCT_C)]}


# ------------------------------------------------------------------ loading
def load_one(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    r = d[0] if isinstance(d, list) else d
    keep = {k: r.get(k) for k in ("game", "seed", "suite", "condition", "agent", "census", "nav", "levels")}
    return keep


def family(game):
    if not (game.startswith("MiniGrid-") or game.startswith("BabyAI-")):
        return game
    prefix, rest = game.split("-", 1)
    rest = re.sub(r"-v\d+$", "", rest)
    toks = []
    for t in rest.split("-"):
        if re.match(r"^[A-Z]?\d", t) or t in ("Random", "Full"):
            break
        toks.append(t)
    name = "-".join(toks)
    name = re.sub(r"(S\d+)?(N\d+)?(R\d+)?(Random)?(Carrying)?(Debug)?\d*$", "", name) or name
    return f"{prefix}-{name}"


# ------------------------------------------------------------------ per-seed evidence
def evidence(nav, assumption):
    nav = nav or {}
    learn = nav.get("learn") or {}
    c = nav.get("counters") or {}
    levels = nav.get("levels") or [{}]
    lv0 = levels[0] or {}
    if assumption == "A1":
        return {"shift": {k: v.get("shift") for k, v in sorted(learn.items())}}
    if assumption == "A2":
        return {"decided": {k: v.get("decided") for k, v in sorted(learn.items())},
                "avatar_found": c.get("avatar_found", 0)}
    if assumption == "A3":
        return {"learn": {k: [v.get("agree"), v.get("decided"), v.get("shift")] for k, v in sorted(learn.items())},
                "fallback_level1": lv0.get("fallback"), "avatar_found": c.get("avatar_found", 0)}
    if assumption == "A4":
        return {"wall_contradicted": c.get("wall_contradicted", 0), "walls": nav.get("walls"),
                "n_walls": len(nav.get("walls") or []), "fallback_level1": lv0.get("fallback")}
    return {"goal_confirmed": c.get("goal_confirmed", 0), "goal_recorded": c.get("goal_recorded", 0),
            "goal_reached_no_end": c.get("goal_reached_no_end", 0),
            "goal_targets_total": sum((lv or {}).get("goal_targets", 0) or 0 for lv in levels),
            "goal_targets_level1": lv0.get("goal_targets", 0)}


def summarise(evs):
    """Console summary of a list of per-seed evidence dicts: categorical values counted, numeric
    values min / median / max."""
    out = {}
    keys = sorted({k for e in evs for k in e})
    for k in keys:
        vals = [e.get(k) for e in evs]
        if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in vals):
            out[k] = f"min {min(vals)} med {statistics.median(vals):g} max {max(vals)}"
        elif k in ("learn", "decided", "shift"):
            per_key = defaultdict(Counter)
            for v in vals:
                for kk, x in (v or {}).items():
                    per_key[kk][json.dumps(x)] += 1
            out[k] = {kk: dict(cn.most_common(4)) for kk, cn in sorted(per_key.items())}
        else:
            out[k] = dict(Counter(json.dumps(v) for v in vals).most_common(5))
    return out


# ------------------------------------------------------------------ part 1
def part1(rows_by, truth):
    report = {}
    for (suite, cond), subsets in SUBSETS.items():
        rows = rows_by.get((suite, cond), [])
        if not rows:
            print(f"\n== {TAG}: no N rows for {suite} {cond}")
            continue
        per_game = defaultdict(list)
        for r in rows:
            per_game[r["game"]].append(r)
        conf_games = [g for g in C.confirmatory(suite, truth[suite]) if g in per_game]
        for name, restrict in subsets:
            games = [g for g in conf_games if restrict is None or g in restrict]
            for a in C.ASSUMPTIONS:
                key = f"{suite} | {cond} | {name} | {a}"
                table = Counter()
                fam_dis = defaultdict(list)
                dissent = {}
                for g in games:
                    seeds = sorted(per_game[g], key=lambda r: r["seed"])
                    per_seed = [C.census_from_report(r.get("nav"))[a] for r in seeds]
                    maj = C.majority(per_seed)
                    t = C.truth_for(suite, cond, truth[suite][g], a)
                    table[(t, maj)] += 1
                    dissent[g] = sum(v != maj for v in per_seed)
                    if maj != t:
                        fam_dis[family(g)].append(dict(game=g, truth=t, census=maj, per_seed=[
                            dict(seed=r["seed"], verdict=v, evidence=evidence(r.get("nav"), a))
                            for r, v in zip(seeds, per_seed)]))
                print(f"\n== {TAG} 1a {suite} {cond} {name} {a} (n={len(games)})")
                print(f"   {TAG} confusion: truth \\ census   holds  fails  undetermined")
                for t in (C.HOLDS, C.FAILS):
                    print(f"   truth {t:5s}                  {table[(t, C.HOLDS)]:5d}  {table[(t, C.FAILS)]:5d}  "
                          f"{table[(t, C.UNDET)]:12d}")
                n_dis = sum(len(v) for v in fam_dis.values())
                print(f"   {TAG} 1b disagreeing: {n_dis} of {len(games)} in {len(fam_dis)} families")
                fam_out = {}
                for fam, items in sorted(fam_dis.items(), key=lambda kv: (-len(kv[1]), kv[0])):
                    kinds = Counter(f"truth {i['truth']} / census {i['census']}" for i in items)
                    evs = [s["evidence"] for i in items for s in i["per_seed"]]
                    summ = summarise(evs)
                    print(f"   {fam} ({len(items)}): {dict(kinds)}")
                    print(f"      ids: {', '.join(i['game'] for i in items)}")
                    print(f"      {TAG} 1c seeds {len(evs)}: {json.dumps(summ)[:900]}")
                    fam_out[fam] = dict(kinds=dict(kinds), summary=summ, games=items)
                report[key] = dict(n=len(games), confusion={f"{t} / {p}": table[(t, p)]
                                                            for t in (C.HOLDS, C.FAILS)
                                                            for p in (C.HOLDS, C.FAILS, C.UNDET)},
                                   families=fam_out, seeds_against_majority=dissent,
                                   family_of={g: family(g) for g in games})
    print(f"\n== {TAG} 1d seeds whose per-seed verdict differs from the game's majority")
    for key, v in report.items():
        d = v["seeds_against_majority"]
        hist = Counter(d.values())
        print(f"   {key}: games with any dissenting seed {sum(1 for x in d.values() if x)} of {len(d)}; "
              f"largest {max(d.values()) if d else 0}; histogram {dict(sorted(hist.items()))}")
    return report


# ------------------------------------------------------------------ part 2
def part2(arc_path, workers):
    print(f"\n== {TAG} Part 2: ARC V2 reported line (reported, never tested)")
    if not os.path.exists(arc_path):
        print(f"   {arc_path} not found; skipped")
        return None
    rows = C.load_rows([arc_path])
    census = C.census_by_game(rows, "arc", "native")
    held = [g for g in ARC_HELD_OUT if g in census]
    if len(held) != 17:
        print(f"   STOP: {len(held)} held-out games have a census, not 17")
    out = {}
    for name, games in (("all 25 (check against docs/tables/v2.md)", sorted(census)), ("held-out 17", held)):
        line = []
        for agent in ("N", "R"):
            gt = V2.game_table(rows, "arc", "native", agent, games, census)
            st = V2.v2_stats(gt, workers=workers)
            st["verdict"] = f"{TAG}, not tested"
            out[f"{name} | {agent}"] = dict(st, games=[x[0] for x in gt],
                                           per_game=[dict(game=x[0], S=x[1], P=x[2], Y=x[3]) for x in gt])
            f = lambda v: "None" if v is None else f"{v:.4f}"  # noqa: E731
            line.append(f"{agent} n={st['n']} pos={st['pos']} auroc={f(st['auroc'])} ci=[{f(st['ci_low'])}, "
                        f"{f(st['ci_high'])}] ba={f(st['ba'])} auroc_B={f(st['auroc_B'])} {st['verdict']}")
        print(f"   {name}: " + " ; ".join(line))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="EXPLORATORY V1 diagnosis and ARC held-out V2 line")
    ap.add_argument("--suites", default=os.path.join(REPO, "runs", "suites"))
    ap.add_argument("--arc", default=os.path.join(REPO, "runs", "navrun_prereg_e6_arc_25x10.json"))
    ap.add_argument("--out", default=os.path.join(REPO, "runs", "exploratory", "v1_diagnosis.json"))
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args(argv)
    print(f"{TAG} -- V1 diagnosis (not a registered analysis; enters no claim; G3 outcome unchanged)")

    truth = {"minigrid": C.parse_truth_minigrid(os.path.join(REPO, "docs", "GROUND_TRUTH_minigrid.md")),
             "procgen": C.parse_truth_procgen(os.path.join(REPO, "docs", "GROUND_TRUTH_procgen.md"))}
    paths = []
    for (suite, cond) in SUBSETS:
        conf = set(C.confirmatory(suite, truth[suite]))
        for p in sorted(glob.glob(os.path.join(args.suites, suite, cond, "nav", "*.json"))):
            if os.path.basename(p).rsplit("__", 1)[0] in conf:
                paths.append(p)
    with Pool(args.workers) as pool:
        loaded = pool.map(load_one, paths, chunksize=16)
    rows_by = defaultdict(list)
    mism = 0
    for r in loaded:
        rows_by[(r["suite"], r["condition"])].append(r)
        if r.get("census") and r["census"] != C.census_from_report(r.get("nav")):
            mism += 1
    print("loaded N rows: " + ", ".join(f"{s} {c} {len(rows_by[(s, c)])}" for (s, c) in SUBSETS))
    print(f"{TAG} 1e census field vs census_from_report: {mism} mismatches")

    report = dict(label=f"{TAG}: not a registered analysis; enters no claim; does not alter the G3 outcome "
                        f"(docs/STATE.md amendment (k))",
                  rows_loaded={f"{s} | {c}": len(rows_by[(s, c)]) for (s, c) in SUBSETS},
                  census_field_mismatches=mism, part1=part1(rows_by, truth), part2=part2(args.arc, args.workers))
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    tmp = args.out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1, default=str)
    os.replace(tmp, args.out)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
