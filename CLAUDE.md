# CLAUDE.md — arc3-frame-only-study

Measurement study of frame-only, prior-free, CPU-runnable agents on the ARC-AGI-3 public
demonstration set (25 games), targeted at IEEE Transactions on Games (10-page full paper,
double-anonymous). Single author. No GPU. No money. Every number in any document must come from
a script in this repository run by the author, with its output saved under runs/.

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

- hash_state explorer, held-out 4 seeds x 20,000 actions: mean 0.3329; every point from level 1 of
  tn36/r11l/sp80/cd82; level 3 never won in 1,088 held-out runs; median agent/human ratio 35-145.
- 100,000 actions: NO budget claim until E3. The old line "0.3615 vs 0.3329 — coverage does not pay"
  compared different mechanisms: 0.3615 is mode base (and its three give-up variants, identical),
  2 seeds, 100k (runs/ablate_kaggle_giveup_100k.json); 0.3329 was hash_state, 4 seeds, 20k.
  Corrected 26 Sep 2026; see docs/TOG_PLAN_v2.md RQ1.
- Selection on the one 8/17 split: train pick is held-out-best for 3 of 17 games; oracle 0.3632.
- G-NAV planner (g_nav.py, hook on g_agent.py): train 0.70 vs 0.18 (all tu93), held-out 0.24-0.26
  vs 0.33 (loss is sp80); goal_confirmed 0 of 17. v2 census (4 seeds): no keys r11l s5i5 tn36;
  no controllable object cd82 sb26 su15; 2-D lattice walker cn04 ka59 re86 sp80 g50t; 1-D walker
  bp35 sk48; key-controlled non-walker ar25 wa30 tr87. ar25 level 1: 4/4 nav seeds vs 0/12
  hash_state seeds — UNEXPLAINED, report as such, never build on it.
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
- 10 pages + supplement; double-anonymous: no names, handles, affiliations in manuscript or code.
- E1 decision thresholds are written down in docs/ BEFORE any external agent is run.

## Repository layout

- scripts/   all runnable code (g_agent.py, g_nav.py, g_nav_run.py, g_decompose.py, ...)
- runs/      every JSON a script produced, named <experiment>_<machine>_<seeds>.json, never edited
- docs/      HANDOFF_GNAV.md, TOG_PLAN.md, TOG_PLAN_v2.md, manuscript drafts
- audit/     external reviews of the plan or drafts
- external/  third-party agents for E1, each in its own folder with LICENSE and commit hash
- kaggle_*/  lab notebook builders' output folders (never a submission kernel)

## Open tasks, in order

1. docs/TOG_PLAN_v2.md: the plan with every audit correction applied; the E1 decision thresholds.
2. scripts/g_split_transfer.py (E5) and scripts/g_ceiling.py (E4): no game runs; outputs to runs/.
3. E1 adapters under external/: Rudakov et al. agent first; official non-LLM templates second
   (baseline, not independent evidence); verify licence, commit, CPU runtime.
4. E2/E3/E6: 10-seed hash_state, budget curve (3k/20k/50k/100k), 25-game census at 10 seeds.
5. Goal-oracle intervention on tu93/dc22/ls20; formal goal-identification cost definition.
6. Manuscript, 10 pages, anonymised; reproduction script that regenerates every table from runs/.
