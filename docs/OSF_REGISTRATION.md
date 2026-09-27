# OSF_REGISTRATION.md — text for the OSF open-ended registration

RKM pastes the text between the two rules into an OSF open-ended registration, after creating the git tag. The commit hash is filled in from `git rev-parse prereg-v1`.

---

**Title:** [working title — deferred to gate G3] An assumption census for frame-only game agents: instrument validity and prediction of first-level success across three benchmark suites

**Claim.** A fixed, cheap, frame-only probe battery (the assumption census: A1 input coupling, A2 one controlled object, A3 lattice motion, A4 blocking by a fixed obstacle set, A5 place goal), with every parameter frozen on eight ARC-AGI-3 training games, (i) reports the ground-truth mechanics of unseen games at a registered accuracy, and (ii) predicts, before any agent is run, on which unseen games assumption-driven frame-only agents complete the first level. Ground truth is derived from each game's source code and committed before any run. A goal-identification cost G is measured and reported alongside, not tested. ARC-AGI-3 is the development instance and does not count toward generality.

**Tests and thresholds.**
- **V1, instrument validity:** per suite and assumption, agreement between the census and source-derived truth. PASS if agreement ≥ 0.90 and Cohen's κ ≥ 0.70; FAIL if agreement < 0.75. κ is used only where both truth values have at least three games; otherwise agreement alone.
- **V2, predictive validity:** per suite and agent.
  - PASS if AUROC(census score → level-1 completion) ≥ 0.80, its bootstrap 95% CI lower bound (2,000 resamples of games) is > 0.60, the balanced accuracy of the conjunctive prediction A2∧A3∧A4∧A5 is ≥ 0.80, and AUROC exceeds a nuisance logistic baseline (grid area, action count, colour count) by ≥ 0.10.
  - FAIL if AUROC ≤ 0.65.
  - VOID if fewer than 10% or more than 90% of games are completed.
  - Evidence agents: the author's explorer R and an independent agent I1. The author's planner N is an instrument check only.
- **V3:** census parameters identical on every suite.

**Suites and sample sizes.** Games are the unit; 10 seeds per game; 20,000 actions per (game, seed).

| suite | development / pilot | confirmatory |
|---|---|---|
| ARC-AGI-3 public set | 8 train games (development) | 17 held-out games: V2 reported, not tested |
| MiniGrid + BabyAI | 6 pilot | 161 environments; raw and absolute-move macro action conditions |
| Procgen (easy, sequential levels) | 2 pilot | 14 games; center_agent False primary, the scrolling view secondary; also reported on the 9 games inside the instrument's operating range |

**Pre-committed outcome and venue.**

| outcome | definition | venue |
|---|---|---|
| Support | V1 passes on MiniGrid/BabyAI (both conditions) and Procgen, V2 passes for R and I1 on MiniGrid/BabyAI-macro and Procgen, and V3 holds | JAIR full article |
| Partial | V1 passes everywhere, but V2 passes only on MiniGrid/BabyAI-macro, is void on Procgen, or passes on Procgen for R only | IEEE Transactions on Games full paper |
| Refute | V1 fails on any suite, V2 fails on MiniGrid/BabyAI-macro, or V2 is void everywhere | repository record only, at most an arXiv note |

**Protocol.** The full protocol is docs/PREREG.md v1 at git tag `prereg-v1`, commit `<fill: output of git rev-parse prereg-v1>`, in the project repository (released with the paper; anonymised for review). This registration and that file are the same protocol; where they differ, docs/PREREG.md v1 governs.

---
