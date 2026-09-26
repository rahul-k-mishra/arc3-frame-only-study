# PRIOR_ART_KILL.md — gate G0 prior-art check

Written 27 September 2026 for gate G0 of docs/TOG_PLAN_v3.md Section 6. The question is whether anything the method paper claims is already in the literature, and in particular whether Statement 1 and Statement 2 of docs/METHOD_BLUEPRINT.md Section 5 are corollaries of published results. Reading only: no experiment was run and runs/ was not opened.

**How the reading was done.**
- Five research sub-agents of this session fetched and read the papers on 27 Sep 2026: seed items 1–8, 9–15, 16–22 and 23–29, plus the Part B search.
- This file compiles their records. Each record's "Read" line says what was actually read.
- A verdict marked PROVISIONAL rests on an abstract, a citing work or a search snippet, because the paper itself could not be fetched.
- I did not re-read the papers myself. Every statement below about a paper is as good as that agent's reading, and a verdict that decides something (Part C, Part D) should be checked against the paper before the manuscript relies on it.
- Quotations are limited to a short phrase, at most one per paper.

**What is tested: the five claim components.**
- (i) the census as a probe battery that reports a game's mechanics;
- (ii) the controllable-object probe A2;
- (iii) census output predicting agent success before the agent runs;
- (iv) the definition of a goal-identification cost from level-end events (G_end, G_act; METHOD_BLUEPRINT.md 2.3);
- (v) Statement 1 or Statement 2 as a bound (METHOD_BLUEPRINT.md 5).

**Verdicts.**
- KILLS: our claim is already theirs.
- SUBSUMES: our statement is a corollary; cite, do not prove.
- BASELINE: compare against it, or position against it in related work.
- CITE ONLY.
- NOT RELEVANT.

**Summary.**
- No paper KILLS any component.
- Two results SUBSUME the formal content of Section 5:
  - Goldman & Kearns 1995 covers the identification half of Statement 1 and the counting in Statement 2;
  - the immobile-hider search game (Gal 1979, as stated by Alpern & Lidbetter) covers the search-cost half of Statement 1 (PROVISIONAL: Gal 1979 was not read directly).
- Statement 2 as written has three defects of its own (Part C2).
- Components (i)–(iii) survive, narrowed:
  - A2's "one controlled object from frames" idea belongs to Bellemare et al. 2012 and Choi et al. 2019;
  - the closest attempt at (iii) is Bontrager et al. 2016, whose game features did not predict performance.

---

## Part A — the seed list

### Controllability and mechanics from frames

**1. Bellemare, Veness, Bowling 2012**
- Citation: M. G. Bellemare, J. Veness, M. Bowling, "Investigating Contingency Awareness Using Atari 2600 Games", Proc. AAAI 2012, pp. 864–871.
- URL: https://ojs.aaai.org/index.php/AAAI/article/view/8321/8180 (author copy https://webdocs.cs.ualberta.ca/~bowling/papers/12aaai-roc.pdf)
- Read: abstract + Sections 1–6.2 (definitions, method, protocol, results).
- What it does:
  - A pixel location is defined as contingent when its next colour depends on which action is taken; a stochastic version uses a KL-divergence threshold between per-pixel transition models.
  - A logistic-regression classifier on local pixel neighbourhoods, trained by SGD, predicts contingency per 5×5 block. Labels come from emulator save/restore offline, or from a learned change model online.
  - A Bayes filter then tracks a single avatar's centroid, and the tracked location feeds SARSA(λ) features.
  - Parameters were set on 5 training games and frozen for 46 test games.
- Components touched: (i), (ii).
- Already covers: detecting from frames which parts of the screen the actions control (our A1 at pixel level); localising one controlled avatar; the frozen-on-training-games protocol.
- Remains distinct:
  - no per-action displacement vector;
  - no lattice, blocking or place-goal tests;
  - no game-level mechanics readout scored against ground truth;
  - no prediction of agent success, no G;
  - it learns weights and uses reward.
- Verdict: **BASELINE.**

**2. Choi et al. 2019**
- Citation: J. Choi, Y. Guo, M. Moczulski, J. Oh, N. Wu, M. Norouzi, H. Lee, "Contingency-Aware Exploration in Reinforcement Learning", ICLR 2019.
- URL: https://arxiv.org/abs/1811.01483
- Read: abstract + Sections 2, 3.1, 3.2, start of 4.
- What it does:
  - An attentive dynamics model, an inverse-dynamics CNN with a sparsemax attention map, is trained online to predict the action just taken from two consecutive frames.
  - The attention argmax is taken as the agent's location.
  - That location serves as a discrete state for a count-based exploration bonus added to the environment reward, on hard-exploration Atari games.
- Components touched: (ii), marginally (i).
- Already covers: self-supervised localisation, from frames alone, of the region the actions control.
- Remains distinct: the output is a location, not a per-key step; learned by gradient descent; no lattice, blocking or goal tests; no readout against ground truth; no prediction; uses reward.
- Verdict: **BASELINE.**

**3. Kansky et al. 2017**
- Citation: K. Kansky, T. Silver, D. A. Mély, M. Eldawy, M. Lázaro-Gredilla, X. Lou, N. Dorfman, S. Sidor, S. Phoenix, D. George, "Schema Networks: Zero-shot Transfer with a Generative Causal Model of Intuitive Physics", ICML 2017, PMLR 70:1809–1818.
- URL: https://proceedings.mlr.press/v70/kansky17a.html
- Read: abstract + Sections 1–4.2.
- What it does: A factor-graph model over entities with binary attributes. Learned AND-of-preconditions schemas predict next-step attributes and reward, and planning is backward inference from reward. Entities and attributes are supplied by an assumed vision system, and it is shown on Breakout variants.
- Components touched: (i), loosely.
- Already covers: learning action-conditioned entity dynamics.
- Remains distinct: entities are given; no probe battery, no accuracy against ground truth, no prediction, no reward-free goal cost.
- Verdict: **CITE ONLY.**

**4. Guzdial, Li, Riedl 2017**
- Citation: M. Guzdial, B. Li, M. O. Riedl, "Game Engine Learning from Video", Proc. IJCAI-17, pp. 3707–3713.
- URL: https://www.ijcai.org/proceedings/2017/0518.pdf
- Read: full text.
- What it does: Parses gameplay video of one Super Mario Bros. level into sprites (with a supplied sprite sheet) and hand-authored fact types, then greedily searches for IF-THEN rules whose simulation reproduces the frames. It evaluates by frame-prediction error and by planning with the learned engine. The authors state that death and level transitions are not represented.
- Components touched: (i), loosely.
- Already covers: inferring mechanics, including player-controlled rules, from frames.
- Remains distinct: needs sprite sheets and fact types; learns offline from video rather than probing; no fixed assumption battery, no cross-game ground-truth check, no prediction; no level ends, so nothing on (iv) or (v).
- Verdict: **CITE ONLY.**

**5. Diuk, Cohen, Littman 2008**
- Citation: C. Diuk, A. Cohen, M. L. Littman, "An Object-Oriented Representation for Efficient Reinforcement Learning", ICML 2008 (pages 240–247 per ACM listing, not verified from the PDF).
- URL: https://carlosdiuk.github.io/papers/OORL.pdf
- Read: full text.
- What it does:
  - States are objects of given classes with attributes and relations (touching in four directions, on). Dynamics are condition–effect pairs per action and attribute, for example "increment by a constant".
  - DOORMAX learns these pairs. It records no-change transitions as failure conditions (for example, touching a wall gives no effect), eliminates contradicted effect types, and comes with a KWIK bound.
  - Experiments on Taxi and Pitfall; in Pitfall, objects come from a colour-cluster heuristic.
- Components touched: (i), (ii) partly, (v) in style only.
- Already covers:
  - the content of A3 (a constant per-action increment, generalised across positions);
  - the content of A4 (blocking learned as failure conditions from wall contact);
  - hypothesis elimination by contradiction, with a sample bound, for transition dynamics.
- Remains distinct:
  - objects, classes and which object is the agent are supplied, so there is no discovery from frame differences (A2);
  - no place-goal test, no readout against ground truth across suites, no prediction;
  - reward is observed;
  - its bound is about learning transitions, not about goal identification, so Statements 1 and 2 are not corollaries of it.
- Verdict: **BASELINE.**

**6. Kunanusont, Lucas, Pérez-Liébana 2017**
- Citation: K. Kunanusont, S. M. Lucas, D. Pérez-Liébana, "General Video Game AI: Learning from Screen Capture", IEEE CEC 2017; arXiv:1704.06945.
- URL: https://arxiv.org/abs/1704.06945
- Read: abstract + Sections I–IV.A.
- What it does: A DQN that learns to play 6 GVGAI games from pre-processed screenshots, compared with a sampling MCTS agent. It learns no forward model and no readout of mechanics.
- Components touched: none.
- Already covers: nothing of (i)–(v); precedent for pixel-only GVGAI learning.
- Remains distinct: all five components.
- Correction: the cite list's "forward-model learning in GVGAI" is not this paper. The GVGAI forward-model paper is Dockhorn & Apeldoorn, "Forward Model Approximation for General Video Game Learning", IEEE CIG 2018. It was not fetched; a search snippet describes learned mechanics rules revised on unseen levels. It is unchecked and potentially BASELINE for (i) (PROVISIONAL).
- Verdict: **NOT RELEVANT** (cite only as a pixel-learning precedent).

**7. Osband et al. 2020**
- Citation: I. Osband, Y. Doron, M. Hessel, J. Aslanides, E. Sezener, A. Saraiva, K. McKinney, T. Lattimore, C. Szepesvári, S. Singh, B. Van Roy, R. Sutton, D. Silver, H. van Hasselt, "Behaviour Suite for Reinforcement Learning", ICLR 2020.
- URL: https://arxiv.org/abs/1908.03568
- Read: abstract only.
- What it does: A collection of purpose-built experiments that probe core capabilities of RL agents, with shared evaluation code. The probes measure agents, not unknown environments.
- Components touched: (i), by analogy.
- Already covers: the idea of a fixed diagnostic battery, aimed at agents.
- Remains distinct: our battery probes the mechanics of unseen environments and predicts agent success from them.
- Verdict: **CITE ONLY** (the contrast case: agent probes against environment probes).

**8. Rajan et al. 2023**
- Citation: R. Rajan, J. L. Borja Diaz, S. Guttikonda, F. Ferreira, A. Biedenkapp, J. O. von Hartz, F. Hutter, "MDP Playground: An Analysis and Debug Testbed for Reinforcement Learning", Journal of Artificial Intelligence Research 77:821–890, 2023; arXiv:1909.07750.
- URL: https://arxiv.org/abs/1909.07750
- Read: abstract + arXiv metadata.
- What it does: A testbed of toy environments, and wrappers for Atari and MuJoCo, each exposing a designer-set dimension of hardness (reward delay, sequence length, stochasticity, irrelevant features and others). It measures how agent performance depends on each dimension.
- Components touched: (iii), by analogy.
- Already covers: relating named environment properties to agent performance, where the properties are injected by the designer.
- Remains distinct: our properties are measured from frames of unseen games, and the prediction is made before any agent runs.
- Correction: the venue is JAIR, not JMLR.
- Verdict: **CITE ONLY.**

### Benchmark characterisation

**9. Cobbe et al. 2020**
- Citation: K. Cobbe, C. Hesse, J. Hilton, J. Schulman, "Leveraging Procedural Generation to Benchmark Reinforcement Learning", ICML 2020, PMLR 119.
- URL: https://arxiv.org/pdf/1912.01588
- Read: abstract + Sections 1–6 (appendices not read).
- What it does: 16 procedurally generated games with 64×64 RGB frames and 15 shared actions. It measures the train–test generalisation gap against the number of training levels, per game and in aggregate. Per-game differences are described, not predicted from measured game properties.
- Components touched: (iii), weakly.
- Remains distinct: all of (i)–(v).
- Verdict: **CITE ONLY** (suite source).

**10. Chevalier-Boisvert et al. 2019**
- Citation: M. Chevalier-Boisvert, D. Bahdanau, S. Lahlou, L. Willems, C. Saharia, T. H. Nguyen, Y. Bengio, "BabyAI: A Platform to Study the Sample Efficiency of Grounded Language Learning", ICLR 2019.
- URL: https://arxiv.org/pdf/1810.08272
- Read: abstract + Sections 3–4.2.
- What it does: 19 levels, each assigned by the designers the competencies it requires (Table 1). Difficulty is measured by imitation-learning success and by the number of demonstrations or RL episodes needed to reach high success. It remarks informally that levels with longer demonstrations tend to be harder.
- Components touched: (i), weakly (the competency table is a ground-truth label); (iii), weakly.
- Already covers: a per-level table of required capabilities, which is a possible ground-truth source for our MiniGrid/BabyAI suite.
- Remains distinct: its table is declared by the designers, while our census is measured from frames; it uses symbolic observations and text instructions.
- Verdict: **BASELINE.**

**11. Machado et al. 2018**
- Citation: M. C. Machado, M. G. Bellemare, E. Talvitie, J. Veness, M. Hausknecht, M. Bowling, "Revisiting the Arcade Learning Environment: Evaluation Protocols and Open Problems for General Agents", JAIR 61:523–562, 2018 (volume and pages not verified from the fetched arXiv version).
- URL: https://arxiv.org/pdf/1709.06009
- Read: abstract, Sections 1–2.1, Section 7 up to 7.4.1, Appendix A.
- What it does: Recommends ALE evaluation protocols (sticky actions, fixed budgets). It describes hard-exploration games qualitatively, and its "Brute" baseline exploits determinism by searching a history tree, a precedent for our hash_state explorer. It does not measure game properties or predict success.
- Components touched: (iii) and (v), qualitatively only.
- Remains distinct: all of (i)–(v).
- Verdict: **CITE ONLY.**

**12. ARC-AGI-3 documents**
- 12a. ARC Prize Foundation, "ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence", arXiv:2603.24621 (v1 24 Mar 2026, revised 17 Apr 2026).
  - URL: https://arxiv.org/abs/2603.24621
  - Read: abstract + Sections 3–6 through a fetch summary.
  - What it does: Defines the benchmark (64×64 frames, 16 colours, keyboard and click actions, 25 public environments), the Core Knowledge priors, the level-weighted efficiency score, and a random-policy acceptance threshold. It names goal inference as a hurdle, qualitatively. It gives no census of mechanics and no per-environment failure analysis.
  - Components touched: (iv), as motivation only.
  - Verdict: **CITE ONLY** (required).
- 12b. G. Kamradt, "ARC-AGI-3 Preview: 30-Day Learnings", ARC Prize blog, 19 Aug 2025.
  - URL: https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings
  - Read: full post through a fetch summary.
  - What it does: Describes the preview winners, including a CNN predicting which actions change the frame and a frame-state graph that prunes no-change actions. It discusses some games per game, qualitatively.
  - Components touched: (ii) weakly, (iii) qualitatively.
  - Verdict: **CITE ONLY.**
- 12c. G. Kamradt, "Announcing ARC-AGI-3", ARC Prize blog, 25 Mar 2026.
  - URL: https://arcprize.org/blog/arc-agi-3-launch
  - Read: full post through a fetch summary.
  - Verdict: **CITE ONLY.**
- 12d. G. Kamradt, "Measuring Human Performance on ARC-AGI-3", ARC Prize blog, 14 Apr 2026.
  - URL: https://arcprize.org/blog/arc-agi-3-human-dataset
  - Read: full post through a fetch summary.
  - What it does: Human first-run data and released step-by-step replays for the 25 public environments. No separate human-performance paper was found; the cite list's entry is probably this post plus the technical report's human section.
  - Components touched: (iv), indirectly (the replays could give an empirical human G on level 1).
  - Verdict: **CITE ONLY.**
- 12e. G. Kamradt, "ARC Prize 2026: ARC-AGI-3 Milestone Prize #1", ARC Prize blog, 6 Jul 2026.
  - URL: https://arcprize.org/blog/arc-prize-2026-milestone-1
  - Read: full post through a fetch summary.
  - What it does: The winners were LLM or VLM agents; none is frame-only and prior-free.
  - Verdict: **CITE ONLY.**

**13. Rudakov, Shock, Cowley 2025**
- Citation: E. Rudakov, J. Shock, B. U. Cowley, "Graph-Based Exploration for ARC-AGI-3 Interactive Reasoning Tasks", arXiv:2512.24156, 30 Dec 2025 (the full title includes "Interactive Reasoning Tasks").
- URL: https://arxiv.org/pdf/2512.24156
- Read: full text.
- What it does:
  - A training-free agent that segments frames into single-colour connected components and masks status bars.
  - It sorts click targets into priority tiers by visual salience, hashes frames as states, and explores a state–action graph towards the nearest untested action.
  - It solved a median of 30 of 52 preview levels.
  - It explains successes and failures per game after the fact.
  - Its "controllable objects" are click-priority tiers, not detected by displacement.
- Components touched: (ii) in a neighbouring sense; (iii) after the fact.
- Already covers: segmentation, status-bar masking, and state-hash graph exploration.
- Remains distinct: the probe battery and its accuracy; the displacement-agreement rule; the prediction registered in advance; G; the bounds.
- Verdict: **BASELINE** (already our E1 agent).

**14a. Balla, Lucas, Perez-Liebana 2020**
- Citation: M. Balla, S. M. Lucas, D. Perez-Liebana, "Evaluating Generalisation in General Video Game Playing", IEEE CoG 2020, pp. 423–430; arXiv:2005.11247.
- URL: https://arxiv.org/abs/2005.11247
- Read: abstract + game-selection and results sections through a fetch summary.
- What it does: Trains A2C variants on a few levels of four GVGAI games and tests on held-out levels. Stochasticity and reward distribution explain generalisation after the fact.
- Components touched: (iii), after the fact.
- Verdict: **CITE ONLY** (precedent for train/held-out level splits in GVGAI).

**14b. Stephenson et al. 2025 — identification uncertain**
- Candidate chosen: M. Stephenson, A. Newcombe, É. Piette, D. Soemers, "Best Agent Identification for General Game Playing", arXiv:2507.00451 (Jul 2025, revised Apr 2026).
- URL: https://arxiv.org/abs/2507.00451
- Read: abstract only.
- What it does: Treats choosing the best agent per game as a set of best-arm-identification bandit problems, on GVGAI and Ludii.
- Components touched: (iii), adjacent (the agents are chosen by running them, not predicted before running).
- Other candidates:
  - Stephenson, Soemers, Piette, Browne, "General Game Heuristic Prediction Based on Ludeme Descriptions", CoG 2021 (arXiv:2105.12846). This predicts heuristic performance from symbolic game descriptions, so it is closer to (iii), but it is from 2021.
  - A 2025 IEEE Transactions on Games paper with Stephenson as a coauthor, not verified.
- **RKM to confirm which paper the cite list meant.**
- Verdict: **CITE ONLY, PROVISIONAL.**

**15. Justesen et al. 2018**
- Citation: N. Justesen, R. R. Torrado, P. Bontrager, A. Khalifa, J. Togelius, S. Risi, "Illuminating Generalization in Deep Reinforcement Learning through Procedural Level Generation", NeurIPS 2018 Deep RL Workshop; arXiv:1806.10729.
- URL: https://arxiv.org/pdf/1806.10729
- Read: Sections 1–7.
- What it does: Parameterised level generators for four GVGAI games, with difficulty adapted to the agent's win rate. It shows overfitting to single levels and partial transfer to human-designed levels, with per-game explanations after the fact.
- Components touched: (iii), weakly.
- Verdict: **CITE ONLY.**

### Goal identification and identifiability

**16. Ng & Russell 2000**
- Citation: A. Y. Ng, S. Russell, "Algorithms for Inverse Reinforcement Learning", ICML 2000.
- URL: https://ai.stanford.edu/~ang/papers/icml00-irl.pdf
- Read: abstract + Sections 1–3.1.
- What it does: Characterises the rewards under which an observed policy is optimal (linear inequalities in the finite case). It notes that the set is degenerate, since a constant reward always satisfies it, and picks among consistent rewards by heuristics.
- Components touched: (iv), loosely.
- Already covers: evidence leaving a set of consistent rewards, including a trivial one that cannot be ruled out, which is the counterpart of our h0.
- Remains distinct: the observer sees an expert; there is no learner using level-end events, and no count of events.
- Verdict: **CITE ONLY.**

**17. Cao, Cohen, Szpruch 2021**
- Citation: H. Cao, S. N. Cohen, L. Szpruch, "Identifiability in inverse reinforcement learning", NeurIPS 2021.
- URL: https://proceedings.neurips.cc/paper/2021/hash/671f0311e2754fcdd37f70a8550379bc-Abstract.html
- Read: abstract only.
- What it does: In entropy-regularised MDPs, characterises the rewards consistent with a policy. It shows recovery up to a constant from demonstrations under two discount factors or two sufficiently different environments.
- Components touched: (iv), loosely.
- Remains distinct: an observer of regularised-optimal behaviour; no level-end evidence; no count of events.
- Verdict: **CITE ONLY.**

**18. Kim, Garg, Shiragur, Ermon 2021**
- Citation: K. Kim, S. Garg, K. Shiragur, S. Ermon, "Reward Identification in Inverse Reinforcement Learning", ICML 2021, PMLR 139:5496–5505.
- URL: https://proceedings.mlr.press/v139/kim21c.html
- Read: abstract only.
- What it does: Necessary and sufficient conditions for reward identifiability from MaxEnt-optimal behaviour in deterministic MDPs, with tests for whether an MDP has the property.
- Components touched: (iv), loosely.
- Remains distinct: the evidence is an expert's behaviour; the answer is a yes/no, not a count of events.
- Verdict: **CITE ONLY.**

**19. Skalse et al. 2023**
- Citation: J. Skalse, M. Farrugia-Roberts, S. Russell, A. Abate, A. Gleave, "Invariance in Policy Optimisation and Partial Identifiability in Reward Learning", ICML 2023, PMLR 202:32033–32058.
- URL: https://proceedings.mlr.press/v202/skalse23a.html
- Read: abstract only.
- What it does: Characterises how far rewards are only partly identifiable from common data sources (demonstrations, trajectory comparisons), and what that ambiguity means for downstream policy optimisation.
- Components touched: (iv).
- Remains distinct: the abstract names no data source matching level-end events observed by the learner about its own goal. An appendix on episode-return data cannot be ruled out without the full text.
- Verdict: **CITE ONLY.** Lower confidence: if the full text treats return-only data, this becomes BASELINE for (iv).

**20a. Keren, Gal, Karpas 2014**
- Citation: S. Keren, A. Gal, E. Karpas, "Goal Recognition Design", ICAPS 2014, pp. 154–162.
- URL: https://groups.csail.mit.edu/mers/publication_uploads/Publications/2014/keren2014icaps/7814-36999-1-PB.pdf
- Read: pp. 154–157 (model, Definitions 1–3, Theorems 1–3).
- What it does:
  - Setting: a deterministic, fully observable planning domain with a set of candidate goals, and an optimal actor.
  - Worst-case distinctiveness (wcd) is the length of the longest action prefix shared by optimal plans to two different goals. It is the worst case of how long an outside observer cannot tell the actor's goal.
  - Theorem 2: past wcd observed actions, at most one goal stays consistent.
  - The design problem is to remove actions so as to reduce wcd without raising any goal's optimal cost.
- Components touched: (iv); (v) in structure.
- Already covers: a goal-identification cost that is a property of the environment and is defined through a consistent goal set; grid-navigation examples.
- Remains distinct:
  - the bounded party is an outside observer of another agent, not the learner of its own unknown goal;
  - the observation is actions, not level-end events;
  - the actor is optimal (we quantify over all policies);
  - the unit is actions in a prefix, not goal-achievement events;
  - no feature hypothesis class, no transfer across levels;
  - the contribution is redesigning the environment.
- Verdict: **BASELINE** (closest published goal-identification cost; does not subsume Statement 1 or 2).

**20b. Keren, Gal, Karpas 2015**
- Citation: S. Keren, A. Gal, E. Karpas, "Goal Recognition Design for Non-Optimal Agents", AAAI 2015, pp. 3298–3304.
- URL: https://ojs.aaai.org/index.php/AAAI/article/download/9645/9504
- Read: abstract + model + bounded non-optimality (pp. 3298–3300).
- What it does: Replaces optimal plans with per-goal sets of legal plans, with a cost budget for bounded non-optimality. It proves monotonicity properties of wcd and computes it by compilation to classical planning.
- Components touched: (iv).
- Remains distinct: as 20a. With unbounded budgets wcd is generally not finite, so "any policy" fits only degenerately.
- Verdict: **BASELINE** (cite together with 20a).

**20c. Keren, Gal, Karpas 2016**
- Citation: S. Keren, A. Gal, E. Karpas, "Goal Recognition Design with Non-Observable Actions", AAAI 2016.
- URL: https://ojs.aaai.org/index.php/AAAI/article/view/10403
- Read: abstract only (PDF redirect failed).
- What it does: Makes some of the actor's actions unobservable, redefines wcd accordingly, and proposes sensor placement.
- Components touched: (iv).
- Remains distinct: the observer is still separate from the actor; what passes through the sensor is the actor's actions, not an outcome signal.
- Verdict: **BASELINE.**

**20d. Wayllace, Hou, Yeoh, Son 2016**
- Citation: C. Wayllace, P. Hou, W. Yeoh, T. C. Son, "Goal Recognition Design with Stochastic Agent Action Outcomes", IJCAI-16, pp. 3279–3285.
- URL: https://www.ijcai.org/Proceedings/16/Papers/464.pdf
- Read: abstract + Sections 1–3.
- What it does: Moves goal recognition design to stochastic shortest-path MDPs. wcd becomes the largest expected cost over non-distinctive policy prefixes, and is reduced by blocking actions.
- Components touched: (iv); (v) in form (an expected cost to identification).
- Remains distinct: an observer and an optimal actor; our expectation is over a coverage policy searching for its own goal.
- Verdict: **BASELINE.**

**20e. Keren, Gal, Karpas 2020**
- Citation: S. Keren, A. Gal, E. Karpas, "Goal Recognition Design — Survey", IJCAI-20 Survey Track, pp. 4847ff.
- URL: https://www.ijcai.org/proceedings/2020/0675.pdf
- Read: pp. 4847–4850 (Sections 5–7 not read).
- What it does: Splits goal recognition design into environment, actor and observer. It surveys stochastic GRD, expected-case distinctiveness (weighted by a goal prior), sub-optimal and deceptive actors, and information shaping.
- Components touched: (iv).
- Remains distinct: in the pages read, no variant has the actor learn its own unknown goal from goal-achievement events.
- Verdict: **BASELINE** (entry point to GRD).

**21a. Ramírez & Geffner 2009**
- Citation: M. Ramírez, H. Geffner, "Plan Recognition as Planning", IJCAI 2009, pp. 1778ff.
- URL: https://www.ijcai.org/Proceedings/09/Papers/296.pdf
- Read: abstract + Sections 1–4.
- What it does: The set of goals consistent with observed actions is those with an optimal plan containing the observations. It is computed by compiling the observations into planning problems for off-the-shelf planners.
- Components touched: (iv).
- Already covers: the consistent-goal-set construction, which our H(t) shares in form.
- Remains distinct: an observer of another agent's actions, filtering by optimality; no count of events.
- Verdict: **CITE ONLY.**

**21b. Ramírez & Geffner 2010**
- Citation: M. Ramírez, H. Geffner, "Probabilistic Plan Recognition Using Off-the-Shelf Classical Planners", AAAI 2010, pp. 1121–1126.
- URL: https://ojs.aaai.org/index.php/AAAI/article/view/7745
- Read: abstract only.
- What it does: A posterior over goals from cost differences between plans that comply with the observations and plans that do not.
- Components touched: (iv), loosely.
- Verdict: **CITE ONLY.**

**22. Baker, Saxe, Tenenbaum 2009**
- Citation: C. L. Baker, R. Saxe, J. B. Tenenbaum, "Action understanding as inverse planning", Cognition 113(3):329–349, 2009.
- URL: https://web.mit.edu/9.s915/www/classes/cognition2009.pdf
- Read: abstract + Section 1 (later sections not used).
- What it does: Models human goal inference about agents moving in mazes as Bayesian inversion of approximately rational planning.
- Components touched: (iv), loosely.
- Remains distinct: an observer inferring another agent's goal; no level-end events; no count.
- Verdict: **CITE ONLY.**

**23. Goldman & Kearns 1995**
- Citation: S. A. Goldman, M. J. Kearns, "On the Complexity of Teaching", Journal of Computer and System Sciences 50(1):20–31, 1995 (journal data from search results; read as tech report WUCS-92-28; preliminary version COLT 1991).
- URL: https://www.cis.upenn.edu/~mkearns/papers/teaching.pdf
- Read: abstract + Sections 1–4.1.
- What it does:
  - The teaching dimension of a concept class is the worst-case size of the smallest labelled sample that leaves only the target consistent.
  - Lemma 1: the class of all singletons plus the empty concept has teaching dimension |C| − 1, because each example separates only one singleton from the empty concept.
  - The teaching dimension of any class is at most |C| − 1.
- Components touched: (iv), (v).
- Already covers:
  - Our H_place(m) plus h0 is exactly "singletons plus the empty concept". A non-ending entry into cell c rules out only c. That is the identification half of Statement 1.
  - Elimination of one hypothesis per example gives the counting in Statement 2.
- Remains distinct: no graph, no movement cost, no policy, no hitting time; its learner is shown chosen examples rather than paying to walk to them.
- Verdict: **SUBSUMES** for the identification half of Statement 1 and for Statement 2's counting; **CITE ONLY** for (iv).

**24. Jin, Krishnamurthy, Simchowitz, Yu 2020**
- Citation: C. Jin, A. Krishnamurthy, M. Simchowitz, T. Yu, "Reward-Free Exploration for Reinforcement Learning", ICML 2020 (read as arXiv:2002.02794; venue not verified from PMLR).
- URL: https://arxiv.org/abs/2002.02794
- Read: abstract + Sections 1–3 (lower-bound construction not read).
- What it does: In tabular episodic MDPs, the agent explores without reward and must then return near-optimal policies for any reward given later. It gives an upper bound and a nearly matching lower bound on the number of episodes, by visiting every significant state.
- Components touched: (iv), (v) in framing.
- Already covers: without reward, the cost is set by covering the states that could carry the goal.
- Remains distinct: the target is episode complexity for planning under any reward; there is no goal hypothesis class, no level-end evidence, no G.
- Verdict: **BASELINE.**

**25. Lim & Auer 2012**
- Citation: S. H. Lim, P. Auer, "Autonomous Exploration For Navigating In MDPs", COLT 2012, JMLR W&CP 23:40.1–40.24.
- URL: https://proceedings.mlr.press/v23/lim12.html
- Read: abstract + Sections 1–2.2.
- What it does:
  - Reward-free exploration from a start state with a reset action.
  - Definition 1 is the expected number of steps before a policy first reaches a state.
  - It learns policies reaching every state reachable within L steps, with a bound on exploration steps and negative results without the incremental restriction.
- Components touched: (iv), (v).
- Already covers: the expected first-hitting time under a given policy, the quantity in Statement 1.
- Remains distinct: no goal hypotheses, no level-end signal, no division by cells visited, no identification claim.
- Verdict: **CITE ONLY** (for the hitting-time notation); BASELINE for autonomous exploration.

**26a. Gal 1979, as stated by Alpern & Lidbetter**
- Citation read: S. Alpern, T. Lidbetter, "Search for an Immobile Hider on a Binary Tree with Unreliable Locational Information", arXiv:2303.13378v2. The result they state is S. Gal, "Search games with mobile and immobile hider", SIAM J. Control Optim. 17(1):99–122, 1979 (bibliographic data from search results).
- URL: https://arxiv.org/pdf/2303.13378
- Read: abstract + Sections 1–2 of the 2024 paper. **Gal 1979 itself was not read.**
- What it does: As they state it, a zero-sum game on a network. The Hider picks a point; the Searcher picks a unit-speed path from the root with no information until arrival. The payoff is the time to reach the Hider. On a tree the game's value equals the tree's total length, with explicit optimal strategies.
- Components touched: (v).
- Already covers: "the target is revealed only on arrival" as a formal model, with search time equal to first-hitting time and minimax values.
- Remains distinct: no division by distinct cells visited; no h0.
- Verdict: **SUBSUMES, PROVISIONAL**, for any claim about the best policy's search cost. Cite Gal 1979 and Alpern & Gal 2003 (neither read).

**26b. Angelopoulos & Lidbetter 2019**
- Citation: S. Angelopoulos, T. Lidbetter, "Competitive Search in a Network", arXiv:1908.02132 (published version not verified).
- URL: https://arxiv.org/pdf/1908.02132
- Read: abstract + Sections 1–2.1.
- What it does: Search for a hidden target in a network, with search time normalised by the target's distance from the root (a competitive ratio). Its related work covers vertex hiders and unknown graphs, among them Koutsoupias, Papadimitriou & Yannakakis 1996 and Fleischer et al. 2008.
- Components touched: (v).
- Remains distinct: its divisor is shortest-path distance, not distinct cells visited.
- Verdict: **BASELINE / CITE ONLY.**

**26c. Deng & Papadimitriou 1990**
- Citation: X. Deng, C. H. Papadimitriou, "Exploring an unknown graph", FOCS 1990; J. Graph Theory 32(3):265–297, 1999 (from search results).
- URL: https://www.semanticscholar.org/paper/ffe64fd3019d58fb86915aeb9108c3a7757eef37 (empty); publisher page 403.
- Read: **not fetched**; search summaries only.
- What it does (per the summaries): Online exploration of every edge of an unknown directed graph, with a competitive ratio depending on the graph's distance from being Eulerian.
- Components touched: (v), weakly. It is about covering all edges, not a target revealed on arrival.
- Verdict: **CITE ONLY, PROVISIONAL.** It is not the closest result to Statement 1; 23 and 26a are.

**27. Blum & Hardt 2015**
- Citation: A. Blum, M. Hardt, "The Ladder: A Reliable Leaderboard for Machine Learning Competitions", ICML 2015 (read as arXiv:1502.04585; venue not verified from PMLR).
- URL: https://arxiv.org/abs/1502.04585
- Read: abstract only.
- What it does: A leaderboard mechanism that stays accurate under adaptive, repeated submissions against a holdout set.
- Components touched: none; relevant to the protocol (frozen on train, measured on held-out).
- Verdict: **CITE ONLY.**

**28. Roelofs et al. 2019**
- Citation: R. Roelofs, V. Shankar, B. Recht, S. Fridovich-Keil, M. Hardt, J. Miller, L. Schmidt, "A Meta-Analysis of Overfitting in Machine Learning", NeurIPS 2019.
- URL: https://papers.nips.cc/paper/2019/hash/ee39e503b6bedf0c98c388b7e8589aca-Abstract.html
- Read: abstract only.
- What it does: Compares public and private leaderboard rankings in many Kaggle competitions and finds little evidence of substantial overfitting from holdout reuse.
- Components touched: none.
- Note: its finding cuts against overstating holdout-reuse risk; cite it carefully next to the E5 selection-transfer results.
- Verdict: **CITE ONLY.**

**29. NeurIPS 2020 pre-registration workshop**
- Citation: there is no position paper. The citable item is L. Bertinetto, J. F. Henriques, S. Albanie, M. Paganini, G. Varol, "Preface", in *The pre-registration experiment: an alternative publication model for machine learning research* (NeurIPS 2020 Workshop), PMLR 148, 2021. The 2021 follow-up workshop is a separate event.
- URL: https://proceedings.mlr.press/v148/bertinetto21a.html (also https://preregister.science/neurips2020.html)
- Read: workshop pages; the preface has no abstract.
- What it does: A publication model in which the protocol is reviewed and accepted before experiments are run.
- Components touched: none; it supports our git-tag and OSF pre-registration.
- Verdict: **CITE ONLY.**

---

## Part B — additions from search (14 added; cap 15)

**ADDED-1. Twin**
- Found by: "ARC-AGI-3 agent 2026 arXiv".
- Citation: A. Skoutnev, K. Acharya, G. Longhitano, M. Udell, K. Ellis, I. Drori, "Twin: Playing an Unknown Game with a Test-Time Digital Twin", arXiv:2608.14490, 14 Aug 2026.
- URL: https://arxiv.org/html/2608.14490
- Read: abstract + problem statement, goal discovery, Appendix D (goal signals), compute, limitations.
- What it does:
  - A coding agent (an LLM, with very large token use) builds an executable model of each ARC-AGI-3 game from rendered frames only.
  - When planning finds no route, it ranks reachable states by visual-change signals and writes a goal predicate for the top candidate.
  - A level boundary confirms the candidate; reaching the predicted state without one rejects it.
  - It cleared 179 of 183 levels, and its first committed goal was correct on 156 of them. That count is not split between first levels and later levels.
- Components touched: (iv), (v), (i) in part.
- Already covers: frame-only goal-hypothesis elimination by level-end events in ARC-AGI-3, which is the operational core of G_end.
- Remains distinct:
  - no definition of a goal-identification cost, no bound, no per-game prediction, no controlled-object detection;
  - its early goal identification comes from visual-salience priors and an LLM. It does not contradict Statement 1 only if Statement 1 is scoped to a prior-free hypothesis class.
- Verdict: **BASELINE** (must-cite).

**ADDED-2. Tycho**
- Found by: "goal inference cost level completion hypothesis elimination ARC-AGI-3 frames 2026 arXiv win condition".
- Citation: J. Lehmann, A. Aioanei, S. Vahdati, "Tycho: Active Abstraction with Programmatic World Models for ARC-AGI-3", arXiv:2607.28287, Jul 2026.
- URL: https://arxiv.org/html/2607.28287v1
- Read: abstract + Definition 3, Sections 4.2, 5.1.
- What it does: Models ARC-AGI-3 games formally as rendered deterministic Moore machines, with a typed interaction history that separates level-completion frames. A coding-agent LLM builds executable hypotheses. It reports cases where the mechanics were right but the objective was not resolved.
- Components touched: (iv); (v) informally.
- Already covers: the empirical point that learning dynamics does not identify the goal; a formal game model.
- Remains distinct: no G, no bounds, no census, no prediction.
- Verdict: **CITE ONLY** (its formalism may be reusable).

**ADDED-3. OPINE-World**
- Found by: "agent identifies goal from terminal events without reward unknown objective game exploration inference 2025 2026".
- Citation: D. Courtis, W. Li, S. Sanner, "OPINE-World: Programmatic World Modeling with Ontology-error-Prioritized Interactive Exploration for ARC-AGI-3", arXiv:2607.01531, Jul 2026.
- URL: https://arxiv.org/html/2607.01531
- Read: abstract + perception, exploration and goal-predicate sections.
- What it does: An LLM agent that synthesises an object extractor from colour-index grids, refines a programmatic world model, and synthesises a goal predicate after level completion. It explains its failures after the fact.
- Components touched: (i), (ii) in part, (iv).
- Remains distinct: no fixed cheap battery, no accuracy against ground truth, no prediction before the run, no bounds.
- Verdict: **CITE ONLY.**

**ADDED-4. Explore Before You Solve**
- Found by: "ARC-AGI-3 agent 2026 arXiv".
- Citation: Liew Keong Han, "Explore Before You Solve: The Speed–Depth Trade-off in Epistemic Agents for ARC-AGI-3", arXiv:2605.25931, May 2026.
- URL: https://arxiv.org/html/2605.25931
- Read: abstract + Sections 3–5.
- What it does: Classifies the 25 public ARC-AGI-3 games by the cheapest blind strategy that reaches a level, and argues that all are reachable without intelligence. It pairs this with a small-LLM exploration agent.
- Components touched: (i), (iii) descriptively.
- Already covers: a cheap, probe-based per-game table of the same 25 games.
- Remains distinct: its categories are reachability by blind strategies, not mechanics; no ground truth, no split, no prediction registered in advance.
- Verdict: **BASELINE.** Compare our census categories and level-1 results with its taxonomy.

**ADDED-5. Executable World Models for ARC-AGI-3**
- Found by: "ARC-AGI-3 agent 2026 arXiv".
- Citation: S. Rodionov, "Executable World Models for ARC-AGI-3 in the Era of Coding Agents", arXiv:2605.05138, May 2026.
- URL: https://arxiv.org/abs/2605.05138
- Read: abstract only.
- What it does: A coding agent maintains and verifies a Python world model; reports per-game solve rates on the 25 public games.
- Components touched: none directly.
- Verdict: **CITE ONLY.**

**ADDED-6. DiG-bench**
- Found by: "ARC-AGI-3 frame-based exploration agent paper 2026 non-LLM".
- Citation: R. M. Battleday et al. (16 authors), "DiG-bench: Discovery in Games", arXiv:2608.12593, Aug 2026.
- URL: https://arxiv.org/html/2608.12593
- Read: abstract + method/evaluation sections.
- What it does: 70 text-played games with hidden rules and win conditions, and ground-truth rules in natural language. Supplying the rules to an LLM raises its win count sharply, a rule-oracle intervention parallel to our E9.
- Components touched: (i), (iv), not separated.
- Remains distinct: text rather than frames; no probe battery, no prediction, no G.
- Verdict: **CITE ONLY.**

**ADDED-7. Matching Games and Algorithms**
- Found by: "GVGAI game features predict controller performance algorithm selection".
- Citation: P. Bontrager, A. Khalifa, A. Mendes, J. Togelius, "Matching Games and Algorithms for General Video Game Playing", AIIDE-16, 2016, pp. 122–128.
- URL: https://cdn.aaai.org/ojs/12884/12884-52-16401-1-2-20201228.pdf
- Read: full text.
- What it does:
  - 23 controllers were played on 49 GVGAI games.
  - Games are clustered by 14 features read from each game's rule description (for example, whether the avatar can move vertically, can use an action, or can die) and, separately, by controller win profiles.
  - The two clusterings agree on 40.8% of games.
  - A decision tree predicting the performance cluster from features overfitted, and the authors judge the features poor indicators of performance.
  - A two-feature tree still drove a selector that beat every single controller.
- Components touched: (iii), (i).
- Already covers: per-game mechanics features used to predict which agent succeeds, including a feature close to A3.
- Remains distinct: features are read from the rules, not measured from frames, so no accuracy question arises; it predicts the best controller, not level-1 completion; the result is negative on predictiveness.
- Verdict: **BASELINE** (closest prior attempt at component iii).

**ADDED-8. General Win Prediction from Agent Experience**
- Found by: "GVGAI predict win or loss from agent log features 80 games classifiers Bravi Perez-Liebana" (added phrase).
- Citation: R. D. Gaina, S. M. Lucas, D. Perez-Liebana, "General Win Prediction from Agent Experience", IEEE CIG 2018 (venue inferred from the paper's data repository name; not on the PDF read).
- URL: https://rdgain.github.io/assets/pdf/papers/gaina2018win.pdf
- Read: abstract + Sections I–IV.
- What it does: Trains classifiers on 80 GVGAI games and tests on 20 unseen games, predicting whether a search agent will win from features of its own ongoing run. It deliberately excludes designed game features.
- Components touched: (iii).
- Already covers: success prediction with a held-out-game split.
- Remains distinct: prediction during the run, from the agent's own experience, not before the run from mechanics; it uses a forward model and score.
- Verdict: **BASELINE.**

**ADDED-9. Hyper-heuristic General Video Game Playing**
- Found by: "hyper-heuristic general video game playing game features predict best algorithm Mendes Togelius Nealen".
- Citation: A. Mendes, J. Togelius, A. Nealen, "Hyper-heuristic general video game playing", IEEE CIG 2016, pp. 94–101 (from search results and citing papers).
- URL: https://ieeexplore.ieee.org/document/7860398/ (empty on fetch)
- Read: **not fetched.**
- What it does (per citing papers): Game features drive an SVM or decision tree that picks a controller for an unseen game.
- Components touched: (iii).
- Verdict: **BASELINE, PROVISIONAL.**

**ADDED-10. Effective horizon**
- Found by: "predicting reinforcement learning algorithm performance from environment characteristics complexity metrics".
- Citation: C. Laidlaw, S. Russell, A. Dragan, "Bridging RL Theory and Practice with the Effective Horizon", NeurIPS 2023.
- URL: https://arxiv.org/abs/2304.09853
- Read: abstract only.
- What it does: Over 155 deterministic benchmark MDPs with full tabular representations, a measured property (the effective horizon) gives bounds that track the empirical sample complexity of PPO and DQN better than earlier bounds.
- Components touched: (iii), (v).
- Already covers: predicting from a measured environment property whether an agent family succeeds, across many environments.
- Remains distinct: needs the full tabular MDP and reward, so it is neither frame-only nor cheap; it predicts sample complexity under reward, not reward-free first-level completion.
- Verdict: **BASELINE.**

**ADDED-11. Disentangling the Controllable Object**
- Found by: a controllable-entity search phrase (added).
- Citation: Y. Zhong, A. Schwing, J. Peng, "Disentangling Controllable Object through Video Prediction Improves Visual Reinforcement Learning", ICASSP 2020; arXiv:2002.09136.
- URL: https://arxiv.org/abs/2002.09136
- Read: abstract only.
- What it does: Action-conditioned video prediction separates the controlled region. Its mask is fed to Double DQN on Atari and raises scores.
- Components touched: (ii).
- Remains distinct: a learned predictor rather than a counting rule; not reported as a readout against ground truth.
- Verdict: **CITE ONLY.**

**ADDED-12. Transporter**
- Found by: a controllable-pixel discovery search phrase (added).
- Citation: T. Kulkarni, A. Gupta, C. Ionescu, S. Borgeaud, M. Reynolds, A. Zisserman, V. Mnih, "Unsupervised Learning of Object Keypoints for Perception and Control", NeurIPS 2019.
- URL: https://arxiv.org/abs/1906.11883
- Read: abstract + Sections 3.2.2, 4.1, 4.2.2.
- What it does: Learns object keypoints from video. A fixed rule then picks the "most controllable" keypoint, the one actions move most in all directions, which often matches the avatar. Keypoint tracking is scored against ground truth; avatar identification is shown only qualitatively.
- Components touched: (ii).
- Already covers: scoring candidate objects by how much actions displace them and picking the most controllable. This is the nearest neural analogue of A2.
- Remains distinct: needs GPU training; no margin test; no "no controllable object" outcome; avatar identification not scored.
- Verdict: **CITE ONLY.**

**ADDED-13. Environment-Probing Interaction policies**
- Found by: "diagnostic probes environment properties reinforcement learning".
- Citation: W. Zhou, L. Pinto, A. Gupta, "Environment Probing Interaction Policies", ICLR 2019; arXiv:1907.11740.
- URL: https://arxiv.org/abs/1907.11740
- Read: abstract only.
- What it does: A learned probing policy takes a short trajectory in a new environment and produces an embedding that conditions the task policy.
- Components touched: (i).
- Remains distinct: the probe is learned, its output is an opaque vector rather than readable mechanics, and it makes no prediction.
- Verdict: **CITE ONLY.**

**ADDED-14. Predicting Task Difficulty Without Rollouts**
- Found by: "predict agent success on unseen environment before training from environment features MiniGrid Procgen difficulty prediction" (added).
- Citation: S. Krsteski, C. Meyer, "Predicting Task Difficulty Without Rollouts", arXiv:2608.05797, Aug 2026.
- URL: https://arxiv.org/abs/2608.05797
- Read: abstract only.
- What it does: Predicts LLM-agent success on a task before any rollout, from the task's text description, across agentic benchmarks.
- Components touched: (iii).
- Remains distinct: text tasks and LLM agents, not frame-based games; no probes.
- Verdict: **CITE ONLY.**

**Search phrases run:** all eight phrases required by the task, plus refinements (controllable-entity discovery, GVGAI feature-based selection, effective horizon, ARC-AGI-3 2026 agents).
- Found and not added:
  - observer-side GRD variants;
  - AdaGoal (Tarbouriech et al. 2022), fetched: its goals are reachable within L steps, not a task goal;
  - further ARC-AGI-3 coding-agent papers;
  - OCAtari and AtariARI (ground truth for Atari objects);
  - Synthetic Monitoring Environments;
  - Prioritized Level Replay;
  - "Compiled Agency" (arXiv 2609.18996), not fetched.
- Phrases that returned nothing relevant: "benchmark mechanics probe agent" and "assumption checking game agent".

---

## Part C — the verdicts that matter

**C1. Statement 1**

The closest published results are two:
- Goldman & Kearns 1995, Lemma 1 (the singletons-plus-empty class) covers the identification half.
- The immobile-hider search game (Gal 1979, read only as stated by Alpern & Lidbetter) covers the cost half.

*The first half follows directly.* It says that before the first level end the consistent set is every not-yet-entered reachable cell plus h0. Under H_place plus h0, the only evidence before the first end is "entered c, no end". Each such entry removes exactly H_place(c) and nothing else. That is Lemma 1's observation that each example separates one singleton from the empty concept. It is a one-line argument and should be cited, not proved.

*The second half is not a bound as written.* It says "expected G_act ≥ expected first-hitting time ÷ cells visited". But G_act is defined as T_hit / N(T_hit), so for a fixed policy and goal the relation is an identity. Beyond that:
- E[T/N] and E[T]/E[N] are not equal in general, and the statement does not say which it means.
- T/N ≥ 1 always.
- The only content that holds for every policy is the minimax or Bayesian search value, which the search-game literature gives, for example the total length of a tree. That value carries no division by cells visited, and nobody we read has converted it to one.
- Under a registered coverage policy, E[T_hit/N] on the reachable-cell graph is a calculation, not a theorem.

*Two scoping gaps must be closed in the text:*
- Statement 1 holds only relative to the prior-free class H_place. A frame-only agent that ranks cells by visual features can commit to the right goal before any level end. Twin (ADDED-1) did so on most levels it cleared, so the statement must say it is about H_place, not about everything visible in the frames.
- Without h0, an agent that has entered every reachable cell but one identifies the goal by exhaustion before any level end. With h0, identification (|H| = 1) is never reached, because h0 is never contradicted. The statement has to fix which version it means.

**C2. Statement 2**

The closest published result is Keren, Gal & Karpas 2014, Theorem 2: past wcd observed actions, at most one goal remains consistent. Wayllace et al. 2016 gives the expected-cost analogue.

*Statement 2 does not follow from it, directly or with a short argument.* The gaps are exact:
1. The observation there is the actor's action sequence; ours is (cell, features, level-end) outcomes.
2. Elimination there comes from the actor's optimality; ours comes from contradiction with outcomes, with no assumption on the policy.
3. The unit there is actions; ours is level-end events.
4. There is no transfer across episodes and no feature class there. Our assumption that the goal feature is the same in every level is our own.
5. The bounded party there is an outside observer; ours is the learner itself.

Only the shape "past enough evidence the consistent set has at most one element" is shared. So goal recognition design is BASELINE for component (iv), not SUBSUMES.

*Statement 2 is covered by elementary learning theory.* It is version-space candidate elimination (Mitchell 1982; not fetched, so attributed on the standard definition), plus the teaching-dimension bound of Goldman & Kearns (at most |C| − 1 eliminations). **Verdict for Statement 2: SUBSUMES, by Goldman & Kearns and version-space elimination. Cite, do not prove.**

*Three defects in Statement 2 as written:*
1. h0 is never eliminated, so |H(t)| = 1 is never reached, G_end is always infinite, and "= 1 when the end cell carries a unique feature" is false. Identification must be redefined, for example as "exactly one non-h0 hypothesis left", or h0 must be made testable.
2. "1 + (d − 1) further ends" is not implied by elimination. An end at a cell whose features include every surviving candidate eliminates nothing, so the number of ends can be unbounded. Entering a feature-f cell without an end eliminates f at no cost in ends. The bound needs a stated condition, for example that each counted end removes at least one survivor.
3. "Unique feature" must mean that the end cell's surviving feature set has one element when cells carry several attributes.

With these fixed, Statement 2 is a short counting argument.

**C3. The census as prediction (component iii)**

The closest published attempt is Bontrager, Khalifa, Mendes & Togelius, AIIDE 2016 (ADDED-7), with its companion Mendes, Togelius & Nealen, CIG 2016 (ADDED-9, PROVISIONAL):
- They read 14 mechanics features from each GVGAI game's rule description and tried to predict which controller cluster succeeds.
- The features did not predict the performance clusters: 40.8% agreement, and a decision tree that overfitted.
- A two-feature selector still beat every single controller.

What ours does that theirs does not:
1. Our properties are measured from frames by interaction, and their accuracy against source-derived ground truth is itself tested (V1). Theirs are read from the rules and are exact by construction.
2. Our prediction target is first-level completion by a stated class of assumption-driven frame-only agents, not the best controller in a portfolio.
3. Our rule is frozen on 8 ARC train games and registered before any held-out run.

Other precedents to position against:
- Theory: Laidlaw et al. 2023 (ADDED-10). A measured property predicts deep-RL sample complexity, but from the full tabular MDP with reward.
- Held-out-game prediction: Gaina et al. 2018 (ADDED-8). A held-out-game split, but the prediction is made during the run from the agent's own experience.

Bontrager et al.'s negative result is the prior most relevant to our own risk (METHOD_BLUEPRINT.md Section 9).

**C4. The controllable-object probe (component ii)**

A2 is different in kind from Bellemare et al. 2012 and Choi et al. 2019, not a re-implementation. The specific differences:
1. **Output.** A2 outputs a per-key step vector: an agreed displacement of one changed-cell component. Bellemare outputs per-location contingency probabilities and a filtered centroid; Choi outputs an attended location. Neither outputs a displacement per action.
2. **Criterion.** Their shared criterion is dependence on the action: a location whose colour differs across actions, or a region that predicts the action. That criterion is our A1. A2 adds consistency of motion: the same displacement on at least 3 presses, with a 2:1 margin over the runner-up.
3. **Mechanism.** A2 is a fixed counting rule with no fitted weights, on exact integer-colour frame differences. Bellemare fits a logistic regression, with labels from emulator resets or a learned model and a threshold its authors could not fix across games. Choi trains a neural network.

What A2 reuses from them is the idea itself: find the one part of the frame the actions control, from frames alone, assuming a single avatar. That idea is theirs and must be credited.

The nearest neural analogue of A2's displacement-scoring is Transporter's "most controllable keypoint" rule (ADDED-12). The claim for component (ii) is therefore narrowed to the weight-free, displacement-agreement form with a per-key step output and an explicit "no controllable object" outcome, with its accuracy reported.

---

## Part D — gate G0 recommendation

**Recommendation (the decision is RKM's): cite and drop the theorem.**

1. The identification half of Statement 1 is the singletons-plus-empty example of Goldman & Kearns 1995, and its cost half is either an identity (G_act as defined) or the known value of immobile-hider search games. Statement 2 is version-space elimination bounded by the same teaching-dimension argument.
2. Goal recognition design is the closest formal quantity, but it bounds an outside observer of an optimal actor and subsumes neither statement. Statement 2 as written also has three defects that must be fixed before it is even a correct counting fact.
3. The paper should therefore:
   - keep G_end and G_act as defined, measured quantities, with the corrected Statement 2 and Statement 1's first half stated as cited observations (METHOD_BLUEPRINT.md Section 5 rule);
   - make no claim of a new bound;
   - stand on components (i)–(iii), none of which is killed.

---

## Part E — the three closest papers overall

1. **Bontrager, Khalifa, Mendes, Togelius 2016 (AIIDE).** Related-work sentence: *"The closest prior attempt to predict agent success from game mechanics, Bontrager et al. (2016), read features from GVGAI rule files and found they did not predict which controllers succeed; our census measures its features from frames, reports their accuracy against source-derived ground truth, and registers its prediction of first-level completion before any agent is run."*
2. **Bellemare, Veness, Bowling 2012 (AAAI).** Related-work sentence: *"Bellemare et al. (2012) introduced contingency awareness — detecting from frames the screen regions an agent's actions control — and froze their parameters on training games before testing on unseen ones; our A1 is their contingency criterion at the level of whole frames, and our A2 adds a fixed, weight-free test that the controlled region moves by a consistent per-action displacement."*
3. **Keren, Gal, Karpas 2014 (ICAPS), with Wayllace et al. 2016.** Related-work sentence: *"Goal recognition design (Keren et al., 2014) measures how long an outside observer can remain unsure of an optimal actor's goal; our goal-identification cost instead counts the level-end events a frame-only learner needs to identify its own goal, and its bounds reduce to version-space elimination (Goldman and Kearns, 1995) rather than to distinctiveness."*

Next in line, and must-cite:
- Twin (arXiv:2608.14490): frame-only goal-hypothesis elimination on ARC-AGI-3, with visual priors.
- Diuk, Cohen, Littman 2008: the content of A3 and A4, with objects given.
- Choi et al. 2019: learned controllable-region localisation.

---

## Open reads and corrections for RKM

**Not read, needed before the related-work section is written:**
- Gal 1979 and Alpern & Gal 2003 (search games);
- Zoroa et al. 2013 (search on lattice nodes);
- Angluin 1988 (queries);
- Mitchell 1982 (version spaces);
- Deng & Papadimitriou 1990;
- Dockhorn & Apeldoorn 2018 (GVGAI forward-model learning; possible BASELINE for component i);
- the full text of Skalse et al. 2023, Keren et al. 2016 and Mendes et al. 2016.

**Corrections to the CLAUDE.md cite list:**
- "Kunanusont et al., forward-model learning" is a pixel-DQN paper; the forward-model paper is Dockhorn & Apeldoorn 2018.
- MDP Playground is JAIR 2023, not JMLR.
- "Stephenson et al. 2025" is unidentified; RKM to confirm (Part A 14b).
- Rudakov et al.'s full title includes "Interactive Reasoning Tasks".
- The "human-performance paper" appears to be the ARC Prize blog post plus the technical report's human section.
