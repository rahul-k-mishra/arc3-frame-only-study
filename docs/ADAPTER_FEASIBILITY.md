# ADAPTER_FEASIBILITY.md — running the frozen census code on suites B and C

Written 27 September 2026 (W2), after the tag prereg-v1 (commit 19f2a9f).

The census and the agents R and N are frozen by blob hash (PREREG.md Section 5.4): scripts/g_agent.py, g_nav.py, g_motion.py, g_control_probe.py, g_census_table.py and g_nav_run.py. None of them is edited. This file lists every ARC-specific assumption they make, read from source at the tag. For each one it states how suite B (MiniGrid/BabyAI) and suite C (Procgen) are presented to the unchanged code.

**The boundary is one shim**, scripts/env_frame.py `install_arc_shim`:
- It places stand-ins for the modules `arc_agi` and `arcengine` in `sys.modules` before the frozen code is imported.
- g_agent.play's own `from arc_agi import Arcade` / `from arcengine import GameAction` (g_agent.py:317-318) then resolve to an Arcade whose `make(game)` returns an adapter-backed environment.
- A runner (scripts/run_suite.py, W2, to be registered with PREREG v1.1) installs the shim. It then calls `g_nav.play` and `g_agent.play` with `Config(max_actions=20000, seed=s, **MODES[mode])`, exactly as g_nav_run.py:166 builds the configuration for E6.

## 1. ARC-specific assumptions in the frozen code, and how the shim meets each

| # | assumption (source) | suite B | suite C |
|---|---|---|---|
| T1 | **Environment construction**: `Arcade(operation_mode="offline", environments_dir=...)`, `arc.open_scorecard(tags=...)`, `arc.make(game, scorecard_id=card)`, `arc.close_scorecard(card)` with `.environments[*].id/.score/.runs` (g_agent.py:321-323, 834-845) | shim Arcade; open_scorecard returns a token; close_scorecard returns an object with no environments, so the row's score stays 0.0 and no card fields are written (ARC scoring does not apply) | same |
| T2 | **Observation fields**: `raw.frame[-1]` (a 2-D array), `raw.state.name` ∈ {NOT_FINISHED, WIN, GAME_OVER, NOT_STARTED}, `raw.levels_completed`, `raw.available_actions` (g_agent.py:324-337, 427, 493-530; g_control_probe.py:50-56; g_nav.py:378-379) | shim `_Raw`. state is GAME_OVER after an adapter game_end, NOT_FINISHED otherwise; WIN never occurs, so a run ends at the action budget. levels_completed counts the adapter's level ends | same |
| T3 | **Action interface**: `env.step(GameAction.RESET)`, `env.step(GameAction.from_id(k))`, `env.step(GameAction.ACTION6, data={"x","y"})` for clicks (g_agent.py:381-388) | stand-in GameAction (RESET = 0, ACTION1–7). RESET calls adapter.restart(); ACTIONk calls the adapter action given by the key map (item 9). ACTION6 is not offered | same |
| T4 | **Key set**: only actions in `M1.KEYS = (1, 2, 3, 4, 5, 7)` are pressed as keys (g_agent.py:326; g_nav.py:379; g_control_probe.py:47). 6 is reserved for clicks. **At most six non-click actions per game** | the adapter's actions must be mapped onto ids 1, 2, 3, 4, 5, 7 (items 9–10) | the 15 Procgen actions must be mapped onto six ids (item 11) |
| T5 | **Clicks**: `can_click = 6 in avail` (g_agent.py:327). The click scan and click targets assume a 64 × 64 board and 16 colours (`bincount(...clip(0, 15), minlength=16)`, g_agent.py:278, 420-421) | not offered: can_click is False, and the click code never runs | same |
| T6 | **Grid**: `M1.grid` copies frame[-1] into a 64 × 64 int16 array anchored at the top-left and zero-filled (g_control_probe.py:50-56) | the tile grid (at most 25 × 25) is placed on a 64 × 64 canvas (item 12) | the 64 × 64 index grid fills the canvas (item 13) |
| T7 | **Crop**: rows 0 and 63 are never read: `g[1:63]` in g_agent.py:244, 269, 277; g_motion.py:30-31; g_nav.py:192, 211, 683, 720, 870 | canvas row offset 1 (item 12), so no grid row is lost | rows 0 and 63 of the Procgen frame are invisible to the frozen code (item 13) |
| T8 | **Palette**: the census paths use `np.unique` and set membership, with no 16-colour limit (g_motion.py:36; g_nav.py:688, 871). The only 16-colour assumption is `clip(0, 15)` in the click-target and push paths (g_agent.py:278, 829-830). Clicks are off (row T5), and push is off under the registered modes (Config.push = False; MODES in g_nav_run.py:53-55 set only mode "hash") | tile-pattern indices from 1, uncapped (PREREG 3.2); index 0 is the padding | exact-RGB indices 1–64 (PREREG 3.3) |
| T9 | **Level and win signals**: a change of `levels_completed` marks a level end (g_agent.py:516-539; g_nav.py:783-784 via `level_changed`); `state == "WIN"` stops play (g_agent.py:503-504); `"GAME_OVER"` triggers a RESET (g_agent.py:505-515) | level_end = episode success; game_end = failure or truncation; the next episode begins per the episode seeding (item 14) | level_end = prev_level_complete; game_end = death or timeout; RESET per item 15 |
| T10 | **Wall clock**: `play(..., seconds)` stops at the time cap (g_agent.py:462); g_nav_run's default is 900 s per game (g_nav_run.py:148) | the cap must not bind before 20,000 actions (item 16) | same |

**Consequences of registered choices (not new parameters):**
- Under suite-B **raw**, the four agent orientations share one palette index (PREREG 3.2), so a turn changes nothing in the grid the census sees. Turns are no-ops to the frozen code, and forward moves the agent one cell in a direction that the grid does not show. This is the instrument test the truth table predicts (A3-raw fails everywhere), now also invisible to the explorer's state hash.
- The **macro** condition reads `env.unwrapped.agent_dir` inside the adapter to choose its turns. This is part of the action's definition (PREREG 3.2), not an observation, and the census never sees it.

## 2. Needs PREREG v1.1

Each item below is a parameter that the adapters or the shim need and that PREREG v1 did not register. Each gives a proposed value and why. Where scripts/env_frame.py or the adapters implement a value, it is the proposal, unless PREREG v1 already fixed the behaviour. Nothing here is used in a confirmatory run until v1.1 registers it.

9. **Suite B, raw condition: key map.**
   - Proposed: ARC id 1 → left, 2 → right, 3 → forward, 4 → pickup, 5 → drop, 7 → toggle. `done` is not exposed.
   - Why: the primitive set has seven actions and the frozen code presses at most six (row T4). `done` is the least used: BabyAI's done actions are off (verifier.py:26), and in MiniGrid only GoToDoor and GoToObject need it (gotodoor.py:144-147, gotoobject.py:155-158).
   - Consequence: the five confirmatory GoToDoor/GoToObject ids cannot be completed by R or N in either condition. Their truth is A5 fails, so this does not contradict the truth table, but it forces their outcome Y = 0.
10. **Suite B, macro condition: key map.**
    - Proposed: 1 → north, 2 → south, 3 → west, 4 → east, 5 → pickup, 7 → toggle. `drop` and `done` are not exposed.
    - Why: again six slots. pickup and toggle are needed for keys, doors and boxes on most object environments.
    - Consequence: environments whose success needs a drop cannot be completed under macro: PutNear, BabyAI PutNext*, MoveTwoAcross, and LevelGen levels that draw a PutNext instruction. All of them are A5-fails in the truth table.
    - Alternative: 5 → drop instead of pickup. It is worse, because far more environments need pickup.
11. **Suite C: action subset and key map.**
    - Proposed: 1 → action 5 (vx 0, vy +1: up), 2 → action 3 (down), 3 → action 1 (left), 4 → action 7 (right), 5 → action 9 (special 1), 7 → action 10 (special 2). Action ids decode as vx = a/3 − 1, vy = a%3 − 1 (basic-abstract-game.cpp:658-662).
    - Why: PREREG 3.3 registered all 15 actions, but the frozen code presses at most six. The four cardinal moves and the first two special actions are the non-duplicate core. Special 1 is fire in bossfight, caveflyer, dodgeball, fruitbot, plunder, starpilot and ninja; special 2 is starpilot's backward fire and ninja's diagonal throw.
    - Consequence: diagonal moves (for example jump-right in coinrun, action 8) are available only as sequences. Ninja's throws 3 and 4 are unavailable.
    - **This changes PREREG 3.3's action list from 15 to these 6 for every agent.** The adapter keeps all 15 internally, and the fidelity check still exercises all 15.
12. **Suite B: canvas placement and padding.**
    - Proposed: the grid at rows 1..h, columns 0..w−1 of the 64 × 64 canvas; every other cell holds padding index 0.
    - Why: the frozen code reads rows 1–62 only (row T7), and M1.grid anchors at the top-left (row T6), so a grid at row 0 would lose its top row. Adapter palettes start at 1, so the padding never equals a game colour. The padding never changes, so it never registers as motion.
    - The largest suite-B grid (25 × 25) fits.
13. **Suite C: rows 0 and 63.**
    - Proposed: accept that the frozen code does not see the top and bottom pixel rows of the 64 × 64 Procgen frame, and record it.
    - Why: rescaling would change the pixel geometry that MAX_STEP (10 cells) and min_cells (2) act on, and the frozen code cannot be told to read them.
    - The operating-range table (PREREG Section 4) is unaffected.
14. **Suite B: episode seeding and RESET.**
    - PREREG v1 registered "later resets unseeded", but the frozen explorer also RESETs mid-episode: its stuck rule (Config.stuck_limit = 200, g_agent.py:54) and after every GAME_OVER. On ARC, a RESET restarts the current level.
    - Proposed ("replay"): episode k is reset with seed seed·100000 + k; k advances only on a success; a RESET replays episode k's layout. This matches the ARC meaning of RESET, and every layout is reproducible from (seed, k).
    - The v1 behaviour ("unseeded": every RESET starts a new layout) stays the adapter default until v1.1 decides.
15. **Suite C: RESET.**
    - Procgen cannot restart a level. Proposed: a RESET takes no step and returns the current grid.
    - The explorer still counts it as an action (g_agent.py:381-382), so stuck-rule RESETs cost budget and do nothing. After a death, procgen has already moved to a new level (game.cpp:101), so the RESET that follows GAME_OVER only clears the state.
16. **Wall-clock cap per game.**
    - Proposed: set from the fidelity check's steps per second so that 20,000 actions fit three times over, rounded up to a whole minute, one value per suite.
    - The value will be computed from runs/fidelity and registered in v1.1. It is not chosen here.
17. **The runner.** scripts/run_suite.py (W2) installs the shim with the key map of items 9–11 and the placement of items 12–13. Its blob hash is registered in v1.1 with the adapters' hashes (V3 checks them).
18. **For I1 only** (docs/I1_feasibility.md):
    - palette indices ≥ 16 are presented shifted by one (16 is I1's status-bar marker);
    - its level counter is capped at 254 (their FrameData.score, structs.py:210);
    - it uses keys 1–5 only (their action map, heuristic_agent.py:54-58), so on each suite it has the first five mapped actions.

## 3. What does not change

- No frozen file is edited. Every census constant and blob hash of PREREG Section 5.4 is unchanged, and V3 compares them in every row's adapter record (`frozen`).
- The truth tables, thresholds, suites and seeds are unchanged.
- The fidelity check (scripts/fidelity_check.py) drives the adapters directly, without the shim. It therefore tests adapter determinism independently of items 9–17.
