# E1 phase 2 protocol: Rudakov et al. agent on the 25 public games

Written 25 September 2026, before any held-out game has been played by this agent. The plan is
docs/archive/TOG_PLAN_v2.md Section 3; no threshold in it is changed here. The author runs every command
below; nothing in this document is a result of phase 2.

Agent: Rudakov, Shock & Cowley's "heuristicagent" (arXiv 2512.24156), vendored unedited at
commit c2d98318ecca38c8ee9fb49b5af159e51770bad7 (external/rudakov_just_explore/PROVENANCE.md).
Harness: scripts/e1_rudakov_adapter.py at the commit that adds this document's --resume support
(1c898d7), mode name "rudakov". Engine: arc-agi 0.9.8, arcengine 0.9.3, offline, environment files
in D:\Research\arc3\brutus\environment_files. Machine: lenovo, 8 workers.

## 1. Admissibility results already in runs/

| item | result | file |
|---|---|---|
| A1 code, licence, commit | commit pinned, MIT, file hashes recorded | external/rudakov_just_explore/PROVENANCE.md |
| A2 licence | MIT: use and modification permitted | same |
| A3 CPU only | no GPU code or weights | docs/E1_rudakov_feasibility.md Section 4 |
| A4 no LLM or network at play time | none on the heuristicagent path; the adapter makes no network call | same |
| A5 adapter changes I/O only | no line of theirs edited; boundary items B1-B7 | docs/E1_rudakov_feasibility.md Section 5 |
| A6 fidelity, as registered (1,000 actions, ft09 and tu93, seed 1000) | their REST loop vs adapter: IDENTICAL, 1,001 issued actions on each game; scorecard per-level counts identical; identical under PYTHONHASHSEED 1 and 2. **No level was won in either game**, so this run does not exercise level transitions | runs/e1_rudakov_fidelity_ft09-tu93_1000.json |
| A6, phase-1 check (300 actions, tu93) | IDENTICAL, 301 issued actions | runs/e1_rudakov_fidelity_tu93_300.json |
| A6, level transitions (300 actions, vc33 and lp85, seed 1000) | **not yet in runs/.** In the assistant's test run: IDENTICAL on both, with vc33 winning 2 levels (card_levels [26, 136, 138, ...]) and lp85 1 level ([118, 182, ...]). To be run by the author before the held-out run (command 0 below) | runs/e1_rudakov_fidelity_vc33-lp85_300.json (to be written) |
| A7 cost, as registered (2,000 actions, ft09 and tu93) | ft09 0.021 s/action (engine 0.0016), tu93 0.0186 s/action (engine 0.0008); below the 0.28 s threshold | runs/e1_rudakov_a7_cost.json |
| phase-1 timing (200 actions, tu93 and dc22) | tu93 0.0188, dc22 0.017 s/action | runs/e1_rudakov_phase1_timing.json |

Consequence of A7 under plan 3.1: 0.021 s is below 0.28 s, so the registered protocol is the full
one, **10 seeds (1000-1009)**. The 4-seed variant in plan 3.1 applies only between 0.28 and
0.70 s per action. See Section 3.

Cost growth: in their code, per-action cost grows with the number of distinct frames seen
(docs/E1_rudakov_feasibility.md Section 7). A7 was measured at 2,000 actions; a 20,000-action run
can be slower per action. Each row records sec_per_action, so the actual cost is reported.

## 2. Known behaviour of their agent that the results must be read with

### 2.1 levels_completed vs score (API version difference)

Their code was written for the 2025 Preview API, where a frame's `score` field is the number of
levels completed. The arc-agi 0.9.8 engine reports this as `levels_completed` and has no `score`.
Their `FrameData` model ignores the unknown field, so an unconverted frame reports `score = 0`
forever. Their `main()` would then never see a level end, and never reset its graph or re-detect
status bars for the new level.

How the adapter handles it (boundary item B2): every engine frame is converted into their
`FrameData` with `score = levels_completed`. Nothing else in their code is touched. Checks:
- In the fidelity check's REST arm the same mapping is applied on the server side. Both arms
  agree on games where levels are won (vc33, lp85; Section 1, pending the author's run).
- Every phase-2 row records the steps at which levels were won
  (`diag.level_wins_at_step`), and how many of those wins were followed by their
  `GraphExplorer.reset` (`diag.level_wins_followed_by_graph_reset`). The reset is observed, not
  altered.
- The end-of-run report prints "level wins not followed by their graph reset". Anything other
  than "none" means B2 failed on that run, and the run is reported as an adapter failure.

### 2.2 ACTION7 is absent from their agent

The 0.9.8 engine has ACTION7; their `GameAction` enum stops at ACTION6, and `choose_action` maps
only keyboard actions 1-5. Games that offer ACTION7 are played without it. This is their policy
as published, run unchanged, and the adapter does not add ACTION7.

Games where our own agent pressed key 7 on level 1 (runs/census_v2.json, G-NAV learn phase,
4 held-out seeds, 2 train seeds). The list is what G-NAV tried, not a full inventory of every
level's available actions:

| game | split | keys tried by G-NAV | key 7 in G-NAV's census | consequence for their agent |
|---|---|---|---|---|
| ar25 | held-out | 1 2 3 4 5 7 | accepted, step [3, 3] | the same step as keys 2 and 3; likely little effect |
| bp35 | held-out | 3 4 7 | accepted, step [-6, 0] | key 7 was the only reliable leftward move (key 3 agreed on 1 of 7 presses): their agent's keyboard control on bp35 is likely one-directional |
| sb26 | held-out | 5 7 | not accepted | one of two keyboard actions unavailable to them |
| sk48 | held-out | 1 2 3 4 7 | not accepted by the press test, but in G-NAV's final effect model on all 4 seeds as [0, -6] (the same step as key 1) | likely little effect |
| su15 | held-out | 7 | not accepted | their agent has no keyboard action on su15; clicks only |
| lf52 | train | 1 2 3 4 7 | not accepted | uncertain |

These six games are marked "ACTION7 unavailable to this agent" in every E1 table. The decision
rule (Section 4) is applied as registered, with no exclusion; any game where the absence of
ACTION7 plausibly changed the outcome is named beside the result.

### 2.3 Their error-recovery path

On tu93, from step 300 onward, a (masked frame, action) pair that their agent had already
recorded produced a different outcome. Their `choose_action` then raises
`ValueError: Old value 1.0 is not equal to new value -1.0` (heuristic_agent.py line 298). Their
recovery re-initialises the graph, but it then fails repeatedly with the assertion "Edge result
must be untested before recording a test", and each failure repeats the last action.

The counts on tu93:
- A7 run: 1,667 such errors in 2,000 actions (runs/e1_rudakov_a7_cost.json,
  diag.their_prints.Error).
- Fidelity run: 686 errors in 1,000 actions in their own REST loop, 687 through the adapter; the
  one extra is the adapter's final call after the budget, whose result is not used.

This is their code's behaviour on the current tu93, not an adapter effect. Their README notes
that non-determinism or partial observation "can also cause issues". Every row reports the count;
the end-of-run report lists every run with a non-zero count; results are reported with it and no
run is dropped for it.

### 2.4 Other differences from their published runs

- Their runs were seeded from the wall clock; ours use seeds 1000-1009 (boundary item B3).
- Their per-action sleep of 0.31 s is removed (B4); it changes no decision (the fidelity checks
  compare against their loop with the sleep in place).
- Their games and API were the 2025 Preview's; their published numbers (median 30 of 52 preview
  levels in the paper; 12 of 25 private levels in the official preview evaluation) are not
  comparable one-to-one with ours, and no sentence will compare them as if they were.

## 3. Commands, in order (PowerShell, working directory D:\Research\arc3\repo)

Settings common to all phase-2 runs:
- `--budget 20000`: the registered action budget.
- `--game-seconds 28440`: their own per-game time limit (TOTAL_TIME_ALLOWED = 7.9 h). It is set
  so the action budget, not our clock, ends a run. Time-truncated runs are listed at the end of
  each run and kept, labelled.
- `--workers 8`.

Command 0: level-transition fidelity check. Train games only; about 4 minutes.

```powershell
cd D:\Research\arc3\repo
$py = "D:\Research\arc3\brutus\.venv\Scripts\python.exe"
& $py scripts\e1_rudakov_adapter.py --fidelity --fidelity-games vc33,lp85 --fidelity-actions 300
```

Expected: `U_vs_A IDENTICAL (301 issued actions)` and `card_levels_U_vs_A IDENTICAL` for both
games. Anything else: stop and do not run command 1.

Command 1 (stage 1): all 25 games, seeds 1000-1003, 20,000 actions. This is the 4-seed run
requested. It plays held-out games.

```powershell
cd D:\Research\arc3\repo
$py = "D:\Research\arc3\brutus\.venv\Scripts\python.exe"
& $py scripts\e1_rudakov_adapter.py --games all --allow-heldout --seeds 4 --budget 20000 --game-seconds 28440 --workers 8 --tag lenovo_25x4_20k
```

Output: runs/e1_rudakov_lenovo_25x4_20k.json (100 rows). While it runs, completed rows are appended
to runs/e1_rudakov_lenovo_25x4_20k.json.partial.jsonl; the partial file is deleted when all 100
rows are complete.

If it stops: run the same command again (the partial file is read); if the output file already
exists but is incomplete, add `--resume`:

```powershell
cd D:\Research\arc3\repo
$py = "D:\Research\arc3\brutus\.venv\Scripts\python.exe"
& $py scripts\e1_rudakov_adapter.py --games all --allow-heldout --seeds 4 --budget 20000 --game-seconds 28440 --workers 8 --tag lenovo_25x4_20k --resume
```

Expected end of output: "complete: 100 of 100 (game, seed) runs"; "level wins not followed by
their graph reset ...: none"; the list of time-truncated runs (expected: none) and of runs where
their choose_action raised (expected: at least the tu93 runs).

Command 2 (stage 2): extend to the registered 10 seeds, reusing the 100 stage-1 rows unchanged
(stage 1's file is only read).

```powershell
cd D:\Research\arc3\repo
$py = "D:\Research\arc3\brutus\.venv\Scripts\python.exe"
& $py scripts\e1_rudakov_adapter.py --games all --allow-heldout --seeds 10 --budget 20000 --game-seconds 28440 --workers 8 --tag lenovo_25x10_20k --resume runs\e1_rudakov_lenovo_25x4_20k.json
```

Output: runs/e1_rudakov_lenovo_25x10_20k.json (250 rows; "resume: 100 completed rows taken from
...", then 150 runs).

Which set decides (decided by the author on 25 September 2026, before any phase-2 result was
read). The 10-seed protocol is used as registered, because the measured cost is 0.02 s per action
(A7: ft09 0.021, tu93 0.0186), below the 0.28 s threshold that plan 3.1 ties to the full 10-seed
protocol. The 10-seed file (command 2) is the one the Section 4 rule is applied to. The 4-seed
file from command 1 is stage 1 of the same run. It may be reported only as "4 seeds, interim",
and it is not used to classify the agent.

Secondary arm: skipped (decided by the author on 25 September 2026, before any phase-2 result
was read). This is a recorded deviation from plan 3.2, which says: "If the agent's published
configuration uses a different action budget, that budget is run as a secondary arm and reported
separately". Their published configuration has no action budget: MAX_ACTIONS 1,000,000 and a
7.9 h time limit per game. It is skipped for three reasons:
- 25 games at up to 7.9 h per game, repeated over seeds, is not affordable on the lenovo within
  the E1 deadline (9 October 2026).
- The registered 20,000-action run answers the question Section 3 asks. The decision uses the
  20,000 arm in any case (plan 3.2).
- Their published preview-challenge result is cited as they report it, and is not re-measured.
The manuscript states that the published configuration was not run, and why, wherever the E1
result appears.

Command 3 (scoring input): held-out decomposition of the 10-seed file. This reads rows only and
plays no game.

```powershell
cd D:\Research\arc3\repo\scripts
$py = "D:\Research\arc3\brutus\.venv\Scripts\python.exe"
& $py g_decompose.py --files ..\runs\e1_rudakov_lenovo_25x10_20k.json --env-dir D:\Research\arc3\brutus\environment_files --games heldout --tag e1_rudakov_heldout_10
```

Output: runs/decompose_e1_rudakov_heldout_10.json.

Command 4 (the decision). This reads rows only and plays no game. It needs the E2 file (our
hash_state at 10 seeds, 20,000 actions, all 25 games), which does not exist yet; E2 runs first.

```powershell
cd D:\Research\arc3\repo
$py = "D:\Research\arc3\brutus\.venv\Scripts\python.exe"
& $py scripts\e1_decide.py --agent runs\e1_rudakov_lenovo_25x10_20k.json --reference runs\navrun_e2_hash_25x10.json
```

Output: runs/e1_decision.json. It prints M1-M4 for both files with hierarchical bootstrap 95%
intervals (descriptive; the point values decide), each condition (i)-(vi) with its value, and one
line "DECISION: REPRODUCES | BREAKS | INCONCLUSIVE - decided by ...". When a BREAKS condition
and the REPRODUCES conditions both hold, it prints BREAKS and lists both condition sets with
their values (precedence, Section 4).

## 4. The decision rule (docs/archive/TOG_PLAN_v2.md Sections 3.2-3.4, verbatim)

Measures (3.2):

> Per agent, computed on the 17 held-out games (the 8 train games, with tu93/dc22/ls20 labelled
> source-informed, are reported beside them but do not enter the decision):
> - M1 recorded: mean over games of the seed-mean scorecard score.
> - M2 AT HUMAN: the score the same runs would have had if every won level had cost exactly the
>   human count (same won levels, no extra level), mean over games of seed means; and the ratio
>   M2/M1 (undefined if M1 = 0; then reported as "M1 = 0").
> - M3 lv3+: the number of (game, seed) runs on held-out games that won level 3 or a later level.
> - M4 levels: sum over the 17 held-out games of the seed-mean levels completed (levels per seed).
> Reference values from our agent (hash_state, 4 seeds): M1 = 0.3329 (runs/ablate_lenovo_6x4.json);
> M4 = 11.2 levels per seed summed over the 17 held-out games (docs/HANDOFF_GNAV.md, UNTRACED to a
> script output; E2 recomputes it at 10 seeds before any external agent is scored).

Classification (3.3):

> REPRODUCES if all of:
>   (i)   M1 < 0.5;
>   (ii)  M2 / M1 > 5;
>   (iii) M3 = 0.
> BREAKS if any of:
>   (iv)  M1 >= 1.0 (three times our 0.3329, rounded up);
>   (v)   level 3 or later won on at least 2 held-out games, each in at least half of that
>         agent's seeds;
>   (vi)  M4 at least twice our E2 value of M4.
> INCONCLUSIVE otherwise (for example M1 = 0.6, or a single lucky lv3 win), or if the agent
> could not produce per-level scorecard counts.
>
> Precedence (added 25 September 2026, decided before any phase-2 result was read): BREAKS takes
> precedence over REPRODUCES. If any of (iv)-(vi) holds, the label is BREAKS even when (i)-(iii)
> also hold. Reason: REPRODUCES asserts that the pattern measured on our agent also holds for an
> independently authored agent. An agent completing at least twice E2's levels has not reproduced
> that pattern, whatever its score. The card-count clause comes first (also decided 25 September
> 2026, before any phase-2 result was read): if the agent's rows lack per-level scorecard counts,
> the label is INCONCLUSIVE before any BREAKS or REPRODUCES condition is considered. Reason: M2
> (AT HUMAN) cannot be computed without those counts, and a label from a partial set of measures
> would not be the registered one. M1, M3 and M4 could still be computed (from the recorded score
> and levels completed); they are reported, but no label is given from them alone. (The
> rule above as first written did not order these labels; the gaps were found while writing
> scripts/e1_decide.py, and no threshold is changed by this paragraph.)

What the paper says (3.4):

> - At least two admissible independent agents REPRODUCE and none BREAKS: the paper may say "the
>   pattern (i)-(iii) holds for the N independent frame-only agents we measured on the public set".
>   Still not "frame-only agents plateau".
> - Any admissible independent agent BREAKS: this is a headline result. The abstract is rewritten
>   around it; our agent's pattern becomes "a property of our agents, not of the agents measured".
> - Fewer than two admissible independent agents by 9 October 2026: every family statement is
>   removed; the paper speaks of the agents we measured, by name. The venue decision in Section 9
>   is re-taken.
> - The official non-LLM templates never count toward "independent". They are reported as a
>   baseline.
>
> "Independent" means authored by people other than the author of this paper, not derived from our
> code, and not an organiser template.

How each measure is computed from the rows (fixed now; it adds no threshold):
- M1: for each held-out game, the mean of `score` over its seeds; then the mean over the 17
  games.
- M2: AT HUMAN per run, computed by e1_decide.py from the row's `levels` (k) and the length N of
  its `card_baseline` with the scorecard rule: 100 k(k+1) / (N(N+1)). Then the seed mean per game,
  then the mean over the 17 games.
- M3: the number of held-out rows with `levels >= 3`. This is not g_decompose's "lv3+" column,
  which counts won levels, not runs.
- M4: for each held-out game, the mean of `levels` over its seeds; then the sum over the 17 games.
- (v): for each held-out game, the number of seeds with `levels >= 3`; count the games where
  that is at least half the seeds.

These computations are implemented in scripts/e1_decide.py (command 4). It was written and tested
on synthetic rows before any phase-2 or E2 output was read.

Change record, 25 September 2026 (before any phase-2 result was read). The rule as first
registered did not say what happens when REPRODUCES and BREAKS both hold. This can happen:
(i)-(iii) true together with (vi), e.g. an agent that wins levels 1 and 2 on many games, slowly,
and never level 3, so that M4 is at least twice E2's M4 while M1 < 0.5 and M3 = 0. The first
version of e1_decide.py (commit e82dc11) printed CONFLICT in that case. The author settled the
precedence: **BREAKS takes precedence over REPRODUCES**, with the reason recorded in docs/
archive/TOG_PLAN_v2.md Section 3.3 (quoted above). e1_decide.py now prints BREAKS in that case and lists
both condition sets with their values; CONFLICT is no longer an outcome. The rule's last clause
(no per-level scorecard counts gives INCONCLUSIVE) is checked before anything else, as in the
first version; the author confirmed this order on 25 September 2026, with the reason that
M2 cannot be computed without per-level counts and a label from partial measures would not be the
registered one. It is recorded in Section 3.3 (quoted above). No threshold changed.

Precondition for scoring (not for running): BREAKS (vi) needs our E2 value of M4 (hash_state,
10 seeds). E2 has not been run. Plan 3.2 says E2 is recomputed before any external agent is
scored. Commands 1-3 may run now, but the classification waits for E2.

## 5. What each outcome lets the paper say, for this agent

This is the first admissible independent agent. The two-agent condition in 3.4 cannot be met by it
alone.

- **REPRODUCES**: "Run through our harness on the current 25-game public set, the Rudakov et al.
  agent shows the same pattern: recorded score below 0.5, AT HUMAN more than five times the
  recorded score, no level 3 won on the held-out games." It counts as one of the two independent
  agents 3.4 requires. With no second admissible independent agent by 9 October 2026, no family
  statement is made; the paper names the agents measured.
- **BREAKS**: a headline result. The abstract is rewritten around it, and our agents' pattern is
  described as "a property of our agents, not of the agents measured". The comparison is stated
  with its differences: their agent ran unchanged apart from B1-B7, without ACTION7, on the
  current games rather than the preview games.
- **INCONCLUSIVE**: the numbers are reported with the reason (which condition missed). The agent
  does not count toward the two REPRODUCES agents, and no family statement rests on it.

In every outcome:
- The six games without ACTION7 (Section 2.2) and the error-recovery counts (Section 2.3) are
  reported beside the result.
- The source-informed train games (tu93, dc22, ls20) are reported apart and do not enter the
  decision.
- No sentence says anything about the private set, or compares these numbers directly with their
  preview-challenge numbers.
