#!/usr/bin/env python
"""
pilot_check.py -- read-only checks on the W2 pilot rows and the fidelity outputs.

Reads   runs/suites/<suite>/<condition>/<mode>/<game>__<seed>.json   (pilot rows)
        runs/fidelity/<suite>/<game>__<condition>.json                 (fidelity outputs)
Writes  runs/pilot_checks/pilot_check.json
Plays no game, runs no census, changes no file under runs/suites or runs/fidelity.

What it reports, in order:
 1. inventory: rows per suite x condition x mode; rows with an error; rows with actions below the budget
 2. cross-condition identity: for every (game, mode, seed) present under both conditions of a suite,
    which fields differ between the two conditions after timing fields are dropped; the fields that
    differ in EVERY pair are the condition's own identity fields, the fields that differ in only SOME
    pairs are the outcome fields that the condition actually changed
 3. structural zeros: (game, mode) with zero levels on every seed under every condition
 4. wall time: longest row per suite, per mode and per condition, and the overhead factor
    agent overhead = wall time - env-only time, where env-only time = actions / steps-per-second from
    the fidelity output of the same game and condition (the fidelity check drives the same adapter)
 5. cap projection: for every game in the fidelity outputs, projected wall time for 20,000 actions
    = 20,000 / steps-per-second + (largest pilot agent overhead for that mode); the two terms add
    because the env is stepped and the agent computes in turn; games whose projection exceeds the cap
    given on the command line are listed

The row schema is not assumed: keys are discovered by name. Every discovered key is printed so the
reader can see what was compared.
"""
import argparse
import json
import re
import statistics
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

TIMING_RE = re.compile(r"(seconds|sec_per|elapsed|timestamp|started_at|finished_at|wall_time|wallclock|duration|hostname)", re.I)
SPS_RE = re.compile(r"(steps_per|per_second|per_sec|\bsps\b|step_rate|steps/s)", re.I)


def flatten(obj, prefix="", recurse_lists=False):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            out.update(flatten(v, key, recurse_lists))
    elif isinstance(obj, list) and recurse_lists:
        for i, v in enumerate(obj):
            key = f"{prefix}.{i}" if prefix else str(i)
            out.update(flatten(v, key, recurse_lists))
    else:
        if isinstance(obj, (list, dict)):
            out[prefix] = json.dumps(obj, sort_keys=True)
        else:
            out[prefix] = obj
    return out


def load_row(path_str):
    p = Path(path_str)
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    parts = p.parts
    meta = {}
    try:
        idx = parts.index("suites")
        meta["suite"] = parts[idx + 1]
        meta["condition"] = parts[idx + 2]
        meta["mode"] = parts[idx + 3]
        stem = p.stem
        if "__" in stem:
            game, seed = stem.rsplit("__", 1)
        else:
            game, seed = stem, ""
        meta["game"] = game
        meta["seed"] = seed
    except (ValueError, IndexError):
        pass
    if isinstance(data, list):
        data = data[0] if data else {}
    flat = flatten(data)
    # fall back to content keys when the path did not give the metadata
    for k in ("suite", "condition", "mode", "agent", "game", "seed"):
        if k not in meta or meta[k] == "":
            if k in flat:
                meta["mode" if k == "agent" else k] = str(flat[k])
    meta["seed"] = str(meta.get("seed", ""))
    return {"path": str(p), "meta": meta, "flat": flat}


def load_fidelity(path_str):
    p = Path(path_str)
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    parts = p.parts
    meta = {}
    try:
        idx = parts.index("fidelity")
        meta["suite"] = parts[idx + 1]
        stem = p.stem
        if "__" in stem:
            game, cond = stem.rsplit("__", 1)
        else:
            game, cond = stem, ""
        meta["game"] = game
        meta["condition"] = cond
    except (ValueError, IndexError):
        pass
    flat = flatten(data, recurse_lists=True)
    for k in ("suite", "game", "condition"):
        if not meta.get(k) and k in flat:
            meta[k] = str(flat[k])
    sps_vals = [v for k, v in flat.items() if SPS_RE.search(k) and isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0]
    sps_keys = sorted({k for k, v in flat.items() if SPS_RE.search(k) and isinstance(v, (int, float)) and not isinstance(v, bool)})
    return {"path": str(p), "meta": meta, "sps": (statistics.mean(sps_vals) if sps_vals else None), "sps_keys": sps_keys,
            "top_keys": sorted({k.split(".")[0] for k in flat})}


def pick_key(keys, name):
    exact = [k for k in keys if k == name]
    if exact:
        return name
    ends = sorted([k for k in keys if k.endswith("." + name)], key=len)
    return ends[0] if ends else None


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suites", default="runs/suites")
    ap.add_argument("--fidelity", default="runs/fidelity")
    ap.add_argument("--out", default="runs/pilot_checks/pilot_check.json")
    ap.add_argument("--budget", type=int, default=20000)
    ap.add_argument("--cap", action="append", default=[], help="suite=seconds, e.g. minigrid=3300 (repeatable)")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    caps = {}
    for c in args.cap:
        s, v = c.split("=")
        caps[s.strip()] = float(v)

    row_files = sorted(str(p) for p in Path(args.suites).rglob("*.json"))
    fid_files = sorted(str(p) for p in Path(args.fidelity).rglob("*.json"))
    print(f"pilot rows: {len(row_files)} files under {args.suites}; fidelity: {len(fid_files)} files under {args.fidelity}")
    if not row_files:
        print("no pilot rows found; nothing to check")
        sys.exit(1)
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        rows = list(ex.map(load_row, row_files, chunksize=8))
        fids = list(ex.map(load_fidelity, fid_files, chunksize=8)) if fid_files else []

    report = {"n_rows": len(rows), "n_fidelity": len(fids), "budget": args.budget, "caps": caps}
    all_keys = set()
    for r in rows:
        all_keys.update(r["flat"].keys())
    k_levels = pick_key(all_keys, "levels")
    k_actions = pick_key(all_keys, "actions")
    k_seconds = pick_key(all_keys, "seconds")
    k_error = pick_key(all_keys, "error")
    timing_keys = sorted(k for k in all_keys if TIMING_RE.search(k))
    print(f"keys used: levels={k_levels} actions={k_actions} seconds={k_seconds} error={k_error}")
    print(f"timing keys dropped from the cross-condition comparison ({len(timing_keys)}): {timing_keys}")
    report["keys"] = {"levels": k_levels, "actions": k_actions, "seconds": k_seconds, "error": k_error, "timing_dropped": timing_keys,
                      "top_level_keys": sorted({k.split('.')[0] for k in all_keys})}

    # ---- 1. inventory
    print("\n== 1. inventory")
    inv = defaultdict(int)
    errors, short = [], []
    for r in rows:
        m = r["meta"]
        inv[(m.get("suite"), m.get("condition"), m.get("mode"))] += 1
        e = r["flat"].get(k_error) if k_error else None
        if e not in (None, "", False, 0, "null"):
            errors.append((r["path"], str(e)[:200]))
        a = r["flat"].get(k_actions) if k_actions else None
        if num(a) and a < args.budget:
            short.append((r["path"], a))
    for key in sorted(inv, key=lambda t: tuple(str(x) for x in t)):
        print(f"  {key[0]:9s} {key[1]:11s} {key[2]:11s} rows {inv[key]}")
    if k_error is None:
        print("  no error field in the rows; errors are reported on the runner's console, and a failed job leaves no row, so the row counts above are the check")
    else:
        print(f"  rows with an error: {len(errors)}")
        for p, e in errors[:20]:
            print(f"    {p}: {e}")
    print(f"  rows with {k_actions} < {args.budget}: {len(short)}")
    for p, a in short[:20]:
        print(f"    {p}: {a}")
    report["inventory"] = {" | ".join(str(x) for x in k): v for k, v in inv.items()}
    report["errors"] = errors
    report["short_rows"] = short

    # ---- 2. cross-condition identity
    print("\n== 2. cross-condition identity (timing keys dropped)")
    by_suite = defaultdict(list)
    for r in rows:
        by_suite[r["meta"].get("suite")].append(r)
    xcond = {}
    for suite, srows in sorted(by_suite.items(), key=lambda t: str(t[0])):
        conds = sorted({r["meta"].get("condition") for r in srows}, key=str)
        if len(conds) != 2:
            print(f"  {suite}: {len(conds)} conditions {conds}; pairwise comparison needs exactly 2, skipped")
            continue
        c0, c1 = conds
        index = {}
        for r in srows:
            m = r["meta"]
            index[(m.get("condition"), m.get("game"), m.get("mode"), m.get("seed"))] = r
        per_gm = defaultdict(list)
        for (cond, game, mode, seed), r in index.items():
            if cond != c0:
                continue
            other = index.get((c1, game, mode, seed))
            if other is None:
                continue
            a = {k: v for k, v in r["flat"].items() if not TIMING_RE.search(k)}
            b = {k: v for k, v in other["flat"].items() if not TIMING_RE.search(k)}
            diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
            per_gm[(game, mode)].append({"seed": seed, "diff": diff})
        suite_out = {}
        print(f"  {suite}: {c0} vs {c1}")
        for (game, mode), pairs in sorted(per_gm.items(), key=lambda t: (str(t[0][0]), str(t[0][1]))):
            diffsets = [set(p["diff"]) for p in pairs]
            in_all = set.intersection(*diffsets) if diffsets else set()
            in_some = (set.union(*diffsets) - in_all) if diffsets else set()
            n_ident = sum(1 for d in diffsets if not d)
            n_same_outcome = sum(1 for d in diffsets if not (d - in_all))
            print(f"    {game:34s} {mode:10s} pairs {len(pairs):2d}  identical {n_ident:2d}  same apart from every-pair keys {n_same_outcome:2d}")
            print(f"      differ in every pair: {sorted(in_all)}")
            print(f"      differ in some pairs: {sorted(in_some)}")
            suite_out[f"{game} | {mode}"] = {"pairs": len(pairs), "identical": n_ident, "same_apart_from_every_pair_keys": n_same_outcome,
                                             "differ_in_every_pair": sorted(in_all), "differ_in_some_pairs": sorted(in_some),
                                             "per_seed": pairs}
        xcond[suite] = {"conditions": [c0, c1], "games": suite_out}
    report["cross_condition"] = xcond

    # ---- 3. structural zeros and level summary
    print("\n== 3. levels per (suite, game, mode, condition): min / median / max, zero-level rows")
    lv = defaultdict(list)
    for r in rows:
        m = r["meta"]
        v = r["flat"].get(k_levels) if k_levels else None
        if num(v):
            lv[(m.get("suite"), m.get("game"), m.get("mode"), m.get("condition"))].append(v)
    levels_out = {}
    for key in sorted(lv, key=lambda t: tuple(str(x) for x in t)):
        vals = lv[key]
        levels_out[" | ".join(str(x) for x in key)] = {"n": len(vals), "min": min(vals), "median": statistics.median(vals), "max": max(vals),
                                                     "zero_rows": sum(1 for v in vals if v == 0), "values": vals}
        print(f"  {key[0]:9s} {str(key[1]):34s} {str(key[2]):10s} {str(key[3]):11s} n {len(vals):2d}  min {min(vals):5g}  med {statistics.median(vals):7g}  max {max(vals):5g}  zeros {sum(1 for v in vals if v == 0)}")
    zeros_all = defaultdict(lambda: [0, 0])
    for key, vals in lv.items():
        z = zeros_all[(key[0], key[1], key[2])]
        z[0] += sum(1 for v in vals if v == 0)
        z[1] += len(vals)
    structural = [(k, z) for k, z in zeros_all.items() if z[1] > 0 and z[0] == z[1]]
    print("  (game, mode) with zero levels on every seed under every condition:")
    for (suite, game, mode), z in sorted(structural, key=lambda t: tuple(str(x) for x in t[0])):
        print(f"    {suite} {game} {mode}: {z[0]} of {z[1]} rows")
    report["levels"] = levels_out
    report["structural_zeros"] = [{"suite": k[0], "game": k[1], "mode": k[2], "rows": z[1]} for k, z in structural]

    # ---- 4. wall time and overhead factor
    print("\n== 4. wall time")
    sps = {}
    for f in fids:
        m = f["meta"]
        if f["sps"] is not None:
            sps[(m.get("suite"), m.get("game"), m.get("condition"))] = f["sps"]
    if fids:
        print(f"  fidelity steps-per-second key(s) found: {sorted(set(sum((f['sps_keys'] for f in fids), [])))}")
        if not sps:
            print(f"  no steps-per-second value recognised; top-level keys seen in fidelity files: {sorted(set(sum((f['top_keys'] for f in fids), [])))}")
    longest = {}
    overhead = defaultdict(list)
    for r in rows:
        m = r["meta"]
        s = r["flat"].get(k_seconds) if k_seconds else None
        a = r["flat"].get(k_actions) if k_actions else None
        if not num(s):
            continue
        key = (m.get("suite"), m.get("mode"), m.get("condition"))
        if key not in longest or s > longest[key][0]:
            longest[key] = (s, m.get("game"), m.get("seed"))
        rate = sps.get((m.get("suite"), m.get("game"), m.get("condition")))
        if rate and num(a) and a > 0:
            overhead[(m.get("suite"), m.get("mode"))].append({"overhead_s": s - (a / rate), "env_only_s": a / rate, "game": m.get("game"), "condition": m.get("condition"), "seed": m.get("seed"), "seconds": s, "sps": rate})
    for key in sorted(longest, key=lambda t: tuple(str(x) for x in t)):
        s, g, sd = longest[key]
        print(f"  longest {key[0]:9s} {str(key[1]):10s} {str(key[2]):11s}: {s:8.1f} s  ({g} seed {sd})")
    max_overhead = {}
    for key in sorted(overhead, key=lambda t: tuple(str(x) for x in t)):
        best = max(overhead[key], key=lambda d: d["overhead_s"])
        max_overhead[key] = best
        print(f"  max agent overhead {key[0]:9s} {str(key[1]):10s}: wall - env-only = {best['overhead_s']:8.1f} s  ({best['game']} {best['condition']} seed {best['seed']}: wall {best['seconds']:.1f} s, env-only {best['env_only_s']:.1f} s at {best['sps']:.1f} steps/s)")
    report["longest"] = {" | ".join(str(x) for x in k): {"seconds": v[0], "game": v[1], "seed": v[2]} for k, v in longest.items()}
    report["max_overhead"] = {" | ".join(str(x) for x in k): v for k, v in max_overhead.items()}

    # ---- 5. cap projection
    print("\n== 5. cap projection for 20,000 actions per game (20,000 / fidelity steps/s + max pilot agent overhead)")
    proj_out = {}
    pilot_games = {(r["meta"].get("suite"), r["meta"].get("game")) for r in rows}
    for suite in sorted({k[0] for k in sps}, key=str):
        modes = sorted({k[1] for k in max_overhead if k[0] == suite}, key=str)
        if not modes:
            print(f"  {suite}: no overhead factor available (no matching fidelity steps/s for the pilot games)")
            continue
        cap = caps.get(suite)
        entries = []
        for (s, game, cond), rate in sps.items():
            if s != suite:
                continue
            env_only = args.budget / rate
            for mode in modes:
                oh = max_overhead[(suite, mode)]["overhead_s"]
                entries.append({"game": game, "condition": cond, "mode": mode, "sps": rate, "env_only_s": env_only, "agent_overhead_s": oh, "projected_s": env_only + oh,
                                "pilot_game": (suite, game) in pilot_games, "over_cap": (cap is not None and env_only + oh > cap)})
        entries.sort(key=lambda d: -d["projected_s"])
        print(f"  {suite}: cap {cap}; {len(entries)} (game, condition, mode) projections; slowest 12:")
        for e in entries[:12]:
            flag = " OVER CAP" if e["over_cap"] else ""
            print(f"    {e['game']:34s} {e['condition']:11s} {e['mode']:10s} {e['sps']:7.1f} steps/s  env-only {e['env_only_s']:7.1f} s + agent {e['agent_overhead_s']:7.1f} s = projected {e['projected_s']:8.1f} s{flag}")
        n_over = sum(1 for e in entries if e["over_cap"])
        print(f"  {suite}: projections over the cap: {n_over}")
        proj_out[suite] = {"cap": cap, "n_over_cap": n_over, "entries": entries}
    report["cap_projection"] = proj_out

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1, default=str)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
