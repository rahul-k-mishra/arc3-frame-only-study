# E6_RERUN.md — re-running the eight cut E6 rows (PREREG v1.1 draft D12), then the E6 census

Written 27 September 2026.
- The re-run is under the tag prereg-v1, in the worktree `D:\Research\arc3\repo_prereg_v1`, as E6 was.
- The ARC venv is `D:\Research\arc3\brutus\.venv`.

**No removal script is needed.** scripts/g_nav_run.py `--resume` does not keep a row that used fewer than 20,000 actions without winning; it runs it again (g_nav_run.py:130). The eight cut rows (D12) are therefore re-run and the other 492 are kept.

**Warning.** `--resume` writes back only the rows of the selection on the command line (g_nav_run.py:176-184, 206). **Use the full E6 selection below.** A command limited to re86 and sp80 would drop the other 492 rows from the file.

## Re-run

R1. Make sure the worktree's output file is the committed E6 file. Compare the two hashes. If the worktree file is missing or differs, copy the committed one into place:

```powershell
cd D:\Research\arc3\repo_prereg_v1\scripts
Get-FileHash .\navrun_prereg_e6_arc_25x10.json, D:\Research\arc3\repo\runs\navrun_prereg_e6_arc_25x10.json
Copy-Item D:\Research\arc3\repo\runs\navrun_prereg_e6_arc_25x10.json .\navrun_prereg_e6_arc_25x10.json -Force
```

R2. Re-run with the registered ARC cap of 3600 s. Expected first line: `resume: 492 completed rows kept ...; 8 rows that did not use the full budget and did not win ... will be run again`.

```powershell
cd D:\Research\arc3\repo_prereg_v1\scripts
D:\Research\arc3\brutus\.venv\Scripts\python.exe g_nav_run.py --games all --modes hash_state,nav --seeds 10 --budget 20000 --workers 8 --env-dir D:\Research\arc3\brutus\environment_files --tag prereg_e6_arc_25x10 --game-seconds 3600 --resume
```

R3. RKM copies the file back into the main repository's runs/ and commits it. Then run the identity checks again. Expected: (c) 0 rows with actions < 20000; (a) 250 of 250.

```powershell
cd D:\Research\arc3\repo
Copy-Item D:\Research\arc3\repo_prereg_v1\scripts\navrun_prereg_e6_arc_25x10.json .\runs\navrun_prereg_e6_arc_25x10.json -Force
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\e6_check.py
```

## E6 census (only after R3 shows 0 cut rows)

C1. The frozen scripts/g_census_table.py reads a held-out file and a train file and concatenates them. E6 has all 25 games in one file, so an empty list is passed as the train file; passing the E6 file twice would count every row twice. g_census_table.py in the main checkout is blob-identical to the tag (PREREG Section 5.4).

```powershell
cd D:\Research\arc3\repo
'[]' | Set-Content -Encoding ascii "$env:TEMP\empty_rows.json"
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\g_census_table.py --heldout runs\navrun_prereg_e6_arc_25x10.json --train "$env:TEMP\empty_rows.json" --out runs\census_e6.json --md docs\census_e6.md
```

**Caveat, stated before the run.** The frozen script's markdown text is fixed for census v2: its header names runs/navrun_v2_heldout.json and "train rows 2 seeds, 3,000 actions". The table numbers in docs/census_e6.md come from E6, but that fixed wording will be wrong. It cannot be edited. A short note file, docs/census_e6_NOTE.md, will state the true source (E6, 25 games × 10 seeds × 20,000, tag prereg-v1) next to it. runs/census_e6.json is the authoritative output.
