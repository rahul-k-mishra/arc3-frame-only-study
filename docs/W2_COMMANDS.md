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

**The cap (v1.1 draft D5).**
- The fidelity check does not set the cap; its speeds are recorded as infrastructure facts only.
- The pilot (block C) runs with --seconds 86400.
- The confirmatory cap per suite is three times the longest pilot run's wall time in that suite, over all modes and conditions, rounded up to a whole minute. scripts/pilot_cap.py computes it from the pilot rows (block D), and it is recorded in D5 at the v1.1 tag.

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

C1. Suite B pilots, raw and macro, modes hash_state, nav and i1. That is 6 games × 10 seeds × 3 modes × 2 conditions = 360 runs of 20,000 actions, with no cap in practice (86,400 s).

```powershell
cd D:\Research\arc3\repo
Remove-Item Env:BABYAI_DONE_ACTIONS -ErrorAction SilentlyContinue
& D:\Research\arc3\brutus\.venv_games\Scripts\python.exe scripts\run_suite.py --suite minigrid --condition raw,macro --games pilot --modes hash_state,nav,i1 --seeds 10 --budget 20000 --workers 8 --seconds 86400 --resume
```

C2. Suite C pilots, center_off and center_on, modes hash_state, nav and i1. That is 2 games × 10 seeds × 3 modes × 2 conditions = 120 runs, with no cap in practice (86,400 s).

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe scripts\run_suite.py --suite procgen --condition center_off,center_on --games pilot --modes hash_state,nav,i1 --seeds 10 --budget 20000 --workers 8 --seconds 86400 --resume
```

C3. If a run ends with an error, rerun the same command. Rows written without error are skipped; errored rows rerun.

**Output:** runs/suites/<suite>/<condition>/<mode>/<game>__<seed>.json, one per run. The console ends with `summary: N rows written this call, N errors, N cut by the cap`.

## Block D — the confirmatory cap from the pilot rows

D1. After blocks C1 and C2 finish, compute the cap per suite (v1.1 draft D5). It reads runs/suites/ and plays nothing.

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\pilot_cap.py
```

Expected: one line per suite, `<suite>: N pilot rows, N with an error; longest <game> <condition> <mode> seed <s> <t> s -> cap <c> s`.
