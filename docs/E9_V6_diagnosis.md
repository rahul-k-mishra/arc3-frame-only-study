# E9 check V6 failure on ls20: diagnosis

Written 26 September 2026, after the author's registered E9 run reported V6 failing on all ten ls20
seeds ("arm O differs from arm N"). The registered run's file was not opened: runs/ is the
author's.

## Method

Runs are deterministic given the seed, so the ls20 arms were reproduced outside runs/, in the
assistant's scratch folder, with the code as committed:
- `g_nav_run.one`, the same function the registered run uses;
- modes `nav` (arm N) and `nav_oracle` (arm O);
- seeds 1000-1009, 20,000 actions, the registered configuration;
- arc-agi 0.9.8, arcengine 0.9.3, offline.

ls20 is a train game; no held-out game was played. Each pair of rows was compared leaf by leaf,
recursively through every nested field, including the full G-NAV report (`nav`). A 3,000-action,
2-seed reproduction was run first and gave the same result.

## Evidence

All 20 runs completed with 20,000 actions and no errors. Per seed, the leaves that differ between
arm N and arm O, excluding the wall-clock field `seconds`:

| seed | differing leaves | field | arm N | arm O |
|---|---|---|---|---|
| 1000 | 1 | `mode` | `nav` | `nav_oracle` |
| 1001 | 1 | `mode` | `nav` | `nav_oracle` |
| 1002 | 1 | `mode` | `nav` | `nav_oracle` |
| 1003 | 1 | `mode` | `nav` | `nav_oracle` |
| 1004 | 1 | `mode` | `nav` | `nav_oracle` |
| 1005 | 1 | `mode` | `nav` | `nav_oracle` |
| 1006 | 1 | `mode` | `nav` | `nav_oracle` |
| 1007 | 1 | `mode` | `nav` | `nav_oracle` |
| 1008 | 1 | `mode` | `nav` | `nav_oracle` |
| 1009 | 1 | `mode` | `nav` | `nav_oracle` |

With `mode` and `seconds` excluded, the two rows are identical on every seed. That covers the
score, levels completed, `card_levels`, `card_baseline`, `card_scores`, `level_log`, `diag`, and
the whole G-NAV report with its counters, learned step vectors and per-level records. **The arm-O
reports for ls20 contain no oracle field at all:** no `oracle_colours`, `oracle_targets`,
`oracle_confirmed`, `oracle_ambiguity` or `oracle_reached_no_end`, at any level or in the
counters.

## Which case it is

Neither case as posed. The single differing field, `mode`, is **not an oracle field**. It is the
arm label, written by the harness after the game has been played:

    scripts/g_nav_run.py line 78:    r["mode"], r["seed"] = mode, cfg_d["seed"]

No policy path reads it. It differs between any two arms by construction.

- **Not case (b):** nothing produced by play differs. The oracle is inert on ls20, as the protocol
  requires. No change to the E9 play code (g_nav.py, g_nav_run.py) is needed, and gate G2
  (e9_equiv.py) is unaffected; it compares plays that carry no `mode` label.
- **Not case (a) as stated:** no oracle-only recorded field differs; there are none in the ls20
  rows.

**The failure is a bug in scripts/e9_report.py:** V6 compared whole rows excluding only `seconds`
(its `strip` function), so it compared the arm labels and could never pass. The fix is for V6 to
compare the rows excluding the arm label `mode` as well as `seconds`, and to list per seed any
field that still differs.

The fields V6 now excludes:
- `mode`: the arm label, set by the harness after play;
- `seconds`: wall-clock time.

V1 (arm F against E2) is not affected: both sides carry the label `hash_state`.

## Limit of this diagnosis

It rests on reproduction, not on the registered file. The corrected V6, run by the author on the
registered file, is the confirmation: it prints every field that differs per seed and fails if
any field other than `mode` and `seconds` differs.
