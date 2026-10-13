# STATE: the entry point for a fresh session (26 September 2026)

Read this first, then the file named on each line. Every number here comes from the file named
beside it; do not quote a number from memory. Game sets: train tu93 ls20 vc33 m0r0 ft09 lp85 lf52
dc22; held-out the other 17. tu93, dc22 and ls20 are source-informed.

## 1. What the project is now

- **Plan of record in the files:** `docs/TOG_PLAN_v2.md` Sections 0 and 9, and `CLAUDE.md`. They
  describe a 6-8 page ARC-only short paper for IEEE CoG or a workshop, venue chosen 9 October 2026.
  The ToG full paper was dropped because E1 found one INCONCLUSIVE external agent and E1c found no
  second one (`docs/E1_result.md`, `docs/E1c_search.md`).
- **Decision of 26 September 2026 (author):** strengthen the work into a **method paper across
  several benchmarks** rather than ship the ARC-only short paper.
  - This decision is **not yet written into `docs/TOG_PLAN_v2.md` or `CLAUDE.md`**, which still
    name the short paper. Recording it there, with the benchmarks chosen and a protocol for the
    method, is the first task of the next session (Section 5).
  - The plan already listed a second CPU benchmark (GVGAI learning track) as optional
    (`docs/TOG_PLAN_v2.md` Section 7).

## 2. Evidence base

HO = the 17 held-out games; games are the unit, seeds nested. Scripts are in `scripts/`.

| result | numbers | file / script |
|---|---|---|
| E4 ceiling | S(k,r,N) = 100·k(k+1)/(N(N+1))·min(1, r⁻²), validated against arc-agi 0.9.8's scorecard on 2,463 cases. Mean over 25 games, first level only: 3.52 at the human count, 0.14 at 5×, 0.0039 at 30×. tu93 level 1 at 356 vs 19 = level score 0.28, game score 0.0063 | `runs/ceiling.json` / `g_ceiling.py` |
| E2 reference | hash_state, HO, 10 seeds × 20,000 actions, 170 runs: M1 0.3274, M4 10.50 levels per seed, no level 3 won | `runs/navrun_e2_hash_25x10.json` / `g_nav_run.py` |
| E2 decomposition | HO: recorded 0.3274; AT HUMAN 3.0602 (9.35×); 2× 0.7651; 5× 0.1224; 82 level-1 and 23 level-2 wins, none later; median agent/human ratio 59.7 over the 105 won levels. Train contrast: AT HUMAN 8.0060, median ratio 19.4, 29 level-3+ wins (all tu93, 8 of 80 runs) | `runs/decompose_e2_hash_25x10_{heldout,train}.json` / `g_decompose.py` |
| E3 budget curve | hash_state, HO, seeds 1000-1003: M1 0.3328 / 0.3329 / 0.3329 / 0.3329 at 3k / 20k / 50k / 100k actions. M4 6.25 / 11.25 / 13.00 / 14.75. M3 = 0 throughout. Paired difference 100k − 20k: M1 0.0000 [0.0000, 0.0000], M4 +3.50 [0.50, 7.75]. More actions buy levels worth nothing. All checks passed, including nesting (600 checks). The 20k point is the 4-seed subset of E2 | `runs/e3_curve.json` / `e3_curve.py`; inputs `runs/navrun_e3_hash_25x4_{3k,50k,100k}.json` |
| E5 selection transfer | 6×4 matrix, fixed split: the train pick is repeat_key (HO 0.1464); hash_state is held-out-best (0.3329) but ranks 6 of 6 on train. Per-game oracle 0.3632, cross-fitted 0.2517. 10,000 random splits: pick is held-out-best 0.0113 vs chance 0.1668; pick HO 0.2258 vs random 0.2547; mean tau −0.4282. Exploratory 16-mechanism matrix: mean tau +0.3673 | `runs/split_transfer.json` / `g_split_transfer.py`; `docs/TOG_PLAN_v2.md` §4 |
| Census v2 | HO: 14 of 17 have keyboard input, 11 have an object the keys move; goal_confirmed 0 in every seed. Categories 3 / 3 / 5 / 3 / 3 (sc25 a weak 1-D walker); the rule codifies an earlier census and is not pre-registered | `runs/census_v2.json`, `docs/census_v2.md` / `g_census_table.py` |
| E1 Rudakov et al. | 10 seeds × 20,000 actions: **INCONCLUSIVE** by (ii), M2/M1 = 4.05 against > 5. M1 0.1750, M4 3.30, M3 0. **Confounds:** (1) ACTION7 absent from their action set (pressed on 5 HO games, accepted on ar25 and bp35); (2) their choose_action raises on most actions in most runs (HO median 17,342 of 20,000); (3) preview vs 2026 games and API. Their preview result is not contradicted | `runs/e1_decision.json`, `runs/e1_rudakov_lenovo_25x10_20k.json` / `e1_decide.py`, `e1_rudakov_adapter.py`; `docs/E1_result.md` |
| E1c | **Closed**, no admissible second agent. Prometheus rejected: direction priors measured on all 25 public games. Strongest non-LLM agents have no licence. Most high-scoring non-LLM notebooks run the game's own simulator | `docs/E1c_search.md`, `docs/E1c_prometheus_check.md` |
| E9 goal oracle | Verdict **INCONCLUSIVE**; all checks passed; V2 50 of 50 oracle-arm wins on an oracle colour (tu93), 0 not seen; V5 0 on every level. **tu93 MIXED:** levels 4.7 → 5.0 (dL +0.30); level 1 ratio 3.74 → 2.34, a 37% cut, not halved; game score 0.2442 → 1.0283. **dc22 NOT BINDING:** no level won by any arm. **ls20 NOT TESTABLE** (finding: predicate not a place). Two source-informed games; no general claim | `runs/e9_report.json`, `runs/navrun_e9_oracle_3x10.json` / `e9_report.py`, `g_nav.py` (nav_oracle); `docs/E9_protocol.md`, `docs/E9_goals.md`, `docs/E9_V6_diagnosis.md` |

## 3. Claims withdrawn or corrected

| claim as it stood | why it fell | where corrected |
|---|---|---|
| "100,000 vs 20,000 actions, 0.3615 vs 0.3329: coverage does not pay" | 0.3615 was mode base (2 seeds, 100k); 0.3329 was hash_state (4 seeds, 20k). Different mechanisms, so no budget effect was measured. E3 now measures it | `docs/TOG_PLAN_v2.md` RQ1, `CLAUDE.md`, `docs/HANDOFF_GNAV.md` note |
| "A per-game oracle over 20 mechanisms is worth 0.03" | 0.3632 was over the 6-mechanism matrix, and the 0.03 gap was in-sample. Cross-fitted, the oracle (0.2517) scores below hash_state (0.3329) | `docs/TOG_PLAN_v2.md` §4.2 |
| "Train pick held-out-best 3 of 17; selected 0.3329" | 0.3329 and "3 of 17" belong to hash_state, the held-out-best mechanism, which is last on train. Reporting it was selection on the held-out games | `docs/TOG_PLAN_v2.md` §4.2 |
| Selection is anti-informative / rankings reverse | Held only in the primary matrix (tau −0.43); the exploratory matrix gives +0.37. The phrase "anti-informative" does not appear in any document in the repo; the written form is §4.4's "rankings reverse is not general" | `docs/TOG_PLAN_v2.md` §4.4 |
| "1,088 held-out runs" | No file produces it; the files it could sum repeat the same deterministic runs (162 of 680 rows were duplicates). The reference is E2's 170 | `docs/TOG_PLAN_v2.md` RQ1, `CLAUDE.md` |
| "Median agent/human ratio 35-145" | Untraced range; retired | E2 decomposition: 59.7 |
| "ar25: hash_state 0/12" (and 0/8) | The same four deterministic runs were counted in three (or two) files. Correct: hash_state 0 of 4 seeds; G-NAV 8 of 8 across v1 and v2 | `docs/TOG_PLAN_v2.md` §10, `runs/decompose_ar25_three_files_heldout.json` |
| "None of the fourteen with a controllable object" | 14 is the keyboard count; 11 have an object the keys move. sc25 was missing from the categories | `docs/TOG_PLAN_v2.md` RQ3, `docs/census_v2.md` |
| tu93 example "level 1 at 356 vs 19 is worth 0.3 of 100" | 0.28 is the level score; the game score is 0.0063 (level weight 1 of 45) | `docs/TOG_PLAN_v2.md` §5.4, `runs/ceiling.json` |
| Old title "Why Frame-Only Agents Plateau"; "the barrier is goal inference" | Rudakov et al.'s preview result is a counterexample to a general plateau; E1 does not establish a family claim; E9 is INCONCLUSIVE | `docs/TOG_PLAN_v2.md` title, C3, C4, RQ4 |

## 4. Standing rules

Summarised from `CLAUDE.md`:
- **Selection and sources:** select on train games only; never open a held-out game's source;
  label tu93, dc22 and ls20 source-informed everywhere.
- **Seeds and evidence:** at least 4 seeds for any reported number and 10 for final tables, with
  games as the unit and seeds nested. Runs are deterministic given the seed, so a repeated seed
  adds nothing. Every number comes from a script in the repo run by the author, with output in
  `runs/`. Quote pasted output exactly.
- **Scripts:** parallel, resumable, ablate-format JSON, no silent overwrite.
- **Working method:** commands go in fenced PowerShell blocks. State what must be true, and how
  failure shows, before building anything; report failures and own bugs as prominently as
  successes. Nothing is submitted to Kaggle.
- **Writing:** plain prose, every step shown, every limit stated where the claim is made.
- **Protocols:** registered before runs; thresholds never changed after output exists; changes
  are dated amendments.
- **Files:** `runs/` is the author's (never stage, commit or open run outputs uninstructed).
  `docs/TOG_PLAN.md` and `audit/TOG_PLAN_RUTHLESS_AUDIT.md` are historical records and are never
  edited; corrections go in current documents only.

## 5. Decided, and open: do not re-decide

Decided (change only by a dated amendment in the named file):
- **E1 rule, precedence and outcome:** BREAKS over REPRODUCES; card-count clause first; Rudakov
  INCONCLUSIVE (`docs/TOG_PLAN_v2.md` §3.3, `docs/E1_phase2_protocol.md`, `docs/E1_result.md`).
- **E1c closed; Prometheus rejected** (`docs/TOG_PLAN_v2.md` §3.5, `docs/E1c_search.md`,
  `docs/E1c_prometheus_check.md`).
- **E5 specification and matrices:** 6×4 primary, 20×1 exploratory with truncated mechanisms
  excluded (`docs/TOG_PLAN_v2.md` §4).
- **E3 design and reporting** (`docs/TOG_PLAN_v2.md` §7 E3).
- **E9:**
  - colour oracle as the only verdict arm; ls20 NOT TESTABLE;
  - decisions D1-D4: V2 "ending not seen" passes and is excluded; eligible level = one seed;
    colours read at the first planner step; disclosure of the 1,500-action glimpse;
  - verdict INCONCLUSIVE (`docs/E9_protocol.md` §§1-8, `docs/E9_goals.md`).
- **E2 at 10 seeds is the reference for every comparison** (`docs/TOG_PLAN_v2.md` §8).

Open (decide only through a registered protocol, named here):
- **The method-paper direction:** which benchmarks, what the method is, and what replaces the
  ARC-only plan. There is no protocol file yet; update `docs/TOG_PLAN_v2.md` (or a successor plan)
  and `CLAUDE.md` first.
- **E9 optional arm P** (the coordinate oracle, outside the verdict): run or drop
  (`docs/E9_protocol.md` §3).
- **E6 census at 10 seeds on all 25 games**, with the category rule frozen by code hash before
  the run (`docs/TOG_PLAN_v2.md` §7).
- **E10 formal goal-identification cost:** hypothesis class G to be fixed and hashed before use
  (`docs/TOG_PLAN_v2.md` §6).
- **Venue:** the 9 October 2026 decision in `docs/TOG_PLAN_v2.md` §9 predates the method-paper
  decision and must be re-taken with it.
- **E1b (organiser templates, baseline only) and E7 (14B LLM cost):** optional
  (`docs/TOG_PLAN_v2.md` §7).

## Amendment 27 Sep 2026

Session-end amendment. The lines above are unchanged; where this section corrects one of them, this section governs.

**W0 commits.**
- 0c1bf9c "W0: add method-paper blueprint 1.0 and plan of record v3" added:
  - docs/TOG_PLAN_v3.md, the plan of record for the method paper;
  - docs/METHOD_BLUEPRINT.md draft 1, the protocol draft.
- 4d1d8a5 "W0: carry-over, plan archive, blueprint 1.1, reconciliation, frozen params" added:
  - docs/PLAN_MERGE_20260927.md: 21 items of the method-paper decision carried from TOG_PLAN_v2.md and CLAUDE.md into TOG_PLAN_v3.md Section 10;
  - TOG_PLAN_v3.md Section 2, listing every named run with its file;
  - METHOD_BLUEPRINT.md draft 1.1, with the three corrections of TOG_PLAN_v3.md Section 3;
  - docs/RECONCILE_20260927.md: the blueprint checked against this file;
  - docs/PREREG_PARAMS.md: the census constants, copied from source with file, line and commit;
  - the method-paper section of CLAUDE.md.
- The commit carrying this amendment adds docs/HELDOUT.md, closes the untraced values in RECONCILE_20260927.md, and brings METHOD_BLUEPRINT.md to draft 1.2.

**Archive moves (4d1d8a5, contents unchanged).**
- docs/TOG_PLAN.md → docs/archive/TOG_PLAN_v1.md
- docs/TOG_PLAN_v2.md → docs/archive/TOG_PLAN_v2.md

References to the old paths elsewhere in this file are read as the new paths.

**Where the decision is written.**
- The method-paper decision of 26 September 2026 is now written in docs/TOG_PLAN_v3.md (Sections 1, 3, 5 and 10) and in CLAUDE.md ("Current objective", "Rules that bind every task", "Open decisions").
- docs/METHOD_BLUEPRINT.md (draft 1.2) is the draft protocol. It is not yet registered: it becomes docs/PREREG.md v1 only at the prereg-v1 tag.

**Venue.**
- JAIR first, IEEE Transactions on Games second (TOG_PLAN_v3.md Section 1).
- The venue is pre-committed by outcome at gate G3 (TOG_PLAN_v3.md Section 6):
  - support → JAIR full article (research note as fallback if V4 is dropped);
  - partial → IEEE ToG;
  - refute → repository record, at most an arXiv note.

**The split file.**
- docs/HELDOUT.md was copied unchanged from D:\Research\arc3\brutus\HELDOUT.md.
- SHA-256: 8c07813ab01f5228a6af10f91771702dad0291f26b0f920892ef3a79763a122d
- Its train set and held-out set are identical to this file's header.
- Its notes on source reading differ from this file's "source-informed" list:
  - HELDOUT.md marks tu93, ls20, vc33 and m0r0 "source read, family built";
  - this file's header names tu93, dc22 and ls20.
- This amendment records the difference and does not resolve it.

**Stale lines listed in docs/RECONCILE_20260927.md, each with its correction.**
1. Section 1: the decision is "not yet written into docs/TOG_PLAN_v2.md or CLAUDE.md". Correction: it was written there in commits c1eea2c and 1af3a1e, and into docs/TOG_PLAN_v3.md in 0c1bf9c.
2. Sections 1 and 5 name docs/TOG_PLAN_v2.md and docs/TOG_PLAN.md. Correction: they are docs/archive/TOG_PLAN_v2.md and docs/archive/TOG_PLAN_v1.md.
3. Section 5 (Open): "There is no protocol file yet" for the method-paper direction. Correction: docs/METHOD_BLUEPRINT.md is its draft protocol, not yet registered.
4. Section 5 (Open): the venue is listed as open. Correction: TOG_PLAN_v3.md Section 1 records JAIR first and ToG second, pre-committed by outcome at gate G3. Which one is submitted to first remains open (TOG_PLAN_v3.md Section 8, item 4).

## Amendment 27 Sep 2026 (b)

Second session-end amendment of 27 September 2026. The lines above are unchanged; where this section corrects one of them, this section governs.

**Decisions 1–8, taken by RKM on 27 Sep 2026** (recorded in docs/TOG_PLAN_v3.md Section 8, CLAUDE.md "Open decisions", METHOD_BLUEPRINT.md draft 1.4):
1. Suite C is **Procgen** (W0 check C1 passed: procgen 0.10.7 in D:\Research\arc3\brutus\.venv_procgen).
2. The formal result is **dropped**: cite, do not prove.
3. Budget: **20,000 actions per game on every suite**, unless the fidelity script forces a registered per-suite value.
4. JAIR-first or ToG-first is **decided at gate G3 by outcome** (support → JAIR full article; partial → IEEE ToG; refute → repository record, at most an arXiv note).
5. **OSF registration** alongside the git tag.
6. The W0 checks are **registered infrastructure checks, not experiments** (docs/W0_CHECKS.md).
7. Working title: **deferred to G3**.
8. ARC-AGI-3 items:
   - **E6** (census at 10 seeds on all 25 games under the tagged code) is **mandatory** in W1;
   - **E10** is carried by the goal-identification cost G;
   - **E9 arm P, E1b and E7 are dropped.**

**Gate G0 outcome: cite and drop the theorem** (docs/PRIOR_ART_KILL.md Part D).
- No paper kills any claim component.
- Statement 1's identification half and Statement 2 are covered by Goldman & Kearns 1995 and version-space elimination; Statement 1's cost half is covered by immobile-hider search games (PROVISIONAL: Gal 1979 not read directly).
- METHOD_BLUEPRINT.md draft 1.4 therefore:
  - removes Statements 1–2, the enumeration check and V4;
  - keeps G_end and G_act as registered, measured quantities.

**Consequences for this file.**
- Section 5 "Open" listed E9 arm P, E1b and E7 as optional, and E6 and E10 as open. This amendment closes all five: E9 arm P, E1b and E7 are dropped, E6 is mandatory, and E10 is carried by G.
- Section 5 "Open" also listed the venue and the method-paper direction. Both are closed by decisions 1–8 above and by the first amendment of 27 Sep 2026.

## Amendment 27 Sep 2026 (c)

Third session-end amendment of 27 September 2026. The lines above are unchanged.

**PREREG v1 written.** docs/PREREG.md v1 is the registered protocol, assembled from:
- METHOD_BLUEPRINT.md draft 1.4;
- PREREG_PARAMS.md;
- the two truth tables;
- W0_CHECKS.md.

It carries a preface listing six details this session filled in (marked "[registered here]" in the file). Tagging confirms them.

Also written:
- the analysis scripts scripts/analyze_common.py, analyze_v1.py, analyze_v2.py and analyze_g.py;
- their synthetic tests (10 tests, all passing, no runs/ file read);
- docs/OSF_REGISTRATION.md.

**Decisions taken by RKM on 27 Sep 2026:**
- **Camera (suite C):**
  - primary: center_agent False for all 16 Procgen games;
  - secondary, reported: the default scrolling view;
  - an instrument operating range derived from source (PREREG.md Section 4). Outside the range: caveflyer, climber, coinrun, fruitbot, jumper, ninja.
- **Levels (suite C):**
  - use_sequential_levels True, num_levels 0, start_level = rand_seed = the seed (1000–1009);
  - level end = prev_level_complete.
  - Finding recorded in PREREG.md Section 3.3: with num_levels 0, procgen ignores start_level (vecgame.cpp:287-289), so the level sequence is set by rand_seed alone.
- **Pilots:**
  - suite B: MiniGrid-Empty-5x5-v0, MiniGrid-FourRooms-v0, MiniGrid-DoorKey-8x8-v0, MiniGrid-Dynamic-Obstacles-6x6-v0, MiniGrid-Fetch-5x5-N2-v0, BabyAI-GoToRedBallGrey-v0;
  - suite C: coinrun, bigfish.
- **A5 readings:** fruitbot holds; leaper fails.
- **V1 on constant truth columns:** agreement rate only; κ only where both truth values have at least three members.

**Truth tables.**
- docs/GROUND_TRUTH_minigrid.md (commit f12e529): 178 ids. Suite B confirmatory = 161 (A5 holds on 36).
- docs/GROUND_TRUTH_procgen.md (commit 8d209b3): 16 games. Suite C confirmatory = 14 (A5 holds on 6).
- No ARC train truth table exists yet. V1 on ARC waits for docs/GROUND_TRUTH_arc_train.md.

**Tag.** `prereg-v1` is to be created by RKM on the commit that adds docs/PREREG.md. The OSF registration follows, with that commit's hash filled in. No run on a confirmatory suite-B or suite-C game before the tag. The adapters, I1 feasibility and scripts/g_goal_cost.py are W2 work under PREREG v1.1.

## Amendment 27 Sep 2026 (d)

Fourth amendment of 27 September 2026. The lines above are unchanged.

- **Tag.** `prereg-v1` created by RKM on commit 19f2a9f25043997d1deffd5976f2f2150e5f086f (annotated tag object 9696ce13ee15aaba26fc09a52b30c8b3aeb82fc9). docs/PREREG.md v1 at that commit is the registered protocol.
- **OSF.**
  - Open-ended registration https://osf.io/2znhw, approved by RKM from the OSF email.
  - Embargoed until 30 June 2030, to be ended early at acceptance.
  - Anonymised view-only link for reviewers: https://osf.io/2znhw/overview?view_only=f82b8a3e8a7f48ca94a952495e9520d3. The manuscript for review uses this link; the camera-ready uses the public URL.
- **Suite-level FAIL rule** as coded (decided by whichever evidence agents are present and non-void) accepted by RKM as tagged.
- **E6** launched by RKM from the worktree D:\Research\arc3\repo_prereg_v1 under the tag.
- **W2 begins:**
  - docs/ADAPTER_FEASIBILITY.md, whose Section 2 lists the parameters that need PREREG v1.1;
  - scripts/env_frame.py (contract and ARC shim), scripts/adapter_minigrid.py, scripts/adapter_procgen.py and scripts/fidelity_check.py;
  - docs/I1_feasibility.md (I1 adaptable through the same contract with boundary changes);
  - docs/W2_COMMANDS.md.

  No run on a confirmatory suite-B or suite-C game has been made. Whether the fidelity check may run on confirmatory games before v1.1 is RKM's decision (W2_COMMANDS.md).

## Amendment 27 Sep 2026 (e)

Fifth amendment of 27 September 2026. The lines above are unchanged.

- **E6 completed** (runs/navrun_prereg_e6_arc_25x10.json, committed by RKM in 248a12f). 500 runs in 173 minutes: 25 games × {hash_state, nav} × 10 seeds × 20,000 actions, under the tag prereg-v1. RKM's numbers:

  | split | hash_state M1 | hash_state levels per seed | nav M1 | nav levels per seed |
  |---|---|---|---|---|
  | train (8 games; tu93, dc22, ls20 source-informed) | 0.1901 | 11.1 | 0.2035 | 10.8 |
  | held-out (17 games) | 0.3274 | 10.5 | 0.2612 | 11.1 |

  goal_confirmed fired on tu93 only (a source-informed train game). It fired on no held-out game.
  These numbers include the eight cut nav rows below, so the nav values are provisional until the re-run.
- **Identity checks** (scripts/e6_check.py, run 27 Sep 2026):
  - (a) The 250 hash_state rows of E6 are identical to E2 (runs/navrun_e2_hash_25x10.json) in every field except `seconds`, 250 of 250. The tagged code is the E2 code for hash_state, and E6's hash_state held-out 0.3274 is E2's value.
  - (b) E6 nav rows for seeds 1000-1003 against census v2's nav rows (runs/navrun_v2_heldout.json, 17 held-out games): 66 of 68 are identical except `seconds`. The two that differ, sp80 seeds 1001 and 1003, are E6 rows cut by the 900 s clock (7,150 and 18,086 actions against 20,000 in v2). Their level logs agree with v2 up to the cut. So census v2's nav rows were produced by the code now tagged, as far as these rows can show. The full 68 of 68 is checked after the re-run.
  - (c) Eight E6 rows stopped before 20,000 actions, all nav and all at the 900 s clock:
    - re86 seeds 1004, 1006, 1007, 1008 (1,015 / 11,240 / 16,221 / 6,083 actions, 0 levels);
    - sp80 seeds 1001, 1003, 1004, 1006 (7,150 / 18,086 / 7,003 / 19,123 actions, 2 levels each).
- **The wall-clock cap, PREREG v1.1 draft D12.**
  - v1 inherited g_nav_run.py's 900 s default without registering it.
  - The registered ARC cap is now 3600 s per run.
  - The eight cut rows are re-run under the tagged code with that cap. The new rows replace the cut ones; a run is deterministic given the seed.
  - `--resume` re-runs them without a removal script. The command must name the full E6 selection. Commands are in docs/E6_RERUN.md.
  - The E6 census (runs/census_e6.json, docs/census_e6.md) is made only after the re-run.
- **ar25 at 10 seeds** (update to the "UNEXPLAINED" ar25 note in CLAUDE.md): hash_state completes level 1 on 6 of 10 seeds; nav completes it on 10 of 10. The earlier "hash_state 0 of 4" was seeds 1000-1003 only. The difference between the two arms is smaller at 10 seeds than at 4, and it is still not explained. Nothing is built on it.

## Amendment 27 Sep 2026 (f)

Sixth amendment of 27 September 2026. The lines above are unchanged; where this section corrects one of them, this section governs. The Claude Code session was restarted on 27 Sep 2026; this amendment was written in the first working session after the restart.

**E6, completed.**
- **Re-run of the eight cut nav rows** under the tag with the 3600 s cap (PREREG v1.1 draft D12): commit b3509de. scripts/e6_check.py then reported:
  - (a) 250 of 250 hash_state rows identical to E2 except `seconds`;
  - (b) 68 of 68 nav rows (seeds 1000–1003, 17 held-out games) identical to census v2 except `seconds`;
  - (c) 0 rows under 20,000 actions.
- **The E6 census** (commit e75551a):
  - files: runs/census_e6.json, docs/census_e6.md;
  - CLAUDE.md category agreement: 16 of 16 assigned games, with sc25 unassigned (the rule gives 1-D walker);
  - docs/census_e6_NOTE.md names the labels the frozen script printed from its census-v2 defaults, and adds sc25 to the category table (17 of 17 with it).
- **Still provisional: the nav numbers of amendment (e).** Its table (nav M1 train 0.2035, held-out 0.2612; levels per seed 10.8 and 11.1) was computed with the eight cut rows included. No document yet gives the nav values after the re-run. **Not yet run:** the recomputation from runs/navrun_prereg_e6_arc_25x10.json as committed in b3509de. The hash_state values are unaffected: every cut row was a nav row.

**W2 infrastructure, done (RKM).**
- **Fidelity check** (commit 51eba49): suite B 334 of 334 identical, suite C 32 of 32 (runs/fidelity/).
- **Dry run** (W2_COMMANDS block B), both suites: `frozen blob hashes: 6 of 6 match`.
- **C0 installs:** requests 2.34.2 and pydantic 2.13.5 in both suite venvs. numpy unchanged: 2.4.6 in .venv_games, 1.26.4 in .venv_procgen.

**The pilot** (commit db1e6ac; W2_COMMANDS block C).
- 360 suite-B rows and 120 suite-C rows. Every row is at 20,000 actions, none was cut, and all ran uncapped (--seconds 86400).
- **Caps, from scripts/pilot_cap.py:**
  - minigrid: longest 1081.6 s (MiniGrid-FourRooms-v0, raw, I1, seed 1003) → cap 3300 s;
  - procgen: longest 2481.5 s (bigfish, center_off, I1, seed 1003) → cap 7500 s.
  - Both are recorded in PREREG v1.1 draft D5.
- **Checks** (commits 387314c and cda7aa0). scripts/pilot_check.py (runs/pilot_checks/pilot_check.json) and scripts/procgen_camera_check.py (runs/pilot_checks/procgen_camera_check.json) are infrastructure checks in the class of fidelity_check.py (PREREG v1.1 D8, extended). From pilot_check.json:
  - no row has an error field;
  - 0 rows under 20,000 actions;
  - **structural zeros** (0 levels on every row of a (game, mode), both conditions): MiniGrid-DoorKey-8x8-v0 I1 (20 rows), bigfish R (20 rows) and bigfish N (20 rows). The bigfish zeros are pilot facts, recorded here and not explained. bigfish is a pilot and enters no confirmatory analysis;
  - cap projection: 0 confirmatory (game, condition, mode) over its cap. The largest projections are 1517.8 s on suite B (MiniGrid-MultiRoom-N2-S4-v0, macro, I1) and 2550.0 s on suite C (ninja, center_off, I1). This is an infrastructure check, not a guarantee (D5).
- **No confirmatory row exists.** The D6 count code of docs/W2_COMMANDS.md was run once on 27 Sep 2026 against runs/suites while it was written. It read 0 of 9,660 suite-B and 0 of 840 suite-C confirmatory rows.

**Three findings from the pilot, and RKM's decisions** (all written into the PREREG v1.1 draft; nothing is registered until the tag prereg-v1.1):
1. **Camera identity (D13).**
   - Finding: ten Procgen games set center_agent inside game_reset. At procgen 0.10.7, bigfish, bossfight, chaser, leaper, plunder and starpilot set it to false; dodgeball, heist, maze and miner set it to `distribution_mode == MemoryMode`, which is false under easy. center_on therefore draws the same frame as center_off on them. procgen_camera_check.py agrees: 401 of 401 identical frames on those ten, and a difference at step 0 on caveflyer, climber, coinrun, fruitbot, jumper and ninja. The 30 bigfish pilot pairs are identical in every non-timing field.
   - Decision: center_on is a distinct condition only on caveflyer, climber, fruitbot, jumper and ninja among the confirmatory games. V1's and V2's secondary line is reported on those five. On the other nine, the center_on rows are still run and must equal the center_off rows in every non-timing field, as a determinism check. The nine are exactly the Section 4 operating range.
2. **The I1 key set (D9b).**
   - Finding: I1 presses ids 1–5 only, so it has no toggle on suite B and no special 2 on suite C. It completed 0 levels on MiniGrid-DoorKey-8x8-v0 in all 20 rows, while R and N completed it in both conditions.
   - Decision: I1's map stays ids 1–5, with no remapping. D9's rule is applied to I1's own map for I1's evidence line, and a secondary line reports I1 with those environments included.
   - **Decision taken in this session (RKM, answering the assistant's question): "requires" is read as reachability, for every agent.** An action is required when success cannot be reached on any seed without it: either it triggers success, or it is a precondition, such as a locked or closed door on every path, or a carried key that must be put down before the target can be picked up. Under the predicate-only reading D9 had used, DoorKey would not have been excluded for I1.
   - Consequences:
     - D9's macro list for R and N grows from 20 to 48 (28 drop-precondition ids: KeyCorridor, UnlockPickup, BlockedUnlockPickup, UnlockToUnlock, ObstructedMaze);
     - raw stays 5;
     - I1's lists are 62 (raw) and 77 (macro), each with a source reason per id;
     - suite C has no D9b exclusion (no level end needs special 2).
   - The code change is in analyze_common.py and analyze_v2.py with two new synthetic tests. 14 of 14 synthetic tests pass with warnings as errors, and no run file was read. New blobs: analyze_v2.py fd68354e2c5a20c9ddcad9713178a575c4355f1c, analyze_common.py ddb807171046c0c10b5f7fd2839f4cbccff04600 (D11).
3. **Environments with fewer actions than the key map (D1).**
   - Finding: the suite-B adapter builds its action list from the action space, and the shim drops map entries the environment lacks. MiniGrid-Dynamic-Obstacles-6x6-v0 therefore has three entries under raw (ids 1–3: left, right, forward) and four under macro (ids 1–4, id 4 = east).
   - Correction to the question as posed: there is no id 4 under raw. `adapter.key_map.4` appears in pilot_check's list of keys that differ between conditions because it exists under macro only.
   - Decision: recorded, behaviour unchanged.
- **No adapter change after the pilot** (D14).

**Open before the tag prereg-v1.1** (named here so that the tag is not created early):
- **D13 in code.**
  - analyze_v1.py and analyze_v2.py still report center_on on all 14 confirmatory games.
  - No script yet runs the nine-game determinism check on confirmatory rows.
  - Both are registered in D13 but not implemented.
- **scripts/g_goal_cost.py does not exist.** PREREG Section 6 has it add a per-step log to N's run. RKM must decide whether G's rows come from the confirmatory N runs, which would need the script before block D, or from a separate logged re-run, whose action sequence is checked against N's.
- **Wording in D12.** "The registered ARC cap is now 3600 s" sits inside the unregistered v1.1 draft. It becomes registered only at the v1.1 tag. The re-run used that cap under the v1 tag.
- **The OSF v1.1 registration:** text in docs/OSF_REGISTRATION_v1_1.md, pasted by RKM after the tag.

**Files written in this session.**
- docs/PREREG.md v1.1 draft: D1 addition, D5 values, D8 extension, D9 amendment, D9b, D11, D12 outcome, D13, D14.
- docs/census_e6_NOTE.md.
- docs/W2_COMMANDS.md: blocks D (confirmatory runs, after the tag) and E (analysis); the old block D, the cap, is now C4.
- docs/OSF_REGISTRATION_v1_1.md.
- scripts/analyze_common.py, scripts/analyze_v2.py, scripts/test_analyze_v2.py.

**Source reading.** The procgen 0.10.7 sources were fetched raw from GitHub to verify D13 and D9b, into the session scratchpad and not into the repository. The minigrid 3.1.0 sources were read in the installed package. The assistant read runs/pilot_checks/*.json and a few pilot rows in runs/suites (the key maps). It also listed the file names at the top of runs/ once, and opened no other file there.

## Amendment 27 Sep 2026 (g)

Seventh amendment of 27 September 2026. The lines above are unchanged; where this section corrects one of them, this section governs.

**Decisions by RKM (27 Sep 2026):**
1. **D13 goes into the code before the tag.**
2. **G's rows come from a separate logged replay of N**, made after the confirmatory runs and registered as prereg-v1.2 before that replay (option B). This is PREREG v1.1 draft D15.
3. **The OSF v1.1 claim sentence is the v1 sentence verbatim.** docs/OSF_REGISTRATION_v1_1.md now carries the claim paragraph of docs/OSF_REGISTRATION_final.txt word for word, checked by string comparison. It includes the sentences on G ("measured and reported alongside, not tested") and on ARC-AGI-3 as the development instance.

**D13 implemented.**
- analyze_common.CAMERA_DISTINCT_C = (caveflyer, climber, fruitbot, jumper, ninja) is registered next to IN_RANGE_C.
- analyze_v1.py and analyze_v2.py report suite C center_on on the "camera_distinct" subset only. Every such line, and the V2 suite line, reads "reported, not tested". center_off keeps "all" and "in_range" unchanged.
- Hand-worked tests: test_center_on in test_analyze_v1.py and test_analyze_v2.py.
- **scripts/determinism_check.py** (D8 class, standard library only) compares, on the nine identical-frame games, every center_on row with its center_off row. It leaves out the seven timing fields and the three condition labels. It exits non-zero on any difference (1) or missing row (2) and writes runs/checks/determinism_check.json.
  - It has a synthetic test with 4 cases.
  - Its command is block D7 of docs/W2_COMMANDS.md, run after D4.
  - Before commit, its comparison function was applied to the 30 bigfish pilot pairs, which are not among the nine: 30 of 30 identical. That agrees with pilot_check.json.

**The reachability rule, one more pass (RKM's Step 3).**
- All 161 confirmatory suite-B environments were checked against their success predicates in docs/GROUND_TRUTH_minigrid.md.
- **MiniGrid-Playground-v0 has no success at all.** It places no goal and does not override step(), so it ends only by truncation (playground.py:16-31; truth-table note 4). It is now on every agent's list in both conditions (D9 amendment; analyze_common `_NO_SUCCESS`).
- The five done-requiring ids were already listed.
- Every other predicate is reachable on some seed under the six-key map.
- **Counts now:**

| agent | raw | macro |
|---|---|---|
| R and N | 6 | 49 |
| I1 | 63 | 78 |

  Primary games: 155, 112, 98 and 83. D9, D9b, test_registered_lists and the OSF text were changed accordingly.

**D15 (new).**
- scripts/g_goal_cost.py does not exist at the v1.1 tag.
- G's rows come from a separate replay of N on every confirmatory (game, condition, seed), after block D. The replay script is registered as prereg-v1.2 before any replay runs.
- Each replay must reproduce the confirmatory N row's action sequence and level log exactly. The script reports that check per row.
- G stays reported, not tested. Block D does not wait for it, and block E4 is marked "after prereg-v1.2 and the replay".

**D12 reworded.** "The registered ARC cap is now 3600 s" became "3600 s per run, registered at prereg-v1.1". This resolves the wording item of amendment (f).

**D11 re-recorded.** The table in docs/PREREG.md now gives each script's blob at prereg-v1, at 6f6f090, at 3cd61d2 and now. New blobs:
- analyze_common.py caad22731807db78aff9c92c993a79a63f042ec3;
- analyze_v1.py 515f44b0f007182172022272383de548e80d5a11;
- analyze_v2.py 90a849c44e47addd8efdbfa579efdb16288edd50;
- test_analyze_v1.py 61877fbb342ca02aca44a9c35c865361803d8de0;
- test_analyze_v2.py ca3f477b45fceff43a92de297f899e791d95b8af;
- determinism_check.py 4f98f6430e9221deb1a43f2313eb00f5ca676969 and test_determinism_check.py c0fc140faaed7aa7983fcc44b7a2284a5e6bc4f0, both under D8.

analyze_g.py is unchanged. **Synthetic tests, with warnings as errors: 5 + 9 + 2 + 4 = 20 of 20 OK. No runs/ file was read by any test.**

**scripts/e6_summary.py written, not yet run.**
- Blob: f962759ff9b25e50f2d15547176ea3f41e95ce6c. Standard library only; it writes nothing.
- It reads runs/navrun_prereg_e6_arc_25x10.json and prints the amendment (e) table per mode and split, with the definitions of docs/archive/TOG_PLAN_v2.md Section 3.2:
  - M1 = the mean over games of the seed-mean score;
  - levels per seed = the sum over games of the seed-mean levels;
  - the games where goal_confirmed fired.
- It also prints g_nav_run.py's form of each number and whether the two agree, and the row checks.
- It was exercised on a fabricated 500-row file only. The E6 file was not read.
- **Not yet run:** the post-re-run nav values. Amendment (e)'s nav values stay provisional until RKM runs it. The hash_state values must reproduce (e) exactly (0.1901 / 11.1 train, 0.3274 / 10.5 held-out).

**Open before the tag prereg-v1.1** (the list of amendment (f), reduced):
- RKM runs scripts/e6_summary.py. Its nav values replace amendment (e)'s provisional ones in the next STATE amendment. This does not block the tag: E6 is ARC development, outside v1.1.
- RKM reviews the v1.1 draft (D1–D15) and creates the tag. Then:
  - fill the commit hash and D11 blob hashes into docs/OSF_REGISTRATION_v1_1.md;
  - register it on OSF.
- Resolved since (f): D13 in code; the G sequencing (D15); the D12 wording.
- Still outside v1.1, by D15: scripts/g_goal_cost.py and PREREG v1.2, before the replay.
- Still outside v1.1: docs/GROUND_TRUTH_arc_train.md, for ARC V1, development only.

## Amendment 27 Sep 2026 (h)

Eighth amendment of 27 September 2026. The lines above are unchanged; where this section corrects one of them, this section governs.

**The tag prereg-v1.1.**
- Created by RKM on commit 8b2b2b9b432dbea4ba5f62cfceb1aad5558d1ecc (annotated tag object 76179fa87d218e412b21a2f2c20a28ffb13c30ce).
- `git ls-tree` at the tag gives analyze_common.py caad22731807db78aff9c92c993a79a63f042ec3, analyze_v1.py 515f44b0f007182172022272383de548e80d5a11 and analyze_v2.py 90a849c44e47addd8efdbfa579efdb16288edd50. These equal PREREG v1.1 D11 (checked again when this amendment was written).
- docs/PREREG.md v1.1 at that commit is the registered protocol. The heading "(DRAFT — not registered until tagged prereg-v1.1 after the pilot)" in the file describes it before the tag.
- Commits just before the tag:
  - a376170 (OSF v1.1 heading D1 to D15);
  - 8b2b2b9 (docs/OSF_REGISTRATION_final.txt, the v1 registration text as pasted; osf.io/2znhw).
- Commit after the tag: 3a8ff62 (docs/OSF_REGISTRATION_v1_1_final.txt, the v1.1 registration text as pasted).

**OSF v1.1.**
- https://osf.io/zu5vq, an Open-Ended Registration from project https://osf.io/29eas, embargoed until 30 June 2030, approved by RKM from the OSF email.
- The registered text is docs/OSF_REGISTRATION_v1_1_final.txt.
- One difference was found and corrected. In D11 the file had "(fill from `git ls-files -s` at the tag; the values of 27 Sep 2026 are given)", but the registered text reads "(checked against the tag on 27 Sep 2026)". That one line was changed in the commit carrying this amendment. **The file now matches the registered text as RKM reports it.** No other line was changed.

**E6 summary (scripts/e6_summary.py, run by RKM on runs/navrun_prereg_e6_arc_25x10.json).**
- Checks: 500 rows (25 games × 2 modes × 10 seeds), 0 errors, 0 rows short of 20,000 actions without a win.

| split | hash_state M1 | hash_state levels per seed | nav M1 | nav levels per seed |
|---|---|---|---|---|
| train (8 games; tu93, dc22, ls20 source-informed) | 0.1901 | 11.10 | 0.2035 | 10.80 |
| held-out (17 games) | 0.3274 | 10.50 | 0.2612 | 11.10 |

- The per-game form and the g_nav_run.py form agree ("same") on every line.
- goal_confirmed ≥ 1 in some seed: train tu93 only; held-out none.
- The hash_state values reproduce amendment (e) exactly, as they had to.
- **The nav values equal amendment (e)'s provisional ones.** So the re-run of the eight cut rows changed no level count, and the M1 values are unchanged to four decimals. **The "provisional" label on amendment (e)'s nav values is dropped.**

**Block D1 done.** The worktree D:\Research\arc3\repo_prereg_v1_1 is at prereg-v1.1; `git describe --tags --exact-match` prints prereg-v1.1.

**Block D2 done** (construction check, one reset per environment, no step). From runs/logs/dryrun_confirmatory_minigrid.log and runs/logs/dryrun_confirmatory_procgen.log (UTF-16, as Tee-Object writes them; read, not changed):

| | suite B (minigrid) | suite C (procgen) |
|---|---|---|
| frozen-hash line | `frozen blob hashes: 6 of 6 match PREREG.md Section 5.4` (line 1) | `frozen blob hashes: 6 of 6 match PREREG.md Section 5.4` (line 11, after the gym warning) |
| environment blocks | `minigrid raw ` 161, `minigrid macro ` 161: 322 = 161 × 2 | `procgen center_off ` 14, `procgen center_on ` 14: 28 = 14 × 2 |
| pilot games | none of the six appear | coinrun and bigfish do not appear |
| MiniGrid-Playground-v0 | appears, in both conditions (log lines 472 and 974) | — |

- **The single case-insensitive "ERROR" match** is in the procgen log, line 6:
  `    + FullyQualifiedErrorId : NativeCommandError`
  It is not a construction error. PowerShell 5.1 wraps a native program's stderr line in an error record when `2>&1` is used. The stderr line here is gym's import-time notice, log line 1: `python.exe : Gym has been unmaintained since 2022 and does not support NumPy 2.0 amongst other critical functionality.`, followed by its migration advice (lines 8-10).
- No environment line carries ERROR. The minigrid log has no match.
- The minigrid log's other 38 lines are BabyAI "Sampling rejected: …" notices: 30 "unreachable object", 6 "objs already next to", 2 "there are objects tha…". They come from layout rejection during reset (roomgrid_level.py:137) and are not errors.

**Operating rule for block D (RKM).**
- The caps were measured with 8 workers on an otherwise idle machine.
- D3 and D4 therefore run one at a time, never together, with no other Python job on the machine.
- The order is D4 (suite C) first, then D3.
- This rule is also written at the head of block D in docs/W2_COMMANDS.md.

**Next.**
1. D4 (suite C confirmatory, 840 runs, cap 7500 s).
2. D6 and D7 for suite C: the row count, then the nine-game determinism check.
3. D3 (suite B confirmatory, 9,660 runs, cap 3300 s).

**Still outside v1.1:** scripts/g_goal_cost.py and PREREG v1.2 before the G replay (D15); docs/GROUND_TRUTH_arc_train.md (ARC V1, development only).

## Amendment 28 Sep 2026 (i)

Ninth amendment (28 September 2026). The lines above are unchanged.

**OSF v1.1 (https://osf.io/zu5vq).** The embargo is confirmed on the registration page: "embargoed until Sun Jun 30 2030".

**Block D4 done: suite C confirmatory,** under the tag prereg-v1.1, from the worktree D:\Research\arc3\repo_prereg_v1_1. Log: runs/logs/confirmatory_procgen.log (UTF-16; read, not changed).
- `frozen blob hashes: 6 of 6 match PREREG.md Section 5.4`.
- `run_suite procgen center_off,center_on: 14 games x 10 seeds x 3 modes x 2 conditions = 840 jobs, 840 to run, 8 workers`.
- `summary: 840 rows written this call, 0 errors, 0 cut by the cap`.
- The log has 840 per-row "done" lines. Every one ends in "actions 20000", and none carries CUT or ERROR.
- The log's other lines are notices, not errors:
  - gym's import-time notice (8 times, once with PowerShell's NativeCommandError wrapper, as in D2);
  - 7 × "matplotlib is not installed, plots will not be available", I1's own notices.

**Block D6 for suite C** (RKM's output):
- six lines "140 of 140 rows";
- then "procgen: 840 of 840 confirmatory rows; missing 0; with an error 0; cut by the cap 0".
- Suite B showed 0 of 9,660, as expected before D3.

**Block D7: the determinism check** (scripts/determinism_check.py, PREREG v1.1 D8 and D13).
- Log: runs/logs/determinism_check.log. Output: runs/checks/determinism_check.json (pairs_compared 270, pairs_identical 270, pairs_missing 0, verdict "PASS"). Exit code 0, as RKM reports; the log does not contain that line.
- It covered 9 games × 30 pairs (3 modes × 10 seeds): bossfight, chaser, dodgeball, heist, leaper, maze, miner, plunder, starpilot. 30 of 30 were identical on each, 270 of 270 in all, with 0 differing and 0 missing.
- **What this establishes.** D13's identity holds on the confirmatory rows. On the nine in-range games, every center_on run equals its center_off run in every field except the seven timing fields and the three condition labels. That is what the source (game_reset sets center_agent false) and procgen_camera_check.py predicted. On those nine the secondary condition carries no information, which is why D13 reports center_on on the five camera-distinct games only.
- **What it does not establish.**
  - Nothing about V1 or V2. It compares rows with rows; it does not compare census verdicts with truth, or census scores with level-1 outcomes.
  - Nothing about the five camera-distinct games, where the two conditions are expected to differ.
  - Nothing about suite B.
  - It is an infrastructure check with no threshold of its own and enters no claim.

**Committed by RKM:** commit 5ac65c1, 845 files. It holds the suite-C rows, the determinism check output and the logs, including the D2 dry-run logs.

**Block D3 started (suite B confirmatory,** 161 games × 2 conditions × 3 modes × 10 seeds = 9,660 runs, cap 3300 s).
- Started on 28 Sep 2026 from the worktree under the tag, alone on the machine per the load rule of amendment (h).
- Log: runs/logs/confirmatory_minigrid.log.
- Its rows are being written into runs/suites while this amendment is written. This commit stages docs/STATE.md only.

**Next.**
1. D5 if D3 ends with errors.
2. D6 for suite B. D7 applies to suite C only.
3. Block E under the tag.

## Amendment 13 Oct 2026 (j)

Tenth amendment (13 October 2026). The lines above are unchanged.

**Block D3 done: suite B confirmatory,** under the tag prereg-v1.1, from the worktree D:\Research\arc3\repo_prereg_v1_1. It started 28 Sep 2026, finished by 13 Oct 2026, and had one start. Log: runs/logs/confirmatory_minigrid.log (UTF-16; read, not changed).
- The log has one `run_suite` line: `run_suite minigrid raw,macro: 161 games x 10 seeds x 3 modes x 2 conditions = 9660 jobs, 9660 to run, 8 workers`.
- It has one `frozen blob hashes: 6 of 6 match PREREG.md Section 5.4` line.
- It has one summary line: `summary: 9660 rows written this call, 0 errors, 0 cut by the cap` (with a prefix, see below).
- **Counts on the log** (RKM's, and checked again when this amendment was written):
  - 9,660 "done" lines, counted without a line anchor;
  - 0 of them with actions other than 20000;
  - 0 carrying CUT or ERROR.
- **A console artefact, not a run fault.**
  - 261 of the "done" lines carry a prefix, and so does the summary line, which reads `Sampling rejected: summary: …`. 236 of the 261 begin exactly "Sampling rejected: done ".
  - Eight workers share one console pipe. A BabyAI "Sampling rejected: …" notice from one worker (layout rejection during reset, roomgrid_level.py:137) and a "done" line from another landed on the same line.
  - The rows themselves are unaffected: each row is its own JSON file, written atomically by its worker.
  - The window filter of block D3 (`-notmatch 'Sampling rejected'`) hid those merged lines at the time. The log keeps them.

**Block D6 for both suites** (RKM's output):
- suite B: six lines "1610 of 1610 rows", then "minigrid: 9660 of 9660 confirmatory rows; missing 0; with an error 0; cut by the cap 0";
- suite C: six lines "140 of 140 rows", then "procgen: 840 of 840 confirmatory rows; missing 0; with an error 0; cut by the cap 0".
- **No row of either suite was cut by the D5 caps** (3300 s for suite B, 7500 s for suite C).

**Committed by RKM:** commit 8a986d9, "Confirmatory suite B under prereg-v1.1: 9660 rows, 0 errors, 0 cut; console log", 9,661 files: the 9,660 rows and runs/logs/confirmatory_minigrid.log (13.3 MB).

**State of the confirmatory data.**
- The confirmatory rows of both suites are committed, all produced under the tag prereg-v1.1: 9,660 for suite B (8a986d9) and 840 for suite C (5ac65c1).
- **No analysis script has yet been run on them.** No V1, V2 or G number exists for suite B or C. Every such number is "not yet run".

**Next.**
1. Block E under the tag: E1 (synthetic tests), E2 (analyze_v1.py), E3 (analyze_v2.py). The tables go into docs/tables.
2. Gate G3, decided by the registered outcome table (PREREG.md v1 Section 10, "Outcome and venue, pre-committed").
3. G (E4) waits for scripts/g_goal_cost.py, prereg-v1.2 and the replay (D15). G is reported, not tested, and is not part of the G3 decision.

## Amendment 13 Oct 2026 (k)

Eleventh amendment (13 October 2026). The lines above are unchanged. docs/PREREG.md is not changed by this amendment.

**Block E run** under the tag prereg-v1.1, from the worktree D:\Research\arc3\repo_prereg_v1_1.
- **E1:** 5 + 9 + 2 + 4 = 20 synthetic tests OK, with warnings as errors (test_analyze_v1, test_analyze_v2, test_analyze_g, test_determinism_check).
- **E2 and E3:**
  - Outputs: docs/tables/v1.md, docs/tables/v1.json, docs/tables/v2.md and docs/tables/v2.json.
  - Logs: runs/logs/analyze_v1.log and runs/logs/analyze_v2.log.
  - All committed by RKM in **commit bb0f1a1** ("Block E under prereg-v1.1: V1 and V2 tables (docs/tables), analysis logs; gate G3 outcome REFUTE").
- **No change after the tag.** `git diff prereg-v1.1 HEAD` over scripts/, docs/PREREG.md and the two truth tables is empty at the commit carrying this amendment. No threshold, parameter, exclusion list, truth entry or analysis script was changed after the tag. The verdicts below are those of the tagged code.

**E2: V1, every verdict line of docs/tables/v1.md, verbatim (commit bb0f1a1):**

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

**E3: V2, every verdict line of docs/tables/v2.md, verbatim (commit bb0f1a1):**

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

**E3, the V2 suite lines, verbatim** (docs/tables/v2.json "suite_lines"; runs/logs/analyze_v2.log):

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

**A defect in the ARC rows of the V2 table** (found while writing this amendment; recorded, not corrected, because the analysis code is frozen).
- The two ARC lines (suite arc, role "reported") carry the per-agent verdict "FAIL", and they are computed over 25 games.
- PREREG v1 says ARC held-out is "reported, not tested", and the suite line says so. analyze_v2.py overrides the per-agent verdict only on untested subsets, and it takes every ARC game that has a census, train games included.
- So the ARC per-agent "FAIL" has no registered meaning. Those two lines are development numbers over the 25 public games, not a test and not a held-out-only figure.
- They enter no gate. The G3 outcome below does not use them.

**Gate G3, applied by the registered outcome table** (PREREG.md v1 Section 10, "Outcome and venue, pre-committed", unchanged at v1.1; OSF https://osf.io/2znhw and https://osf.io/zu5vq).

*V1 (verdict lines above):*
- **Suite B, macro:** A1 PASS, A2 PASS; **A3, A4, A5 FAIL**.
- **Suite B, raw:** A1 PASS; **A2, A3, A4, A5 FAIL**.
- **Suite C, center_off, all 14:** A1 PASS; **A2, A3, A4, A5 FAIL**.
- **Suite C, center_off, in_range (9):** A1 "neither" (agreement 0.8889); A2, A3, A4, A5 FAIL.
- center_on is reported, not tested.
- So A1 passes on every "all" line, but not on the suite-C in-range subset, where it is "neither". A2 passes under macro only.
- Cohen's κ is negative:
  - for A5 on macro (−0.4125), on raw (−0.3374) and on suite C (−0.7843);
  - for A4 on macro (−0.0435).

*V2:*
- **No agent reaches PASS on any suite or subset.**
- Suite B macro, primary:
  - R VOID: 101 of 112 completed level 1, share 0.9018 > 0.90;
  - I1 "neither";
  - N (instrument check) "neither";
  - suite line "not failed (decided by I1 alone)".
- Suite B raw, primary:
  - R, I1 and N FAIL;
  - suite line "suite FAIL (decided by R and I1)".
- Suite C, center_off, all:
  - I1 FAIL (0.6458), R "neither" (0.7222);
  - suite line "not failed (decided by R and I1)".
- Suite C, in_range: all "neither".
- **The nuisance baseline B** (grid area, action count, colour count):
  - it has a higher AUROC than the census on every tested (primary) suite-B line, and on 12 of the 14 suite-B lines in all;
  - the exceptions are the reported "all games" macro lines of N (census 0.6352 against B 0.5752) and R (0.6434 against 0.5589).

*Outcome:*
- **REFUTE, by the clause "V1 fails on any suite".** V1 fails on suite B, in both conditions, and on suite C.
- The other refute clauses do not apply: the V2 macro suite line is "not failed", and V2 is not void everywhere. They are not needed, because one clause decides the outcome.
- **Pre-committed consequence: repository record only, at most an arXiv note.** No JAIR, no IEEE ToG.
- **This classification was written before any results prose.** No results text, abstract, discussion or figure exists for these runs.

**Corrections to the summary as it was given for this amendment** (each checked against the tables in commit bb0f1a1; the outcome is unaffected):
1. "A1 PASS everywhere": A1 is PASS on every "all" line, but "neither" on the suite-C in-range subset (0.8889).
2. "The nuisance baseline exceeds the census AUROC on every suite-B line": true on every primary (tested) suite-B line. Not true on the two reported macro "all games" lines of N and R.
3. "A5's kappa is negative on macro and on suite C": also negative on raw (−0.3374), and A4's κ on macro is negative too (−0.0435).

**A lesson, recorded as a lesson and not as a change.**
- The pilot rows (commit db1e6ac) contained census vectors (the N rows' `census` field) for eight games with truth-table entries. These were the six suite-B pilots and the two suite-C pilots, whose truth rows are in docs/GROUND_TRUTH_minigrid.md and docs/GROUND_TRUTH_procgen.md.
- A V1-style comparison on them before the v1.1 tag would have shown the instrument failure before the confirmatory runs.
- That comparison was not registered, and it was not done. It would have been a pilot diagnostic on 8 games, excluded from every confirmatory analysis. It could have changed adapter code, but no registered census constant, threshold or truth entry.
- Nothing in v1 or v1.1 is changed by this lesson.

**Open decisions for RKM** (none is pre-empted here):
- (a) Whether to write the pre-registered negative result as an arXiv note. That is the only venue the pre-commitment allows.
- (b) Whether the G replay (D15, prereg-v1.2) is still run, or dropped by a dated amendment, given that the instrument it accompanies failed V1.
- (c) Whether to do an exploratory diagnosis of the V1 failures, after this amendment: per-assumption confusion tables per suite, from docs/tables/v1.json and the rows. If done, it is labelled exploratory and used only in the note's discussion, never as a claim.

## Amendment 13 Oct 2026 (l)

Twelfth amendment (13 October 2026). The lines above are unchanged.

**The exploratory V1 diagnosis, after gate G3.** It is labelled EXPLORATORY everywhere, enters no claim, and does not alter the G3 outcome of amendment (k).
- **Script:** scripts/explore_v1_diagnosis.py (commit f43526a), run by RKM in the ARC venv from the main checkout.
- **Output:** runs/exploratory/v1_diagnosis.json.
- **Document:** docs/EXPLORATORY_V1_DIAGNOSIS.md, written from that JSON. Its tables were generated with jq, not by hand.
- **Checks:**
  - The stored census field and `census_from_report` recomputed agree: 0 mismatches over 3,500 N rows (1,610 + 1,610 + 140 + 140).
  - The ARC 25-game line reproduces docs/tables/v2.md to four decimals.
- **The exploratory ARC line on the 17 held-out games** (reported, never tested):
  - N: n 17, 8 positive, AUROC 0.3542, CI [0.1041, 0.6346];
  - R: n 17, 9 positive, AUROC 0.3403, CI [0.0909, 0.6213].
- **Its reading, in one sentence:** for A2 under raw, A3, A4 and A5, the census probes and the truth-table definitions are not the same constructs (document, Section 7). That is a description, not a fix.
- **Corrections the document makes to how the diagnosis was summarised before writing:**
  - Under macro, four step vectors were accepted on 850 of 920 seeds of the A3-disagreeing games, not on every seed.
  - On suite C, wall_contradicted is > 0 on some seeds of every one of the 13 truth-holds A4 games, but on all 10 seeds of only five of them.
  - The negative κ for A5 comes mainly from "undetermined" verdicts, which the registered κ rule maps to the opposite of the truth:
    - 61 of 84 on macro and 105 of 120 on raw are undetermined, against 23 and 15 GoTo/OpenDoor-family "holds";
    - on suite C it comes entirely from undetermined games.

**RKM's decisions (13 Oct 2026):**
- **G replay dropped.** PREREG v1.2, diff entry D16: "G is not measured." D15's replay is withdrawn, and no G value is produced for suites B or C. v1.2 is registered when RKM tags it `prereg-v1.2`; the tag is not yet created.
- **The preprint goes to OSF Preprints.** arXiv endorsement is not available to the author. The registered clause "repository record only, at most an arXiv note" is read as "at most a preprint".
- **No journal submission of this result.**

**Next:** the preprint draft, in docs/preprint/.
