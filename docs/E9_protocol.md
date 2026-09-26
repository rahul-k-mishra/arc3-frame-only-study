# E9 protocol: the goal-oracle intervention

Written 26 September 2026: protocol only, before any code or run. Registered here; once any E9
output exists, no threshold or prediction below may change. The plan entry is docs/TOG_PLAN_v2.md
Section 6 (E9).

Question: for the G-NAV planner (scripts/g_nav.py, a hook on the hash_state explorer), on tu93,
dc22 and ls20, does supplying the true goal, with everything else unchanged, change what the
planner achieves?

Amended 26 September 2026, before any E9 code, by the author's decision after gate G1
(docs/E9_goals.md). Changed:
- the goal is handed in G-NAV's own language, a colour, not as target cells (Sections 1-2);
- ls20 is NOT TESTABLE, reported as a finding, and the verdict rests on tu93 and dc22 (Section 5);
- check V2 is rewritten for the colour oracle, and V5 (colour ambiguity) is added (Section 4);
- the coordinate arm is optional, secondary and outside the verdict (Section 3).
No threshold in Section 5 changed. The version before this amendment is commit 3d2bde7.

Scope: only tu93, dc22 and ls20, the three train games whose source files were read on 24 September
2026 while debugging g_nav.py (CLAUDE.md rule 1). **No held-out game is ever used in E9**, and no
held-out source is ever opened.

## 1. How the true goal is expressed

The oracle expresses each level's true win condition in G-NAV's own hypothesis language: a goal
colour. G-NAV names a place only by colour:
- `goal_hyps` is a list of colours;
- a position qualifies when its footprint shows a goal colour (`_goal_cells`, scripts/g_nav.py
  lines 247-248);
- `_replan` step 1 (lines 253-264) targets the nearest such position.

So the oracle hands the planner, once per level at level start, **the set of colours of the
target's visible cells**. They are read from the level's first frame at the position of the sprite
that the game's level-end predicate names (docs/E9_goals.md). The level's background colour and
the avatar's colours are removed, exactly as G-NAV's own `_record_goal` removes them (lines
762-765 and 771). This set replaces `goal_hyps` for that level and lifts the `goal_tries` cap; nothing else
changes.

This keeps the instrument the same. A result is about identifying the goal in the planner's own
terms, not about being handed a coordinate the planner could never form.

The goal table (docs/E9_goals.md) states each target by the rule the game checks ("the position of
the sprite tagged X"), never by recorded coordinates, colours or layouts. The only read of the
running game is the oracle's, at each level start: it finds that sprite, its position and its
visible cells, for tu93 and dc22 only.

A level whose predicate is not "the controlled object reaches a place" (object state, several
targets, or a sequence) is not expressible. For such a level:
- the oracle hands nothing, and the oracle arm plays it exactly as the planner arm;
- the level is reported as **NOT TESTABLE, as a finding**: the planner's goal language cannot
  represent it, and the predicate is quoted from docs/E9_goals.md.

Status after G1 (docs/E9_goals.md, commit 8f8047f, SHA-256
e87c1778c73752549a2defc9f5bfbddca81a7c96d7b5780bcc370b71576063bd):
- **tu93: testable.** The level ends when every arrow-controlled sprite stands at an exit
  sprite's position.
- **dc22: testable.** The level ends when the controlled sprite stands at the target sprite's
  position.
- **ls20: NOT TESTABLE at every level.** The level ends when every target has been reached with
  matching shape, colour and rotation; this is not expressible as a place.

Disclosure, in every table and figure: **source-informed**. The level-end rules come from reading
the games' source, and these are the games the planner was debugged on.

## 2. What the oracle replaces, and what it must not touch

The oracle arm is a new mode, `nav_oracle`, in scripts/g_nav_run.py. It uses the same `NavHook`
with one addition: at each level start (`on_level` → `_new_level`) it receives that level's
oracle colours (Section 1), or nothing if the level is not expressible.

It replaces **only the goal hypothesis and its confirmation path**:
- **`goal_hyps` for the level:** replaced by the oracle colours at level start. `_replan` step 1
  (lines 253-264) then runs unchanged: nearest position whose footprint shows an oracle colour.
  Selection, `_goal_cells`, path search (`_bfs`, `_path`) and one-step execution are unchanged. If
  no position showing an oracle colour is reachable, `_replan` falls through to step 2 (the
  frontier) exactly as now.
- **The attempt cap `goal_tries`:** lifted for oracle colours. The goal colour is known, so it is
  never written off.
- **The per-position path (lines 490-495, `goal_tried`, `goal_reached_no_end`):** unchanged. A
  position showing an oracle colour that is reached without the level ending is added to
  `goal_tried`, as now, so the planner moves on to another position of that colour. This can
  happen legitimately, since the colour can cover more cells than the exact place the game checks.
  In arm O these arrivals are also counted as `oracle_reached_no_end`, reported beside V5.
- **`_record_goal` (lines 753-784):** still runs and still updates its counters, but it does not
  change the oracle colours for the level. At each level end, a new counter `oracle_confirmed`
  records whether the position the level ended on showed an oracle colour (check V2).

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
targeted an oracle colour (per-level counter `oracle_targets > 0`). Per-level fallback reasons are
reported for both planner arms.

## 3. Arms

All three arms: games tu93, dc22, ls20; seeds 1000-1009; 20,000 actions per run; arc-agi 0.9.8,
arcengine 0.9.3, offline; the same environment files; per-level counts from the scorecard;
g_nav_run.py.

| arm | mode | what it is |
|---|---|---|
| F (floor) | `hash_state` | the plain explorer, no planner |
| N (planner) | `nav` | G-NAV as it is |
| O (oracle) | `nav_oracle` | G-NAV plus the true goal colour (Sections 1-2) |
| P (optional) | `nav_oracle_place` | secondary; see below; **not in the verdict** |

Arm F is also in runs/navrun_e2_hash_25x10.json (E2). It is re-run in the same E9 command, and the
E9 rows must equal E2's rows for these three games and seeds (determinism check V1). Any
difference stops E9.

ls20 is run in all arms although it is NOT TESTABLE. Arm O plays it exactly as arm N, so its
rows must equal arm N's rows for ls20 (a free equivalence check, V6).

**Optional secondary arm P, the coordinate arm (`nav_oracle_place`).** Run only if arm O is
completed and time allows.
- **What it hands:** once per level, a single lattice position
  p* = target (x, y) + (G-NAV anchor − controlled-sprite origin). The offset is measured from game
  state at level start: G-NAV's position is the top-left of the avatar's visible cells (`_anchor`,
  line 54), while the game's check compares sprite origins. Step 1 targets exactly p*.
- **How it is reported:** only as "the value of knowing the exact place", never as goal
  identification. It does not enter the Section 5 verdict.
- **Rotation caveat, tu93:** the game rotates the controlled sprite when it moves, and rotation
  can change the offset between the sprite's origin and its top-left visible cell. p* is then
  wrong on rotated steps. For arm P on tu93, `oracle_reached_no_end` at p* is reported per level
  with this caveat, and a non-zero count on tu93 is read first as an offset error, not as evidence
  about the goal.

The exact commands are in Section 7.

When the colours are read (decision D3, Section 8): at the level's first planner step, which on
level 1 may follow the explorer's opening actions. Avatar colours are removed when the colours
are used, not when they are read.

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

Validity checks (V1-V4 and V6 must pass before any E9 number is reported; V5 is reported, not
passed or failed):
- **V1:** arm F's rows equal E2's rows for these games and seeds.
- **V2, the oracle colour is where the level ends** (revised by decision D1, Section 8): for every
  win by arm O on a testable level where the oracle handed colours, there are two outcomes that
  matter:
  - **The ending position showed no oracle colour** (`oracle_confirmed` false). This FAILS V2 and
    blocks the report: the colour set is wrong for that level.
  - **The planner could not read the ending position** (`oracle_confirmed` missing or None). This
    covers a level won during the explorer's click scan, won by any click action (the planner
    observes only its keyboard steps), or won when the planner had no position after a fallback.
    It is **not** a V2 failure. It is reported as "ending not seen", counted per game for arm O
    (the only arm with an oracle), and excluded from V2's denominator. The exclusion is stated
    beside every result it affects.
- **V3, positive control on tu93:** arm O's seed-mean levels completed is not below arm N's by 0.5
  or more. tu93 is the game where N already confirms its goals, so O falling below N there means
  the oracle plumbing is broken.
- **V4:** every run used its full 20,000 actions or won the game.
- **V5, colour ambiguity:** for each testable level, from the level's first frame alone, with no
  source read, count the cells showing any oracle colour outside the target sprite's visible
  cells, and the number of connected components they form. Both counts are reported beside that
  level's result in every table. A non-zero count means the goal colour also marks other places,
  and the level's arm-O result is read with that in view: `oracle_reached_no_end` is expected to
  be non-zero there. V5 excludes no level.
- **V6:** on ls20 (NOT TESTABLE), arm O's rows equal arm N's rows.

If V2 fails on a level:
- the colour-set rule was wrong for that level;
- the correction is dated and recorded in `docs/E9_goals.md` with its reason;
- all arms are run again, and both runs are reported.

If V3 or V6 fails, nothing from E9 is used until the cause is found.

(The earlier V2, "`oracle_reached_no_end` = 0", was written for exact target cells. Under the
colour oracle, arrivals at a colour cell that is not the exact place are legitimate, so V2 now
tests the colour at the place where the level actually ends.)

## 5. Predictions, written now

Definitions, per game G (arms N and O, seeds 1000-1009):
- **dL** = O's seed-mean levels completed minus N's.
- **A shared level** is one won by both arms in at least 5 of 10 seeds. For a shared level,
  **rN** and **rO** are the median agent/human action ratios over the seeds that won it.
- **A newly won level** is one O wins in at least 5 seeds and N in at most 4.

Only levels expressible in the goal table, and on which arm O used an oracle colour
(`oracle_targets > 0`), count toward these definitions. Only arm O enters them; arm P never does.
**Eligible level** (decision D2, Section 8): a level counts as one on which arm O used an oracle
colour if `oracle_targets > 0` on that level in at least one seed of arm O.

Per game, the goal is:
- **BINDING** if any of: dL >= 1.0; at least one newly won level; or, on at least one shared
  level, rO <= rN / 2 (the oracle at least halves the actions per level);
- **NOT BINDING** if all of: |dL| < 0.5; no newly won level; and on every shared level
  rO > 0.75 rN (less than a 25% reduction);
- **MIXED** otherwise;
- **NOT TESTABLE** if the game has no expressible level on which arm O used its oracle target.

Across games. ls20 is NOT TESTABLE (docs/E9_goals.md), so the verdict rests on tu93 and dc22
only, both source-informed:
- **Goal identification is the binding constraint for this instrument on these two games** if
  both are BINDING.
- **It is not** if both are NOT BINDING.
- **Inconclusive** otherwise, including if either game turns out NOT TESTABLE in practice (no
  level on which arm O used an oracle colour).

This is the same rule as before applied to two testable games. **Two games cannot support a
general claim** about the planner, about goal identification, or about any other game; Section 6
limits the wording accordingly.

What is expected, stated so that a surprise is visible:
- **tu93:** G-NAV already reaches its goal from level 2 on, so the oracle's room is mainly level 1
  (N took 81 actions against a human 19 in the v1 runs, docs/HANDOFF_GNAV.md line 17, and 71 in
  the v2 train-quick census, docs/census_v2.md) and any level whose goal differs from
  level 1's.
- **dc22:** no G-NAV run has won level 1, so dc22 separates "the goal was unknown" from "the goal
  was known but unreachable by this planner".
- **ls20:** NOT TESTABLE (docs/E9_goals.md). Its predicate, every target reached with matching
  shape, colour and rotation, is not expressible as a place. This is reported as a finding about
  the planner's goal language, not as missing data.

## 6. What the paper may and may not conclude

Constraints that hold in every outcome:
- the verdict rests on two games, tu93 and dc22; ls20 is reported as NOT TESTABLE;
- all three are source-informed (the level-end rules and the planner's debugging both used their
  source);
- all three are train games, on which the planner was developed;
- one planner (G-NAV) over one explorer (hash_state);
- seeds are nested in games, and **two games cannot support a general claim**: no statement about
  a population of games, about other planners, or about goal identification in general.

The paper never says "the barrier is goal inference" in general, never extends E9 to the held-out
games, to other agents, to "frame-only agents", or to ARC-AGI-3, and always names the three games
and the instrument.

- **BINDING (goal information is the binding constraint):**
  - *May say:* "For our planner on two train games whose source we read (tu93, dc22), supplying
    the true goal colour with everything else unchanged [raised levels completed by x / cut the
    actions per level by a factor y / won level(s) z]; for this instrument on these two games,
    identifying the goal was the binding constraint." It may then connect this, as consistent and
    not as proof, to the held-out census, where no goal was ever confirmed.
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
- **NOT TESTABLE (ls20):** reported as a finding: the planner's goal language (reach a place,
  named by colour) cannot represent ls20's predicate, quoted from `docs/E9_goals.md` ("every
  target reached with matching shape, colour and rotation").
- **Arm P, if run:** reported only as "the value of knowing the exact place", beside the verdict
  and never as part of it, with the tu93 rotation caveat (Section 3).

## 7. Gates and commands

- **G1 done:** docs/E9_goals.md, commit 8f8047f, SHA-256
  e87c1778c73752549a2defc9f5bfbddca81a7c96d7b5780bcc370b71576063bd.
- **G2:** `nav_oracle` implemented, and equivalence with `nav` shown with the oracle switched off
  (no colours handed), on all three games, seeds 1000-1001, 3,000 actions. The code hashes of
  g_nav.py and g_nav_run.py are recorded after G2 passes; no code changes after that point.
- **G3:** a reporting script that computes Sections 4-5 from the rows, written before any E9
  output is read.

No E9 game is run before G2 and G3 are committed.

Commands, once the code exists. Run from `D:\Research\arc3\repo\scripts`; each output is
written to `scripts\` and moved to `runs\` by the author. Script names for G2 and G3 are
provisional until that code is written.

G2, equivalence with the oracle off (no game outcome is read; only whether the two modes' rows are
identical):

```powershell
cd D:\Research\arc3\repo\scripts
$py = "D:\Research\arc3\brutus\.venv\Scripts\python.exe"
$env_dir = "D:\Research\arc3\brutus\environment_files"
& $py e9_equiv.py --games tu93,dc22,ls20 --seeds 2 --budget 3000 --env-dir $env_dir
```

The E9 run, arms F, N, O:

```powershell
cd D:\Research\arc3\repo\scripts
$py = "D:\Research\arc3\brutus\.venv\Scripts\python.exe"
$env_dir = "D:\Research\arc3\brutus\environment_files"
& $py g_nav_run.py --games tu93,dc22,ls20 --modes hash_state,nav,nav_oracle --seeds 10 --budget 20000 --game-seconds 36000 --hours 48 --workers 8 --env-dir $env_dir --tag e9_oracle_3x10 --resume
```

Output `scripts\navrun_e9_oracle_3x10.json` (90 rows), moved by the author to
`runs\navrun_e9_oracle_3x10.json`.

The report (G3; reads the E9 file and the E2 file, plays no game):

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\e9_report.py --e9 runs\navrun_e9_oracle_3x10.json --e2 runs\navrun_e2_hash_25x10.json
```

Optional arm P, only after the report of arms F, N, O exists and time allows:

```powershell
cd D:\Research\arc3\repo\scripts
$py = "D:\Research\arc3\brutus\.venv\Scripts\python.exe"
$env_dir = "D:\Research\arc3\brutus\environment_files"
& $py g_nav_run.py --games tu93,dc22 --modes nav_oracle_place --seeds 10 --budget 20000 --game-seconds 36000 --hours 48 --workers 8 --env-dir $env_dir --tag e9_place_2x10 --resume
```

## 8. Decisions recorded 26 September 2026, before any E9 output existed

These were decided by the author on 26 September 2026, after the E9 code was written and tested
at small budgets on tu93 and dc22, and **before any E9 output existed** (the registered E9 run of
Section 7 had not been started). No threshold in Section 5 changed.

**D1, V2 separates two failure kinds, and only one blocks.**
- A level that ended on a position showing no oracle colour **fails V2 and blocks the report**.
- A level whose ending position the planner could not read is **not a V2 failure**. This covers a
  level won during the explorer's click scan, won by a click action (the planner observes only its
  keyboard steps), or won when the planner had no position after a fallback. It is reported as
  "ending not seen", counted per game for arm O, and excluded from the V2 denominator, with that
  exclusion stated beside every result.

Reason: "not seen" is a limit of the instrument's observation, not evidence that the oracle colour
was wrong, and blocking on it would make dc22 unreportable for a reason unrelated to the question.

**D2, eligible level, as registered.** A level counts as eligible for Section 5 (shared, newly won)
if arm O targeted an oracle colour on it (`oracle_targets > 0`) in at least one seed.

**D3, when the oracle colours are read.**
- They are read at the level's first planner step. On level 1 that step may follow the explorer's
  opening actions (for example a click scan), so the oracle is **not necessarily available from
  action 1** of level 1. On later levels the first planner step is the level's first frame.
- Avatar colours are removed at use, not at read, because the avatar is not yet known at level 1's
  start (G-NAV learns it in its first steps).

**D4, disclosure of an observation made during testing.** While testing the code at 1,500
actions (tu93, seed 1000, not a registered run), the author's assistant observed:
- tu93 level 1 was won in 43 actions with the oracle, against 71 without (human count 19);
- the oracle colour marked only the exit (V5 = 0 cells).

The protocol and its thresholds (Sections 1-6) were fixed before that observation, and nothing in
them was changed after it. D1-D3 concern the reporting of V2, the definition of an eligible level
and the timing of the colour read; none changes a threshold or a prediction.
