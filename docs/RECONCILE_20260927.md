# RECONCILE_20260927.md — METHOD_BLUEPRINT.md against docs/STATE.md

Written 27 September 2026. docs/STATE.md was read in full (102 lines, commit 23b2f7a, unchanged since and not changed here). STATE.md is followed on every mismatch, and METHOD_BLUEPRINT.md is corrected. A value that STATE.md does not contain is marked "not in STATE.md" and is not filled from any other file.

## Table 1. METHOD_BLUEPRINT.md Section 12, item by item

Section 12's nine bullets are split where a bullet holds several values (1a, 1b, ...).

| # | item | value in STATE.md (section / run file) | value in METHOD_BLUEPRINT.md | verdict |
|---|---|---|---|---|
| 1a | v2 learner parameters | not in STATE.md | three agreeing presses, 2:1 margin over the runner-up, at most 10 px, at most 8 presses per key (2.2) | not in STATE.md. **Closed 27 Sep 2026: traced to a repository file** — docs/PREREG_PARAMS.md Section 1 (scripts/g_nav.py:55 LEARN_AGREE = 3, :756 2:1 margin, :57 MAX_STEP = 10, :56 LEARN_MAX = 8); cited in METHOD_BLUEPRINT.md Section 12 |
| 1b | script and commit of the v2 learner | not in STATE.md | "the script's commit hash" (2.2), no value given | not in STATE.md. **Closed 27 Sep 2026: traced** — scripts/g_nav.py, commit ccc4d57e26cdee73ea0eabdbd7d7fdfe847ed265 (docs/PREREG_PARAMS.md); cited in METHOD_BLUEPRINT.md Section 12 |
| 2a | held-out games with keyboard input | 14 of 17 (§2 Census v2; runs/census_v2.json) | 14 of 17 | match |
| 2b | held-out games with a moved object | 11 (§2 Census v2; runs/census_v2.json) | 11 | match |
| 2c | goal_confirmed | 0 in every seed (§2 Census v2; runs/census_v2.json) | 0 in every seed | match |
| 2d | sc25 placement | "sc25 a weak 1-D walker"; categories 3/3/5/3/3 (§2 Census v2; runs/census_v2.json, docs/census_v2.md) | "the sc25 placement" (no value) | match: no conflicting value. The blueprint names the item without a value; STATE.md gives it |
| 3a | E2 held-out M1 | 0.3274, 10 seeds × 20,000 actions, 170 runs (§2 E2 reference; runs/navrun_e2_hash_25x10.json) | 0.3274 (10 seeds) | match |
| 3b | E2 held-out M4 | 10.50 levels per seed (§2 E2 reference; runs/navrun_e2_hash_25x10.json) | 10.50 | match |
| 3c | E1 Rudakov M1 | 0.1750 (§2 E1; runs/e1_decision.json) | 0.1750 | match |
| 3d | E1 M2/M1 against the > 5 rule | 4.05 against > 5, INCONCLUSIVE by (ii) (§2 E1; runs/e1_decision.json) | 4.05 against the > 5 rule | match |
| 3e | the three E1 confounds | (1) ACTION7 absent from their action set; (2) their choose_action raises on most actions in most runs (HO median 17,342 of 20,000); (3) preview vs 2026 games and API (§2 E1; runs/e1_decision.json, runs/e1_rudakov_lenovo_25x10_20k.json, docs/E1_result.md) | "the three E1 confounds" (no list) | match: no conflicting value |
| 4a | best_hit vs chance | 0.0113 vs 0.1668 (§2 E5; runs/split_transfer.json) | 1.1% vs 16.7% | match (the same values, rounded to percent) |
| 4b | rank correlation | mean tau −0.4282 (§2 E5; runs/split_transfer.json) | −0.43 | match (rounded) |
| 4c | regret 0.092 / 0.206 | not in STATE.md (STATE.md gives "pick HO 0.2258 vs random 0.2547", which is a different quantity) | 0.092 / 0.206 | not in STATE.md. **Closed 27 Sep 2026: found in runs/** — runs/split_transfer.json, key primary.random.summary.regret_best.mean = 0.09230168980392157 (0.092) and key primary.random.summary.regret_oracle.mean = 0.20608736289215684 (0.206); cited in METHOD_BLUEPRINT.md Section 12. Kept |
| 4d | fixed split 0.1464 / 0.3329 / 0.3632 / 0.2517 | pick repeat_key HO 0.1464; hash_state 0.3329 (ranks 6 of 6 on train); per-game oracle 0.3632; cross-fitted 0.2517 (§2 E5; runs/split_transfer.json) | 0.1464 / 0.3329 / 0.3632 / 0.2517 | match |
| 4e | whether split-transfer numbers enter the method paper | not in STATE.md | proposal: ARC background only, one paragraph | not in STATE.md. **Closed 27 Sep 2026: traced to docs/TOG_PLAN_v3.md Section 2**, which limits the ARC background to one paragraph on the census and the E9 verdicts, "Nothing else"; the blueprint's proposal is replaced by that citation (none of these numbers enters the method paper) |
| 5a | ceiling 3.52 | 3.52: mean over 25 games, first level only, at the human count (§2 E4; runs/ceiling.json) | 3.52 | match |
| 5b | ceiling 10.57 | not in STATE.md (STATE.md's other ceiling values are 0.14 at 5× and 0.0039 at 30×) | 10.57 | not in STATE.md. **Closed 27 Sep 2026: found in runs/** — runs/ceiling.json, key means.all25.closed["2,1"] = 10.570562770562772 (first 2 levels at the human count; the same value under means.all25.whole["2,1"]); cited in METHOD_BLUEPRINT.md Section 12. Kept |
| 5c | ceiling 21.14 | not in STATE.md | 21.14 | not in STATE.md. **Closed 27 Sep 2026: found in runs/** — runs/ceiling.json, key means.all25.closed["3,1"] = 21.141125541125543 (first 3 levels at the human count; the same value under means.all25.whole["3,1"]); cited in METHOD_BLUEPRINT.md Section 12. Kept |
| 5d | ceiling out of the method paper | not in STATE.md | proposal: out | not in STATE.md. **Closed 27 Sep 2026: traced to docs/TOG_PLAN_v3.md Section 2** (Ceiling row: "ARC-scoring-specific, stays out of the method paper's tests"); cited in METHOD_BLUEPRINT.md Section 12 |
| 6a | train / held-out split | train tu93 ls20 vc33 m0r0 ft09 lp85 lf52 dc22; held-out the other 17; tu93, dc22, ls20 source-informed (§ header) | 8 train / 17 held-out per HELDOUT.md, dc22 moved to train | match on the sets. The HELDOUT.md / dc22 part, not in STATE.md, is **closed 27 Sep 2026: traced to docs/HELDOUT.md** (copied unchanged from D:\Research\arc3\brutus\HELDOUT.md, SHA-256 8c07813ab01f5228a6af10f91771702dad0291f26b0f920892ef3a79763a122d: "dc22 MOVED FROM HELD-OUT on 21 Sep 2026"; train and held-out sets identical to STATE.md's header); cited in METHOD_BLUEPRINT.md Section 12 |
| 6b | which ARC games count as train for parameter freezing | not in STATE.md (it lists the train set, not a parameter-freezing role) | the 8 train games | not in STATE.md. **Closed 27 Sep 2026: traced to docs/TOG_PLAN_v3.md Section 3** ("with every parameter frozen on the eight ARC-AGI-3 training games") and Section 2 (Split row); cited in METHOD_BLUEPRINT.md Section 12 |
| 7a | 0.28 s per-action admissibility threshold | not in STATE.md | 0.28 s | not in STATE.md. **Closed 27 Sep 2026: traced to docs/archive/TOG_PLAN_v2.md Section 3.1, A7** ("at most 0.28 s per action on the lenovo, measured over 2,000 actions on each of ft09 and tu93"); measured values for the E1 agent in docs/E1_phase2_protocol.md Section 1; cited in METHOD_BLUEPRINT.md Section 12 |
| 7b | E1 fidelity procedure as the admissibility rule | not in STATE.md | reused | not in STATE.md. **Closed 27 Sep 2026: traced to docs/archive/TOG_PLAN_v2.md Section 3.1, A6** (first 1,000 actions on ft09 and tu93 with a fixed seed identical under the agent's own loop and ours, else "adapter only, fidelity not checked"); results in docs/E1_phase2_protocol.md Section 1; cited in METHOD_BLUEPRINT.md Section 12 |
| 8a | ar25 counts | hash_state 0 of 4 seeds; G-NAV 8 of 8 across v1 and v2 (§3, row "ar25: hash_state 0/12"; runs/decompose_ar25_three_files_heldout.json) | 8/8 vs 0/4 | match |
| 8b | whether the ar25 discrepancy is explained | not in STATE.md (§3 corrects the counts only) | "if not, it is reported as unexplained" | not in STATE.md. **Closed 27 Sep 2026: traced** — docs/archive/TOG_PLAN_v2.md Section 10 ("The cause is unknown; it is reported as unexplained") and CLAUDE.md, State of the evidence ("UNEXPLAINED"): not explained; cited in METHOD_BLUEPRINT.md Section 12 |
| 9a | precedence: BREAKS before REPRODUCES | "BREAKS over REPRODUCES" (§5 Decided, E1 rule) | BREAKS before REPRODUCES | match |
| 9b | the clause evaluated first | "card-count clause first" (§5 Decided, E1 rule) | "missing-scorecard clause first" | mismatch, in name only (both mean rows without per-level scorecard counts give INCONCLUSIVE, docs/archive/TOG_PLAN_v2.md Section 3.3). Corrected: METHOD_BLUEPRINT.md Section 12 now uses STATE.md's name, "card-count clause". Also aligned in TOG_PLAN_v3.md Section 2 and CLAUDE.md rule 11 |

Mismatches found: 1 (9b, corrected). Values not in STATE.md: 1a, 1b, 4c, 4e, 5b, 5c, 5d, 6b, 7a, 7b, 8b, and the HELDOUT.md / dc22 part of 6a.

Amended 27 Sep 2026: every row that said "not in STATE.md" is closed by a citation to a repository file. No value was deleted: 0.092, 0.206, 10.57 and 21.14 were all found in runs/ (runs/split_transfer.json and runs/ceiling.json were opened read-only for this search only).

## Table 2. In STATE.md, but in neither METHOD_BLUEPRINT.md nor TOG_PLAN_v3.md (as they stood at 0c1bf9c)

"Mentioned" means the item is named with its result or rule. Actions taken in this commit are stated. Where the action says "listed here only", the item is not yet in the plan or the blueprint, and PREREG.md v1 or the manuscript must decide where it goes.

Runs, E1c and E3 to E9:

| # | item | STATE.md section | action |
|---|---|---|---|
| R1 | E1c details: Prometheus rejected (direction priors measured on all 25 public games); the strongest non-LLM agents have no licence; most high-scoring non-LLM notebooks run the game's own simulator (docs/E1c_search.md, docs/E1c_prometheus_check.md) | §2 E1c; §5 Decided | TOG_PLAN_v3.md §2 E1c row now names both docs and the Prometheus rejection. The simulator finding belongs in PRIOR_ART_KILL.md and related work; listed here only |
| R2 | E2 decomposition (runs/decompose_e2_hash_25x10_{heldout,train}.json; g_decompose.py) | §2 E2 decomposition | added to TOG_PLAN_v3.md §2 |
| R3 | E3 budget curve (runs/e3_curve.json; e3_curve.py; inputs runs/navrun_e3_hash_25x4_{3k,50k,100k}.json) | §2 E3 | added to TOG_PLAN_v3.md §2 (Step 0) |
| R4 | E4 ceiling's validation (2,463 cases against arc-agi 0.9.8's scorecard) and the tu93 example (level score 0.28, game score 0.0063) | §2 E4; §3 | listed here only; the ceiling is out of the method paper's tests (TOG_PLAN_v3.md §2) |
| R5 | E5 details beyond Table 1 (pick HO 0.2258 vs random 0.2547; exploratory tau +0.3673) | §2 E5 | listed here only |
| R6 | E1 run files runs/e1_decision.json and runs/e1_rudakov_lenovo_25x10_20k.json, M4 3.30, M3 0 | §2 E1 | files and M4 added to TOG_PLAN_v3.md §2. Also corrected there: "M2/M1 4.05 against the > 5 rule" stood in the E2 row; STATE.md gives it to E1 |
| R7 | E9 run files runs/e9_report.json and runs/navrun_e9_oracle_3x10.json; checks passed; V2 50 of 50; V5 0 on every level; tu93 figures | §2 E9 | files added to TOG_PLAN_v3.md §2. The verdicts and the tu93 figures are now in METHOD_BLUEPRINT.md §1. Corrected in TOG_PLAN_v3.md §1–2: ls20 "not expressible" is now "NOT TESTABLE" (STATE.md's label) |

Closed decisions:

| # | item | STATE.md section | action |
|---|---|---|---|
| D1 | E5 specification: 6×4 primary matrix, 20×1 exploratory with truncated mechanisms excluded | §5 Decided | matrices named in TOG_PLAN_v3.md §2; the specification is listed here only |
| D2 | E3 design and reporting (docs/archive/TOG_PLAN_v2.md §7 E3) | §5 Decided | listed here only |
| D3 | E9: colour oracle as the only verdict arm; decisions D1–D4 (V2 "ending not seen" excluded; eligible level = one seed; colours read at the first planner step; disclosure of the 1,500-action glimpse); verdict INCONCLUSIVE | §5 Decided | verdict carried. D1–D4 are listed here only; the E9 paragraph of the paper must state D4 |
| D4 | E2 at 10 seeds is the reference for every comparison | §5 Decided | added to the E2 row of TOG_PLAN_v3.md §2 |

Withdrawn or corrected claims. None may re-enter through the ARC background paragraph; each is listed here only:

| # | item | STATE.md section |
|---|---|---|
| W1 | "100,000 vs 20,000 actions, 0.3615 vs 0.3329: coverage does not pay" | §3 |
| W2 | "A per-game oracle over 20 mechanisms is worth 0.03" | §3 |
| W3 | "Train pick held-out-best 3 of 17; selected 0.3329" | §3 |
| W4 | "Selection is anti-informative / rankings reverse" | §3 |
| W5 | "1,088 held-out runs" | §3 |
| W6 | "Median agent/human ratio 35-145" (replaced by 59.7) | §3 |
| W7 | "ar25: hash_state 0/12" (and 0/8) | §3 |
| W8 | "None of the fourteen with a controllable object" (14 is the keyboard count; 11 have an object) | §3 |
| W9 | tu93 example "worth 0.3 of 100" (0.28 level score; 0.0063 game score) | §3 |
| W10 | Old title "Why Frame-Only Agents Plateau"; "the barrier is goal inference" | §3 |

Registered rules:

| # | item | STATE.md section | action |
|---|---|---|---|
| S1 | never open a held-out game's source; label tu93, dc22, ls20 source-informed everywhere | §4 | listed here only (in force through CLAUDE.md rule 1). PREREG.md must say how "source-informed" applies to the ARC train games inside the method paper |
| S2 | at least 4 seeds for any reported number, 10 for final tables | §4 | listed here only (CLAUDE.md rule 2); the blueprint uses 10 seeds |
| S3 | quote pasted output exactly | §4 | listed here only (CLAUDE.md rule 3) |
| S4 | scripts write ablate-format JSON; no silent overwrite | §4 | listed here only (CLAUDE.md rule 4). The blueprint's "one JSON per (suite, game, seed)" does not yet name the fields |
| S5 | state what must be true, and how failure shows, before building; report failures and own bugs as prominently as successes | §4 | listed here only (CLAUDE.md rule 6) |
| S6 | nothing is submitted to Kaggle | §4 | listed here only (CLAUDE.md rule 7) |
| S7 | protocols: thresholds never changed after output exists; changes are dated amendments | §4 | covered in substance by TOG_PLAN_v3.md §7 rules 2–3; "dated" is listed here only |
| S8 | runs/ is the author's: never stage, commit or open run outputs uninstructed | §4 | listed here only |
| S9 | docs/TOG_PLAN.md and audit/TOG_PLAN_RUTHLESS_AUDIT.md are historical records, never edited | §4 | the first is now docs/archive/TOG_PLAN_v1.md: moved, not edited. The STATE.md line still names the old path (STATE.md not changed, as instructed) |

Open items STATE.md lists (§5 Open), absent from both files at 0c1bf9c:

| # | item | STATE.md section | action |
|---|---|---|---|
| O1 | E9 optional arm P | §5 Open | carried: TOG_PLAN_v3.md §10 item 10, §8 item 8 |
| O2 | E6 census at 10 seeds on all 25 games, rule frozen by code hash | §5 Open | carried: TOG_PLAN_v3.md §10 item 8 |
| O3 | E10 formal goal-identification cost, hypothesis class fixed and hashed before use | §5 Open | carried: TOG_PLAN_v3.md §10 item 9 (mapped to G and V4) |
| O4 | E1b and E7, optional | §5 Open | carried: TOG_PLAN_v3.md §10 item 10 |

## Where STATE.md itself is out of date (recorded, not changed)

STATE.md was not edited, as instructed. These lines no longer match the repository. The next session-end STATE.md update (TOG_PLAN_v3.md §7 rule 5) is where they get fixed:

- §1 says the method-paper decision is "not yet written into docs/TOG_PLAN_v2.md or CLAUDE.md". It was written there in commits c1eea2c and 1af3a1e, and into TOG_PLAN_v3.md in 0c1bf9c.
- §1 and §5 name docs/TOG_PLAN_v2.md and docs/TOG_PLAN.md. They are now docs/archive/TOG_PLAN_v2.md and docs/archive/TOG_PLAN_v1.md.
- §5 Open says "There is no protocol file yet" for the method-paper direction. docs/METHOD_BLUEPRINT.md is its draft protocol (not yet registered).
- §5 Open lists the venue as open. TOG_PLAN_v3.md §1 records JAIR first and ToG second; only the order is still open (§8 item 4).
