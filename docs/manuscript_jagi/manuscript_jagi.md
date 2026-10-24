---
title: "A Frame-Only Census of Game Mechanics Built on ARC-AGI-3 Failed a Preregistered Generality Test on MiniGrid/BabyAI and Procgen"
lang: en-US
---

::: {custom-style="Author Address"}
Independent Researcher, Ranchi, Jharkhand, India

ORCID 0009-0004-9671-4055

mishra.rahul98@gmail.com
:::

## Abstract

::: {custom-style="Abstract Text"}
A general agent that meets an unseen game must learn from interaction how the game works. I asked whether a cheap description of an unseen game's mechanics, read from frames before any agent is chosen, carries over from the benchmark on which it was built to games from other benchmarks. Before any confirmatory run, I registered the claim that a fixed battery of frame-only probes, the assumption census, with every parameter frozen on eight ARC-AGI-3 games, would report five mechanical assumptions of unseen games as each game's source code states them, and would predict on which games assumption-driven frame-only agents complete the first level. Test V1 compared the census with source-derived truth tables; test V2 compared a census score with first-level completion by three agents. The census and the agents ran on 161 MiniGrid/BabyAI environments under two action conditions and on 14 Procgen games, 10,500 runs in all. By the registered outcome table the result is a refutation, under the clause "V1 fails on any suite". V1 failed for three or four of the five assumptions on each suite and condition, and no agent passed V2. On all six primary MiniGrid/BabyAI lines, a baseline built from grid area, action count and color count ranked the games better than the census did. An exploratory reading suggests that for four assumptions the probes and the truth definitions were different constructs. An instrument never scored against known truth where its parameters were set brought no evidence of generality to the other benchmarks.

**Keywords:** preregistration; generality; frame-only agents; benchmark transfer; negative result; MiniGrid, Procgen, ARC-AGI-3
:::

## 1 Introduction

A general agent has to cope with environments it has not seen. One widely cited definition takes intelligence to be an agent's ability to achieve goals in a wide range of environments (Legg and Hutter, 2007). Game benchmarks turn that idea into a test. The first General Video Game Playing Competition asked for a single agent that can play many different games, some of them unknown to the entrants when they submitted, and left it to the agents to discover the mechanics of each game (Perez-Liebana et al., 2016). This article is about one small part of that problem: whether the mechanics of an unseen game can be described cheaply, from the screen alone, by an instrument that was built on a different benchmark.

The agents in question are frame-only. Such an agent sees the picture on the screen and is told when a level or the game ends, and nothing more. It receives no score, no list of objects, no text and no access to the game's code, and it chooses an action from a fixed set after each frame. The agents studied here also carry built-in assumptions about how games work, for example that one object on the screen is the player and that the arrow keys move it one cell at a time. The idea this study tested is that such an agent does well where its assumptions hold and poorly where they fail. If one could tell, before running any agent, which assumptions an unseen game satisfies, one could predict where such agents will finish the first level, and choose or build agents accordingly. The same description would also tell an evaluator whether the games of a new benchmark share the mechanics that a family of agents relies on.

The assumption census was meant to supply that description. It is a fixed set of probes that reads frames only and reports, for each game, whether five mechanical assumptions hold. A1, input coupling, says that the actions change the picture and that different actions change it differently. A2, one controlled object, says that exactly one object on the screen moves as a fixed function of the action. A3, lattice motion, says that each movement action shifts that object by a constant step whenever it is not blocked. A4, blocking by a fixed obstacle set, says that whenever a move has no effect, a fixed set of obstacles explains it, and that this set changes only through the agent's own actions. A5, place goal, says that a level ends when the controlled object enters a particular place, with no other condition at that moment. Each assumption is a property of the game, and each can be read off the game's source code. The census tries to infer them from play.

The question of generality is built into how the census was made. I set its parameters while developing a planner on eight of the 25 public games of ARC-AGI-3, and I then froze them. The registered protocol states that ARC-AGI-3 "is the development instance and does not count toward generality". Generality was to be shown on two benchmarks the census had never been tuned on: MiniGrid/BabyAI, which joins MiniGrid (Chevalier-Boisvert et al., 2023) and BabyAI (Chevalier-Boisvert et al., 2019), and Procgen (Cobbe et al., 2020). The census either describes the mechanics of games from those benchmarks, as their source code states them, or it does not.

I preregistered the claim because it is easy to fool oneself with an instrument of this kind. Almost any reading of its output on new games can be made to look sensible after the fact. A preregistration fixes, before any confirmatory data exist, the claim, the games, the truth against which the instrument is scored, the tests, their thresholds and the consequence of each outcome. The author then commits to reporting what the tests return, whatever it is, and to changing the protocol only through dated amendments that state what changed and why.

The outcome, by the registered outcome table, is a refutation: the census failed the validity test V1 on both confirmatory benchmarks, and no agent passed the prediction test V2 on any of them. Section 2 places the study among earlier work, Section 3 gives the method and every departure from the registered protocol, Section 4 the registered results, Section 5 an exploratory diagnosis written after the outcome, and Section 6 what the failure means for claims of generality.

## 2 Background

Six lines of earlier work bear on the study: general game playing, the measurement of general intelligence, the ARC benchmarks, finding the controlled object from frames, holdout reuse, and preregistration. The last subsection describes the closest earlier attempt to predict agent success from game mechanics, which also failed.

### 2.1 General Game Playing and GVGAI

Genesereth et al. (2005) define a general game playing system as one that can accept a formal description of a game and play it effectively without human intervention, and contrast it with specialized players that rely on algorithms designed in advance for specific games. Their agents receive the rules. The General Video Game AI framework moved the problem toward games whose rules the agent is not shown. Its organizers presented the competition as an approximation of general artificial intelligence, because the amount of game-dependent heuristics had to be severely limited (Perez-Liebana et al., 2016). Five years after the framework was released, Perez-Liebana et al. (2019) describe it as games written in the Video Game Description Language and a set of tracks in which agents play unknown games with or without access to a simulation of the game, or design new levels or rules. The agents studied here sit at the hard end of that range: they have no rules, no simulation and no score, only frames and the signal that a level has ended.

### 2.2 Measuring General Intelligence and Designing Benchmarks

Legg and Hutter (2007) took as their informal working definition that intelligence measures an agent's ability to achieve goals in a wide range of environments, and turned it into a formal measure for arbitrary machines. Hernández-Orallo (2017) argues for a universal evaluation of cognition, in which living organisms are a special case, and uses algorithmic information theory as the foundation for questions such as whether the difficulty of a task can be derived from the task itself. Chollet (2019) argues that skill at any given task falls short of measuring intelligence, because unlimited priors or training data can buy arbitrary levels of skill, defines intelligence as skill-acquisition efficiency, and presents the Abstraction and Reasoning Corpus (ARC), a benchmark built on an explicit set of priors designed to be close to innate human priors. All three treat the set of environments, and what an agent brings to them, as part of what a measurement means. The census is a much narrower thing, a description of the environments themselves, but it raises the same question: whether a description that was checked on one set of environments means the same on another.

### 2.3 ARC and ARC-AGI-3

ARC-AGI-3, which carries the ARC name, is a set of interactive games in which each game must be learned from interaction alone. Its 25 public games were the development instance of this study. Rudakov et al. (2025) published a graph-based explorer for these games, which is one of the agents used here. Liew (2026) classifies the public games by the simplest strategy without reasoning that reaches a level, a classification that concerns reachability rather than mechanics and makes no registered prediction. Skoutnev et al. (2026) identify goals with a coding agent built on a large pretrained model, which writes an executable world model of each game and so brings a learned prior; that places it outside the prior-free class studied here.

### 2.4 Contingency and the Controlled Object

The census builds on earlier work on finding, from frames alone, the part of the screen that the actions control. Bellemare et al. (2012) brought contingency awareness into reinforcement learning, defining contingent regions as the parts of an observation whose next value depends on the agent's action. Choi et al. (2019) learned controllable regions with a neural network. The first two census assumptions take that idea from them and replace the learned components with fixed counting rules: A2 adds a weight-free test that the controlled region moves by a consistent displacement for each key.

### 2.5 Holdout Reuse

When the same held-out set is consulted again and again while choices are made, choices can come to fit it (Blum and Hardt, 2015). Roelofs et al. (2019) measured this effect across many machine learning competitions and found little of it. The study kept a fixed split of the ARC-AGI-3 games for that reason, and kept the two confirmatory benchmarks out of development altogether.

### 2.6 Preregistration in Machine Learning

Bertinetto et al. (2021) describe a model of preregistration for machine learning research, in which the experimental protocol is fixed and reviewed before the experiments are run. The protocol of this study follows that model without the review: it was fixed, tagged in the repository and registered on the Open Science Framework before any confirmatory game was played.

### 2.7 The Prior Negative Result

The closest earlier attempt to predict agent success from game mechanics reported a mainly negative result. Bontrager et al. (2016) read mechanics features from the rule files of general video game playing games. A clustering of the games by those features agreed poorly with a clustering by controller performance, and the authors concluded that the features were not good indicators of performance. A selection agent built on two of the features did beat each of its constituent controllers on the same games. One possible objection to that design is that features read from rules say nothing about whether an agent could perceive them. Another is that the target, the best controller from a portfolio, was not tied to any assumption the features express. This study was designed to meet both objections. The census measures its features from frames, as an agent would; its accuracy against source-derived truth is tested separately, as test V1; and its prediction target, first-level completion by a stated class of agents that rely on the assumptions, is tested as V2, registered before any run. Two other lines of work predict success from different information. Laidlaw et al. (2023) predict the sample complexity of deep reinforcement learning from a property of the full tabular decision process with its reward, which a frame-only agent does not have. Gaina et al. (2018) predict wins on held-out games from an agent's own experience during play, not before it.

## 3 Method

This section describes the instrument, the benchmarks and how each was presented to it, the truth tables, the agents, the registration, the tests, the exclusions, the runs and the checks, and ends with every departure from the registered protocol. The file and line of each registered constant, the full amendment trail, the exclusion lists and the hashes of the frozen files are in the supplement.

### 3.1 The Instrument

The census reads the run of one agent, the planner N described below, on a game for 20,000 actions per seed. It uses the frames of that run and the signals that a level or the game has ended, and nothing else: no reward, no symbolic state, no text. From the planner's report at the end of the run it makes five decisions per seed, with rules written into the registered protocol and implemented in the frozen analysis code. A1 holds when some key has a learned shift and the tried keys' shifts are not all equal. A2 holds when some key was accepted as moving one object and the planner located that object. Acceptance needs three agreeing presses with a margin of 2:1 over the next most frequent displacement.

A3 holds when A2 holds and the planner's model of the first level did not end in a failure of prediction or localization. A4 holds when A3 holds and the planner never walked through a color it had classified as a wall. A5 holds when a place recorded at a level end later ended a level again. It fails when such a place was reached without a level end and never confirmed, and it is undetermined otherwise. The verdict for a game is the majority over its 10 seeds: it holds if at least half of the seeds say so, else it fails if at least half say so, else it is undetermined.

I froze every parameter of the census before registration and copied each into the protocol from its source file. They include three agreeing presses to accept a key, the 2:1 margin, at most eight presses per key while learning, a planner search limit of 40000 nodes, and a motion detector that needs at least 2 changed cells. Six files hold the census and its two agents. Their git blob hashes are registered (Supplement, Section S.6), and the runner refused to start if any of them differed.

I set these parameters while developing the planner on eight ARC-AGI-3 training games. I kept the other 17 public games as a held-out set whose source code I never opened. The split is fixed in a file of the repository. That file held 18 games in the held-out set until 21 September 2026, when I moved one of them, dc22, to the development set to debug the agent's wall learning on it, before any detailed study of the game. The protocol provided for a truth table derived from source for the eight development games, and for V1 on them, labeled development, once that table existed. I never wrote the table, so the census was never scored against source-derived truth on its development instance. The registered ARC-AGI-3 baseline ran my agents R and N on all 25 public games with 10 seeds and 20,000 actions under the registered code, 500 runs in all.

### 3.2 The Benchmarks and How Each Is Presented

The frozen code presses six key identifiers only, so every benchmark is presented to it through a fixed key map of at most six actions. On MiniGrid/BabyAI the environments run with minigrid 3.1.0, gymnasium 1.3.0 and Python 3.11.9, and there are two conditions. Under primitive actions the keys are turn left, turn right, forward, pickup, drop and toggle. Under absolute moves they are north, south, west and east, each a turn to face that direction followed by a step forward, plus pickup and toggle. The action "done" is offered in neither condition, and "drop" is not offered under absolute moves. The grid is rendered with 8 × 8 pixel tiles, each distinct tile pattern receives an integer index, and the four orientations of the agent's triangle are merged into one index. The grid is then placed at the top left of a 64 × 64 canvas, one row down, because the frozen code reads rows 1 to 62 only.

On Procgen (procgen 0.10.7, Python 3.10, easy mode, sequential levels) the keys are up, down, left, right and two special actions. Frames are 64 × 64 color images, mapped to integer indices by exact color and capped at 64 indices. The frozen code does not see the top and bottom pixel rows, which was recorded and not corrected. The primary condition draws the whole level into the frame (center_agent off). In that view the agent can be very small, and the census detects motion only when at least 2 cells change. The protocol therefore registered an operating range before any run: the games whose agent spans at least 2 pixels. Nine of the 14 confirmatory games fall in that range, and Procgen results are reported over all 14 games and again over these nine.

The secondary condition, a view centered on the agent, turned out to be identical to the primary one on most games. Ten Procgen games set the camera option themselves at every level start, and nine of them are confirmatory games, exactly the nine in the operating range. A camera check found 401 of 401 frames identical between the two conditions on those ten games, and a difference from the first frame on the other six. The secondary condition is therefore distinct on five games only, and it is reported there and never tested.

### 3.3 Truth from Source

Each benchmark has a truth table, committed before the protocol was registered, with one line per environment. For MiniGrid/BabyAI I read the entries by hand from the installed minigrid 3.1.0 source, once per environment class and its step function or instruction verifier. For Procgen I read them from the C++ source at tag 0.10.7. Each entry names the file and line that justify it, and the definitions of A1 to A5 used by the truth tables are written out in the protocol. Under primitive actions A3 fails on every MiniGrid/BabyAI environment, because the displacement of forward depends on which way the agent faces. On the 161 confirmatory MiniGrid/BabyAI environments, A1, A2 and A3 under absolute moves hold everywhere, A4 fails on 5 and A5 holds on 36. On the 14 confirmatory Procgen games, A2 holds on 6, A3 on 2, A4 on 13 and A5 on 6. The truth tables are the registered answer key of test V1; the census is the instrument under test.

### 3.4 Agents

Three agents ran on every game, seed and condition. R is my explorer, which tries actions and records the frames it has seen, and it is evidence for V2. N is my planner, which learns a step vector for each key, locates the controlled object, plans toward unexplored places and tests goal hypotheses. N uses the five assumptions by construction, so its V2 lines are an instrument check only. Its runs also supply the census. I1 is the graph-based explorer of Rudakov et al. (2025), run unchanged behind a boundary adapter, and it is evidence for V2. I1's own code maps five actions, so it has no toggle on MiniGrid/BabyAI and no second special action on Procgen.

### 3.5 Registration and Amendment Trail

I registered version v1 of the protocol on 27 September 2026 as git tag prereg-v1 on commit 19f2a9f25043997d1deffd5976f2f2150e5f086f. On the same day I registered it on the Open Science Framework (OSF) as an open-ended registration (https://osf.io/2znhw). It fixed the claim, the agents, the census rules and constants, the truth tables, the benchmarks and their splits between pilot and confirmatory games, the seeds and budget, the tests and thresholds, the analysis code and the outcome table. The registered claim, in the OSF text, reads:

> A fixed, cheap, frame-only probe battery (the assumption census: A1 input coupling, A2 one controlled object, A3 lattice motion, A4 blocking by a fixed obstacle set, A5 place goal), with every parameter frozen on eight ARC-AGI-3 training games, (i) reports the ground-truth mechanics of unseen games at a registered accuracy, and (ii) predicts, before any agent is run, on which unseen games assumption-driven frame-only agents complete the first level. Ground truth is derived from each game's source code and committed before any run. A goal-identification cost G is measured and reported alongside, not tested. ARC-AGI-3 is the development instance and does not count toward generality.

The claim sentence differs in wording between the two registered texts of v1. The git-tagged protocol names the goal-identification cost G as part of the battery and says "in three suites". The OSF text describes G as "measured and reported alongside, not tested" and names no number of suites. The tests, thresholds and outcome table are the same in both. G counted level ends until one goal hypothesis was left. Its elimination steps over places are the singletons-plus-empty example of Goldman and Kearns (1995), which they state in complement form, and its elimination over features is version-space elimination in the sense of Mitchell (1982), so the protocol cited them rather than proving anything new. Goal recognition design is related but different: Keren et al. (2014) bound the number of actions an optimal actor can take before an outside observer can tell its goal, and Wayllace et al. (2016) extend that measure to an expected cost under stochastic action outcomes, whereas G concerns a learner's own goal.

The protocol also fixed the pilot rules. The pilot games, six MiniGrid/BabyAI environments and two Procgen games, could be run before the confirmatory set and are excluded from every confirmatory analysis. The pilot could change adapter code but never a census constant, threshold, truth entry or frozen file. Every change had to be logged in the next version's dated diff section. After the pilot I registered version v1.1 on 27 September 2026 as git tag prereg-v1.1 on commit 8b2b2b9b432dbea4ba5f62cfceb1aad5558d1ecc, and on the same day on the OSF (https://osf.io/zu5vq). Both registrations have been public since 14 October 2026, when I ended their embargoes. I wrote version v1.2 after the outcome and tagged it prereg-v1.2 on commit 66e560645d9d98bca39ee7da9b1039ada1bc579b on 13 October 2026.

The amendment trail has 16 entries, D1 to D16, given in full in Supplement, Section S.3. D1 to D15 form the v1.1 diff, written on 27 September 2026 after the pilot and before any confirmatory game was played. D1 to D4 fix how each benchmark is presented through the six-key limit, D5 sets the per-run time caps, D6 the runner, D7 the boundary of I1 and D8 the infrastructure checks. D9 and D9b set the exclusions from V2, and D10 and D11 the analysis code at the tag. D12 sets a time cap for ARC-AGI-3 and the repeat of eight ARC runs that an unregistered clock had cut short. D13 records the Procgen camera identity, D14 the absence of any adapter change after the pilot, and D15 a separate replay planned for G. D16 is the only entry of v1.2, written after the outcome: it withdraws G without measuring it. No threshold, parameter, exclusion list, truth entry or analysis script changed after the prereg-v1.1 tag.

### 3.6 Tests and Thresholds

Test V1, instrument validity, compares the census's game verdict with the truth table, per benchmark, condition and assumption, over the confirmatory games. It passes when the share of agreeing games is at least 0.90 and Cohen's κ is at least 0.70. It fails when agreement is below 0.75, and anything between is "neither". κ is computed only where both truth values have at least 3 games; elsewhere agreement decides alone. An undetermined census verdict never counts as agreement, and for κ it is mapped to the value opposite the truth. That treatment of "undetermined" is in the registered text, which reads "An 'undetermined' census never agrees. For κ it is mapped to the value opposite the truth." The frozen analysis code at the tag implements the same rule.

Test V2, predictive validity, works per benchmark, condition and agent. Each game has a census score, the number of the five assumptions whose verdict holds (undetermined does not hold). It also has a conjunctive prediction, that A2, A3, A4 and A5 all hold, and an outcome: the agent completed the first level in at least half of its 10 seeds. The score is judged by the area under the receiver operating characteristic curve (AUROC) for the outcome. V2 passes when four conditions all hold. The AUROC is at least 0.80. The lower end of its 95% bootstrap interval, from 2,000 resamples of games with seed 20260927, is above 0.60. The balanced accuracy of the conjunctive prediction is at least 0.80. The AUROC exceeds that of a nuisance baseline by at least 0.10.

V2 fails when the AUROC is at most 0.65, and the test is void when the share of games completed lies outside [0.10, 0.90]. The nuisance baseline is a logistic regression of the outcome on grid area, number of actions and number of palette colors, fitted in-sample. It is the registered answer to the question of whether the census adds anything to the size and variety of a game. Evidence comes from R and I1, and a benchmark fails V2 when every non-void evidence agent fails. On MiniGrid/BabyAI the registered text tests V2 under absolute moves and reports it under primitive actions. On ARC-AGI-3, V2 on the 17 held-out games is reported and not tested.

Test V3, parameter transfer, requires every census constant and frozen file to be identical on every benchmark. The protocol registered it as a check of the adapter and code fields of every row. The analysis code does not compute that check, and no V3 line exists among its outputs. What the record does show is that the runner compared the six frozen files with their registered hashes before each confirmatory block and refused to start on any difference, and that its logs report all six matching for both blocks. The missing row-level check is among the deviations.

The protocol fixed three outcomes and the venue that each would allow, before any confirmatory run. Support needed V1 to pass on both benchmarks and V2 to pass for R and I1. Partial needed V1 to pass everywhere with a weaker V2. Refute follows when V1 fails on any suite, or V2 fails on MiniGrid/BabyAI under absolute moves, or V2 is void on every suite. Its registered venue is "repository record only, at most an arXiv note". The table is reproduced in Section 4 (Table 3).

### 3.7 Exclusions from V2

Some MiniGrid/BabyAI environments cannot be completed by an agent whose key map lacks a needed action. The registered rule (D9) excludes an environment from an agent's primary V2 line when, on every seed, success cannot be reached without an action missing from that agent's map. The action may trigger success, or it may be a precondition of every successful episode. One environment has no success at all and is excluded for every agent. For R and N the rule excludes 6 environments under primitive actions and 49 under absolute moves, leaving 155 and 112. In the pilot, I1, which has no toggle, completed no level on a locked-door environment in any of its 20 runs. D9b therefore applied the same rule to I1's own key map, adding the 57 environments where success needs toggle on every seed. I1's primary lines exclude 63 and 78 environments, leaving 98 and 83. Procgen has no exclusion. Lines with the excluded environments included are reported and not tested. The lists, with identifiers, are in Supplement, Section S.4.

### 3.8 Seeds, Budget and Caps

Every agent ran with seeds 1000 to 1009 and a budget of 20,000 actions per game, seed and condition. The wall-clock cap per run was three times the longest pilot run: 3300 s on MiniGrid/BabyAI, where the longest pilot run took 1081.6 s, and 7500 s on Procgen, where it took 2481.5 s. The cap for the ARC-AGI-3 baseline was 3600 s. There were 9,660 confirmatory runs on MiniGrid/BabyAI (161 environments, 2 conditions, 3 agents, 10 seeds) and 840 on Procgen (14 games, 2 conditions, 3 agents, 10 seeds), 10,500 in all. Every run reached its budget, with 0 errors and 0 runs cut by the cap. The MiniGrid/BabyAI block ran on one CPU machine; it started on 28 September 2026 and had finished by 13 October 2026.

### 3.9 Checks Before and After the Runs

Four infrastructure checks were registered, and none computes a census or a test statistic. A fidelity check played 200 random actions twice per game and condition. It found identical frames in 334 of 334 comparisons on MiniGrid/BabyAI and 32 of 32 on Procgen. A pilot check read the 480 pilot runs, 360 on MiniGrid/BabyAI and 120 on Procgen, and found 0 errors and 0 runs short of the budget. It also projected the running time of every confirmatory configuration and found 0 over its cap, the largest projections being 1517.8 s and 2550.0 s. The camera check is described above. A determinism check compared, on the nine Procgen games where the two camera conditions draw the same frames, every secondary run with its primary run. All 270 of 270 pairs were identical in every field except timing and the condition labels, with 0 missing. The analysis code and the determinism check passed 20 of 20 synthetic tests at the tag before the analysis read any confirmatory row.

### 3.10 Deviations from the Registered Protocol

Eight departures from the registered protocol, or from what it implies, are recorded here. None changes a test, a threshold or the outcome. The first is D16, written on 13 October 2026, after the outcome was known. The registered claim says that the goal-identification cost G is "measured and reported alongside, not tested", and D16 withdrew G without measuring it, because the instrument it accompanies had failed V1.

The second concerns the venue. The registered consequence of a refutation is "repository record only, at most an arXiv note". On 13 October 2026, with no arXiv endorsement available to me, I recorded that the clause would be read as "at most a preprint" and that no journal submission would follow. After the preprint drafts of 14 October 2026 I reversed the second part and chose to seek peer review of the negative result. An earlier version of this article is a preprint on Zenodo, and this version is submitted to the Journal of Artificial General Intelligence. This changes no analysis and no number.

The third is a defect in the frozen analysis code, found on 13 October 2026 and recorded, not corrected. The code computes the two ARC-AGI-3 lines of V2 over all 25 public games, the eight development games included, instead of over the 17 held-out games. It also prints a per-agent verdict on them that has no registered meaning. The fourth is an omission rather than a departure. The pilot runs contained census verdicts for eight games that have truth-table entries, and a V1 comparison on them before the v1.1 tag would have shown the failure before the confirmatory runs. It was not registered and I did not make it; I recorded it as a lesson on 13 October 2026. The fifth I found on 14 October 2026, while writing an earlier version of this article. The registered text tests V2 on MiniGrid/BabyAI under absolute moves and only reports it under primitive actions, but the frozen code prints verdicts, and a suite line, for the primitive-action lines as well. Those verdicts enter no outcome clause.

The last three I also found on 14 October 2026, while reviewing that earlier version against the protocol. The sixth: v1 provided for a truth table of the eight ARC-AGI-3 development games and for V1 on them, labeled development, once the table existed. The record listed the table as still outstanding at the v1.1 tag, and I never wrote it. The seventh: v1 listed I1 among the agents to run on ARC-AGI-3, but the registered ARC baseline ran R and N only. The eighth: V3 was registered as a check of every row's adapter and code fields, and the analysis code never computed it. The ARC-AGI-3 lines are reported and not tested, and V3 matters only for the outcome Support, so none of these three changes the outcome.

## 4 Results

The results in this section are the registered tests, exactly as the frozen analysis code wrote them. Where the code prints a verdict that the registered text does not test, the text says so. The full tables, with every statistic, are in Supplement, Sections S.1 and S.2; Tables 1 and 2 here give only the verdict of each line.

Figure 1 and Table 1 give V1. On MiniGrid/BabyAI under absolute moves, A1 and A2 pass and A3, A4 and A5 fail. Under primitive actions only A1 passes; A2, A3, A4 and A5 fail. On Procgen with the whole-level view, over all 14 games, A1 passes and the other four fail. On the nine in-range games, A1 is "neither", with agreement 0.8889, and A2 to A5 fail. The camera-on condition is reported and not tested. Cohen's κ is negative for A5 under absolute moves (−0.4125), under primitive actions (−0.3374) and on Procgen (−0.7843), and for A4 under absolute moves (−0.0435).

![Figure 1. Test V1: agreement between the census and the source-derived truth table, per assumption, for each benchmark and condition. Dashed line: 0.75, below which V1 fails. Dotted line: 0.90, which V1 needs to pass (with κ of at least 0.70 where κ applies). The word above each bar is the verdict printed by the frozen analysis code; a bar of agreement 0.0000 is not visible. Registered test; the values are those of Supplement, Section S.1.](fig1.png){width=100% fig-alt="Grouped bar chart of V1 agreement for assumptions A1 to A5 on each benchmark and condition, with the two threshold lines. Only A1, and A2 under absolute moves, reach the pass line."}

| benchmark and condition | games | A1 | A2 | A3 | A4 | A5 |
|----------------------------------|-------|------------|------------|------------|------------|------------|
| MiniGrid/BabyAI, absolute moves | 161 | PASS | PASS | FAIL | FAIL | FAIL |
| MiniGrid/BabyAI, primitive actions | 161 | PASS | FAIL | FAIL | FAIL | FAIL |
| Procgen, whole-level view, all games | 14 | PASS | FAIL | FAIL | FAIL | FAIL |
| Procgen, whole-level view, in-range games | 9 | neither | FAIL | FAIL | FAIL | FAIL |
| Procgen, view centered on the agent, camera-distinct games | 5 | reported, not tested | reported, not tested | reported, not tested | reported, not tested | reported, not tested |

: Table 1. Test V1, the verdict of each line as printed by the frozen analysis code at prereg-v1.1. The agreement and κ behind each verdict are in Supplement, Section S.1.

Figure 2 and Table 2 give V2. No agent reached PASS on any benchmark or subset. On MiniGrid/BabyAI under absolute moves, the primary line of R is void, because R completed the first level on 101 of 112 games, a share of 0.9018, above the registered 0.90. I1 is "neither" there, with AUROC 0.7187, and so is N, the instrument check. On the primitive-action lines, which the registered text only reports, the frozen code prints FAIL for R and I1, with AUROC 0.5224 and 0.5370. On Procgen over all 14 games I1 fails, with AUROC 0.6458, and R is "neither", with 0.7222. On the nine in-range games every agent is "neither". The intervals on Procgen are wide: over 14 games, let alone nine, the lower end of the 95% interval does not reach 0.60 for any agent, which the protocol anticipated before any run. The interval is not the only obstacle, though. Every Procgen line also has a balanced accuracy of 0.5000, below the registered 0.80, so no Procgen line misses a pass on the interval alone.

![Figure 2. Test V2: AUROC of the census score for first-level completion (filled circle) with its 95% bootstrap interval, and the AUROC of the nuisance baseline (open square), per agent and line. Dashed line: 0.65, at or below which V2 fails. Dotted line: 0.80, which V2 needs to pass, among three further conditions. The word at the right is the verdict printed by the frozen analysis code; the void line has no interval. The two ARC-AGI-3 lines are reported and not tested, and the "FAIL" printed on them has no registered meaning (Section 3.10). The primitive-action lines are reported by the registered text, so the "FAIL" printed on their primary lines enters no outcome clause. Registered test; the values are those of Supplement, Section S.2.](fig2.png){width=100% fig-alt="Dot plot of V2 AUROC with bootstrap intervals for agents R, N and I1 on each line, with the baseline AUROC beside each. No census point reaches the pass line together with the other three conditions."}

| line | R | I1 | N (instrument check) | benchmark line |
|--------------------------------|---------|---------|-------------|------------------------------|
| MiniGrid/BabyAI, absolute moves, primary | VOID | neither | neither | not failed (decided by I1 alone) |
| MiniGrid/BabyAI, primitive actions, primary (reported) | FAIL | FAIL | FAIL | suite FAIL (decided by R and I1) |
| Procgen, whole-level view, all games | neither | FAIL | neither | not failed (decided by R and I1) |
| Procgen, whole-level view, in-range games | neither | neither | neither | not failed (decided by R and I1) |
| ARC-AGI-3, 25 public games (reported) | FAIL | not run | FAIL | reported, not tested |

: Table 2. Test V2, the verdict of each agent and the benchmark line, as printed by the frozen analysis code at prereg-v1.1, for the lines that enter or could enter an outcome clause, and for the reported ARC-AGI-3 line. The lines with excluded environments put back, the camera-on lines and every statistic are in Supplement, Section S.2.

Under absolute moves the MiniGrid/BabyAI benchmark line is "not failed", a verdict decided by I1 alone because R is void. Procgen with the whole-level view is "not failed" over all games and over the in-range games. The primitive-action line reads "suite FAIL", but the registered text only reports that condition, so this line enters no outcome clause (Section 3.10).

The nuisance baseline ranked the games better than the census on all six primary MiniGrid/BabyAI lines: the three under absolute moves, which the registered text tests, and the three under primitive actions, which it reports (Figure 2). Over all 14 MiniGrid/BabyAI lines, primary or not, the baseline is higher on 12. The two exceptions are reported lines under absolute moves with all games included, for N (census 0.6352, baseline 0.5752) and for R (census 0.6434, baseline 0.5589). On Procgen the baseline is below the census on every line of the whole-level view.

The two ARC-AGI-3 lines are reported and not tested, as registered. Because of the defect recorded among the deviations, they are computed over all 25 public games rather than the 17 held-out games. The "FAIL" printed on them has no registered meaning and enters no gate. The line over the 17 held-out games is given, as exploratory, in Section 5.

Gate G3 applies the registered outcome table (Table 3). The outcome is a refutation, by the clause "V1 fails on any suite": V1 fails on MiniGrid/BabyAI in both conditions and on Procgen. The other two clauses of the refutation do not apply, since the V2 benchmark line under absolute moves is "not failed" and V2 is not void on every benchmark. One clause is enough. This classification was recorded on 13 October 2026, before any text about the results was written.

| outcome | definition (registered) | venue (registered) |
|----------|----------------------------------------------------------|------------------------------|
| Support | V1 passes on B (both conditions) and C, V2 passes for R and I1 on B-macro and C (not void), and V3 holds | JAIR full article |
| Partial | V1 passes everywhere, but V2 passes on B-macro only or is void on C, or passes on C for R only | IEEE Transactions on Games full paper |
| Refute | V1 fails on any suite, or V2 fails on B-macro, or V2 is void on every suite | repository record only, at most an arXiv note |

: Table 3. The registered outcome table, as fixed in the protocol before any confirmatory run (B: MiniGrid/BabyAI; C: Procgen; B-macro: MiniGrid/BabyAI under absolute moves).

## 5 Exploratory Diagnosis

This section is exploratory. It was written after the outcome was known, it tests nothing, and it changes nothing in the registered results above. Its numbers come from an exploratory script that calls the frozen analysis functions unchanged (Supplement, Section S.5). Two consistency checks come first, and both are exploratory. The census verdict stored in each of the 3,500 planner rows equals the verdict recomputed from that row's report, with 0 mismatches. The 25-game ARC-AGI-3 lines recomputed by the same functions equal those of the registered table to four decimals.

Figure 3 shows, for every V1 line, how the games split between truth and census, and Figure 4 shows how often single seeds disagree with their game's majority. Both are exploratory.

![Figure 3. An exploratory view of V1: for each benchmark and condition and each assumption, the games where the truth table says the assumption holds (bar h) or fails (bar f), split by the census verdict (holds, fails, undetermined). A missing bar is a truth class with zero games. Exploratory, read after the outcome was known; source in Supplement, Section S.5.](fig3.png){width=100% fig-alt="Stacked bars per assumption and condition showing, for games where the truth holds and where it fails, how many the census called holds, fails or undetermined."}

In this exploratory reading, for A1 the census agrees with the truth on 151 of 161 games under primitive actions, 159 of 161 under absolute moves, 13 of 14 on Procgen and 4 of 5 on the camera-on games. Every disagreement is a game where the truth holds and the census fails. On those games most seeds failed the per-seed A1 rule, which fails when no key has a learned shift or when every tried key has the same shift. A1, input coupling, is the assumption that the census and the truth table describe in nearly the same terms, and it is the only one with no failing V1 line.

The exploratory counts for A2 under primitive actions are these: 87 games have the truth holding and the census failing. On their 870 seeds the two turn keys were recorded as producing no movement on all 870, and forward was accepted on 208. A turn changes the agent's facing but not its cell, and the adapter merges the four facings into one tile index, so a turn changes nothing the census can see. Under primitive actions the census's A2 therefore rested on forward alone. Under absolute moves, where every move key displaces the agent, A2 agrees on 159 of 161 games. On Procgen there are 6 games where the truth fails A2 because other entities also respond to the action. The census rule has no clause for that, and on these games it found one controlled object on at least 9 of 10 seeds.

The exploratory counts for A3 under absolute moves are these: 92 games have the truth holding and the census failing. Four step vectors were accepted on 850 of their 920 seeds, so the learned motion was mostly right. Of the 775 seeds whose verdict is "fails", 755 carry the planner's first-level outcome "mispredicted" and the other 20 never located the agent. The census's A3 failure therefore comes from the planner's prediction during play, not from the learned step vectors. Under primitive actions the truth fails everywhere, because forward depends on facing, and the census says "holds" on 73 games. One step vector per key, learned from the starting facing, cannot reveal a dependence on facing while the turns record no shift.

For A4 the exploratory reading is short. The census rule for A4 is conditional on A3, so most A4 failures on MiniGrid/BabyAI follow from those of A3. On Procgen the counter of walked-through "walls" is above zero on some seeds of all 13 games where the truth holds A4, and on all 10 seeds of 5 of them. That counter rises when the planner walks through a color it had classified as a wall. The counters do not say whether that came from the game's obstacles, from momentum or from the planner's classification.

For A5, the exploratory counts show that most seeds with an undetermined verdict never recorded a goal place at all: 620 of 663 under absolute moves, 986 of 1,074 under primitive actions and 70 of 110 on Procgen. A place is recorded only at a level end, so on these seeds the census had nothing to test. The census said "holds" where the truth fails on 23 games under absolute moves and 15 under primitive actions, and on 0 Procgen games. Success in each of those environments needs facing the target, a toggle or a pickup. They belong to the GoTo, GoToObj, OpenDoor, OneRoom, Fetch and Unlock families. The level then ends on a cell beside or in front of the target, and the census, reading places only, recorded that cell as a goal. In the same exploratory counts, the negative κ values for A5 come mostly from "undetermined", which the registered κ maps to the value opposite the truth. The cell "truth fails, census holds" used by κ therefore contains 23 census "holds" and 61 undetermined games under absolute moves (84 in all), 15 and 105 under primitive actions (120 in all), and 0 and 8 on Procgen (8 in all).

![Figure 4. An exploratory view of seed dissent: for each benchmark and condition and each assumption, the games split by how many of their 10 seeds give a census verdict different from the game's majority verdict. Exploratory, read after the outcome was known; source in Supplement, Section S.5.](fig4.png){width=100% fig-alt="Stacked bars per assumption and condition showing how many games have zero, one, two or more seeds that disagree with the game's majority census verdict."}

In the same exploratory data, seeds often disagree with their game's majority where the verdict depends on the course of the planner's run: its learning phase for A2, or its first-level outcome for A3 and A4 (Figure 4). At least one seed dissents on 134 of 161 games for A2 under primitive actions, 135 for A3 under primitive actions, and 111 each for A3 and A4 under absolute moves. Dissent is rare for A1 and A2 under absolute moves, on 3 and 6 games, and for A4 on Procgen, on 2 of 14 games.

The exploratory reading that ties these counts together concerns constructs. For A2 under primitive actions, and for A3, A4 and A5, the census probe and the truth definition are not the same construct. The census A2 asks whether some key moves one located object; the truth asks whether exactly one object's displacement is a fixed function of the action, turns included. The census A3 asks whether the planner's first-level model mispredicted; the truth asks whether each action's unblocked displacement is constant. The census A4 is conditional on A3 and counts walked-through "wall" colors; the truth asks whether every blocked move is explained by a fixed obstacle set. The census A5 asks whether a place recorded at a level end ended a level again, and it is silent when no level ends; the truth asks whether success is triggered by entering a place. In each case the census reads a by-product of one planner's run, while the truth reads the environment's step function. This is a description of the mismatch, made after the outcome. It is not a fix and not a result.

On the 17 held-out ARC-AGI-3 games, the exploratory V2 line computed by the same frozen functions gives AUROC 0.3542 for N and 0.3403 for R, with the full line in Supplement, Section S.7. It is reported and never tested. None of this exploratory material supports a causal claim. These are counts of counters, read after the outcome was known.

## 6 Discussion

The registered answer is no on both counts: the census did not describe the mechanics of games from the two other benchmarks as their source code states them, and its score did not predict first-level success there. This section says what that implies for claims of generality, why the failure was invisible where the instrument was built, what could have caught it earlier, and what the study does not show.

### 6.1 What the Failure Means for Generality Claims

V1 compares the census verdict on each game with that game's entry in the source-derived truth table, and the two do not stand on equal footing. The truth table is the registered answer key: it was committed before registration, and each entry names the source line that justifies it. The census verdict is the instrument under test. A failing V1 line therefore says that the instrument disagreed with the answer key too often, on the registered games and by the registered thresholds. In plain terms, the census as registered does not measure that assumption on that benchmark. By the registered outcome table, a V1 failure on any benchmark decides the outcome by itself, whatever V2 shows, and a prediction built on a score that does not measure what it names would be hard to interpret even if it had passed.

For generality the finding has a specific shape. The census kept every parameter fixed across benchmarks, which was the registered meaning of transfer, and it still failed. Holding an instrument's parameters fixed is a statement about the procedure. It says nothing about whether the procedure measures the same property on new games. Legg and Hutter (2007) define intelligence over a range of environments, so a claim that an instrument describes environments in general is a claim about a range too, and it has to be tested on each part of the range it names. Chollet (2019) asks that a benchmark of general intelligence control for priors and experience; an instrument that characterizes games carries priors of its own, here the planner whose by-products the census read. The one assumption that held up across both benchmarks, A1, is the one whose probe and truth predicate say nearly the same thing. The others depended on how one planner's run went, and that dependence did not carry over.

For registered claims in this area the study shows the mechanism working as designed. The claim was stated before the data, the answer key was committed before the data, and the outcome followed from a clause written in advance. No reading of the results after the fact could turn the refutation into support, and none is offered here.

### 6.2 Why the Failure Could Not Show on the Development Benchmark

I set the census constants while developing the planner on eight ARC-AGI-3 games, and I wrote the per-seed rules on top of the planner's report. The protocol provided for a truth table derived from source for those games and for V1 on them, labeled development. I never wrote that table, so V1 was never computed on the development instance. The census was tuned to make the planner work, and nothing on ARC-AGI-3 measured whether its verdicts matched the games' mechanics. A disagreement between census and truth could not show there, because nothing there was looking for it. The registered phrase that ARC-AGI-3 "does not count toward generality" was meant to keep the development games out of the evidence; in practice it also kept them out of the one check that would have exposed the instrument.

### 6.3 The Pilot Check That Was Not Done

The pilot runs contained census verdicts for eight games, six MiniGrid/BabyAI environments and two Procgen games, all of which have truth-table entries. Comparing those verdicts with the truth before the v1.1 tag would have shown the disagreement before the 10,500 confirmatory runs were made. The protocol did not register such a check, and I did not make one. The pilot rules allowed adapter code to change after the pilot, but no census constant, threshold or truth entry. An early warning could therefore not have rescued the registered claim. It would have changed what was run next, and how much machine time was spent finding out.

### 6.4 The Nuisance Baseline

On all six primary MiniGrid/BabyAI lines, a logistic regression on grid area, action count and color count ranked the games by first-level completion better than the census score did. Three of those lines are tested by the registered text and three are reported. How large and how varied an environment is predicted completion better than the five assumptions as measured. This holds for the agents and conditions examined, and it is a statement about the measured census, not about the assumptions as properties of the games. On Procgen the baseline did not rank the games better than the census on any line.

### 6.5 The Methodological Mistake

The mistake, stated plainly and read from the exploratory diagnosis, is that the probes and the truth predicates were not the same constructs, and that no test existed where the parameters were set. The census decisions were by-products of one planner's run: whether it located an avatar from its first presses, whether its first-level model mispredicted, whether it walked through a color it had called a wall, whether a recorded place ended a level again. The truth entries are properties of the environment's step function. Only A1 is measured in nearly the same terms on both sides, and only A1 had no failing V1 line. I wrote the truth definitions and the census rules separately and never checked on any game, before registration, that one estimated the other.

### 6.6 What a Second Registered Study Would Have to Change

What follows are requirements for a different study, not a result and not an existing instrument. It would have to define each probe and its truth predicate as the same construct before registration, and show on development games that the two agree. It would have to write a truth table for the development instance and compute V1 there before registration, rather than leave it for later as this protocol did. It would have to register a V1 gate on the pilot games of every benchmark, with a stop rule, before any confirmatory run. It would have to register how "undetermined" enters each test, rather than mapping it to the opposite of the truth for κ, so that a silent instrument and a wrong one are told apart. And it would have to name, before registration, a nuisance baseline that the census must beat on the development instance.

### 6.7 What This Study Does Not Show

This study does not show that frame-only agents cannot complete these games, and it says nothing about their ability in general. It does not show that A1 to A5 are poor descriptions of the games; the truth tables say how often each holds, and that is not in question. It says nothing about the hidden ARC-AGI-3 games, which were not used, and nothing about agents that bring priors of any kind, visual or learned, to the games. It does not show that a differently built census would fail, and it does not show that instruments built on one benchmark cannot transfer to others. It shows that this instrument, registered with these thresholds, did not.

## 7 Conclusion

The registered objective was a frame-only census, fitted on ARC-AGI-3, that would report the mechanics of games from other benchmarks at a registered accuracy and predict where assumption-driven agents complete the first level. It failed in each registered respect. The instrument failed V1 on both confirmatory benchmarks, for three or four of the five assumptions depending on the benchmark and condition. The prediction test V2 passed for no agent on any benchmark, and on MiniGrid/BabyAI a baseline built from the size and variety of the environments ranked them better than the census did. The registered consequence followed: a refutation. For anyone who builds an instrument on one benchmark and means to use it on others, the record here is that freezing the parameters secured nothing about validity, and that the check which would have shown the failure, a comparison with known truth on the development games and on the pilot games, was the one that was never run.

## Data and Code Availability

All data and code are public in the repository https://github.com/rahul-k-mishra/arc3-frame-only-study under the MIT license. The data are the 10,500 confirmatory rows, 9,660 for MiniGrid/BabyAI and 840 for Procgen, one JSON file per benchmark, condition, agent, game and seed. They also include the 500-row ARC-AGI-3 baseline, the pilot rows and the outputs of the fidelity, pilot, camera and determinism checks, together with the analysis logs and the V1 and V2 tables. The code is every script that produced them, including the frozen census, the runner, the adapters, the analysis scripts, the exploratory diagnosis and the scripts that build and check this article's numbers and figures. The agent I1 is kept in its own directory with the upstream MIT notice of its authors. The registered protocol is at three tags: prereg-v1 (commit 19f2a9f25043997d1deffd5976f2f2150e5f086f), prereg-v1.1 (commit 8b2b2b9b432dbea4ba5f62cfceb1aad5558d1ecc) and prereg-v1.2 (commit 66e560645d9d98bca39ee7da9b1039ada1bc579b). The two registrations are https://osf.io/2znhw (v1) and https://osf.io/zu5vq (v1.1); both are public, and their registered texts are also in the repository. An earlier version of this article is on Zenodo under CC-BY 4.0 at https://doi.org/10.5281/zenodo.23375065. The supplement, with the full tables, the amendment trail, the exclusion lists, the provenance of every number and the hashes of the frozen files, is at SUPPLEMENT_DOI.

## Funding

This research received no funding.

## Conflicts of Interest

The author declares no conflicts of interest.

## References

::: {custom-style="References"}
Bellemare, M. G.; Veness, J.; and Bowling, M. 2012. Investigating Contingency Awareness Using Atari 2600 Games. *Proceedings of the AAAI Conference on Artificial Intelligence* 26(1): 864–871. https://doi.org/10.1609/aaai.v26i1.8321

Bertinetto, L.; Henriques, J. F.; Albanie, S.; Paganini, M.; and Varol, G. 2021. Preface. In Bertinetto, L.; Henriques, J. F.; Albanie, S.; Paganini, M.; and Varol, G., eds., *NeurIPS 2020 Workshop on Pre-registration in Machine Learning*, Proceedings of Machine Learning Research 148, i. PMLR. https://proceedings.mlr.press/v148/bertinetto21a.html

Blum, A., and Hardt, M. 2015. The Ladder: A Reliable Leaderboard for Machine Learning Competitions. In Bach, F., and Blei, D., eds., *Proceedings of the 32nd International Conference on Machine Learning*, Proceedings of Machine Learning Research 37, 1006–1014. PMLR. https://proceedings.mlr.press/v37/blum15.html

Bontrager, P.; Khalifa, A.; Mendes, A.; and Togelius, J. 2016. Matching Games and Algorithms for General Video Game Playing. *Proceedings of the AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment* 12(1): 122–128. https://doi.org/10.1609/aiide.v12i1.12884

Chevalier-Boisvert, M.; Bahdanau, D.; Lahlou, S.; Willems, L.; Saharia, C.; Nguyen, T. H.; and Bengio, Y. 2019. BabyAI: A Platform to Study the Sample Efficiency of Grounded Language Learning. In *International Conference on Learning Representations*. https://openreview.net/forum?id=rJeXCo0cYX

Chevalier-Boisvert, M.; Dai, B.; Towers, M.; Perez-Vicente, R.; Willems, L.; Lahlou, S.; Pal, S.; Castro, P. S.; and Terry, J. 2023. Minigrid & Miniworld: Modular & Customizable Reinforcement Learning Environments for Goal-Oriented Tasks. In *Advances in Neural Information Processing Systems 36*, 73383–73394. https://doi.org/10.52202/075280-3209

Choi, J.; Guo, Y.; Moczulski, M.; Oh, J.; Wu, N.; Norouzi, M.; and Lee, H. 2019. Contingency-Aware Exploration in Reinforcement Learning. In *International Conference on Learning Representations*. https://openreview.net/forum?id=HyxGB2AcY7

Chollet, F. 2019. On the Measure of Intelligence. Preprint, arXiv. https://arxiv.org/abs/1911.01547

Cobbe, K.; Hesse, C.; Hilton, J.; and Schulman, J. 2020. Leveraging Procedural Generation to Benchmark Reinforcement Learning. In Daumé III, H., and Singh, A., eds., *Proceedings of the 37th International Conference on Machine Learning*, Proceedings of Machine Learning Research 119, 2048–2056. PMLR. https://proceedings.mlr.press/v119/cobbe20a.html

Gaina, R. D.; Lucas, S. M.; and Perez-Liebana, D. 2018. General Win Prediction from Agent Experience. In *2018 IEEE Conference on Computational Intelligence and Games (CIG)*, 1–8. https://doi.org/10.1109/CIG.2018.8490439

Genesereth, M.; Love, N.; and Pell, B. 2005. General Game Playing: Overview of the AAAI Competition. *AI Magazine* 26(2): 62–72. https://doi.org/10.1609/aimag.v26i2.1813

Goldman, S. A., and Kearns, M. J. 1995. On the Complexity of Teaching. *Journal of Computer and System Sciences* 50(1): 20–31. https://doi.org/10.1006/jcss.1995.1003

Hernández-Orallo, J. 2017. *The Measure of All Minds: Evaluating Natural and Artificial Intelligence*. Cambridge University Press. https://doi.org/10.1017/9781316594179

Keren, S.; Gal, A.; and Karpas, E. 2014. Goal Recognition Design. *Proceedings of the International Conference on Automated Planning and Scheduling* 24(1): 154–162. https://doi.org/10.1609/icaps.v24i1.13617

Laidlaw, C.; Russell, S. J.; and Dragan, A. 2023. Bridging RL Theory and Practice with the Effective Horizon. In *Advances in Neural Information Processing Systems 36*, 58953–59007. https://doi.org/10.52202/075280-2573

Legg, S., and Hutter, M. 2007. Universal Intelligence: A Definition of Machine Intelligence. *Minds and Machines* 17(4): 391–444. https://doi.org/10.1007/s11023-007-9079-x

Liew, K. H. 2026. Explore Before You Solve: The Speed–Depth Trade-off in Epistemic Agents for ARC-AGI-3. Preprint, arXiv. https://arxiv.org/abs/2605.25931

Mitchell, T. M. 1982. Generalization as Search. *Artificial Intelligence* 18(2): 203–226. https://doi.org/10.1016/0004-3702(82)90040-6

Perez-Liebana, D.; Samothrakis, S.; Togelius, J.; Schaul, T.; Lucas, S. M.; Couetoux, A.; Lee, J.; Lim, C.-U.; and Thompson, T. 2016. The 2014 General Video Game Playing Competition. *IEEE Transactions on Computational Intelligence and AI in Games* 8(3): 229–243. https://doi.org/10.1109/TCIAIG.2015.2402393

Perez-Liebana, D.; Liu, J.; Khalifa, A.; Gaina, R. D.; Togelius, J.; and Lucas, S. M. 2019. General Video Game AI: A Multitrack Framework for Evaluating Agents, Games, and Content Generation Algorithms. *IEEE Transactions on Games* 11(3): 195–214. https://doi.org/10.1109/TG.2019.2901021

Roelofs, R.; Shankar, V.; Recht, B.; Fridovich-Keil, S.; Hardt, M.; Miller, J.; and Schmidt, L. 2019. A Meta-Analysis of Overfitting in Machine Learning. In *Advances in Neural Information Processing Systems 32*. https://papers.nips.cc/paper_files/paper/2019/hash/ee39e503b6bedf0c98c388b7e8589aca-Abstract.html

Rudakov, E.; Shock, J.; and Cowley, B. U. 2025. Graph-Based Exploration for ARC-AGI-3 Interactive Reasoning Tasks. Preprint, arXiv. https://arxiv.org/abs/2512.24156

Skoutnev, A.; Acharya, K.; Longhitano, G.; Udell, M.; Ellis, K.; and Drori, I. 2026. Twin: Playing an Unknown Game with a Test-Time Digital Twin. Preprint, arXiv. https://arxiv.org/abs/2608.14490

Wayllace, C.; Hou, P.; Yeoh, W.; and Son, T. C. 2016. Goal Recognition Design with Stochastic Agent Action Outcomes. In *Proceedings of the Twenty-Fifth International Joint Conference on Artificial Intelligence (IJCAI-16)*, 3279–3285. https://www.ijcai.org/Proceedings/16/Papers/464.pdf

:::
