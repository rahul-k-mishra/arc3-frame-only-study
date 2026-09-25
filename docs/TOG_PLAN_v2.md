# Plan v2: IEEE Transactions on Games submission

Prepared 25 September 2026. Replaces docs/TOG_PLAN.md. Every correction in
audit/TOG_PLAN_RUTHLESS_AUDIT.md is applied here; Section 11 maps each audit item to the place it
is handled. Every number below is either marked HAVE and named by the run file it comes from, or
marked NEED and does not exist yet. A HAVE number whose file is not named is marked UNTRACED and may
not enter the manuscript until a script ties it to a file.

## Working title

"Scoring, Selection, and Goal-Identification Failures of Frame-Only Agents on the ARC-AGI-3
Public Demonstration Set"

The old title ("Why Frame-Only Agents Plateau on ARC-AGI-3") is withdrawn. It claimed a general
cause and a general plateau. A published frame-based agent (Rudakov, Shock, Cowley, arXiv
2512.24156) solved a median 30 of 52 preview levels, so a general plateau statement is false as
written. The title may be revised again after E1; it may not become broader than this one.

---

## 0. What this paper is, and what it is not

It is a measurement study of one benchmark's public demonstration set (25 games) and of what
frame-only, prior-free, CPU-runnable agents do on it, with a formal definition of
goal-identification cost measured on those games.

It is not a new method, not a competitive result, not a statement about ARC-AGI-3's private
evaluation set, and not a statement that frame-only agents in general plateau.

The 25 public games are a demonstration subset published by the organisers. They are not a
random sample of ARC-AGI-3. The 17 held-out games are a split of that subset made by the author.
No sentence in any document may describe them as "the unseen ARC-AGI-3 test set" or say anything
about the private set.

Venue constraint: ToG full paper, 10 pages exactly, plus a supplement. Pages above 10 carry
mandatory charges and the author has no budget. Double-anonymous review: no names, handles,
affiliations, acknowledgements, or identifying links in the manuscript, the supplement, or the
code release.

---

## 1. Claims the paper may make, and the exact wording allowed

C1. Scoring structure (supporting). The environment score is derived from arc_agi/scorecard.py
(arc-agi 0.9.8), not from the technical report's prose equations. The report's displayed
equations use a fixed n = 5 example while the benchmark has variable level counts; the
implementation is the authority and the paper says so. What we add to the organisers' published
rule is the closed-form ceiling for a stated policy class (E4) and a measured decomposition.
Allowed: "under this scoring rule", "for an agent that completes the first k levels at a constant
ratio r".

C2. Selection transfer (supporting). Measured over 10,000 random 8/17 splits of the 25 games,
with a selection statistic fixed in Section 4 before the analysis runs (E5). This is not new as a
question (Balla et al. 2020; Stephenson et al. 2025; Blum & Hardt 2015; Roelofs et al. 2019); what
we report is its size on this benchmark and scoring rule. Allowed: "on splits of the 25 public
games", "for the six mechanisms of the primary matrix".

C3. Goal identification (central, if E9 and E10 deliver). Until they do, the only allowed
sentence is: "goal identification is the dominant observed failure mode for this instrument on
this public subset". Forbidden until E9/E10 support more: "the barrier is goal inference", "not
perception or search", any causal sentence built from planner counters alone.

C4. External agents (load-bearing for any statement about more than our own agents). Nothing is
claimed about "frame-only agents" as a family unless E1 meets its pre-registered rule
(Section 3). With fewer than two admissible independent agents, the paper speaks only of "the
agents we measured" and names them.

C5. CPU language-model cost (secondary, half a page at most). A feasibility bound for our two
machines, nothing more. Forbidden: "every leaderboard leader runs a GPU-served vision model", or
any statement about leaders' internals beyond what a dated, cited source says about a named
system.

Forbidden everywhere: statements about the private set; "necessary"/"impossible" in general;
"state of the art"; "frame-only agents plateau"; any number not in a JSON under runs/; any
sentence that cannot be pointed to a run.

---

## 2. Research questions and evidence status

RQ1. How does the scoring rule allocate credit, and what is the ceiling for an agent that
completes the first k levels at a constant action ratio r?
- Formula from arc_agi/scorecard.py: HAVE (source read, Section 5 of this plan).
- Measured decomposition of hash_state, held-out, 4 seeds x 20,000 actions, mean 0.3329:
  HAVE (runs/ablate_lenovo_6x4.json, mode hash_state).
- Counterfactuals AT HUMAN 3.0-3.8 vs recorded 0.30-0.46: HAVE, UNTRACED (the file and the
  g_decompose.py invocation that produced them must be recorded).
- 100,000 vs 20,000 actions, 0.3615 vs 0.3329: HAVE (runs/ablate_kaggle_giveup_100k.json against
  runs/ablate_lenovo_6x4.json). Only 2 seeds at 100k, below the 4-seed minimum; it may be
  reported only as a 2-seed observation until E3 replaces it.
- "1,088 held-out runs": UNTRACED. The number does not follow from one file. Before it is used,
  a script must list which files and modes it counts.
- Analytic ceiling validated against the scorecard: NEED (E4, scripts/g_ceiling.py).

RQ2. Does mechanism selection on a subset of public games transfer to the rest?
- One split: train pick held-out-best for 3 of 17 games; per-game oracle 0.3632 vs selected
  0.3329: HAVE, but which matrix produced 3/17 and 0.3632 is not recorded. E5 prints the fixed
  split for both matrices; whichever reproduces the numbers is named as their source.
- 10,000 random splits: NEED (E5, scripts/g_split_transfer.py).

RQ3. For a planner that checks its own assumptions at play time, which assumption fails, per game?
- v2 census, 4 seeds (runs/navrun_v2_heldout.json): HAVE, with two defects that must be fixed
  before use:
  (a) The categories cover 16 of 17 held-out games: no keys r11l s5i5 tn36 (3); no controllable
      object cd82 sb26 su15 (3); 2-D lattice walker cn04 ka59 re86 sp80 g50t (5); 1-D walker
      bp35 sk48 (2); key-controlled non-walker ar25 wa30 tr87 (3). sc25 is in no category. Its
      row must be read from the JSON by a script and stated.
  (b) The old plan says "none of the fourteen with a controllable object". The categories give
      10 (5 + 2 + 3), or 11 with sc25. The count must be recomputed from the JSON.
- goal_confirmed 0 of 17: HAVE (runs/navrun_heldout_full.json).
- 10 seeds, all 25 games: NEED (E6).
- Planner-dependent rows (frontier exhausted, stalled, junk step vectors) are kept separate
  from game-dependent rows (no keys, no controllable object, recorded goal falsified on retry).

RQ4. Do agents we did not write show the same pattern?
- Rudakov et al. agent through our harness: NEED (E1a).
- Official non-LLM templates: NEED (E1b); these are a baseline, not independent evidence.
- The "public CPU-only 0.26-0.27 agent" of the old plan: not verified (no repository, commit,
  licence or runtime established). It is dropped from E1 and from the text until it is traceable.

RQ5. What does a CPU-hosted LLM cost per action against the per-action budget?
- 7B, two machines, two encodings, 218-1,254 s per action against ~2.9 s: HAVE, UNTRACED to a
  file under runs/ (the speed-script outputs must be copied into runs/).
- 14B: NEED (E7), optional.

---

## 3. E1: external agents, with the decision rule written before any is run

These thresholds are fixed on 25 September 2026, before any external agent has been downloaded
or run. They may not be changed after an external agent produces any output. If a threshold
turns out to be ill-posed (for example, an agent cannot produce per-level counts), the defect is
reported and the agent is classified INCONCLUSIVE; the threshold is not edited.

Disclosure: the REPRODUCES thresholds (i)-(iii) below are the ones in the old plan, and they were
chosen after seeing our own agent's results. They are kept unchanged because changing them now
would be worse. The BREAKS thresholds are new and were set without seeing any external result.

### 3.1 Admissibility (checked before the agent's first game run; all must hold)

A1. Code at a pinned commit, stored under external/<agent>/ with its LICENSE file and the commit
    hash in external/<agent>/COMMIT.
A2. The licence permits running and modifying the code for research and publishing results.
    No licence, or a licence that forbids this: inadmissible, reported as such.
A3. Runs on CPU only. A hidden GPU requirement makes the agent inadmissible.
A4. No LLM or remote API calls at play time.
A5. The adapter changes only I/O: it maps our harness's (frame, available actions, level state)
    to the agent's input and the agent's output to one action. Policy code is not edited. Every
    changed line outside the adapter is listed in external/<agent>/PATCHES.md with the reason
    (API version changes only).
A6. Fidelity check: where the agent can be run in its own loop on the current engine, the first
    1,000 actions on ft09 and tu93 with a fixed seed are identical under its loop and ours. If its
    own loop cannot run on the current engine, this is stated and the agent is labelled "adapter
    only, fidelity not checked".
A7. Cost: at most 0.28 s per action on the lenovo, measured over 2,000 actions on each of ft09
    and tu93. This is what fits the full protocol (25 games x 10 seeds x 20,000 actions =
    5,000,000 actions) into 48 hours at 8 workers: 48 x 3600 x 8 / 5,000,000 = 0.276 s.
    Between 0.28 and 0.70 s per action: run 4 seeds instead of 10 (2,000,000 actions, 48 h
    at 0.69 s) and label every number "4 seeds". Above 0.70 s: run 4 seeds on Kaggle sessions
    if that finishes by 9 October, else inadmissible for cost, reported with the measured
    seconds per action.

### 3.2 Protocol

All 25 public games, seeds 1000-1009, 20,000 actions per run, the same environment files and
engine (arc-agi 0.9.8, arcengine 0.9.3), per-level action counts taken from the scorecard
(card_levels, card_baseline), resets counted as the scorecard counts them. Rows written in the
ablate format. If the agent's published configuration uses a different action budget, that
budget is run as a secondary arm and reported separately; the decision uses the 20,000 arm.

Per agent, computed on the 17 held-out games (the 8 train games, with tu93/dc22/ls20 labelled
source-informed, are reported beside them but do not enter the decision):
- M1 recorded: mean over games of the seed-mean scorecard score.
- M2 AT HUMAN: the score the same runs would have had if every won level had cost exactly the
  human count (same won levels, no extra level), mean over games of seed means; and the ratio
  M2/M1 (undefined if M1 = 0; then reported as "M1 = 0").
- M3 lv3+: the number of (game, seed) runs on held-out games that won level 3 or a later level.
- M4 levels: sum over the 17 held-out games of the seed-mean levels completed (levels per seed).
Reference values from our agent (hash_state, 4 seeds): M1 = 0.3329 (runs/ablate_lenovo_6x4.json);
M4 = 11.2 levels per seed summed over the 17 held-out games (docs/HANDOFF_GNAV.md, UNTRACED to a
script output; E2 recomputes it at 10 seeds before any external agent is scored).

### 3.3 Classification of each admissible agent (fixed)

REPRODUCES if all of:
  (i)   M1 < 0.5;
  (ii)  M2 / M1 > 5;
  (iii) M3 = 0.
BREAKS if any of:
  (iv)  M1 >= 1.0 (three times our 0.3329, rounded up);
  (v)   level 3 or later won on at least 2 held-out games, each in at least half of that
        agent's seeds;
  (vi)  M4 at least twice our E2 value of M4.
INCONCLUSIVE otherwise (for example M1 = 0.6, or a single lucky lv3 win), or if the agent
could not produce per-level scorecard counts.

### 3.4 What the paper says, by outcome (fixed)

- At least two admissible independent agents REPRODUCE and none BREAKS: the paper may say "the
  pattern (i)-(iii) holds for the N independent frame-only agents we measured on the public set".
  Still not "frame-only agents plateau".
- Any admissible independent agent BREAKS: this is a headline result. The abstract is rewritten
  around it; our agent's pattern becomes "a property of our agents, not of the agents measured".
- Fewer than two admissible independent agents by 9 October 2026: every family statement is
  removed; the paper speaks of the agents we measured, by name. The venue decision in Section 9
  is re-taken.
- The official non-LLM templates never count toward "independent". They are reported as a
  baseline.

"Independent" means authored by people other than the author of this paper, not derived from our
code, and not an organiser template.

### 3.5 Candidate order

E1a. Rudakov, Shock, Cowley, "Graph-Based Exploration for ARC-AGI-3", code at
     github.com/dolphin-in-a-coma/arc-agi-3-just-explore. First. Their result was on the preview
     games and the preview API; ours is the current 25-game public set and arc-agi 0.9.8. Both
     differences are stated wherever their number and ours appear together. We report what their
     agent does on the current games through our harness; we do not claim to have reproduced or
     refuted their preview result.
E1b. Official ARC-AGI-3-Agents non-LLM templates (random and any deterministic template).
     Baseline only.
E1c. Any other public CPU-only frame-based agent with a repository, licence and commit. If none is
     found, state that and how we searched (sources, dates, queries).

What must be true for E1 to mean anything: the adapter must not change the policy (A5, A6), and
the action accounting must be the scorecard's (3.2). How failure shows: a fidelity mismatch in A6,
or scorecard and level_log totals that disagree by more than probe and reset presses explain.

---

## 4. E5: selection transfer, specified before the analysis runs

Script: scripts/g_split_transfer.py. No game runs. Output: runs/split_transfer.json.

Matrices.
- Primary: runs/ablate_lenovo_6x4.json. 6 mechanisms (adapt_lazy, base, burst, death,
  hash_state, repeat_key), seeds 1000-1003, 20,000 actions, 25 games, 600 rows.
- Exploratory: runs/ablate_kaggle_20x1.json. 20 mechanisms, seed 1000 only, 10,000 actions,
  25 games, 500 rows. Its budget is half the primary's, so it is not a larger version of the same
  experiment; it is reported only as a sensitivity analysis and never mixed with the primary.
- Time-truncated runs (added 25 September 2026, from the actions, state and seconds fields only,
  before any score in either matrix was looked at). A run is time-truncated if it did not end in
  WIN and used fewer actions than the matrix's budget (the largest action count in the matrix).
  The primary matrix has none (its two short runs are WINs). The exploratory matrix has 47, all
  stopped at the 240 s wall-clock limit: reset_in_graph 25 of 25 (16-501 actions), object_state
  20 of 25, coarse_state 2, seek 2. Those four mechanisms did not get the same budget as the
  others. The exploratory analysis therefore uses the 16 mechanisms with no time-truncated run;
  the 20-mechanism version is printed as a sensitivity check and labelled as including truncated
  runs. The script counts truncated runs per mechanism and applies this rule itself.
- To be stated by the author in the manuscript: how the six primary mechanisms were chosen, and
  whether any held-out score had been seen when they were chosen.

Cell value. For game g and mechanism m: the mean over the matrix's seeds of the recorded
scorecard score (field "score"). Nothing is recomputed from level_log.

Selection statistic (fixed). For a train set T of 8 games: train(m) = unweighted mean over g in T
of cell(g, m). The pick is argmax_m train(m). If several mechanisms tie (to 1e-12), every outcome
is averaged over the tied mechanisms with equal weight.

Splits (fixed). 10,000 draws. Draw k uses numpy.random.default_rng([20260925, k]) and takes
8 of the 25 games without replacement as train; the other 17 are held-out. The draw does not
depend on the number of workers.

Outcomes per split, with H the 17 held-out games and ho(m) the mean over H of cell(g, m):
- best_hit: whether the pick is argmax_m ho(m) (ties: the pick counts as best if it ties the
  maximum; fractional if the pick itself is a tie).
- per-game hits: the number of games in H where the pick attains max_m cell(g, m); also the number
  of games in H where all mechanisms tie (these carry no information and are reported apart).
- pick_ho = ho(pick); best_ho = max_m ho(m); oracle_ho = mean over H of max_m cell(g, m).
- regret_best = best_ho - pick_ho; regret_oracle = oracle_ho - pick_ho.
- the pick's rank among mechanisms on H (1 = best, ties share the better rank).
- Kendall tau-b between train(m) and ho(m) over mechanisms.
- chance references: the probability a uniformly random mechanism is held-out-best, and the
  expected held-out score of a uniformly random mechanism.

Reported: the fraction of splits with best_hit; mean and 5/25/50/75/95 percentiles of each
outcome; how often each mechanism is picked; the same for the chance references.

Secondary analyses (fixed now):
- S1 pinned: tu93, dc22, ls20 (source-informed) always in train; 5 more train games drawn from
  the other 22; 10,000 draws seeded [20260926, k].
- S2 seed-noise check on the oracle (primary only): the in-sample oracle takes a maximum over
  noisy seed means and is biased upward. For each of the three ways to split seeds 1000-1003 into
  two pairs, choose each game's best mechanism on one pair and score it on the other, both ways;
  average the six. Report in-sample and cross-fitted oracles side by side.
- The author's fixed split (train tu93 ls20 vc33 m0r0 ft09 lp85 lf52 dc22) is printed for both
  matrices, with a per-game table that marks source-informed games.

What must be true. Every (game, mechanism, seed) cell is present exactly once; within a matrix
all runs use the same budget. How failure shows: the script stops on a missing or duplicate cell,
and prints the budgets found per matrix. On the fixed split the primary matrix must give a
hash_state held-out mean of 0.3329; if it does not, the loader is wrong and nothing else it prints
is used.

Limits stated where the result appears. The 10,000 splits are splits of the same 25 authored
games; they share games and are strongly dependent, so the fraction is a property of this set, not
an estimate for a population of games, and no p-value is attached. Seeds are nested within games.

---

## 5. E4: the analytic ceiling, derived from the implementation

Script: scripts/g_ceiling.py. No game runs. Reads only the "baseline_actions" list of each
environment_files/<game>/<version>/metadata.json; never lists or opens a game's .py file.
Output: runs/ceiling.json.

### 5.1 The rule as implemented (arc_agi/scorecard.py, arc-agi 0.9.8)

- Level i (1-based) of a game with N levels has human baseline h_i (metadata baseline_actions).
- Actions per level come from the card: cumulative action counts recorded when levels_completed
  changes; the level's actions are the difference. A reset also adds one action
  (Card.inc_reset_count).
- A completed level with a_i > 0 actions scores s_i = min(115, 100 (h_i / a_i)^2). A completed
  level with a_i = 0 scores 0. An uncompleted level scores 0.
- Weights are the level index: w_i = i. Let W_N = 1 + 2 + ... + N = N(N+1)/2.
- Weighted mean: A = (sum_i i s_i) / W_N.
- Environment cap: M = 100 (sum over i with s_i > 0 of i) / W_N.
- Environment score E = min(A, M).
- A card with several plays of the same game scores the maximum over plays
  (EnvironmentScoreList.score). The scorecard score is the mean of E over the games in the card.
- If the card records more completed levels than the metadata has baselines, the environment
  scores 0 ("Human baseline actions size mismatch").

### 5.2 Ceiling for the policy class P(k, r)

P(k, r): the agent completes levels 1..k (levels are sequential, so the completed set of one play
is always a prefix) and spends a_i = r h_i actions on each, with a constant r > 0.

Step 1. For i <= k, s_i = min(115, 100 / r^2) > 0, and it does not depend on h_i. For i > k,
s_i = 0.
Step 2. A = min(115, 100/r^2) (1 + ... + k) / W_N = min(115, 100/r^2) W_k / W_N.
Step 3. Every completed level has s_i > 0, so M = 100 W_k / W_N.
Step 4. E = min(A, M) = (W_k / W_N) min(115, 100/r^2, 100) = 100 (W_k / W_N) min(1, 1/r^2).
Step 5. W_k / W_N = k(k+1) / (N(N+1)).

    S(k, r, N) = 100 * k(k+1) / (N(N+1)) * min(1, 1/r^2).

Consequences, each a direct reading of Step 4:
- Under a constant ratio the per-level 115 cap never binds: the environment cap removes
  everything above 100.
- Being faster than a human (r < 1) on every level is worth nothing beyond r = 1.
- The human baselines cancel; only N matters.
- For any play that completes exactly k levels, whatever its per-level ratios, E <= M =
  100 k(k+1)/(N(N+1)). If every completed level has ratio at least rho >= 1, then
  E <= 100 k(k+1)/(N(N+1)) / rho^2.
- With mixed ratios the 115 cap can bind: a level faster than human can offset a slower one, but
  never beyond M.

Integer actions. a_i must be a whole number, so the achievable count at ratio at most r is
floor(r h_i) (at least 1), whose ratio is at most r. S(k, r, N) is therefore exact when every
r h_i is an integer; the script also computes the whole-action version through the scorecard's
own calculator, with a_i = max(1, floor(r h_i)), for each game.

### 5.3 Validation against the scorecard (the script fails loudly if any case disagrees)

The script implements E = min(A, M) independently and compares it, to 1e-9, with
EnvironmentScoreCalculator (add_level, to_score) and with EnvironmentScorecard.from_scorecard on a
constructed Card and EnvironmentInfo, on:
- V1 the closed form S(k, r, N) for N = 1..10, k = 0..N, r in {0.5, 0.9, 1, 1.5, 2, 5, 30},
  baselines chosen so r h_i is an integer;
- V2 cases where the environment cap binds: all levels at half the human count (weighted mean
  115, score 100); N = 3 with level 1 at r = 0.5 and level 2 at r = 1 (A = 52.5, M = 50, E = 50);
- V3 a completed level with 0 actions (score 0, weight excluded from M);
- V4 k = 0 (score 0), and an unfinished run with actions spent on level k+1 (no effect);
- V5 two plays in one card (the score is the maximum);
- V6 a reset adds one action to the level in which it happens;
- V7 more completed levels than baselines (score 0);
- V8 2,000 random heterogeneous cases (fixed RNG), comparing the independent formula with both
  scorecard paths.

What must be true: the installed arc_agi is 0.9.8 and scorecard.py is the file the runs used. The
script prints the file's path and SHA-256 and writes them into the output. How failure shows: any
mismatch is printed with the case and the script exits non-zero without writing the output.

### 5.4 Correction to the old plan's worked example

The old plan says tu93 "level 1 won at 356 vs 19 is worth 0.3 of 100". 0.3 is the level score:
100 (19/356)^2 = 0.2848. tu93 has N = 9 levels, W_9 = 45, and level 1 has weight 1, so the game
score is 0.2848 / 45 = 0.0063 (before averaging over games). The manuscript uses the game score,
computed by g_ceiling.py, not the level score.

Public-set outputs: per game, N, S(1, r, N) and S(k, r, N) for k = 1, 2, 3 and r in
{1, 2, 5, 10, 30, 100, 150}; means over the 25 games, the 17 held-out and the 8 train games, with
tu93, dc22 and ls20 labelled source-informed. The measured points (E2) are overlaid later from
scorecard counts (card_levels), not from level_log, which undercounts.

---

## 6. E9 and E10: goal identification

E9. Goal-oracle intervention (tu93, dc22, ls20 only; these are source-informed, so the true goal
is known from their source, read on 24 September 2026). Supply g_nav.py with the true goal of each
level at level start; nothing else changes (same explorer, same step learning, same counters, same
seeds 1000-1009, 20,000 actions). Arms: hash_state, nav, nav+oracle.
- What must be true: each game's true goal can be written in the planner's goal language (a target
  place or colour). Where it cannot (for example a goal that is a panel state rather than a place),
  the game is reported as "goal not expressible in the instrument", which is itself a result.
- Positive control: tu93, where nav already confirms its goal on all 4 seeds. nav+oracle below nav
  on tu93 means the oracle plumbing is broken; nothing from E9 is used until that is fixed.
- What it can show: for this instrument on these three games, how much of the gap to the human
  count closes when the goal is given and nothing else changes. What it cannot show: anything about
  held-out games, or about other agents.

E10. Goal-identification cost, a narrow formal definition, measured on the 25 games.
- Setting. A play is a sequence of frames x_0, x_1, ... and actions; the only goal-relevant
  feedback is the level-completion signal e_t in {0, 1}.
- Hypothesis class G. A finite, fixed-in-advance set of predicates on frames (for example: "a
  cell of colour c is covered by the controlled object", "no cell of colour c remains", "the
  controlled object is at the place it was when the previous level ended"). G is written down and
  hashed before it is evaluated on any held-out trace.
- Consistency. g in G is consistent with a history up to t if g(x_i) = e_i for every i <= t.
- Goal-identification cost of a trace: the first t at which the consistent set is non-empty and
  all its members recommend the same next target, or "not identified" within the trace.
- Restricted ambiguity result (to be proved in the manuscript): if two hypotheses agree on every
  frame an action policy visits before step T, no learner that observes only frames and e_t can
  distinguish them before T under that policy. The proof is one step (the two histories are
  identical); its use is that it turns counter readings into a measurable quantity per game.
- Measured on existing and E2 traces (frames must be logged, or the estimator runs on-line in the
  harness). What must be true: G must contain each game's true goal for the cost to be finite;
  where it does not (known on tu93/dc22/ls20 only), that is reported.
- Allowed wording after E10: the measured cost per game for this G; nothing about goals outside G.

---

## 7. Remaining experiments

E2. hash_state at 10 seeds (1000-1009), all 25 games, 20,000 actions, scorecard per-level counts.
    Recomputes M1-M4 of Section 3.2 for our agent before any external agent is scored.
E3. Budget curve: 3,000, 20,000, 50,000, 100,000 actions, hash_state, 4 seeds, 25 games.
E6. v2 census, all 25 games, 10 seeds, hash_state and nav. Train games in the same table, tu93 as
    a source-informed positive control; dc22 and ls20 labelled source-informed. The census
    categories and counters are frozen (code hash recorded) before the run.
E7. 14B CPU LLM cost. Optional; half a page at most.
E8. Reproduction package: anonymised repository; one script regenerates every table and figure
    from runs/; engine versions; SHA-256 of every JSON; the scorecard.py hash.
Optional, only after E1, E9, E10: a second CPU benchmark (GVGAI learning track) to test whether the
census categories transfer without rewriting.

Order: E5 and E4 (no games); E1 admissibility checks in parallel (the adapters are the work); E2;
E6; E9; E10; E3; E7.

---

## 8. Statistics

- Games are the statistical unit. Seeds are nested within games. A mean over games is reported
  with a hierarchical bootstrap: resample games with replacement, then seeds within each resampled
  game. An interval over seeds only is labelled "seed variation for these games" and is never used
  to support a statement about games.
- 17 or 25 authored games are a descriptive set, not a random sample. Intervals describe
  variation within this set.
- Minimum 4 seeds for any number in a document; 10 seeds for the final tables. No single-seed
  number is reported as a result (the 20x1 matrix is exploratory and labelled 1 seed wherever it
  appears).
- Efficiency ratios come from scorecard counts, never from level_log (level_log undercounts: probe,
  scan and reset presses are outside it; ls20 seed 1003: 41 vs 25, ft09 seed 1003: 212 vs 90).
- Every table has a per-game version in the supplement. Source-informed games (tu93, dc22, ls20)
  are marked in every table and figure and kept apart from held-out evidence.

---

## 9. Manuscript: 10 pages plus supplement

1. Introduction (0.75 p): the benchmark, the questions, the contributions, what is not claimed.
2. Related work (0.75 p): organiser publications; Rudakov et al.; GVGAI generalisation (Balla et
   al.) and screen-capture learning (Kunanusont et al.); best-agent identification (Stephenson et
   al.); leaderboard overfitting (Blum & Hardt; Roelofs et al.); assumption monitoring and trace
   diagnosis (Introspective Environment Modeling; AgentRx); game-agent benchmarks for LLMs
   (BALROG); Milestone-1 winners' published descriptions, dated.
3. The scoring rule and its ceiling (1.25 p): from scorecard.py; S(k, r, N); validation; the
   public-set numbers.
4. Agents and harness (1 p): hash_state and G-NAV as instruments; E1 agents; action accounting;
   determinism.
5. Measured decomposition (1 p): E2, E3.
6. Selection transfer (1 p): fixed split, then E5.
7. Goal identification (2 p): census (game-dependent rows apart from planner-dependent rows);
   E9; E10; tu93 as source-informed positive control; the ar25 anomaly.
8. External agents (1 p): E1 by the pre-registered rule.
9. Threats to validity (0.75 p) and CPU LLM cost (0.25 p).
10. Conclusion (0.25 p).
Supplement: per-game tables, full census evidence, killed mechanisms with measured reasons,
source-reading disclosure, E1 admissibility records.

Venue: ToG if E1 has at least two admissible independent agents and E9 or E10 delivers. Otherwise
IEEE CoG or a workshop, decided on 9 October 2026 (CoG 2026 page and fee rules to be checked on the
call page, not copied from older editions).

---

## 10. Disclosures (in the manuscript, in these words or plainer)

- The source files of tu93, dc22 and ls20 were read on 24 September 2026 while debugging the
  planner. No held-out game's source was opened. These three games are source-informed controls
  and are not evidence for a source-blind census. Reading public source was not against any rule.
- The held-out split was fixed before the first mechanism was measured and never changed. The
  code hash of the census and counters is recorded before each held-out run.
- The ar25 anomaly: G-NAV won ar25 level 1 on 4 of 4 seeds; hash_state did not win it. The
  hash_state seed count differs between documents (0/8 in docs/HANDOFF_GNAV.md, 0/12 in
  CLAUDE.md); the correct count is to be computed from runs/ by a script before it is written. The
  cause is unknown; it is reported as unexplained and nothing is built on it.
- Engine and scorer versions (arc-agi 0.9.8, arcengine 0.9.3, scorecard.py SHA-256), game file
  versions, dates. Leaderboard state is quoted only with a date and a source.
- Use of an AI assistant in coding and drafting, per IEEE policy, in the final non-anonymous
  version.

---

## 11. Audit corrections and where each is applied

| Audit item | Handled in |
|---|---|
| Title overclaims; Rudakov et al. is a counterexample to a general plateau | Title; C4; 3.5 |
| "Barrier is goal inference" not supported by counters | C3; E9; E10 |
| RQ1 from scorecard.py, not the report's n = 5 equations; validate incl. cap | C1; Section 5 |
| E1 no-go; two independent licensed runnable agents needed | Section 3 |
| E1 thresholds fixed before external runs; disclose their origin | 3 (preamble), 3.3, 3.4 |
| Organiser templates are a baseline, not independent evidence | 3.4, 3.5 |
| Unverified 0.26-0.27 agent | RQ4 (dropped until traceable) |
| E5 mixes 20x1 and 6x4 | Section 4 (6x4 primary, 20x1 exploratory; budgets differ) |
| Selection protocol fixed before analysis | Section 4 |
| Public 25 are a demonstration subset; no private-set sentences | Section 0; C-rules |
| 17 games not a random sample; seeds nested in games | Section 8 |
| "Every leaderboard leader runs a GPU-served vision model" | C5 (forbidden) |
| 12 pages vs 10-page fee threshold | Section 9 (10 pages + supplement) |
| Source-read games labelled; not passed off as blind | Sections 8, 10 |
| Code hash / protocol lock | E6; Section 10 |
| Missing citations | Section 9 item 2 |
| ar25 anomaly kept | Section 10 |
| Raw run records, hashes | E8 |
| Leaderboard dated | Section 10 |
| Formal goal-identification cost | E10 |
| Second benchmark | Section 7 (optional, after E1/E9/E10) |
