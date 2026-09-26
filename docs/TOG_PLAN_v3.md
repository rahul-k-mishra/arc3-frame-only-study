# TOG_PLAN_v3.md

Plan of record for the paper from the ARC-AGI-3 frame-only work. Supersedes TOG_PLAN.md (the ARC-only measurement plan) and TOG_PLAN_v2.md (the E1 external-agents protocol). Archive both, do not delete them — they are the record of the ARC-only programme and its registered rules.

Written 27 September 2026 from the decision of 26 September 2026. docs/STATE.md remains the single source of truth for numbers and run files; where this file and STATE.md disagree, STATE.md wins and this file is corrected.

---

## 1. Decision record (26 September 2026)

What was decided:

- The ARC-only short paper is not shipped. The measurement programme on the 25 public ARC-AGI-3 games is complete and every number in it is traceable to a file in runs/; it becomes background for a larger paper, not a paper of its own.
- The work is strengthened, with more compute and more datasets, into a method paper: the assumption census and the goal-identification measure, pre-registered and frozen, demonstrated on three CPU-runnable benchmarks — ARC-AGI-3 as one instance, MiniGrid/BabyAI, and one more suite (Section 5).
- Venue order: JAIR first, IEEE Transactions on Games second. TMLR is rejected. IEEE CoG and any conference whose acceptance requires paid registration or travel is ruled out. No venue with an APC.
- Work continues in the private GitHub repository with Claude Code writing scripts and documents; RKM runs every experiment and pastes console output; a fresh chat starts from docs/STATE.md.

Why (the two closures that forced it):

- E1c closed with no admissible second independent agent. The ARC-only paper's transfer claim rested on a single independent agent (Rudakov, Shock & Cowley) whose E1 result was inconclusive with three recorded confounds. Without a second, the ARC-only paper could not make the class claim.
- E9, the goal-oracle intervention on the source-informed train games, returned tu93 MIXED, dc22 NOT BINDING, ls20 not expressible. Goal identification is not a single binding barrier across games. That removes the thesis the short paper was built around and is exactly why the new paper is a census (a vector of assumptions, each measured) rather than a one-barrier claim.

Constraints that shape everything below: CPU only (lenovo, 8 workers; Kaggle CPU sessions); no GPU; no money for fees or travel; runtime is not a constraint — full-scale designs, no scope trimmed for compute.

---

## 2. The ARC-AGI-3 record (complete; background only in the new paper)

Frozen evidence, by file. Numbers are those recorded in STATE.md and are quoted here only to identify the runs; the paper cites the files.

| Item | File | What it established |
|---|---|---|
| E1 | runs/ (Rudakov, 25 × 10 × 20,000) | independent agent M1 0.1750; inconclusive against the rules, three confounds recorded in docs/E1_result.md |
| E1c | STATE.md entry | search for a second admissible independent agent: closed, none |
| E2 | runs/navrun_e2_hash_25x10.json | reference explorer held-out M1 0.3274 (10 seeds), M4 10.50; M2/M1 4.05 against the > 5 rule |
| Census v2 | runs/census_v2.json, docs/census_v2.md | assumption tallies on all 25 games; goal_confirmed 0 in every seed |
| Selection transfer | runs/split_transfer.json | ranking on train does not transfer to held-out |
| Ceiling | runs/ceiling.json | analytic scoring ceiling — ARC-scoring-specific, stays out of the method paper's tests |
| E9 | STATE.md entry | goal-oracle on train games: tu93 MIXED, dc22 NOT BINDING, ls20 not expressible |
| Split | HELDOUT.md | 8 train / 17 held-out (dc22 moved to train); the 8 train games are the parameter-freezing set |

Rules from TOG_PLAN.md and TOG_PLAN_v2.md that carry forward unchanged: the admissibility procedure (per-action time threshold, fidelity check), rule precedence (BREAKS before REPRODUCES; missing-scorecard clause first), and "no statement without a run RKM executed".

What from the ARC record enters the method paper: one background paragraph (the census exists, was frozen on 8 games, and its held-out ARC results are reported, not tested) and the E9 verdicts as the reason a vector measure is needed. Nothing else.

---

## 3. The new paper, in one paragraph

A fixed, cheap, frame-only probe battery (the assumption census: A1 input coupling, A2 one controlled object, A3 lattice motion, A4 blocking by a fixed obstacle set, A5 place goal) together with a defined goal-identification cost G, with every parameter frozen on the eight ARC-AGI-3 training games, (i) reports the ground-truth mechanics of unseen games in three suites at a registered accuracy (instrument validity), and (ii) predicts, before any agent is run, on which unseen games assumption-driven frame-only agents complete the first level (predictive validity). Both halves must hold. ARC-AGI-3 is the development instance and does not count toward generality.

The full draft protocol is docs/METHOD_BLUEPRINT.md (draft 1, 26 September). It becomes docs/PREREG.md once the numbers are final and it is tagged.

Corrections to METHOD_BLUEPRINT.md draft 1, from the record:

1. Section 1 says the goal-oracle intervention was never run. It was: E9. Replace with the E9 verdicts and the reading in Section 1 above.
2. Section 2.4 lists I2 as an independent agent "to find". E1c already searched and closed with none. I2 is removed; the search reopens only if ARC-AGI-3 Milestone-2 releases after 30 September add a permissive-licence, non-LLM, CPU frame-only agent.
3. Sections 4 and 8 name CoG or a workshop as the venue for the refute outcome. CoG is ruled out (paid registration, travel). The refute outcome is: repository record only; at most an arXiv note, no conference.

---

## 4. Frozen-protocol skeleton

PREREG.md is the authority once tagged. Until then, this is the skeleton (details in METHOD_BLUEPRINT.md Sections 2.1–2.8):

- Environment contract: reset(seed) → frame; step(action) → frame, level_end, game_end. Frames only. No reward, no text, no accepted flag. Determinism checked by a fidelity script per game before any census run.
- Census: five assumptions, one probe each, parameters copied from the v2 learner source with its commit hash (three agreeing presses, 2:1 margin, ≤10 px, ≤8 presses per key), outputs in {holds, fails, undetermined}, one JSON per (suite, game, seed). Perception on frame differences, to be re-verified on the 8 ARC train games before the change is accepted.
- G: two measured quantities (G_end, level ends until the registered hypothesis class is a singleton; G_act, actions to first level end per cell visited under the registered coverage policy). New script; never yet run on any game.
- Agents: R (E2 explorer), N (G-NAV planner), I1 (Rudakov, if adaptable outside ARC — feasibility documented either way). No I2.
- Tests and thresholds: V1 instrument validity, V2 predictive validity with a void precondition, V3 parameter transfer, V4 formal (or absent). Proposed numbers in METHOD_BLUEPRINT.md Section 2.6; RKM registers the final ones.
- Pilot: at most 6 MiniGrid environments and 2 games of suite C, named in advance, excluded from confirmatory analysis; changes logged as PREREG v1.1 diffs.
- Analysis scripts committed and unit-tested on synthetic data under the prereg tag; not edited afterwards except logged crash fixes.

---

## 5. Benchmarks

| Suite | Role | Status |
|---|---|---|
| ARC-AGI-3, 25 public | development instance; parameters frozen on the 8 train games | runs exist; only G measurement is new |
| MiniGrid + BabyAI, 178 environments | lattice suite; V1 positive control in the raw-action condition (A3 must fail by construction); V2 test in the absolute-move macro condition | installed in .venv_games |
| Suite C: Procgen, 16 games (recommended) | non-lattice generality test: pixel physics, textures, explicit level_complete, deterministic per level seed | needs a Python 3.10 venv on the lenovo; install test is W0 |
| Fallback: ALE / Atari | only if Procgen cannot be installed | A1–A4 testable, G undefined (no level ends), prior art (Bellemare et al. 2012) on the same measurement |

Ground-truth tables docs/GROUND_TRUTH_minigrid.md and docs/GROUND_TRUTH_<suiteC>.md — per game, the A1–A5 truth vector with source file and line — are written and committed under the prereg tag before any run on B or C. They are both the V1 answer key and the pre-registered per-game predictions.

---

## 6. Order of work and gates

| Week | Work | Gate |
|---|---|---|
| W0 | reconcile METHOD_BLUEPRINT.md with STATE.md; docs/PRIOR_ART_KILL.md; Procgen install test in a 3.10 venv; decide suite C | G0: formal result non-trivial, yes or no (either continues) |
| W1 | PREREG.md v1 with final numbers, ground-truth tables, agent list, pilot set; analysis scripts with synthetic tests; git tag prereg-v1; OSF registration of the same file; re-verify ARC train census under frame-difference perception | G1: no run on any B or C game before the tag |
| W2 | env contract, MiniGrid adapter (raw + macro), suite C adapter, fidelity script; I1 adaptability documented; pilot; PREREG v1.1 with diff; tag prereg-v1.1 | G2 |
| W3–W4 | confirmatory census (V1) on B and C; agents on B-macro and C (V2); G on B, C and ARC 25 — RKM runs, pastes console | G3: outcome classified (support / partial / refute) before any results text is written |
| W5 | frozen analysis scripts run once; enumeration check; V4 verdict | |
| W6–W7 | manuscript in JAIR format; code and runs/ released; OSF link in the paper; submit | |

Outcome → venue, pre-committed: support → JAIR full article (research note as fallback if V4 is dropped); partial → IEEE ToG; refute → repository record, at most an arXiv note.

---

## 7. Rules for this repository from now on

1. No claim without a run RKM executed. Every number in any docs/ file or manuscript cites a runs/ file and the script that produced it.
2. Thresholds before runs. A test that was not in the tagged PREREG.md before its run is reported as exploratory and does not enter a claim.
3. PREREG.md, once tagged, changes only by a new version with an explicit diff section. Analysis scripts are frozen at the tag.
4. Scripts are parallel (worker pool), deterministic given seed, resume-safe, one JSON per unit of work; run commands are given in order, copy-pasteable, with the working directory, in fenced code blocks.
5. STATE.md is updated at the end of every session: what was run, which file, what changed in the plan.
6. Manuscript language: plain, no overclaiming, no "state of the art", every mathematical step on the page, and an explicit account of what the method can and cannot do.
7. Venues: JAIR, then IEEE ToG. Nothing with fees or required travel.

---

## 8. Open decisions (owner: RKM)

1. Suite C: Procgen (3.10 venv) or ALE fallback — after the W0 install test.
2. Whether Section 5 of METHOD_BLUEPRINT.md (the formal result) is attempted, given G0.
3. Per-suite action budget: the E2 value of 20,000 everywhere, or registered per suite after the fidelity script.
4. JAIR first (calendar cost, roughly four to nine months to a decision) or ToG first.
5. OSF registration in addition to the git tag (recommended: both).

---

## 9. What supersedes what

- TOG_PLAN.md → archived as docs/archive/TOG_PLAN_v1.md; TOG_PLAN_v2.md (E1 external-agents protocol) → archived as docs/archive/TOG_PLAN_v2.md. Their rules remain the ARC record.
- METHOD_BLUEPRINT.md draft 1 → corrected per Section 3 → PREREG.md v1 at the W1 tag.
- CLAUDE.md → the method-paper section (see CLAUDE_md_method_paper_section.md) replaces any earlier "current objective" section; everything else in CLAUDE.md stays.
