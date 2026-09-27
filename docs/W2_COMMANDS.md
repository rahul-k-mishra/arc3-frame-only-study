# W2_COMMANDS.md — commands for the W2 fidelity checks

Written 27 September 2026. The working directory for every block is `D:\Research\arc3\repo` (the main checkout, not the E6 worktree).

## Before running: is the fidelity check allowed before PREREG v1.1?

PREREG.md v1 Section 8 says nothing from a confirmatory game is run before v1.1 is tagged, "except the registered W0 infrastructure checks". The fidelity check (PREREG Section 2.1; scripts/fidelity_check.py) plays every game of a suite, confirmatory ones included, with 200 random actions twice. It runs no census and no agent, and produces infrastructure facts only: determinism, grid shape, colour count, steps per second.

It is not named in the Section 8 exception. **RKM decides one of these before running:**
1. It counts as a registered infrastructure check, like W0. Run blocks 1–4.
2. It runs on the 8 pilot games only now (blocks 5–6), and on the confirmatory games after v1.1 is tagged.

## Blocks 1–4: the full fidelity check (both suites, both conditions)

1. Make sure BabyAI's done actions are off (PREREG 3.2):

```powershell
cd D:\Research\arc3\repo
Remove-Item Env:BABYAI_DONE_ACTIONS -ErrorAction SilentlyContinue
```

2. Suite B (MiniGrid + BabyAI), conditions raw and macro, in .venv_games. This is 167 games × 2 conditions.

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_games\Scripts\python.exe scripts\fidelity_check.py --suite minigrid --workers 8
```

3. Suite C (Procgen), conditions center_off and center_on, in .venv_procgen. This is 16 games × 2 conditions.

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe scripts\fidelity_check.py --suite procgen --workers 8
```

4. If any job ends with status error, rerun the same command. Error rows are rerun without --force; ok rows are skipped.

## Blocks 5–6: pilots only (option 2)

5. Suite B pilots:

```powershell
cd D:\Research\arc3\repo
Remove-Item Env:BABYAI_DONE_ACTIONS -ErrorAction SilentlyContinue
& D:\Research\arc3\brutus\.venv_games\Scripts\python.exe scripts\fidelity_check.py --suite minigrid --workers 8 --games MiniGrid-Empty-5x5-v0,MiniGrid-FourRooms-v0,MiniGrid-DoorKey-8x8-v0,MiniGrid-Dynamic-Obstacles-6x6-v0,MiniGrid-Fetch-5x5-N2-v0,BabyAI-GoToRedBallGrey-v0
```

6. Suite C pilots:

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe scripts\fidelity_check.py --suite procgen --workers 8 --games coinrun,bigfish
```

**Output:** runs/fidelity/<suite>/<game>__<condition>.json, one per job. The last lines of the console are a table and the summary line `summary: N ok, N error, N missing; identical on N of N`. Paste the console output; the assistant does not open runs/fidelity/.
