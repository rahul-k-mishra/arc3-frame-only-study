# W2_COMMANDS.md — fidelity check, dry run, pilot

Written 27 September 2026, after RKM's decisions on docs/ADAPTER_FEASIBILITY.md Section 2 (PREREG.md v1.1 draft).

- Working directory for every block: `D:\Research\arc3\repo`, the main checkout, not the E6 worktree.
- One venv per suite: suite B (MiniGrid/BabyAI) in `D:\Research\arc3\brutus\.venv_games`, suite C (Procgen) in `D:\Research\arc3\brutus\.venv_procgen`.
- Paste each block's console output. The assistant does not open runs/.

## Block A — fidelity check, both suites, both conditions, all games

An infrastructure check under the PREREG Section 8 exception (v1.1 draft D8): 200 random actions twice per game and condition, no census, no agent.

A1. BabyAI done actions off:

```powershell
cd D:\Research\arc3\repo
Remove-Item Env:BABYAI_DONE_ACTIONS -ErrorAction SilentlyContinue
```

A2. Suite B, raw and macro, 167 games × 2 conditions:

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_games\Scripts\python.exe scripts\fidelity_check.py --suite minigrid --workers 8
```

A3. Suite C, center_off and center_on, 16 games × 2 conditions:

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe scripts\fidelity_check.py --suite procgen --workers 8
```

A4. If any job ends with status error, rerun the same command. Error rows rerun; ok rows are skipped.

**The cap for block C (v1.1 draft D5).** Cap = 3 × the slowest game's time for 20,000 actions = 3 × 20,000 / (the smallest steps_per_s in the suite's table). Rounded up to a whole minute, one value per suite. The assistant computes it from the pasted tables if asked, and the value is recorded in the v1.1 diff section.

## Block B — dry run of run_suite.py on the eight pilot games

This builds each environment once (one reset, no step) and prints the grid size and both key maps (R/N and I1). It plays nothing.

B1. Suite B pilots, raw and macro:

```powershell
cd D:\Research\arc3\repo
Remove-Item Env:BABYAI_DONE_ACTIONS -ErrorAction SilentlyContinue
& D:\Research\arc3\brutus\.venv_games\Scripts\python.exe scripts\run_suite.py --suite minigrid --condition raw,macro --games pilot --dry-run
```

B2. Suite C pilots, center_off and center_on:

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe scripts\run_suite.py --suite procgen --condition center_off,center_on --games pilot --dry-run
```

Expected first line of each: `frozen blob hashes: 6 of 6 match PREREG.md Section 5.4`.

## Block C — the pilot

**Nothing in block C touches a confirmatory game.** `--games pilot` resolves to exactly the eight registered pilots (PREREG Section 8): six on suite B, two on suite C. run_suite.py refuses to start if a frozen file's blob hash differs from PREREG Section 5.4.

C0. Install I1's two import dependencies in each suite venv, at the ARC venv's versions, then check that nothing else moved.
- Expected versions after the install: requests 2.34.2, pydantic 2.13.5.
- numpy must be unchanged: 2.4.6 in .venv_games, 1.26.4 in .venv_procgen. Record any difference before going on.

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_games\Scripts\python.exe -m pip install "requests==2.34.2" "pydantic==2.13.5"
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe -m pip install "requests==2.34.2" "pydantic==2.13.5"
& D:\Research\arc3\brutus\.venv_games\Scripts\python.exe -c "import importlib.metadata as m; print('games', 'numpy', m.version('numpy'), 'requests', m.version('requests'), 'pydantic', m.version('pydantic'))"
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe -c "import importlib.metadata as m; print('procgen', 'numpy', m.version('numpy'), 'requests', m.version('requests'), 'pydantic', m.version('pydantic'))"
```

C1. Suite B pilots, raw and macro, modes hash_state, nav and i1. That is 6 games × 10 seeds × 3 modes × 2 conditions = 360 runs of 20,000 actions. Replace `<CAP_B_SECONDS>` with the suite-B cap from block A.

```powershell
cd D:\Research\arc3\repo
Remove-Item Env:BABYAI_DONE_ACTIONS -ErrorAction SilentlyContinue
& D:\Research\arc3\brutus\.venv_games\Scripts\python.exe scripts\run_suite.py --suite minigrid --condition raw,macro --games pilot --modes hash_state,nav,i1 --seeds 10 --budget 20000 --workers 8 --seconds <CAP_B_SECONDS> --resume
```

C2. Suite C pilots, center_off and center_on, modes hash_state, nav and i1. That is 2 games × 10 seeds × 3 modes × 2 conditions = 120 runs. Replace `<CAP_C_SECONDS>` with the suite-C cap from block A.

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe scripts\run_suite.py --suite procgen --condition center_off,center_on --games pilot --modes hash_state,nav,i1 --seeds 10 --budget 20000 --workers 8 --seconds <CAP_C_SECONDS> --resume
```

C3. If a run ends with an error, rerun the same command. Rows written without error are skipped; errored rows rerun.

**Output:** runs/suites/<suite>/<condition>/<mode>/<game>__<seed>.json, one per run. The console ends with `summary: N rows written this call, N errors, N cut by the cap`.
