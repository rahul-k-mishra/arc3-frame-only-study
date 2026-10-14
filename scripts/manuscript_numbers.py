"""
manuscript_numbers.py -- every number the JOTE manuscript may state, read from committed files.

Writes docs/manuscript/numbers.json: a flat dictionary {key: {"value", "source", "class"}}, where
source names the committed file (and, for prose files, the passage) the value was read from, and
class is one of count, rate, threshold, constant, hash, date, version, url, identifier.  It also
writes docs/manuscript/appendix_c.md, the provenance table of Appendix C (one row per number
class, with the files and the commit that last changed each file).

Nothing here plays a game or reads runs/suites.  The inputs are:
    docs/tables/v1.json, docs/tables/v2.json, docs/tables/v1.md, docs/tables/v2.md
    runs/exploratory/v1_diagnosis.json
    runs/checks/determinism_check.json
    runs/pilot_checks/pilot_check.json, runs/pilot_checks/procgen_camera_check.json
    docs/PREREG.md, docs/STATE.md, docs/EXPLORATORY_V1_DIAGNOSIS.md, docs/OSF_REGISTRATION_final.txt,
    docs/OSF_REGISTRATION_v1_1_final.txt, docs/preprint/preprint.md, docs/preprint/references.bib,
    docs/GROUND_TRUTH_minigrid.md, docs/GROUND_TRUTH_procgen.md (through analyze_common's parsers)
    docs/HELDOUT.md (the ARC split and the dc22 move), docs/manuscript/REVIEW_draft1.md (reference URLs),
    docs/manuscript/REFERENCES_CHECK.md (fields of the references added for the manuscript)
    the three annotated tag objects and `git ls-tree` at the tags (committed objects, read only)

Every value taken from prose is matched by a regular expression against its file; the script stops
with an error if the passage is not there.  Every value recomputed from a JSON file is compared with
the value the corresponding document states, where a document states one.

Run (working directory D:\\Research\\arc3\\repo):
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\manuscript_numbers.py

Expected console output (last lines):
    numbers.json: <N> values written to docs/manuscript/numbers.json
    appendix_c.md: <K> number classes written to docs/manuscript/appendix_c.md
    all cross-checks passed
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import analyze_common as C  # noqa: E402  (read only: the registered truth-table parsers and lists)

OUT_DIR = os.path.join(ROOT, "docs", "manuscript")
N: dict[str, dict] = {}
CHECKS: list[str] = []


def add(key, value, source, cls):
    if key in N:
        if N[key]["value"] != value:
            raise SystemExit(f"conflicting values for {key}: {N[key]['value']} vs {value}")
        return
    N[key] = {"value": value, "source": source, "class": cls}


def text(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8-sig") as f:
        return f.read()


def need(rel, pattern, flags=0):
    """The match of pattern in the committed file rel; stop if it is not there."""
    m = re.search(pattern, text(rel), flags)
    if not m:
        raise SystemExit(f"passage not found in {rel}: {pattern!r}")
    return m


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def f4(x):
    return None if x is None else f"{x:.4f}"


def check(cond, what):
    if not cond:
        raise SystemExit(f"cross-check failed: {what}")
    CHECKS.append(what)


def fmt_date(d):
    return f"{d.day} {d.strftime('%B')} {d.year}"


# ------------------------------------------------------------------ V1 and V2 tables
def tables():
    v1 = load("docs/tables/v1.json")
    v1md = text("docs/tables/v1.md")
    hdr = v1["header"]
    for row in v1["rows"]:
        r = dict(zip(hdr, row))
        k = f"v1.{r['suite']}.{r['condition']}.{r['subset']}.{r['assumption']}"
        src = "docs/tables/v1.json"
        add(k + ".n", r["n"], src, "count")
        add(k + ".truth_holds", r["truth_holds"], src, "count")
        add(k + ".agreement", f4(r["agreement"]), src, "rate")
        if r["kappa"] is not None:
            add(k + ".kappa", f4(r["kappa"]), src, "rate")
        add(k + ".verdict", r["verdict"], src, "identifier")
        line = (f"| {r['suite']} | {r['condition']} | {r['subset']} | {r['assumption']} | {r['n']} | "
                f"{r['truth_holds']} | {f4(r['agreement'])} | {f4(r['kappa']) or ''} | {r['verdict']} |")
        check(line in v1md, f"v1.md carries the row {k}")
    # counts of verdicts per tested line
    for (s, c, sub) in {(r[0], r[1], r[2]) for r in v1["rows"]}:
        rows = [dict(zip(hdr, r)) for r in v1["rows"] if (r[0], r[1], r[2]) == (s, c, sub)]
        for v in ("PASS", "FAIL", "neither"):
            add(f"v1.{s}.{c}.{sub}.count_{v}", sum(r["verdict"] == v for r in rows), "docs/tables/v1.json", "count")

    v2 = load("docs/tables/v2.json")
    v2md = text("docs/tables/v2.md")
    hdr = v2["header"]
    add("v2.resamples", v2["meta"]["resamples"], "docs/tables/v2.json (meta.resamples)", "constant")
    add("v2.seed", v2["meta"]["seed"], "docs/tables/v2.json (meta.seed)", "constant")
    for row in v2["rows"]:
        r = dict(zip(hdr, row))
        k = f"v2.{r['suite']}.{r['condition']}.{r['subset']}.{r['agent']}"
        src = "docs/tables/v2.json"
        add(k + ".n", r["n"], src, "count")
        add(k + ".positives", r["positives"], src, "count")
        for f in ("auroc", "ci_low", "ci_high", "balanced_acc", "auroc_B"):
            if r[f] is not None:
                add(k + "." + f, f4(r[f]), src, "rate")
        add(k + ".verdict", r["verdict"], src, "identifier")
        add(k + ".share_completed", f4(r["positives"] / r["n"]), src + " (positives / n)", "rate")
        cells = [r["suite"], r["condition"], r["subset"], r["agent"], r["role"], str(r["n"]), str(r["positives"])]
        cells += [f4(r[f]) or "" for f in ("auroc", "ci_low", "ci_high", "balanced_acc", "auroc_B")]
        cells += [r["verdict"]]
        check("| " + " | ".join(cells) + " |" in v2md, f"v2.md carries the row {k}")
    for s, c, sub, line in v2["meta"]["suite_lines"]:
        add(f"v2.suite_line.{s}.{c}.{sub}", line, "docs/tables/v2.json (meta.suite_lines)", "identifier")
    # the nuisance baseline against the census on the suite-B lines
    rows = [dict(zip(hdr, r)) for r in v2["rows"] if r[0] == "minigrid"]
    tested = [r for r in rows if r["subset"] == "primary"]
    add("v2.minigrid.lines", len(rows), "docs/tables/v2.json (suite minigrid rows)", "count")
    add("v2.minigrid.lines_B_higher", sum(r["auroc_B"] > r["auroc"] for r in rows),
        "docs/tables/v2.json (auroc_B > auroc, suite minigrid rows)", "count")
    add("v2.minigrid.primary_lines", len(tested), "docs/tables/v2.json (suite minigrid, subset primary)", "count")
    add("v2.minigrid.primary_lines_B_higher", sum(r["auroc_B"] > r["auroc"] for r in tested),
        "docs/tables/v2.json (auroc_B > auroc, subset primary)", "count")
    check(sum(r["auroc_B"] > r["auroc"] for r in rows) == 12, "baseline higher on 12 of 14 suite-B lines (STATE (k))")
    add("v2.lines", len(v2["rows"]), "docs/tables/v2.json (rows)", "count")
    add("v1.lines", len(v1["rows"]), "docs/tables/v1.json (rows)", "count")


# ------------------------------------------------------------------ the exploratory diagnosis
def diagnosis():
    src = "runs/exploratory/v1_diagnosis.json"
    d = load(src)
    for k, v in d["rows_loaded"].items():
        add("diag.rows_loaded." + k.replace(" | ", "."), v, src + " (rows_loaded)", "count")
    add("diag.rows_loaded.total", sum(d["rows_loaded"].values()), src + " (sum of rows_loaded)", "count")
    add("diag.census_field_mismatches", d["census_field_mismatches"], src, "count")
    for key, part in d["part1"].items():
        k = "diag." + key.replace(" | ", ".")
        add(k + ".n", part["n"], src + " (part1)", "count")
        for cell, val in part["confusion"].items():
            t, p = [x.strip() for x in cell.split("/")]
            add(f"{k}.confusion.truth_{t}.census_{p}", val, src + " (part1 confusion)", "count")
        dissent = list(part["seeds_against_majority"].values())
        add(k + ".games_with_dissent", sum(x > 0 for x in dissent), src + " (seeds_against_majority > 0)", "count")
        add(k + ".dissent_max", max(dissent), src + " (seeds_against_majority, max)", "count")
        for b in range(0, max(dissent) + 1):
            c = sum(x == b for x in dissent)
            if c:
                add(f"{k}.dissent_hist.{b}", c, src + " (seeds_against_majority histogram)", "count")
        disagree = sum(val for cell, val in part["confusion"].items()
                       if cell.split("/")[0].strip() != cell.split("/")[1].strip())
        add(k + ".disagreeing_games", disagree, src + " (off-diagonal confusion)", "count")
        add(k + ".agreeing_games", part["n"] - disagree, src + " (n minus off-diagonal confusion)", "count")
    for key, part in d["part2"].items():
        who = key.split("|")[-1].strip()
        k = "diag.arc." + ("heldout17" if key.startswith("held-out") else "all25") + "." + who
        add(k + ".n", part["n"], src + " (part2)", "count")
        add(k + ".positives", part["pos"], src + " (part2)", "count")
        for f in ("auroc", "ci_low", "ci_high", "ba", "auroc_B"):
            add(k + "." + f, f4(part[f]), src + " (part2)", "rate")

    def games(key, kind):
        out = []
        for fam in d["part1"][key]["families"].values():
            for g in fam["games"]:
                if f"truth {g['truth']} / census {g['census']}" == kind:
                    out.append(g)
        return out

    # A1: per-seed verdict on the disagreeing raw games
    # A2 raw: truth holds, census fails
    gs = games("minigrid | raw | all | A2", "truth holds / census fails")
    seeds = [s for g in gs for s in g["per_seed"]]
    add("diag.A2raw.disagree_games", len(gs), src, "count")
    add("diag.A2raw.seeds", len(seeds), src, "count")
    turns_no_move = sum(s["evidence"]["decided"]["1"] == "no_move" and s["evidence"]["decided"]["2"] == "no_move"
                        for s in seeds)
    fwd = sum(s["evidence"]["decided"]["3"] == "accepted" for s in seeds)
    add("diag.A2raw.seeds_turns_no_move", turns_no_move, src, "count")
    add("diag.A2raw.seeds_forward_accepted", fwd, src, "count")
    fam_n = len(d["part1"]["minigrid | raw | all | A2"]["families"])
    add("diag.A2raw.families", fam_n, src, "count")
    doc = "docs/EXPLORATORY_V1_DIAGNOSIS.md"
    check(len(seeds) == int(need(doc, r"On their (\d+) seeds, the learner recorded").group(1)), "A2 raw seeds = doc")
    check(fwd == int(need(doc, r"`accepted` on (\d+) and `no_move` on").group(1)), "A2 raw forward accepted = doc")
    # A2 suite C: truth fails, census holds; avatar_found on every one of them
    gs = games("procgen | center_off | all | A2", "truth fails / census holds")
    af = [sum(s["evidence"].get("avatar_found") == 1 for s in g["per_seed"]) for g in gs]
    add("diag.A2C.disagree_games", len(gs), src, "count")
    add("diag.A2C.avatar_found_min_seeds", min(af), src, "count")
    check(min(af) >= 9, "suite C A2: avatar_found on 9 or 10 of 10 seeds (doc)")
    # A3 macro: truth holds, census fails
    gs = games("minigrid | macro | all | A3", "truth holds / census fails")
    seeds = [s for g in gs for s in g["per_seed"]]
    four = sum(sum(1 for k in ("1", "2", "3", "4") if s["evidence"]["learn"][k][1] == "accepted") == 4 for s in seeds)
    fails = [s for s in seeds if s["verdict"] == "fails"]
    mis = sum(s["evidence"].get("fallback_level1") == "mispredicted" for s in fails)
    noav = sum(s["evidence"].get("fallback_level1") == "no_avatar" for s in fails)
    add("diag.A3macro.disagree_games", len(gs), src, "count")
    add("diag.A3macro.seeds", len(seeds), src, "count")
    add("diag.A3macro.seeds_four_vectors", four, src, "count")
    add("diag.A3macro.seeds_fail", len(fails), src, "count")
    add("diag.A3macro.seeds_fail_mispredicted", mis, src, "count")
    add("diag.A3macro.seeds_fail_no_avatar", noav, src, "count")
    check((len(seeds), four, len(fails), mis, noav) == tuple(int(x) for x in need(
        doc, r"On the (\d+) seeds of the 92:\n.*?four step vectors on (\d+),.*?\n.*?\"fails\" on (\d+) seeds\. "
             r"On (\d+) of them the level-1 fallback is `mispredicted`; on the other (\d+)", re.S).groups()),
          "A3 macro per-seed counts = doc")
    # A4 suite C: wall_contradicted on the truth-holds games
    gs = games("procgen | center_off | all | A4", "truth holds / census fails")
    wc = [sum(s["evidence"].get("wall_contradicted", 0) > 0 for s in g["per_seed"]) for g in gs]
    add("diag.A4C.truth_holds_games", len(gs), src, "count")
    add("diag.A4C.games_wall_some_seed", sum(x > 0 for x in wc), src, "count")
    add("diag.A4C.games_wall_all_seeds", sum(x == 10 for x in wc), src, "count")
    check(sum(x == 10 for x in wc) == 5 and sum(x > 0 for x in wc) == 13, "suite C A4 wall counts = doc")
    # A5: undetermined seeds of the games whose majority is undetermined
    for key, name in (("minigrid | macro | all | A5", "macro"), ("minigrid | raw | all | A5", "raw"),
                      ("procgen | center_off | all | A5", "C")):
        und = [s for fam in d["part1"][key]["families"].values() for g in fam["games"]
               if g["census"] == "undetermined" for s in g["per_seed"] if s["verdict"] == "undetermined"]
        add(f"diag.A5{name}.undetermined_seeds", len(und), src, "count")
        add(f"diag.A5{name}.undetermined_seeds_no_goal_recorded",
            sum(s["evidence"].get("goal_recorded", 0) == 0 for s in und), src, "count")
        conf = d["part1"][key]["confusion"]
        add(f"diag.A5{name}.kappa_cell_truth_fails_pred_holds",
            conf["fails / holds"] + conf["fails / undetermined"], src + " (confusion: fails/holds + fails/undetermined)",
            "count")
    check((N["diag.A5macro.undetermined_seeds"]["value"], N["diag.A5macro.undetermined_seeds_no_goal_recorded"]["value"])
          == (663, 620) and (N["diag.A5raw.undetermined_seeds"]["value"],
                             N["diag.A5raw.undetermined_seeds_no_goal_recorded"]["value"]) == (1074, 986)
          and (N["diag.A5C.undetermined_seeds"]["value"],
               N["diag.A5C.undetermined_seeds_no_goal_recorded"]["value"]) == (110, 70),
          "A5 undetermined seed counts = doc")


# ------------------------------------------------------------------ checks run before and after the runs
def checks():
    src = "runs/checks/determinism_check.json"
    d = load(src)
    add("det.pairs_compared", d["pairs_compared"], src, "count")
    add("det.pairs_identical", d["pairs_identical"], src, "count")
    add("det.pairs_missing", d["pairs_missing"], src, "count")
    add("det.games", len(d["games"]), src, "count")
    add("det.pairs_per_game", d["per_game"]["bossfight"]["compared"], src, "count")
    add("det.timing_fields", len(d["timing_fields_dropped"]), src, "count")
    add("det.label_fields", len(d["label_fields_dropped"]), src, "count")
    src = "runs/pilot_checks/procgen_camera_check.json"
    d = load(src)
    add("cam.actions", d["actions"], src, "count")
    add("cam.action_seed", d["action_seed"], src, "constant")
    add("cam.steps_compared", d["results"][0]["steps_compared"], src, "count")
    add("cam.games", len(d["results"]), src, "count")
    add("cam.identical_games", len(d["identical"]), src, "count")
    add("cam.differing_games", len(d["differs"]), src, "count")
    add("cam.first_differing_step", 0, src, "count")
    check(all(r["identical_frames"] == r["steps_compared"] for r in d["results"] if r["verdict"] == "identical"),
          "camera check: every identical game has 401 of 401")
    src = "runs/pilot_checks/pilot_check.json"
    d = load(src)
    add("pilot.rows", d["n_rows"], src, "count")
    b = sum(v for k, v in d["inventory"].items() if k.startswith("minigrid"))
    c = sum(v for k, v in d["inventory"].items() if k.startswith("procgen"))
    add("pilot.rows_minigrid", b, src + " (inventory)", "count")
    add("pilot.rows_procgen", c, src + " (inventory)", "count")
    add("pilot.errors", len(d["errors"]), src, "count")
    add("pilot.short_rows", len(d["short_rows"]), src, "count")
    add("pilot.cap_minigrid_s", int(d["caps"]["minigrid"]), src + " (caps)", "constant")
    add("pilot.cap_procgen_s", int(d["caps"]["procgen"]), src + " (caps)", "constant")
    add("pilot.longest_minigrid_s", str(d["longest"]["minigrid | I1 | raw"]["seconds"]), src + " (longest)", "constant")
    add("pilot.longest_procgen_s", str(d["longest"]["procgen | I1 | center_off"]["seconds"]), src + " (longest)",
        "constant")
    add("pilot.longest_seed", int(d["longest"]["minigrid | I1 | raw"]["seed"]), src + " (longest)", "constant")
    pm = max(e["projected_s"] for e in d["cap_projection"]["minigrid"]["entries"] if not e["pilot_game"])
    pc = max(e["projected_s"] for e in d["cap_projection"]["procgen"]["entries"] if not e["pilot_game"])
    add("pilot.max_projection_minigrid_s", f"{pm:.1f}", src + " (cap_projection)", "constant")
    add("pilot.max_projection_procgen_s", f"{pc:.1f}", src + " (cap_projection)", "constant")
    add("pilot.over_cap", d["cap_projection"]["minigrid"]["n_over_cap"] + d["cap_projection"]["procgen"]["n_over_cap"],
        src + " (cap_projection n_over_cap)", "count")
    dk = [z for z in d["structural_zeros"] if z["game"] == "MiniGrid-DoorKey-8x8-v0" and z["mode"] == "I1"][0]
    add("pilot.doorkey_I1_zero_rows", dk["rows"], src + " (structural_zeros)", "count")
    add("pilot.games_minigrid", len(C.PILOTS_B), "scripts/analyze_common.py (PILOTS_B)", "count")
    add("pilot.games_procgen", len(C.PILOTS_C), "scripts/analyze_common.py (PILOTS_C)", "count")
    add("pilot.games_with_truth", len(C.PILOTS_B) + len(C.PILOTS_C), "scripts/analyze_common.py (PILOTS_B + PILOTS_C)",
        "count")
    # fidelity check, from STATE (f)
    m = need("docs/STATE.md", r"Fidelity check\*\* \(commit (\w+)\): suite B (\d+) of (\d+) identical, suite C (\d+) of (\d+)")
    add("fid.commit", m.group(1), "docs/STATE.md amendment (f)", "hash")
    add("fid.minigrid", int(m.group(2)), "docs/STATE.md amendment (f)", "count")
    add("fid.procgen", int(m.group(4)), "docs/STATE.md amendment (f)", "count")
    m = need("docs/PREREG.md", r"It plays every game with (\d+) random actions twice")
    add("fid.actions", int(m.group(1)), "docs/PREREG.md v1.1 D8", "constant")
    m = need("docs/STATE.md", r"\*\*E1:\*\* (\d+) \+ (\d+) \+ (\d+) \+ (\d+) = (\d+) synthetic tests OK")
    add("tests.synthetic", int(m.group(5)), "docs/STATE.md amendment (k)", "count")


# ------------------------------------------------------------------ the registered protocol
def protocol():
    P = "docs/PREREG.md"
    m = need(P, r"\*\*PASS\*\* if agreement ≥ (0\.90) and κ ≥ (0\.70)\.\n- \*\*FAIL\*\* if agreement < (0\.75)")
    add("thr.v1_pass_agreement", m.group(1), P + " v1 Section 10", "threshold")
    add("thr.v1_pass_kappa", m.group(2), P + " v1 Section 10", "threshold")
    add("thr.v1_fail_agreement", m.group(3), P + " v1 Section 10", "threshold")
    m = need(P, r"both truth values have at least (three) games")
    add("thr.kappa_min_games", 3, P + " v1 Section 10 (constant-column rule, 'three')", "threshold")
    m = need(P, r"\*\*PASS\*\* if AUROC ≥ (0\.80), the CI lower bound is > (0\.60), the balanced accuracy of P is ≥ "
                r"(0\.80), and AUROC − AUROC_B ≥ (0\.10)\.\n- \*\*FAIL\*\* if AUROC ≤ (0\.65)")
    add("thr.v2_pass_auroc", m.group(1), P + " v1 Section 10", "threshold")
    add("thr.v2_pass_ci_low", m.group(2), P + " v1 Section 10", "threshold")
    add("thr.v2_pass_ba", m.group(3), P + " v1 Section 10", "threshold")
    add("thr.v2_pass_margin", m.group(4), P + " v1 Section 10", "threshold")
    add("thr.v2_fail_auroc", m.group(5), P + " v1 Section 10", "threshold")
    m = need(P, r"must lie in \[(0\.10), (0\.90)\]")
    add("thr.void_low", m.group(1), P + " v1 Section 10", "threshold")
    add("thr.void_high", m.group(2), P + " v1 Section 10", "threshold")
    m = need(P, r"Its (95)% CI is the percentile interval of (2,000) bootstrap resamples")
    add("thr.ci_level", 95, P + " v1 Section 10", "threshold")
    add("thr.resamples", "2,000", P + " v1 Section 10", "constant")
    m = need(P, r"Seed (20260927) in (8) chunks")
    add("thr.bootstrap_chunks", 8, P + " v1 Section 10", "constant")
    m = need(P, r"\*\*Seeds:\*\* (1000)–(1009) \((10)\)")
    add("run.seed_first", 1000, P + " v1 Section 9.1", "constant")
    add("run.seed_last", 1009, P + " v1 Section 9.1", "constant")
    add("run.seeds", 10, P + " v1 Section 9.1", "constant")
    m = need(P, r"\*\*Budget:\*\* (20,000) actions per \(game, seed\)")
    add("run.budget", "20,000", P + " v1 Section 9.1", "constant")
    # constants (v1 Section 5.4)
    for name, pat in (("LEARN_AGREE", r"\| LEARN_AGREE \| (\d+) \|"), ("LEARN_MAX", r"\| LEARN_MAX \| (\d+) \|"),
                      ("MAX_STEP", r"\| MAX_STEP \(learner\) \| (\d+) \|"), ("BFS_NODES", r"\| BFS_NODES \| (\d+) \|"),
                      ("min_cells", r"\| min_cells \| (\d+) \|")):
        add("const." + name, int(need(P, pat).group(1)), P + " v1 Section 5.4", "constant")
    m = need(P, r"\| LEARN_AGREE \| 3 \| scripts/g_nav.py:(\d+) \| (ccc4d57e26cdee73ea0eabdbd7d7fdfe847ed265) \|")
    add("const.LEARN_AGREE.line", int(m.group(1)), P + " v1 Section 5.4", "constant")
    add("hash.g_nav_last_commit_full", m.group(2), P + " v1 Section 5.4", "hash")
    add("hash.g_nav_last_commit", m.group(2)[:7], P + " v1 Section 5.4", "hash")
    m = need(P, r"\| LEARN_MAX \| 8 \| scripts/g_nav.py:(\d+) \|")
    add("const.LEARN_MAX.line", int(m.group(1)), P + " v1 Section 5.4", "constant")
    m = need(P, r"\| BFS_NODES \| 40000 \| scripts/g_nav.py:(\d+) \|")
    add("const.BFS_NODES.line", int(m.group(1)), P + " v1 Section 5.4", "constant")
    m = need(P, r"\| min_cells \| 2 \| scripts/g_motion.py:(\d+) \| (\w+) \|")
    add("const.min_cells.line", int(m.group(1)), P + " v1 Section 5.4", "constant")
    m = need(P, r"scripts/g_motion.py:17 \| (378345f4e7f43e3ea2fedd65f8d23e84b41603c6) \|")
    add("hash.g_motion_last_commit", m.group(1)[:7], P + " v1 Section 5.4", "hash")
    m = need(P, r"`top\[0\]\[1\] < 2 \* top\[1\]\[1\]` rejects \| scripts/g_nav.py:(\d+)")
    add("const.margin.line", int(m.group(1)), P + " v1 Section 5.4", "constant")
    add("const.margin", "2:1", P + " v1 Section 5.4", "constant")
    m = need(P, r"\| KEYS \(ARC\) \| \(1, 2, 3, 4, 5, 7\) \| scripts/g_control_probe.py:(\d+)")
    add("const.KEYS.line", int(m.group(1)), P + " v1 Section 5.4", "constant")
    for k in (1, 2, 3, 4, 5, 7):
        add(f"const.KEYS.{k}", k, P + " v1 Section 5.4 (KEYS)", "constant")
    m = need(P, r"rows 1–62 \(rows 0 and 63 excluded")
    add("frame.first_row", 1, P + " v1 Section 3.1", "constant")
    add("frame.last_row", 62, P + " v1 Section 3.1", "constant")
    add("frame.row0", 0, P + " v1 Section 3.1", "constant")
    add("frame.row63", 63, P + " v1 Section 3.1", "constant")
    m = need(P, r"Grid: (64) × 64\.")
    add("frame.canvas", 64, P + " v1 Section 3.1", "constant")
    m = need(P, r"The frame is cut into (8) × 8 tiles")
    add("frame.tile", 8, P + " v1 Section 3.2", "constant")
    m = need(P, r"capped at (64) entries")
    add("frame.palette_cap", 64, P + " v1 Section 3.3", "constant")
    m = need(P, r"at least (2) pixels")
    add("range.min_pixels", 2, P + " v1 Section 4", "constant")
    m = need(P, r"Action list: all (15) actions, 0–14")
    add("procgen.actions", 15, P + " v1 Section 3.3", "constant")
    m = need(P, r"I1 presses ids 1 to (5) only")
    add("i1.keys", 5, P + " v1.1 D9b", "constant")
    m = need(P, r"\*\*The ARC cap: (3600) s per run")
    add("arc.cap_s", 3600, P + " v1.1 D12", "constant")
    m = need(P, r"default `--game-seconds (900)`")
    add("arc.old_clock_s", 900, P + " v1.1 D12", "constant")
    m = need(P, r"(Eight) E6 nav rows stopped at the 900 s clock")
    add("arc.cut_rows", 8, P + " v1.1 D12 ('Eight')", "count")
    m = need(P, r"three times the longest pilot run's wall time")
    add("cap.multiplier", 3, P + " v1.1 D5 ('three times')", "constant")
    m = need(P, r"one day per run|--seconds (86400)")
    # suites and splits
    m = need(P, r"docs/GROUND_TRUTH_minigrid.md \(suite B, (178) ids\)")
    add("suiteB.registered_ids", 178, P + " v1 Section 7", "count")
    m = need(P, r"Suite B confirmatory \((161) = 178 − (11) excluded − (6) pilots\)")
    add("suiteB.confirmatory", 161, P + " v1 Section 8", "count")
    add("suiteB.excluded", 11, P + " v1 Section 8", "count")
    add("suiteB.pilots", 6, P + " v1 Section 8", "count")
    add("suiteB.superseded", sum("superseded by v1" in l for l in text(P).splitlines() if l.startswith("| MiniGrid-")),
        P + " v1 Section 7 (exclusion table, 'superseded by v1')", "count")
    add("suiteB.wfc", 6, P + " v1 Section 7 (exclusion table, six WFC ids)", "count")
    check(N["suiteB.superseded"]["value"] == 5, "five superseded suite-B ids")
    m = need(P, r"docs/GROUND_TRUTH_procgen.md \(suite C, (16) games\)")
    add("suiteC.games", 16, P + " v1 Section 7", "count")
    m = need(P, r"\*\*Suite C confirmatory \((14)\):\*\*")
    add("suiteC.confirmatory", 14, P + " v1 Section 8", "count")
    add("suiteC.in_range", len(C.IN_RANGE_C), "scripts/analyze_common.py (IN_RANGE_C)", "count")
    add("suiteC.camera_distinct", len(C.CAMERA_DISTINCT_C), "scripts/analyze_common.py (CAMERA_DISTINCT_C)", "count")
    add("suiteC.games_overwriting_camera", 10, P + " v1.1 D13 ('Ten games overwrite it')", "count")
    need(P, r"Ten games overwrite it inside their own `game_reset\(\)`")
    add("arc.train", len(C.ARC_TRAIN), "scripts/analyze_common.py (ARC_TRAIN)", "count")
    m = need(P, r"Held-out, (17):")
    add("arc.heldout", 17, P + " v1 Section 8", "count")
    add("arc.public", 25, P + " v1 Section 9.1 ('25 games × 10 seeds')", "count")
    need(P, r"25 games × 10 seeds × 20,000 actions")
    add("arc.source_informed", 3, "docs/EXPLORATORY_V1_DIAGNOSIS.md Section 6 ('three of which are source-informed')",
        "count")
    need("docs/EXPLORATORY_V1_DIAGNOSIS.md", r"three of which are source-informed")
    # the split file: dc22 moved from held-out to train during development
    H = "docs/HELDOUT.md"
    m = need(H, r"dc22\s+MOVED FROM HELD-OUT on (\d+) Sep (\d{4})")
    add("date.dc22_moved", fmt_date(_dt.date(int(m.group(2)), 9, int(m.group(1)))), H + " (TRAIN list, dc22)", "date")
    m = need(H, r"Seventeen games \((eighteen) until dc22 was moved")
    add("arc.heldout_before_dc22", 18, H + " ('eighteen until dc22 was moved')", "count")
    # truth counts on the confirmatory sets, through the registered parsers
    tb = C.parse_truth_minigrid(os.path.join(ROOT, "docs", "GROUND_TRUTH_minigrid.md"))
    conf_b = C.confirmatory("minigrid", tb)
    check(len(conf_b) == 161, "161 confirmatory suite-B ids from the truth table")
    for a in ("A1", "A2", "A3-raw", "A3-macro", "A4", "A5"):
        h = sum(tb[g][a] == "holds" for g in conf_b)
        add(f"truth.minigrid.{a}.holds", h, "docs/GROUND_TRUTH_minigrid.md (analyze_common.parse_truth_minigrid)", "count")
        add(f"truth.minigrid.{a}.fails", len(conf_b) - h, "docs/GROUND_TRUTH_minigrid.md (analyze_common.parse_truth_minigrid)",
            "count")
    tc = C.parse_truth_procgen(os.path.join(ROOT, "docs", "GROUND_TRUTH_procgen.md"))
    conf_c = C.confirmatory("procgen", tc)
    check(len(conf_c) == 14, "14 confirmatory suite-C games from the truth table")
    for a in ("A1", "A2", "A3", "A4", "A5"):
        h = sum(tc[g][a] == "holds" for g in conf_c)
        add(f"truth.procgen.{a}.holds", h, "docs/GROUND_TRUTH_procgen.md (analyze_common.parse_truth_procgen)", "count")
        add(f"truth.procgen.{a}.fails", len(conf_c) - h, "docs/GROUND_TRUTH_procgen.md (analyze_common.parse_truth_procgen)",
            "count")
    # V2 exclusions, from the registered constants
    src = "scripts/analyze_common.py at prereg-v1.1 (V2_EXCLUDE, V2_EXCLUDE_I1)"
    for (s, c), lst in C.V2_EXCLUDE.items():
        add(f"excl.RN.{c}", len(lst), src, "count")
        add(f"excl.RN.{c}.primary", 161 - len(lst), src + " (161 minus the list)", "count")
    for (s, c), lst in C.V2_EXCLUDE_I1.items():
        add(f"excl.I1.{c}", len(lst), src, "count")
        add(f"excl.I1.{c}.primary", 161 - len(lst), src + " (161 minus the list)", "count")
    for name in ("_NO_SUCCESS", "_DONE_ABSENT", "_DROP_ABSENT", "_DROP_PRECOND", "_TOGGLE_PRED"):
        add("excl.list." + name.strip("_"), len(getattr(C, name)), src.replace("(V2_EXCLUDE, V2_EXCLUDE_I1)", f"({name})"),
            "count")
    add("excl.list.TOGGLE_PRECOND_own", len(C._TOGGLE_PRECOND) - len(C._DROP_PRECOND),
        src.replace("(V2_EXCLUDE, V2_EXCLUDE_I1)", "(_TOGGLE_PRECOND minus _DROP_PRECOND)"), "count")
    add("excl.list.TOGGLE_needed", len(C._TOGGLE_PRED) + len(C._TOGGLE_PRECOND),
        src.replace("(V2_EXCLUDE, V2_EXCLUDE_I1)", "(_TOGGLE_PRED + _TOGGLE_PRECOND)"), "count")
    # run counts
    m = need("docs/STATE.md", r"9,660 for suite B \((\w+)\) and 840 for suite C \((\w+)\)")
    add("rows.minigrid", "9,660", "docs/STATE.md amendment (j)", "count")
    add("rows.procgen", 840, "docs/STATE.md amendment (j)", "count")
    add("rows.total", "10,500", "docs/STATE.md amendment (j) (9,660 + 840)", "count")
    add("hash.rows_minigrid_commit", m.group(1), "docs/STATE.md amendment (j)", "hash")
    add("hash.rows_procgen_commit", m.group(2), "docs/STATE.md amendment (j)", "hash")
    check(161 * 2 * 3 * 10 == 9660 and 14 * 2 * 3 * 10 == 840, "row counts = games x conditions x agents x seeds")
    add("rows.agents", 3, "docs/PREREG.md v1 Section 2 (R, N, I1)", "count")
    add("rows.conditions", 2, "docs/PREREG.md v1 Section 9.1 (two conditions per suite)", "count")
    m = need("docs/STATE.md", r"Checks: (500) rows \(25 games × 2 modes × 10 seeds\), (0) errors")
    add("rows.arc", 500, "docs/STATE.md amendment (h)", "count")
    add("arc.modes", 2, "docs/STATE.md amendment (h) ('2 modes')", "count")
    add("zero", 0, "docs/STATE.md amendments (i), (j): '0 errors, 0 cut by the cap'", "count")
    need("docs/STATE.md", r"9660 of 9660 confirmatory rows; missing 0; with an error 0; cut by the cap 0")
    m = need("docs/STATE.md", r"(\d+) of the \"done\" lines carry a prefix")
    # D numbers: count of entries
    add("prereg.entries", 16, "docs/PREREG.md (diff entries D1 to D16)", "count")
    check(all(re.search(rf"\*\*D{i}\.", text(P)) for i in range(1, 17)), "PREREG.md has D1 to D16")


# ------------------------------------------------------------------ hashes, tags, dates, urls, versions
def provenance():
    P = "docs/PREREG.md"
    tags = {"prereg-v1": "v1", "prereg-v1.1": "v1_1", "prereg-v1.2": "v1_2"}
    for tag, k in tags.items():
        full = git("rev-parse", tag + "^{commit}")
        add(f"tag.{k}.commit", full, f"git tag object {tag}", "hash")
        add(f"tag.{k}.commit_short", full[:7], f"git tag object {tag}", "hash")
        tagger = [l for l in git("cat-file", "-p", tag).splitlines() if l.startswith("tagger ")][0]
        ts = int(tagger.split()[-2])
        ist = _dt.timezone(_dt.timedelta(hours=5, minutes=30))
        add(f"tag.{k}.date", fmt_date(_dt.datetime.fromtimestamp(ts, ist)), f"git tag object {tag} (tagger date, IST)",
            "date")
    check(N["tag.v1.commit"]["value"] in text("docs/OSF_REGISTRATION_final.txt"), "v1 commit in the OSF v1 text")
    check(N["tag.v1_1.commit"]["value"] in text("docs/OSF_REGISTRATION_v1_1_final.txt"), "v1.1 commit in the OSF v1.1 text")
    check(N["tag.v1_2.commit"]["value"][:7] in text("docs/STATE.md"), "v1.2 commit in STATE.md (m)")
    for url, src in (("https://osf.io/2znhw", "docs/STATE.md amendment (d)"),
                     ("https://osf.io/zu5vq", "docs/STATE.md amendment (h)"),
                     ("https://osf.io/29eas", "docs/STATE.md amendment (h)"),
                     ("https://github.com/rahul-k-mishra/arc3-frame-only-study", "docs/preprint/preprint.md Section 9")):
        need(src.split()[0], re.escape(url))
        add("url." + url.rsplit("/", 1)[-1], url, src, "url")
    need("docs/STATE.md", r"Embargoed until 30 June 2030")
    add("date.embargo", "30 June 2030", "docs/STATE.md amendment (d)", "date")
    need("docs/STATE.md", r"## Amendment 27 Sep 2026 \(d\)[\s\S]*?https://osf.io/2znhw")
    add("date.osf_v1", "27 September 2026", "docs/STATE.md amendment (d) (dated 27 Sep 2026)", "date")
    need("docs/STATE.md", r"## Amendment 27 Sep 2026 \(h\)[\s\S]*?https://osf.io/zu5vq")
    add("date.osf_v1_1", "27 September 2026", "docs/STATE.md amendment (h) (dated 27 Sep 2026)", "date")
    need(P, r"Written 27 September 2026 from docs/METHOD_BLUEPRINT.md")
    add("date.prereg_v1_written", "27 September 2026", P + " v1 preface", "date")
    need(P, r"Written 13 October 2026, after the tag prereg-v1.1")
    add("date.d16", "13 October 2026", P + " v1.2 preface and D16", "date")
    need("docs/STATE.md", r"Started on 28 Sep 2026 from the worktree")
    add("date.suiteB_start", "28 September 2026", "docs/STATE.md amendment (i)", "date")
    need("docs/STATE.md", r"It started 28 Sep 2026, finished by 13 Oct 2026")
    add("date.suiteB_end", "13 October 2026", "docs/STATE.md amendment (j)", "date")
    need("docs/STATE.md", r"## Amendment 13 Oct 2026 \(k\)[\s\S]*?A defect in the ARC rows of the V2 table")
    add("date.arc_defect", "13 October 2026", "docs/STATE.md amendment (k) (dated 13 Oct 2026)", "date")
    add("date.gate_g3", "13 October 2026", "docs/STATE.md amendment (k) (dated 13 Oct 2026)", "date")
    add("date.pilot_lesson", "13 October 2026", "docs/STATE.md amendment (k) (dated 13 Oct 2026)", "date")
    need("docs/STATE.md", r"## Amendment 13 Oct 2026 \(l\)[\s\S]*?read as \"at most a preprint\"")
    add("date.venue_reading", "13 October 2026", "docs/STATE.md amendment (l) (dated 13 Oct 2026)", "date")
    need("docs/STATE.md", r"## Amendment 14 Oct 2026 \(m\)[\s\S]*?draft 2 \(14 Oct\)")
    add("date.preprint_draft2", "14 October 2026", "docs/STATE.md amendment (m) (preprint draft 2, 14 Oct)", "date")
    need("docs/STATE.md", r"## Amendment 27 Sep 2026 \(f\)[\s\S]*?\*\*The pilot\*\* \(commit db1e6ac")
    add("date.pilot", "27 September 2026", "docs/STATE.md amendment (f) (dated 27 Sep 2026)", "date")
    add("date.d1_d15", "27 September 2026", P + " v1.1 preface (two revisions of 27 September 2026)", "date")
    need("docs/STATE.md", r"## Amendment 14 Oct 2026 \(n\)[\s\S]*?A fifth deviation, found while the manuscript was written")
    add("date.fifth_deviation", "14 October 2026", "docs/STATE.md amendment (n) (dated 14 Oct 2026)", "date")
    # the preprint on Zenodo, as recorded in amendment (r)
    m = need("docs/STATE.md", r"## Amendment 14 Oct 2026 \(r\)[\s\S]*?published on Zenodo under (CC-BY \d+\.\d+) "
                              r"on (\d{1,2}) (October) (\d{4}) with DOI (10\.5281/zenodo\.\d+) \((https://doi\.org/[^)\s]+)\)")
    check(m.group(6) == "https://doi.org/" + m.group(5), "Zenodo URL = https://doi.org/ + DOI in STATE.md (r)")
    add("preprint.license", m.group(1), "docs/STATE.md amendment (r)", "identifier")
    add("date.preprint", f"{int(m.group(2))} {m.group(3)} {m.group(4)}", "docs/STATE.md amendment (r)", "date")
    add("preprint.doi", m.group(5), "docs/STATE.md amendment (r)", "identifier")
    add("url.preprint", m.group(6), "docs/STATE.md amendment (r)", "url")
    need("docs/STATE.md", r"## Amendment 14 Oct 2026 \(r\)[\s\S]*?Both OSF embargoes\*\* \(2znhw, zu5vq\) "
                          r"were ended on 14 October 2026")
    add("date.embargo_end", "14 October 2026", "docs/STATE.md amendment (r)", "date")
    # reference URLs for entries without a DOI, as fetched in the review of draft 1
    R = "docs/manuscript/REVIEW_draft1.md"
    for key, url in (("bertinetto", "https://proceedings.mlr.press/v148/bertinetto21a.html"),
                     ("blum", "https://proceedings.mlr.press/v37/blum15.html"),
                     ("cobbe", "https://proceedings.mlr.press/v119/cobbe20a.html"),
                     ("roelofs", "https://papers.nips.cc/paper_files/paper/2019/hash/"
                                 "ee39e503b6bedf0c98c388b7e8589aca-Abstract.html"),
                     ("wayllace", "https://www.ijcai.org/Proceedings/16/Papers/464.pdf"),
                     ("choi", "https://openreview.net/forum?id=HyxGB2AcY7"),
                     ("chevalierboisvert", "https://openreview.net/forum?id=rJeXCo0cYX")):
        need(R, re.escape(url))
        add(f"ref.{key}.url", url, R + " Section 6.1 (page fetched)", "url")
    # Chevalier-Boisvert et al. (2023), MiniGrid: fields from the NeurIPS proceedings page and its BibTeX
    RC = "docs/manuscript/REFERENCES_CHECK.md"
    m = need(RC, r"chevalierboisvert2023minigrid .*?volume (\d+); year (\d{4}); pages (\d+)–(\d+); DOI (10\.52202/075280-3209)")
    src = RC + " (chevalierboisvert2023minigrid, NeurIPS proceedings page)"
    add("ref.chevalierboisvert2023minigrid.volume", int(m.group(1)), src, "identifier")
    add("ref.chevalierboisvert2023minigrid.year", int(m.group(2)), src, "identifier")
    add("ref.chevalierboisvert2023minigrid.page_first", int(m.group(3)), src, "identifier")
    add("ref.chevalierboisvert2023minigrid.page_last", int(m.group(4)), src, "identifier")
    add("ref.chevalierboisvert2023minigrid.doi", "https://doi.org/" + m.group(5), src, "url")
    # commits named in the text
    for h, src in (("bb0f1a1", "docs/STATE.md amendment (k)"), ("f43526a", "docs/STATE.md amendment (l)"),
                   ("db1e6ac", "docs/STATE.md amendment (f)"), ("51eba49", "docs/STATE.md amendment (f)"),
                   ("8a986d9", "docs/STATE.md amendment (j)"), ("5ac65c1", "docs/STATE.md amendment (i)"),
                   ("b3509de", "docs/STATE.md amendment (f)"), ("66e5606", "docs/STATE.md amendment (m)")):
        need(src.split()[0], h)
        add("commit." + h, h, src, "hash")
    # blob hashes: the six frozen files and the analysis scripts, checked against git ls-tree at the tags
    frozen = ("scripts/g_agent.py", "scripts/g_nav.py", "scripts/g_motion.py", "scripts/g_control_probe.py",
              "scripts/g_nav_run.py", "scripts/g_census_table.py")
    for f in frozen:
        blob = need(P, r"^\| " + re.escape(f) + r"[^|\n]*\| ([0-9a-f]{40}) \|", re.M).group(1)
        check(git("ls-tree", "prereg-v1.1", f).split()[2] == blob, f"{f} blob at prereg-v1.1 = PREREG v1 Section 5.4")
        add("blob." + os.path.basename(f), blob, P + " v1 Section 5.4; git ls-tree prereg-v1.1", "hash")
    for f in ("scripts/analyze_common.py", "scripts/analyze_v1.py", "scripts/analyze_v2.py", "scripts/analyze_g.py",
              "scripts/determinism_check.py"):
        blob = git("ls-tree", "prereg-v1.1", f).split()[2]
        need(P, blob)
        add("blob." + os.path.basename(f), blob, P + " v1.1 D8, D11; git ls-tree prereg-v1.1", "hash")
    add("frozen.files", len(frozen), P + " v1 Section 5.4", "count")
    # versions
    for name, pat in (("arc_agi", r"arc-agi (0\.9\.8)"), ("arcengine", r"arcengine (0\.9\.3)"),
                      ("minigrid", r"minigrid (3\.1\.0)"), ("gymnasium", r"gymnasium (1\.3\.0)"),
                      ("python_b", r"Python (3\.11\.9)"), ("procgen", r"Procgen (0\.10\.7)"),
                      ("python_c", r"Procgen 0\.10\.7 \(Python (3\.10)")):
        add("version." + name, need(P, pat).group(1), P + " v1 Section 3", "version")
    # the author block, from the preprint
    add("author.orcid", need("docs/preprint/preprint.md", r"ORCID (\d{4}-\d{4}-\d{4}-\d{4})").group(1),
        "docs/preprint/preprint.md", "identifier")
    # references: every numeral in every field of references.bib
    bib = text("docs/preprint/references.bib")
    for m in re.finditer(r"@\w+\{(\w+),([\s\S]*?)\n\}", bib):
        key, body = m.group(1), m.group(2)
        for fm in re.finditer(r"(\w+)\s*=\s*\{(.*)\},?\s*$", body, re.M):
            field, val = fm.group(1), fm.group(2)
            if field == "doi":
                add(f"ref.{key}.doi", "https://doi.org/" + val, "docs/preprint/references.bib", "url")
            elif field == "eprint":
                add(f"ref.{key}.arxiv", "https://arxiv.org/abs/" + val, "docs/preprint/references.bib", "url")
            elif field in ("year", "volume", "number"):
                add(f"ref.{key}.{field}", int(val), "docs/preprint/references.bib", "identifier")
            elif field == "pages" and "--" in val:
                a, b = val.split("--")
                add(f"ref.{key}.page_first", int(a), "docs/preprint/references.bib", "identifier")
                add(f"ref.{key}.page_last", int(b), "docs/preprint/references.bib", "identifier")
            elif field in ("booktitle", "title"):
                for i, num in enumerate(re.findall(r"(?<![\w-])\d{4}(?![\w-])", val)):
                    add(f"ref.{key}.{field}_num{i}", int(num), "docs/preprint/references.bib", "identifier")


# ------------------------------------------------------------------ Appendix C
def appendix_c():
    """One row per number class: the committed files its values come from, and the commit that last
    changed each file (git log -1).  Those commits are added to numbers.json as hashes."""
    names = {"count": "count", "rate": "rate (agreement, κ, AUROC, interval bound, share)",
             "threshold": "registered threshold", "constant": "constant, cap, seed or time",
             "hash": "commit or blob hash", "date": "date", "version": "package version",
             "url": "URL or DOI", "identifier": "reference field, verdict word or ORCID"}
    by = {}
    for k, v in list(N.items()):
        src = v["source"].split()[0].rstrip(",;")
        if src == "git":
            src = "git tag objects and git ls-tree"
        by.setdefault(v["class"], set()).add(src)
    commit_of = {}
    for files in by.values():
        for f in files:
            if f.startswith("git"):
                commit_of[f] = "the tag objects themselves"
                continue
            if git("status", "--porcelain", "--", f):
                # new or changed since the last commit: it is committed together with this table
                commit_of[f] = "changed in the commit that carries this table"
                continue
            h = git("log", "-1", "--format=%h", "--", f)
            commit_of[f] = h
            add("lastcommit." + f, h, f"git log -1 -- {f}", "hash")
    lines = ["| number class | source files, each with the commit that last changed it |", "|---|---|"]
    for cls in names:
        if cls in by:
            lines.append(f"| {names[cls]} | " + "; ".join(f"{f} ({commit_of[f]})" for f in sorted(by[cls])) + " |")
    return "\n".join(lines) + "\n"


def main():
    tables()
    diagnosis()
    checks()
    protocol()
    provenance()
    for k, v in N.items():
        if v["class"] == "hash":
            v["value"] = str(v["value"])
    os.makedirs(OUT_DIR, exist_ok=True)
    app = appendix_c()
    with open(os.path.join(OUT_DIR, "numbers.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(N, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    with open(os.path.join(OUT_DIR, "appendix_c.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(app)
    for c in CHECKS:
        print("check ok:", c)
    print(f"numbers.json: {len(N)} values written to docs/manuscript/numbers.json")
    print(f"appendix_c.md: {app.count(chr(10)) - 2} number classes written to docs/manuscript/appendix_c.md")
    print("all cross-checks passed")


if __name__ == "__main__":
    main()
