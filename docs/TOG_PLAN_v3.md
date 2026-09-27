# TOG_PLAN_v3.md

Plan of record for the paper from the ARC-AGI-3 frame-only work. Supersedes docs/archive/TOG_PLAN_v1.md (formerly docs/TOG_PLAN.md, the ARC-only measurement plan) and docs/archive/TOG_PLAN_v2.md (formerly docs/TOG_PLAN_v2.md, the E1 external-agents protocol). Both were archived on 27 September 2026, not deleted — they are the record of the ARC-only programme and its registered rules. Everything in the method-paper decision as first recorded in docs/archive/TOG_PLAN_v2.md ("Plan of record") and CLAUDE.md (commit 1af3a1e) that this file lacked is in Section 10; the item-by-item record is docs/PLAN_MERGE_20260927.md.

Written 27 September 2026 from the decision of 26 September 2026. docs/STATE.md remains the single source of truth for numbers and run files; where this file and STATE.md disagree, STATE.md wins and this file is corrected.

---

## 1. Decision record (26 September 2026)

What was decided:

- The ARC-only short paper is not shipped. The measurement programme on the 25 public ARC-AGI-3 games is complete and every number in it is traceable to a file in runs/; it becomes background for a larger paper, not a paper of its own.
- The work is strengthened, with more compute and more datasets, into a method paper: the assumption census and the goal-identification measure, pre-registered and frozen, demonstrated on three CPU-runnable benchmarks — ARC-AGI-3 as one instance, MiniGrid/BabyAI, and one more suite (Section 5).
- Pre-registration (27 September 2026): docs/PREREG.md v1, git tag prereg-v1 on commit 19f2a9f25043997d1deffd5976f2f2150e5f086f. OSF open-ended registration https://osf.io/2znhw (embargoed until 30 June 2030, to be ended early at acceptance). The manuscript for review cites the anonymised view-only link https://osf.io/2znhw/overview?view_only=f82b8a3e8a7f48ca94a952495e9520d3; the camera-ready cites the public URL.
- Venue order: JAIR first, IEEE Transactions on Games second. TMLR is rejected. IEEE CoG and any conference whose acceptance requires paid registration or travel is ruled out. No venue with an APC.
- Work continues in the private GitHub repository with Claude Code writing scripts and documents; RKM runs every experiment and pastes console output; a fresh chat starts from docs/STATE.md.

Why (the two closures that forced it):

- E1c closed with no admissible second independent agent. The ARC-only paper's transfer claim rested on a single independent agent (Rudakov, Shock & Cowley) whose E1 result was inconclusive with three recorded confounds. Without a second, the ARC-only paper could not make the class claim.
- E9, the goal-oracle intervention on the source-informed train games, returned tu93 MIXED, dc22 NOT BINDING, ls20 NOT TESTABLE (its goal predicate is not a place); overall verdict INCONCLUSIVE (docs/STATE.md Section 2, runs/e9_report.json). Goal identification is not a single binding barrier across games. That removes the thesis the short paper was built around and is exactly why the new paper is a census (a vector of assumptions, each measured) rather than a one-barrier claim.

Gate G0 outcome (27 September 2026): cite and drop the theorem. The prior-art check (docs/PRIOR_ART_KILL.md) found no paper that kills any claim component. Statement 1's identification half and Statement 2 are covered by Goldman & Kearns 1995 and version-space elimination, and Statement 1's cost half by immobile-hider search games. G_end and G_act stay as registered, measured quantities (METHOD_BLUEPRINT.md Section 5, draft 1.4); the paper proves no theorem, and V4 is removed.

Constraints that shape everything below: CPU only (lenovo, 8 workers; Kaggle CPU sessions); no GPU; no money for fees or travel; runtime is not a constraint — full-scale designs, no scope trimmed for compute.

---

## 2. The ARC-AGI-3 record (complete; background only in the new paper)

Frozen evidence, by file. Numbers are those recorded in STATE.md and are quoted here only to identify the runs; the paper cites the files.

| Item | File | What it established |
|---|---|---|
| E1 | runs/e1_decision.json, runs/e1_rudakov_lenovo_25x10_20k.json (Rudakov, 25 × 10 × 20,000) | independent agent M1 0.1750, M4 3.30; INCONCLUSIVE by (ii), M2/M1 4.05 against the > 5 rule; three confounds recorded in docs/E1_result.md |
| E1c | no run file; docs/E1c_search.md, docs/E1c_prometheus_check.md | search for a second admissible independent agent: closed, none; Prometheus rejected |
| E2 | runs/navrun_e2_hash_25x10.json | reference explorer (hash_state) held-out M1 0.3274 (10 seeds × 20,000 actions, 170 runs), M4 10.50; the reference for every comparison |
| E2 decomposition | runs/decompose_e2_hash_25x10_heldout.json, runs/decompose_e2_hash_25x10_train.json | where E2's score comes from, by level index and agent/human ratio |
| E3 | runs/e3_curve.json; inputs runs/navrun_e3_hash_25x4_3k.json, runs/navrun_e3_hash_25x4_50k.json, runs/navrun_e3_hash_25x4_100k.json (20k point = 4-seed subset of runs/navrun_e2_hash_25x10.json) | hash_state budget curve, 3k / 20k / 50k / 100k actions: M1 flat, more actions buy levels worth nothing |
| Census v2 | runs/census_v2.json, docs/census_v2.md; inputs runs/navrun_v2_heldout.json (G-NAV v2, held-out, 4 seeds), runs/navrun_v2_train_quick.json (train, 2 seeds × 3,000: below the 4-seed minimum) | assumption tallies on all 25 games; goal_confirmed 0 in every seed |
| G-NAV v1 | runs/navrun_heldout_full.json | G-NAV v1 held-out runs, 4 seeds; goal_confirmed 0; ar25 level-1 wins (4 of the 8) |
| Selection transfer | runs/split_transfer.json; matrices runs/ablate_lenovo_6x4.json (primary, 6 × 4) and runs/ablate_kaggle_20x1.json (exploratory, 20 × 1) | ranking on train does not transfer to held-out |
| Ceiling | runs/ceiling.json | analytic scoring ceiling — ARC-scoring-specific, stays out of the method paper's tests |
| E9 | runs/e9_report.json, runs/navrun_e9_oracle_3x10.json; docs/E9_protocol.md | goal-oracle on train games: INCONCLUSIVE; tu93 MIXED, dc22 NOT BINDING, ls20 NOT TESTABLE |
| ar25 duplicate check | runs/decompose_ar25_three_files_heldout.json | the same four hash_state runs sit in three files; hash_state 0 of 4 seeds on ar25 level 1 vs G-NAV 8 of 8; unexplained |
| Withdrawn 100k line | runs/ablate_kaggle_giveup_100k.json | mode base, 2 seeds, 100,000 actions; its "0.3615 vs 0.3329" comparison is WITHDRAWN (docs/STATE.md Section 3) and replaced by E3 |
| Split | docs/HELDOUT.md, copied unchanged on 27 Sep 2026 from D:\Research\arc3\brutus\HELDOUT.md; SHA-256 8c07813ab01f5228a6af10f91771702dad0291f26b0f920892ef3a79763a122d | 8 train / 17 held-out (dc22 moved to train); the 8 train games are the parameter-freezing set |

Rules from docs/archive/TOG_PLAN_v1.md and docs/archive/TOG_PLAN_v2.md that carry forward unchanged: the admissibility procedure (per-action time threshold, fidelity check), rule precedence (BREAKS before REPRODUCES; the card-count clause — rows lacking per-level scorecard counts give INCONCLUSIVE — first), and "no statement without a run RKM executed".

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
- Tests and thresholds: V1 instrument validity, V2 predictive validity with a void precondition, V3 parameter transfer. (V4 removed at gate G0, 27 Sep 2026.) Proposed numbers in METHOD_BLUEPRINT.md Section 2.6; RKM registers the final ones.
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
| W0 | reconcile METHOD_BLUEPRINT.md with STATE.md; docs/PRIOR_ART_KILL.md; Procgen install test in a 3.10 venv; decide suite C | G0: formal result non-trivial, yes or no — closed 27 Sep 2026: no; cite and drop (docs/PRIOR_ART_KILL.md Part D) |
| W1 | PREREG.md v1 with final numbers, ground-truth tables, agent list, pilot set; analysis scripts with synthetic tests; git tag prereg-v1; OSF registration of the same file; E6 (census at 10 seeds on all 25 ARC games under the tagged code, mandatory) | G1: no run on any B or C game before the tag |
| W2 | env contract, MiniGrid adapter (raw + macro), suite C adapter, fidelity script; I1 adaptability documented; pilot; PREREG v1.1 with diff; tag prereg-v1.1 | G2 |
| W3–W4 | confirmatory census (V1) on B and C; agents on B-macro and C (V2); G on B, C and ARC 25 — RKM runs, pastes console | G3: outcome classified (support / partial / refute) before any results text is written |
| W5 | frozen analysis scripts run once | |
| W6–W7 | manuscript in JAIR format; code and runs/ released; OSF link in the paper; submit | |

Outcome → venue, pre-committed: support → JAIR full article; partial → IEEE ToG; refute → repository record, at most an arXiv note.

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

## 8. Decisions (owner: RKM) — all closed 27 September 2026

1. Suite C: **Procgen** (3.10 venv; W0 check C1 passed).
2. The formal result (METHOD_BLUEPRINT.md Section 5): **dropped** per docs/PRIOR_ART_KILL.md Part D. Cite, do not prove.
3. Per-suite action budget: **20,000 actions per game on every suite**, unless the fidelity script forces a registered per-suite value.
4. JAIR first or ToG first: **decided at gate G3 by outcome** (Section 6 pre-commitment).
5. OSF registration: **yes**, alongside the git tag.
6. Install, timing and fidelity probes before the tag: **registered infrastructure checks, not experiments** (docs/W0_CHECKS.md).
7. The working title: **deferred to G3**.
8. The open ARC-AGI-3 items: **E6 is mandatory in W1 under the tagged code; E10 is carried by G; E9 arm P, E1b and E7 are dropped.**

---

## 9. What supersedes what

- TOG_PLAN.md → archived as docs/archive/TOG_PLAN_v1.md; TOG_PLAN_v2.md (E1 external-agents protocol) → archived as docs/archive/TOG_PLAN_v2.md (done 27 September 2026). Their rules remain the ARC record.
- METHOD_BLUEPRINT.md draft 1 → corrected per Section 3 (draft 1.1, 27 September 2026; reconciled against STATE.md in docs/RECONCILE_20260927.md) → PREREG.md v1 at the W1 tag. The census parameters it copies are listed from source in docs/PREREG_PARAMS.md.
- CLAUDE.md → the method-paper section ("Current objective", "Rules that bind every task", "Open decisions") replaced the 1af3a1e method-paper text on 27 September 2026; everything else in CLAUDE.md stays.

---

## 10. Carried over from TOG_PLAN_v2.md and CLAUDE.md, 27 Sep 2026

Items of the method-paper decision as recorded in docs/archive/TOG_PLAN_v2.md "Plan of record" (commit c1eea2c) and CLAUDE.md (commit 1af3a1e) that Sections 1–9 lacked. One row each in docs/PLAN_MERGE_20260927.md. Where docs/STATE.md contradicts an item, STATE.md is followed and the contradiction is recorded there.

Standing, from the 26 September decision:

1. Every ARC-AGI-3 result stands as recorded, with its protocol, checks and limits: E1, E1c, E2, E3, E4, E5, E9 and the census (docs/STATE.md Section 2; files in Section 2 above). Nothing already measured is re-run or re-decided because of the change of target. New ARC measurements named in this plan (G on the ARC 25; the ARC train census under frame-difference perception) are new runs under PREREG.md, not re-runs of recorded results, and change no recorded number.
2. The rules of the ARC programme apply to every new benchmark: a selection split fixed before any mechanism is measured (for suites B and C: the declared pilot set against the confirmatory set, named in PREREG.md v1 before any run); a registered protocol before any run; games as the unit, seeds nested; CPU only, no money; double-anonymous.
3. Double-anonymous: no names, handles, affiliations, acknowledgements or identifying links in the manuscript, the supplement or the code release. This holds whatever the venue's own review policy.
4. No new run before a registered protocol. This is stricter than gate G1, which names only B and C games. Whether the W0 Procgen install test (one game, 1,000 steps) and the timing and fidelity probes count as "new runs" is an open decision for RKM (item 11); none of them may produce a number that enters a document.
5. The method is stated so that it applies unchanged to every benchmark: its inputs, its outputs, and what would show it fails. Sections 3–4 and METHOD_BLUEPRINT.md Sections 2 and 4 are that statement in draft; it is registered only when PREREG.md v1 is tagged.
6. Superseded: the ARC-only short paper (6–8 pages, IEEE CoG or a workshop, the 9 October 2026 venue choice) and the ARC-only 10-page ToG full paper. IEEE ToG as the second venue of the method paper (Section 1) is a different paper and is not affected.
7. The GVGAI learning track, named in docs/archive/TOG_PLAN_v2.md Section 7 as an optional second CPU benchmark, was a candidate, not a choice. It is not among the suites of Section 5 and is not added as an option without RKM's decision.

Open ARC-AGI-3 items (docs/STATE.md Section 5 lists each as open; STATE.md is followed over Section 2's word "complete"):

8. E6: census at 10 seeds on all 25 games, category rule frozen by code hash before the run (docs/archive/TOG_PLAN_v2.md Section 7). Relation to W1 step 7 (re-verifying the 8 train games under frame-difference perception) is for RKM to decide. Closed 27 Sep 2026: E6 is mandatory in W1 under the tagged code (Section 8, item 8).
9. E10: formal goal-identification cost; hypothesis class fixed and hashed before use (docs/archive/TOG_PLAN_v2.md Section 6). In this plan it is carried by G (Section 4); the E10 name is kept so the ARC record stays traceable. (V4 removed at G0, 27 Sep 2026.)
10. Optional: E9 arm P (coordinate oracle, outside the verdict; run or drop, docs/E9_protocol.md Section 3); E1b organiser templates (baseline only); E7 14B LLM cost. Closed 27 Sep 2026: all three dropped (Section 8, item 8).

Open decisions added to Section 8 by this carry-over (owner: RKM):

11. Whether install, timing and fidelity probes before the tag count as new runs (item 4).
12. The working title: replaced once the method is registered; it may claim no more than the evidence across the chosen benchmarks supports.

Deliverables carried:

13. The manuscript is anonymised, and a reproduction script regenerates every table from runs/.
