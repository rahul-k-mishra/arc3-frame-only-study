"""
Synthetic test of scripts/analyze_v1.py (docs/PREREG.md v1, Section 11).  Reads no runs/ file and
plays no game: it writes a tiny truth table and a tiny run file into a temporary folder.

Suite "procgen", condition "center_off".  Games: alpha bravo charlie delta echo maze (status
confirmatory), coinrun (a registered pilot: must be ignored), gamma (excluded: must be ignored).
maze is the only game in the registered in-range list.

Truth (holds h / fails f), games in the order alpha bravo charlie delta echo maze:
    A1  h h h h h h        A2  h h h h f f        A3  f f f f f f
    A4  h h h f f f        A5  h h h f f f
N-row census per seed, and the seed majority (holds if >= half hold; else fails if >= half fail;
else undetermined):
    A2: alpha [h,h]=h  bravo [h,f,h]=h  charlie [h]=h  delta [f,f]=f  echo [f]=f  maze [h]=h
    A4: alpha [h,h]=h  bravo [h,h,f]=h  charlie [h,f,f]=f  delta [f]=f  echo [f]=f  maze [h]=h
    A5: alpha [h,h]=h  bravo [u,u,h]=u  charlie [h]=h  delta [f]=f  echo [f]=f  maze [h,f]=h (tie -> h)
    A1 = h and A3 = f everywhere.
Hand computation, subset "all" (n = 6):
    A1: agreement 6/6 = 1.0; kappa undefined (fails has 0 < 3 games); verdict PASS.
    A2: agree on alpha bravo charlie echo = 4/6 = 0.6667; kappa undefined (fails has 2 < 3); FAIL (< 0.75).
    A3: agreement 1.0; kappa undefined (holds has 0); PASS.
    A4: agree on alpha bravo delta echo = 4/6 = 0.6667.  2x2: TT-h 2 (alpha, bravo), truth h / pred f 1
        (charlie), TT-f 2 (delta, echo), truth f / pred h 1 (maze).  po = 4/6; p_truth_h = 3/6 = .5;
        p_pred_h = 3/6 = .5; pe = .5*.5 + .5*.5 = .5; kappa = (0.6667 - .5)/(1 - .5) = 0.3333.  FAIL.
    A5: agree on alpha charlie delta echo = 4/6 = 0.6667 (bravo "undetermined" never agrees).  For kappa
        bravo's undetermined maps to the value opposite its truth (h -> f): pred h f h f f h; po = 4/6;
        p_pred_h = 3/6; pe = .5; kappa = 0.3333.  FAIL.
Subset "in_range" (maze only, n = 1): A2 truth f, census h -> agreement 0.0, kappa undefined, FAIL;
A1 agreement 1.0 PASS.

Command (PowerShell, from D:\\Research\\arc3\\repo):
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\test_analyze_v1.py
Expected: "Ran 4 tests ... OK".
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest


def _write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze_common as C  # noqa: E402
import analyze_v1  # noqa: E402

GAMES = ["alpha", "bravo", "charlie", "delta", "echo", "maze"]
TRUTH = {"A1": "hhhhhh", "A2": "hhhhff", "A3": "ffffff", "A4": "hhhfff", "A5": "hhhfff"}
W = {"h": "holds", "f": "fails", "u": "undetermined"}
CENSUS = {  # per game: list of per-seed dicts
    "alpha": [dict(A2="h", A4="h", A5="h"), dict(A2="h", A4="h", A5="h")],
    "bravo": [dict(A2="h", A4="h", A5="u"), dict(A2="f", A4="h", A5="u"), dict(A2="h", A4="f", A5="h")],
    "charlie": [dict(A2="h", A4="h", A5="h"), dict(A2="h", A4="f", A5="h"), dict(A2="h", A4="f", A5="h")],
    "delta": [dict(A2="f", A4="f", A5="f"), dict(A2="f", A4="f", A5="f")],
    "echo": [dict(A2="f", A4="f", A5="f")],
    "maze": [dict(A2="h", A4="h", A5="h"), dict(A2="h", A4="h", A5="f")],
    "coinrun": [dict(A2="h", A4="h", A5="h")] * 3,
    "gamma": [dict(A2="h", A4="h", A5="h")] * 3,
}


def procgen_table(path, games_status):
    lines = ["| game | A1 | A2 | A3 | A4 | A5 | predicate | actions | notes | status |", "|---|---|---|---|---|---|---|---|---|---|"]
    for g, status, t in games_status:
        lines.append(f"| {g} | {W[t['A1']]} | **{W[t['A2']]}** | {W[t['A3']]} | {W[t['A4']]} | **{W[t['A5']]} (x)** | p | a | n | {status} |")
    _write(path, "\n".join(lines) + "\n")


def build(tmp):
    gs = []
    for i, g in enumerate(GAMES):
        gs.append((g, "confirmatory", {a: TRUTH[a][i] for a in TRUTH}))
    gs.append(("coinrun", "pilot candidate", {a: "f" for a in TRUTH}))
    gs.append(("gamma", "excluded: test", {a: "f" for a in TRUTH}))
    procgen_table(os.path.join(tmp, "gt_procgen.md"), gs)
    _write(os.path.join(tmp, "gt_minigrid.md"), "\n")
    rows = []
    for g, seeds in CENSUS.items():
        for k, c in enumerate(seeds):
            census = {"A1": "holds", "A3": "fails", "A2": W[c["A2"]], "A4": W[c["A4"]], "A5": W[c["A5"]]}
            rows.append(dict(game=g, mode="nav", agent="N", suite="procgen", condition="center_off", seed=1000 + k,
                             census=census))
    _write(os.path.join(tmp, "runs.json"), json.dumps(rows))


class T(unittest.TestCase):
    def test_majority(self):
        self.assertEqual(C.majority(["holds", "fails"]), "holds")
        self.assertEqual(C.majority(["undetermined", "undetermined", "holds"]), "undetermined")
        self.assertEqual(C.majority(["fails", "fails", "holds"]), "fails")

    def test_census_from_report(self):
        """Hand check of the registered per-seed census (PREREG.md Section 5.3).
        Report 1: keys 1 and 2 learned shifts (0,-6) and (0,6), key 1 accepted, avatar_found 1, level-1
        fallback "stalled", walls [3], wall_contradicted 0, goal_confirmed 1:
            A1 holds (shifts not all equal), A2 holds, A3 holds (stalled is not a model failure),
            A4 holds (one wall, no contradiction), A5 holds (goal_confirmed 1).
        Report 2: one key with shift None, decided no_move, avatar_found 0, goal_reached_no_end 2:
            A1 fails (no shift), A2 fails, A3 fails, A4 fails, A5 fails (reached without end, never confirmed).
        Report 3 = report 1 with fallback "mispredicted", walls [] and no goal counters:
            A1 holds, A2 holds, A3 fails, A4 fails, A5 undetermined.
        ARC row (mode nav, levels 2, nav = report 1): normalised to suite arc, condition native,
        agent N, level1_completed True, census as report 1."""
        r1 = dict(learn={"1": dict(shift=[0, -6], decided="accepted"), "2": dict(shift=[0, 6], decided="-")},
                  counters=dict(avatar_found=1, wall_contradicted=0, goal_confirmed=1),
                  levels=[dict(fallback="stalled")], walls=[3])
        r2 = dict(learn={"1": dict(shift=None, decided="no_move")}, counters=dict(avatar_found=0, goal_reached_no_end=2),
                  levels=[dict(fallback="no_avatar")], walls=[])
        r3 = dict(r1, levels=[dict(fallback="mispredicted")], walls=[], counters=dict(avatar_found=1))
        h, f, u = "holds", "fails", "undetermined"
        self.assertEqual(C.census_from_report(r1), dict(A1=h, A2=h, A3=h, A4=h, A5=h))
        self.assertEqual(C.census_from_report(r2), dict(A1=f, A2=f, A3=f, A4=f, A5=f))
        self.assertEqual(C.census_from_report(r3), dict(A1=h, A2=h, A3=f, A4=f, A5=u))
        n = C.normalise(dict(game="tu93", mode="nav", seed=1000, levels=2, nav=r1))
        self.assertEqual((n["suite"], n["condition"], n["agent"], n["level1_completed"]), ("arc", "native", "N", True))
        self.assertEqual(n["census"], dict(A1=h, A2=h, A3=h, A4=h, A5=h))

    def test_kappa(self):
        a, k = C.agreement_kappa(["holds"] * 3 + ["fails"] * 3, ["holds", "holds", "fails", "fails", "fails", "holds"])
        self.assertAlmostEqual(a, 4 / 6)
        self.assertAlmostEqual(k, 1 / 3)

    def test_v1(self):
        with tempfile.TemporaryDirectory() as tmp:
            build(tmp)
            table = analyze_v1.main(["--runs", os.path.join(tmp, "runs.json"), "--truth-procgen",
                                     os.path.join(tmp, "gt_procgen.md"), "--truth-minigrid",
                                     os.path.join(tmp, "gt_minigrid.md"), "--out", tmp])
            got = {(r[2], r[3]): r for r in table}
            exp = {("all", "A1"): (6, 1.0, None, "PASS"), ("all", "A2"): (6, 4 / 6, None, "FAIL"),
                   ("all", "A3"): (6, 1.0, None, "PASS"), ("all", "A4"): (6, 4 / 6, 1 / 3, "FAIL"),
                   ("all", "A5"): (6, 4 / 6, 1 / 3, "FAIL"), ("in_range", "A2"): (1, 0.0, None, "FAIL"),
                   ("in_range", "A1"): (1, 1.0, None, "PASS")}
            for key, (n, agree, kappa, verdict) in exp.items():
                r = got[key]
                self.assertEqual(r[4], n, key)
                self.assertAlmostEqual(r[6], agree, msg=str(key))
                if kappa is None:
                    self.assertIsNone(r[7], key)
                else:
                    self.assertAlmostEqual(r[7], kappa, msg=str(key))
                self.assertEqual(r[8], verdict, key)
            self.assertTrue(os.path.exists(os.path.join(tmp, "v1.md")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
