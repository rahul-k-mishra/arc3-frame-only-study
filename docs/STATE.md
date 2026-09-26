# STATE: the entry point for a fresh session (26 September 2026)

Read this first, then the file named on each line. Every number here comes from the file named
beside it; do not quote a number from memory. Game sets: train tu93 ls20 vc33 m0r0 ft09 lp85 lf52
dc22; held-out the other 17. tu93, dc22 and ls20 are source-informed.

## 1. What the project is now

- **Plan of record in the files:** `docs/TOG_PLAN_v2.md` Sections 0 and 9, and `CLAUDE.md`. They
  describe a 6-8 page ARC-only short paper for IEEE CoG or a workshop, venue chosen 9 October 2026.
  The ToG full paper was dropped because E1 found one INCONCLUSIVE external agent and E1c found no
  second one (`docs/E1_result.md`, `docs/E1c_search.md`).
- **Decision of 26 September 2026 (author):** strengthen the work into a **method paper across
  several benchmarks** rather than ship the ARC-only short paper.
  - This decision is **not yet written into `docs/TOG_PLAN_v2.md` or `CLAUDE.md`**, which still
    name the short paper. Recording it there, with the benchmarks chosen and a protocol for the
    method, is the first task of the next session (Section 5).
  - The plan already listed a second CPU benchmark (GVGAI learning track) as optional
    (`docs/TOG_PLAN_v2.md` Section 7).

## 2. Evidence base

HO = the 17 held-out games; games are the unit, seeds nested. Scripts are in `scripts/`.

| result | numbers | file / script |
|---|---|---|
| E4 ceiling | S(k,r,N) = 100·k(k+1)/(N(N+1))·min(1, r⁻²), validated against arc-agi 0.9.8's scorecard on 2,463 cases. Mean over 25 games, first level only: 3.52 at the human count, 0.14 at 5×, 0.0039 at 30×. tu93 level 1 at 356 vs 19 = level score 0.28, game score 0.0063 | `runs/ceiling.json` / `g_ceiling.py` |
| E2 reference | hash_state, HO, 10 seeds × 20,000 actions, 170 runs: M1 0.3274, M4 10.50 levels per seed, no level 3 won | `runs/navrun_e2_hash_25x10.json` / `g_nav_run.py` |
| E2 decomposition | HO: recorded 0.3274; AT HUMAN 3.0602 (9.35×); 2× 0.7651; 5× 0.1224; 82 level-1 and 23 level-2 wins, none later; median agent/human ratio 59.7 over the 105 won levels. Train contrast: AT HUMAN 8.0060, median ratio 19.4, 29 level-3+ wins (all tu93, 8 of 80 runs) | `runs/decompose_e2_hash_25x10_{heldout,train}.json` / `g_decompose.py` |
| E3 budget curve | hash_state, HO, seeds 1000-1003: M1 0.3328 / 0.3329 / 0.3329 / 0.3329 at 3k / 20k / 50k / 100k actions. M4 6.25 / 11.25 / 13.00 / 14.75. M3 = 0 throughout. Paired difference 100k − 20k: M1 0.0000 [0.0000, 0.0000], M4 +3.50 [0.50, 7.75]. More actions buy levels worth nothing. All checks passed, including nesting (600 checks). The 20k point is the 4-seed subset of E2 | `runs/e3_curve.json` / `e3_curve.py`; inputs `runs/navrun_e3_hash_25x4_{3k,50k,100k}.json` |
| E5 selection transfer | 6×4 matrix, fixed split: the train pick is repeat_key (HO 0.1464); hash_state is held-out-best (0.3329) but ranks 6 of 6 on train. Per-game oracle 0.3632, cross-fitted 0.2517. 10,000 random splits: pick is held-out-best 0.0113 vs chance 0.1668; pick HO 0.2258 vs random 0.2547; mean tau −0.4282. Exploratory 16-mechanism matrix: mean tau +0.3673 | `runs/split_transfer.json` / `g_split_transfer.py`; `docs/TOG_PLAN_v2.md` §4 |
| Census v2 | HO: 14 of 17 have keyboard input, 11 have an object the keys move; goal_confirmed 0 in every seed. Categories 3 / 3 / 5 / 3 / 3 (sc25 a weak 1-D walker); the rule codifies an earlier census and is not pre-registered | `runs/census_v2.json`, `docs/census_v2.md` / `g_census_table.py` |
| E1 Rudakov et al. | 10 seeds × 20,000 actions: **INCONCLUSIVE** by (ii), M2/M1 = 4.05 against > 5. M1 0.1750, M4 3.30, M3 0. **Confounds:** (1) ACTION7 absent from their action set (pressed on 5 HO games, accepted on ar25 and bp35); (2) their choose_action raises on most actions in most runs (HO median 17,342 of 20,000); (3) preview vs 2026 games and API. Their preview result is not contradicted | `runs/e1_decision.json`, `runs/e1_rudakov_lenovo_25x10_20k.json` / `e1_decide.py`, `e1_rudakov_adapter.py`; `docs/E1_result.md` |
| E1c | **Closed**, no admissible second agent. Prometheus rejected: direction priors measured on all 25 public games. Strongest non-LLM agents have no licence. Most high-scoring non-LLM notebooks run the game's own simulator | `docs/E1c_search.md`, `docs/E1c_prometheus_check.md` |
| E9 goal oracle | Verdict **INCONCLUSIVE**; all checks passed; V2 50 of 50 oracle-arm wins on an oracle colour (tu93), 0 not seen; V5 0 on every level. **tu93 MIXED:** levels 4.7 → 5.0 (dL +0.30); level 1 ratio 3.74 → 2.34, a 37% cut, not halved; game score 0.2442 → 1.0283. **dc22 NOT BINDING:** no level won by any arm. **ls20 NOT TESTABLE** (finding: predicate not a place). Two source-informed games; no general claim | `runs/e9_report.json`, `runs/navrun_e9_oracle_3x10.json` / `e9_report.py`, `g_nav.py` (nav_oracle); `docs/E9_protocol.md`, `docs/E9_goals.md`, `docs/E9_V6_diagnosis.md` |

## 3. Claims withdrawn or corrected

| claim as it stood | why it fell | where corrected |
|---|---|---|
| "100,000 vs 20,000 actions, 0.3615 vs 0.3329: coverage does not pay" | 0.3615 was mode base (2 seeds, 100k); 0.3329 was hash_state (4 seeds, 20k). Different mechanisms, so no budget effect was measured. E3 now measures it | `docs/TOG_PLAN_v2.md` RQ1, `CLAUDE.md`, `docs/HANDOFF_GNAV.md` note |
| "A per-game oracle over 20 mechanisms is worth 0.03" | 0.3632 was over the 6-mechanism matrix, and the 0.03 gap was in-sample. Cross-fitted, the oracle (0.2517) scores below hash_state (0.3329) | `docs/TOG_PLAN_v2.md` §4.2 |
| "Train pick held-out-best 3 of 17; selected 0.3329" | 0.3329 and "3 of 17" belong to hash_state, the held-out-best mechanism, which is last on train. Reporting it was selection on the held-out games | `docs/TOG_PLAN_v2.md` §4.2 |
| Selection is anti-informative / rankings reverse | Held only in the primary matrix (tau −0.43); the exploratory matrix gives +0.37. The phrase "anti-informative" does not appear in any document in the repo; the written form is §4.4's "rankings reverse is not general" | `docs/TOG_PLAN_v2.md` §4.4 |
| "1,088 held-out runs" | No file produces it; the files it could sum repeat the same deterministic runs (162 of 680 rows were duplicates). The reference is E2's 170 | `docs/TOG_PLAN_v2.md` RQ1, `CLAUDE.md` |
| "Median agent/human ratio 35-145" | Untraced range; retired | E2 decomposition: 59.7 |
| "ar25: hash_state 0/12" (and 0/8) | The same four deterministic runs were counted in three (or two) files. Correct: hash_state 0 of 4 seeds; G-NAV 8 of 8 across v1 and v2 | `docs/TOG_PLAN_v2.md` §10, `runs/decompose_ar25_three_files_heldout.json` |
| "None of the fourteen with a controllable object" | 14 is the keyboard count; 11 have an object the keys move. sc25 was missing from the categories | `docs/TOG_PLAN_v2.md` RQ3, `docs/census_v2.md` |
| tu93 example "level 1 at 356 vs 19 is worth 0.3 of 100" | 0.28 is the level score; the game score is 0.0063 (level weight 1 of 45) | `docs/TOG_PLAN_v2.md` §5.4, `runs/ceiling.json` |
| Old title "Why Frame-Only Agents Plateau"; "the barrier is goal inference" | Rudakov et al.'s preview result is a counterexample to a general plateau; E1 does not establish a family claim; E9 is INCONCLUSIVE | `docs/TOG_PLAN_v2.md` title, C3, C4, RQ4 |

## 4. Standing rules

Summarised from `CLAUDE.md`:
- **Selection and sources:** select on train games only; never open a held-out game's source;
  label tu93, dc22 and ls20 source-informed everywhere.
- **Seeds and evidence:** at least 4 seeds for any reported number and 10 for final tables, with
  games as the unit and seeds nested. Runs are deterministic given the seed, so a repeated seed
  adds nothing. Every number comes from a script in the repo run by the author, with output in
  `runs/`. Quote pasted output exactly.
- **Scripts:** parallel, resumable, ablate-format JSON, no silent overwrite.
- **Working method:** commands go in fenced PowerShell blocks. State what must be true, and how
  failure shows, before building anything; report failures and own bugs as prominently as
  successes. Nothing is submitted to Kaggle.
- **Writing:** plain prose, every step shown, every limit stated where the claim is made.
- **Protocols:** registered before runs; thresholds never changed after output exists; changes
  are dated amendments.
- **Files:** `runs/` is the author's (never stage, commit or open run outputs uninstructed).
  `docs/TOG_PLAN.md` and `audit/TOG_PLAN_RUTHLESS_AUDIT.md` are historical records and are never
  edited; corrections go in current documents only.

## 5. Decided, and open: do not re-decide

Decided (change only by a dated amendment in the named file):
- **E1 rule, precedence and outcome:** BREAKS over REPRODUCES; card-count clause first; Rudakov
  INCONCLUSIVE (`docs/TOG_PLAN_v2.md` §3.3, `docs/E1_phase2_protocol.md`, `docs/E1_result.md`).
- **E1c closed; Prometheus rejected** (`docs/TOG_PLAN_v2.md` §3.5, `docs/E1c_search.md`,
  `docs/E1c_prometheus_check.md`).
- **E5 specification and matrices:** 6×4 primary, 20×1 exploratory with truncated mechanisms
  excluded (`docs/TOG_PLAN_v2.md` §4).
- **E3 design and reporting** (`docs/TOG_PLAN_v2.md` §7 E3).
- **E9:**
  - colour oracle as the only verdict arm; ls20 NOT TESTABLE;
  - decisions D1-D4: V2 "ending not seen" passes and is excluded; eligible level = one seed;
    colours read at the first planner step; disclosure of the 1,500-action glimpse;
  - verdict INCONCLUSIVE (`docs/E9_protocol.md` §§1-8, `docs/E9_goals.md`).
- **E2 at 10 seeds is the reference for every comparison** (`docs/TOG_PLAN_v2.md` §8).

Open (decide only through a registered protocol, named here):
- **The method-paper direction:** which benchmarks, what the method is, and what replaces the
  ARC-only plan. There is no protocol file yet; update `docs/TOG_PLAN_v2.md` (or a successor plan)
  and `CLAUDE.md` first.
- **E9 optional arm P** (the coordinate oracle, outside the verdict): run or drop
  (`docs/E9_protocol.md` §3).
- **E6 census at 10 seeds on all 25 games**, with the category rule frozen by code hash before
  the run (`docs/TOG_PLAN_v2.md` §7).
- **E10 formal goal-identification cost:** hypothesis class G to be fixed and hashed before use
  (`docs/TOG_PLAN_v2.md` §6).
- **Venue:** the 9 October 2026 decision in `docs/TOG_PLAN_v2.md` §9 predates the method-paper
  decision and must be re-taken with it.
- **E1b (organiser templates, baseline only) and E7 (14B LLM cost):** optional
  (`docs/TOG_PLAN_v2.md` §7).

## Amendment 27 Sep 2026

Session-end amendment. The lines above are unchanged; where this section corrects one of them, this section governs.

**W0 commits.**
- 0c1bf9c "W0: add method-paper blueprint 1.0 and plan of record v3" added:
  - docs/TOG_PLAN_v3.md, the plan of record for the method paper;
  - docs/METHOD_BLUEPRINT.md draft 1, the protocol draft.
- 4d1d8a5 "W0: carry-over, plan archive, blueprint 1.1, reconciliation, frozen params" added:
  - docs/PLAN_MERGE_20260927.md: 21 items of the method-paper decision carried from TOG_PLAN_v2.md and CLAUDE.md into TOG_PLAN_v3.md Section 10;
  - TOG_PLAN_v3.md Section 2, listing every named run with its file;
  - METHOD_BLUEPRINT.md draft 1.1, with the three corrections of TOG_PLAN_v3.md Section 3;
  - docs/RECONCILE_20260927.md: the blueprint checked against this file;
  - docs/PREREG_PARAMS.md: the census constants, copied from source with file, line and commit;
  - the method-paper section of CLAUDE.md.
- The commit carrying this amendment adds docs/HELDOUT.md, closes the untraced values in RECONCILE_20260927.md, and brings METHOD_BLUEPRINT.md to draft 1.2.

**Archive moves (4d1d8a5, contents unchanged).**
- docs/TOG_PLAN.md → docs/archive/TOG_PLAN_v1.md
- docs/TOG_PLAN_v2.md → docs/archive/TOG_PLAN_v2.md

References to the old paths elsewhere in this file are read as the new paths.

**Where the decision is written.**
- The method-paper decision of 26 September 2026 is now written in docs/TOG_PLAN_v3.md (Sections 1, 3, 5 and 10) and in CLAUDE.md ("Current objective", "Rules that bind every task", "Open decisions").
- docs/METHOD_BLUEPRINT.md (draft 1.2) is the draft protocol. It is not yet registered: it becomes docs/PREREG.md v1 only at the prereg-v1 tag.

**Venue.**
- JAIR first, IEEE Transactions on Games second (TOG_PLAN_v3.md Section 1).
- The venue is pre-committed by outcome at gate G3 (TOG_PLAN_v3.md Section 6):
  - support → JAIR full article (research note as fallback if V4 is dropped);
  - partial → IEEE ToG;
  - refute → repository record, at most an arXiv note.

**The split file.**
- docs/HELDOUT.md was copied unchanged from D:\Research\arc3\brutus\HELDOUT.md.
- SHA-256: 8c07813ab01f5228a6af10f91771702dad0291f26b0f920892ef3a79763a122d
- Its train set and held-out set are identical to this file's header.
- Its notes on source reading differ from this file's "source-informed" list:
  - HELDOUT.md marks tu93, ls20, vc33 and m0r0 "source read, family built";
  - this file's header names tu93, dc22 and ls20.
- This amendment records the difference and does not resolve it.

**Stale lines listed in docs/RECONCILE_20260927.md, each with its correction.**
1. Section 1: the decision is "not yet written into docs/TOG_PLAN_v2.md or CLAUDE.md". Correction: it was written there in commits c1eea2c and 1af3a1e, and into docs/TOG_PLAN_v3.md in 0c1bf9c.
2. Sections 1 and 5 name docs/TOG_PLAN_v2.md and docs/TOG_PLAN.md. Correction: they are docs/archive/TOG_PLAN_v2.md and docs/archive/TOG_PLAN_v1.md.
3. Section 5 (Open): "There is no protocol file yet" for the method-paper direction. Correction: docs/METHOD_BLUEPRINT.md is its draft protocol, not yet registered.
4. Section 5 (Open): the venue is listed as open. Correction: TOG_PLAN_v3.md Section 1 records JAIR first and ToG second, pre-committed by outcome at gate G3. Which one is submitted to first remains open (TOG_PLAN_v3.md Section 8, item 4).
