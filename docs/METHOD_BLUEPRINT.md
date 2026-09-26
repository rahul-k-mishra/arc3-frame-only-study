# METHOD_BLUEPRINT.md

Draft 1.4 — 27 Sep 2026

(Draft 1.1 — corrected 27 Sep 2026 per TOG_PLAN_v3.md Section 3. Draft 1.2 — census input, registered adapter parameters, E6 as the ARC baseline, untraced values closed. Draft 1.3 — source exposure (Section 2.9), V1 on ARC limited to the 8 train games, W0 infrastructure checks. Draft 1.4 — gate G0 closed as cite-and-drop (docs/PRIOR_ART_KILL.md Part D): Statements 1–2, the enumeration check and V4 removed; G registered as measured definitions; agent family restated; RKM decisions 1–8 of 27 Sep 2026.)

Assumption census and goal-identification cost as a pre-registered measurement method

Draft 1 — 26 September 2026 — for review before anything is frozen. Target: JAIR (full article), then IEEE Transactions on Games.

---

## 0. What this document is, and what it is not

- It was drafted from the repository record as it stood at the end of the 25–26 September sessions: E1 inconclusive (Rudakov agent, 25 × 10 × 20,000), E2 (runs/navrun_e2_hash_25x10.json), the census (runs/census_v2.json, docs/census_v2.md), selection transfer (runs/split_transfer.json), the analytic ceiling (runs/ceiling.json), HELDOUT.md, HANDOFF_GNAV.md, docs/E1_result.md. docs/STATE.md was not available when this was written. Section 12 lists what must be reconciled against it before Section 2 is frozen. Where STATE.md and this document differ, STATE.md wins. Reconciled on 27 September 2026: docs/RECONCILE_20260927.md.
- Nothing here is a result. Every number quoted below already exists in a named run file. Every threshold is a proposal to be registered, not a finding.
- The governing rule for everything downstream: a sentence goes into the paper only if a script in scripts/ produced its number from a run recorded in runs/, executed by RKM, and the decision rule for that sentence was in docs/PREREG.md — git-tagged and OSF-timestamped — before the run started.

---

## 1. The claim the paper has to earn

One sentence:

> A fixed, cheap, frame-only probe battery (the assumption census) together with a defined goal-identification cost G, with every parameter frozen on eight ARC-AGI-3 training games, (i) reports the ground-truth mechanics of unseen games in three suites at a registered accuracy, and (ii) predicts, before any agent is run, on which unseen games assumption-driven frame-only agents complete the first level.

Two halves, both required:

- Half (i) is instrument validity: the census says what the game's source code says.
- Half (ii) is predictive validity: the census verdict predicts what an agent of the stated class does.

Neither half is a claim that ARC-AGI-3 is hard. ARC-AGI-3 is where the instrument was built; it is the development instance, not evidence of generality (Section 3).

Explicitly not claimed: that goal inference is "the" barrier on ARC-AGI-3 (E1 was inconclusive; the goal-oracle intervention was run as E9 and returned INCONCLUSIVE: tu93 MIXED — levels 4.7 → 5.0, level-1 agent/human ratio 3.74 → 2.34, game score 0.2442 → 1.0283; dc22 NOT BINDING — no level won by any arm; ls20 NOT TESTABLE — its goal predicate is not a place; two source-exposed games, no general claim; runs/e9_report.json, docs/E9_protocol.md. Goal identification is therefore not a single binding barrier across games, which is why the census is a vector of assumptions rather than a one-barrier claim); that any agent here is strong; that anything transfers to hidden ARC-AGI-3 games or the leaderboard; that the census is complete.

---

## 2. The frozen protocol (draft of docs/PREREG.md)

### 2.1 Environment contract

Every suite is wrapped into one interface and nothing else is exposed to the census or the agents:

```
reset(seed)        -> grid                         # integer colour-index grid, after the adapter's quantisation and crop
step(action_id)    -> grid, level_end, game_end    # bools from the suite's own flags
actions            -> fixed list of integer ids per game
```

- The census consumes an integer colour-index grid, not RGB pixels: scripts/g_motion.py best_shift and scripts/g_nav.py compare colour indices cell by cell (docs/PREREG_PARAMS.md). Each suite's adapter therefore registers four parameters:
  1. palette quantisation from RGB to colour indices (ARC: none, the frame is already an integer grid) — registered per suite before any run;
  2. frame crop (ARC: rows 1–62; rows 0 and 63 are excluded, scripts/g_motion.py:30–31, scripts/g_nav.py:192) — registered per suite before any run;
  3. grid size (ARC: 64 × 64, scripts/g_nav.py:192) — registered per suite before any run;
  4. action list (ARC: KEYS = 1,2,3,4,5,7 from scripts/g_control_probe.py:47) — registered per suite before any run.

- No reward, no symbolic state, no text, no instruction string, no "action accepted" flag. ARC exposes an accepted flag; the census must not read it, because MiniGrid and Procgen have no such flag. Register: the census uses frames only.
- level_end is the suite's own signal: ARC level completion; MiniGrid episode success; Procgen level_complete. game_end is ARC's WIN or the suite's terminal.
- Determinism: frames are a function of (seed, action sequence). A fidelity script runs every game twice with the same seed and the same 200 actions and requires byte-identical frame sequences. No census run starts on a suite until that script passes on every game in it.
- Rendering conditions are registered per suite (Section 3): MiniGrid full-grid top-down frame, fixed tile size, agent-view highlight off; Procgen with use_backgrounds off and monochrome assets as the primary condition, full textures as a secondary robustness condition reported either way.

### 2.2 The census

Five assumptions. Each has a probe, a budget, a decision rule and an output in {holds, fails, undetermined}. The numerical parameters are the ones already frozen on the eight ARC train games in the v2 learner (three agreeing presses, 2:1 margin over the runner-up, at most 10 px, at most 8 presses per key). They are copied into PREREG.md from the script source, not from memory, with the script's commit hash; the full list, with file, line and commit, is docs/PREREG_PARAMS.md.

- MAX_STEP = 10 is defined independently in scripts/g_nav.py:57 (the learner) and scripts/g_motion.py:17 (the motion detector). Both are registered; changing one does not change the other.
- learn_tries (scripts/g_nav.py:114, default 12) is stored and never read. It has no effect and is registered as such.
- The explorer, scripts/g_agent.py, drives the game while the census observes; its many constants shape which frames the census sees. It is frozen by file hash (git blob hash at the prereg tag), not constant by constant.

| | Assumption | Probe | Holds when |
|---|---|---|---|
| A1 | Input coupling | each action pressed k times from one state; frame diff | some action changes the frame, and the change differs across actions |
| A2 | One controlled object | v2 learner phase on frame differences | some action yields ≥3 agreeing displacements of one changed-pixel component, 2:1 margin, ≤10 px |
| A3 | Lattice motion | displacements from A2 re-measured from ≥2 distinct positions | per-action displacement constant across presses and positions; record 1-D vs 2-D |
| A4 | Blocking by a fixed obstacle set | wall probe | learned obstacle set predicts the next N blocked/unblocked presses better than the "always moves" baseline by the registered margin |
| A5 | Place goal | goal counters from the v2 census | goal_confirmed ≥ 1; fails when a recorded end-place is re-entered without a level end; undetermined when never retested within budget |

Per-assumption, per-game, per-seed budgets are registered as exact action counts (propose the v2 census values). Output is a five-vector plus the raw counters, written to one JSON per (suite, game, seed).

Perception input is the colour-index grid of Section 2.1, for every suite. The census code is not changed for other suites; what changes per suite is the adapter's four parameters (palette quantisation, frame crop, grid size, action list), each registered per suite before any run. On a textured suite (Procgen) the quantisation decides what the census can see, which is why it is registered before, not tuned after, the first run.

### 2.3 Goal-identification cost G

Two measured quantities. Their registered definitions (elimination rules, "identified", h_0) are in Section 5; there is no formal statement to prove (gate G0, docs/PRIOR_ART_KILL.md Part D).

Hypothesis classes, registered:

- H_place(m): "the level ends when the controlled object enters cell c", one hypothesis per cell of the m reachable cells, plus h_0: "level end is not a function of the controlled object's cell".
- H_feat(k): "the level ends when the controlled object enters a cell carrying feature f", one hypothesis per feature value (colour or texture class) observed, plus h_0.

The consistent set H(t) is every hypothesis not contradicted by the observed (cell entered, feature, level_end) pairs up to action t.

- G_end: number of observed level-end events until the goal is identified (exactly one non-h_0 hypothesis survives, Section 5), per class; ∞ if h_0 is the verdict or the budget ends first.
- G_act: actions from level start to the first level end under the registered coverage policy, divided by the number of distinct cells the controlled object has occupied by then. This is the per-cell price of finding the goal by exhaustion under the registered prior-free class; it is an identity used as a measurement, not a bound.

Both are measured on every game where A2 holds; on games where A2 fails, G is recorded as undefined, not as ∞. G is not measured on the ARC 25 today — the goal_confirmed counters exist, G does not; scripts/g_goal_cost.py is new work.

### 2.4 Agents

The claim in half (ii) is about a family: frame-only, prior-free, CPU-runnable agents that do not read game source (the definition of docs/archive/TOG_PLAN_v2.md Section 0). It has to be instantiated by more than the author's own code, or it shrinks to "predicts my agent".

V2 evidence comes only from agents that do not use A1–A5 in their policy: R (the hash_state explorer) and I1 (the Rudakov graph explorer). N uses A1–A5 by construction — it completes a level exactly when the assumptions let it walk to an end-place — so predicting N from the census is circular; N's V2 row is reported as an instrument check, not as evidence.

- R (reference explorer): the E2 hash_state explorer. Author-written, deterministic given seed, code released.
- N (reference navigator): the G-NAV planner. Rejected as a competition agent, but it is the purest instantiation of A1–A5 — it completes a level exactly when it can walk a controlled object to an end-place. Author-written. Instrument check only (see above); not V2 evidence.
- I1 (independent): the Rudakov, Shock & Cowley agent (MIT, no GPU/LLM/network, 0.02–0.056 s per action on ARC). Adaptability to MiniGrid/Procgen is unknown: if it hard-codes the 64×64 grid or the 16-colour palette, that is recorded and the paper states that no independent agent could be run outside ARC.
- No I2. E1c searched for a second admissible independent agent and closed with none (docs/E1c_search.md, docs/E1c_prometheus_check.md). The search reopens only if ARC-AGI-3 Milestone-2 releases after 30 September add a permissive-licence, non-LLM, CPU frame-only agent.

Admissibility (registered): no GPU, no LLM, no network; per-action cost at or under the E1 threshold; deterministic given seed. Budget: 20,000 actions per game per seed on every suite (the E2 budget) unless the fidelity script shows a suite's level is unreachable in that budget by the coverage policy, in which case the per-suite budget is registered once, before the confirmatory run, and never changed.

### 2.5 Metrics and unit

- Unit: the game. Seeds (10) are nested replications; runs are deterministic given the seed, so seed count is replication count and is said so.
- Outcome per (agent, game): completed level 1 within budget (binary); number of levels completed (count).
- The family measured: frame-only, prior-free, CPU-runnable agents that do not read game source. V2 evidence agents: R and I1; N is reported as an instrument check (Section 2.4).
- Census score S: number of A1–A5 holding (0–5). Binary prediction P: "the agent completes level 1 iff A2 ∧ A3 ∧ A4 ∧ A5 hold", tested for R and I1, reported for N.
- Nuisance baseline B: logistic prediction from frame size, number of actions, number of distinct colours — things any reviewer will suspect drive the result.

### 2.6 Registered thresholds (proposals — RKM registers the final numbers)

| Test | Passes if | Fails if |
|---|---|---|
| V1 instrument validity | per assumption, agreement with source-derived truth ≥ 0.90 and Cohen's κ ≥ 0.70 on the confirmatory set of each suite. On ARC-AGI-3, V1 is run on the 8 train games only and labelled development, because the held-out sources cannot be opened to build an answer key (Section 2.9); V2 on the ARC held-out games is reported, not tested | agreement < 0.75 for any assumption on any suite |
| V2 predictive validity | per agent, per suite: AUROC(S → completion) ≥ 0.80 with bootstrap 95% CI lower bound > 0.60; balanced accuracy of P ≥ 0.80; AUROC exceeds B by ≥ 0.10 | AUROC ≤ 0.65 for both an author agent and an independent agent on a suite where the test is not void |
| V2 precondition | the agent completes level 1 on between 10% and 90% of the suite's games | outside that band the test is void for that agent on that suite and is reported as void, not as pass |
| V3 parameter transfer | A1–A5 parameters identical to the ARC-train values on every suite | any re-tuning on B or C downgrades the claim to "after re-tuning on suite X" |

### 2.7 Pilot rules

- Declared pilot set: at most 6 MiniGrid environments and 2 Procgen games, named in PREREG v1.
- The pilot may fix adapter bugs and the perception scale rule (pixel thresholds expressed as a multiple of tile size — the scaling rule is registered, new constants are not).
- Every change is logged as a diff in PREREG v1.1. Pilot games are excluded from every confirmatory analysis.
- Nothing from a confirmatory game is run before PREREG v1.1 is tagged, except the registered W0 infrastructure checks (docs/W0_CHECKS.md): random actions, no census, no agent, infrastructure facts only, none of which enters the manuscript.

### 2.8 Analysis code is frozen too

scripts/analyze_v1.py, scripts/analyze_v2.py, scripts/analyze_g.py are written, unit-tested on synthetic JSON with known answers, and committed under the prereg tag before confirmatory runs. They read runs/ and write the tables. No analysis script is edited after the tag except to fix a crash, and each such fix is logged.

### 2.9 Source exposure

Definition. An ARC-AGI-3 game is **source-exposed** if its environment_files were opened, or it was studied through an oracle, by RKM at any time.

The record:
- docs/HELDOUT.md (lines 17–24):
  - source read: tu93, ls20, vc33, m0r0;
  - studied through the oracle: ft09, lp85;
  - partly studied: lf52 (avatar deltas were read from it);
  - dc22: moved from held-out to train on 21 Sep 2026 to debug BRUTUS-G milestone 2.
- docs/STATE.md header: tu93, dc22 and ls20. Their sources were read on 24 Sep 2026 while debugging g_nav.py (CLAUDE.md rule 1), and they are the games E9 was run on.

Consequences:
- All 8 train games (tu93 ls20 vc33 m0r0 ft09 lp85 lf52 dc22) are source-exposed.
- The 17 held-out games are not source-exposed and are never opened (docs/HELDOUT.md: "NEVER read the source of these, for any reason").
- Every table and figure labels source-exposed games as such.
- On ARC, an answer key built from source exists only for source-exposed games. V1 on ARC is therefore run on the 8 train games only and labelled development (Section 2.6), and V2 on the ARC held-out games is reported, not tested.

---

## 3. Benchmarks and why

| Suite | Role | Why | Ground truth from | Main risk |
|---|---|---|---|---|
| ARC-AGI-3, 25 public games (8 train / 17 held-out per HELDOUT.md) | development instance | the census was built and its parameters frozen here; the 17 held-out games are the only within-ARC transfer already measured | shipped game sources in environment_files, for the 8 source-exposed train games only (Section 2.9); held-out sources are never opened, so V1 on ARC covers the 8 train games only, labelled development, and V2 on ARC held-out is reported, not tested | it does not count toward generality. The census v2 runs predate the repository and their code cannot be shown from git (docs/PREREG_PARAMS.md Section 3), so census_v2 numbers are development only. E6 — census at 10 seeds on all 25 games under the tagged code — is the ARC baseline of the paper, run in W1 after the tag |
| MiniGrid + BabyAI (178 environments, already installed in .venv_games) | lattice suite with known mechanics; positive control for V1; predictive test for V2 | cheap; open Python source; place goals (Empty, FourRooms, LavaCrossing, DoorKey, MultiRoom, Crossing) and non-place goals (Fetch, PutNear, Unlock, BabyAI object tasks) both present, so A5 has variance | Python source per environment | raw actions are rotate/forward, so A3 fails by construction — see the two-condition design below |
| Procgen (16 games) | non-lattice generality test | pixel physics, gravity, enemies, textures, explicit level_complete flag, deterministic per level seed, CPU-native, permissive licence; this is what the census must survive to be called general | C++ source per game (about 300 lines each) | wheels exist only for Python 3.7–3.10 (needs a separate 3.10 venv on the lenovo; Kaggle's image may not run it); perception on textures; lattice agents may complete nothing, voiding V2 |
| Fallback: ALE / Atari | only if Procgen cannot be installed | pip-installable on 3.12, ROMs bundled | game manuals, not source | most games have no level-end event, so G is undefined and only A1–A4 is testable; Bellemare, Veness & Bowling 2012 already measured controllable regions there, so it invites "already done" |

Why not Atari as the third suite by default: the paper's framing is "level ends, no reward". Atari has reward and no levels. Procgen matches ARC's structure (many small games, frames, levels, deterministic) while breaking the lattice — that is the test a reviewer will ask for.

MiniGrid two-condition design (registered):

- Condition B-raw: MiniGrid's own action set (turn left, turn right, forward, pick up, drop, toggle, done). Prediction registered now: A2 holds, A3 fails on every environment, because "forward" depends on facing. This is an instrument test — the census must report exactly that.
- Condition B-macro: an absolute-move wrapper (north/south/east/west, each a macro of ≤3 primitive actions; the frame returned is the one after the macro). Prediction: A3 holds; A4 holds where walls exist; A5 holds on goal-tile environments and fails on object-task environments. This is the predictive test with variance in the outcome.

Ground truth. Before any run on B or C, a truth table docs/GROUND_TRUTH_minigrid.md and docs/GROUND_TRUTH_procgen.md records, per game, the A1–A5 truth vector and the expected A5 answer, each entry with the source file and line that justifies it. This table is both the V1 answer key and the pre-registered per-game prediction. It is committed under the prereg tag.

---

## 4. What supports generality and what refutes it

Support — all of the following:

1. V1 passes on B (both conditions) and C.
2. V2 passes for R and for I1 on B-macro and on C (not void); N's rows are instrument checks and do not count (Section 2.4).
3. V3 untouched: no parameter changed after the ARC-train freeze.
4. The ARC-AGI-3 held-out results are consistent with rule P when the same analysis script is run on the existing E2 and G-NAV runs (reported, not tested — they predate the registration).

Partial — publishable at ToG, not JAIR:

- V1 passes everywhere but V2 passes on B-macro only, or is void on C because no agent completes any Procgen level. Claim shrinks to "the census predicts lattice agents on lattice games", which is true and narrow.
- V2 passes on C for R only (I1 not adaptable). Claim shrinks to "predicts the author's explorer".

Refute — the method claim is dropped:

- V1 fails on any suite: the instrument does not measure mechanics.
- V2 fails on B-macro: the census cannot predict even the easy case.
- V2 void on every suite: no predictive claim exists; what remains is an instrument-validity note.

Pre-commitment table (which outcome sends the manuscript where):

| Outcome | Venue |
|---|---|
| Support | JAIR full article |
| Partial | IEEE ToG full paper |
| Refute | repository record only, at most an arXiv note |

---

## 5. Goal-identification cost: definitions and cited observations

Gate G0 closed on 27 September 2026 as "cite and drop the theorem" (docs/PRIOR_ART_KILL.md Part D, decided by RKM). The paper proves no theorem. G_end and G_act are measured quantities with the registered definitions below.

Registered definitions:

- The hypothesis classes H_place(m) and H_feat(k) (Section 2.3) are prior-free and registered: every reachable cell, or every observed feature value, is a hypothesis on equal footing, plus h_0 ("level end is not a function of the controlled object's cell").
- A level end at cell c with feature set F(c) eliminates every place hypothesis except c, and every feature hypothesis outside F(c).
- An entry into a cell without a level end eliminates that cell's place hypothesis and, for H_feat, nothing.
- "Identified" means exactly one non-h_0 hypothesis survives.
- h_0 is the verdict when no non-h_0 hypothesis survives.
- G_end is the number of level ends until identified; ∞ if the verdict is h_0 or if the budget ends first.
- G_act is the number of actions from level start to the first level end, divided by the number of distinct cells the controlled object has occupied by then. It is an identity used as a measurement, not a bound.

Cited observations (cite, do not prove; docs/PRIOR_ART_KILL.md Part C1 and C2):

- Elimination per example over the place class is the singletons-plus-empty example of Goldman & Kearns 1995, Lemma 1: each observation separates one singleton from the empty concept.
- Elimination over H_feat is version-space candidate elimination (Mitchell 1982), bounded by the teaching-dimension count of Goldman & Kearns 1995.

Scope: an agent with visual priors or an LLM can identify the goal before any level end (Twin, arXiv:2608.14490), so G is a property of the registered prior-free class, not of frame-only agents in general.

---

## 6. Order of work, with gates

W0 (this week)
1. Reconcile this document with docs/STATE.md (Section 12).
2. Prior-art kill: one document, docs/PRIOR_ART_KILL.md, one paragraph per paper, verdict per paper on what it already covers.
3. Gate G0: is there a non-trivial formal result? Closed 27 Sep 2026: no — cite and drop (docs/PRIOR_ART_KILL.md Part D; Section 5).
4. Decide suite C (Procgen vs ALE fallback) after installing Procgen in a 3.10 venv and running one game for 1,000 steps.

W1 — freeze
5. docs/PREREG.md v1: Sections 2.1–2.8 with final numbers; the truth tables for B and C; the agent list; the pilot set. Analysis scripts committed with synthetic-data tests.
6. Git tag prereg-v1. OSF registration of the same file (free, timestamped, independent of the repository). Gate G1: no run on any B or C game before this tag exists.
7. E6, after the tag: census at 10 seeds on all 25 ARC games under the tagged code. This is the ARC baseline of the paper. The census v2 runs predate the repository and their code cannot be shown from git, so census_v2 numbers are development only and are not the baseline.

W2 — adapters and pilot
8. scripts/env_frame.py (contract), scripts/adapter_minigrid.py (raw and macro conditions), scripts/adapter_procgen.py, scripts/fidelity_check.py. All parallel (worker pool), all with ordered run commands.
9. Rudakov adapter feasibility on MiniGrid and Procgen: docs/I1_feasibility.md with the exact reason if not adaptable.
10. Pilot on the declared set. PREREG v1.1 with diff. Tag prereg-v1.1. Gate G2.

W3–W4 — confirmatory runs (RKM runs, pastes console)
11. Census on all of B (both conditions) and C, 10 seeds → V1 tables.
12. Agents R, N, I1 (if adaptable) on B-macro and C, 10 seeds → V2 tables (no I2: E1c closed with none).
13. G measurement on B, C and the ARC 25 (new script; ARC runs are re-executed, not reconstructed).
14. Gate G3: outcome classified by Section 4 before a word of the results section is written.

W5 — analysis
15. Frozen analysis scripts run once; outputs committed.

W6–W7 — manuscript
16. JAIR format, code release (MIT), data release (all runs/ JSON), OSF link in the paper. Submit.

Rough calendar: 7 weeks if I1 adapts and Procgen installs; 5 weeks if neither, because the paper is then smaller. JAIR's own statistics put the expected time to a decision after submission at months (Section 8).

---

## 7. Compute plan (CPU only)

To be checked by scripts/timing_probe.py before the confirmatory runs; the figures below are feasibility estimates, not results.

- MiniGrid and Procgen step in the thousands of frames per second per core. 178 + 16 games × 10 seeds × (census budget + 20,000 agent actions) is a few tens of millions of steps; on 8 lenovo workers this is hours, not days.
- ARC-AGI-3: the E2 and G-NAV runs exist. The only new ARC run is G measurement (scripts/g_goal_cost.py), 25 × 10 × 20,000, which on the lenovo is the same scale as E2 — the E2 wall time is the estimate.
- Kaggle CPU sessions can take the MiniGrid block (Python 3.12, pip-installable, internet on for plain notebooks). Procgen stays on the lenovo 3.10 venv unless the Kaggle image runs it.
- Nothing needs a GPU. Nothing costs money. OSF registration is free.

---

## 8. Odds — plainly

JAIR's own published statistics (2025 submissions): overall acceptance 13.4%; 58.3% among submissions not summarily rejected; expected time to acceptance including one revision about 39 weeks.

For this paper, my estimate:

| Scenario | JAIR | ToG |
|---|---|---|
| Support | 15–20% | 40–50% |
| Partial (lattice-only or R-only) | under 5% | 30–40% |
| Refute | no submission | no submission |

The JAIR case rests on V1 and V2 holding across three suites with an independent agent (I1) outside ARC.

Why the ceiling is low even in the best case:

- Summary rejection risk. "Benchmark diagnostic for frame-only agents" reads as an evaluation study; JAIR asks for originality and significance to AI broadly. The manuscript must be written as a method with a falsified-or-not prediction, and the introduction must say in the first page what the census predicts and where it was wrong.
- Single author, no institution, code-heavy. Not a formal barrier at JAIR; it is a barrier to benefit of the doubt.
- Two of the three suites are the real test, and one of them (Procgen) can kill the method outright. That is the correct design, and it is why the odds are not higher.

Why try JAIR anyway: the submission is free, the reviews arrive either way, and the same manuscript reformats to ToG. The cost is calendar time, roughly four to nine months. Whether JAIR or ToG comes first is decided at gate G3 by outcome (RKM, 27 Sep 2026; Section 4 pre-commitment table).

---

## 9. What will not clear the bar as it stands

1. E1 is one independent agent, inconclusive, with three recorded confounds. Outside ARC there may be zero independent agents. Without one, half (ii) is "predicts my code" and JAIR is not realistic.
2. ARC-AGI-3 cannot be counted as one of three generality tests. It is the development set. The paper has two test suites.
3. MiniGrid passing is weak evidence: the census was built for lattices. Procgen is the only test that can fail for an interesting reason, and it can fail for a boring one (perception on textures).
4. G does not exist in code. goal_confirmed counters exist. The measure the paper is named for has never been run on any game.
5. The census consumes an integer colour-index grid. Outside ARC, what it sees is decided by the adapter's palette quantisation, frame crop, grid size and action list; a bad quantisation on a textured suite fails the census for a boring reason. The four parameters are registered per suite before any run and never tuned after.
6. There is no formal result (gate G0: cite and drop). G is a measured quantity; its elimination rules are cited observations (Section 5).
7. "Assumption fails → agent fails" can be confounded by search budget and by the analytic scoring ceiling. V2 must be budget-matched and the nuisance baseline registered; the ceiling result is ARC-scoring-specific and stays out of V2.
8. Prior art that a JAIR reviewer will name on sight: contingency awareness (Bellemare et al. 2012), reward identifiability (Ng & Russell; Cao, Cohen & Szpruch; Skalse et al.), reward-free exploration bounds (Jin et al.), the Procgen and BabyAI papers' difficulty analyses, Balla et al. on ARC-AGI-3, Blum & Hardt and Roelofs et al. on held-out reuse. Every one is cited and positioned (docs/PRIOR_ART_KILL.md) or the paper is desk-rejected on related work.
9. The adapter parameters (Section 2.1) are new, registered per suite, and untested on any suite but ARC; the census has only ever run on ARC's native integer grid.
10. MAX_STEP is defined twice (scripts/g_nav.py:57, scripts/g_motion.py:17). A change to one alone would silently split the learner from the motion detector; both are registered.
11. learn_tries is a declared parameter with no effect (scripts/g_nav.py:114, 121). A reader may take it for a live setting; it is registered as having no effect.
12. The explorer (scripts/g_agent.py) is frozen by file hash only; its constants are not listed, so any edit to it changes what the census sees without changing a registered census parameter.
13. The census v2 runs predate the repository; the code that produced them cannot be shown from git. The ARC census numbers used so far are development only; the ARC baseline exists only after E6 runs under the tagged code in W1.
14. Prior negative result on component (iii): Bontrager et al. 2016 (AIIDE) read mechanics features from GVGAI rule files and found they did not predict which controllers succeed. The paper's answer has three parts (docs/PRIOR_ART_KILL.md C3):
    - our properties are measured from frames by interaction, and their accuracy against source-derived ground truth is itself tested (V1);
    - our target is first-level completion by a stated family of agents, not the best controller in a portfolio;
    - our rule is frozen on the 8 ARC train games and registered before any held-out run.
    If V2 fails, it fails in the same way theirs did, and that is reported.
15. Circularity of N: the G-NAV planner uses A1–A5 by construction, so its agreement with the census is not evidence. V2 rests on R and I1 alone; if I1 cannot be adapted outside ARC, V2 on B and C rests on R only.
16. The ARC taxonomy of Liew (arXiv:2605.25931) classifies the same 25 games by the cheapest blind strategy that reaches a level. The census must be compared with it category by category, and every disagreement reported.

---

## 10. Decisions needed from RKM now

All closed by RKM on 27 Sep 2026 (docs/TOG_PLAN_v3.md Section 8): suite C is Procgen; the formal result is dropped (cite, do not prove); 20,000 actions per game on every suite unless the fidelity script forces a registered per-suite value; JAIR-first or ToG-first decided at G3 by outcome; OSF registration alongside the git tag. The list below is kept as the record of the questions.

1. Suite C: Procgen (requires a Python 3.10 venv on the lenovo) or the ALE fallback (A1–A4 only, no G). Recommendation: Procgen; decide after the W0 install test.
2. Whether Section 5 is attempted at all, given Gate G0's likely answer.
3. Whether the E2 20,000-action budget is the registered per-suite budget on B and C, or a per-suite budget is registered after the fidelity script.
4. JAIR first (calendar cost) or ToG first (label cost).
5. OSF registration: yes or repository tag only. Recommendation: both; the OSF timestamp is independent of the author.

---

## 11. First Claude Code tasks once Section 10 is settled

1. docs/PRIOR_ART_KILL.md (W0 step 2). Done 27 Sep 2026.
2. scripts/env_frame.py, scripts/adapter_minigrid.py (raw + macro), scripts/fidelity_check.py — parallel, ordered run commands, working directory stated.
3. docs/GROUND_TRUTH_minigrid.md from source, with file and line per entry.
4. docs/PREREG.md v1 assembled from Section 2 with the final numbers.
5. Only after the tag: the Procgen adapter and the pilot.

---

## 12. STATE.md reconciliation checklist

Confirm or correct from docs/STATE.md before Section 2 is frozen. Done 27 September 2026, item by item, in docs/RECONCILE_20260927.md; values that STATE.md did not contain were traced to a repository file on 27 September 2026 and are cited below.

- The exact v2 learner parameters and the script/commit they live in. Traced: docs/PREREG_PARAMS.md Section 1 (scripts/g_nav.py:55–57 and :756, commit ccc4d57e26cdee73ea0eabdbd7d7fdfe847ed265).
- The census_v2 tallies used in the paper (14 of 17 held-out games with keyboard input, 11 with a moved object; goal_confirmed 0 in every seed; the sc25 placement).
- E2 held-out numbers: M1 0.3274 (10 seeds), M4 10.50; E1 Rudakov M1 0.1750; M2/M1 4.05 against the > 5 rule; the three E1 confounds.
- The split-transfer numbers Section 4 of the ToG plan reports (1.1% vs 16.7%; rank correlation −0.43; regret 0.092 / 0.206 — runs/split_transfer.json, keys primary.random.summary.regret_best.mean = 0.0923 and primary.random.summary.regret_oracle.mean = 0.2061; fixed split 0.1464 / 0.3329 / 0.3632 / 0.2517) and whether any of them survives into the method paper: none does — docs/TOG_PLAN_v3.md Section 2 limits the ARC background to one paragraph on the census and the E9 verdicts, "Nothing else".
- The ceiling numbers (3.52 / 10.57 / 21.14) — runs/ceiling.json, keys means.all25.closed["1,1"] = 3.5235, ["2,1"] = 10.5706, ["3,1"] = 21.1411 (key "k,r": first k levels at ratio r; the same values under means.all25.whole). Out of the method paper's tests: docs/TOG_PLAN_v3.md Section 2 (Ceiling row).
- HELDOUT.md split (dc22 moved to train; 17 held-out) — docs/HELDOUT.md, copied unchanged from D:\Research\arc3\brutus\HELDOUT.md, SHA-256 8c07813ab01f5228a6af10f91771702dad0291f26b0f920892ef3a79763a122d ("dc22 MOVED FROM HELD-OUT on 21 Sep 2026") — and which ARC games count as "train" for parameter freezing: the 8 train games, docs/TOG_PLAN_v3.md Section 3 and Section 2 (Split row).
- The 0.28 s per-action admissibility threshold (docs/archive/TOG_PLAN_v2.md Section 3.1, A7; measured values in docs/E1_phase2_protocol.md Section 1) and the E1 fidelity procedure (docs/archive/TOG_PLAN_v2.md Section 3.1, A6; results in docs/E1_phase2_protocol.md Section 1), to be reused as the admissibility rule.
- Whether ar25's nav-versus-hash_state discrepancy (8/8 vs 0/4) is explained: it is not — docs/archive/TOG_PLAN_v2.md Section 10 ("The cause is unknown; it is reported as unexplained") and CLAUDE.md (State of the evidence, "UNEXPLAINED"). It is reported as unexplained.
- W6 reading list, before the related-work section is written (docs/PRIOR_ART_KILL.md "Open reads"): Gal 1979 and Alpern & Gal 2003; Zoroa et al. 2013; Angluin 1988; Mitchell 1982; Deng & Papadimitriou 1990; Dockhorn & Apeldoorn 2018; the full texts of Skalse et al. 2023, Keren et al. 2016 and Mendes et al. 2016.
- Read by RKM directly before the manuscript relies on them (the prior-art verdicts rest on sub-agent readings): Goldman & Kearns 1995, Lemma 1; Bontrager et al. 2016; Keren, Gal & Karpas 2014, Definitions 1–3 and Theorem 2.
- The registered-rule precedence decisions (BREAKS before REPRODUCES; card-count clause first — rows lacking per-level scorecard counts give INCONCLUSIVE; named as in docs/STATE.md Section 5, corrected 27 Sep 2026 from "missing-scorecard clause") — carried into PREREG.md as the template for rule precedence.
