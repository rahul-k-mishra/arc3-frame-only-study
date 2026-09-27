# PREREG.md — v1

Registered protocol for the method paper "assumption census and goal-identification cost". Written 27 September 2026 from docs/METHOD_BLUEPRINT.md draft 1.4, docs/PREREG_PARAMS.md, docs/GROUND_TRUTH_minigrid.md, docs/GROUND_TRUTH_procgen.md and docs/W0_CHECKS.md.

**Registration.** This file becomes the registered protocol when RKM creates the git tag `prereg-v1` on the commit that contains it, and registers the same text on OSF (docs/OSF_REGISTRATION.md). Before the tag nothing here binds. After it, the file changes only by a new version with a diff section (Section 12).

**What exists at v1, and what does not.**
- Exists:
  - the census code (scripts/g_nav.py and its dependencies) and the ARC runner (scripts/g_nav_run.py);
  - the three analysis scripts, with synthetic tests;
  - the two truth tables.
- Written in W2, under PREREG v1.1: the suite-B and suite-C adapters, the I1 adaptation and scripts/g_goal_cost.py.
- The runs of Section 9 that need those scripts can therefore only be performed after v1.1. The runs that need nothing new (E6 and R on ARC) can be performed under this version.

**Pre-tag confirmations.** Where RKM's decisions left a detail open, this file fills it and marks the text **[registered here]**. Tagging v1 confirms each one; changing one before the tag is a normal edit, and after the tag it needs a new version. The items:
1. The per-seed census rules on the G-NAV report (Section 5.3), and the seed-majority rule.
2. The game outcome for V2: completed level 1 in at least half the seeds; "level 1 completed" on suites B and C (Section 9.3).
3. The suite-B macro action list: four macros plus pickup, drop, toggle and done passed through (Section 3.2).
4. The suite-C palette overflow rule, and the Procgen settings carried over from W0 check C2 (distribution_mode easy, use_backgrounds False, use_monochrome_assets True) (Section 3.3).
5. The details of the nuisance baseline B and of the bootstrap (Section 10.2).
6. The G coverage policy (N's frontier rule) and the feature set F(c) (Section 6).

**Corrected before v1 tag (27 Sep 2026).** Three corrections made by RKM before the tag. They are part of v1 as tagged, not amendments:
1. **A4 rule (Section 5.3).** The "at least one wall colour learned" clause is dropped. On games whose only blocker is the world boundary no wall colour can be learned, and the truth table gives A4 holds there.
2. **Suite-level FAIL (Section 10).** Decided by the evidence agents present and non-void: R and I1 together when both are non-void, R alone when I1 is absent or void. Support still requires I1 to pass.
3. **Suite C power note (Section 10).** Added under V2.

Two facts found while writing this file, recorded rather than resolved:
- **start_level has no effect when num_levels is 0** (vecgame.cpp:287-289, Section 3.3). The Procgen level sequence is fixed by rand_seed alone.
- **No ARC truth table exists** for the 8 train games. V1 on ARC (development) is computed only after docs/GROUND_TRUTH_arc_train.md is written from source (W2).

---

## 1. Claim and non-claims

> A fixed, cheap, frame-only probe battery (the assumption census) together with a defined goal-identification cost G, with every parameter frozen on eight ARC-AGI-3 training games, (i) reports the ground-truth mechanics of unseen games in three suites at a registered accuracy, and (ii) predicts, before any agent is run, on which unseen games assumption-driven frame-only agents complete the first level.

- Half (i), instrument validity: the census says what the game's source code says (V1).
- Half (ii), predictive validity: the census verdict predicts whether an agent of the stated family completes level 1 (V2).
- Both halves are required. ARC-AGI-3 is the development instance; it is not evidence of generality.

Not claimed:
- that goal inference is "the" barrier on ARC-AGI-3. E1 was inconclusive. The goal-oracle intervention E9 returned INCONCLUSIVE: tu93 MIXED, dc22 NOT BINDING, ls20 NOT TESTABLE (runs/e9_report.json, docs/E9_protocol.md).
- that any agent here is strong;
- that anything transfers to hidden ARC-AGI-3 games or the leaderboard;
- that the census is complete;
- any theorem. G is a measured quantity with cited observations (Section 6; docs/PRIOR_ART_KILL.md Part D).

## 2. Family and agents

**Family.** Frame-only, prior-free, CPU-runnable agents that do not read game source (docs/archive/TOG_PLAN_v2.md Section 0).

| agent | what | role in V2 |
|---|---|---|
| R | the E2 hash_state explorer, scripts/g_agent.py (mode hash_state) | evidence |
| N | the G-NAV planner, scripts/g_nav.py on scripts/g_agent.py (mode nav) | instrument check only: N uses A1–A5 by construction, so its agreement with the census is circular; its runs also supply the census (Section 5) |
| I1 | Rudakov, Shock & Cowley, "Graph-Based Exploration for ARC-AGI-3 Interactive Reasoning Tasks" (arXiv:2512.24156; MIT; external/, adapter scripts/e1_rudakov_adapter.py) | evidence |

- **No I2.** E1c searched and closed with none (docs/E1c_search.md). The search reopens only if Milestone-2 releases add a permissive-licence, non-LLM, CPU frame-only agent.
- **I1 outside ARC.** Whether I1 can be adapted to suites B and C is documented in W2 (docs/I1_feasibility.md). If it cannot, the paper carries this sentence: *"No independent agent could be run outside ARC-AGI-3; on suites B and C, V2 rests on the author's explorer R alone, and the predictive claim there is narrowed to 'predicts the author's explorer'."*

**Admissibility** (docs/archive/TOG_PLAN_v2.md Section 3.1, reused unchanged):
- No GPU, no LLM, no network; deterministic given seed.
- **A6, fidelity:** where the agent can run in its own loop, its first 1,000 actions on ft09 and tu93 with a fixed seed are identical under its loop and ours. Otherwise it is labelled "adapter only, fidelity not checked".
- **A7, cost:** at most 0.28 s per action on the lenovo, measured over 2,000 actions on each of ft09 and tu93. Between 0.28 and 0.70 s: 4 seeds instead of 10, labelled so. Above 0.70 s: inadmissible for cost.

## 3. Environment contract and per-suite adapter parameters

**Contract.** Every suite is wrapped so that the census and the agents see only:
- `reset(seed) -> grid`, where grid is an integer colour-index array;
- `step(action) -> grid, level_end, game_end`;
- a fixed action list per game.

No reward, no symbolic state, no text, no "accepted" flag.

**Each adapter parameter below is registered here and never tuned after.** The pilot (Section 8) may fix adapter code and the tile-size scaling rule, never a parameter value.

### 3.1 ARC-AGI-3 (development instance)
- Frame: the native integer grid of arc-agi 0.9.8 / arcengine 0.9.3; 64 × 64; palette none (the frame is already colour indices).
- Crop: rows 1–62 (rows 0 and 63 excluded; scripts/g_motion.py:30-31, scripts/g_nav.py:192).
- Grid: 64 × 64.
- Census key set: KEYS = (1, 2, 3, 4, 5, 7), scripts/g_control_probe.py:47. The agents act on the game's available actions, as in E2.
- level_end: an ARC level completion. game_end: WIN or the action budget.

### 3.2 Suite B — MiniGrid and BabyAI (Python 3.11.9, minigrid 3.1.0, gymnasium 1.3.0, D:\Research\arc3\brutus\.venv_games)
- Construction: `gymnasium.make(id, render_mode="rgb_array", highlight=False, tile_size=8, agent_pov=False)` (keywords from minigrid/minigrid_env.py:43-47). The frame is `env.render()`, the full grid (minigrid_env.py:736-742).
- **Palette, tile-pattern:**
  - The frame is cut into 8 × 8 tiles. Each distinct 8 × 8 RGB tile pattern gets one integer index, in order of first appearance within the run (online).
  - The four agent orientations are merged into one index. The adapter renders the agent's four patterns in advance with minigrid's own renderer (Grid.render_tile with agent_dir 0–3, highlight False, tile size 8, on an empty cell), and maps any tile equal to one of them to a single index.
  - An agent tile drawn over a non-empty cell (an open door) is a distinct pattern and is not merged. This is a known limit.
  - No cap.
- Grid: frame height / 8 × frame width / 8, per environment (3 × 7 to 25 × 25; W0_CHECKS.md amendment of 27 Sep 2026).
- Crop: none.
- **Two action conditions:**
  - **raw:** the primitive action set — left, right, forward, pickup, drop, toggle, done (0–6, minigrid/core/actions.py:9-20). Dynamic-Obstacles exposes only left, right, forward (envs/dynamicobstacles.py:104).
  - **macro:** north, south, east, west. Each is turn-to-face (the fewest left/right turns, at most 2) then forward, and the frame returned is the one after the forward. If a sub-step terminates, the macro stops there and returns that frame. **[registered here]** The non-move primitives pickup, drop, toggle and done are passed through unchanged as four more actions (eight in all; Dynamic-Obstacles has the four macros only), because doors and objects cannot be operated otherwise.
- Seeding: `env.reset(seed=seed)` once; later resets are unseeded, so the environment RNG continues deterministically (as in W0 check C3). BABYAI_DONE_ACTIONS is unset (verifier.py:26).
- **level_end:** an episode that terminates with reward > 0, i.e. success. Termination with reward 0 or −1, and truncation, are game_end without a level end. The next episode begins with an unseeded reset.

### 3.3 Suite C — Procgen 0.10.7 (Python 3.10, D:\Research\arc3\brutus\.venv_procgen)
- Construction: `ProcgenGym3Env(num=1, env_name=game, distribution_mode="easy", use_backgrounds=False, use_monochrome_assets=True, center_agent=<condition>, use_sequential_levels=True, num_levels=0, start_level=seed, rand_seed=seed, num_threads=1)`.
- **Camera (RKM decision):**
  - Primary condition `center_off`: center_agent False for all 16 games.
  - Secondary condition `center_on`: the default scrolling view (center_agent True), reported alongside.
- **Levels (RKM decision):** use_sequential_levels True, num_levels 0, start_level = rand_seed = the seed (1000–1009).
  - **Finding:** with num_levels 0, procgen sets the level-seed range to [0, INT32_MAX) and never reads start_level (vecgame.cpp:287-289). The first level's seed is drawn by `level_seed_rand_gen`, which is seeded from `game_level_seed_gen.seed(rand_seed)` (vecgame.cpp:301-314). The level sequence is therefore fixed by rand_seed alone, and start_level = seed is recorded but inert.
  - On completion the next level is seed + 997 with no episode boundary (game.cpp:97-99, 148-150). After a death or timeout, a fresh level seed is drawn (game.cpp:101).
- **Frame:** obs["rgb"][0], 64 × 64 × 3, native, no crop.
- **Palette, exact-RGB online:** each distinct RGB triple gets the next integer index in order of first appearance within the run, capped at 64 entries. **[registered here]** From the 65th distinct colour on, a colour maps to the existing index with the smallest squared RGB distance, ties to the lowest index. The number of distinct colours seen is recorded.
- Grid: 64 × 64 (one cell per pixel).
- Action list: all 15 actions, 0–14. Duplicates and no-ops are kept; they are listed per game in GROUND_TRUTH_procgen.md.
- **level_end:** info key `prev_level_complete` == 1 (game.cpp:163; vecgame.cpp:250). game_end: the `first` flag, i.e. death or timeout.
- **[registered here]** Carried over from W0 check C2: distribution_mode easy, use_backgrounds False, use_monochrome_assets True.

## 4. Instrument operating range (suite C)

The census detects motion only when at least min_cells = 2 cells change (scripts/g_motion.py:20). With center_agent False, procgen draws the whole world into 64 pixels: `visibility = main_width > main_height ? main_width : main_height;` then `raw_unit = 64 / visibility` pixels per world unit (basic-abstract-game.cpp:825-831). The agent spans 2·min(rx, ry)·64 / max(W, H) pixels.

**The operating range is the set of games whose agent spans at least 2 pixels.** Easy mode, sources at tag 0.10.7 (file:line as in GROUND_TRUTH_procgen.md):

| game | world W × H (source) | agent rx, ry (source) | px per unit | agent span (px) | in range |
|---|---|---|---|---|---|
| bigfish | 20 × 20 (bigfish.cpp:27-28) | 1.0 (easy start_r, bigfish.cpp:67-76) | 3.20 | 6.40 | yes (pilot) |
| bossfight | 20 × 20 (bossfight.cpp:65-66) | rx .75; ry from asset aspect (bossfight.cpp:241-242, BAG:1014-1022) | 3.20 | 4.80 (rx) | yes |
| caveflyer | 30 × 30 (caveflyer.cpp:133-134) | 0.4 default (BAG:778) | 2.13 | 1.71 | **no** |
| chaser | 11 × 11 (chaser.cpp:144, 136-137) | .5 (chaser.cpp:168-169) | 5.82 | 5.82 | yes |
| climber | 16 × 64 (climber.cpp:231-232) | .5 (climber.cpp:245-246) | 1.00 | 1.00 | **no** |
| coinrun | 64 × 64 (coinrun.cpp:54-55) | .5, .5787 (coinrun.cpp:435-436) | 1.00 | 1.00 | **no** (pilot) |
| dodgeball | 20 × 20 (dodgeball.cpp:249-256) | 1.0 easy (dodgeball.cpp:286-287) | 3.20 | 6.40 | yes |
| fruitbot | 10 × 60 (fruitbot.cpp:149, 154) | 0.4 default | 1.07 | 0.85 | **no** |
| heist | 9 × 9 (heist.cpp:102, 111-112) | .375 × maze_scale 1 (heist.cpp:142-143) | 7.11 | 5.33 | yes |
| jumper | 20 × 20 (jumper.cpp:210, 217-218) | .254, .4 (jumper.cpp:375-376) | 3.20 | 1.63 | **no** |
| leaper | 9 × 9 (leaper.cpp:109, 114-115) | 0.4 default | 7.11 | 5.69 | yes |
| maze | 15 × 15 (maze.cpp:44, 51-52) | .5 (maze.cpp:68-69) | 4.27 | 4.27 | yes |
| miner | 10 × 10 (miner.cpp:120-122) | .5 (miner.cpp:135-136) | 6.40 | 6.40 | yes |
| ninja | 64 × 64 (ninja.cpp:36-37) | .5 (ninja.cpp:320-321) | 1.00 | 1.00 | **no** |
| plunder | 20 × 20 (plunder.cpp:37-38) | rx 1.5 easy (plunder.cpp:125, 180); ry from asset aspect | 3.20 | 9.60 (rx) | yes |
| starpilot | 16 × 16 (starpilot.cpp:52-53) | 0.4 default | 4.00 | 3.20 | yes |

- **Predicted outside the range:** caveflyer, climber, coinrun, fruitbot, jumper, ninja. These are the large-world games that scroll by default.
- **Confirmatory games in range (9):** bossfight, chaser, dodgeball, heist, leaper, maze, miner, plunder, starpilot. **Out of range (5):** caveflyer, climber, fruitbot, jumper, ninja.
- For bossfight and plunder, ry is set from the asset's aspect ratio (match_aspect_ratio) and was not computed from source; the span uses rx.
- **V1 and V2 on suite C are reported on all 14 confirmatory games, and again on the 9 in range** (analyze_common.IN_RANGE_C). The secondary condition center_on is reported on all 14.

## 5. The census

### 5.1 Definitions
The truth definitions of Section 7 are the definitions the census estimates.

### 5.2 Probe and budget
- The census is read from N's run: scripts/g_nav.py NavHook on the scripts/g_agent.py explorer, 20,000 actions per (game, seed), as in the ARC census v2 (scripts/g_census_table.py). There is no separate probe budget.
- The learning phase is bounded by LEARN_MAX presses per key. Every later observation comes from the same run.

### 5.3 Per-seed decision rules [registered here]
These rules are applied to NavHook.report() (scripts/g_nav.py:899-915) and implemented in scripts/analyze_common.py, `census_from_report`:
- **A1** holds iff some key's learned shift is not None and the tried keys' shifts are not all equal.
- **A2** holds iff some key was decided "accepted" (LEARN_AGREE agreeing presses with a 2:1 margin) and counters.avatar_found == 1.
- **A3** holds iff A2 holds and the level-1 fallback is not "mispredicted" or "localise_failed" (scripts/g_census_table.py:77). Suite B: evaluated separately in the raw and macro conditions.
- **A4** holds iff A3 holds and counters.wall_contradicted == 0. (Corrected before v1 tag: the earlier clause "at least one wall colour was learned" is dropped. On games whose only blocker is the world boundary no wall colour can be learned, and the truth table gives A4 holds there.)
- **A5** holds iff counters.goal_confirmed ≥ 1. It fails iff counters.goal_reached_no_end ≥ 1 and goal_confirmed == 0. It is undetermined otherwise.

**Game verdict:** the seed majority (analyze_common.majority). Holds if at least half the seeds say holds; else fails if at least half say fails; else undetermined. This follows the half-the-seeds convention of scripts/g_census_table.py:146,148.

### 5.4 Constants
From docs/PREREG_PARAMS.md, which copies them from source. Every value below was read at the commit named.

| constant | value | file:line | file's last commit |
|---|---|---|---|
| LEARN_AGREE | 3 | scripts/g_nav.py:55 | ccc4d57e26cdee73ea0eabdbd7d7fdfe847ed265 |
| 2:1 margin | `top[0][1] < 2 * top[1][1]` rejects | scripts/g_nav.py:756 | ccc4d57 |
| LEARN_MAX | 8 | scripts/g_nav.py:56 | ccc4d57 |
| MAX_STEP (learner) | 10 | scripts/g_nav.py:57 | ccc4d57 |
| MAX_STEP (motion detector) — defined independently, both registered | 10 | scripts/g_motion.py:17 | 378345f4e7f43e3ea2fedd65f8d23e84b41603c6 |
| BFS_NODES | 40000 | scripts/g_nav.py:54 | ccc4d57 |
| wall_min, deadly_min | 2, 2 | scripts/g_nav.py:113 | ccc4d57 |
| goal_tries | 6 | scripts/g_nav.py:113 | ccc4d57 |
| stall_steps, mispredict_max, block_steps, wait_max | 150, 8, 40, 12 | scripts/g_nav.py:114 | ccc4d57 |
| learn_tries | 12 — **no effect** (stored at :121, never read) | scripts/g_nav.py:114 | ccc4d57 |
| wall rule | walked × 8 ≤ wall | scripts/g_nav.py:233 | ccc4d57 |
| deadly / avoid-near rules | 10·d ≥ 3·(d + walked / near_safe) | scripts/g_nav.py:239, 217 | ccc4d57 |
| observed-press window | 150 per level | scripts/g_nav.py:493 | ccc4d57 |
| co-mover limits | 400 cells, half the colour, 4096 pairs, 70% match | scripts/g_nav.py:695, 699, 710 | ccc4d57 |
| avatar search limit | 40 × shape size | scripts/g_nav.py:722 | ccc4d57 |
| goal ring radius, hypotheses kept | 1, 6 | scripts/g_nav.py:876-877, 888 | ccc4d57 |
| min_cells | 2 | scripts/g_motion.py:20 | 378345f |
| per-colour cell limit, pair limit, match share | 600, 4096, 0.7 | scripts/g_motion.py:39, 46, 60 | 378345f |
| KEYS (ARC) | (1, 2, 3, 4, 5, 7) | scripts/g_control_probe.py:47 | 378345f |
| Config.avoid_death | True | scripts/g_agent.py:96 | 378345f |
| MODEL_FAILS; half-the-seeds rules | ("mispredicted", "localise_failed"); count × 2 ≥ n | scripts/g_census_table.py:77, 146, 148 | a6b315bdd077b8a254542a9441ce1781b82ce70c |

**Frozen by git blob hash** (git ls-files -s at commit 8d209b3; unchanged by this commit):

| file | blob hash |
|---|---|
| scripts/g_agent.py, the explorer (frozen whole; its constants are not listed one by one) | 72585a4dbb926d4512ff9596f58118a176bb0646 |
| scripts/g_nav.py | a8a7eb61e62a658c239b98e0224e3588a662d1a0 |
| scripts/g_motion.py | 14018512a5c6b0efc81aed61c5466654d338be0b |
| scripts/g_control_probe.py | d5ff2a4dc77b9e1148929e7db03fe99a9d2b0bf8 |
| scripts/g_nav_run.py | 2cc0146a697e525e5873d4e29cb80f4ae8bd6297 |
| scripts/g_census_table.py (the E6 category rule) | 488feaca9c10985c4d0ff62791ceb4fa6fa6b9a8 |

Any change to these files after the tag is a protocol change (Section 12).

## 6. Goal-identification cost G

**Hypothesis classes (prior-free, registered):**
- H_place(m): one hypothesis per reachable cell c, "the level ends when the controlled object enters c", plus h0, "level end is not a function of the controlled object's cell".
- H_feat(k): one hypothesis per observed feature value f, "the level ends when the controlled object enters a cell carrying f", plus h0.
- **[registered here]** A cell c is the controlled object's anchor, the top-left of its footprint (scripts/g_nav.py:60-61). F(c) is the set of colour indices under the footprint in the frame before entry, excluding the avatar's colours and the frame's most frequent colour (the rule of scripts/g_nav.py:870-873).

**Elimination:**
- A level end at c eliminates every place hypothesis except c, and every feature hypothesis outside F(c).
- An entry without a level end eliminates that cell's place hypothesis and, for H_feat, nothing.
- "Identified" means exactly one non-h0 hypothesis survives. h0 is the verdict when none survives.

**Measures:**
- **G_end** = the number of level ends until identified. It is ∞ if the verdict is h0 or the budget ends first.
- **G_act** = actions from level start to the first level end, divided by the distinct cells the controlled object has occupied by then. It is an identity used as a measurement, not a bound.
- Both are measured where A2 holds. Where A2 fails, G is recorded as undefined, not ∞.

**[registered here] Coverage policy.** G is computed on N's run. N's frontier rule is the coverage policy: go to the nearest position never stood on (scripts/g_nav.py:364-369). scripts/g_goal_cost.py (W2) adds a per-step log of (anchor cell, F(cell), level_end) to that run and computes G from it. It must not change any action N takes; this is checked by comparing its action sequence with N's at the same seed.

**Cited observations** (cite, do not prove; docs/PRIOR_ART_KILL.md C1, C2):
- Elimination per example over the place class is the singletons-plus-empty example of Goldman & Kearns 1995, Lemma 1.
- Elimination over H_feat is version-space candidate elimination (Mitchell 1982), bounded by the teaching-dimension count of Goldman & Kearns 1995.

**Scope.** An agent with visual priors or an LLM can identify the goal before any level end (Twin, arXiv:2608.14490). G is therefore a property of the registered prior-free class, not of frame-only agents in general.

## 7. Ground truth

- The V1 answer key and the per-game predictions are docs/GROUND_TRUTH_minigrid.md (suite B, 178 ids) and docs/GROUND_TRUTH_procgen.md (suite C, 16 games), committed before this file.
- For ARC, docs/GROUND_TRUTH_arc_train.md does not exist yet (preface).

**Definitions, verbatim from the truth tables:**
- A1 holds iff at least one action changes the rendered frame and different actions can change it differently.
- A2 holds iff exactly one rendered object's displacement is a deterministic function of the action (the agent).
- A3-raw: under the primitive action set (turn left, turn right, forward, pickup, drop, toggle, done), holds iff each action's displacement of the agent is constant across positions and facings. Expected false everywhere because forward depends on facing; record it from source, not by assumption.
- A3-macro: under the absolute-move macro (north, south, east, west, each a turn-to-face then forward), holds iff each macro's displacement is constant when unblocked.
- A4 holds iff every zero-displacement move is explained by the cell ahead holding an object that cannot be overlapped, and that set of blocking objects changes only through the agent's own actions (a door opened by toggle counts as agent-caused; an obstacle that moves on its own, as in Dynamic-Obstacles, fails A4; lava does not block, it terminates, so it is recorded under A5 and does not affect A4).
- A5 holds iff the episode terminates with success when the agent enters a specific cell, with no facing requirement and no non-move action; terminates-on-adjacency, terminates-on-pickup/drop/toggle/done, and terminates-on-facing all fail A5. Record the exact predicate and where it is evaluated (the env's step or the BabyAI verifier), with file and line.
- Termination by failure (lava, wrong object in Memory, max steps) is recorded in the predicate column and does not count as a level end.

Pixel-physics additions (suite C):
- A2 holds iff exactly one entity's motion is a deterministic function of the action (the agent); if the agent is present but other entities also respond to the action, say so and record A2 as failing.
- A3 holds iff each movement action, when unblocked, displaces the agent by a constant vector regardless of position and history. Velocity that persists across steps, acceleration, gravity, or a jump arc all fail A3. Record from source how the agent's position is updated per action (the velocity assignment, any gravity term, any momentum), and quote the line.
- A4 holds iff every zero-displacement move is explained by a fixed set of wall or obstacle cell types present at level start that changes only through the agent's own actions; an obstacle that moves on its own fails A4; an entity that kills on contact rather than blocking is recorded under the termination predicate and does not affect A4.
- A5 holds iff the level completes when the agent's position enters a specific region, with no other condition at that moment; a completion that requires collecting a set of items, defeating enemies, or surviving a duration fails A5; a completion that requires reaching a region only after a precondition has been met elsewhere (a gem behind a key) holds A5 with the precondition recorded.

**A5 decisions (RKM):** fruitbot **holds**; leaper **fails**.

**The 11 suite-B exclusions:**

| id | reason |
|---|---|
| MiniGrid-MultiRoom-N4-S5-v0 | superseded by v1 |
| MiniGrid-ObstructedMaze-1Q-v0 | superseded by v1 |
| MiniGrid-ObstructedMaze-2Dlhb-v0 | superseded by v1 |
| MiniGrid-ObstructedMaze-2Q-v0 | superseded by v1 |
| MiniGrid-ObstructedMaze-Full-v0 | superseded by v1 |
| MiniGrid-WFC-DungeonMazeScaled-v0, MiniGrid-WFC-MazeSimple-v0, MiniGrid-WFC-ObstaclesAngular-v0, MiniGrid-WFC-ObstaclesBlackdots-v0, MiniGrid-WFC-ObstaclesHogs3-v0, MiniGrid-WFC-RoomsFabric-v0 | not constructible: the installed minigrid 3.1.0 ships without wfc/patterns/*.png (FileNotFoundError; W0_CHECKS.md amendment (b)) |

## 8. Suites and splits

**ARC-AGI-3 (development instance; source-exposure rule in METHOD_BLUEPRINT.md 2.9):**
- Train: tu93 ls20 vc33 m0r0 ft09 lp85 lf52 dc22. All are source-exposed. V1 is run here, labelled development, once the ARC truth table exists.
- Held-out, 17: ar25 bp35 cd82 cn04 g50t ka59 r11l re86 s5i5 sb26 sc25 sk48 sp80 su15 tn36 tr87 wa30. Never opened. V2 is reported, not tested.
- Split file: docs/HELDOUT.md, SHA-256 8c07813ab01f5228a6af10f91771702dad0291f26b0f920892ef3a79763a122d.

**Suite B pilots (RKM):** MiniGrid-Empty-5x5-v0, MiniGrid-FourRooms-v0, MiniGrid-DoorKey-8x8-v0, MiniGrid-Dynamic-Obstacles-6x6-v0, MiniGrid-Fetch-5x5-N2-v0, BabyAI-GoToRedBallGrey-v0.

**Suite B confirmatory (161 = 178 − 11 excluded − 6 pilots).**
- Truth counts on this set:
  - A5 holds on 36 and fails on 125.
  - A4 fails on 5 (Dynamic-Obstacles).
  - A1, A2 and A3-macro hold on all 161, and A3-raw fails on all 161.
- The ids:

1. BabyAI-ActionObjDoor-v0
2. BabyAI-BlockedUnlockPickup-v0
3. BabyAI-BossLevel-v0
4. BabyAI-BossLevelNoUnlock-v0
5. BabyAI-FindObjS5-v0
6. BabyAI-FindObjS6-v0
7. BabyAI-FindObjS7-v0
8. BabyAI-GoTo-v0
9. BabyAI-GoToDoor-v0
10. BabyAI-GoToImpUnlock-v0
11. BabyAI-GoToLocal-v0
12. BabyAI-GoToLocalS5N2-v0
13. BabyAI-GoToLocalS6N2-v0
14. BabyAI-GoToLocalS6N3-v0
15. BabyAI-GoToLocalS6N4-v0
16. BabyAI-GoToLocalS7N4-v0
17. BabyAI-GoToLocalS7N5-v0
18. BabyAI-GoToLocalS8N2-v0
19. BabyAI-GoToLocalS8N3-v0
20. BabyAI-GoToLocalS8N4-v0
21. BabyAI-GoToLocalS8N5-v0
22. BabyAI-GoToLocalS8N6-v0
23. BabyAI-GoToLocalS8N7-v0
24. BabyAI-GoToObj-v0
25. BabyAI-GoToObjDoor-v0
26. BabyAI-GoToObjMaze-v0
27. BabyAI-GoToObjMazeOpen-v0
28. BabyAI-GoToObjMazeS4-v0
29. BabyAI-GoToObjMazeS4R2-v0
30. BabyAI-GoToObjMazeS5-v0
31. BabyAI-GoToObjMazeS6-v0
32. BabyAI-GoToObjMazeS7-v0
33. BabyAI-GoToObjS4-v0
34. BabyAI-GoToObjS6-v1
35. BabyAI-GoToOpen-v0
36. BabyAI-GoToRedBall-v0
37. BabyAI-GoToRedBallNoDists-v0
38. BabyAI-GoToRedBlueBall-v0
39. BabyAI-GoToSeq-v0
40. BabyAI-GoToSeqS5R2-v0
41. BabyAI-KeyCorridor-v0
42. BabyAI-KeyCorridorS3R1-v0
43. BabyAI-KeyCorridorS3R2-v0
44. BabyAI-KeyCorridorS3R3-v0
45. BabyAI-KeyCorridorS4R3-v0
46. BabyAI-KeyCorridorS5R3-v0
47. BabyAI-KeyCorridorS6R3-v0
48. BabyAI-KeyInBox-v0
49. BabyAI-MiniBossLevel-v0
50. BabyAI-MoveTwoAcrossS5N2-v0
51. BabyAI-MoveTwoAcrossS8N9-v0
52. BabyAI-OneRoomS12-v0
53. BabyAI-OneRoomS16-v0
54. BabyAI-OneRoomS20-v0
55. BabyAI-OneRoomS8-v0
56. BabyAI-Open-v0
57. BabyAI-OpenDoor-v0
58. BabyAI-OpenDoorColor-v0
59. BabyAI-OpenDoorDebug-v0
60. BabyAI-OpenDoorLoc-v0
61. BabyAI-OpenDoorsOrderN2-v0
62. BabyAI-OpenDoorsOrderN2Debug-v0
63. BabyAI-OpenDoorsOrderN4-v0
64. BabyAI-OpenDoorsOrderN4Debug-v0
65. BabyAI-OpenRedBlueDoors-v0
66. BabyAI-OpenRedBlueDoorsDebug-v0
67. BabyAI-OpenRedDoor-v0
68. BabyAI-OpenTwoDoors-v0
69. BabyAI-Pickup-v0
70. BabyAI-PickupAbove-v0
71. BabyAI-PickupDist-v0
72. BabyAI-PickupDistDebug-v0
73. BabyAI-PickupLoc-v0
74. BabyAI-PutNextLocal-v0
75. BabyAI-PutNextLocalS5N3-v0
76. BabyAI-PutNextLocalS6N4-v0
77. BabyAI-PutNextS4N1-v0
78. BabyAI-PutNextS5N1-v0
79. BabyAI-PutNextS5N2-v0
80. BabyAI-PutNextS5N2Carrying-v0
81. BabyAI-PutNextS6N3-v0
82. BabyAI-PutNextS6N3Carrying-v0
83. BabyAI-PutNextS7N4-v0
84. BabyAI-PutNextS7N4Carrying-v0
85. BabyAI-Synth-v0
86. BabyAI-SynthLoc-v0
87. BabyAI-SynthS5R2-v0
88. BabyAI-SynthSeq-v0
89. BabyAI-UnblockPickup-v0
90. BabyAI-Unlock-v0
91. BabyAI-UnlockLocal-v0
92. BabyAI-UnlockLocalDist-v0
93. BabyAI-UnlockPickup-v0
94. BabyAI-UnlockPickupDist-v0
95. BabyAI-UnlockToUnlock-v0
96. MiniGrid-BlockedUnlockPickup-v0
97. MiniGrid-DistShift1-v0
98. MiniGrid-DistShift2-v0
99. MiniGrid-DoorKey-16x16-v0
100. MiniGrid-DoorKey-5x5-v0
101. MiniGrid-DoorKey-6x6-v0
102. MiniGrid-Dynamic-Obstacles-16x16-v0
103. MiniGrid-Dynamic-Obstacles-5x5-v0
104. MiniGrid-Dynamic-Obstacles-8x8-v0
105. MiniGrid-Dynamic-Obstacles-Random-5x5-v0
106. MiniGrid-Dynamic-Obstacles-Random-6x6-v0
107. MiniGrid-Empty-16x16-v0
108. MiniGrid-Empty-6x6-v0
109. MiniGrid-Empty-8x8-v0
110. MiniGrid-Empty-Random-5x5-v0
111. MiniGrid-Empty-Random-6x6-v0
112. MiniGrid-Fetch-6x6-N2-v0
113. MiniGrid-Fetch-8x8-N3-v0
114. MiniGrid-GoToDoor-5x5-v0
115. MiniGrid-GoToDoor-6x6-v0
116. MiniGrid-GoToDoor-8x8-v0
117. MiniGrid-GoToObject-6x6-N2-v0
118. MiniGrid-GoToObject-8x8-N2-v0
119. MiniGrid-KeyCorridorS3R1-v0
120. MiniGrid-KeyCorridorS3R2-v0
121. MiniGrid-KeyCorridorS3R3-v0
122. MiniGrid-KeyCorridorS4R3-v0
123. MiniGrid-KeyCorridorS5R3-v0
124. MiniGrid-KeyCorridorS6R3-v0
125. MiniGrid-LavaCrossingS11N5-v0
126. MiniGrid-LavaCrossingS9N1-v0
127. MiniGrid-LavaCrossingS9N2-v0
128. MiniGrid-LavaCrossingS9N3-v0
129. MiniGrid-LavaGapS5-v0
130. MiniGrid-LavaGapS6-v0
131. MiniGrid-LavaGapS7-v0
132. MiniGrid-LockedRoom-v0
133. MiniGrid-MemoryS11-v0
134. MiniGrid-MemoryS13-v0
135. MiniGrid-MemoryS13Random-v0
136. MiniGrid-MemoryS17Random-v0
137. MiniGrid-MemoryS7-v0
138. MiniGrid-MemoryS9-v0
139. MiniGrid-MultiRoom-N2-S4-v0
140. MiniGrid-MultiRoom-N4-S5-v1
141. MiniGrid-MultiRoom-N6-v0
142. MiniGrid-ObstructedMaze-1Dl-v0
143. MiniGrid-ObstructedMaze-1Dlh-v0
144. MiniGrid-ObstructedMaze-1Dlhb-v0
145. MiniGrid-ObstructedMaze-1Q-v1
146. MiniGrid-ObstructedMaze-2Dl-v0
147. MiniGrid-ObstructedMaze-2Dlh-v0
148. MiniGrid-ObstructedMaze-2Dlhb-v1
149. MiniGrid-ObstructedMaze-2Q-v1
150. MiniGrid-ObstructedMaze-Full-v1
151. MiniGrid-Playground-v0
152. MiniGrid-PutNear-6x6-N2-v0
153. MiniGrid-PutNear-8x8-N3-v0
154. MiniGrid-RedBlueDoors-6x6-v0
155. MiniGrid-RedBlueDoors-8x8-v0
156. MiniGrid-SimpleCrossingS11N5-v0
157. MiniGrid-SimpleCrossingS9N1-v0
158. MiniGrid-SimpleCrossingS9N2-v0
159. MiniGrid-SimpleCrossingS9N3-v0
160. MiniGrid-Unlock-v0
161. MiniGrid-UnlockPickup-v0

**Suite C pilots (RKM):** coinrun, bigfish.

**Suite C confirmatory (14):** bossfight, caveflyer, chaser, climber, dodgeball, fruitbot, heist, jumper, leaper, maze, miner, ninja, plunder, starpilot. Truth counts on this set:

| | holds | fails |
|---|---|---|
| A2 | 6 | 8 |
| A3 | 2 | 12 |
| A4 | 13 | 1 |
| A5 | 6 | 8 |

**Pilot rules** (METHOD_BLUEPRINT.md 2.7):
- Pilot games are run before the confirmatory set and are excluded from every confirmatory analysis.
- The pilot may fix adapter bugs and the tile-size scaling rule (thresholds expressed as a multiple of tile size — the rule is registered, new constants are not).
- Every change is logged as a diff in PREREG v1.1, and nothing from a confirmatory game is run before v1.1 is tagged.
- The only exception is the registered W0 infrastructure checks (docs/W0_CHECKS.md), which ran random actions only.

## 9. Runs

### 9.1 Design
- **Seeds:** 1000–1009 (10) for every (agent, game).
- **Budget:** 20,000 actions per (game, seed) for every agent on every suite and condition. The only exception is a registered per-suite value forced by the fidelity script, registered once before the confirmatory run.
- **Suites and conditions:**
  - ARC: native.
  - B: raw and macro. The census is run in both conditions; the agents run in both.
  - C: center_off (primary) and center_on (secondary).
- **Agents:** R and N everywhere; I1 on ARC, and on B and C if adaptable (Section 2). **The census is taken from N's run counters** (Section 5).
- **E6, the ARC baseline:**
  - N with the v2 hook plus R, 25 games × 10 seeds × 20,000 actions, under the tagged code.
  - The category rule is frozen by the blob hash of scripts/g_census_table.py (Section 5.4).
  - The census v2 numbers (runs/census_v2.json) predate the repository and are development only.
- **G:** measured on every suite and condition by scripts/g_goal_cost.py (W2; Section 6).

### 9.2 Commands available at v1 (PowerShell, working directory D:\Research\arc3\repo)
E6 and R on ARC under the tagged code:

```powershell
cd D:\Research\arc3\repo
git checkout prereg-v1
cd scripts
D:\Research\arc3\brutus\.venv\Scripts\python.exe g_nav_run.py --games all --modes hash_state,nav --seeds 10 --budget 20000 --workers 8 --env-dir D:\Research\arc3\brutus\environment_files --tag prereg_e6_arc_25x10 --resume
```

- The rows are written to scripts/navrun_prereg_e6_arc_25x10.json, where the script writes its output. RKM moves the file to runs/.
- The hash_state rows must be identical to runs/navrun_e2_hash_25x10.json in every field except seconds. Runs are deterministic given the seed, so this is the check that the tagged code is the E2 code.
- Commands for suites B and C, I1 and G are added in PREREG v1.1 with the adapter scripts (W2).

### 9.3 Output schema [registered here]
One row per (suite, condition, agent, game, seed). Every run file is a JSON list of rows.

- **The ablate format of the ARC runs:** game, mode, seed, score, levels, level_log, card_levels, card_baseline. score and card_* are ARC-only and null on B and C.
- **Extended by:**

| field | type | meaning |
|---|---|---|
| suite | "arc" \| "minigrid" \| "procgen" | |
| condition | "native" \| "raw" \| "macro" \| "center_off" \| "center_on" | |
| agent | "R" \| "N" \| "I1" \| "G" | mode hash_state → R, nav → N, the I1 mode → I1, g_cost → G |
| actions | int | actions used |
| level1_completed | bool | at least one level end within the budget. On B a level end is an episode success; on C it is prev_level_complete == 1; on ARC it is levels ≥ 1 |
| level1_actions | int \| null | actions to the first level end |
| adapter | object | the adapter parameters used: palette ("native" \| "tile8" \| "rgb64"), n_colours (distinct palette indices seen), crop, grid [h, w], action_list (list), camera and level settings (suite C), the code blob hashes of the adapter and census files |
| census | object | N rows only: {A1..A5: "holds" \| "fails" \| "undetermined"} by Section 5.3, and the raw NavHook report under nav as in the ARC runs |
| G | object | G rows only: {defined: bool, G_end_place: int \| null, G_end_feat: int \| null, G_act: float \| null}; null G_end means ∞, null G_act means no level end |

- ARC rows written by scripts/g_nav_run.py, which lack suite, agent and census, are normalised by analyze_common.normalise, and the census is computed from the nav report by the same Section 5.3 rules.

## 10. Tests

**V1, instrument validity** (scripts/analyze_v1.py). Per suite, condition and assumption A1–A5, over the confirmatory games, the seed-majority census is compared with the truth (A3-raw truth for raw, A3-macro for macro):
- **PASS** if agreement ≥ 0.90 and κ ≥ 0.70.
- **FAIL** if agreement < 0.75.
- Otherwise neither.
- An "undetermined" census never agrees. For κ it is mapped to the value opposite the truth.
- **Constant-column rule (RKM):** Cohen's κ is computed only where both truth values have at least three games. Otherwise the test is the agreement rate alone, and PASS needs agreement ≥ 0.90.
- Where κ applies on the confirmatory sets:
  - suite B: A4 (5 fails) and A5;
  - suite C: A2 and A5.
  - Agreement only: suite B A1, A2, A3-raw and A3-macro; suite C A1, A3 and A4.
- Suite C is reported on all 14 games and again on the 9 in range.
- ARC V1 (8 train games, development) is computed once its truth table exists.

**V2, predictive validity** (scripts/analyze_v2.py). Per suite, condition and agent, over the confirmatory games:
- **Quantities per game:**
  - census score S = the number of A1–A5 whose seed-majority verdict holds (undetermined does not hold);
  - prediction P = A2 ∧ A3 ∧ A4 ∧ A5 hold;
  - **[registered here]** outcome Y = the agent completed level 1 in at least half of its 10 seeds.
- **Void precondition:** the share of games with Y = 1 must lie in [0.10, 0.90]. Outside that band the test is VOID for that agent and suite, reported as void and not as a pass.
- **Nuisance baseline B [registered here]:** a logistic regression of Y on grid area (h × w), action-list length and number of palette colours. The features are the per-game means over the agent's seeds, standardised; constant features are dropped. It is fitted in-sample by Newton/IRLS with an L2 ridge of 10⁻⁶ on the coefficients, and AUROC_B is the AUROC of its fitted probabilities.
- **AUROC(S → Y)** is the Mann–Whitney statistic with ties counted ½. Its 95% CI is the percentile interval of 2,000 bootstrap resamples of games with replacement. Resamples with one class only are skipped and counted. Seed 20260927 in 8 chunks (default_rng([20260927, k])) on a worker pool.
- **PASS** if AUROC ≥ 0.80, the CI lower bound is > 0.60, the balanced accuracy of P is ≥ 0.80, and AUROC − AUROC_B ≥ 0.10.
- **FAIL** if AUROC ≤ 0.65. Otherwise neither.
- **Evidence and suite-level failure:**
  - Evidence comes from R and I1. N's rows are reported as an instrument check.
  - **Suite-level FAIL** is decided by the evidence agents present and non-void (corrected before v1 tag):
    - if R and I1 are both non-void, both must have AUROC ≤ 0.65;
    - if only R is non-void (I1 absent or void), R alone decides: the suite FAILs if R's AUROC ≤ 0.65;
    - with no non-void evidence agent, the suite is not decidable.
    - Support still requires I1 to pass.
  - ARC held-out: reported, not tested.
- Suite C is reported on all 14 games and again on the 9 in range. B is tested in the macro condition; the raw condition is reported.

*Power on suite C (recorded before any run).* Suite C has 14 confirmatory games, 9 of them in the operating range. With games as the unit, the bootstrap CI of AUROC over 14 games, let alone 9, is wide. The criterion "CI lower bound > 0.60" is therefore demanding at this size: a suite-C AUROC well above 0.80 can still fail to PASS on the CI alone. This was known before any run, and the thresholds are kept unchanged. A suite-C result that is not a PASS only because of the CI criterion is reported as such, with the interval.

**V3, parameter transfer.** Every census constant and frozen blob hash of Section 5.4 is identical on every suite (checked from the adapter and code fields of every row). Any re-tuning downgrades the claim to "after re-tuning on suite X".

**G** (scripts/analyze_g.py) is reported per game and suite, with no threshold.

**Outcome and venue, pre-committed** (METHOD_BLUEPRINT.md Section 4; decided at gate G3 before any results text is written):
- **Support:** V1 passes on B (both conditions) and C, V2 passes for R and I1 on B-macro and C (not void), and V3 holds.
- **Partial:** V1 passes everywhere, but V2 passes on B-macro only or is void on C, or passes on C for R only.
- **Refute:** V1 fails on any suite, or V2 fails on B-macro, or V2 is void on every suite.

| outcome | venue |
|---|---|
| Support | JAIR full article |
| Partial | IEEE Transactions on Games full paper |
| Refute | repository record only, at most an arXiv note |

## 11. Analysis code

**Scripts.** Each reads run files under runs/ and writes a table as markdown and JSON under docs/tables/:
- scripts/analyze_common.py (shared; census rules, statistics);
- scripts/analyze_v1.py → docs/tables/v1.md, docs/tables/v1.json;
- scripts/analyze_v2.py → docs/tables/v2.md, docs/tables/v2.json;
- scripts/analyze_g.py → docs/tables/g.md, docs/tables/g.json.

The bootstrap runs on a worker pool (--workers).

**Synthetic tests**, whose expected numbers are computed by hand in each file's docstring:
- scripts/test_analyze_v1.py (4 tests, including the Section 5.3 census rules);
- scripts/test_analyze_v2.py (5 tests);
- scripts/test_analyze_g.py (2 tests).

All eleven passed on 27 Sep 2026 (after the pre-tag corrections) without reading any runs/ file or playing any game.

The analysis code is frozen at the tag. The only permitted change is a crash fix, logged in Section 13.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\test_analyze_v1.py
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\test_analyze_v2.py
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\test_analyze_g.py
```

## 12. Amendment rules

- PREREG changes only by a new version (v1.1, v1.2, …), each carrying a dated diff section that lists every changed line and why.
- The pilot may change adapter code and the tile-size scaling rule, never a census constant, a threshold, a truth-table entry or a frozen blob hash.
- Every change is logged. A test that was not in the tagged version before its run is exploratory and enters no claim.

## 13. Diff section

Empty in v1.

---
---

# PREREG.md — v1.1 (DRAFT — not registered until tagged prereg-v1.1 after the pilot)

Drafted 27 September 2026 after the tag prereg-v1 (commit 19f2a9f), from RKM's decisions on docs/ADAPTER_FEASIBILITY.md Section 2.
- Version v1 above is the registered protocol; this block changes it only where the diff section below says so.
- The pilot (Section 8) runs under this draft. It may still change adapter code and the tile-size scaling rule, never a census constant, threshold, truth-table entry or frozen blob hash.
- Every change made before the tag is added to this diff section.

## Diff section (v1 → v1.1)

**D1. The six-action limit of the frozen code** (new; Section 3). The frozen explorer presses only ARC action ids 1, 2, 3, 4, 5 and 7 as keys (g_agent.py:326; g_nav.py:379; g_control_probe.py:47). Id 6 is a click, and the runner never offers it. Every suite is therefore presented through a key map of at most six actions, applied by the ARC shim (scripts/env_frame.py `KEY_MAPS`):

| suite, condition | 1 | 2 | 3 | 4 | 5 | 7 | not exposed |
|---|---|---|---|---|---|---|---|
| B raw (Section 3.2 changed) | left | right | forward | pickup | drop | toggle | done |
| B macro (Section 3.2 changed) | north | south | west | east | pickup | toggle | drop, done |
| C center_off / center_on (Section 3.3 changed) | action 5 (up) | action 3 (down) | action 1 (left) | action 7 (right) | action 9 (special 1) | action 10 (special 2) | the diagonals 0, 2, 6, 8; the no-op 4; specials 11–14 |

- On Dynamic-Obstacles only left, right and forward (raw) or the four macros exist.
- Section 3.3's "action list: all 15 actions" becomes these six for every agent. The adapter keeps all 15 internally, and the fidelity check exercises all 15.

**D2. Canvas placement** (new; Section 3.2). A suite-B grid is placed at rows 1..h, columns 0..w−1 of a 64 × 64 canvas; every other cell holds palette index 0, reserved as padding (adapter palettes start at 1). Reason: the frozen code reads rows 1–62 only and anchors the frame at the top-left (g_control_probe.py:50-56; g_motion.py:30-31).

**D3. Procgen rows 0 and 63** (new; Section 3.3). The 64 × 64 Procgen grid fills the canvas, and the frozen code does not see its top and bottom pixel rows. This is recorded, not corrected. No rescaling is applied.

**D4. RESET semantics per suite** (Section 3.2 changed; Section 3.3 new).
- Suite B, "replay": episode k is reset with seed seed·100000 + k; k advances only on a success; a RESET (the explorer's stuck rule, or the RESET after a failure) replays episode k's layout. This replaces v1's "later resets are unseeded".
- Suite C: a RESET takes no step and returns the current grid, because procgen cannot restart a level. It still counts as an action.
- **The sentence the paper carries:** *"The ARC RESET restarts the current level on ARC-AGI-3 and replays the current layout on MiniGrid/BabyAI, but is a no-op on Procgen, which cannot restart a level; on Procgen a failed level is followed by a new level."*

**D5. Wall-clock cap** (new; Section 9.1).
- The cap per run is three times the slowest game's measured time for 20,000 actions in that suite. That time is computed from the fidelity check's steps per second (runs/fidelity), and the cap is one value per suite. **Value pending: filled in after the fidelity check.**
- Rows cut by the cap (actions < budget) are kept, marked cut_by_cap, and reported as cut.

**D6. The runner** (new; Section 9.2).
- scripts/run_suite.py is the registered runner for suites B and C. It installs the shim with D1–D4. It calls R and N exactly as scripts/g_nav_run.py does (Config(max_actions=20000, seed=s, **MODES[mode]); g_nav.play for nav, g_agent.play for hash_state). Before playing, it refuses to run if any of the six frozen blob hashes differs from Section 5.4.
- Rows are written to runs/suites/<suite>/<condition>/<mode>/<game>__<seed>.json in the Section 9.3 schema.
- Blob hashes at this draft (re-recorded at the v1.1 tag):

| file | blob hash |
|---|---|
| scripts/run_suite.py | d51f56edbe7e9a69497c123864d1df96383874f6 |
| scripts/env_frame.py | bb3ff60acf88c220ec64e287c6c1d6bb899f879b |
| scripts/adapter_minigrid.py | 370028ab178eaed65803d2f0f7d86c29adf14328 |
| scripts/adapter_procgen.py | 91cca0f59ea632da8b5b0f6652c7b1a13f1fbb3d |
| scripts/i1_suite_adapter.py | 9d8a18548b958e70b1365b2eacb25d25f83284ba |
| scripts/fidelity_check.py | 9e483f2ca2fb33bdeaaaa404166fcdca8c1740f7 |

**D7. I1 boundary on suites B and C** (Section 2 extended). scripts/i1_suite_adapter.py applies C1–C5 of docs/I1_feasibility.md around the unchanged scripts/e1_rudakov_adapter.py (blob 39ab52f82f2fef3460ce83cb9db30d892b571d5b):
- C1: the shim;
- C2: the suite key map restricted to ids 1–5 (I1 maps only ACTION1–5);
- C3: palette indices ≥ 16 presented as k + 1, since 16 is their status-bar marker;
- C4: level count seen by I1 capped at 254, with the true count kept in the row;
- C5: B1–B7 unchanged.

Consequences:
- I1 lacks toggle in both suite-B conditions and special 2 on suite C.
- Their code needs requests 2.34.2 and pydantic 2.13.5, the versions of the ARC venv, installed in the suite venvs as an infrastructure step (docs/W2_COMMANDS.md).

**D8. The fidelity check** (Section 8 exception extended). The fidelity check (scripts/fidelity_check.py; Section 2.1 of METHOD_BLUEPRINT.md) is an infrastructure check under the Section 8 exception, like the W0 checks. It plays every game with 200 random actions twice, with no census and no agent, and produces infrastructure facts only.

**D9. V2 exclusions** (Section 10 changed).
- V2's primary analysis excludes confirmatory environments whose success predicate requires an action absent from the condition's key map (D1). A secondary line reports V2 with them included.
- V1 is unaffected: the truth of A1–A5 does not depend on the key map.
- The list below is derived from the truth table's success predicates (docs/GROUND_TRUTH_minigrid.md, with file and line there):
  - **Suite B raw (done absent) — 5:** MiniGrid-GoToDoor-5x5-v0, MiniGrid-GoToDoor-6x6-v0, MiniGrid-GoToDoor-8x8-v0, MiniGrid-GoToObject-6x6-N2-v0, MiniGrid-GoToObject-8x8-N2-v0. Their success is a done action beside the target (gotodoor.py:144-147; gotoobject.py:155-158).
  - **Suite B macro (drop and done absent) — 27:**
    - The 5 above.
    - Success on a drop (PutNear, putnear.py:193-197; PutNextInstr, verifier.py:411-435; MoveTwoAcross, BeforeInstr of two PutNextInstr, other.py:423-426) — 15: MiniGrid-PutNear-6x6-N2-v0, MiniGrid-PutNear-8x8-N3-v0, BabyAI-PutNextLocal-v0, BabyAI-PutNextLocalS5N3-v0, BabyAI-PutNextLocalS6N4-v0, BabyAI-PutNextS4N1-v0, BabyAI-PutNextS5N1-v0, BabyAI-PutNextS5N2-v0, BabyAI-PutNextS5N2Carrying-v0, BabyAI-PutNextS6N3-v0, BabyAI-PutNextS6N3Carrying-v0, BabyAI-PutNextS7N4-v0, BabyAI-PutNextS7N4Carrying-v0, BabyAI-MoveTwoAcrossS5N2-v0, BabyAI-MoveTwoAcrossS8N9-v0.
    - LevelGen levels whose instruction may be a PutNext (action kinds include putnext, levelgen.py:41; synth.py:91, 173 and defaults) — 7: BabyAI-Synth-v0, BabyAI-SynthS5R2-v0, BabyAI-SynthLoc-v0, BabyAI-SynthSeq-v0, BabyAI-MiniBossLevel-v0, BabyAI-BossLevel-v0, BabyAI-BossLevelNoUnlock-v0. Excluded because the predicate can require the absent action.
  - **Suite C — none.** No Procgen success predicate requires a diagonal or specials 11–14. Special 1 (fire), which bossfight, dodgeball and plunder need, is mapped.
- **Code change:** scripts/analyze_v2.py gains these lists, implemented and tested at the v1.1 tag. The v1 script is otherwise unchanged. I1's narrower key map (D7) is not an exclusion criterion; its effect is reported per suite.

**D10. Section 3.2 seeding text** is replaced by D4. Section 9.2 gains the run_suite.py commands (docs/W2_COMMANDS.md blocks B and C).
