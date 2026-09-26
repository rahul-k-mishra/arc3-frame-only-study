# PREREG_PARAMS.md — census constants, copied from source

Written 27 September 2026 for docs/METHOD_BLUEPRINT.md Section 2.2 ("copied into PREREG.md from the script source, not from memory, with the script's commit hash"). Every value below was read from the file named on its row, at the line given, in the working tree at HEAD 0c1bf9c. No document was used as a source. Each file was clean against HEAD when read (git diff empty).

The commit column is the last commit that changed the file (`git log -1 --format=%H -- <file>`):

| file | last commit |
|---|---|
| scripts/g_nav.py | ccc4d57e26cdee73ea0eabdbd7d7fdfe847ed265 |
| scripts/g_motion.py | 378345f4e7f43e3ea2fedd65f8d23e84b41603c6 |
| scripts/g_control_probe.py | 378345f4e7f43e3ea2fedd65f8d23e84b41603c6 |
| scripts/g_agent.py | 378345f4e7f43e3ea2fedd65f8d23e84b41603c6 |
| scripts/g_census_table.py | a6b315bdd077b8a254542a9441ce1781b82ce70c |
| scripts/g_nav_run.py | b2e071f5c27a90f5c874bc4f9d1bc18f184d45f3 |

## 1. The four named learner parameters

| parameter (METHOD_BLUEPRINT.md 2.2) | constant in source | value | file:line | code |
|---|---|---|---|---|
| three agreeing presses | LEARN_AGREE | 3 | scripts/g_nav.py:55 | `LEARN_AGREE = 3      # agreeing presses before a key's step vector is trusted` |
| 2:1 margin over the runner-up | literal 2 in `_agreed` | 2 | scripts/g_nav.py:756 | `if len(top) > 1 and top[0][1] < 2 * top[1][1]:` (a key is accepted when its top vector has at least LEARN_AGREE votes, line 754, and at least twice the runner-up's votes; exactly 2:1 is accepted) |
| at most 10 px | MAX_STEP | 10 | scripts/g_nav.py:57 | `MAX_STEP = 10        # a step vector component beyond this is a throw or a teleport, not a step` (applied per component at lines 477, 498, 784) |
| at most 8 presses per key | LEARN_MAX | 8 | scripts/g_nav.py:56 | `LEARN_MAX = 8        # presses per key in the learning phase` (stop rule at line 771: a key is decided "no_move" when `n >= LEARN_MAX or (LEARN_MAX - n) < (LEARN_AGREE - best)`) |

The same bound MAX_STEP = 10 is defined separately in the motion detector: scripts/g_motion.py:17 (`MAX_STEP = 10`), applied at scripts/g_motion.py:56. The two definitions are independent; changing one does not change the other.

## 2. Other numeric constants the census depends on

### scripts/g_nav.py (NavHook, the v2 learner and planner; commit ccc4d57)

| constant | value | line | what it controls |
|---|---|---|---|
| BFS_NODES | 40000 | 54 | cap on lattice positions searched per plan (used at 287) |
| NavHook default wall_min | 2 | 113 | bumps before a colour can be a wall (used at 233) |
| NavHook default deadly_min | 2 | 113 | death-step votes before a colour can be deadly or avoid-near (used at 217, 239) |
| NavHook default goal_tries | 6 | 113 | goal-colour targets per level before the planner stops trying recorded goals (used at 349) |
| NavHook default stall_steps | 150 | 114 | steps without a new position before fallback "stalled" (used at 425) |
| NavHook default mispredict_max | 8 | 114 | planner mispredictions before fallback "mispredicted" (used at 428) |
| NavHook default learn_tries | 12 | 114 | stored at 121; not read anywhere else in g_nav.py (it has no effect on the census) |
| NavHook default block_steps | 40 | 114 | steps after which a non-fatal bump with no wall colour expires (used at 268) |
| NavHook default wait_max | 12 | 114 | waits per level when the path is sealed only dynamically (used at 625) |
| NavHook default avoid_death | True | 113 | overridden by the explorer's Config.avoid_death at 917 (see g_agent.py below) |
| wall rule ratio | walked × 8 ≤ wall | 233 | a bumped colour stays a wall while walked-on count is at most 1/8 of its bump count |
| deadly rule ratio | 10·d ≥ 3·(d + walked) | 239 | a colour is deadly when at least 30% of steps onto it killed |
| avoid-near rule ratio | 10·d ≥ 3·(d + near_safe) | 217 | a colour next to the avatar at death is avoided when at least 30% of its sightings were at a death |
| observed-press window | lv_presses < 150 | 493 | the explorer's presses counted for co-mover statistics: the first 150 of every level, plus the planner's own |
| frame rows used | rows 1–62 | 192, 211, 683, 720, 870 | rows 0 and 63 (bars and counters) are excluded |
| co-mover: cell limit | 400 | 695 | a colour with more than 400 vanished cells is not a co-mover |
| co-mover: half of the colour | 2·gone ≥ n_all | 695 | at least half of the colour's cells must shift |
| co-mover: pair limit | 4096 | 699 | gone × came above this is skipped |
| co-mover: match share | 10·matched ≥ 7·gone | 710 | at least 70% of vanished cells line up under the best offset |
| avatar search limit | 40 × shape size | 722 | more avatar-coloured cells than this: the avatar is not searched for by colour |
| arrow-key hypothesis | keys 1–4 | 821 | when exactly one of keys 1–4 is unlearned and the other three agree in step length, the fourth is hypothesised |
| goal ring radius | 1 (dy, dx in −1..1) | 876–877 | colours around the ending position counted as the recorded goal |
| goal hypotheses kept | 6 | 888 | recorded goal colours kept per game, most recent first |

### scripts/g_motion.py (best_shift, the frame-difference motion detector; commit 378345f)

| constant | value | line | what it controls |
|---|---|---|---|
| MAX_STEP | 10 | 17 | offsets beyond ±10 in either component are ignored (56) |
| min_cells | 2 | 20 | fewer changed cells than this: no shift |
| frame rows used | rows 1–62 | 30–31 | rows 0 and 63 excluded |
| per-colour cell limit | 600 | 39 | a colour with more than 600 vanished or appeared cells casts no vote |
| pair limit for the offset histogram | 4096 | 46 | above it the offset is the rounded centroid difference (53–55) |
| match share | 0.7 | 60 | at least 70% of the colour's cells must line up under the offset |

### scripts/g_control_probe.py (commit 378345f)

| constant | value | line | what it controls |
|---|---|---|---|
| KEYS | (1, 2, 3, 4, 5, 7) | 47 | the actions treated as keyboard keys; g_nav.py takes its key set from this at line 379 |

### scripts/g_agent.py (the explorer that drives the game while the census observes; commit 378345f)

| constant | value | line | what it controls |
|---|---|---|---|
| Config.avoid_death | True | 96 | passed to NavHook at g_nav.py:917 |

### scripts/g_census_table.py (category rule; commit a6b315b)

| constant | value | line | what it controls |
|---|---|---|---|
| MODEL_FAILS | ("mispredicted", "localise_failed") | 77 | level-1 fallbacks that make a game a key-controlled non-walker |
| half-the-seeds rule, non-walker | count × 2 ≥ n | 146 | at least half the seeds have a MODEL_FAILS fallback |
| half-the-seeds rule, 2-D walker | count × 2 ≥ n | 148 | at least half the seeds have step vectors spanning two dimensions (rank2, lines 88–95) |
| below-minimum flag | n < 4 | 158 | rows with fewer than 4 seeds are flagged below the 4-seed minimum |

### scripts/g_nav_run.py (runner; commit b2e071f)

| constant | value | line | what it controls |
|---|---|---|---|
| --game-seconds default | 900 | 148 | wall-clock cap per game run; a row cut by it before the budget is not kept (docstring, lines 19–22) |
| --budget default | 3000 | 146 | default only; the census v2 held-out run used 20,000 actions and seeds 1000–1003 per the g_census_table.py docstring (lines 4–5), a command-line choice, not a constant |

## 3. Limits of this list

- The census v2 held-out runs (runs/navrun_v2_heldout.json) predate this repository's first commit (378345f, 25 Sep 2026). g_nav.py has two commits, 378345f and ccc4d57; the diff between them (read in full for lines containing digits) changes none of the constants above. The only changed parameter line is 114, where `oracle=None` was appended to the signature. The other five files have not changed since the commits listed. Whether the census runs used exactly the 378345f code cannot be shown from git; runs/ was not opened.
- "Any other numeric constant the census depends on" was read as: every literal in g_nav.py's NavHook, g_motion.best_shift and g_census_table.py's category rule that changes a census output, plus the key set and the explorer's avoid_death switch. The explorer (g_agent.py) has many further constants that shape which frames the census sees; they are not listed here, and PREREG.md must say whether the explorer is frozen as a whole (by file hash) instead.
- learn_tries = 12 is a declared parameter with no effect; it is listed so that nobody registers it as if it did something.
