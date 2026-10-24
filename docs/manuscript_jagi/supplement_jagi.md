---
title: |
  Supplement to:\
  A Frame-Only Census of Game Mechanics Built on\
  ARC-AGI-3 Failed a Preregistered Generality Test on MiniGrid/BabyAI and Procgen
lang: en-US
---

This supplement accompanies the article of the same title. The article cites it as "Supplement, Section S.n". It holds the full registered tables, the amendment trail, the exclusion lists, the provenance of every number and the hashes of the frozen files, and the exploratory ARC-AGI-3 line on the 17 held-out games. Everything here is copied from committed files of the repository, and every number in it is checked against the same list of values as the article.

## S.1 The Full V1 Table

Table S1 is docs/tables/v1.md (commit bb0f1a1), as written by the frozen analysis code at prereg-v1.1, with every row and cell unchanged. Agreement is the share of games where the census verdict equals the truth, and kappa is given only where both truth values have at least 3 games. The code's identifiers are kept. On MiniGrid/BabyAI, "macro" is absolute moves and "raw" primitive actions. On Procgen, "center_off" is the whole-level view and "center_on" the view centered on the agent, "in_range" is the nine games of the operating range, and "camera_distinct" the five games where the two views differ.

| suite | condition | subset | assumption | n | truth_holds | agreement | kappa | verdict |
|---------|-----------|------------------|------------|-----|-----------|----------|---------|------------------|
| minigrid | macro | all | A1 | 161 | 161 | 0.9876 |  | PASS |
| minigrid | macro | all | A2 | 161 | 161 | 0.9876 |  | PASS |
| minigrid | macro | all | A3 | 161 | 161 | 0.4286 |  | FAIL |
| minigrid | macro | all | A4 | 161 | 156 | 0.3354 | -0.0435 | FAIL |
| minigrid | macro | all | A5 | 161 | 36 | 0.2671 | -0.4125 | FAIL |
| minigrid | raw | all | A1 | 161 | 161 | 0.9379 |  | PASS |
| minigrid | raw | all | A2 | 161 | 161 | 0.4596 |  | FAIL |
| minigrid | raw | all | A3 | 161 | 0 | 0.5466 |  | FAIL |
| minigrid | raw | all | A4 | 161 | 156 | 0.0621 | 0.0021 | FAIL |
| minigrid | raw | all | A5 | 161 | 36 | 0.0994 | -0.3374 | FAIL |
| procgen | center_off | all | A1 | 14 | 14 | 0.9286 |  | PASS |
| procgen | center_off | all | A2 | 14 | 6 | 0.5714 | 0.2222 | FAIL |
| procgen | center_off | all | A3 | 14 | 2 | 0.5714 |  | FAIL |
| procgen | center_off | all | A4 | 14 | 13 | 0.0714 |  | FAIL |
| procgen | center_off | all | A5 | 14 | 6 | 0.0714 | -0.7843 | FAIL |
| procgen | center_off | in_range | A1 | 9 | 9 | 0.8889 |  | neither |
| procgen | center_off | in_range | A2 | 9 | 4 | 0.4444 | 0.0000 | FAIL |
| procgen | center_off | in_range | A3 | 9 | 2 | 0.4444 |  | FAIL |
| procgen | center_off | in_range | A4 | 9 | 8 | 0.1111 |  | FAIL |
| procgen | center_off | in_range | A5 | 9 | 2 | 0.1111 |  | FAIL |
| procgen | center_on | camera_distinct | A1 | 5 | 5 | 0.8000 |  | reported, not tested |
| procgen | center_on | camera_distinct | A2 | 5 | 2 | 0.8000 |  | reported, not tested |
| procgen | center_on | camera_distinct | A3 | 5 | 0 | 0.6000 |  | reported, not tested |
| procgen | center_on | camera_distinct | A4 | 5 | 5 | 0.0000 |  | reported, not tested |
| procgen | center_on | camera_distinct | A5 | 5 | 4 | 0.0000 |  | reported, not tested |

: Table S1. Test V1, every line, verbatim from docs/tables/v1.md.

## S.2 The Full V2 Tables

Table S2 is docs/tables/v2.md (commit bb0f1a1), as written by the frozen analysis code at prereg-v1.1. Its thirteen columns do not fit the page, so it is printed in two parts with the same rows in the same order: Table S2a gives each line and its verdict, Table S2b its statistics. No row, cell or value is changed. The agents are R, the explorer, N, the planner (instrument check), and I1, the graph-based explorer. Lines marked "primary" exclude the environments of Section S.4, "primary, D9b included" puts back the exclusions specific to I1, and "all games" includes every environment. auroc_B is the AUROC of the nuisance baseline, ci_low and ci_high the 95% bootstrap interval, and balanced_acc the balanced accuracy of the conjunctive prediction. Condition identifiers are as in Table S1; "native" is ARC-AGI-3. The two ARC-AGI-3 lines are computed over all 25 public games because of the defect described in the article (Section 3.10), and the "FAIL" printed on them has no registered meaning.

| suite | condition | subset | agent | role | n | positives | verdict |
|---------|-----------|----------------------|------|-----------------|-----|----------|----------------------|
| arc | native | all | N | reported | 25 | 14 | FAIL |
| arc | native | all | R | reported | 25 | 15 | FAIL |
| minigrid | macro | primary | I1 | evidence | 83 | 61 | neither |
| minigrid | macro | primary | N | instrument check | 112 | 100 | neither |
| minigrid | macro | primary | R | evidence | 112 | 101 | VOID |
| minigrid | macro | primary, D9b included | I1 | evidence | 112 | 61 | reported, not tested |
| minigrid | macro | all games | I1 | evidence | 161 | 61 | reported, not tested |
| minigrid | macro | all games | N | instrument check | 161 | 100 | reported, not tested |
| minigrid | macro | all games | R | evidence | 161 | 101 | reported, not tested |
| minigrid | raw | primary | I1 | evidence | 98 | 71 | FAIL |
| minigrid | raw | primary | N | instrument check | 155 | 130 | FAIL |
| minigrid | raw | primary | R | evidence | 155 | 126 | FAIL |
| minigrid | raw | primary, D9b included | I1 | evidence | 155 | 71 | reported, not tested |
| minigrid | raw | all games | I1 | evidence | 161 | 71 | reported, not tested |
| minigrid | raw | all games | N | instrument check | 161 | 130 | reported, not tested |
| minigrid | raw | all games | R | evidence | 161 | 126 | reported, not tested |
| procgen | center_off | all | I1 | evidence | 14 | 6 | FAIL |
| procgen | center_off | all | N | instrument check | 14 | 9 | neither |
| procgen | center_off | all | R | evidence | 14 | 9 | neither |
| procgen | center_off | in_range | I1 | evidence | 9 | 4 | neither |
| procgen | center_off | in_range | N | instrument check | 9 | 5 | neither |
| procgen | center_off | in_range | R | evidence | 9 | 5 | neither |
| procgen | center_on | camera_distinct | I1 | evidence | 5 | 3 | reported, not tested |
| procgen | center_on | camera_distinct | N | instrument check | 5 | 4 | reported, not tested |
| procgen | center_on | camera_distinct | R | evidence | 5 | 4 | reported, not tested |

: Table S2a. Test V2, the lines and their verdicts, from docs/tables/v2.md.

| suite | condition | subset | agent | auroc | ci_low | ci_high | balanced_acc | auroc_B |
|---------|-----------|----------------------|------|--------|--------|--------|------------|--------|
| arc | native | all | N | 0.4188 | 0.1978 | 0.6379 | 0.5357 | 0.5000 |
| arc | native | all | R | 0.4100 | 0.1850 | 0.6354 | 0.5333 | 0.5000 |
| minigrid | macro | primary | I1 | 0.7187 | 0.5902 | 0.8298 | 0.5838 | 0.8413 |
| minigrid | macro | primary | N | 0.6613 | 0.5049 | 0.7941 | 0.5700 | 0.8725 |
| minigrid | macro | primary | R | 0.6985 |  |  | 0.5693 | 0.8515 |
| minigrid | macro | primary, D9b included | I1 | 0.7719 | 0.6840 | 0.8529 | 0.5968 | 0.8734 |
| minigrid | macro | all games | I1 | 0.7517 | 0.6764 | 0.8223 | 0.6016 | 0.7562 |
| minigrid | macro | all games | N | 0.6352 | 0.5514 | 0.7114 | 0.5700 | 0.5752 |
| minigrid | macro | all games | R | 0.6434 | 0.5609 | 0.7208 | 0.5693 | 0.5589 |
| minigrid | raw | primary | I1 | 0.5370 | 0.4324 | 0.6410 | 0.5070 | 0.8534 |
| minigrid | raw | primary | N | 0.5255 | 0.4320 | 0.6156 | 0.5038 | 0.6202 |
| minigrid | raw | primary | R | 0.5224 | 0.4330 | 0.6096 | 0.5040 | 0.6561 |
| minigrid | raw | primary, D9b included | I1 | 0.6258 | 0.5405 | 0.7065 | 0.5070 | 0.8184 |
| minigrid | raw | all games | I1 | 0.6069 | 0.5235 | 0.6926 | 0.5070 | 0.8086 |
| minigrid | raw | all games | N | 0.4772 | 0.3829 | 0.5696 | 0.5038 | 0.6036 |
| minigrid | raw | all games | R | 0.4805 | 0.3919 | 0.5687 | 0.5040 | 0.6472 |
| procgen | center_off | all | I1 | 0.6458 | 0.3333 | 0.9445 | 0.5000 | 0.5104 |
| procgen | center_off | all | N | 0.7222 | 0.5000 | 0.9333 | 0.5000 | 0.5667 |
| procgen | center_off | all | R | 0.7222 | 0.5000 | 0.9333 | 0.5000 | 0.5667 |
| procgen | center_off | in_range | I1 | 0.8750 | 0.5000 | 1.0000 | 0.5000 | 0.4750 |
| procgen | center_off | in_range | N | 0.8000 | 0.5000 | 1.0000 | 0.5000 | 0.7000 |
| procgen | center_off | in_range | R | 0.8000 | 0.5000 | 1.0000 | 0.5000 | 0.7000 |
| procgen | center_on | camera_distinct | I1 | 0.3333 | 0.0000 | 1.0000 | 0.5000 | 0.6667 |
| procgen | center_on | camera_distinct | N | 0.3750 | 0.0000 | 0.8333 | 0.5000 | 1.0000 |
| procgen | center_on | camera_distinct | R | 0.3750 | 0.0000 | 0.8333 | 0.5000 | 1.0000 |

: Table S2b. Test V2, the statistics of the same lines, in the same order, from docs/tables/v2.md.

The analysis code also writes one verdict line per suite, given in Table S3 verbatim from docs/tables/v2.json (commit bb0f1a1).

| suite | condition | subset | suite line |
|----------|------------|----------------------|------------------------------------|
| arc | native | all | reported, not tested |
| minigrid | macro | primary | not failed (decided by I1 alone) |
| minigrid | macro | primary, D9b included | reported, not tested |
| minigrid | macro | all games | reported, not tested |
| minigrid | raw | primary | suite FAIL (decided by R and I1) |
| minigrid | raw | primary, D9b included | reported, not tested |
| minigrid | raw | all games | reported, not tested |
| procgen | center_off | all | not failed (decided by R and I1) |
| procgen | center_off | in_range | not failed (decided by R and I1) |
| procgen | center_on | camera_distinct | reported, not tested |

: Table S3. The V2 suite lines, verbatim from docs/tables/v2.json.

## S.3 The Amendment Trail, D1 to D16

Each entry is condensed from the diff sections of the registered protocol, where the full text, the file and line references and the dates are given. D1 to D15 were written on 27 September 2026 and registered at prereg-v1.1; D16 was written on 13 October 2026 and registered at prereg-v1.2.

D1, six actions at most. The frozen explorer presses key identifiers 1, 2, 3, 4, 5 and 7 only, so each suite is presented through a fixed key map: turn left, turn right, forward, pickup, drop and toggle under primitive MiniGrid/BabyAI actions; north, south, west, east, pickup and toggle under absolute moves; and up, down, left, right and two special actions on Procgen. An environment with fewer actions keeps only those it has.

D2, canvas placement. A MiniGrid/BabyAI grid sits one row down at the top left of a 64 × 64 canvas, and every other cell holds a reserved padding index, because the frozen code reads rows 1 to 62 only and anchors the frame at the top left.

D3, the Procgen border rows. The 64 × 64 Procgen frame fills the canvas, so the frozen code does not see its top and bottom pixel rows. This is recorded and not corrected.

D4, what a reset does. On MiniGrid/BabyAI a reset replays the current layout, and the layout advances only on a success. Procgen cannot restart a level, so a reset there takes no step and returns the current frame, and it still counts as an action.

D5, the wall-clock cap. The cap per suite is three times the longest pilot run, rounded up to a whole minute and computed by a script: 3300 s for MiniGrid/BabyAI and 7500 s for Procgen. Pilot runs were uncapped. A run cut by the cap is kept and reported as cut; none was cut.

D6, the runner. One registered script runs both suites, calls the author's agents exactly as the ARC-AGI-3 runner does, refuses to run if any frozen file differs from its registered hash, and writes one row per run.

D7, the boundary of I1. I1 runs unchanged behind an adapter that offers it key identifiers 1 to 5 only, shifts palette values that collide with its status-bar marker, and caps the level count it sees. It therefore lacks toggle on MiniGrid/BabyAI and the second special action on Procgen.

D8, infrastructure checks. The fidelity check, the pilot check, the Procgen camera check and the determinism check play random actions or read existing rows. None computes a census, an agent decision or a test statistic.

D9, exclusions for R and N. An environment is excluded from an agent's primary V2 line when, on every seed, success cannot be reached without an action missing from the agent's key map, either as the success action or as a precondition of every successful episode. The environment with no success at all is on every list. The lists hold 6 environments under primitive actions and 49 under absolute moves.

D9b, exclusions for I1. After the pilot showed I1 completing no level on a locked-door environment, the D9 rule was applied to I1's own key map, adding the 57 environments where success needs toggle on every seed. I1's lists hold 63 and 78 environments. Procgen has no exclusion, because no level end needs the second special action.

D10, seeding text. The v1 seeding text for MiniGrid/BabyAI is replaced by D4, and the runner's commands are added.

D11, the analysis code. The blob hashes of the analysis scripts at the tag are recorded; the scripts changed only to implement D9, D9b and D13. The synthetic tests passed, 20 of 20.

D12, the ARC-AGI-3 cap. The registered ARC-AGI-3 baseline had inherited an unregistered clock of 900 s per run, which cut eight runs short. The cap is 3600 s per run, registered at prereg-v1.1. The eight runs were repeated under the v1 tag, and the repeats replaced the cut rows.

D13, camera identity. Ten Procgen games set the camera option themselves at every level start, so the camera-on condition draws the same frames as the camera-off condition on the nine confirmatory games among them. The camera-on condition is reported on the five other games only and never tested; on the nine, the camera-on runs must equal the camera-off runs, which is checked as a matter of determinism.

D14, no adapter change after the pilot. The pilot showed no errors, no cut runs and the expected identity between conditions, and no adapter was changed.

D15, G by a registered replay. The rows for the goal-identification cost G were to come from a separate replay of N, registered as a further version before any replay, with every replay required to reproduce the confirmatory actions exactly.

D16, G is not measured. The replay of D15 is withdrawn after the outcome, because the instrument that G would accompany failed V1 on both suites. G remains defined in the protocol, and no value of it is reported.

## S.4 The Exclusion Lists

These lists are the registered constants in scripts/analyze_common.py at prereg-v1.1. The source reason for each identifier is given in the protocol under D9 and D9b.

B1. No success at all (1 environment; on every agent's list in both conditions):

MiniGrid-Playground-v0.

B2. Success needs "done" (5; on every list in both conditions; "done" is in no key map):

MiniGrid-GoToDoor-5x5-v0; MiniGrid-GoToDoor-6x6-v0; MiniGrid-GoToDoor-8x8-v0; MiniGrid-GoToObject-6x6-N2-v0; MiniGrid-GoToObject-8x8-N2-v0.

B3. Success is a drop (15; on the absolute-move lists of every agent):

MiniGrid-PutNear-6x6-N2-v0; MiniGrid-PutNear-8x8-N3-v0; BabyAI-PutNextLocal-v0; BabyAI-PutNextLocalS5N3-v0; BabyAI-PutNextLocalS6N4-v0; BabyAI-PutNextS4N1-v0; BabyAI-PutNextS5N1-v0; BabyAI-PutNextS5N2-v0; BabyAI-PutNextS5N2Carrying-v0; BabyAI-PutNextS6N3-v0; BabyAI-PutNextS6N3Carrying-v0; BabyAI-PutNextS7N4-v0; BabyAI-PutNextS7N4Carrying-v0; BabyAI-MoveTwoAcrossS5N2-v0; BabyAI-MoveTwoAcrossS8N9-v0.

B4. A drop is a precondition (28; on the absolute-move lists of every agent, and on I1's lists in both conditions as toggle preconditions):

MiniGrid-KeyCorridorS3R1-v0; MiniGrid-KeyCorridorS3R2-v0; MiniGrid-KeyCorridorS3R3-v0; MiniGrid-KeyCorridorS4R3-v0; MiniGrid-KeyCorridorS5R3-v0; MiniGrid-KeyCorridorS6R3-v0; MiniGrid-UnlockPickup-v0; MiniGrid-BlockedUnlockPickup-v0; MiniGrid-ObstructedMaze-1Dl-v0; MiniGrid-ObstructedMaze-1Dlh-v0; MiniGrid-ObstructedMaze-1Dlhb-v0; MiniGrid-ObstructedMaze-1Q-v1; MiniGrid-ObstructedMaze-2Dl-v0; MiniGrid-ObstructedMaze-2Dlh-v0; MiniGrid-ObstructedMaze-2Dlhb-v1; MiniGrid-ObstructedMaze-2Q-v1; MiniGrid-ObstructedMaze-Full-v1; BabyAI-KeyCorridor-v0; BabyAI-KeyCorridorS3R1-v0; BabyAI-KeyCorridorS3R2-v0; BabyAI-KeyCorridorS3R3-v0; BabyAI-KeyCorridorS4R3-v0; BabyAI-KeyCorridorS5R3-v0; BabyAI-KeyCorridorS6R3-v0; BabyAI-UnlockPickup-v0; BabyAI-UnlockPickupDist-v0; BabyAI-BlockedUnlockPickup-v0; BabyAI-UnlockToUnlock-v0.

B5. Success is a toggle (20; on I1's lists in both conditions):

MiniGrid-Unlock-v0; MiniGrid-RedBlueDoors-6x6-v0; MiniGrid-RedBlueDoors-8x8-v0; BabyAI-Open-v0; BabyAI-OpenDoor-v0; BabyAI-OpenDoorColor-v0; BabyAI-OpenDoorDebug-v0; BabyAI-OpenDoorLoc-v0; BabyAI-OpenDoorsOrderN2-v0; BabyAI-OpenDoorsOrderN2Debug-v0; BabyAI-OpenDoorsOrderN4-v0; BabyAI-OpenDoorsOrderN4Debug-v0; BabyAI-OpenRedBlueDoors-v0; BabyAI-OpenRedBlueDoorsDebug-v0; BabyAI-OpenRedDoor-v0; BabyAI-OpenTwoDoors-v0; BabyAI-Unlock-v0; BabyAI-UnlockLocal-v0; BabyAI-UnlockLocalDist-v0; BabyAI-KeyInBox-v0.

B6. A toggle is a precondition (these 9, plus the 28 of B4; on I1's lists in both conditions):

MiniGrid-DoorKey-5x5-v0; MiniGrid-DoorKey-6x6-v0; MiniGrid-DoorKey-16x16-v0; MiniGrid-LockedRoom-v0; MiniGrid-MultiRoom-N2-S4-v0; MiniGrid-MultiRoom-N4-S5-v1; MiniGrid-MultiRoom-N6-v0; BabyAI-GoToImpUnlock-v0; BabyAI-PickupAbove-v0.

| agent and condition | lists | excluded | primary games |
|---|---|---|---|
| R and N, primitive actions | B1, B2 | 6 | 155 |
| R and N, absolute moves | B1, B2, B3, B4 | 49 | 112 |
| I1, primitive actions | B1, B2, B4, B5, B6 | 63 | 98 |
| I1, absolute moves | B1, B2, B3, B4, B5, B6 | 78 | 83 |
| any agent, Procgen | none | 0 | 14 |

: Table S4. The exclusion lists per agent and condition.

## S.5 Provenance of the Numbers

Every number in the article and in this supplement is a value in docs/manuscript_jagi/numbers.json, which is a copy of the file that scripts/manuscript_numbers.py writes from committed files into docs/manuscript, made by the build described in docs/manuscript_jagi/BUILD.md. scripts/manuscript_check.py, run with the option --dir docs/manuscript_jagi, rejects any numeral in either file that is not one of those values. The only exceptions are the fields of the six reference entries added for this version, which were verified against the publisher's or arXiv's page and are recorded, entry by entry, in docs/manuscript_jagi/REFERENCES_CHECK_jagi.md; the check accepts such an entry only if it equals the recorded entry character for character. The years of in-text citations are also exempt when the cited work is in the reference list. Table S5 lists, for each class of number, the committed files its values come from and the commit that last changed each file. It is written by scripts/manuscript_numbers.py and copied here unchanged.

| number class | source files, each with the commit that last changed it |
|---|---|
| count | docs/EXPLORATORY_V1_DIAGNOSIS.md (7d9205e); docs/GROUND_TRUTH_minigrid.md (f12e529); docs/GROUND_TRUTH_procgen.md (8d209b3); docs/HELDOUT.md (4d2c02c); docs/PREREG.md (7d9205e); docs/STATE.md (at the commit tagged jagi-submission-v1); docs/manuscript_jagi/REFERENCES_CHECK_jagi.md (changed in the commit that carries this table); docs/tables/v1.json (bb0f1a1); docs/tables/v2.json (bb0f1a1); runs/checks/determinism_check.json (5ac65c1); runs/exploratory/v1_diagnosis.json (66e5606); runs/pilot_checks/pilot_check.json (cda7aa0); runs/pilot_checks/procgen_camera_check.json (cda7aa0); scripts/analyze_common.py (a96e49e) |
| rate (agreement, kappa, AUROC, interval bound, share) | docs/tables/v1.json (bb0f1a1); docs/tables/v2.json (bb0f1a1); runs/exploratory/v1_diagnosis.json (66e5606) |
| registered threshold | docs/PREREG.md (7d9205e) |
| constant, cap, seed or time | docs/PREREG.md (7d9205e); docs/manuscript_jagi/REFERENCES_CHECK_jagi.md (changed in the commit that carries this table); docs/tables/v2.json (bb0f1a1); runs/pilot_checks/pilot_check.json (cda7aa0); runs/pilot_checks/procgen_camera_check.json (cda7aa0) |
| commit or blob hash | docs/PREREG.md (7d9205e); docs/STATE.md (at the commit tagged jagi-submission-v1); git tag objects and git ls-tree (the tag objects themselves) |
| date | docs/HELDOUT.md (4d2c02c); docs/PREREG.md (7d9205e); docs/STATE.md (at the commit tagged jagi-submission-v1); docs/manuscript_jagi/REFERENCES_CHECK_jagi.md (changed in the commit that carries this table); git tag objects and git ls-tree (the tag objects themselves) |
| package version | docs/PREREG.md (7d9205e) |
| URL or DOI | docs/STATE.md (at the commit tagged jagi-submission-v1); docs/manuscript/REFERENCES_CHECK.md (6df6718); docs/manuscript/REVIEW_draft1.md (48931d2); docs/manuscript_jagi/REFERENCES_CHECK_jagi.md (changed in the commit that carries this table); docs/preprint/preprint.md (8bed48b); docs/preprint/references.bib (8bed48b) |
| reference field, verdict word or ORCID | docs/STATE.md (at the commit tagged jagi-submission-v1); docs/manuscript/REFERENCES_CHECK.md (6df6718); docs/manuscript_jagi/REFERENCES_CHECK_jagi.md (changed in the commit that carries this table); docs/preprint/preprint.md (8bed48b); docs/preprint/references.bib (8bed48b); docs/tables/v1.json (bb0f1a1); docs/tables/v2.json (bb0f1a1) |

: Table S5. Number classes and their sources.

The sources of the article's figures, tables and constants are these. Figures 1 and 2 are drawn by scripts/manuscript_figures.py from docs/tables/v1.json and docs/tables/v2.json; Figures 3 and 4 by the same script from runs/exploratory/v1_diagnosis.json, written by scripts/explore_v1_diagnosis.py at commit f43526a, which calls the frozen analysis functions unchanged. Tables 1 and 2 of the article are the verdict columns of Tables S1 and S2a; Table 3 is the outcome table of the registered protocol. The census constants are registered with their file, line and commit: LEARN_AGREE = 3 at scripts/g_nav.py:55, the 2:1 margin at scripts/g_nav.py:756, LEARN_MAX = 8 at scripts/g_nav.py:56 and the search limit of 40000 nodes at scripts/g_nav.py:54, all at commit ccc4d57, and the motion threshold of 2 cells at scripts/g_motion.py:20, commit 378345f. The ARC-AGI-3 split, with the move of dc22, is in docs/HELDOUT.md. The registered texts of the two OSF registrations are in the repository as docs/OSF_REGISTRATION_final.txt and docs/OSF_REGISTRATION_v1_1_final.txt. The agent I1 is in the directory external/rudakov_just_explore, which is not covered by the repository's license and keeps the upstream MIT notice of its own authors.

## S.6 Frozen Files and Analysis Scripts

The six census files were frozen at prereg-v1 and are identical at prereg-v1.1; the runner checked their blob hashes before every run. The analysis scripts are those at prereg-v1.1. Each hash below equals the output of git ls-tree at prereg-v1.1.

| file | role | git blob hash |
|---|---|---|
| scripts/g_agent.py | explorer R, frozen | 72585a4dbb926d4512ff9596f58118a176bb0646 |
| scripts/g_nav.py | planner N and census report, frozen | a8a7eb61e62a658c239b98e0224e3588a662d1a0 |
| scripts/g_motion.py | motion detector, frozen | 14018512a5c6b0efc81aed61c5466654d338be0b |
| scripts/g_control_probe.py | key set, frozen | d5ff2a4dc77b9e1148929e7db03fe99a9d2b0bf8 |
| scripts/g_nav_run.py | ARC-AGI-3 runner, frozen | 2cc0146a697e525e5873d4e29cb80f4ae8bd6297 |
| scripts/g_census_table.py | ARC-AGI-3 census table rule, frozen | 488feaca9c10985c4d0ff62791ceb4fa6fa6b9a8 |
| scripts/analyze_common.py | census rules, statistics, exclusion lists | caad22731807db78aff9c92c993a79a63f042ec3 |
| scripts/analyze_v1.py | test V1 | 515f44b0f007182172022272383de548e80d5a11 |
| scripts/analyze_v2.py | test V2 | 90a849c44e47addd8efdbfa579efdb16288edd50 |
| scripts/analyze_g.py | cost G (not run) | 46bf991d86400f0189d8898a7e068044d25c629a |
| scripts/determinism_check.py | determinism check | 4f98f6430e9221deb1a43f2313eb00f5ca676969 |

: Table S6. Git blob hashes of the frozen files and the analysis scripts.

## S.7 The Exploratory ARC-AGI-3 Line on the 17 Held-Out Games

This section is exploratory. Table S7 gives the V2 line on the 17 held-out ARC-AGI-3 games, computed after the outcome by the same frozen functions, from runs/exploratory/v1_diagnosis.json. It is reported and never tested. ARC-AGI-3 rows carry no adapter fields, so the baseline's features are constant there and its AUROC is 0.5000 by construction.

| agent | n | positives | AUROC | 95% interval | balanced accuracy | baseline AUROC |
|---|---|---|---|---|---|---|
| N | 17 | 8 | 0.3542 | [0.1041, 0.6346] | 0.5000 | 0.5000 |
| R | 17 | 9 | 0.3403 | [0.0909, 0.6213] | 0.5000 | 0.5000 |

: Table S7. Exploratory V2 line on the 17 held-out ARC-AGI-3 games. Reported, never tested.
