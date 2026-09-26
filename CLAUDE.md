# CLAUDE.md — arc3-frame-only-study

Measurement study of frame-only, prior-free, CPU-runnable agents on the ARC-AGI-3 public
demonstration set (25 games), targeted at a 6-8 page short paper for IEEE CoG or a workshop
(venue chosen 9 October 2026; double-anonymous). Single author. No GPU. No money. Every number in
any document must come from a script in this repository run by the author, with its output saved
under runs/.

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
  26 Sep 2026; see docs/TOG_PLAN_v2.md RQ1. E3 is registered in TOG_PLAN_v2 Section 7.
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
- Plan of record (TOG_PLAN_v2 Sections 0 and 9): the short-paper route, 6-8 pages, IEEE CoG or a
  workshop, venue chosen 9 Oct 2026. The 10-page ToG full paper is not pursued.
- Ten mechanisms killed with measured reasons (docs/HANDOFF_GNAV.md).

## Corrections imposed by the audit (audit/TOG_PLAN_RUTHLESS_AUDIT.md) — standing instructions

- Rudakov, Shock, Cowley, "Graph-Based Exploration for ARC-AGI-3" (arXiv 2512.24156, code at
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
- 6-8 page short paper (IEEE CoG or a workshop, venue chosen 9 October 2026); double-anonymous:
  no names, handles, affiliations in manuscript or code.
- E1 decision thresholds are written down in docs/ BEFORE any external agent is run.

## Repository layout

- scripts/   all runnable code (g_agent.py, g_nav.py, g_nav_run.py, g_decompose.py, ...)
- runs/      every JSON a script produced, named <experiment>_<machine>_<seeds>.json, never edited
- docs/      HANDOFF_GNAV.md, TOG_PLAN.md, TOG_PLAN_v2.md, manuscript drafts
- audit/     external reviews of the plan or drafts
- external/  third-party agents for E1, each in its own folder with LICENSE and commit hash
- kaggle_*/  lab notebook builders' output folders (never a submission kernel)

## Open tasks, in order (updated 26 Sep 2026)

Done: TOG_PLAN_v2 with audit corrections and E1 thresholds (plus the 3.3 precedence); E4
(runs/ceiling.json); E5 (runs/split_transfer.json); census table (runs/census_v2.json); E1a
Rudakov et al. adapter, protocol and 10-seed run, INCONCLUSIVE (docs/E1_result.md); E2 hash_state
10 seeds (runs/navrun_e2_hash_25x10.json); E2 decomposition (runs/decompose_e2_hash_25x10_*.json);
E1c search, closed with no admissible second agent (docs/E1c_search.md).

1. E3 budget curve: hash_state at 3,000 / 50,000 / 100,000 actions with E2 as the 20,000 point,
   reported by scripts/e3_curve.py after its checks pass. Until it exists, no budget claim.
2. E6 census at 10 seeds on all 25 games, category rule frozen (code hash) before the run.
3. E9 goal-oracle intervention on tu93/dc22/ls20 (tu93 as positive control); E10 formal
   goal-identification cost with the restricted ambiguity result.
4. 9 Oct 2026: venue decision between IEEE CoG and a workshop for the short paper. Optional,
   baseline only: E1b official non-LLM templates; E7 14B LLM cost.
5. Manuscript on the short-paper route (6-8 pages), anonymised; reproduction script that
   regenerates every table from runs/.
