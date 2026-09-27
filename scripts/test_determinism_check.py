"""
Synthetic test of scripts/determinism_check.py (docs/PREREG.md v1.1 draft D8, D13).  Reads no runs/
file and plays no game: rows are written into a temporary folder.

Rows, seed 1000 only, for games maze and heist and modes nav and hash_state.  Each center_off row:
    {"game", "levels": 2, "actions": 20000, "seconds": 10.0, "agent_seconds": 9.0, "condition":
     "center_off", "adapter": {"condition": "center_off", "camera": {"center_agent": false},
     "n_colours": 7}, "level_log": [{"level": 0, "actions": 500, "sec_per_action": 0.01}],
     "diag": {"acts": 20000}}
The center_on row is the same with the three labels set to center_on / true and every timing value
changed (seconds 11.5, agent_seconds 10.2, level_log.0.sec_per_action 0.02), except:
    heist hash_state: levels 3 and diag.acts 19999 on center_on.
Test 1: 4 pairs compared, 3 identical (the timing and label differences are dropped), heist
    hash_state differs in exactly ["diag.acts", "levels"]; exit code 1; the JSON records verdict
    "FAIL (a pair differs)".
Test 2: the heist hash_state center_on row is made equal to the others: 4 of 4 identical, exit code 0,
    verdict "PASS".
Test 3: the maze nav center_on row is deleted (and heist fixed as in test 2): 3 pairs compared, 3
    identical, 1 missing, exit code 2.
Test 4: the script's nine games equal analyze_common.IN_RANGE_C, are disjoint from
    analyze_common.CAMERA_DISTINCT_C, and the two together are the 14 suite-C confirmatory games of
    docs/GROUND_TRUTH_procgen.md.

Command (PowerShell, from D:\\Research\\arc3\\repo):
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\test_determinism_check.py
Expected: "Ran 4 tests ... OK".
"""
from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze_common as C  # noqa: E402
import determinism_check as D  # noqa: E402


def row(game, cond):
    on = cond == "center_on"
    return {"game": game, "levels": 2, "actions": 20000, "seconds": 11.5 if on else 10.0,
            "agent_seconds": 10.2 if on else 9.0, "condition": cond,
            "adapter": {"condition": cond, "camera": {"center_agent": on}, "n_colours": 7},
            "level_log": [{"level": 0, "actions": 500, "sec_per_action": 0.02 if on else 0.01}],
            "diag": {"acts": 20000}}


def write(root, game, mode, cond, r):
    p = os.path.join(root, "procgen", cond, mode, f"{game}__1000.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump([r], f)


def build(root, heist_differs=True, drop_maze_nav=False):
    for g in ("maze", "heist"):
        for m in ("nav", "hash_state"):
            for c in ("center_off", "center_on"):
                r = row(g, c)
                if heist_differs and g == "heist" and m == "hash_state" and c == "center_on":
                    r = copy.deepcopy(r)
                    r["levels"] = 3
                    r["diag"]["acts"] = 19999
                if drop_maze_nav and g == "maze" and m == "nav" and c == "center_on":
                    continue
                write(root, g, m, c, r)


def run(root):
    out = os.path.join(root, "out", "determinism_check.json")
    code = D.main(["--suites", root, "--out", out, "--games", "maze,heist", "--modes", "nav,hash_state",
                   "--seeds", "1", "--workers", "1"])
    with open(out, encoding="utf-8") as f:
        return code, json.load(f)


class T(unittest.TestCase):
    def test_one_pair_differs(self):
        with tempfile.TemporaryDirectory() as tmp:
            build(tmp)
            code, rep = run(tmp)
            self.assertEqual(code, 1)
            self.assertEqual((rep["pairs_compared"], rep["pairs_identical"], rep["pairs_missing"]), (4, 3, 0))
            self.assertEqual(rep["per_game"]["heist"]["differing_fields"], ["diag.acts", "levels"])
            self.assertEqual(rep["per_game"]["heist"]["differing_pairs"][0]["mode"], "hash_state")
            self.assertEqual(rep["per_game"]["maze"]["identical"], 2)
            self.assertEqual(rep["verdict"], "FAIL (a pair differs)")

    def test_all_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            build(tmp, heist_differs=False)
            code, rep = run(tmp)
            self.assertEqual(code, 0)
            self.assertEqual((rep["pairs_compared"], rep["pairs_identical"]), (4, 4))
            self.assertEqual(rep["verdict"], "PASS")

    def test_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            build(tmp, heist_differs=False, drop_maze_nav=True)
            code, rep = run(tmp)
            self.assertEqual(code, 2)
            self.assertEqual((rep["pairs_compared"], rep["pairs_identical"], rep["pairs_missing"]), (3, 3, 1))

    def test_constants(self):
        self.assertEqual(set(D.NINE), set(C.IN_RANGE_C))
        self.assertEqual(set(D.NINE) & set(C.CAMERA_DISTINCT_C), set())
        truth = C.parse_truth_procgen(os.path.join(os.path.dirname(HERE), "docs", "GROUND_TRUTH_procgen.md"))
        self.assertEqual(set(D.NINE) | set(C.CAMERA_DISTINCT_C), set(C.confirmatory("procgen", truth)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
