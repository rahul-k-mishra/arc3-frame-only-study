# CLAUDE.md — arc3-frame-only-study

Measurement study of frame-only, prior-free, CPU-runnable agents on the ARC-AGI-3 public
demonstration set (25 games), now the development instance of a method paper across three
benchmarks (see "Current objective"; docs/TOG_PLAN_v3.md). Single author. No GPU. No money. Every
number in any document must come from a script in this repository run by the author, with its
output saved under runs/.

## Current objective (decision of 26 September 2026)

The ARC-only short paper is dropped. The ARC-AGI-3 measurement programme on the 25 public games is complete and frozen; every number in it is traceable to a file in runs/. It is background, not a paper. Every ARC-AGI-3 result stands as recorded; nothing already measured is re-run or re-decided because of the change of target. Of the ARC-AGI-3 items docs/STATE.md Section 5 listed as open, E6 is mandatory in W1 under the tagged code and E10 is carried by G; E9 arm P, E1b and E7 were dropped on 27 Sep 2026 (docs/TOG_PLAN_v3.md Section 8).

The paper now being built is a method paper: the assumption census (A1–A5) and the goal-identification cost G, pre-registered and frozen, demonstrated on three CPU-runnable benchmarks — ARC-AGI-3 (development instance, does not count toward generality), MiniGrid/BabyAI, and one more suite (Procgen recommended; ALE fallback). The claim has two halves and both must hold: the census reports ground-truth mechanics of unseen games at a registered accuracy, and it predicts, before any agent runs, where assumption-driven frame-only agents complete the first level.

Venues: JAIR first, IEEE Transactions on Games second. TMLR rejected. No conference that requires paid registration or travel (IEEE CoG is out). No venue with an APC. Double-anonymous whatever the venue: no names, handles, affiliations, acknowledgements or identifying links in the manuscript, the supplement or the code release. The ARC-only short paper and the ARC-only 10-page ToG full paper are superseded.

Plan of record: docs/TOG_PLAN_v3.md (docs/archive/TOG_PLAN_v1.md and docs/archive/TOG_PLAN_v2.md are archived ARC-programme records; what the 26 September decision first recorded in them is carried in TOG_PLAN_v3.md Section 10). Protocol draft: docs/METHOD_BLUEPRINT.md, which becomes docs/PREREG.md when tagged; its frozen census constants are listed from source in docs/PREREG_PARAMS.md. Single source of truth for numbers and run files: docs/STATE.md — update it at the end of every session.

## Rules that bind every task on this repository

1. You do not run experiments. You write scripts; RKM runs them and pastes the console output. You never estimate, extrapolate, or fill in a number. Every number in any document cites the runs/ file and the script that produced it. If a number does not exist yet, the document says "not yet run".
2. No result sentence without three things: a run file, the script, and a decision rule that was in the tagged PREREG.md before the run. Anything else is labelled exploratory and stays out of claims.
3. Once prereg-v1 is tagged, PREREG.md changes only by a new version (v1.1, v1.2) carrying an explicit diff section. Analysis scripts are frozen at the tag; a crash fix is allowed and must be logged in PREREG's diff section.
4. No run touches a confirmatory MiniGrid, BabyAI or suite-C game before the prereg tag exists. Only the declared pilot set may be run before it, and pilot games are excluded from every confirmatory analysis. Every benchmark has its selection split (pilot against confirmatory) fixed in PREREG.md before any mechanism is measured on it; games are the unit, seeds nested.
5. Ground-truth tables (docs/GROUND_TRUTH_<suite>.md) are built from source code, one line per game with the file and line that justifies each A1–A5 entry. Never from documentation summaries, never from memory.
6. The census reads frames only: no reward, no symbolic state, no text, no ARC "accepted" flag. Any code path that reads more than the frame is a bug.
7. Scripts are parallel (multiprocessing worker pool), deterministic given seed, resume-safe, and write one JSON per (suite, game, seed). Every script is delivered with its run commands in order, copy-pasteable, with the working directory stated, in a fenced code block. No inline code spans in prose.
8. Deliverables are complete and self-contained, not patches. Zips are flat.
9. Manuscript text: plain human language, no overclaiming, no "state of the art", every mathematical step written out, and an explicit statement of what the method can and cannot do. A theorem that turns out to be a corollary of cited work is cited, not proved, and the paper is written to stand without it.
10. Hardware: CPU only. lenovo (8 workers) and Kaggle CPU sessions. No GPU, no LLM, no network in any admissible agent. No money. Runtime is not a constraint; do not trim scope to save compute. Procgen wheels exist only for Python 3.7–3.10 and need a separate venv; the ARC venv stays on its pinned Python.
11. Rule precedence carries over from the ARC programme: BREAKS before REPRODUCES; the card-count clause (rows lacking per-level scorecard counts give INCONCLUSIVE) is evaluated first; the per-action admissibility threshold and fidelity procedure from E1 are reused unchanged.
12. When a task would require a number, a threshold, or a design choice that is not yet registered, stop and ask RKM. Do not choose it silently.

## Open decisions (RKM decides; do not pre-empt)

All eight closed by RKM on 27 Sep 2026 (docs/TOG_PLAN_v3.md Section 8):
1. Suite C: Procgen.
2. The formal result: dropped; cite, do not prove.
3. Budget: 20,000 actions per game on every suite, unless the fidelity script forces a registered per-suite value.
4. JAIR-first or ToG-first: decided at gate G3 by outcome.
5. OSF registration: yes, alongside the git tag.
6. W0 probes: registered infrastructure checks, not experiments (docs/W0_CHECKS.md).
7. Working title: deferred to G3.
8. ARC-AGI-3 items: E6 mandatory in W1 under the tagged code; E10 carried by G; E9 arm P, E1b and E7 dropped.

Gate G0 is closed: cite and drop the theorem (docs/PRIOR_ART_KILL.md Part D). There are no open decisions until gate G1.

## Non-negotiable rules (from the author; do not relax them)

1. Selection uses TRAIN games only. HELD-OUT is measured, never chosen on. Train: tu93 ls20 vc33
   m0r0 ft09 lp85 lf52 dc22. Held-out: ar25 bp35 cd82 cn04 g50t ka59 r11l re86 s5i5 sb26 sc25
   sk48 sp80 su15 tn36 tr87 wa30. Never open a held-out game's source (environment_files/<game>/*/).
   The sources of tu93, dc22, ls20 WERE read on 24 Sep 2026 while debugging g_nav.py; those three
   games are "source-informed" and must be labelled so in every table and figure.
2. Never report a single seed as a result. Minimum 4 seeds for any number that goes in a document;
   10 seeds for the final tables. Games are the statistical unit; seeds are nested within games.
   Seed replication never implies population certainty about 17 games.
3. Every claim comes from a run the author executed. Provide the script; never assume its output.
   When the author pastes output, quote its numbers exactly.
4. Scripts run in parallel (multiprocessing Pool, --workers), are resumable, write JSON in the
   ablate format (game, mode, seed, score, levels, level_log, card_levels, card_baseline), and
   print the commands' expected outputs in their docstrings.
5. Commands for the author are given as ordered, copy-pasteable PowerShell blocks with the working
   directory. The author's chat client renders inline code badly: put commands in fenced blocks.
6. Before building any mechanism or analysis, state what must be true for it to work and how its
   failure will be visible. Report failures and your own bugs as prominently as successes.
7. Nothing is submitted to the Kaggle competition from this repository. Kaggle notebooks built
   here are plain lab notebooks in their own folders with their own kernel ids.
8. Prose in documents: plain language, no filler, no "state of the art", no overselling; every
   mathematical step shown; every limitation stated where the reader meets the claim.

## Machines

- lenovo: Windows, 32 GB RAM, 8 workers, arc-agi 0.9.8 / arcengine 0.9.3 in
  D:\Research\arc3\brutus\.venv; game files in D:\Research\arc3\brutus\environment_files.
- Kaggle CPU sessions: 4 vCPUs (2 physical cores), 31 GB RAM, internet on for plain notebooks.
  Measured: a 7B LLM on CPU costs 218-1,254 s per action; the rerun budget is ~2.9 s. No LLM runs.

## State of the evidence (all HAVE, all under runs/)

- Reference, E2 (updated 26 Sep 2026): hash_state, held-out, 10 seeds x 20,000 actions: M1 0.3274,
  M4 10.50 levels per seed, no level 3 won in 170 held-out runs; level 2 won in 23 of them (cd82 10,
  sp80 8, r11l 3, ar25 2), with near-zero level-2 scores (runs/navrun_e2_hash_25x10.json). This
  is the reference for every comparison. The 4-seed 0.3329 (runs/ablate_lenovo_6x4.json) survives
  only as a record in registered text. Run count: 170 held-out runs (17 games x 10 seeds, E2). The
  earlier "1,088 held-out runs" is WITHDRAWN: no single file produces it, and the files it could be
  summed from contain the same deterministic runs more than once (hash_state seeds 1000-1003 in
  three files; 162 of 680 rows dropped as duplicates when those three were read together).
  E2 decomposition (runs/decompose_e2_hash_25x10_heldout.json): AT HUMAN 3.0602 (9.35 x recorded),
  at 2x 0.7651, at 5x 0.1224; 82 level-1 and 23 level-2 wins, none later; level-1 wins give 0.3240
  of the recomputed 0.3286; median agent/human ratio 59.7 over the 105 won levels. The untraced
  "median agent/human ratio 35-145" is RETIRED. Train contrast
  (runs/decompose_e2_hash_25x10_train.json): AT HUMAN 8.0060, median ratio 19.4, 29 won levels of
  index 3+ (all tu93, 8 of 80 runs).
- 100,000 actions: WITHDRAWN; NO budget claim holds until E3. The old line "0.3615 vs 0.3329 —
  coverage does not pay" compared different mechanisms, so it never measured what a larger budget
  buys: 0.3615 is the held-out mean of mode base, 2 seeds, at 100,000 actions
  (runs/ablate_kaggle_giveup_100k.json; its three give-up variants give the same value; the file
  has no hash_state rows); 0.3329 was hash_state, 4 seeds, at 20,000 actions. Corrected
  26 Sep 2026; see docs/archive/TOG_PLAN_v2.md RQ1. E3 is registered in docs/archive/TOG_PLAN_v2.md Section 7.
- Selection transfer (runs/split_transfer.json; 4-seed 6-mechanism matrix, corrected 26 Sep 2026):
  on the fixed 8/17 split the train pick is repeat_key (held-out 0.1464). hash_state is
  held-out-best (0.3329, 4-seed value) but ranks 6 of 6 on train, so it was never a train pick;
  the old "train pick held-out-best for 3 of 17 games" described hash_state. Per-game oracle 0.3632,
  cross-fitted 0.2517. Over 10,000 random splits the pick is held-out-best in 1.1% of splits vs
  16.7% chance; mean Kendall tau -0.43. The 1-seed exploratory matrix gives mean tau +0.37, so
  "rankings reverse" is not general.
- G-NAV planner (g_nav.py, hook on g_agent.py): train 0.70 vs 0.18 (all tu93), held-out 0.24-0.26
  vs 0.33 (hash_state on the same 4 seeds; loss is sp80); goal_confirmed 0 of 17. v2 census
  (runs/census_v2.json, 4 seeds): 14 of 17 held-out games have keyboard input, 11 an object the keys
  move. No keys r11l s5i5 tn36; no controllable object cd82 sb26 su15; 2-D lattice walker cn04 ka59
  re86 sp80 g50t; 1-D walker bp35 sk48 sc25 (sc25 weak: only key 3 passed the press test);
  key-controlled non-walker ar25 wa30 tr87. The category rule codifies the earlier census and is not
  pre-registered. ar25 level 1: G-NAV 8 of 8 runs (v1 and v2, 4 seeds each) vs hash_state 0 of 4
  seeds (the same four runs appear in three files) — UNEXPLAINED, report as such, never build on it.
- E1 (docs/E1_result.md, runs/e1_decision.json): Rudakov et al. agent, 10 seeds x 20,000 actions,
  INCONCLUSIVE by (ii): M2/M1 = 4.05 against > 5 (M1 0.1750, M4 3.30). Confounded by the absence
  of ACTION7, their choose_action raising on most actions in most runs, and preview vs 2026
  games/API. RQ4 NOT ESTABLISHED; no family claim.
- E1c CLOSED 26 Sep 2026 (docs/E1c_search.md): no admissible second independent agent. ZubMono
  "Prometheus" rejected (docs/E1c_prometheus_check.md): its direction priors were measured on all
  25 public games, including the 17 held-out; A5 forbids removing them. The remaining MIT
  candidates (conchocon154, ReplicaWormhole) are not pursued, for cost against the deadline, not
  quality. The strongest non-LLM agents found have no licence (BDR-Pro v79 = the old "0.26-0.27
  agent", Cryptic2-0, Curio, Hunter-Seeker v2). Related-work finding: most higher-scoring non-LLM
  notebooks load the game's source and search its simulator (docs/E1c_search.md Section 8), so they
  are not frame-only and their scores are not comparable with ours.
- Plan of record: docs/TOG_PLAN_v3.md (see "Current objective"; decided 26 Sep 2026, first
  recorded in docs/archive/TOG_PLAN_v2.md "Plan of record"). The ARC-AGI-3 results above stand as
  recorded.
- Ten mechanisms killed with measured reasons (docs/HANDOFF_GNAV.md).

## Corrections imposed by the audit (audit/TOG_PLAN_RUTHLESS_AUDIT.md) — standing instructions

- Rudakov, Shock, Cowley, "Graph-Based Exploration for ARC-AGI-3 Interactive Reasoning Tasks" (arXiv 2512.24156, code at
  github.com/dolphin-in-a-coma/arc-agi-3-just-explore) is a published frame-based agent that solved a
  median 30/52 preview levels. Never write that frame-only agents plateau. Run their agent on the
  current 25 public games through our harness (E1) and report what happens.
- "The barrier is goal inference" is not supported by counters alone. Allowed wording: "goal
  identification is the dominant observed failure mode for this instrument on this public subset".
  The intervention that could support more: on tu93/dc22/ls20 (source-informed), supply the true
  goal to g_nav.py with everything else unchanged and measure; and a narrow formal definition of
  goal-identification cost with a restricted ambiguity result, measured on the 25 games.
- Analytic ceiling (E4) is derived from arc_agi/scorecard.py, not from the technical report's
  prose equations, and validated against the scorecard on toy cases including the environment cap.
- Selection transfer (E5): the 6-mechanism x 4-seed lenovo matrix is primary; the 20 x 1 Kaggle
  matrix is exploratory; selection statistic fixed before analysis; 10,000 random 8/17 splits.
- 25 public games are a demonstration subset, not a sample of ARC-AGI-3; no sentence about the
  private set, no "unseen ARC-AGI-3 test set".
- Cite: ARC-AGI-3 technical report, launch post, preview 30-day learnings, human-performance
  paper, Milestone-1 write-ups; Balla et al. 2020; Kunanusont et al.; Stephenson et al. 2025;
  Blum & Hardt 2015; Roelofs et al. 2019; Introspective Environment Modeling; AgentRx; BALROG.
  Corrections from docs/PRIOR_ART_KILL.md (27 Sep 2026):
  - Kunanusont, Lucas, Pérez-Liébana 2017 (CEC) is a pixel-input DQN paper, not a forward-model
    paper. The GVGAI forward-model paper is Dockhorn & Apeldoorn 2018 (IEEE CIG).
  - MDP Playground (Rajan et al.) is JAIR 77, 2023, not JMLR.
  - "Stephenson et al. 2025" is UNIDENTIFIED; RKM to confirm which paper (PRIOR_ART_KILL.md 14b).
  - Rudakov et al.'s full title ends "for ARC-AGI-3 Interactive Reasoning Tasks".
  - The "human-performance paper" appears to be the ARC Prize blog post "Measuring Human
    Performance on ARC-AGI-3" plus the technical report's human section.
  Must-cite additions (PRIOR_ART_KILL.md Part B):
  - Twin (Skoutnev et al., arXiv:2608.14490);
  - Tycho (Lehmann et al., arXiv:2607.28287);
  - OPINE-World (Courtis et al., arXiv:2607.01531);
  - Liew, "Explore Before You Solve" (arXiv:2605.25931);
  - DiG-bench (Battleday et al., arXiv:2608.12593);
  - Bontrager et al. 2016 (AIIDE);
  - Gaina et al. 2018 (IEEE CIG);
  - Laidlaw et al. 2023 (NeurIPS).
- Method paper across three benchmarks (venues in "Current objective"); double-anonymous:
  no names, handles, affiliations in manuscript or code.
- E1 decision thresholds are written down in docs/ BEFORE any external agent is run.

## Repository layout

- scripts/   all runnable code (g_agent.py, g_nav.py, g_nav_run.py, g_decompose.py, ...)
- runs/      every JSON a script produced, named <experiment>_<machine>_<seeds>.json, never edited
- docs/      STATE.md, TOG_PLAN_v3.md, METHOD_BLUEPRINT.md, HANDOFF_GNAV.md, manuscript drafts;
             docs/archive/ TOG_PLAN_v1.md (was docs/TOG_PLAN.md), TOG_PLAN_v2.md
- audit/     external reviews of the plan or drafts
- external/  third-party agents for E1, each in its own folder with LICENSE and commit hash
- kaggle_*/  lab notebook builders' output folders (never a submission kernel)

## Open tasks, in order (updated 27 Sep 2026)

Done: docs/archive/TOG_PLAN_v2.md with audit corrections and E1 thresholds (plus the 3.3 precedence); E4
(runs/ceiling.json); E5 (runs/split_transfer.json); census table (runs/census_v2.json); E1a
Rudakov et al. adapter, protocol and 10-seed run, INCONCLUSIVE (docs/E1_result.md); E2 hash_state
10 seeds (runs/navrun_e2_hash_25x10.json); E2 decomposition (runs/decompose_e2_hash_25x10_*.json);
E1c search, closed with no admissible second agent (docs/E1c_search.md); E3 budget curve
(runs/e3_curve.json); E9 goal oracle, INCONCLUSIVE (runs/e9_report.json, docs/E9_protocol.md).
Method, benchmarks and venue decided 26 Sep 2026 (docs/TOG_PLAN_v3.md Sections 1, 3, 5); the method
is registered only when docs/PREREG.md is tagged. W0 so far: plan archive, carry-over
(docs/PLAN_MERGE_20260927.md), METHOD_BLUEPRINT.md draft 1.1, reconciliation with STATE.md
(docs/RECONCILE_20260927.md), frozen census constants (docs/PREREG_PARAMS.md).
Entry point for a new session: docs/STATE.md.

1. W0, rest (docs/TOG_PLAN_v3.md Section 6): docs/PRIOR_ART_KILL.md; gate G0; Procgen install
   test in a Python 3.10 venv; suite C decision.
2. W1: docs/PREREG.md v1 with final numbers, ground-truth tables, agent list, pilot set (each
   benchmark's selection split fixed before any mechanism is measured on it); analysis scripts
   with synthetic tests; tag prereg-v1 (+ OSF); then E6 (census at 10 seeds on all 25 ARC games
   under the tagged code, mandatory). No new run before the tag except the registered W0
   infrastructure checks (docs/W0_CHECKS.md).
3. W2-W5: adapters, fidelity script, I1 feasibility, pilot, PREREG v1.1; confirmatory runs (RKM);
   frozen analysis.
4. ARC-AGI-3 items (closed 27 Sep 2026): E6 census at 10 seeds (category rule frozen by code
   hash before the run) is W1 above; E10 is carried by G; E9 arm P, E1b and E7 are dropped.
5. Manuscript for the method paper, anonymised (JAIR format); reproduction script that regenerates
   every table from runs/.
