# E1 result: the Rudakov et al. agent is INCONCLUSIVE

Written 26 September 2026 from runs/e1_decision.json (created 2026-09-26 07:06:39 by
scripts/e1_decide.py). The protocol was docs/E1_phase2_protocol.md and the rule
docs/TOG_PLAN_v2.md Section 3; both were fixed before any phase-2 result was read. No threshold
has been changed since.

Inputs (SHA-256 from the decision file):
- Agent: runs/e1_rudakov_lenovo_25x10_20k.json (db836da4...), mode `rudakov`, 25 games x
  seeds 1000-1009 x 20,000 actions, 250 rows. No error rows, no time-truncated runs. Every level
  win was followed by the agent's graph reset, so the levels_completed -> score mapping held in
  every run.
- Reference: runs/navrun_e2_hash_25x10.json (1dd3293e...), our hash_state explorer, E2: the same
  games, seeds and budget.

## 1. Decision

**INCONCLUSIVE, decided by (ii): M2 / M1 = 0.7082 / 0.1750 = 4.05, against the registered
threshold M2 / M1 > 5.** Conditions (i) and (iii) hold. No BREAKS condition holds.

| condition | value | holds |
|---|---|---|
| (i) M1 < 0.5 | M1 = 0.1750 | yes |
| (ii) M2 / M1 > 5 | M2 / M1 = 0.7082 / 0.1750 = 4.05 | **no** |
| (iii) M3 = 0 | M3 = 0 | yes |
| (iv) M1 >= 1.0 (three times our 0.3329, rounded up) | M1 = 0.1750 | no |
| (v) level 3 or later won on at least 2 held-out games, each in at least half of that agent's seeds | games with level >= 3 in >= half (5) of the seeds: none | no |
| (vi) M4 at least twice our E2 value of M4 | M4 = 3.30 vs 2 x E2 M4 = 2 x 10.50 = 21.00 | no |

## 2. Measures (17 held-out games, 10 seeds; games the unit, seeds nested)

| measure | Rudakov et al. agent | 95% interval | our hash_state (E2) | 95% interval |
|---|---|---|---|---|
| M1 recorded | 0.1750 | [0.0018, 0.5441] | 0.3274 | [0.0143, 0.7323] |
| M2 AT HUMAN | 0.7082 | [0.2110, 1.3655] | 3.0602 | [1.2932, 5.2242] |
| M2 / M1 | 4.05 | [2.03, 211.71] | 9.35 | [4.09, 154.89] |
| M3 lv3+ runs | 0 | [0, 0] | 0 | [0, 0] |
| M4 levels per seed | 3.30 | [1.00, 6.10] | 10.50 | [5.70, 15.80] |

The intervals are hierarchical bootstrap percentiles (resample games, then seeds within each
game; 10,000 draws). They describe variation within these 17 authored games, and they do not
enter the rule. The rule used the point values.

What the numbers show, without going beyond them:
- The agent scored less than our explorer (M1 0.1750 vs 0.3274) and completed less than a third
  of its levels (M4 3.30 vs 10.50 levels per seed, summed over the 17 games). It won no level 3
  (M3 = 0), as ours did not.
- (ii) failed narrowly, and the interval for M2 / M1 over games, [2.03, 211.71], contains 5. The
  ratio is set almost entirely by one game. On r11l the agent won level 1 in 19-54 actions in all
  10 seeds (seed-mean score 2.7613), before its error loop (Section 3.2) began. r11l contributes
  2.7613 / 17 = 0.1624 of M1 = 0.1750 (93%). A fast first-level win raises M1 relative to the
  AT HUMAN value, which pushes M2 / M1 down. This is a description of where the ratio comes from,
  not a reason to exclude r11l; the registered result stands as computed.
- The E2 reference itself changed slightly from the 4-seed values the plan quotes: M1 0.3274 at
  10 seeds (0.3329 at 4 seeds), M4 10.50 (11.2 at 4 seeds, which was untraced).

Per held-out game:

| game | agent score | agent levels | E2 score | E2 levels | their errors per run, median (min-max) | ACTION7 unavailable |
|---|---|---|---|---|---|---|
| ar25 | 0.0000 | 0.0 | 0.0001 | 0.7 | 18577 (18154-19536) | yes |
| bp35 | 0.1236 | 0.9 | 0.0001 | 1.0 | 2 (0-19051) | yes |
| cd82 | 0.0000 | 0.0 | 0.1257 | 2.0 | 19562 (19000-19649) |  |
| cn04 | 0.0000 | 0.2 | 0.0000 | 0.2 | 0 (0-14130) |  |
| g50t | 0.0000 | 0.0 | 0.0000 | 0.0 | 19137 (174-19169) |  |
| ka59 | 0.0000 | 0.0 | 0.0000 | 0.7 | 18189 (16674-18820) |  |
| r11l | 2.7613 | 1.0 | 1.3141 | 1.3 | 19605 (19288-19645) |  |
| re86 | 0.0000 | 0.0 | 0.0000 | 0.1 | 0 (0-0) |  |
| s5i5 | 0.0001 | 0.1 | 0.0009 | 0.9 | 19314 (15924-19505) |  |
| sb26 | 0.0000 | 0.1 | 0.0000 | 0.0 | 0 (0-2) | yes |
| sc25 | 0.0000 | 0.0 | 0.0000 | 0.0 | 19321 (14306-19489) |  |
| sk48 | 0.0004 | 0.5 | 0.0001 | 0.3 | 342 (6-17177) | yes |
| sp80 | 0.0564 | 0.2 | 1.7517 | 1.8 | 19079 (7425-19264) |  |
| su15 | 0.0000 | 0.0 | 0.0000 | 0.0 | 19281 (19190-19382) | yes |
| tn36 | 0.0000 | 0.0 | 2.3404 | 1.0 | 16348 (15282-18158) |  |
| tr87 | 0.0329 | 0.3 | 0.0329 | 0.5 | 0 (0-0) |  |
| wa30 | 0.0000 | 0.0 | 0.0000 | 0.0 | 17074 (0-19264) |  |

Train games (beside, not in the rule; tu93, dc22 and ls20 source-informed): agent M1 0.2276,
M4 7.10; E2 M1 0.1901, M4 11.10, with 8 lv3+ runs, all on tu93.

## 3. Three confounds, with their evidence

None of these changes the registered label, and none is used to reinterpret it. Each limits what
the measurement says about the agent as its authors built it.

### 3.1 ACTION7 is absent from their action set

Their `GameAction` enum stops at ACTION6, and their `choose_action` maps keyboard actions 1-5
only (docs/E1_rudakov_feasibility.md Section 5). The arc-agi 0.9.8 engine offers ACTION7 on some
games, and their agent never presses it. From our census (runs/census_v2.json, G-NAV's level-1
learn phase), key 7 was:
- **pressed** on five held-out games: ar25, bp35, sb26, sk48, su15;
- **accepted as a movement key** on two of them: ar25 (step [3, 3], the same as keys 2 and 3)
  and bp35 (step [-6, 0], the only reliable leftward move).

On su15, key 7 is the only keyboard action, so their agent played su15 by clicks alone. On the
train game lf52 key 7 was pressed but not accepted.

(A correction to the request that produced this document: it said key 7 was *accepted* on five
held-out games; the census says *pressed* on five and *accepted* on two.)

### 3.2 Their choose_action raises on most actions in most runs

Their `main()` catches any exception in `choose_action`, re-initialises its graph, and re-sends
the previous action. Each such exception is counted per run in `diag.their_prints.Error`
(runs/e1_rudakov_lenovo_25x10_20k.json).

The counts out of 20,000 actions:
- **All 250 runs:** median 17,626. At least 19,000 in 96 runs (38%), at least 18,000 in 120
  (48%), none in 64.
- **The 170 held-out runs:** median 17,342. At least 19,000 in 60, at least 18,000 in 80, at
  least 10,000 in 111 (65%), none in 37.

(A correction to the request: it said "about 19,000 of 20,000 actions in most runs". That holds
for 38% of all runs; "at least 10,000 in 65% of held-out runs, median 17,342" is what the file
shows.)

The counts are strongly game-dependent:
- **Median at least 10,000:** 11 of the 17 held-out games (ar25, cd82, g50t, ka59, r11l, s5i5,
  sc25, sp80, su15, tn36, wa30).
- **No errors in any seed:** re86, tr87, ft09, ls20.

Once the loop starts, the agent repeats one action for the rest of the run. In 100 of the 170
held-out runs a single action accounts for at least 90% of the 20,000 steps. For example, in
seed 1000 ar25 issued ACTION5 18,622 times, and cd82 issued ACTION4 19,666 times.

The first error on tu93 is `ValueError: Old value 1.0 is not equal to new value -1.0`
(heuristic_agent.py line 298): a (masked frame, action) pair it had already recorded produced a
different outcome. The recovery then fails with "Edge result must be untested before recording a
test" on almost every later step. This is their code, not the adapter: on tu93 at 1,000 actions
their own REST loop against the local server raised 686 times and the adapter 687 times, with
identical actions (runs/e1_rudakov_fidelity_ft09-tu93_1000.json; the one extra is the adapter's
unused final call). The vc33/lp85 fidelity check (runs/e1_rudakov_fidelity_vc33-lp85_300.json)
reached no error in 300 actions in either arm, so it adds no evidence either way.

Why the error appears so often on the current games has not been established. It may be
engine-version non-determinism, partial observation (their README names both as problems for the
method), or something else. Their published runs were on different games through a different
API, and whether the same loop occurred there is not known.

Consequence: over most of most runs, the measured agent was their error-recovery loop, not their
graph explorer. The result measures their released code, unchanged, on the current games; it is
not a measurement of the method as it behaved in their evaluation.

### 3.3 Preview vs 2026 game set and API

Their agent was built and evaluated for the 2025 ARC-AGI-3 Preview:
- **Games:** six public preview games and 25 private levels.
- **API:** a REST API whose frame field `score` counts levels completed, and whose action set
  ends at ACTION6.

This measurement used a different setting:
- **Games:** the 2026 public demonstration set of 25 games.
- **Engine:** arc-agi 0.9.8, which reports `levels_completed` (mapped to their `score` by the
  adapter) and offers ACTION7.
- **Seeds:** fixed, where their runs were wall-clock-seeded.
- **Budget:** 20,000 actions, where their configuration had no action cap and a 7.9 h time limit;
  the published-configuration arm was skipped (protocol Section 3).

The game ids ls20, ft09 and vc33 named in their README also appear in the current set (all three
are train games here). Whether the current versions of those games equal the preview versions was
not checked.

## 4. What Section 3.4 permits the paper to say

Section 3.4 (verbatim, relevant items):

> - Fewer than two admissible independent agents by 9 October 2026: every family statement is
>   removed; the paper speaks of the agents we measured, by name. The venue decision in Section 9
>   is re-taken.

and, from 3.3 and the protocol: an INCONCLUSIVE agent does not count toward the two REPRODUCES
agents, and no family statement rests on it.

There is one admissible independent agent; its result is INCONCLUSIVE, and no second agent has
been run. So, unless a second admissible independent agent is found and measured before
9 October 2026:

- **No family statement.** The paper does not say that the pattern holds for "frame-only agents",
  for "independent agents", or for "the agents we measured" as a group. RQ4 is not established.
- **The paper may say**, naming the agent: "The released code of Rudakov et al.'s graph-exploration
  agent, run unchanged apart from input/output on the 25-game 2026 public set (10 seeds, 20,000
  actions), scored M1 = 0.175 on the 17 held-out games, completed 3.3 levels per seed across them
  and no level 3; our pre-registered criterion for reproducing our explorer's pattern was not met,
  because AT HUMAN / recorded was 4.05 against a threshold of 5." In the same place it must say
  that the agent's own error handling was active on most actions in most runs, that ACTION7 was
  unavailable to it, and that it was built for the preview games and API.
- **The paper may not say** that the agent reproduces or breaks our pattern, that it
  "plateaus", that it performs worse "as a method", or anything about the private set.

**Their published preview result is not contradicted by this measurement.** They report results
on different games (the 2025 preview), through a different API, under their own configuration
(no action cap, 7.9 h per game, wall-clock seeds). Our run was on the 2026 public games, with a
20,000-action budget and fixed seeds, and their released code spent most of most runs in its
error-recovery loop. Their numbers are cited as reported, and no sentence of the paper sets our
number against theirs as a test of it.
