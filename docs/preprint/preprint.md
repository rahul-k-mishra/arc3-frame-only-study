# A pre-registered test of a frame-only assumption census on MiniGrid/BabyAI and Procgen: the instrument failed its validity test

**Rahul Kumar Mishra**
Independent Researcher, Ranchi, Jharkhand, India
ORCID 0009-0004-9671-4055

Draft 2, 14 October 2026.

**How to read the citations.**
- Every number in this paper names the file it comes from, in the project repository (Section 9).
- "PREREG" means docs/PREREG.md, which holds the registered protocol in three versions (v1, v1.1, v1.2).
- "STATE (x)" means amendment (x) of docs/STATE.md, the project's dated log.

---

## 1. Summary

A method was registered before any confirmatory run. A fixed battery of frame-only probes, called the assumption census, was to report five mechanical assumptions of an unseen game, A1 to A5. It was to do so accurately against truth derived from each game's source code, which is test V1, and in a way that predicts, before any agent runs, which games a class of assumption-driven frame-only agents complete the first level of, which is test V2. Every parameter was frozen on eight ARC-AGI-3 games. The protocol was registered on 27 September 2026 as git tag prereg-v1 and on OSF (osf.io/2znhw). After a pilot on registered pilot games only, it was amended as prereg-v1.1 (osf.io/zu5vq).

The census and three agents were then run on 161 MiniGrid/BabyAI environments in two action conditions and on 14 Procgen games in two camera conditions, with 10 seeds and 20,000 actions per run (PREREG v1 Section 9.1): 10,500 rows in all (STATE (i), (j)).

By the registered outcome table (PREREG v1 Section 10), the result is REFUTE. V1 failed on both suites: on MiniGrid/BabyAI for three of five assumptions under absolute moves and four of five under primitive actions, and on Procgen for four of five (docs/tables/v1.md). No agent passed V2 on any suite (docs/tables/v2.md). The registered consequence of REFUTE is a repository record and at most a preprint, and this paper is that preprint.

The protocol, code, truth tables, run rows, tables and log are in the repository, under the tags named in Section 2. Section 6 adds an exploratory diagnosis of why V1 failed, marked as such.

This paper does not show that frame-only agents fail on these suites, nor that the assumptions are wrong about the games. It shows that this census, as registered, does not measure them.

## 2. The claim and the pre-registration

This section gives the claim as registered, where and when it was registered, and how the protocol changed afterwards. It does not argue for the claim.

**The claim, verbatim from the v1 registration** (docs/OSF_REGISTRATION_final.txt):

> **Claim.** A fixed, cheap, frame-only probe battery (the assumption census: A1 input coupling, A2 one controlled object, A3 lattice motion, A4 blocking by a fixed obstacle set, A5 place goal), with every parameter frozen on eight ARC-AGI-3 training games, (i) reports the ground-truth mechanics of unseen games at a registered accuracy, and (ii) predicts, before any agent is run, on which unseen games assumption-driven frame-only agents complete the first level. Ground truth is derived from each game's source code and committed before any run. A goal-identification cost G is measured and reported alongside, not tested. ARC-AGI-3 is the development instance and does not count toward generality.

**Registrations and tags.** Tag dates come from the annotated tag objects (`git cat-file -p <tag>`), in IST.

| version | git tag | commit | tag date | OSF |
|---|---|---|---|---|
| v1 | prereg-v1 | 19f2a9f25043997d1deffd5976f2f2150e5f086f | 27 Sep 2026 07:41 | https://osf.io/2znhw, open-ended registration, recorded 27 Sep 2026 (STATE (d)); embargoed until 30 June 2030 |
| v1.1 | prereg-v1.1 | 8b2b2b9b432dbea4ba5f62cfceb1aad5558d1ecc | 27 Sep 2026 23:16 | https://osf.io/zu5vq, open-ended registration from project https://osf.io/29eas, recorded 27 Sep 2026 (STATE (h)); embargo until 30 June 2030 confirmed on the registration page (STATE (i)) |
| v1.2 | prereg-v1.2 | 66e560645d9d98bca39ee7da9b1039ada1bc579b | 13 Oct 2026 21:21 | none recorded in docs/STATE.md; v1.2 is registered by its git tag |

**The rule after each tag.**
- After a tag, the protocol changed only by a new version with a dated diff section (PREREG v1 Section 12).
- No threshold, parameter, exclusion list, truth-table entry or analysis script was changed after prereg-v1.1. `git diff prereg-v1.1` over scripts/, docs/PREREG.md and the two truth tables is empty at the commit that recorded the outcome (STATE (k)).
- v1.2 adds one entry, D16, written after the outcome. It withdraws an unmeasured quantity (G) and changes no test.

**The amendment trail.**
- D1 to D15 form the v1.1 diff, written in two dated revisions of 27 September 2026 (STATE (f), (g)) before the v1.1 tag. D16 is v1.2, written on 13 October 2026.
- Every confirmatory run was made after the v1.1 tag. The only earlier contact with confirmatory games was the infrastructure checks of D8, which play random actions and compute no census or test statistic.
- Appendix A gives each entry in full.

| entry | what it registers |
|---|---|
| D1 | at most six actions per suite, through fixed key maps (ARC ids 1, 2, 3, 4, 5, 7) |
| D2 | MiniGrid/BabyAI grids placed on a 64 × 64 canvas, padding index 0 |
| D3 | Procgen top and bottom pixel rows not seen; recorded, not corrected |
| D4 | what RESET does per suite (replay on MiniGrid/BabyAI, no-op on Procgen) |
| D5 | wall-clock cap per run: 3300 s on MiniGrid/BabyAI, 7500 s on Procgen, from the pilot |
| D6 | the registered runner, which refuses to run if a frozen file changed |
| D7 | the boundary for the independent agent I1: five keys only |
| D8 | infrastructure checks (fidelity, pilot rows, camera, determinism) |
| D9 | V2 exclusions for R and N, read as reachability; Playground added |
| D9b | V2 exclusions for I1's own key map |
| D10 | MiniGrid/BabyAI seeding text replaced by D4 |
| D11 | blob hashes of the analysis scripts at the tag |
| D12 | ARC wall-clock cap of 3600 s, and the re-run of eight cut ARC rows |
| D13 | Procgen camera identity: the secondary condition differs on five games only |
| D14 | no adapter change after the pilot |
| D15 | G from a separately registered replay (withdrawn by D16) |
| D16 | G not measured |

**What this section does not show.** That the registrations were reviewed by anyone. OSF registrations are self-registered and were not peer-reviewed.

## 3. The instrument

This section describes the census exactly as registered: what it reads, what it decides, and where its parameters come from. It does not claim that these choices were good.

**3.1 What the census reads.**
- The census reads frames only: no reward, no symbolic state, no text (PREREG v1 Section 3).
- It is read from the run of the planner N (Section 4.3). N is G-NAV, scripts/g_nav.py on the explorer scripts/g_agent.py, run for 20,000 actions per (game, seed) (PREREG v1 Section 5.2).
- Its report, NavHook.report() (scripts/g_nav.py:899-915), holds:
  - the learned step vector of each key;
  - counters such as avatar_found, wall_contradicted, goal_confirmed and goal_reached_no_end;
  - the planner's reason for stopping planning on level 1 (the "level-1 fallback").

**3.2 The five decisions per seed, as registered** (PREREG v1 Section 5.3; scripts/analyze_common.py, `census_from_report`).
- **A1** (input coupling) holds iff some key's learned shift is not None and the tried keys' shifts are not all equal.
- **A2** (one controlled object) holds iff some key was decided "accepted" (3 agreeing presses with a 2:1 margin) and avatar_found = 1.
- **A3** (lattice motion) holds iff A2 holds and the level-1 fallback is not "mispredicted" or "localise_failed".
- **A4** (blocking by a fixed obstacle set) holds iff A3 holds and wall_contradicted = 0.
- **A5** (place goal) holds iff goal_confirmed ≥ 1. It fails iff goal_reached_no_end ≥ 1 and goal_confirmed = 0. It is undetermined otherwise.
- **The game verdict is the seed majority:** holds if at least half the seeds say holds; else fails if at least half say fails; else undetermined (`majority`).

**3.3 Frozen parameters** (PREREG v1 Section 5.4, copied there from source with file, line and commit):

| constant | value | file:line | commit |
|---|---|---|---|
| LEARN_AGREE | 3 | scripts/g_nav.py:55 | ccc4d57 |
| 2:1 margin | `top[0][1] < 2 * top[1][1]` rejects | scripts/g_nav.py:756 | ccc4d57 |
| LEARN_MAX | 8 | scripts/g_nav.py:56 | ccc4d57 |
| MAX_STEP (learner; motion detector) | 10; 10 | scripts/g_nav.py:57; scripts/g_motion.py:17 | ccc4d57; 378345f |
| BFS_NODES | 40000 | scripts/g_nav.py:54 | ccc4d57 |
| wall_min, deadly_min, goal_tries | 2, 2, 6 | scripts/g_nav.py:113 | ccc4d57 |
| stall_steps, mispredict_max, block_steps, wait_max | 150, 8, 40, 12 | scripts/g_nav.py:114 | ccc4d57 |
| min_cells (motion) | 2 | scripts/g_motion.py:20 | 378345f |
| KEYS | (1, 2, 3, 4, 5, 7) | scripts/g_control_probe.py:47 | 378345f |

**The six frozen files.** Their git blob hashes are checked by the runner before any run (PREREG v1 Section 5.4; v1.1 D6):

| file | blob |
|---|---|
| scripts/g_agent.py | 72585a4dbb926d4512ff9596f58118a176bb0646 |
| scripts/g_nav.py | a8a7eb61e62a658c239b98e0224e3588a662d1a0 |
| scripts/g_motion.py | 14018512a5c6b0efc81aed61c5466654d338be0b |
| scripts/g_control_probe.py | d5ff2a4dc77b9e1148929e7db03fe99a9d2b0bf8 |
| scripts/g_nav_run.py | 2cc0146a697e525e5873d4e29cb80f4ae8bd6297 |
| scripts/g_census_table.py | 488feaca9c10985c4d0ff62791ceb4fa6fa6b9a8 |

**3.4 Development on ARC-AGI-3.**
- The census and its constants were developed on the eight ARC-AGI-3 training games tu93, ls20, vc33, m0r0, ft09, lp85, lf52 and dc22 (PREREG v1 Section 8).
- The other 17 public games were never opened at source.
- **No ARC truth table was written.** The PREREG v1 preface records that none exists for the eight train games. V1 was therefore never computed on ARC.
- The registered ARC baseline E6 ran on all 25 games, with both agents, 10 seeds and 20,000 actions, under the tag (STATE (e), (h)). Its per-game census table is docs/census_e6.md, with the wording note docs/census_e6_NOTE.md.

**3.5 How the suites are presented** (PREREG v1.1 D1, D2, D3; PREREG v1 Section 3).
- **Key maps (D1).** The frozen code presses ARC ids 1, 2, 3, 4, 5 and 7 only, so every suite is presented through a map of at most six actions:
  - MiniGrid/BabyAI primitive ("raw"): left, right, forward, pickup, drop, toggle;
  - absolute-move ("macro"): north, south, west, east, pickup, toggle;
  - Procgen: up, down, left, right, special 1, special 2.
  - An environment with fewer actions keeps only those it has. Dynamic-Obstacles has three under raw and four under macro.
- **Palette and canvas (D2; Section 3).**
  - MiniGrid/BabyAI frames are cut into 8 × 8 tiles. Each distinct tile pattern gets an integer index, with the four agent orientations merged into one.
  - The grid is placed at rows 1 to h of a 64 × 64 canvas, padding index 0.
  - Procgen frames are 64 × 64 RGB, mapped to indices by exact colour, capped at 64.
  - The frozen code reads rows 1 to 62 only. On Procgen it does not see the top and bottom pixel rows (D3).
- **Operating range (PREREG v1 Section 4).** With center_agent off, Procgen draws the whole level into 64 pixels. The census detects motion only when at least 2 cells change. The registered operating range is the set of games whose agent spans at least 2 pixels: 9 of the 14 confirmatory games (bossfight, chaser, dodgeball, heist, leaper, maze, miner, plunder, starpilot).
- **Camera identity (D13).**
  - In the Procgen source at tag 0.10.7, ten games set center_agent false inside their own game_reset. In easy mode, nine of them are confirmatory games, and they are exactly the nine in the operating range.
  - On those nine the secondary condition (center_agent on) draws the same frames as the primary one. A camera check found 401 of 401 identical frames on those ten, and a difference from the first frame on the other six (runs/pilot_checks/procgen_camera_check.json).
  - The secondary condition is therefore distinct only on caveflyer, climber, fruitbot, jumper and ninja. It is reported there, and not tested.

**What this section does not show.** That the census measures the five assumptions. That is what V1 tests (Section 5).

## 4. The protocol

This section describes what was run, on what, and with which checks. Results are in Section 5.

**4.1 Suites and splits** (PREREG v1 Section 8).

| suite | development / pilot | confirmatory |
|---|---|---|
| ARC-AGI-3 public set (arc-agi 0.9.8, arcengine 0.9.3) | 8 train games (development) | 17 held-out games: V2 reported, not tested |
| MiniGrid/BabyAI (minigrid 3.1.0; BabyAI: Chevalier-Boisvert et al., 2019) | 6 pilots | 161 environments, raw and macro |
| Procgen 0.10.7 (Cobbe et al., 2020), easy, sequential levels | 2 pilots (coinrun, bigfish) | 14 games, center_off (primary) and center_on (secondary; 5 camera-distinct games, D13) |

- Suite B's 161 are its 178 registered ids, minus 11 excluded (5 superseded versions, 6 WFC presets the installed package cannot build), minus the 6 pilots (PREREG v1 Sections 7 and 8).
- Suite C's 14 are its 16 games minus the 2 pilots (PREREG v1 Section 8).

**4.2 Truth from source.**
- docs/GROUND_TRUTH_minigrid.md and docs/GROUND_TRUTH_procgen.md give one line per environment, with the file and line of the installed or tagged source behind each A1–A5 entry. Both were committed before the v1 tag (PREREG v1 Section 7).
- Truth counts on the confirmatory sets (PREREG v1 Section 8):
  - suite B: A1, A2 and A3-macro hold on all 161; A3-raw fails on all 161; A4 fails on 5; A5 holds on 36;
  - suite C: A2 holds on 6 of 14, A3 on 2, A4 on 13, A5 on 6.

**4.3 Agents** (PREREG v1 Section 2; v1.1 D7).
- **R**, the explorer: scripts/g_agent.py, mode hash_state. Evidence for V2.
- **N**, the planner G-NAV. It uses A1–A5 by construction, so its V2 lines are an instrument check only. Its runs supply the census.
- **I1**, the graph-based explorer of Rudakov, Shock and Cowley (arXiv:2512.24156; MIT licence), unchanged behind a boundary adapter. Evidence for V2.
  - I1's own code maps five actions, so it sees ids 1 to 5 only: no toggle on suite B, no special 2 on Procgen (D7).

**4.4 V2 exclusions** (PREREG v1.1 D9, D9b; scripts/analyze_common.py).
- V2's primary line excludes, per agent, every environment where success cannot be reached on any seed without an action missing from that agent's key map.
- "Cannot be reached" is read as reachability: the action either triggers success, or is a precondition of every successful episode. Examples are a locked door on every path, or a key that must be put down before the target can be picked up.
- MiniGrid-Playground-v0 has no success at all and is excluded for every agent.

| agent | raw: excluded / primary games | macro: excluded / primary games |
|---|---|---|
| R and N | 6 / 155 | 49 / 112 |
| I1 | 63 / 98 | 78 / 83 |

- Procgen has no exclusion.
- The lists, with their source reasons, are in Appendix B and PREREG v1.1 D9 and D9b.

**4.5 Seeds, budget, caps.**
- Seeds 1000 to 1009 and 20,000 actions per (agent, game, seed, condition) (PREREG v1 Section 9.1).
- The per-run wall-clock cap (D5) is three times the longest pilot run, rounded up to a whole minute:
  - suite B: 3300 s (longest pilot run 1081.6 s, MiniGrid-FourRooms-v0, raw, I1, seed 1003);
  - suite C: 7500 s (longest 2481.5 s, bigfish, center_off, I1, seed 1003) (runs/pilot_checks/pilot_check.json; PREREG v1.1 D5).
- **No confirmatory row was cut.** Suite B has 9,660 of 9,660 rows and suite C 840 of 840, with 0 errors and 0 cut by the cap (STATE (i), (j)).

**4.6 Checks before and after the runs** (PREREG v1.1 D8).
- **Fidelity check.** 200 random actions twice per game and condition. Suite B: 334 of 334 identical. Suite C: 32 of 32 (STATE (f); commit 51eba49).
- **Pilot.**
  - 360 suite-B and 120 suite-C rows, on the pilot games only. Every row reached 20,000 actions, and no row carries an error (runs/pilot_checks/pilot_check.json).
  - I1 completed no level on MiniGrid-DoorKey-8x8-v0 in any of its 20 rows, which led to D9b (same file).
  - A projection from fidelity speed plus the largest pilot agent overhead put no confirmatory run over its cap. The largest projections were 1517.8 s (suite B) and 2550.0 s (suite C) (same file).
- **Camera check.** As in Section 3.5 (runs/pilot_checks/procgen_camera_check.json).
- **Determinism check.** On the nine identical-frame Procgen games, each center_on row equals its center_off row in every field except timing and the condition labels: 270 of 270 pairs, 0 differing, 0 missing (runs/checks/determinism_check.json).
- **Synthetic tests of the analysis code.** 20 of 20 pass under the tag, with warnings as errors (STATE (k)).

**4.7 A lesson recorded after the outcome** (STATE (k)).
- The pilot rows contained census vectors for eight games that have truth-table entries.
- A V1-style comparison on them before the v1.1 tag would have shown the instrument failure before the confirmatory runs.
- That comparison was not registered and was not done.

**What this section does not show.** That the protocol's choices (key maps, palette, exclusion reading) were the best available. They were registered, and they are what was tested.

## 5. Results (registered)

This section reports the registered tests exactly as the tagged analysis code wrote them. It adds no interpretation beyond the registered verdict rules, which are those of PREREG v1 Section 10.

V1 passes for an assumption when the agreement between census and truth is at least 0.90 and κ is at least 0.70, and fails when agreement is below 0.75; anything between is "neither". κ is computed only where both truth values have at least 3 games. An "undetermined" census verdict never counts as agreement, and for κ it is mapped to the value opposite the truth. V2 passes for an agent when four conditions all hold: AUROC is at least 0.80, the lower bound of its bootstrap confidence interval is above 0.60, the balanced accuracy of the conjunctive prediction is at least 0.80, and AUROC exceeds the nuisance baseline's by at least 0.10. V2 fails when AUROC is at most 0.65, and it is void when the share of games completed lies outside [0.10, 0.90].

**Table 1. V1, docs/tables/v1.md verbatim** (commit bb0f1a1; written by scripts/analyze_v1.py at prereg-v1.1):

| suite | condition | subset | assumption | n | truth_holds | agreement | kappa | verdict |
|---|---|---|---|---|---|---|---|---|
| minigrid | macro | all | A1 | 161 | 161 | 0.9876 |  | PASS |
| minigrid | macro | all | A2 | 161 | 161 | 0.9876 |  | PASS |
| minigrid | macro | all | A3 | 161 | 161 | 0.4286 |  | FAIL |
| minigrid | macro | all | A4 | 161 | 156 | 0.3354 | -0.0435 | FAIL |
| minigrid | macro | all | A5 | 161 | 36 | 0.2671 | -0.4125 | FAIL |
| minigrid | raw | all | A1 | 161 | 161 | 0.9379 |  | PASS |
| minigrid | raw | all | A2 | 161 | 161 | 0.4596 |  | FAIL |
| minigrid | raw | all | A3 | 161 | 0 | 0.5466 |  | FAIL |
| minigrid | raw | all | A4 | 161 | 156 | 0.0621 | 0.0021 | FAIL |
| minigrid | raw | all | A5 | 161 | 36 | 0.0994 | -0.3374 | FAIL |
| procgen | center_off | all | A1 | 14 | 14 | 0.9286 |  | PASS |
| procgen | center_off | all | A2 | 14 | 6 | 0.5714 | 0.2222 | FAIL |
| procgen | center_off | all | A3 | 14 | 2 | 0.5714 |  | FAIL |
| procgen | center_off | all | A4 | 14 | 13 | 0.0714 |  | FAIL |
| procgen | center_off | all | A5 | 14 | 6 | 0.0714 | -0.7843 | FAIL |
| procgen | center_off | in_range | A1 | 9 | 9 | 0.8889 |  | neither |
| procgen | center_off | in_range | A2 | 9 | 4 | 0.4444 | 0.0000 | FAIL |
| procgen | center_off | in_range | A3 | 9 | 2 | 0.4444 |  | FAIL |
| procgen | center_off | in_range | A4 | 9 | 8 | 0.1111 |  | FAIL |
| procgen | center_off | in_range | A5 | 9 | 2 | 0.1111 |  | FAIL |
| procgen | center_on | camera_distinct | A1 | 5 | 5 | 0.8000 |  | reported, not tested |
| procgen | center_on | camera_distinct | A2 | 5 | 2 | 0.8000 |  | reported, not tested |
| procgen | center_on | camera_distinct | A3 | 5 | 0 | 0.6000 |  | reported, not tested |
| procgen | center_on | camera_distinct | A4 | 5 | 5 | 0.0000 |  | reported, not tested |
| procgen | center_on | camera_distinct | A5 | 5 | 4 | 0.0000 |  | reported, not tested |

Read by the registered rules, Table 1 gives the verdicts collected in Table 2. On suite B under absolute moves (macro), A1 and A2 pass and A3, A4 and A5 fail. Under primitive actions (raw), only A1 passes. On suite C with center_agent off, over all 14 games, A1 passes and the other four fail. On the in-range subset of 9 games, A2 to A5 fail and A1 is "neither", with agreement 0.8889. The center_on condition is reported and not tested. κ is negative for A5 on macro (−0.4125), raw (−0.3374) and suite C (−0.7843), and for A4 on macro (−0.0435).

**Table 2. V1 verdicts by suite and condition** (from Table 1):

| suite, condition | PASS | FAIL | other |
|---|---|---|---|
| suite B, macro | A1, A2 | A3, A4, A5 | — |
| suite B, raw | A1 | A2, A3, A4, A5 | — |
| suite C, center_off (all 14) | A1 | A2, A3, A4, A5 | — |
| suite C, in-range subset (9) | — | A2, A3, A4, A5 | A1 "neither" (agreement 0.8889) |
| suite C, center_on | — | — | reported, not tested |

**Table 3. V2, docs/tables/v2.md verbatim** (commit bb0f1a1; written by scripts/analyze_v2.py at prereg-v1.1):

| suite | condition | subset | agent | role | n | positives | auroc | ci_low | ci_high | balanced_acc | auroc_B | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arc | native | all | N | reported | 25 | 14 | 0.4188 | 0.1978 | 0.6379 | 0.5357 | 0.5000 | FAIL |
| arc | native | all | R | reported | 25 | 15 | 0.4100 | 0.1850 | 0.6354 | 0.5333 | 0.5000 | FAIL |
| minigrid | macro | primary | I1 | evidence | 83 | 61 | 0.7187 | 0.5902 | 0.8298 | 0.5838 | 0.8413 | neither |
| minigrid | macro | primary | N | instrument check | 112 | 100 | 0.6613 | 0.5049 | 0.7941 | 0.5700 | 0.8725 | neither |
| minigrid | macro | primary | R | evidence | 112 | 101 | 0.6985 |  |  | 0.5693 | 0.8515 | VOID |
| minigrid | macro | primary, D9b included | I1 | evidence | 112 | 61 | 0.7719 | 0.6840 | 0.8529 | 0.5968 | 0.8734 | reported, not tested |
| minigrid | macro | all games | I1 | evidence | 161 | 61 | 0.7517 | 0.6764 | 0.8223 | 0.6016 | 0.7562 | reported, not tested |
| minigrid | macro | all games | N | instrument check | 161 | 100 | 0.6352 | 0.5514 | 0.7114 | 0.5700 | 0.5752 | reported, not tested |
| minigrid | macro | all games | R | evidence | 161 | 101 | 0.6434 | 0.5609 | 0.7208 | 0.5693 | 0.5589 | reported, not tested |
| minigrid | raw | primary | I1 | evidence | 98 | 71 | 0.5370 | 0.4324 | 0.6410 | 0.5070 | 0.8534 | FAIL |
| minigrid | raw | primary | N | instrument check | 155 | 130 | 0.5255 | 0.4320 | 0.6156 | 0.5038 | 0.6202 | FAIL |
| minigrid | raw | primary | R | evidence | 155 | 126 | 0.5224 | 0.4330 | 0.6096 | 0.5040 | 0.6561 | FAIL |
| minigrid | raw | primary, D9b included | I1 | evidence | 155 | 71 | 0.6258 | 0.5405 | 0.7065 | 0.5070 | 0.8184 | reported, not tested |
| minigrid | raw | all games | I1 | evidence | 161 | 71 | 0.6069 | 0.5235 | 0.6926 | 0.5070 | 0.8086 | reported, not tested |
| minigrid | raw | all games | N | instrument check | 161 | 130 | 0.4772 | 0.3829 | 0.5696 | 0.5038 | 0.6036 | reported, not tested |
| minigrid | raw | all games | R | evidence | 161 | 126 | 0.4805 | 0.3919 | 0.5687 | 0.5040 | 0.6472 | reported, not tested |
| procgen | center_off | all | I1 | evidence | 14 | 6 | 0.6458 | 0.3333 | 0.9445 | 0.5000 | 0.5104 | FAIL |
| procgen | center_off | all | N | instrument check | 14 | 9 | 0.7222 | 0.5000 | 0.9333 | 0.5000 | 0.5667 | neither |
| procgen | center_off | all | R | evidence | 14 | 9 | 0.7222 | 0.5000 | 0.9333 | 0.5000 | 0.5667 | neither |
| procgen | center_off | in_range | I1 | evidence | 9 | 4 | 0.8750 | 0.5000 | 1.0000 | 0.5000 | 0.4750 | neither |
| procgen | center_off | in_range | N | instrument check | 9 | 5 | 0.8000 | 0.5000 | 1.0000 | 0.5000 | 0.7000 | neither |
| procgen | center_off | in_range | R | evidence | 9 | 5 | 0.8000 | 0.5000 | 1.0000 | 0.5000 | 0.7000 | neither |
| procgen | center_on | camera_distinct | I1 | evidence | 5 | 3 | 0.3333 | 0.0000 | 1.0000 | 0.5000 | 0.6667 | reported, not tested |
| procgen | center_on | camera_distinct | N | instrument check | 5 | 4 | 0.3750 | 0.0000 | 0.8333 | 0.5000 | 1.0000 | reported, not tested |
| procgen | center_on | camera_distinct | R | evidence | 5 | 4 | 0.3750 | 0.0000 | 0.8333 | 0.5000 | 1.0000 | reported, not tested |

The analysis script also writes one line per suite (docs/tables/v2.json, "suite_lines"; runs/logs/analyze_v2.log):

```text
suite arc native all: reported, not tested
suite minigrid macro primary: not failed (decided by I1 alone)
suite minigrid macro primary, D9b included: reported, not tested
suite minigrid macro all games: reported, not tested
suite minigrid raw primary: suite FAIL (decided by R and I1)
suite minigrid raw primary, D9b included: reported, not tested
suite minigrid raw all games: reported, not tested
suite procgen center_off all: not failed (decided by R and I1)
suite procgen center_off in_range: not failed (decided by R and I1)
suite procgen center_on camera_distinct: reported, not tested
```

No agent reached PASS on any suite or subset. On the primary suite-B macro line, R is VOID, because it completed 101 of 112 games, a share of 0.9018, above 0.90. I1 is "neither" there, so the suite is "not failed", and that verdict is decided by I1 alone. On the primary raw line, R and I1 both fail, and so does the suite. On suite C with center_agent off, over all 14 games, I1 fails (AUROC 0.6458) and R is "neither" (0.7222), so the suite is "not failed". On the in-range subset every agent is "neither".

The nuisance baseline B is a logistic regression on grid area, action count and colour count (PREREG v1 Section 10). Its AUROC is the column auroc_B of Table 3. On every tested suite-B line it is higher than the census's AUROC, as Table 4 shows. Over all 14 suite-B lines, B is higher on 12. The two exceptions are reported, untested lines: macro "all games" for N (census 0.6352, B 0.5752) and for R (0.6434, B 0.5589).

**Table 4. Census and baseline AUROC on the tested suite-B lines** (from Table 3):

| line | census AUROC | B's AUROC |
|---|---|---|
| macro, I1 | 0.7187 | 0.8413 |
| macro, N | 0.6613 | 0.8725 |
| macro, R | 0.6985 | 0.8515 |
| raw, I1 | 0.5370 | 0.8534 |
| raw, N | 0.5255 | 0.6202 |
| raw, R | 0.5224 | 0.6561 |

The two ARC lines are reported and not tested (PREREG v1 Section 10, "ARC held-out: reported, not tested"), and the suite line says so. A defect in the frozen code computed them wrongly (STATE (k)). scripts/analyze_v2.py takes every ARC game that has a census, so the lines cover all 25 games, train games included, instead of the 17 held-out games. It also prints a per-agent verdict, "FAIL", on these lines, because it overrides the verdict only on untested subsets. That "FAIL" has no registered meaning and enters no gate. Section 6 gives the line on the 17 held-out games, as exploratory.

Gate G3 is decided by the registered outcome table (PREREG v1 Section 10, "Outcome and venue, pre-committed"; unchanged at v1.1), copied in Table 5.

**Table 5. The registered outcome table.**

| outcome | definition (registered) | venue (registered) |
|---|---|---|
| Support | V1 passes on B (both conditions) and C, V2 passes for R and I1 on B-macro and C (not void), and V3 holds | JAIR full article |
| Partial | V1 passes everywhere, but V2 passes on B-macro only or is void on C, or passes on C for R only | IEEE Transactions on Games full paper |
| Refute | V1 fails on any suite, or V2 fails on B-macro, or V2 is void on every suite | repository record only, at most an arXiv note |

The outcome is REFUTE, by the clause "V1 fails on any suite": V1 fails on suite B in both conditions and on suite C. The other two refute clauses do not apply, since the macro suite line is "not failed" and V2 is not void on every suite. The classification was written in STATE (k) before any results prose. The registered venue clause reads "at most an arXiv note". arXiv endorsement was not available to the author, so the clause is read as "at most a preprint" (STATE (l)).

This section does not show why V1 failed; Section 6 is the exploratory attempt to say. Nor does it show that the agents' level-1 outcomes are unrelated to game mechanics, since V2 tests one census score against them and nothing more.

## 6. Exploratory diagnosis

This section is exploratory. It was written after gate G3 (STATE (k)), from scripts/explore_v1_diagnosis.py (commit f43526a), its output runs/exploratory/v1_diagnosis.json and docs/EXPLORATORY_V1_DIAGNOSIS.md. It tests nothing, enters no claim, and does not change the outcome in Section 5.

Two checks come first. The census stored in each row equals the census recomputed from that row's report, with 0 mismatches over 3,500 rows. The ARC lines recomputed by the same functions reproduce the ARC lines of Table 3 to four decimals (docs/EXPLORATORY_V1_DIAGNOSIS.md, Section 1).

The readings per assumption follow docs/EXPLORATORY_V1_DIAGNOSIS.md, Section 5, with per-seed counts from the JSON. For A1, agreement is high on every subset: 151, 159, 13 and 4 games of 161, 161, 14 and 5. Every disagreement is a game where the truth holds and the census fails, and on these games no key produced a learned shift on most seeds.

For A2 under raw actions, 87 games have the truth holding and the census failing. On their 870 seeds the turn keys were recorded "no_move" on all 870, and forward was accepted on 208. A turn changes no tile index, because the adapter merges the agent's four orientations into one, so A2 rested on forward alone. Under macro actions A2 agrees on 159 of 161 games. On suite C there are six games where the truth fails A2 because other entities also respond to the action; on these the census found one controlled object on 9 or 10 of 10 seeds.

For A3 under macro actions, 92 games have the truth holding and the census failing. Four step vectors were accepted on 850 of their 920 seeds. Of the 775 per-seed failures, 755 carry the level-1 fallback "mispredicted" and the other 20 carry "no_avatar". The failure therefore comes from the planner's prediction during play, not from the learned vectors. Under raw actions the truth is "fails" everywhere, because forward depends on facing. The census says "holds" on 73 games; a per-key step vector cannot show a dependence on facing while turns record no shift.

The A4 rule is conditional on A3, so most A4 failures on suite B follow from those of A3: 807 of 1,030 macro seeds and 844 of 1,510 raw seeds of the games where the truth holds and the census fails. On suite C, wall_contradicted is above 0 on some seeds of all 13 games where the truth holds, and on all 10 seeds of five of them.

For A5, most undetermined seeds never recorded a goal place: 620 of 663 under macro, 986 of 1,074 under raw, and 70 of 110 on suite C. The census said "holds" where the truth fails on 23 macro and 15 raw environments. Success in every one of them needs facing, a toggle or a pickup; they belong to the GoTo, GoToObj, OpenDoor, OneRoom, Fetch and Unlock families. There were none on suite C. The negative κ for A5 is driven mainly by "undetermined". The registered κ maps "undetermined" to the value opposite the truth, so the cell "truth fails, predicted holds" contains 23 census "holds" and 61 undetermined verdicts under macro, 15 and 105 under raw, and 0 and 8 on suite C.

Seeds often disagree with their game's majority where the verdict hinges on the level-1 fallback (Table 3 of docs/EXPLORATORY_V1_DIAGNOSIS.md, not of this paper). The number of games with at least one dissenting seed was 134 of 161 for raw A2, 135 for raw A3, 111 for macro A3 and 111 for macro A4. Dissent is rare for macro A1 (3 games) and macro A2 (6 games), and for suite C A4 (2 of 14).

Table 6 gives the ARC line on the 17 held-out games, computed by the same functions (docs/EXPLORATORY_V1_DIAGNOSIS.md, Section 6). It is exploratory, reported and never tested. ARC rows carry no adapter field, so the baseline's features are constant and its AUROC is 0.5 by construction.

**Table 6. Exploratory ARC line on the 17 held-out games.**

| agent | n | positives | AUROC | 95% CI | balanced accuracy | AUROC_B |
|---|---|---|---|---|---|---|
| N | 17 | 8 | 0.3542 | [0.1041, 0.6346] | 0.5000 | 0.5000 |
| R | 17 | 9 | 0.3403 | [0.0909, 0.6213] | 0.5000 | 0.5000 |

The last exploratory reading concerns where the constructs part company (docs/EXPLORATORY_V1_DIAGNOSIS.md, Section 7). For A2 under raw actions, A3, A4 and A5, the census probes and the truth-table definitions are not the same constructs. The census A2 test asks whether some key moves one located object, while the truth asks whether exactly one object's displacement is a deterministic function of the action, turns included. The census A3 test asks whether the planner's level-1 model mispredicted, while the truth asks whether each action's unblocked displacement is constant. The census A4 test is conditional on A3 and counts walked-through "wall" colours, while the truth asks whether every blocked move is explained by a fixed obstacle set. The census A5 test asks whether a cell recorded at a level end ends a level again, and is silent when no level ends, while the truth asks whether success is triggered by entering a cell. The census reads by-products of one planner's run; the truth reads the source. This describes the mismatch. It is not a fix and not a result.

None of this supports a causal claim. These are counts of counters, read after the outcome was known.

## 7. What this shows and what it does not

### 7.1 The method claim is refuted under its own registration

The registered claim had two halves: that the census reports ground-truth mechanics at a registered accuracy, and that it predicts first-level completion. The first half failed on both confirmatory suites (Table 1), and by the registered outcome table that alone decides REFUTE (Section 5). The second half did not pass for any agent on any suite (Table 3). Nothing was changed after the tag to reach or to avoid this outcome (Section 2).

### 7.2 What V1 failing means here

V1 compares the census's verdict on each game with that game's entry in the source-derived truth table, and the two do not stand on the same footing. The truth table is the registered answer key: it was committed before the v1 tag, and each entry names the file and line of source code that justifies it (Section 4.2). The census verdict is the instrument under test. A V1 FAIL therefore says that the instrument disagreed with the answer key too often, on the registered sets and by the registered thresholds; in other words, the census as registered does not measure that assumption.

The exploratory reading in Section 6 suggests why. For A2 under raw actions, A3, A4 and A5, the census decisions are by-products of one planner's run: whether it located an avatar from its first presses, whether its level-1 model mispredicted, whether it walked through a colour it had called a wall, and whether a recorded cell ended a level again. The truth entries are properties of the environment's step function. Only A1, input coupling, is measured in nearly the same terms on both sides, and only A1 had no FAIL line. This reading is exploratory and is not part of the refutation.

### 7.3 Why the failure did not show on ARC-AGI-3

The census constants were set while the planner was developed on eight ARC-AGI-3 games (PREREG v1 Section 5.4), and the per-seed decision rules were written for v1 on the planner's report (PREREG v1 Section 5.3). No ARC truth table derived from source was written, so V1 was never computed on ARC (PREREG v1 preface). The development instance therefore gave the census no check against source-derived truth before registration. A disagreement between census and truth could not show there, because nothing on ARC measured it.

### 7.4 What a pilot V1 check would have shown

The pilot rows held census vectors for the eight pilot games, all of which have truth-table entries (STATE (k)). Comparing them with the truth before the v1.1 tag would have shown the disagreement before the 10,500 confirmatory runs were made (STATE (i), (j)). That check was not registered and was not done.

### 7.5 The nuisance baseline

On every tested suite-B line, a logistic regression on grid area, action count and colour count ranked the games better than the census score did (Section 5, Table 4). On suite B, then, how large and how varied an environment is predicted first-level completion better than the five assumptions as measured. This holds for the agents and conditions tested. It is not a statement about the assumptions as properties of the games.

### 7.6 What a second, separately registered study would have to change

What follows is a set of design requirements, not a result and not an existing instrument. A second study would have to define each census probe and its truth predicate as the same construct before registration, and show on development games that the two agree. It would have to write a truth table for the development instance, so that V1 can be measured where the parameters are set. It would have to register a V1 gate on the pilot games, with a stop rule, before any confirmatory run. It would have to register how "undetermined" enters each test, instead of mapping it to the opposite of the truth. And it would have to choose, before registration, a nuisance baseline that the census must beat on the development instance.

### 7.7 What this paper does not show

This paper does not show that frame-only agents cannot complete these games, that A1 to A5 are poor descriptions of the games, or that a different census would fail. It says nothing about hidden ARC-AGI-3 games, or about agents that bring priors of any kind to the games.

### 7.8 The author's position

This is single-author work with no institution, no funding and no GPU, and every run was made on one CPU machine. Every number in this paper is produced by a script in the repository, from rows in the repository, and names its file. The registered tests can be re-run from the tags (Section 9).

## 8. Related work

This section places the work among prior results, following docs/PRIOR_ART_KILL.md Parts C and E. It does not claim that this work improves on any of them.

**Predicting agent success from game mechanics.**
- The closest prior attempt is Bontrager et al. (2016). They read 14 mechanics features from GVGAI rule files and found that they did not predict which controllers succeed.
- Our census measured its features from frames, tested their accuracy against source-derived truth, and registered its prediction of first-level completion before any run.
- It failed at the first of these steps. Bontrager et al.'s features were exact by construction and failed at prediction; ours were not exact.
- Laidlaw et al. (2023) predict deep-RL sample complexity from a property of the full tabular MDP with reward. Gaina et al. (2018) predict wins from an agent's own experience during play on held-out games.

**Finding the controlled object.**
- The idea behind A1 and A2, finding the part of the frame the actions control from frames alone, is that of Bellemare et al. (2012) on contingency awareness, and Choi et al. (2019) on learned controllable regions.
- A2 adds a fixed, weight-free test that the controlled region moves by a consistent per-key displacement (docs/PRIOR_ART_KILL.md C4).
- Under primitive MiniGrid actions this test depended on forward alone (Section 6, exploratory).

**The goal-identification cost.**
- The registered quantity G counted level ends until a goal hypothesis is identified. Its elimination steps are the singletons-plus-empty example of Goldman and Kearns (1995) and version-space elimination (Mitchell, 1982).
- Goal recognition design (Keren et al., 2014; Wayllace et al., 2016) bounds an outside observer of an optimal actor and is related but different (docs/PRIOR_ART_KILL.md C1, C2, Part E).
- G was withdrawn without being measured (D16).

**ARC-AGI-3 agents.**
- Rudakov et al. (2025) published the graph-based frame explorer used here as I1.
- Liew (2026) classifies the 25 public games by the cheapest blind strategy that reaches a level. That taxonomy is about reachability, not mechanics, and makes no registered prediction.
- Skoutnev et al. (2026, "Twin") identify goals from frames with visual priors, outside the prior-free class G was defined for.

**Held-out reuse and pre-registration.**
- Blum and Hardt (2015) and Roelofs et al. (2019) study adaptive overfitting to a reused holdout. The ARC split here was fixed before development, and the held-out games were never opened.
- The pre-registration model in machine learning is set out by Bertinetto et al. (2021).

## 9. Reproducibility

This section lists what is needed to check every number. It does not claim that the runs are cheap: the confirmatory suite-B block took from 28 September to 13 October 2026 on one machine (STATE (j)).

**Repository and tags.**
- Repository: https://github.com/rahul-k-mishra/arc3-frame-only-study.
- Tags: prereg-v1 (19f2a9f), prereg-v1.1 (8b2b2b9), prereg-v1.2 (66e5606).
- Every confirmatory run was made from a worktree checked out at prereg-v1.1 (STATE (h), (i), (j)).

**Frozen files.** The six files of Section 3.3, with the blob hashes given there.

**Analysis code at prereg-v1.1** (PREREG v1.1 D11; `git ls-tree prereg-v1.1`):

| file | blob |
|---|---|
| scripts/analyze_common.py | caad22731807db78aff9c92c993a79a63f042ec3 |
| scripts/analyze_v1.py | 515f44b0f007182172022272383de548e80d5a11 |
| scripts/analyze_v2.py | 90a849c44e47addd8efdbfa579efdb16288edd50 |
| scripts/analyze_g.py | 46bf991d86400f0189d8898a7e068044d25c629a |
| scripts/determinism_check.py | 4f98f6430e9221deb1a43f2313eb00f5ca676969 |

**Run commands, by block.** Each block has its copy-pasteable commands, working directory and expected output in docs/W2_COMMANDS.md:
- block A: fidelity check;
- block B: dry run;
- block C: pilot;
- block C4: caps;
- block D: confirmatory runs D1–D7;
- block E: analysis E1–E3.
- The ARC baseline and its re-run are in docs/E6_RERUN.md and PREREG v1 Section 9.2.

**Environments.**
- ARC-AGI-3: arc-agi 0.9.8 and arcengine 0.9.3.
- MiniGrid/BabyAI: minigrid 3.1.0 and gymnasium 1.3.0, Python 3.11.9.
- Procgen: procgen 0.10.7, Python 3.10.
- All from PREREG v1 Section 3.

**Registrations.** https://osf.io/2znhw (v1) and https://osf.io/zu5vq (v1.1), with their registered texts in docs/OSF_REGISTRATION_final.txt and docs/OSF_REGISTRATION_v1_1_final.txt.

**Data.**
- 10,500 confirmatory rows: 9,660 for suite B (commit 8a986d9) and 840 for suite C (commit 5ac65c1). They are one JSON file per (suite, condition, agent, game, seed), under runs/suites/.
- The ARC E6 file, runs/navrun_prereg_e6_arc_25x10.json: 500 rows (STATE (h)).
- The tables are in docs/tables/ (commit bb0f1a1).

**Licence.** The repository's own code, documents and run data are released under the MIT licence, copyright 2026 Rahul Kumar Mishra, in the file LICENSE at the repository root. The directory external/, which holds the third-party agent I1 in external/rudakov_just_explore, is not covered by that licence and keeps the upstream MIT notice of its own authors as shipped (external/rudakov_just_explore/LICENSE).

## Appendix A. The amendment trail, D1 to D16

Each entry is summarised from docs/PREREG.md (v1.1 diff section; v1.2 diff section), where the full text, file and line references, and dates are given.

**D1. Six actions at most.** The frozen explorer presses ARC ids 1, 2, 3, 4, 5 and 7 only, so each suite is presented through a fixed key map.
- Suite B raw: left, right, forward, pickup, drop, toggle. "done" is not offered.
- Suite B macro: north, south, west, east, pickup, toggle. "drop" and "done" are not offered.
- Procgen: Procgen actions 5, 3, 1, 7, 9 and 10 (up, down, left, right, special 1, special 2).
- An environment with fewer actions keeps only those it has. MiniGrid-Dynamic-Obstacles has ids 1–3 under raw and 1–4 under macro.

**D2. Canvas placement.** A suite-B grid sits at rows 1 to h, columns 0 to w−1 of a 64 × 64 canvas. Every other cell holds padding index 0, and adapter palettes start at 1. The frozen code reads rows 1 to 62 and anchors the frame at the top left.

**D3. Procgen rows 0 and 63.** The 64 × 64 Procgen frame fills the canvas, so the frozen code does not see its top and bottom pixel rows. This is recorded, not corrected.

**D4. RESET per suite.**
- Suite B: episode k is reset with seed seed·100000 + k, and k advances only on a success. A RESET replays episode k's layout.
- Procgen cannot restart a level, so a RESET there takes no step and returns the current frame. It counts as an action.

**D5. Wall-clock cap.**
- The cap is three times the longest pilot run per suite, rounded up to a whole minute and computed by scripts/pilot_cap.py: 3300 s for suite B, 7500 s for suite C.
- Pilot runs ran uncapped.
- A projection found no confirmatory run expected over its cap. Rows cut by the cap are kept and reported as cut; none was cut.

**D6. The runner.** scripts/run_suite.py installs the shim with D1–D4, calls R and N exactly as the ARC runner does, refuses to run if any frozen blob hash differs, and writes one row per run.

**D7. I1's boundary.** I1 runs unchanged behind scripts/i1_suite_adapter.py. It sees the key map restricted to ids 1–5, palette indices ≥ 16 shifted by one, and level counts capped at 254. It therefore lacks toggle on suite B and special 2 on Procgen.

**D8. Infrastructure checks.** The fidelity check, the pilot row check, the Procgen camera check and the determinism check play random actions or read existing rows. None computes a census or a test statistic.

**D9. V2 exclusions for R and N.**
- Environments where success cannot be reached on any seed without an action missing from the key map are excluded from V2's primary line.
- "Cannot be reached" is read as reachability: the action triggers success or is a precondition of every successful episode (RKM, 27 Sep 2026).
- MiniGrid-Playground-v0, which has no success at all, is on every list.
- Raw: 6 excluded. Macro: 49.

**D9b. V2 exclusions for I1.** After the pilot showed I1 completing no level on MiniGrid-DoorKey-8x8-v0, the D9 rule was applied to I1's own map. It adds 57 environments where success needs toggle on every seed. Raw: 63 excluded. Macro: 78. Procgen: none, since no level end needs special 2.

**D10.** v1's suite-B seeding text is replaced by D4, and the runner's commands are added.

**D11. Analysis code.** The blob hashes of the analysis scripts at the tag are recorded. They changed only to implement D9, D9b and D13. Synthetic tests: 20 of 20.

**D12. ARC cap.**
- v1 inherited a 900 s per-run clock, which cut eight ARC nav rows short.
- The ARC cap is 3600 s per run, registered at prereg-v1.1. The eight rows were re-run under the v1 tag; the new rows replaced the cut ones, and no row is short.

**D13. Camera identity.**
- Ten Procgen games set center_agent false at every level start (procgen 0.10.7), so the secondary condition is identical to the primary on the nine confirmatory games among them.
- center_on is reported on caveflyer, climber, fruitbot, jumper and ninja only, and never tested.
- On the other nine, the center_on rows must equal the center_off rows, as a determinism check.

**D14. No adapter change after the pilot.** The pilot showed no errors, no cut runs and the expected cross-condition identity. No adapter changed.

**D15. G by registered replay.** G's rows were to come from a separate replay of N, registered as prereg-v1.2 before any replay, with every replay required to reproduce the confirmatory action sequence exactly.

**D16. G is not measured** (v1.2, 13 Oct 2026). D15's replay is withdrawn by RKM after gate G3 returned REFUTE. The instrument G would accompany failed V1 on both suites, so no G value is produced for suites B or C. G_end and G_act remain defined in PREREG v1 Section 6; none is reported.

## Appendix B. The exclusion lists

These lists are copied from the registered constants in scripts/analyze_common.py at prereg-v1.1. The source reason for each id is in PREREG v1.1 D9 and D9b.

**B1. No success at all** (`_NO_SUCCESS`, 1; on every agent's list in both conditions):

- MiniGrid-Playground-v0

**B2. Success needs done** (`_DONE_ABSENT`, 5; on every list in both conditions; done is in no key map):

- MiniGrid-GoToDoor-5x5-v0
- MiniGrid-GoToDoor-6x6-v0
- MiniGrid-GoToDoor-8x8-v0
- MiniGrid-GoToObject-6x6-N2-v0
- MiniGrid-GoToObject-8x8-N2-v0

**B3. Success is a drop** (`_DROP_ABSENT`, 15; macro lists of every agent):

- MiniGrid-PutNear-6x6-N2-v0
- MiniGrid-PutNear-8x8-N3-v0
- BabyAI-PutNextLocal-v0
- BabyAI-PutNextLocalS5N3-v0
- BabyAI-PutNextLocalS6N4-v0
- BabyAI-PutNextS4N1-v0
- BabyAI-PutNextS5N1-v0
- BabyAI-PutNextS5N2-v0
- BabyAI-PutNextS5N2Carrying-v0
- BabyAI-PutNextS6N3-v0
- BabyAI-PutNextS6N3Carrying-v0
- BabyAI-PutNextS7N4-v0
- BabyAI-PutNextS7N4Carrying-v0
- BabyAI-MoveTwoAcrossS5N2-v0
- BabyAI-MoveTwoAcrossS8N9-v0

**B4. A drop is a precondition** (`_DROP_PRECOND`, 28; macro lists of every agent; for I1 also on the raw list as toggle preconditions, B6):

- MiniGrid-KeyCorridorS3R1-v0
- MiniGrid-KeyCorridorS3R2-v0
- MiniGrid-KeyCorridorS3R3-v0
- MiniGrid-KeyCorridorS4R3-v0
- MiniGrid-KeyCorridorS5R3-v0
- MiniGrid-KeyCorridorS6R3-v0
- MiniGrid-UnlockPickup-v0
- MiniGrid-BlockedUnlockPickup-v0
- MiniGrid-ObstructedMaze-1Dl-v0
- MiniGrid-ObstructedMaze-1Dlh-v0
- MiniGrid-ObstructedMaze-1Dlhb-v0
- MiniGrid-ObstructedMaze-1Q-v1
- MiniGrid-ObstructedMaze-2Dl-v0
- MiniGrid-ObstructedMaze-2Dlh-v0
- MiniGrid-ObstructedMaze-2Dlhb-v1
- MiniGrid-ObstructedMaze-2Q-v1
- MiniGrid-ObstructedMaze-Full-v1
- BabyAI-KeyCorridor-v0
- BabyAI-KeyCorridorS3R1-v0
- BabyAI-KeyCorridorS3R2-v0
- BabyAI-KeyCorridorS3R3-v0
- BabyAI-KeyCorridorS4R3-v0
- BabyAI-KeyCorridorS5R3-v0
- BabyAI-KeyCorridorS6R3-v0
- BabyAI-UnlockPickup-v0
- BabyAI-UnlockPickupDist-v0
- BabyAI-BlockedUnlockPickup-v0
- BabyAI-UnlockToUnlock-v0

**B5. Success is a toggle** (`_TOGGLE_PRED`, 20; I1's lists in both conditions):

- MiniGrid-Unlock-v0
- MiniGrid-RedBlueDoors-6x6-v0
- MiniGrid-RedBlueDoors-8x8-v0
- BabyAI-Open-v0
- BabyAI-OpenDoor-v0
- BabyAI-OpenDoorColor-v0
- BabyAI-OpenDoorDebug-v0
- BabyAI-OpenDoorLoc-v0
- BabyAI-OpenDoorsOrderN2-v0
- BabyAI-OpenDoorsOrderN2Debug-v0
- BabyAI-OpenDoorsOrderN4-v0
- BabyAI-OpenDoorsOrderN4Debug-v0
- BabyAI-OpenRedBlueDoors-v0
- BabyAI-OpenRedBlueDoorsDebug-v0
- BabyAI-OpenRedDoor-v0
- BabyAI-OpenTwoDoors-v0
- BabyAI-Unlock-v0
- BabyAI-UnlockLocal-v0
- BabyAI-UnlockLocalDist-v0
- BabyAI-KeyInBox-v0

**B6. A toggle is a precondition** (`_TOGGLE_PRECOND`: these 9 plus the 28 of B4; I1's lists in both conditions):

- MiniGrid-DoorKey-5x5-v0
- MiniGrid-DoorKey-6x6-v0
- MiniGrid-DoorKey-16x16-v0
- MiniGrid-LockedRoom-v0
- MiniGrid-MultiRoom-N2-S4-v0
- MiniGrid-MultiRoom-N4-S5-v1
- MiniGrid-MultiRoom-N6-v0
- BabyAI-GoToImpUnlock-v0
- BabyAI-PickupAbove-v0

**The lists per agent and condition:**

| agent, condition | lists | count |
|---|---|---|
| R and N, raw | B1 + B2 | 6 |
| R and N, macro | B1 + B2 + B3 + B4 | 49 |
| I1, raw | B1 + B2 + B5 + B6 + B4 | 63 |
| I1, macro | B1 + B2 + B3 + B4 + B5 + B6 | 78 |
| any agent, Procgen | none | 0 |

## References

Bellemare, M. G., Veness, J., and Bowling, M. (2012). Investigating Contingency Awareness Using Atari 2600 Games. In *Proceedings of the AAAI Conference on Artificial Intelligence*, 26(1), 864–871. doi:10.1609/aaai.v26i1.8321.

Bertinetto, L., Henriques, J. F., Albanie, S., Paganini, M., and Varol, G. (2021). Preface. In *NeurIPS 2020 Workshop on Pre-registration in Machine Learning*, Proceedings of Machine Learning Research 148, p. i.

Blum, A., and Hardt, M. (2015). The Ladder: A Reliable Leaderboard for Machine Learning Competitions. In F. Bach and D. Blei (Eds.), *Proceedings of the 32nd International Conference on Machine Learning*, Proceedings of Machine Learning Research 37, 1006–1014.

Bontrager, P., Khalifa, A., Mendes, A., and Togelius, J. (2016). Matching Games and Algorithms for General Video Game Playing. In *Proceedings of the AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment*, 12(1), 122–128. doi:10.1609/aiide.v12i1.12884.

Chevalier-Boisvert, M., Bahdanau, D., Lahlou, S., Willems, L., Saharia, C., Nguyen, T. H., and Bengio, Y. (2019). BabyAI: A Platform to Study the Sample Efficiency of Grounded Language Learning. In *International Conference on Learning Representations (ICLR)*. arXiv:1810.08272.

Choi, J., Guo, Y., Moczulski, M., Oh, J., Wu, N., Norouzi, M., and Lee, H. (2019). Contingency-Aware Exploration in Reinforcement Learning. In *International Conference on Learning Representations (ICLR)*. arXiv:1811.01483.

Cobbe, K., Hesse, C., Hilton, J., and Schulman, J. (2020). Leveraging Procedural Generation to Benchmark Reinforcement Learning. In *Proceedings of the 37th International Conference on Machine Learning*, Proceedings of Machine Learning Research 119, 2048–2056.

Gaina, R. D., Lucas, S. M., and Perez-Liebana, D. (2018). General Win Prediction from Agent Experience. In *2018 IEEE Conference on Computational Intelligence and Games (CIG)*, 1–8. doi:10.1109/CIG.2018.8490439.

Goldman, S. A., and Kearns, M. J. (1995). On the Complexity of Teaching. *Journal of Computer and System Sciences*, 50(1), 20–31. doi:10.1006/jcss.1995.1003.

Keren, S., Gal, A., and Karpas, E. (2014). Goal Recognition Design. In *Proceedings of the International Conference on Automated Planning and Scheduling (ICAPS)*, 24(1), 154–162. doi:10.1609/icaps.v24i1.13617.

Laidlaw, C., Russell, S. J., and Dragan, A. (2023). Bridging RL Theory and Practice with the Effective Horizon. In *Advances in Neural Information Processing Systems 36*, 58953–59007. doi:10.52202/075280-2573.

Liew, K. H. (2026). Explore Before You Solve: The Speed–Depth Trade-off in Epistemic Agents for ARC-AGI-3. arXiv:2605.25931.

Mitchell, T. M. (1982). Generalization as Search. *Artificial Intelligence*, 18(2), 203–226. doi:10.1016/0004-3702(82)90040-6.

Roelofs, R., Shankar, V., Recht, B., Fridovich-Keil, S., Hardt, M., Miller, J., and Schmidt, L. (2019). A Meta-Analysis of Overfitting in Machine Learning. In *Advances in Neural Information Processing Systems 32*.

Rudakov, E., Shock, J., and Cowley, B. U. (2025). Graph-Based Exploration for ARC-AGI-3 Interactive Reasoning Tasks. arXiv:2512.24156. AAAI 2026 Workshop on AI for Scientific Research.

Skoutnev, A., Acharya, K., Longhitano, G., Udell, M., Ellis, K., and Drori, I. (2026). Twin: Playing an Unknown Game with a Test-Time Digital Twin. arXiv:2608.14490.

Wayllace, C., Hou, P., Yeoh, W., and Son, T. C. (2016). Goal Recognition Design with Stochastic Agent Action Outcomes. In *Proceedings of the Twenty-Fifth International Joint Conference on Artificial Intelligence (IJCAI-16)*, 3279–3285.
