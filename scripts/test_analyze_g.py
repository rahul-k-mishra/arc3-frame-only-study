"""
Synthetic test of scripts/analyze_g.py (docs/PREREG.md v1, Section 11).  Reads no runs/ file and
plays no game.

Suite "procgen", condition "center_off".  Confirmatory games alpha and bravo; coinrun is a registered
pilot and must be ignored.  G rows (agent "G"):
    alpha seed 1000: defined, place 1,    feat 1,    act 2.0
    alpha seed 1001: defined, place null, feat 2,    act 4.0
    alpha seed 1002: defined, place 3,    feat null, act null
    alpha seed 1003: not defined (A2 fails)
    bravo seed 1000: defined, place 5,    feat 5,    act 10.0
    coinrun seed 1000: defined, place 99, feat 99,   act 99.0   (ignored)
Hand computation (lower median = element at index floor((n-1)/2) of the sorted list, infinity last):
    alpha: seeds 4, undefined 1; place [1, inf, 3] -> sorted [1, 3, inf] -> index 1 -> 3, inf count 1;
           feat [1, 2, inf] -> 2, inf count 1; act [2.0, 4.0] -> index 0 -> 2.0.
    bravo: seeds 1, undefined 0; place 5, inf 0; feat 5, inf 0; act 10.0.
    suite: games 2; place lower median of [3, 5] = 3; feat of [2, 5] = 2; act of [2.0, 10.0] = 2.0.

Command (PowerShell, from D:\\Research\\arc3\\repo):
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\test_analyze_g.py
Expected: "Ran 2 tests ... OK".
"""
from __future__ import annotations

import json
import math
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
import analyze_g  # noqa: E402


def g(defined=True, place=None, feat=None, act=None):
    return dict(defined=defined, G_end_place=place, G_end_feat=feat, G_act=act)


ROWS = [("alpha", 1000, g(place=1, feat=1, act=2.0)), ("alpha", 1001, g(place=None, feat=2, act=4.0)),
        ("alpha", 1002, g(place=3, feat=None, act=None)), ("alpha", 1003, g(defined=False)),
        ("bravo", 1000, g(place=5, feat=5, act=10.0)), ("coinrun", 1000, g(place=99, feat=99, act=99.0))]


class T(unittest.TestCase):
    def test_lower_median(self):
        self.assertEqual(C.lower_median([1, math.inf, 3]), 3)
        self.assertEqual(C.lower_median([2.0, 4.0]), 2.0)
        self.assertIsNone(C.lower_median([]))

    def test_g(self):
        with tempfile.TemporaryDirectory() as tmp:
            lines = ["| game | A1 | A2 | A3 | A4 | A5 | p | a | n | status |", "|---|---|---|---|---|---|---|---|---|---|",
                     "| alpha | holds | holds | holds | holds | holds | p | a | n | confirmatory |",
                     "| bravo | holds | holds | holds | holds | holds | p | a | n | confirmatory |",
                     "| coinrun | holds | holds | fails | holds | holds | p | a | n | pilot candidate |"]
            _write(os.path.join(tmp, "gt_procgen.md"), "\n".join(lines) + "\n")
            _write(os.path.join(tmp, "gt_minigrid.md"), "\n")
            rows = [dict(game=gm, agent="G", mode="g_cost", suite="procgen", condition="center_off", seed=s, G=G)
                    for gm, s, G in ROWS]
            _write(os.path.join(tmp, "runs.json"), json.dumps(rows))
            games, suite = analyze_g.main(["--runs", os.path.join(tmp, "runs.json"), "--truth-procgen",
                                           os.path.join(tmp, "gt_procgen.md"), "--truth-minigrid",
                                           os.path.join(tmp, "gt_minigrid.md"), "--out", tmp])
            by = {r[2]: r for r in games}
            self.assertEqual(sorted(by), ["alpha", "bravo"])
            self.assertEqual(by["alpha"][3:], [4, 1, 3, 1, 2, 1, 2.0])
            self.assertEqual(by["bravo"][3:], [1, 0, 5, 0, 5, 0, 10.0])
            self.assertEqual(suite, [["procgen", "center_off", 2, 3, 2, 2.0]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
