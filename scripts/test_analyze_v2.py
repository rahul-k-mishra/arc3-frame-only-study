"""
Synthetic test of scripts/analyze_v2.py (docs/PREREG.md v1, Section 11).  Reads no runs/ file and
plays no game.

Suite "procgen", condition "center_off", 8 confirmatory games in the order
alpha bravo charlie delta echo maze golf hotel (maze is the only in-range game).
Census (N rows, one seed each), S = number of A1-A5 holding, P = A2 and A3 and A4 and A5 hold:
    alpha   h h h h h  S=5 P=1        bravo   h h h h h  S=5 P=1
    charlie h h h h f  S=4 P=0        delta   h h h f h  S=4 P=0
    echo    h h h f u  S=3 P=0        maze    h h f f f  S=2 P=0
    golf    h f f f f  S=1 P=0        hotel   h f f f f  S=1 P=0
Agent R, level-1 completion per seed, and Y = completed in at least half the seeds:
    alpha [T,T] 1   bravo [T,F] 1 (2*1 >= 2)   charlie [T,T,F] 1 (2*2 >= 3)   delta [F,F,T] 0 (2*1 < 3)
    echo [T] 1      maze [F] 0                 golf [F,F] 0                    hotel [F] 0
Precondition: 4 of 8 positive = 0.5, inside [0.10, 0.90], so not void.
AUROC(S -> Y): positives S = 5,5,4,3; negatives S = 4,2,1,1.  Pair credit: each 5 beats all four
negatives (4 each, 8 total); the 4 ties the negative 4 (0.5) and beats 2,1,1 (3.5); the 3 beats 2,1,1
(3).  Total 14.5 of 16 pairs: AUROC = 0.90625.
Balanced accuracy of P: TP 2 (alpha, bravo), FN 2 (charlie, echo), TN 4, FP 0; TPR .5, TNR 1.0;
BA = 0.75.
Test 1, constant nuisance features (grid 64x64, 15 actions, 10 colours on every game): no feature
varies, B predicts the base rate for every game, AUROC_B = 0.5.  Verdict: AUROC >= 0.80 but BA < 0.80,
so not PASS; AUROC > 0.65, so not FAIL: "neither".  Agent N (same outcomes) has role
"instrument check".  I1 is absent, so the suite line says "not failed (I1 absent ...)".
In-range subset: maze only, 0 of 1 positive, share 0 < 0.10: VOID.
Test 2, grid area varies: grid [x, 1] with x = 8 7 6 5 4 3 2 1 in the game order.  B is a one-feature
logistic regression, increasing in x (x and Y are positively associated), so AUROC_B = AUROC(x):
positives x = 8,7,6,4, negatives x = 5,3,2,1; 8, 7, 6 beat all four (12), 4 beats 3,2,1 (3): 15/16 =
0.9375.
Test 3, every game completed: share 1.0 > 0.90: VOID.
Test 4, the bootstrap is deterministic for a fixed seed and 0 <= low <= high <= 1.

Command (PowerShell, from D:\\Research\\arc3\\repo):
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\test_analyze_v2.py
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
import analyze_v2  # noqa: E402

GAMES = ["alpha", "bravo", "charlie", "delta", "echo", "maze", "golf", "hotel"]
CENSUS = ["hhhhh", "hhhhh", "hhhhf", "hhhfh", "hhhfu", "hhfff", "hffff", "hffff"]
DONE = [[1, 1], [1, 0], [1, 1, 0], [0, 0, 1], [1], [0], [0, 0], [0]]
W = {"h": "holds", "f": "fails", "u": "undetermined"}


def build(tmp, grids=None, done=None):
    lines = ["| game | A1 | A2 | A3 | A4 | A5 | p | a | n | status |", "|---|---|---|---|---|---|---|---|---|---|"]
    for g in GAMES:
        lines.append(f"| {g} | holds | holds | holds | holds | holds | p | a | n | confirmatory |")
    _write(os.path.join(tmp, "gt_procgen.md"), "\n".join(lines) + "\n")
    _write(os.path.join(tmp, "gt_minigrid.md"), "\n")
    rows = []
    for i, g in enumerate(GAMES):
        rows.append(dict(game=g, agent="N", mode="nav", suite="procgen", condition="center_off", seed=1000,
                         census={a: W[c] for a, c in zip(C.ASSUMPTIONS, CENSUS[i])},
                         level1_completed=bool((done or DONE)[i][0]),
                         adapter=dict(grid=[64, 64], action_list=list(range(15)), n_colours=10)))
        for k, d in enumerate((done or DONE)[i]):
            grid = [grids[i], 1] if grids else [64, 64]
            rows.append(dict(game=g, agent="R", mode="hash_state", suite="procgen", condition="center_off",
                             seed=1000 + k, level1_completed=bool(d),
                             adapter=dict(grid=grid, action_list=list(range(15)), n_colours=10)))
    _write(os.path.join(tmp, "runs.json"), json.dumps(rows))


def run(tmp):
    return analyze_v2.main(["--runs", os.path.join(tmp, "runs.json"), "--truth-procgen", os.path.join(tmp, "gt_procgen.md"),
                            "--truth-minigrid", os.path.join(tmp, "gt_minigrid.md"), "--out", tmp, "--workers", "2"])


class T(unittest.TestCase):
    def test_constant_nuisance(self):
        with tempfile.TemporaryDirectory() as tmp:
            build(tmp)
            table, suite_lines = run(tmp)
            r = [x for x in table if x[2] == "all" and x[3] == "R"][0]
            self.assertEqual((r[4], r[5], r[6]), ("evidence", 8, 4))
            self.assertAlmostEqual(r[7], 0.90625)
            self.assertAlmostEqual(r[10], 0.75)
            self.assertAlmostEqual(r[11], 0.5)
            self.assertEqual(r[12], "neither")
            n = [x for x in table if x[2] == "all" and x[3] == "N"][0]
            self.assertEqual(n[4], "instrument check")
            ir = [x for x in table if x[2] == "in_range" and x[3] == "R"][0]
            self.assertEqual((ir[5], ir[6], ir[12]), (1, 0, "VOID"))
            self.assertTrue(any("I1 absent" in s[3] for s in suite_lines))

    def test_varying_grid(self):
        with tempfile.TemporaryDirectory() as tmp:
            build(tmp, grids=[8, 7, 6, 5, 4, 3, 2, 1])
            table, _ = run(tmp)
            r = [x for x in table if x[2] == "all" and x[3] == "R"][0]
            self.assertAlmostEqual(r[7], 0.90625)
            self.assertAlmostEqual(r[11], 0.9375)
            self.assertEqual(r[12], "neither")

    def test_void(self):
        with tempfile.TemporaryDirectory() as tmp:
            build(tmp, done=[[1]] * 8)
            table, _ = run(tmp)
            r = [x for x in table if x[2] == "all" and x[3] == "R"][0]
            self.assertEqual(r[12], "VOID")

    def test_bootstrap(self):
        s = [5, 5, 4, 4, 3, 2, 1, 1]
        y = [1, 1, 1, 0, 1, 0, 0, 0]
        a = C.bootstrap_auroc_ci(s, y, 2000, 20260927, workers=2)
        b = C.bootstrap_auroc_ci(s, y, 2000, 20260927, workers=1)
        self.assertEqual(a, b)
        self.assertTrue(0 <= a[0] <= a[1] <= 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
