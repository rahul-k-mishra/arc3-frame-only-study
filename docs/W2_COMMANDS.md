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

## Block C4 — the confirmatory cap from the pilot rows (done 27 Sep 2026)

*This block was "Block D" until 27 Sep 2026 (f). It was renamed so that D and E can hold the confirmatory runs and the analysis.*

C4. After blocks C1 and C2 finish, compute the cap per suite (v1.1 draft D5). It reads runs/suites/ and plays nothing.

```powershell
cd D:\Research\arc3\repo
& D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\pilot_cap.py
```

Expected: one line per suite, `<suite>: N pilot rows, N with an error; longest <game> <condition> <mode> seed <s> <t> s -> cap <c> s`.

**Result (RKM, 27 Sep 2026), recorded in PREREG v1.1 draft D5:**
- minigrid: longest 1081.6 s (MiniGrid-FourRooms-v0, raw, I1, seed 1003), cap 3300 s;
- procgen: longest 2481.5 s (bigfish, center_off, I1, seed 1003), cap 7500 s.

## Block D — the confirmatory runs (only after the tag prereg-v1.1 exists)

**Do not start block D before RKM has created the tag `prereg-v1.1`.** This is a registered rule, not a precaution: no run on a confirmatory suite-B or suite-C game before v1.1 is tagged (PREREG.md Section 8).

**What must be true first, and how a failure shows:**
- **The tag exists and the worktree is on it.** D1 prints `prereg-v1.1`. Any other output (an error, or a different name): stop.
- **The six frozen files match PREREG Section 5.4.** Every run_suite.py call prints `frozen blob hashes: 6 of 6 match PREREG.md Section 5.4` first. Otherwise it stops by itself.
- **The two D13 code items are in the tagged code** (implemented 27 Sep 2026 (g)): the center_on "camera_distinct" subset in analyze_v1/v2, and scripts/determinism_check.py (D7).
- **BABYAI_DONE_ACTIONS is unset.** The suite-B adapter raises if it is set.

**Why a worktree.** The runs are made from a worktree checked out at the tag, as E6 was. The code that plays is then exactly the tagged code. The rows are written into the main repository's runs\suites with `--out`, and the console logs into the main repository's runs\logs.

**Why Tee-Object.** Every console line is kept in the log file. BabyAI prints one `Sampling rejected: ...` line per rejected layout (minigrid/envs/babyai/core/roomgrid_level.py:137). These lines stay in the log, but a filter keeps them off the window.

D1. Create the worktree at the tag and the log folder (once):

```powershell
cd D:\Research\arc3\repo
git worktree add D:\Research\arc3\repo_prereg_v1_1 prereg-v1.1
git -C D:\Research\arc3\repo_prereg_v1_1 describe --tags --exact-match
New-Item -ItemType Directory -Force D:\Research\arc3\repo\runs\logs | Out-Null
```

Expected last line of output: `prereg-v1.1`.

D2. Construction check on every confirmatory environment, under the tag. It makes one reset per environment, takes no step, and plays nothing:

```powershell
cd D:\Research\arc3\repo_prereg_v1_1
Remove-Item Env:BABYAI_DONE_ACTIONS -ErrorAction SilentlyContinue
& D:\Research\arc3\brutus\.venv_games\Scripts\python.exe scripts\run_suite.py --suite minigrid --condition raw,macro --games confirmatory --dry-run 2>&1 | Tee-Object -FilePath D:\Research\arc3\repo\runs\logs\dryrun_confirmatory_minigrid.log | Where-Object { "$_" -notmatch 'Sampling rejected' }
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe scripts\run_suite.py --suite procgen --condition center_off,center_on --games confirmatory --dry-run 2>&1 | Tee-Object -FilePath D:\Research\arc3\repo\runs\logs\dryrun_confirmatory_procgen.log
Select-String -Path D:\Research\arc3\repo\runs\logs\dryrun_confirmatory_*.log -Pattern 'ERROR' | Measure-Object | Select-Object Count
```

Expected:
- each run_suite call prints `frozen blob hashes: 6 of 6 match PREREG.md Section 5.4` first;
- suite B then prints 161 × 2 = 322 environment blocks, and suite C 14 × 2 = 28;
- the last command prints `Count : 0`.

D3. Suite B, confirmatory: 161 games × 2 conditions × 3 modes × 10 seeds = **9,660 runs** of 20,000 actions, cap 3300 s (PREREG v1.1 D5):

```powershell
cd D:\Research\arc3\repo_prereg_v1_1
Remove-Item Env:BABYAI_DONE_ACTIONS -ErrorAction SilentlyContinue
& D:\Research\arc3\brutus\.venv_games\Scripts\python.exe scripts\run_suite.py --suite minigrid --condition raw,macro --games confirmatory --modes hash_state,nav,i1 --seeds 10 --budget 20000 --workers 8 --seconds 3300 --resume --out D:\Research\arc3\repo\runs\suites 2>&1 | Tee-Object -FilePath D:\Research\arc3\repo\runs\logs\confirmatory_minigrid.log -Append | Where-Object { "$_" -notmatch 'Sampling rejected' }
```

D4. Suite C, confirmatory: 14 games × 2 conditions × 3 modes × 10 seeds = **840 runs** of 20,000 actions, cap 7500 s (PREREG v1.1 D5). On the nine in-range games the center_on rows are required to equal the center_off rows (D13):

```powershell
cd D:\Research\arc3\repo_prereg_v1_1
& D:\Research\arc3\brutus\.venv_procgen\Scripts\python.exe scripts\run_suite.py --suite procgen --condition center_off,center_on --games confirmatory --modes hash_state,nav,i1 --seeds 10 --budget 20000 --workers 8 --seconds 7500 --resume --out D:\Research\arc3\repo\runs\suites 2>&1 | Tee-Object -FilePath D:\Research\arc3\repo\runs\logs\confirmatory_procgen.log -Append
```

D5. If the last line of D3 or D4 reports errors, run the same command again. Rows written without error are skipped. Errored rows run again. Rows cut by the cap are kept, not re-run (PREREG v1.1 D5).

D6. Verify the row counts. This reads runs\suites and plays nothing. It counts only the confirmatory games; the pilot rows sit in the same folders and are not counted:

```powershell
cd D:\Research\arc3\repo_prereg_v1_1
$check = @'
import json, os, sys
sys.path.insert(0, "scripts")
import analyze_common as C
OUT = r"D:\Research\arc3\repo\runs\suites"
truth = {"minigrid": C.parse_truth_minigrid("docs/GROUND_TRUTH_minigrid.md"),
         "procgen": C.parse_truth_procgen("docs/GROUND_TRUTH_procgen.md")}
conds = {"minigrid": ("raw", "macro"), "procgen": ("center_off", "center_on")}
for suite in ("minigrid", "procgen"):
    games = C.confirmatory(suite, truth[suite])
    tot = missing = err = cut = 0
    for cond in conds[suite]:
        for mode in ("hash_state", "nav", "i1"):
            n = 0
            for g in games:
                for s in range(1000, 1010):
                    p = os.path.join(OUT, suite, cond, mode, f"{g}__{s}.json")
                    if not os.path.exists(p):
                        missing += 1
                        continue
                    r = json.load(open(p, encoding="utf-8"))[0]
                    n += 1
                    err += "error" in r
                    cut += bool(r.get("cut_by_cap"))
            print(f"{suite} {cond} {mode}: {n} of {len(games) * 10} rows")
            tot += n
    print(f"{suite}: {tot} of {len(games) * len(conds[suite]) * 3 * 10} confirmatory rows; missing {missing}; with an error {err}; cut by the cap {cut}")
'@
$check | & D:\Research\arc3\brutus\.venv\Scripts\python.exe -
```

Expected:
- six lines `minigrid <condition> <mode>: 1610 of 1610 rows`, then `minigrid: 9660 of 9660 confirmatory rows; missing 0; with an error 0; cut by the cap <n>`;
- six lines `procgen <condition> <mode>: 140 of 140 rows`, then `procgen: 840 of 840 confirmatory rows; missing 0; with an error 0; cut by the cap <n>`.
- Any missing or errored row: go back to D5. A non-zero cut count is not an error. Those rows are reported as cut (PREREG v1.1 D5), and the count goes into STATE.md.

D7. The nine-game determinism check (PREREG v1.1 draft D8, D13). Run it after D4 and D6. It reads runs\suites, plays nothing, and writes runs\checks\determinism_check.json.
- For each of bossfight, chaser, dodgeball, heist, leaper, maze, miner, plunder and starpilot, every mode and every seed, the center_on row must equal the center_off row.
- Two sets of fields are left out of the comparison: the seven timing fields, and the three condition labels.

```powershell
cd D:\Research\arc3\repo_prereg_v1_1
& D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\determinism_check.py --suites D:\Research\arc3\repo\runs\suites --out D:\Research\arc3\repo\runs\checks\determinism_check.json --workers 8 2>&1 | Tee-Object -FilePath D:\Research\arc3\repo\runs\logs\determinism_check.log
"exit code $LASTEXITCODE"
```

Expected:
- nine lines `<game> pairs  30  identical  30`;
- then `total: 270 pairs compared, 270 identical, 0 differing, 0 missing -> PASS`, the `wrote ...` line, and `exit code 0`.
- Exit code 1 (a pair differs; the differing field names are printed): stop and report. The two conditions are then not identical as D13 registers, and the D13 reporting rule does not hold as written.
- Exit code 2 (rows missing): go back to D5 and D6.

## Block E — the analysis (after block D is verified)

**What must be true first:**
- D6 shows every confirmatory row present, with 0 errors.
- The analysis scripts in the worktree carry the D11 blob hashes of the v1.1 tag.
- The synthetic tests pass under the tag (E1).

E runs from the tag worktree, so the tagged analysis code is what runs. The tables are written into the main repository's docs\tables.

E1. The synthetic tests, under the tag:

```powershell
cd D:\Research\arc3\repo_prereg_v1_1
& D:\Research\arc3\brutus\.venv\Scripts\python.exe -W error scripts\test_analyze_v1.py
& D:\Research\arc3\brutus\.venv\Scripts\python.exe -W error scripts\test_analyze_v2.py
& D:\Research\arc3\brutus\.venv\Scripts\python.exe -W error scripts\test_analyze_g.py
& D:\Research\arc3\brutus\.venv\Scripts\python.exe -W error scripts\test_determinism_check.py
```

Expected: `Ran 5 tests ... OK`, `Ran 9 tests ... OK`, `Ran 2 tests ... OK` and `Ran 4 tests ... OK` (as of 27 Sep 2026 (g); the counts in PREREG v1.1 D11 at the tag govern).

E2. V1, instrument validity, suites B and C. It writes docs\tables\v1.md and docs\tables\v1.json:

```powershell
cd D:\Research\arc3\repo_prereg_v1_1
& D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\analyze_v1.py --runs "D:\Research\arc3\repo\runs\suites\minigrid\*\*\*.json" "D:\Research\arc3\repo\runs\suites\procgen\*\*\*.json" --out D:\Research\arc3\repo\docs\tables 2>&1 | Tee-Object -FilePath D:\Research\arc3\repo\runs\logs\analyze_v1.log
```

Expected shape: one line per (suite, condition, subset, assumption), then `wrote ...\docs\tables\v1.md, ...\docs\tables\v1.json`.
- Suite C center_on has only the "camera_distinct" subset, with verdict "reported, not tested" (D13).
- ARC V1 is not computed: docs/GROUND_TRUTH_arc_train.md does not exist.

E3. V2, predictive validity: suites B and C, with ARC E6 as the reported line. It writes docs\tables\v2.md and docs\tables\v2.json:

```powershell
cd D:\Research\arc3\repo_prereg_v1_1
& D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\analyze_v2.py --runs "D:\Research\arc3\repo\runs\suites\minigrid\*\*\*.json" "D:\Research\arc3\repo\runs\suites\procgen\*\*\*.json" "D:\Research\arc3\repo\runs\navrun_prereg_e6_arc_25x10.json" --workers 8 --out D:\Research\arc3\repo\docs\tables 2>&1 | Tee-Object -FilePath D:\Research\arc3\repo\runs\logs\analyze_v2.log
```

Expected shape:
- one line per (suite, condition, subset, agent). The subsets are:
  - suite B: "primary" (verdict), "primary, D9b included" (I1 only; reported) and "all games" (reported);
  - suite C center_off: "all" and "in_range" (verdicts);
  - suite C center_on: "camera_distinct" only (the five games of D13; reported, not tested).
- one suite line per subset;
- then `wrote ...\docs\tables\v2.md, ...\docs\tables\v2.json`.

E4. G, goal-identification cost. **After prereg-v1.2 and the replay; not part of this block's run** (PREREG v1.1 draft D15).
- G's rows come from a separate replay of N on every confirmatory (game, condition, seed), made after block D. The replay script (scripts/g_goal_cost.py) does not exist at the v1.1 tag.
- It is registered as prereg-v1.2 before any replay runs. Each replay must reproduce the confirmatory N row's action sequence and level log exactly, and the script reports that check per row.
- G is reported, not tested. Blocks D, E1–E3 and E5 do not wait for it.
- After the replay, the command has this form, with the G rows' location filled in by v1.2:

```powershell
cd D:\Research\arc3\repo_prereg_v1_1
& D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\analyze_g.py --runs "<G rows, location fixed by g_goal_cost.py>" --out D:\Research\arc3\repo\docs\tables 2>&1 | Tee-Object -FilePath D:\Research\arc3\repo\runs\logs\analyze_g.log
```

Expected shape: one line per (suite, condition, game), one summary line per suite, then `wrote ...\docs\tables\g.md, ...\docs\tables\g.json`.

E5. Paste the console output of D6, D7 and E1–E3. The tables are committed by RKM with the run files.
