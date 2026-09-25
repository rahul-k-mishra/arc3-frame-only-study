# E1a feasibility: Rudakov, Shock & Cowley's graph-exploration agent

Written 25 September 2026, E1 phase 1 (feasibility and adapter). No held-out game was played.
The protocol is docs/TOG_PLAN_v2.md Section 3; nothing here changes a threshold in it.

Code: external/rudakov_just_explore, vendored unedited from
github.com/dolphin-in-a-coma/arc-agi-3-just-explore at commit
c2d98318ecca38c8ee9fb49b5af159e51770bad7 (2026-01-07, latest on the default branch when cloned).
Licence MIT; commit, licence text and file hashes in external/rudakov_just_explore/PROVENANCE.md.
Paper: arXiv 2512.24156.

## 1. Result of phase 1, per admissibility item

| item | status | evidence |
|---|---|---|
| A1 pinned code, licence, commit | met | PROVENANCE.md holds the commit and LICENSE text. The plan names a file `COMMIT`; the hash is in PROVENANCE.md instead (the file layout was set by the phase-1 instruction). |
| A2 licence permits research use and modification | met | MIT |
| A3 CPU only | met | numpy and pure Python; no torch, no CUDA, no model weights |
| A4 no LLM or remote API at play time | met | the policy calls no model; the adapter makes no network call |
| A5 adapter changes I/O only | met, with the list in Section 5 | no file of theirs edited; seven boundary items B1-B7 |
| A6 fidelity | **partly checked** | tu93, seed 1000, 300 steps: identical (Section 6). The registered A6 (1,000 actions on ft09 and tu93) is **not yet run**, and no level was won in the 300-step check, so the level-up path is untested |
| A7 cost at most 0.28 s per action | **preliminary only** | 0.0139 s per action over 400 actions (tu93 and dc22, 200 each). The registered A7 (2,000 actions on each of ft09 and tu93) is **not yet run**; per-action cost is expected to grow with graph size (Section 7) |

Independence (plan 3.4): the policy (agents/heuristic_agent.py, graph_explorer.py) was written by
the paper's authors, not derived from our code. The repository is a fork of the organisers'
ARC-AGI-3-Agents template, but the template parts it keeps (Agent base class, REST client, Swarm,
the LLM templates) are I/O scaffolding that the adapter replaces or does not load. It counts as
independent under the plan's definition; the template parts are named here so a reader can judge.

## 2. What they target

- The ARC-AGI-3 **Preview** challenge (2025) through its REST API at three.arcprize.org:
  `POST /api/scorecard/open`, `POST /api/cmd/{RESET,ACTION1..ACTION6}`, `GET /api/scorecard/...`,
  with an `X-API-Key` header (.env.example: `SCHEME=https`, `HOST=three.arcprize.org`).
  There is no local engine in the repository; games run on the server.
- Python >= 3.12 (.python-version: 3.12). The arc-agi and arcengine packages are not dependencies;
  they postdate the fork.
- Frame schema of the preview API (agents/structs.py, `FrameData`): `frame` (list of 64x64 integer
  grids), `state` (NOT_PLAYED / NOT_FINISHED / WIN / GAME_OVER), **`score` = levels completed**,
  `available_actions`, `guid`, `full_reset`, `action_input`.
- Actions RESET and ACTION1-ACTION6 (their `GameAction` enum has no ACTION7).
- Their published numbers are on the preview games (six public games, 52 levels; 12 of 25
  private levels in the official preview evaluation, a median of 17 after a later bug fix). The
  current 25-game public set and the current API differ from both.

## 3. How they take frames and emit actions

- Loop: `HeuristicAgent.main()` (heuristic_agent.py 454-489) calls
  `choose_action(frames, latest_frame)`, sends the action with `take_action` (agents/agent.py
  155-163: REST POST, reply validated into `FrameData`), appends the frame, and sets `level_up`
  when `frame.score` rises. An exception in `choose_action` sets `failed` and `level_up` and
  re-sends the previous action. The loop stops on WIN, on `MAX_ACTIONS` (1,000,000), or after
  `TOTAL_TIME_ALLOWED` (7.9 h).
- `choose_action` (170-405): RESET on NOT_PLAYED or GAME_OVER. Otherwise it takes the last 64x64
  grid, masks status bars (found at each level start), segments it into single-colour connected
  components, hashes the masked grid, and records the last transition in `GraphExplorer`. It then
  asks `GraphExplorer.choose_edge` for an action index. Indices below the number of segments are
  clicks (a random pixel of that segment, ACTION6); the rest are the keyboard actions 1-5 that
  the frame lists as available.
- `GraphExplorer.choose_edge` (graph_explorer.py 424-450): a random untested action from the
  highest-priority open group, otherwise a random action on a shortest path to the frontier.
  Clicks are grouped into five priority tiers by colour salience and size; keys are in the top
  tier.
- Randomness: Python's global `random`, seeded in `__init__` from the wall clock
  (`int(time.time()*1e6) + hash(game_id) % 1e6`, heuristic_agent.py 68-69). **Their runs are not
  reproducible by design; no seed is exposed.**

## 4. Dependencies, GPU, network, LLM

| declared (pyproject.toml) | needed by heuristicagent? | notes |
|---|---|---|
| numpy, pydantic, requests | yes | agent.py imports requests at module level (the adapter never sends a request) |
| pillow, matplotlib | no | only in debug plotting (`DEBUG_PLOTS=False`) and graph_explorer's demo; imported in try/except |
| dotenv | no | only in agents/__init__.py and main.py |
| langchain[openai], langgraph, langgraph-checkpoint-sqlite, openai, smolagents | **no** | imported by agents/__init__.py for the LLM templates; heuristicagent uses none of them |
| agentops (optional) | no | tracing; a no-op when absent |

- GPU: none anywhere in the heuristicagent path.
- Network: their play loop needs the preview server. Through the adapter: none.
- LLM: none in the policy. The LLM libraries are declared only because the fork keeps the
  organisers' LLM templates. `OPENAI_API_KEY` is never read on the heuristicagent path.
- Our environment (brutus .venv: numpy 2.5.3, pydantic, requests, flask, matplotlib, pillow,
  dotenv; Python 3.12.10) runs the policy with nothing installed. Their literal `main.py` does not
  import here, because agents/__init__.py needs the LLM libraries. Installing them into the
  experiment venv was not done; they are not needed.

## 5. What must change to run their policy unchanged on our offline engine, and what was changed

**No line of any file of theirs was edited** (hashes in PROVENANCE.md). The adapter
(scripts/e1_rudakov_adapter.py) replaces one method and sets five attributes from outside. Every
place where one of their lines is overridden or superseded:

| # | their line(s) | what the adapter does | why |
|---|---|---|---|
| B1 | agents/agent.py 155-163 `take_action` (and `do_action_request` 134-153) | overridden in a subclass: the action goes to `env.step` on the arc-agi 0.9.8 offline engine. Their first RESET of a play returns the environment's initial observation without a step. | no server offline. The 0.9.8 server itself answers the RESET that creates a play with the observation and no step (arc_agi/api.py, `full_reset`), so the scorecard counts match; checked in Section 6 |
| B2 | agents/structs.py 210 `FrameData.score` (read at heuristic_agent.py 472-478) | the engine's `levels_completed` is written into their `score` | **the current API renamed the field**. Unconverted, pydantic ignores `levels_completed`, `score` stays 0, and their agent never registers a level end. It would not reset its graph or status-bar mask at a new level. Their unmodified client against the 0.9.8 server would fail the same way |
| B3 | heuristic_agent.py 68-69 (wall-clock seed) | `random.seed(seed)` once, after construction | seeds are our replication unit (plan Section 8); their seeding makes every run unrepeatable |
| B4 | heuristic_agent.py 101 `minimal_step_time = 0.31` | set to 0 | a sleep that rate-limited the preview server; no decision depends on it (Section 6 compares against their loop with the sleep kept) |
| B5 | heuristic_agent.py 29 `MAX_ACTIONS`, 63 `TOTAL_TIME_ALLOWED` | set from `--budget` and `--game-seconds`; `take_action` stops the loop at the budget | our budget (20,000 actions in the protocol) and time cap; a run stopped by the time cap is marked `time_truncated` |
| B6 | agents/__init__.py (whole file) | not executed; their modules are loaded through a namespace stub for the package | it imports LLM templates that are not installed and not used |
| B7 | their `print` calls (several per action) | redirected to a counter; counts of "Error:", "Suspicious transition", "Lowest dist" are kept in each row's diag | console I/O only |

Not changed, and deliberately so:
- **ACTION7.** The 0.9.8 engine has ACTION7, but their enum stops at ACTION6 and their code maps
  only 1-5 to keys. Games that list ACTION7 are played without it. Our own census runs pressed
  key 7 on ar25, bp35, lf52, sb26, sk48 and su15 (runs/census_v2.json). Whether ACTION7 matters
  on those games is not known. This is an API-version limitation of their agent and is reported
  with phase 2's results; the adapter does not add it, because that would change the policy.
- **Error handling.** Their client validates any server reply into `FrameData`, so an error reply
  becomes a default frame with state NOT_PLAYED, and the agent resets. This happened in the first
  fidelity attempt (Section 6). The adapter never produces error replies.
- **Level-up handling, exception fallback, status-bar logic, priority groups:** all theirs.

## 6. Fidelity check (phase 1: tu93, seed 1000, 300 steps)

The arms:
- **U:** their `HeuristicAgent` with their own REST `take_action` and the 0.31 s sleep, against
  the arc-agi 0.9.8 local Flask server on the offline engine. The server adds `score` =
  `levels_completed` to each reply (B2 on the server side). The seed and action cap are set from
  outside.
- **A:** the adapter in the same process.
- **A1, A2:** the adapter in fresh processes with `PYTHONHASHSEED` 1 and 2. Their graph keeps
  frame hashes in Python sets, so these arms test whether set order reaches the actions.

Result (my test run; the author's run writes runs/e1_rudakov_fidelity_tu93_300.json):

    U vs A        IDENTICAL (301 issued actions: the creating RESET + 300 steps)
    A vs A1, A2   IDENTICAL
    card_levels   IDENTICAL ([300, 0, 0, 0, 0, 0, 0, 0, 0])

The first attempt did not pass, and the reason is recorded. The U arm sent the bare id `tu93`,
the 0.9.8 server replied "game tu93 not found", and their client turned each error into a
NOT_PLAYED frame and reset. So U issued RESET where A issued ACTION1, and the scorecard counted
nothing. Their main.py uses the versioned ids from `/api/games` (`tu93-0768757b`). The U arm now
does the same, and it reports any server error and declares itself invalid if one occurs.

What this check does not show:
- **No level was won in 300 steps, so the level-up path (B2, graph reset, status-bar
  re-detection) was not exercised.**
- **Their literal entry point was not the U arm.** main.py → Swarm has no seed, no action cap and
  imports the uninstalled LLM templates, so no same-seed comparison with it is possible. U runs
  their agent class and REST client unchanged, which is the part that could differ.
- **A6 as registered** (1,000 actions on ft09 and tu93) has not been run. ft09 also exercises
  clicks and, on our explorer's evidence, a level win within a few hundred actions. It should be
  run before phase 2:
  `scripts\e1_rudakov_adapter.py --fidelity --fidelity-games ft09,tu93 --fidelity-actions 1000`.

## 7. Cost per action (preliminary; not the A7 measurement)

tu93 and dc22 (train, source-informed), seed 1000, 200 actions each, lenovo, 2 workers:

    tu93  0.0146 s/action (inside env.step 0.0008)
    dc22  0.0132 s/action (inside env.step 0.0010)
    both  0.0139 s/action over 400 actions, against the 0.28 s threshold

Neither run won a level. dc22 issued 122 clicks and 77 key presses; tu93 issued keys only.

Why 200 actions does not settle A7:
- `GraphExplorer._rebuild_distances` walks every node after most transitions.
- `FrameProcessor.segment_frame` runs a flood fill over 4,096 cells plus a quadratic twin search
  over segments on every frame.

Per-action cost therefore grows with the number of distinct frames seen, and a 20,000-action run
can be much slower per action than a 200-action run. A7 must be measured as registered: 2,000
actions on each of ft09 and tu93. The time per 20,000-action run should also be recorded in
phase 2, since the protocol's 48-hour arithmetic (plan 3.1, A7) assumes a constant cost.

## 8. What is needed before phase 2 (playing all 25 games)

1. Run the registered A6 (ft09, tu93, 1,000 actions) and A7 (ft09, tu93, 2,000 actions); record
   both under runs/.
2. If A6 shows a mismatch, it must be explained before phase 2. The plan's fallback label
   ("adapter only, fidelity not checked") applies only when their loop cannot run, and here it
   can; an unexplained mismatch leaves the agent INCONCLUSIVE. If A7 exceeds 0.28 s, the plan's
   3.1 cost bands decide the number of seeds.
3. Phase 2 command, 25 games x 10 seeds x 20,000 actions, only after 1:
   `scripts\e1_rudakov_adapter.py --games train --seeds 10 --budget 20000 --tag lenovo_10x20k`,
   then the same with `--games heldout --allow-heldout`.
