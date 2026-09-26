> Superseded by docs/TOG_PLAN_v2.md; kept unedited as a record.

# Plan: IEEE Transactions on Games submission
## Working title: "Why Frame-Only Agents Plateau on ARC-AGI-3: Scoring Structure, Selection Transfer, and a Goal-Inference Census"

Prepared 25 September 2026. Every number below is from runs Rahul executed (lenovo, Kaggle CPU) unless marked NEED, in which case it does not exist yet and the paper cannot be written until it does.

---

## 0. Verdict on this plan, before anything else

What this paper is: a measurement study of a benchmark's structure and of what one family of agents (frame-only, prior-free, CPU-runnable) can and cannot do on it, with the reasons per game.

What this paper is not: a new method, a competitive result, or a claim about the hidden test set. Any draft that drifts toward those gets rejected, correctly.

Odds at ToG, honestly: reasonable IF the family study (E1) shows the same plateau and the same level-1-only signature for agents we did not write, AND the analytic ceiling (E4) is derived and matches the runs, AND the selection-transfer analysis (E5) is done over random splits rather than the one split we used. Without E1 the paper is about BRUTUS-G, and a paper about one home-built agent that failed is not archival. Without E4 it is a table of numbers with no explanation. Without E5 the selection claim rests on one split of one dataset.

Scope fit: ToG's stated scope includes "games for artificial intelligence" and "artificial general intelligence"; ARC-AGI-3 is a suite of 2-D games evaluated by human-relative efficiency. Fit is good. Category: full paper, 10-12 pages (fees above 10; above 12 needs justification in the cover letter). Double-anonymous review since 2025: no names, affiliations, acknowledgements, or identifying links (GitHub username, Kaggle handle, "our earlier paper") anywhere in the manuscript or the code release.

---

## 1. The paper in one paragraph

ARC-AGI-3 scores an agent per level by 100 * min(1.15, (human actions / agent actions)^2), weights levels by their index, averages over games, and counts unfinished levels as zero. We show, with the formula and with measurements, that this makes coverage without efficiency worthless: an explorer that wins level 1 of many games at 30-150 times the human cost scores under 0.4 of 100, and five times the action budget buys +0.03. We then show that selecting behaviour on a handful of public games does not transfer: across [E5 result] random train/held-out splits of 25 public games, the mechanism chosen on the train split is the held-out-best in [E5]% of cases, and the per-game oracle over 20 mechanisms is worth 0.03. Finally, we build a planner that verifies its own assumptions on the game it is playing and use its counters to classify every unseen game by which assumption fails: on 17 unseen games, 3 offer no keyboard, 3 no controllable object, 5 a clean lattice walker, 2 a one-dimensional walker, 3 a key-controlled object that is not a walker; and on none of the 14 with a controllable object does the first level end by reaching a place. The planner's only success (tu93) is the one game whose exit is a coloured tile. [E1 result: N other public frame-only agents show the same plateau and signature.] We conclude that the barrier is goal inference, not perception or search, and quantify what a CPU-hosted language model would cost per action (218-1,254 s against a required 2.9 s), explaining why every leaderboard leader runs a GPU-served vision model.

---

## 2. Research questions and claim status

RQ1. How does the ARC-AGI-3 scoring rule allocate credit, and what is the maximum score of an agent whose per-level cost is a multiple of the human baseline?
  Claims: formula analysis (HAVE: from arc_agi/scorecard.py); measured decomposition, 1,088 held-out runs (HAVE); counterfactuals AT HUMAN 3.0-3.8 vs recorded 0.30-0.46 (HAVE); 100k vs 20k actions +0.03 (HAVE); analytic ceiling curve (NEED: E4).

RQ2. Does mechanism selection on public games transfer to unseen public games?
  Claims: on one 8/17 split, train-selected mechanism is held-out-best for 3 of 17 games (HAVE); oracle 0.3632 vs selected 0.3329 (HAVE); over random splits (NEED: E5, no new runs, uses the existing 600+500-run ablation).

RQ3. Which assumption breaks, per unseen game, for a planner that verifies its assumptions at play time?
  Claims: census of 17 games, 4 seeds, per-key evidence (HAVE); goal_confirmed 0 of 17 (HAVE); tu93 exception with source-verified reason (HAVE, train game); 10-seed version (NEED: E6).

RQ4. Is the plateau a property of the agent family or of our agent?
  Claims: one independent public agent reports 0.26-0.27 and calls the programmatic track plateaued (HAVE, citation only); N public frame-only agents through the same harness on the same games and seeds (NEED: E1). This is the load-bearing experiment.

RQ5. What does a CPU-hosted LLM cost per action relative to the evaluation budget?
  Claims: 7B on two machines, two encodings, replies shown (HAVE); 14B (NEED: E7, cheap).

---

## 3. What reviewers will attack, and the answer for each

R1. "Confirms the benchmark's own thesis." Answer: the thesis is qualitative; we give the quantitative structure (squared efficiency, index weighting, the AT HUMAN counterfactual, the budget curve) and a per-game assumption census with evidence. State this in the introduction as the contribution, not as a discovery of the thesis.

R2. "n = 17 unseen games; the private set is 110." Answer: never claim beyond the public set; report intervals; note that the public set was authored by the same team with the same tooling; state the limitation in its own subsection.

R3. "One home-built agent." Answer: E1, or the paper does not go out.

R4. "The train/held-out split is one split." Answer: E5.

R5. "You read the source of three train games while building." Answer: declare it exactly: tu93, dc22, ls20 sources were read to debug the planner; no held-out source was ever opened; the census counters are defined before the held-out run and unchanged after. Put the timestamps in the supplement.

R6. "The planner is weak; a better planner would do better." Answer: agreed and stated; the planner is an instrument, not the contribution. Its counters classify games by the assumption that fails; that classification is the result, and it is robust to the planner's weakness only where the assumption is about the game (no keys, no controllable object, goal falsified by revisiting), not about the planner (frontier exhausted, stalled). Say which rows are which.

R7. "ar25 anomaly." Answer: report it as unexplained, with the numbers (4/4 vs 0/12), and do not build on it. A reviewer will trust the paper more for this than for hiding it.

R8. "Seeds: 4." Answer: E6 and E2 give 10 seeds with bootstrap intervals for every reported mean.

R9. "Live competition; results will be stale." Answer: fix the snapshot (game set version, engine version arc-agi 0.9.8, arcengine 0.9.3, date); cite the leaderboard state at submission; the scoring analysis does not depend on the leaderboard.

R10. "Where is the code?" Answer: anonymised repository at submission, with the decomposition tool, the harness, the census, and the exact JSONs; deterministic runs (equivalence check 16/16 identical across machines and engine builds).

R11. "The LLM cost section is anecdotal." Answer: two machines, two encodings, both cold and steady-state numbers, the caching failure explained, the 14B added, the replies quoted; framed as a feasibility bound, nothing more.

R12. "Why ToG and not a workshop?" Answer: the archival value is the scoring analysis and the census tooling, which apply to any human-relative efficiency benchmark, and ToG lists games-for-AGI in scope.

---

## 4. Experiments required before a line of the manuscript is written

All on CPU (lenovo 8 workers; Kaggle CPU sessions for the slow agents). All scripts worker-pooled, resumable, writing ablate-format JSON so g_decompose.py reads them. Compute is not the constraint; getting E1's agents to run is.

E1. Family study (load-bearing).
  Purpose: show the plateau and the level-1-only signature are properties of frame-only agents, not of ours.
  Agents (minimum three, licence-checked, unchanged except for the harness adapter):
    a) the official ARC-AGI-3-Agents repository's non-LLM template agents (random; any deterministic template);
    b) the public CPU-only programmatic agent whose repository reports 0.26-0.27 (learned transition model, volatility-masked hashing, object-centric navigation);
    c) at least one more public CPU-only Kaggle notebook from the competition's code tab, if one exists; otherwise state that none was found and why.
  Design: all 25 public games, 10 seeds, 20,000 actions, per-level scorecard counts, same env files, same engine.
  Output: per agent, the decomposition table (recorded, AT HUMAN, at 2x, at 5x, median ratio, levels by index) and the per-game table.
  Decision rule: if two or more independent agents show recorded < 0.5, AT HUMAN / recorded > 5, and lv3+ = 0 on held-out, the family claim stands. If any independent agent breaks the pattern, the paper's claim changes to "our family", and the abstract is rewritten.
  Script: g_family_run.py (adapter per agent; each adapter is a function that maps (frame, history) -> action, wrapped by our play loop so the action accounting is identical). Runtime: minutes per agent for ours; unknown for theirs.

E2. Seeds and intervals.
  10 seeds for hash_state on all 25 games at 20,000 actions (we have 4; the lenovo 10-seed variance test covered public games at a smaller budget). Bootstrap 95% intervals on every mean reported. Script: g_nav_run.py with --seeds 10 --modes hash_state. Runtime: about 30 minutes.

E3. Budget curve.
  Budgets 3,000, 20,000, 100,000 actions (we have 20k and 100k for base/giveup); add 3,000 and 50,000 at 4 seeds so the curve has 4 points. Shows saturation of score against actions. Script: g_nav_run.py --modes hash_state --budget B. Runtime: 100k runs are ~3 min each; 25 x 4 = 100 runs ~ 40 min at 8 workers.

E4. Analytic ceiling.
  Derive, from the formula, the score of an agent that completes the first k levels of a game at cost ratio r on each, as a function of the game's level count N and baselines h_i; then the mean over the 25 public games from metadata alone; then the measured points overlaid. Prove every step (the formula is three lines; the game-level cap max_score = completed-weight share must be included). Script: g_ceiling.py reads only baseline_actions from metadata.json. Runtime: seconds.

E5. Selection transfer over random splits (no new runs).
  Use the 20-mechanism x 1-seed x 25-game Kaggle ablation and the 6-mechanism x 4-seed lenovo ablation. For 10,000 random 8/17 splits: (i) pick the train-best mechanism, (ii) record whether it is held-out-best, (iii) record held-out score of the pick vs held-out-best vs held-out oracle. Report the distribution. Script: g_split_transfer.py. Runtime: seconds.

E6. Census at 10 seeds.
  Re-run the v2 census on all 25 games (train included) at 10 seeds so every census row carries a count out of 10, and so the train games appear in the same table (tu93 as the positive control, ls20/dc22/m0r0/lf52 with their source-verified failure reasons). Script: g_nav_run.py --games all --seeds 10 --modes hash_state,nav --budget 20000. Runtime: about 90 minutes.

E7. LLM cost, 14B.
  The same speed script with qwen2.5:14b on both machines, 3 steps, both encodings, with prompt caching fixed (persistent context via the generate endpoint with the returned context, or a single growing prompt) so the number is the best case for CPU. Runtime: 1-2 hours per machine, unattended.

E8. Reproducibility package.
  Anonymised repository: harness, decomposition, census, all JSONs, the equivalence script, engine versions, a one-command reproduction of every table. Determinism statement: identical scores across lenovo and Kaggle for identical seeds (observed on the ablation and on the G-NAV quick check).

Order: E5 and E4 first (no runs, they shape the argument), then E2/E3/E6 (an afternoon), then E1 (the unknown; start immediately in parallel because the adapters are the work), then E7.

---

## 5. Analysis plan

- Every mean over games is reported with a bootstrap 95% interval over seeds (10 seeds) and, where the claim is about games, over games (25 or 17).
- Level-index decomposition: share of score from level 1, level 2, level 3+.
- Efficiency ratio distribution: median and quartiles of agent/human on won levels, from scorecard counts (never from level_log, which undercounts: probe, scan and reset presses are outside it; ls20 seed 1003: 41 vs 25, ft09 seed 1003: 212 vs 90).
- Counterfactuals: AT HUMAN, at 2x, at 5x, from the same won levels.
- Selection transfer: fraction of splits where the train pick is held-out-best; expected held-out regret of the pick vs oracle.
- Census: contingency table games x failing assumption, with the evidence column (keys accepted, agree/presses, first-level outcome).
- Ceiling: the derived curve S(k, r) and the measured points.
- Nothing is averaged that hides a game: every table has a per-game supplement.

---

## 6. Manuscript structure (12 pages, IEEE two-column)

1. Introduction (1 page): the benchmark, the question, the four contributions, what is not claimed.
2. ARC-AGI-3 and its scoring rule (1 page): the formula, derived from the reference implementation; the level-index weighting; the game-level cap; a worked example (tu93: nine levels, level 1 won at 356 vs 19 is worth 0.3 of 100).
3. The analytic ceiling (1 page): derivation, the curve, the public-set numbers.
4. Agents and harness (1.5 pages): the frame-only family; our explorer (hash_state) and planner (G-NAV) described as instruments; the other public agents (E1); the harness and the per-level accounting; determinism.
5. Measured decomposition (1.5 pages): E2, E3; AT HUMAN; the budget curve.
6. Selection transfer (1 page): the one split, then E5 over random splits.
7. The assumption census (2 pages): T1-T5 with their counters; the 25-game table; per-row reasons; tu93 as positive control with its source-verified mechanism; ls20/dc22/m0r0/lf52 with theirs; the ar25 anomaly reported.
8. Cost of a CPU-hosted language model (0.5 page): E7; the required per-action budget; the replies.
9. Threats to validity (1 page): public set only; live benchmark snapshot; three train sources read; planner weakness; seeds.
10. Related work (0.5 page): ARC-AGI-3 organiser publications; the leaderboard winners' open-sourced approaches (Duck: local 27B model writing Python in a REPL with image, ASCII and segmentation views; Reki: Gemma-4-31B policy with JSON actions and reflection memory); the public CPU-only agent; prior work on efficiency-weighted evaluation of game agents.
11. Conclusion (0.25 page).
Figures: (F1) score formula and worked example; (F2) ceiling curve with measured points; (F3) budget curve; (F4) level-index decomposition per agent; (F5) selection-transfer histogram; (F6) census contingency table as a figure; (F7) LLM seconds-per-action bars. Tables: (T1) agents and versions; (T2) decomposition per agent; (T3) census with evidence; (T4) killed mechanisms with the measured reason (ten rows plus the planner).

---

## 7. Rules for the manuscript

Allowed: "on the 25 public games", "for the frame-only agents we measured", "under this scoring rule", "we could not", "we did not observe".
Forbidden: any statement about the hidden set; "necessary" or "impossible" in general; "state of the art"; any estimate of the leaders' internals beyond their published descriptions; any number not in a JSON in the repository; any sentence an author cannot point to a run for.
Disclosures: engine versions and date; train-game sources read (tu93, dc22, ls20) and when; that the held-out split was fixed before the first mechanism was measured and never changed; competition status at submission; use of an AI assistant in drafting and coding per IEEE policy (disclosed in the final, non-anonymous version).
Style: human language, no filler; every mathematical step shown; every limitation stated where the reader meets the claim, not only in a threats section.

---

## 8. Timeline

Week 1 (to 2 Oct): E4, E5 written and run; E2, E3, E6 run; E1 adapters started; results tables generated automatically from JSON.
Week 2 (to 9 Oct): E1 complete or the family claim downgraded; E7; figures.
Week 3 (to 16 Oct): full draft; internal ruthless review against Section 3; every number traced to a file.
Week 4 (to 23 Oct): anonymised repository; cover letter; submission. Competition final results (2 Nov) can be added in revision if reviewers ask.
If E1 cannot be made to run with at least two independent agents by 9 Oct, stop and reassess the venue; a short paper (6-8 pages) on the scoring analysis and the census alone is the fallback, not a full paper with a hole in it.

---

## 9. Draft abstract (numbers in brackets are NEED and will be replaced; nothing else changes)

ARC-AGI-3 evaluates agents on unseen two-dimensional games by the number of actions they need relative to a human baseline: each level scores the squared ratio of human to agent actions, levels are weighted by their index, and unfinished levels score zero. We analyse what this rule rewards and measure what a family of frame-only, prior-free, CPU-runnable agents can do under it. From the scoring formula we derive the maximum score of an agent that completes the first levels of a game at a fixed multiple of the human cost, and show on the 25 public games that winning first levels at 30-150 times the human count is worth under 0.5 of 100; in 1,088 held-out runs of a state-hashing explorer, every point came from the first level of four games, no third level was ever won, and a five-fold larger action budget added 0.03. [N] other public frame-only agents show the same plateau and signature. Selecting behaviour on a subset of public games does not transfer: over [10,000] random 8/17 splits, the mechanism chosen on the train split is the best on the held-out split in [x]% of cases, and a per-game oracle over 20 mechanisms is worth 0.03. To locate the barrier we built a navigation planner that verifies its own assumptions on the game it is playing and used its counters to classify each of 17 unseen games by the assumption that fails: three offer no keyboard, three no controllable object, five a clean lattice walker, two a one-dimensional walker, three a key-controlled object that is not a walker; on none of the fourteen with a controllable object does the first level end by reaching a place, and the planner's only success is the one game whose exit is a coloured tile. The barrier is goal inference, not perception or search. We also measure that a CPU-hosted 7B language model costs 218-1,254 seconds per action against a required 2.9, and cannot read the board, which explains why every leading entry runs a GPU-served vision model. Code, harness and all run records are released.

---

## 10. Checklist for whoever reviews this plan

- Is the family study (E1) feasible with at least two agents we did not write? If not, the paper is a short paper or nothing.
- Is the ceiling derivation (E4) correct, including the game-level cap?
- Is the random-split analysis (E5) the right test of "selection does not transfer"?
- Are the census rows that depend on the game (no keys, no object, goal falsified) separated from the rows that depend on the planner (exhausted, stalled)?
- Is every number in Section 1 and Section 9 traceable to a named JSON?
- Is anything in the abstract a claim about the hidden set, about necessity in general, or about the leaders beyond their published descriptions? If yes, cut it.
- Does the manuscript name the ar25 anomaly?
- Are the three read train sources disclosed?
- Is the manuscript fully anonymised, including the repository?
