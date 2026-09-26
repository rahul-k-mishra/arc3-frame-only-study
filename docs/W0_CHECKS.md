# W0_CHECKS.md — registered W0 infrastructure checks

Registered 27 September 2026, before any of these checks is run. RKM runs them; the assistant never opens their outputs.

## What these checks are, and what they are not

The checks below produce **infrastructure facts only**:
- install success;
- frame shape and dtype;
- action-set size;
- distinct-colour counts;
- actions per second;
- determinism pass or fail.

These facts may inform PREREG.md's registered budgets and adapter parameters (METHOD_BLUEPRINT.md Section 2.1: palette quantisation, frame crop, grid size, action list). **None of them enters the manuscript.**

The checks use random actions only. No census, no agent, no G and no score is computed, and no JSON field is a result about a game's mechanics.

This file registers the checks as the one exception to two rules:
- "no run before the prereg tag" (CLAUDE.md rule 4; TOG_PLAN_v3.md Section 10, items 4 and 11);
- "nothing from a confirmatory game is run before PREREG v1.1 is tagged" (METHOD_BLUEPRINT.md Section 2.7).

C2 and C3 touch every Procgen game and every MiniGrid and BabyAI environment, including the future confirmatory ones. That exposure is limited to what the fields below record, and it is stated here so that the paper can disclose it.

## What must be true, and how failure shows

| check | must be true | failure is visible as |
|---|---|---|
| C1 | a Python 3.10 interpreter exists, and procgen installs and imports in .venv_procgen | winget or pip error; the import check prints a traceback instead of the version line |
| C2 | the installed ProcgenGym3Env accepts the keywords used; each game runs 1,000 steps; frames are 64 × 64 × 3 uint8 if procgen behaves as documented | the script's first line prints "MISSING: [...]" and every game's JSON has status "keyword_missing"; a game that raises has status "error" with the message; a determinism mismatch shows as FAIL@<step> |
| C3 | every MiniGrid- and BabyAI- id accepts render_mode, highlight, tile_size and agent_pov (confirmed in the installed source, see C3) | status "error" with the constructor's message; determinism FAIL@<step> |

A failure is reported as it stands. A check is not rerun with changed settings to make it pass.

## C1 — Procgen install

- Python 3.10 venv at D:\Research\arc3\brutus\.venv_procgen, next to the existing venvs.
  - D:\Research\arc3\brutus\.venv holds ARC.
  - D:\Research\arc3\brutus\.venv_games holds MiniGrid and BabyAI. It is not inside this repository; it sits in D:\Research\arc3\brutus.
- Procgen publishes wheels only for Python 3.7–3.10 (METHOD_BLUEPRINT.md Section 3).
- On 27 Sep 2026, py -0 on the lenovo listed Python 3.12 and 3.11 and no 3.10, so the install line below is needed.
- Records: install success; the procgen version printed by the import check.

## C2 — Procgen smoke (scripts/w0_procgen_smoke.py)

**Settings:**
- all 16 games (procgen.env.ENV_NAMES; a fallback list of the 16 names in the script is used only if that import fails, and the script says so);
- distribution_mode "easy", use_backgrounds False, use_monochrome_assets True;
- one fixed start level: start_level 0, num_levels 1;
- rand_seed 1000;
- 1,000 steps from numpy.random.default_rng([1000, 0]) over the game's own action space.

The constructor keywords were written from memory of procgen 0.10.x. The script checks them against the installed ProcgenGym3Env (inspect.signature) before any game is run. If one is missing, no game is played, and every game's JSON records status "keyword_missing" and the actual signature.

**Records, per game:**
- obs shape and dtype (obs["rgb"]);
- action count (the action space's size);
- which info-dict keys contain "level_complete", and how many of the 1,000 steps had each true;
- all info keys seen;
- episode starts;
- distinct RGB colours over the 1,001 frames;
- steps per second (first run);
- determinism: the same (start level, seed, actions) run twice, frame sequences compared byte for byte (scripts/w0_common.py compare_frames), plus whether the level-complete counts and episode starts agree.

## C3 — MiniGrid and BabyAI smoke (scripts/w0_minigrid_smoke.py)

**Settings:**
- Venv: D:\Research\arc3\brutus\.venv_games (Python 3.11.9, minigrid 3.1.0, gymnasium 1.3.0).
- Every registered gymnasium id starting with MiniGrid- or BabyAI- (178 ids registered: 82 MiniGrid-, 96 BabyAI-).
- Constructed with gymnasium.make(env_id, render_mode="rgb_array", highlight=False, tile_size=8, agent_pov=False).
- Reset with seed 1000, then 200 steps from numpy.random.default_rng(1000) over the primitive action space. After an episode ends the env is reset without a seed, so its RNG continues from the seeded reset.

**Keyword names**, confirmed from the installed source, not from memory:
- minigrid/minigrid_env.py lines 43–47 (MiniGridEnv.__init__: render_mode, highlight, tile_size, agent_pov);
- lines 736–742: with agent_pov False, render() returns the full-grid frame (get_frame → get_full_render).

The source was read on 27 Sep 2026. The id count and the keywords were also confirmed by one make / reset(seed=1000) / render() call on MiniGrid-BlockedUnlockPickup-v0. No step was taken and nothing was saved.

**Records, per env:** the same fields as C2, plus:
- the primitive action count;
- the obs["image"] shape (MiniGrid's partial view, for reference);
- the steps at which episodes ended;
- episodes ended with reward > 0.

## Outputs

- One JSON per game: runs/w0_checks/procgen/<game>.json and runs/w0_checks/minigrid/<env_id>.json.
  - Fields: game, mode "w0_smoke", seed, suite, status, and the facts above.
  - These are infrastructure records, not ablate-format result rows: they carry no score, levels or level_log.
- A console table per suite, and a summary line with the ok count and the determinism pass count.
- Both scripts use a worker pool (8 workers; environments are created inside the worker, spawn-safe on Windows).
- They are deterministic given the seed.
- They are resume-safe: a game whose JSON exists is skipped unless --force; JSON is written atomically.
- The helpers (compare_frames, distinct_colours) were tested on synthetic arrays only.

## Commands (PowerShell, in order)

Working directory for every block: D:\Research\arc3\repo

1. Check for Python 3.10. If it is absent, install it. Then open a new PowerShell window so that py sees it.

```powershell
cd D:\Research\arc3\repo
py -0
if (-not (py -0 | Select-String "3\.10")) { winget install --id Python.Python.3.10 -e --source winget }
```

If winget is unavailable, install the Windows 64-bit Python 3.10 installer from python.org (Python 3.10.11, the last 3.10 release with a Windows installer), with "py launcher" ticked.

2. In the new window, confirm 3.10 and create the venv (C1):

```powershell
cd D:\Research\arc3\repo
py -3.10 --version
py -3.10 -m venv D:\Research\arc3\brutus\.venv_procgen
```

3. Install procgen and numpy into it (C1):

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe -m pip install --upgrade pip
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe -m pip install procgen numpy
```

4. Import check (C1). Expected: one line with the procgen and numpy versions and "import ok".

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe -c "import importlib.metadata as m, numpy; from procgen import ProcgenGym3Env; print('procgen', m.version('procgen'), 'numpy', numpy.__version__, 'import ok')"
```

If this fails with a numpy binary-compatibility error, the installed procgen wheel was built against numpy 1.x. That is an assumption, not a measured fact. Record the error and rerun step 3 with numpy<2 in place of numpy.

5. Procgen smoke (C2), in .venv_procgen:

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe scripts\w0_procgen_smoke.py --workers 8
```

6. MiniGrid and BabyAI smoke (C3), in .venv_games:

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_games\Scripts\python.exe scripts\w0_minigrid_smoke.py --workers 8
```

Paste the console output of steps 4–6. The assistant quotes it exactly and does not open runs/w0_checks/.
