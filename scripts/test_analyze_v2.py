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
"instrument check".  I1 is absent, so R alone decides the suite line: R is non-void with AUROC
0.90625 > 0.65, so "not failed (decided by R alone)".
In-range subset: maze only, 0 of 1 positive, share 0 < 0.10: VOID; no non-void evidence agent, so the
suite line is "not decidable".
Test 2, grid area varies: grid [x, 1] with x = 8 7 6 5 4 3 2 1 in the game order.  B is a one-feature
logistic regression, increasing in x (x and Y are positively associated), so AUROC_B = AUROC(x):
positives x = 8,7,6,4, negatives x = 5,3,2,1; 8, 7, 6 beat all four (12), 4 beats 3,2,1 (3): 15/16 =
0.9375.
Test 3, every game completed: share 1.0 > 0.90: VOID.
Test 4, the bootstrap is deterministic for a fixed seed and 0 <= low <= high <= 1.
Test 5, R alone decides a suite-level FAIL (corrected before the v1 tag).  Every game's census is
h h h h h, so S = 5 on all 8 games and P is true on all 8.  Outcomes as above (4 of 8 positive, not
void).  Every positive-negative pair ties, so AUROC = 16 x 0.5 / 16 = 0.5 <= 0.65: R's verdict is
FAIL.  BA: TPR 4/4 = 1, TNR 0/4 = 0, BA = 0.5.  B is constant, AUROC_B = 0.5.  I1 is absent and R is
non-void, so R alone decides: "suite FAIL (decided by R alone)".

Test 6, the D9 exclusions (PREREG v1.1 draft), suite "minigrid", condition "macro".  Eight
confirmatory games.  Two are on the registered macro exclusion list (analyze_common.V2_EXCLUDE):
MiniGrid-PutNear-6x6-N2-v0 and MiniGrid-GoToDoor-5x5-v0.  The other six are test ids
(MiniGrid-T1-v0 ... MiniGrid-T6-v0).  Census (A1..A5; one N seed each), S, P = A2..A5 all hold, and R's
outcome Y (one seed each):
    T1  h h h h h  S=5 P=1 Y=1        T2  h h h h h  S=5 P=1 Y=1
    T3  f h h h h  S=4 P=1 Y=0        T4  h h h f f  S=3 P=0 Y=1
    T5  h h f f f  S=2 P=0 Y=0        T6  h f f f f  S=1 P=0 Y=0
    PutNear-6x6  h h h h f  S=4 P=0 Y=0   (excluded)
    GoToDoor-5x5 h h h f h  S=4 P=0 Y=0   (excluded)
Primary line (T1-T6; the verdict rules apply):
    positives S = 5, 5, 3; negatives S = 4, 2, 1; 9 pairs.  Each 5 beats all three (6); the 3 loses to
    4 and beats 2 and 1 (2).  AUROC = 8/9 = 0.8889.
    P against Y: TP 2 (T1, T2), FN 1 (T4), FP 1 (T3), TN 2 (T5, T6); TPR 2/3, TNR 2/3; BA = 0.6667.
    Precondition 3/6 = 0.5, not void.  Nuisance features constant, AUROC_B = 0.5.
    Verdict: AUROC >= 0.80 but BA < 0.80, so not PASS; AUROC > 0.65, so not FAIL: "neither".
    Suite line: I1 absent, R non-void with 0.8889 > 0.65: "not failed (decided by R alone)".
"All games" line (all 8; reported, not tested):
    positives 5, 5, 3; negatives 4, 2, 1, 4, 4; 15 pairs.  Each 5 beats all five (10); the 3 beats 2 and
    1 only (2).  AUROC = 12/15 = 0.8.
    TP 2, FN 1, FP 1, TN 4; TPR 2/3, TNR 4/5; BA = (0.6667 + 0.8) / 2 = 0.7333.
    Verdict and suite line: "reported, not tested".
The N rows (instrument check) get the same two lines.  R and N get no "primary, D9b included" line.

Test 7, the D9b I1 lists (PREREG v1.1 draft D9b), suite "minigrid", condition "macro".  Eight
confirmatory games: five test ids T1..T5 on no list, and three registered ids:
    MiniGrid-PutNear-6x6-N2-v0     on the D9 list (drop is the success action): excluded for R, N, I1
    MiniGrid-KeyCorridorS3R1-v0    on the D9 macro list (drop precondition) and on I1's: excluded for all
    MiniGrid-DoorKey-5x5-v0        on I1's list only (toggle precondition): kept for R and N
Census (one N seed each), S and P = A2..A5 all hold; outcomes Y for R (N identical) and for I1:
    T1  h h h h h  S=5 P=1   R 1  I1 1        T2  h h h h f  S=4 P=0   R 1  I1 0
    T3  h h h f f  S=3 P=0   R 0  I1 1        T4  h h f f f  S=2 P=0   R 1  I1 0
    T5  h f f f f  S=1 P=0   R 0  I1 0        DoorKey  h h h h h  S=5 P=1   R 1  I1 0
    KeyCorridor h h h h h  S=5 P=1  R 0  I1 0  PutNear  h h h h f  S=4 P=0   R 0  I1 0
R primary (T1-T5, DoorKey; 6 games): positives S = 5, 4, 2, 5; negatives S = 3, 1; 8 pairs.  Each 5 beats
    both (4), the 4 beats both (2), the 2 beats 1 only (1): AUROC = 7/8 = 0.875.  P: TP 2 (T1, DoorKey),
    FN 2 (T2, T4), TN 2, FP 0: BA = (0.5 + 1) / 2 = 0.75.  Share 4/6, not void.  B constant: 0.5.
    Verdict "neither" (BA < 0.80).
R all games (8): negatives add KeyCorridor 5 and PutNear 4.  Pair credit: T1 5 -> 1+1+0.5+1 = 3.5,
    T2 4 -> 1+1+0+0.5 = 2.5, T4 2 -> 0+1+0+0 = 1, DoorKey 5 -> 3.5; 10.5/16 = 0.65625.  TN 3 (T3, T5,
    PutNear), FP 1 (KeyCorridor): BA = (0.5 + 0.75) / 2 = 0.625.  Reported, not tested.
I1 primary (T1-T5; 5 games): positives S = 5, 3; negatives S = 4, 2, 1; 6 pairs.  The 5 beats all three
    (3), the 3 beats 2 and 1 (2): AUROC = 5/6 = 0.8333.  P: TP 1 (T1), FN 1 (T3), TN 3, FP 0: BA = 0.75.
    Share 2/5 = 0.4, not void.  Verdict "neither".
I1 "primary, D9b included" (R's primary set, 6 games): negatives add DoorKey 5.  T1 ties it (0.5):
    3.5 + 2 = 5.5/8 = 0.6875.  FP 1 (DoorKey), TN 3: BA = (0.5 + 0.75) / 2 = 0.625.  Reported, not tested.
I1 all games (8): negatives 4, 2, 1, 5, 5, 4.  T1: 1+1+1+0.5+0.5+1 = 5; T3: 0+1+1+0+0+0 = 2; 7/12 =
    0.58333.  FP 2 (DoorKey, KeyCorridor), TN 4: BA = (0.5 + 4/6) / 2 = 0.58333.  Reported, not tested.
Suite line, primary: R (0.875) and I1 (0.8333) both non-void and > 0.65: "not failed (decided by R and
I1)".  The "primary, D9b included" and "all games" suite lines: "reported, not tested".

Test 8, the registered lists themselves, against docs/GROUND_TRUTH_minigrid.md (a document; no runs/
file): R/N raw 6 and macro 49; I1 raw 63 and macro 78 (each including MiniGrid-Playground-v0, which
has no success at all; D9 amendment of 27 Sep 2026 (g)); no duplicates; every id is a confirmatory
suite-B environment; I1's list contains the R/N list of the same condition; raw is contained in macro;
no procgen list for either.

Test 9, the secondary condition center_on (PREREG v1.1 draft D13).  Suite "procgen", 7 confirmatory
games: alpha, maze (not camera-distinct; maze is in range) and caveflyer, climber, fruitbot, jumper,
ninja (analyze_common.CAMERA_DISTINCT_C).  The same census, one N seed per game, in both conditions,
and the same R outcome Y (one seed) in both:
    caveflyer h h h h h  S=5 P=1 Y=1     climber h h h h f  S=4 P=0 Y=0     fruitbot h h h f f  S=3 P=0 Y=1
    jumper    h h f f f  S=2 P=0 Y=0     ninja   h f f f f  S=1 P=0 Y=0
    alpha     h h h h h  S=5 P=1 Y=1     maze    h h h h h  S=5 P=1 Y=0
center_on, "camera_distinct" (the five; reported, not tested): positives S = 5, 3; negatives S = 4, 2,
    1; 6 pairs.  The 5 beats all three (3), the 3 beats 2 and 1 (2): AUROC = 5/6 = 0.8333.  P: TP 1
    (caveflyer), FN 1 (fruitbot), TN 3, FP 0: BA = 0.75.  Share 2/5 = 0.4.  B constant: 0.5.  Verdict
    "reported, not tested"; suite line "reported, not tested".  No "all" or "in_range" line exists
    under center_on.
center_off, "all" (7 games; tested): positives 5 (caveflyer), 3 (fruitbot), 5 (alpha); negatives 4, 2, 1,
    5 (maze); 12 pairs.  Each 5 beats 4, 2, 1 and ties 5 (3.5 each, 7), the 3 beats 2 and 1 (2):
    AUROC = 9/12 = 0.75.  P: TP 2 (caveflyer, alpha), FN 1 (fruitbot), TN 3, FP 1 (maze): BA =
    (2/3 + 3/4) / 2 = 0.70833.  Verdict "neither" (0.65 < 0.75 < 0.80).  Suite line: "not failed
    (decided by R alone)".
center_off, "in_range" (maze only): 0 of 1 positive: VOID; suite line "not decidable (no non-void
    evidence agent)".

Command (PowerShell, from D:\\Research\\arc3\\repo):
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\test_analyze_v2.py
Expected: "Ran 9 tests ... OK".
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


def build(tmp, grids=None, done=None, census=None):
    lines = ["| game | A1 | A2 | A3 | A4 | A5 | p | a | n | status |", "|---|---|---|---|---|---|---|---|---|---|"]
    for g in GAMES:
        lines.append(f"| {g} | holds | holds | holds | holds | holds | p | a | n | confirmatory |")
    _write(os.path.join(tmp, "gt_procgen.md"), "\n".join(lines) + "\n")
    _write(os.path.join(tmp, "gt_minigrid.md"), "\n")
    rows = []
    for i, g in enumerate(GAMES):
        rows.append(dict(game=g, agent="N", mode="nav", suite="procgen", condition="center_off", seed=1000,
                         census={a: W[c] for a, c in zip(C.ASSUMPTIONS, (census or CENSUS)[i])},
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
            lines = {s[2]: s[3] for s in suite_lines}
            self.assertEqual(lines["all"], "not failed (decided by R alone)")
            self.assertEqual(lines["in_range"], "not decidable (no non-void evidence agent)")

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

    def test_r_alone_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            build(tmp, census=["hhhhh"] * 8)
            table, suite_lines = run(tmp)
            r = [x for x in table if x[2] == "all" and x[3] == "R"][0]
            self.assertAlmostEqual(r[7], 0.5)
            self.assertAlmostEqual(r[10], 0.5)
            self.assertAlmostEqual(r[11], 0.5)
            self.assertEqual(r[12], "FAIL")
            lines = {s[2]: s[3] for s in suite_lines}
            self.assertEqual(lines["all"], "suite FAIL (decided by R alone)")

    def test_d9_exclusions(self):
        ids = ["MiniGrid-T1-v0", "MiniGrid-T2-v0", "MiniGrid-T3-v0", "MiniGrid-T4-v0", "MiniGrid-T5-v0",
               "MiniGrid-T6-v0", "MiniGrid-PutNear-6x6-N2-v0", "MiniGrid-GoToDoor-5x5-v0"]
        census = ["hhhhh", "hhhhh", "fhhhh", "hhhff", "hhfff", "hffff", "hhhhf", "hhhfh"]
        y = [1, 1, 0, 1, 0, 0, 0, 0]
        with tempfile.TemporaryDirectory() as tmp:
            lines = ["| id | reg | A1 | A2 | A3-raw | A3-macro | A4 | A5 | pred | src | status |", "|---|---|---|---|---|---|---|---|---|---|---|"]
            lines += [f"| {g} | r | holds | holds | fails | holds | holds | holds | p | s | confirmatory |" for g in ids]
            _write(os.path.join(tmp, "gt_minigrid.md"), "\n".join(lines) + "\n")
            _write(os.path.join(tmp, "gt_procgen.md"), "\n")
            rows = []
            ad = dict(grid=[7, 7], action_list=list(range(6)), n_colours=5)
            for i, g in enumerate(ids):
                rows.append(dict(game=g, agent="N", mode="nav", suite="minigrid", condition="macro", seed=1000,
                                 census={a: W[c] for a, c in zip(C.ASSUMPTIONS, census[i])},
                                 level1_completed=bool(y[i]), adapter=ad))
                rows.append(dict(game=g, agent="R", mode="hash_state", suite="minigrid", condition="macro", seed=1000,
                                 level1_completed=bool(y[i]), adapter=ad))
            _write(os.path.join(tmp, "runs.json"), json.dumps(rows))
            table, suite_lines = analyze_v2.main(["--runs", os.path.join(tmp, "runs.json"), "--truth-minigrid",
                                                  os.path.join(tmp, "gt_minigrid.md"), "--truth-procgen",
                                                  os.path.join(tmp, "gt_procgen.md"), "--out", tmp, "--workers", "2"])
            by = {(x[2], x[3]): x for x in table}
            self.assertEqual(sorted({x[2] for x in table}), ["all games", "primary"])
            for agent in ("R", "N"):
                p, a = by[("primary", agent)], by[("all games", agent)]
                self.assertEqual((p[5], p[6]), (6, 3))
                self.assertAlmostEqual(p[7], 8 / 9)
                self.assertAlmostEqual(p[10], 2 / 3)
                self.assertAlmostEqual(p[11], 0.5)
                self.assertEqual(p[12], "neither")
                self.assertEqual((a[5], a[6]), (8, 3))
                self.assertAlmostEqual(a[7], 0.8)
                self.assertAlmostEqual(a[10], (2 / 3 + 0.8) / 2)
                self.assertEqual(a[12], "reported, not tested")
            self.assertEqual(by[("primary", "N")][4], "instrument check")
            sl = {s[2]: s[3] for s in suite_lines}
            self.assertEqual(sl["primary"], "not failed (decided by R alone)")
            self.assertEqual(sl["all games"], "reported, not tested")

    def test_d9b_i1_exclusions(self):
        ids = ["MiniGrid-T1-v0", "MiniGrid-T2-v0", "MiniGrid-T3-v0", "MiniGrid-T4-v0", "MiniGrid-T5-v0",
               "MiniGrid-DoorKey-5x5-v0", "MiniGrid-KeyCorridorS3R1-v0", "MiniGrid-PutNear-6x6-N2-v0"]
        census = ["hhhhh", "hhhhf", "hhhff", "hhfff", "hffff", "hhhhh", "hhhhh", "hhhhf"]
        y_r = [1, 1, 0, 1, 0, 1, 0, 0]
        y_i1 = [1, 0, 1, 0, 0, 0, 0, 0]
        with tempfile.TemporaryDirectory() as tmp:
            lines = ["| id | reg | A1 | A2 | A3-raw | A3-macro | A4 | A5 | pred | src | status |", "|---|---|---|---|---|---|---|---|---|---|---|"]
            lines += [f"| {g} | r | holds | holds | fails | holds | holds | holds | p | s | confirmatory |" for g in ids]
            _write(os.path.join(tmp, "gt_minigrid.md"), "\n".join(lines) + "\n")
            _write(os.path.join(tmp, "gt_procgen.md"), "\n")
            rows = []
            ad = dict(grid=[7, 7], action_list=list(range(6)), n_colours=5)
            for i, g in enumerate(ids):
                rows.append(dict(game=g, agent="N", mode="nav", suite="minigrid", condition="macro", seed=1000,
                                 census={a: W[c] for a, c in zip(C.ASSUMPTIONS, census[i])},
                                 level1_completed=bool(y_r[i]), adapter=ad))
                rows.append(dict(game=g, agent="R", mode="hash_state", suite="minigrid", condition="macro", seed=1000,
                                 level1_completed=bool(y_r[i]), adapter=ad))
                rows.append(dict(game=g, agent="I1", mode="i1", suite="minigrid", condition="macro", seed=1000,
                                 level1_completed=bool(y_i1[i]), adapter=ad))
            _write(os.path.join(tmp, "runs.json"), json.dumps(rows))
            table, suite_lines = analyze_v2.main(["--runs", os.path.join(tmp, "runs.json"), "--truth-minigrid",
                                                  os.path.join(tmp, "gt_minigrid.md"), "--truth-procgen",
                                                  os.path.join(tmp, "gt_procgen.md"), "--out", tmp, "--workers", "2"])
            by = {(x[2], x[3]): x for x in table}
            self.assertEqual(sorted(by), [("all games", "I1"), ("all games", "N"), ("all games", "R"),
                                          ("primary", "I1"), ("primary", "N"), ("primary", "R"),
                                          ("primary, D9b included", "I1")])
            expect = {("primary", "R"): (6, 4, 7 / 8, 0.75, "neither"),
                      ("primary", "N"): (6, 4, 7 / 8, 0.75, "neither"),
                      ("all games", "R"): (8, 4, 10.5 / 16, 0.625, "reported, not tested"),
                      ("primary", "I1"): (5, 2, 5 / 6, 0.75, "neither"),
                      ("primary, D9b included", "I1"): (6, 2, 5.5 / 8, 0.625, "reported, not tested"),
                      ("all games", "I1"): (8, 2, 7 / 12, 7 / 12, "reported, not tested")}
            for k, (n, pos, auc, ba, verdict) in expect.items():
                x = by[k]
                self.assertEqual((x[5], x[6]), (n, pos), k)
                self.assertAlmostEqual(x[7], auc, msg=str(k))
                self.assertAlmostEqual(x[10], ba, msg=str(k))
                self.assertAlmostEqual(x[11], 0.5, msg=str(k))
                self.assertEqual(x[12], verdict, k)
            sl = {s[2]: s[3] for s in suite_lines}
            self.assertEqual(sl["primary"], "not failed (decided by R and I1)")
            self.assertEqual(sl["primary, D9b included"], "reported, not tested")
            self.assertEqual(sl["all games"], "reported, not tested")

    def test_registered_lists(self):
        truth = C.parse_truth_minigrid(os.path.join(os.path.dirname(HERE), "docs", "GROUND_TRUTH_minigrid.md"))
        conf = set(C.confirmatory("minigrid", truth))
        self.assertEqual(len(conf), 161)
        sizes = {("R", "raw"): 6, ("R", "macro"): 49, ("I1", "raw"): 63, ("I1", "macro"): 78}
        for (agent, cond), n in sizes.items():
            lst = C.v2_exclusions("minigrid", cond, agent)
            self.assertEqual(len(lst), n, (agent, cond))
            self.assertEqual(len(set(lst)), n, (agent, cond))
            self.assertEqual(set(lst) - conf, set(), (agent, cond))
            self.assertTrue(set(C.v2_exclusions("minigrid", cond, "R")) <= set(lst))
            self.assertEqual(C.v2_exclusions("minigrid", cond, "N"), C.v2_exclusions("minigrid", cond, "R"))
        for agent in ("R", "I1"):
            self.assertTrue(set(C.v2_exclusions("minigrid", "raw", agent)) <= set(C.v2_exclusions("minigrid", "macro", agent)))
            for cond in ("center_off", "center_on"):
                self.assertEqual(C.v2_exclusions("procgen", cond, agent), ())

    def test_center_on(self):
        games = ["caveflyer", "climber", "fruitbot", "jumper", "ninja", "alpha", "maze"]
        census = ["hhhhh", "hhhhf", "hhhff", "hhfff", "hffff", "hhhhh", "hhhhh"]
        y = [1, 0, 1, 0, 0, 1, 0]
        with tempfile.TemporaryDirectory() as tmp:
            lines = ["| game | A1 | A2 | A3 | A4 | A5 | p | a | n | status |", "|---|---|---|---|---|---|---|---|---|---|"]
            lines += [f"| {g} | holds | holds | holds | holds | holds | p | a | n | confirmatory |" for g in games]
            _write(os.path.join(tmp, "gt_procgen.md"), "\n".join(lines) + "\n")
            _write(os.path.join(tmp, "gt_minigrid.md"), "\n")
            rows = []
            ad = dict(grid=[64, 64], action_list=list(range(6)), n_colours=10)
            for cond in ("center_off", "center_on"):
                for i, g in enumerate(games):
                    rows.append(dict(game=g, agent="N", mode="nav", suite="procgen", condition=cond, seed=1000,
                                     census={a: W[c] for a, c in zip(C.ASSUMPTIONS, census[i])},
                                     level1_completed=bool(y[i]), adapter=ad))
                    rows.append(dict(game=g, agent="R", mode="hash_state", suite="procgen", condition=cond,
                                     seed=1000, level1_completed=bool(y[i]), adapter=ad))
            _write(os.path.join(tmp, "runs.json"), json.dumps(rows))
            table, suite_lines = run(tmp)
            by = {(x[1], x[2], x[3]): x for x in table}
            self.assertEqual(sorted({(x[1], x[2]) for x in table}),
                             [("center_off", "all"), ("center_off", "in_range"), ("center_on", "camera_distinct")])
            r = by[("center_on", "camera_distinct", "R")]
            self.assertEqual((r[5], r[6], r[12]), (5, 2, "reported, not tested"))
            self.assertAlmostEqual(r[7], 5 / 6)
            self.assertAlmostEqual(r[10], 0.75)
            self.assertAlmostEqual(r[11], 0.5)
            r = by[("center_off", "all", "R")]
            self.assertEqual((r[5], r[6], r[12]), (7, 3, "neither"))
            self.assertAlmostEqual(r[7], 0.75)
            self.assertAlmostEqual(r[10], (2 / 3 + 3 / 4) / 2)
            r = by[("center_off", "in_range", "R")]
            self.assertEqual((r[5], r[6], r[12]), (1, 0, "VOID"))
            sl = {(s[1], s[2]): s[3] for s in suite_lines}
            self.assertEqual(sl[("center_on", "camera_distinct")], "reported, not tested")
            self.assertEqual(sl[("center_off", "all")], "not failed (decided by R alone)")
            self.assertEqual(sl[("center_off", "in_range")], "not decidable (no non-void evidence agent)")

    def test_bootstrap(self):
        s = [5, 5, 4, 4, 3, 2, 1, 1]
        y = [1, 1, 1, 0, 1, 0, 0, 0]
        a = C.bootstrap_auroc_ci(s, y, 2000, 20260927, workers=2)
        b = C.bootstrap_auroc_ci(s, y, 2000, 20260927, workers=1)
        self.assertEqual(a, b)
        self.assertTrue(0 <= a[0] <= a[1] <= 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
