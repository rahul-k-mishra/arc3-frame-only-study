# E9 protocol: the goal-oracle intervention

Written 26 September 2026: protocol only, before any code or run. Registered here; once any E9
output exists, no threshold or prediction below may change. The plan entry is docs/TOG_PLAN_v2.md
Section 6 (E9).

Question: for the G-NAV planner (scripts/g_nav.py, a hook on the hash_state explorer), on tu93,
dc22 and ls20, does supplying the true goal, with everything else unchanged, change what the
planner achieves?

Scope: only tu93, dc22 and ls20, the three train games whose source files were read on 24 September
2026 while debugging g_nav.py (CLAUDE.md rule 1). **No held-out game is ever used in E9**, and no
held-out source is ever opened.

## 1. How the true goal is expressed

G-NAV's goal language, from scripts/g_nav.py, is **a place for the controlled object to reach**:
- `_replan` step 1 (lines 253-264) targets the nearest position `p` whose footprint shows a goal
  colour (`_goal_cells`, lines 247-248);
- goals are learned in `_record_goal` (lines 753-784) as the colours stepped on at a level end.

The oracle therefore expresses each level's true win condition as **a set of target cells in that
level's own frame**: the cells the object must occupy for the level to end. It gives no colour, no
action sequence and no sub-goal.

What the repository already records about the three goals:
- **tu93:** the level ends when the avatar reaches the exit, a coloured tile. docs/HANDOFF_GNAV.md
  line 50: "tu93 is the one game in 25 where it is" (the goal is "reach a colour"). G-NAV confirmed
  that goal on all 4 seeds (HANDOFF line 18: `goal_confirmed on all 4 seeds`).
- **dc22 and ls20:** **not recorded.** The repository notes only mechanics: ls20 has a key panel
  and a 12-cell "pusher" (HANDOFF lines 36-37); dc22 has none noted. G-NAV never won a dc22 level
  in any recorded run.

Required before any code (gate G1): the true win condition of every level of the three games is
written to `docs/E9_goals.md` from their source files. For each level it records:
- the source file and line numbers of the win condition, quoted;
- the condition in plain words;
- its expression as target cells in the level's initial frame (a list of (row, col)), **or
  "not expressible"** with the reason. "Not expressible" applies when the win condition is not
  "the object occupies these cells": for example it also requires a key, a panel state, a push,
  or several objects. A condition expressible only as a sequence of sub-goals counts as not
  expressible, because supplying a sequence would give more than the goal.

The author decides who reads the three sources for G1, and the date of that reading is recorded in
`docs/E9_goals.md`. The goal table's SHA-256 is recorded before the first E9 run. A level marked
"not expressible" is played by the oracle arm exactly as the planner arm plays it (Section 2), and
is reported as such. That a win condition cannot be written as a place is itself a result about the
instrument.

Disclosure, in every table and figure: **source-informed**. The goals come from reading the games'
source, and these are the games the planner was debugged on.

## 2. What the oracle replaces, and what it must not touch

The oracle arm is a new mode, `nav_oracle`, in scripts/g_nav_run.py. It uses the same `NavHook`
with one addition: at each level start (`on_level` → `_new_level`) it receives that level's
target cells from the goal table, or nothing if the level is not expressible.

It replaces **only the goal hypothesis and its confirmation path**:
- **`_replan` step 1 (lines 253-264):** instead of candidate positions showing a learned goal
  colour, the targets are positions whose footprint intersects the level's true target cells.
  Selection, path search (`_bfs`, `_path`) and one-step execution are unchanged. The attempt cap
  `goal_tries` does not limit the oracle target: the goal is known, so there is nothing to
  falsify. If the oracle target is unreachable in the current lattice, `_replan` falls through to
  step 2 (the frontier) exactly as now.
- **`_record_goal` (lines 753-784):** still runs and still updates its counters. In the oracle
  arm, `goal_hyps` is not used for targeting on levels with an oracle target.
- **The falsification path (lines 490-495, `goal_reached_no_end`, `goal_tried`):** for an oracle
  target, reaching it without the level ending increments a new counter,
  `oracle_reached_no_end`, and the target stays. **`oracle_reached_no_end` must be 0 on every
  expressible level.** Any other value means the goal table is wrong for that level (validity
  check V2, Section 4).

It must not touch, and the code review before the run checks each item:
- the movement model: key learning (`_learn_observe`, `_finish_learning`,
  `_hypothesise_missing`), step vectors `eff`, avatar finding and localisation;
- passability: `_passable`, walls, deadly colours, bump blocks and their expiry, death avoidance;
- exploration: the frontier order in `_replan` step 2, the `visited` set, BFS limits (`BFS_NODES`);
- the fallbacks: `_fallback` and its conditions (no avatar, frontier exhausted, too many
  mispredictions, the stall limit), waiting (`_wait_action`), the dynamic-seal check;
- the explorer underneath (scripts/g_agent.py, hash_state), the harness (scripts/g_nav_run.py
  apart from registering the new mode), the budget, the seeds, and the scorecard accounting.

Equivalence check (gate G2, before the run): with an empty goal table, `nav_oracle` must produce
action sequences and scorecard rows identical to `nav` on all three games for seeds 1000-1001 at
3,000 actions, by the method of scripts/g_nav_equiv.py. The code hash of g_nav.py and
g_nav_run.py is recorded after G2 passes; no code changes after that point.

Known confound, from docs/HANDOFF_GNAV.md (last OPEN item): the planner's presses change the
explorer's random path after a fallback, so two planner arms can differ on levels where neither
used its plan. Differences are therefore interpreted only on levels where the oracle arm actually
targeted its oracle cells (per-level counter `oracle_targets > 0`). Per-level fallback reasons are
reported for both planner arms.

## 3. Arms

All three arms: games tu93, dc22, ls20; seeds 1000-1009; 20,000 actions per run; arc-agi 0.9.8,
arcengine 0.9.3, offline; the same environment files; per-level counts from the scorecard;
g_nav_run.py.

| arm | mode | what it is |
|---|---|---|
| F (floor) | `hash_state` | the plain explorer, no planner |
| N (planner) | `nav` | G-NAV as it is |
| O (oracle) | `nav_oracle` | G-NAV plus the true goal (Section 2) |

Arm F is also in runs/navrun_e2_hash_25x10.json (E2). It is re-run in the same E9 command, and the
E9 rows must equal E2's rows for these three games and seeds (determinism check V1). Any
difference stops E9.

Command shape (the exact command is written when G1 and G2 pass):
`g_nav_run.py --games tu93,dc22,ls20 --modes hash_state,nav,nav_oracle --seeds 10 --budget 20000 --tag e9_oracle_3x10`

## 4. Measures and validity checks

Per game, per arm, per level i, over seeds 1000-1009:
- **levels completed:** the seed-mean of levels completed per run;
- **level won:** the number of seeds (of 10) in which level i was won;
- **scorecard actions:** for each seed that won level i, `card_levels[i]` against the human count
  `card_baseline[i]`, as the ratio agent/human; reported as the median and range over those seeds;
- **level score:** `card_scores[i]`, the scorecard's `min(115, 100 (human/agent)^2)`, seed-mean
  with unwon levels counted 0;
- **game score:** the recorded scorecard score, seed-mean.

Games are the unit. With three games there is no pooled estimate and no interval over games: each
game is reported on its own, and seed variation within a game is labelled as such. Also reported:
per-level G-NAV counters for arms N and O (goal_targets, goal_confirmed, goal_reached_no_end,
oracle_targets, oracle_reached_no_end, fallback reason).

Validity checks (all must pass before any E9 number is reported):
- V1 arm F's rows equal E2's rows for these games and seeds;
- V2 `oracle_reached_no_end = 0` on every expressible level in every seed of arm O;
- V3 positive control on tu93: arm O's seed-mean levels completed is not below arm N's by 0.5 or
  more. tu93 is the game where N already confirms its goals; O falling below N there means the
  oracle plumbing is broken;
- V4 every run used its full 20,000 actions or won the game.

If V2 fails on a level, the goal table was wrong for that level. The correction is dated and
recorded in `docs/E9_goals.md` with its reason, all arms are run again, and both runs are
reported. If V3 fails, nothing from E9 is used until the cause is found.

## 5. Predictions, written now

Definitions, per game G (arms N and O, seeds 1000-1009):
- **dL** = O's seed-mean levels completed minus N's.
- **A shared level** is one won by both arms in at least 5 of 10 seeds. For a shared level,
  **rN** and **rO** are the median agent/human action ratios over the seeds that won it.
- **A newly won level** is one O wins in at least 5 seeds and N in at most 4.

Only levels expressible in the goal table, and on which arm O used its oracle target
(`oracle_targets > 0`), count toward these definitions.

Per game, the goal is:
- **BINDING** if any of: dL >= 1.0; at least one newly won level; or, on at least one shared
  level, rO <= rN / 2 (the oracle at least halves the actions per level);
- **NOT BINDING** if all of: |dL| < 0.5; no newly won level; and on every shared level
  rO > 0.75 rN (less than a 25% reduction);
- **MIXED** otherwise;
- **NOT TESTABLE** if the game has no expressible level on which arm O used its oracle target.

Across the three games:
- **Goal information is the binding constraint for this instrument on these games** if at least 2
  games are BINDING and none is NOT BINDING.
- **It is not** if at least 2 games are testable and every testable game is NOT BINDING.
- **Inconclusive** otherwise, including when fewer than 2 games are testable.

What is expected, stated so that a surprise is visible:
- **tu93:** G-NAV already reaches its goal from level 2 on, so the oracle's room is mainly level 1
  (N took 81 actions against a human 19 in the v1 runs, docs/HANDOFF_GNAV.md line 17, and 71 in
  the v2 train-quick census, docs/census_v2.md) and any level whose goal differs from
  level 1's.
- **dc22:** no G-NAV run has won level 1, so dc22 separates "the goal was unknown" from "the goal
  was known but unreachable by this planner".
- **ls20:** its mechanics (key panel, pusher) suggest the win condition may not be a place; if so,
  ls20 is NOT TESTABLE, and that is reported as a finding about the goal language, not as missing
  data.

## 6. What the paper may and may not conclude

Constraints that hold in every outcome:
- three games, all source-informed (the goal table and the planner's debugging both used their
  source);
- all three are train games, on which the planner was developed;
- one planner (G-NAV) over one explorer (hash_state);
- seeds are nested in games, and three games support no population statement.

The paper never says "the barrier is goal inference" in general, never extends E9 to the held-out
games, to other agents, to "frame-only agents", or to ARC-AGI-3, and always names the three games
and the instrument.

- **BINDING (goal information is the binding constraint):**
  - *May say:* "For our planner on three train games whose source we read (tu93, dc22, ls20),
    supplying the true goal with everything else unchanged [raised levels completed by x / cut the
    actions per level by a factor y / won level(s) z]; for this instrument on these games, goal
    information was the binding constraint." It may then connect this, as consistent and not as
    proof, to the held-out census, where no goal was ever confirmed.
  - *May not say:* that goal identification is the barrier on the held-out games or for other
    agents.
- **NOT BINDING:**
  - *Must say:* "Supplying the true goal did not change what our planner achieved on these games;
    for this instrument, its limit lies elsewhere." Name the evidence from the counters: movement
    model, passability, exploration or fallbacks, per level.
  - *Must also:* withdraw the goal-identification reading of the census as more than a
    description. The census counters stay reported, but "goal identification is the dominant
    observed failure mode" may be kept only with this result stated next to it.
- **INCONCLUSIVE or MIXED:**
  - *Report:* the per-game results and the reason (which games were not testable, which were
    mixed).
  - *May not:* support any causal wording. The census stays descriptive, and the allowed sentence
    remains "goal identification is the dominant observed failure mode for this instrument on this
    public subset".
- **NOT TESTABLE on a game:** reported as a limit of the planner's goal language (the win condition
  is not "reach these cells"), with the quoted win condition from `docs/E9_goals.md`.

## 7. Gates before any run

- G1: `docs/E9_goals.md` written from the three sources (Section 1), with its SHA-256 recorded.
- G2: `nav_oracle` implemented and equivalence with `nav` shown on an empty goal table (Section 2),
  with the code hashes recorded.
- G3: the exact E9 command and output file names written into this document.

No E9 game is run before G1-G3 are committed.
