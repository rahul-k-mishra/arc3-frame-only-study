# census_e6_NOTE.md — the true source of docs/census_e6.md, and the labels that are wrong in it

Written 27 September 2026 (STATE.md amendment (f)). docs/E6_RERUN.md announced this note before the census was made.

## What docs/census_e6.md is

**Input.** runs/navrun_prereg_e6_arc_25x10.json, the E6 run:
- 25 games × {hash_state, nav} × **10 seeds (1000–1009) × 20,000 actions**, 500 rows;
- run under the tag prereg-v1 (commit 19f2a9f), with the eight nav rows cut at 900 s re-run under the 3600 s cap (PREREG.md v1.1 draft D12; commit b3509de);
- scripts/e6_check.py after the re-run: 250 of 250 hash_state rows identical to E2 except `seconds`, 68 of 68 nav rows identical to census v2 except `seconds`, 0 rows under 20,000 actions.

**How it was made.**
- scripts/g_census_table.py, blob 488feaca9c10985c4d0ff62791ceb4fa6fa6b9a8, one of the six files frozen by PREREG.md Section 5.4.
- The E6 file was passed as `--heldout` and an empty list as `--train`, so no row was counted twice (docs/E6_RERUN.md block C1).
- Outputs runs/census_e6.json and docs/census_e6.md, commit e75551a.

**Why this note exists.** The script is frozen, so it cannot be corrected to describe E6. Some of its text is written into the output from constants in the script, fixed when it was built for census v2. **The corrections are in this note, not in the script and not in docs/census_e6.md.** Where the two disagree, this note governs the wording, and runs/census_e6.json is the authoritative output for the numbers.

## Labels in docs/census_e6.md printed from the script's own defaults

Each label below is a fixed string in scripts/g_census_table.py, not a value computed from the input.

| # | where in docs/census_e6.md | printed text | source in the script | what is true for E6 |
|---|---|---|---|---|
| 1 | title | "Census v2: 25 public games, one row per game" | `markdown()`, g_census_table.py:273 | This is the **E6 census** (prereg-v1), not census v2. |
| 2 | first paragraph | "Generated … from runs/navrun_v2_heldout.json (17 held-out games, 4 seeds, 20,000 actions) and runs/navrun_v2_train_quick.json (8 train games, **2 seeds, 3,000 actions: below the 4-seed minimum, not a result; E6 replaces them**)" | g_census_table.py:275-279 | The only input was runs/navrun_prereg_e6_arc_25x10.json: **all 25 games, train and held-out alike, at 10 seeds × 20,000 actions**. The train rows are not 2 seeds × 3,000 actions; the "E6 replaces them" warning is itself satisfied by this file. The v2 files were not read. |
| 3 | category-rule paragraph | "The rule codifies the census already in CLAUDE.md and was written after reading it; it is not pre-registered." | g_census_table.py:289-290 | The origin is still true: the rule was written on 25 Sep 2026 after the CLAUDE.md census had been read. But for E6 the rule's code was **frozen by blob hash at prereg-v1 before E6 ran** (PREREG.md Sections 5.4 and 9.1). The categories are therefore produced by a rule fixed before the data. The rule was not validated against source; the categories are not part of V1. |
| 4 | section heading | "Held-out summary (17 games, 4 seeds)" | g_census_table.py:312 | The summary is computed over the 17 held-out games at **10 seeds** (the table's column "seeds x actions" reads 10 x 20000 on every row). |
| 5 | "CLAUDE.md agreement" line | "16 of 16 assigned games agree; sc25 was in no CLAUDE.md category, the rule gives 1-D walker" | the agreement is computed against the constant `CLAUDE_MD`, g_census_table.py:79-85 | The count is correct against that constant. The constant is a 25 Sep 2026 copy of the CLAUDE.md census that lists 16 held-out games and omits sc25. CLAUDE.md's census text names sc25 as a weak 1-D walker; the constant was not updated and cannot be now. See the table below. |
| 6 | footnote line | "\* source-informed (sources of tu93, dc22, ls20 read on 24 Sep 2026)" | g_census_table.py:280-281 | Unchanged from CLAUDE.md. docs/HELDOUT.md marks a different set (tu93, ls20, vc33, m0r0 "source read"). STATE.md (amendment of 27 Sep 2026) records the difference and does not resolve it; neither does this note. |

**Labels that are computed from the input, and are correct for E6:**
- the "seeds x actions" column (10 x 20000 on all 25 rows);
- keys tried and accepted;
- category;
- the L1 and goal columns;
- the category counts;
- the keyboard and moved-object counts;
- the sc25 note.

**Also fixed in the script, but outside docs/census_e6.md:**
- The console line "category counts, train (2 seeds x 3,000 actions)" (g_census_table.py:229-230) carries the same wrong train label as item 2.
- The `rule` field of runs/census_e6.json is copied from the script's docstring (g_census_table.py:262), including "it is not a pre-registered classifier" (item 3). Its `inputs` field is computed from the command line and names the E6 file and the empty list.
- This note was written from the script's source. runs/census_e6.json was not opened.

## The CLAUDE.md category table, with sc25 added

This is the constant of g_census_table.py:79-85, which the agreement check reads. It is completed here and not in the script:

| category | held-out games |
|---|---|
| no keys | r11l, s5i5, tn36 |
| no controllable object | cd82, sb26, su15 |
| 2-D lattice walker | cn04, ka59, re86, sp80, g50t |
| 1-D walker | bp35, sk48, **sc25 — added 27 Sep 2026 from E6** (the rule's result on 10 seeds; weak: only key 3 passed the agreeing-presses test, see the sc25 note in docs/census_e6.md) |
| key-controlled non-walker | ar25, wa30, tr87 |

With sc25 added, the agreement against this table is **17 of 17**. The frozen script prints 16 of 16 plus sc25 as unassigned; both statements describe the same result.

**What the categories are not.**
- The category rule is not one of the registered tests (V1, V2, V3, G).
- The categories are a description of ARC-AGI-3 behaviour under the frozen planner, on a development instance.
- They enter no claim of the method paper.
