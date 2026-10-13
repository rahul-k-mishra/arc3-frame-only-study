# EXPLORATORY — V1 diagnosis (after gate G3)

**EXPLORATORY.**
- This document was written after gate G3 returned REFUTE (docs/STATE.md amendment (k)).
- It is not a registered analysis. It enters no claim, changes no registered file, and does not alter the G3 outcome.
- Nothing here is a proposed fix presented as a result.

**Sources.**
- Every number below comes from runs/exploratory/v1_diagnosis.json, written by scripts/explore_v1_diagnosis.py (commit f43526a) and run by RKM in the ARC venv from the main checkout.
- The tables were generated from that JSON with jq, not transcribed by hand. The console output holds the same numbers; it was not available when this document was written, so the JSON is the source cited.
- The census and V2 rules are the registered ones. The script imports `census_from_report`, `majority`, `truth_for` and `confirmatory` from scripts/analyze_common.py, and `game_table` and `v2_stats` from scripts/analyze_v2.py, all unchanged.

## 1. Consistency checks

*EXPLORATORY.*
- **Rows loaded** (N rows, confirmatory games): minigrid raw 1,610; minigrid macro 1,610; procgen center_off 140; procgen center_on 140. That is 161 × 10 and 14 × 10.
- **Stored census field against `census_from_report(nav)`, recomputed: 0 mismatches.** The per-seed verdicts below are therefore the ones the registered V1 analysis used.
- **ARC, all 25 games (Part 2, check):** N n = 25, positives 14, AUROC 0.4188, CI [0.1978, 0.6379], BA 0.5357, AUROC_B 0.5000; R n = 25, positives 15, AUROC 0.4100, CI [0.1850, 0.6354], BA 0.5333, AUROC_B 0.5000. **This reproduces the two ARC lines of docs/tables/v2.md (commit bb0f1a1) to four decimals.** So the 17-game line in Section 6 is computed by the same code on a subset.

## 2. Table 1 — confusion of the seed-majority census against the truth

*EXPLORATORY.*
- Columns are counts of games: truth holds or fails, against census holds (h), fails (f) or undetermined (u).
- The subsets are those of analyze_v1.py. Suite B uses the A3-raw truth for raw and the A3-macro truth for macro. Suite C center_on uses the five camera-distinct games only.
- The v1 verdicts of these lines are in docs/tables/v1.md.

| suite | condition | subset | assumption | n | truth h: census h | truth h: census f | truth h: census u | truth f: census h | truth f: census f | truth f: census u |
|---|---|---|---|---|---|---|---|---|---|---|
| minigrid | raw | all | A1 | 161 | 151 | 10 | 0 | 0 | 0 | 0 |
| minigrid | raw | all | A2 | 161 | 74 | 87 | 0 | 0 | 0 | 0 |
| minigrid | raw | all | A3 | 161 | 0 | 0 | 0 | 73 | 88 | 0 |
| minigrid | raw | all | A4 | 161 | 5 | 151 | 0 | 0 | 5 | 0 |
| minigrid | raw | all | A5 | 161 | 11 | 2 | 23 | 15 | 5 | 105 |
| minigrid | macro | all | A1 | 161 | 159 | 2 | 0 | 0 | 0 | 0 |
| minigrid | macro | all | A2 | 161 | 159 | 2 | 0 | 0 | 0 | 0 |
| minigrid | macro | all | A3 | 161 | 69 | 92 | 0 | 0 | 0 | 0 |
| minigrid | macro | all | A4 | 161 | 53 | 103 | 0 | 4 | 1 | 0 |
| minigrid | macro | all | A5 | 161 | 2 | 25 | 9 | 23 | 41 | 61 |
| procgen | center_off | all | A1 | 14 | 13 | 1 | 0 | 0 | 0 | 0 |
| procgen | center_off | all | A2 | 14 | 6 | 0 | 0 | 6 | 2 | 0 |
| procgen | center_off | all | A3 | 14 | 0 | 2 | 0 | 4 | 8 | 0 |
| procgen | center_off | all | A4 | 14 | 0 | 13 | 0 | 0 | 1 | 0 |
| procgen | center_off | all | A5 | 14 | 1 | 1 | 4 | 0 | 0 | 8 |
| procgen | center_off | in_range | A1 | 9 | 8 | 1 | 0 | 0 | 0 | 0 |
| procgen | center_off | in_range | A2 | 9 | 4 | 0 | 0 | 5 | 0 | 0 |
| procgen | center_off | in_range | A3 | 9 | 0 | 2 | 0 | 3 | 4 | 0 |
| procgen | center_off | in_range | A4 | 9 | 0 | 8 | 0 | 0 | 1 | 0 |
| procgen | center_off | in_range | A5 | 9 | 1 | 0 | 1 | 0 | 0 | 7 |
| procgen | center_on | camera_distinct | A1 | 5 | 4 | 1 | 0 | 0 | 0 | 0 |
| procgen | center_on | camera_distinct | A2 | 5 | 2 | 0 | 0 | 1 | 2 | 0 |
| procgen | center_on | camera_distinct | A3 | 5 | 0 | 0 | 0 | 2 | 3 | 0 |
| procgen | center_on | camera_distinct | A4 | 5 | 0 | 5 | 0 | 0 | 0 | 0 |
| procgen | center_on | camera_distinct | A5 | 5 | 0 | 0 | 4 | 0 | 0 | 1 |

## 3. Table 2 — disagreeing environments by family

*EXPLORATORY.*
- A game disagrees when its seed-majority census differs from its truth; "undetermined" always disagrees.
- Family is the id without its version and size or variant tokens (scripts/explore_v1_diagnosis.py, `family`). The per-game mapping, the ids, and the per-seed evidence are in the JSON (part1 → families → games).
- Families are listed by size, largest first.

| suite | condition | subset | assumption | disagreeing | families (count) |
|---|---|---|---|---|---|
| minigrid | raw | all | A1 | 10 | BabyAI-KeyCorridor 3; MiniGrid-KeyCorridor 3; MiniGrid-DoorKey 2; BabyAI-GoToObj 1; MiniGrid-LavaGap 1 |
| minigrid | raw | all | A2 | 87 | MiniGrid-ObstructedMaze 9; BabyAI-GoToLocal 8; BabyAI-PutNext 5; BabyAI-GoToObjMaze 4; BabyAI-KeyCorridor 4; BabyAI-OpenDoorsOrder 4; MiniGrid-KeyCorridor 4; MiniGrid-SimpleCrossing 4; BabyAI-FindObj 3; BabyAI-PutNextLocal 3; MiniGrid-DoorKey 3; MiniGrid-MultiRoom 3; BabyAI-GoToObj 2; BabyAI-OpenRedBlueDoors 2; BabyAI-PickupDist 2; MiniGrid-Empty 2; BabyAI-ActionObjDoor 1; BabyAI-BlockedUnlockPickup 1; BabyAI-GoToObjDoor 1; BabyAI-GoToRedBall 1; BabyAI-GoToRedBlueBall 1; BabyAI-GoToSeq 1; BabyAI-KeyInBox 1; BabyAI-MiniBossLevel 1; BabyAI-MoveTwoAcross 1; BabyAI-OpenRedDoor 1; BabyAI-OpenTwoDoors 1; BabyAI-PickupLoc 1; BabyAI-Synth 1; BabyAI-UnlockLocal 1; BabyAI-UnlockPickup 1; BabyAI-UnlockPickupDist 1; BabyAI-UnlockToUnlock 1; MiniGrid-BlockedUnlockPickup 1; MiniGrid-Fetch 1; MiniGrid-LavaGap 1; MiniGrid-LockedRoom 1; MiniGrid-Playground 1; MiniGrid-PutNear 1; MiniGrid-Unlock 1; MiniGrid-UnlockPickup 1 |
| minigrid | raw | all | A3 | 73 | MiniGrid-Memory 6; BabyAI-GoToLocal 5; BabyAI-OneRoom 4; MiniGrid-Dynamic-Obstacles 4; MiniGrid-LavaCrossing 4; BabyAI-KeyCorridor 3; BabyAI-PutNext 3; MiniGrid-Empty 3; MiniGrid-GoToDoor 3; BabyAI-GoToObjMaze 2; BabyAI-OpenDoor 2; MiniGrid-DistShift 2; MiniGrid-GoToObject 2; MiniGrid-KeyCorridor 2; MiniGrid-LavaGap 2; MiniGrid-RedBlueDoors 2; BabyAI-BossLevel 1; BabyAI-BossLevelNoUnlock 1; BabyAI-GoTo 1; BabyAI-GoToDoor 1; BabyAI-GoToImpUnlock 1; BabyAI-GoToObj 1; BabyAI-GoToObjMazeOpen 1; BabyAI-GoToOpen 1; BabyAI-GoToRedBallNoDists 1; BabyAI-GoToSeq 1; BabyAI-MoveTwoAcross 1; BabyAI-Open 1; BabyAI-OpenDoorColor 1; BabyAI-OpenDoorLoc 1; BabyAI-Pickup 1; BabyAI-PickupAbove 1; BabyAI-Synth 1; BabyAI-SynthLoc 1; BabyAI-SynthSeq 1; BabyAI-UnblockPickup 1; BabyAI-Unlock 1; BabyAI-UnlockLocalDist 1; MiniGrid-Fetch 1; MiniGrid-PutNear 1 |
| minigrid | raw | all | A4 | 151 | BabyAI-GoToLocal 13; MiniGrid-ObstructedMaze 9; BabyAI-PutNext 8; BabyAI-KeyCorridor 7; BabyAI-GoToObjMaze 6; MiniGrid-KeyCorridor 6; MiniGrid-Empty 5; MiniGrid-Memory 5; BabyAI-OneRoom 4; BabyAI-OpenDoorsOrder 4; MiniGrid-LavaCrossing 4; MiniGrid-SimpleCrossing 4; BabyAI-FindObj 3; BabyAI-GoToObj 3; BabyAI-PutNextLocal 3; MiniGrid-DoorKey 3; MiniGrid-LavaGap 3; MiniGrid-MultiRoom 3; BabyAI-GoToSeq 2; BabyAI-MoveTwoAcross 2; BabyAI-OpenDoor 2; BabyAI-OpenRedBlueDoors 2; BabyAI-PickupDist 2; BabyAI-Synth 2; MiniGrid-DistShift 2; MiniGrid-Fetch 2; MiniGrid-GoToDoor 2; MiniGrid-RedBlueDoors 2; BabyAI-ActionObjDoor 1; BabyAI-BlockedUnlockPickup 1; BabyAI-BossLevel 1; BabyAI-BossLevelNoUnlock 1; BabyAI-GoTo 1; BabyAI-GoToDoor 1; BabyAI-GoToImpUnlock 1; BabyAI-GoToObjDoor 1; BabyAI-GoToObjMazeOpen 1; BabyAI-GoToOpen 1; BabyAI-GoToRedBall 1; BabyAI-GoToRedBallNoDists 1; BabyAI-GoToRedBlueBall 1; BabyAI-KeyInBox 1; BabyAI-MiniBossLevel 1; BabyAI-Open 1; BabyAI-OpenDoorColor 1; BabyAI-OpenDoorLoc 1; BabyAI-OpenRedDoor 1; BabyAI-OpenTwoDoors 1; BabyAI-Pickup 1; BabyAI-PickupAbove 1; BabyAI-PickupLoc 1; BabyAI-SynthLoc 1; BabyAI-SynthSeq 1; BabyAI-UnblockPickup 1; BabyAI-Unlock 1; BabyAI-UnlockLocal 1; BabyAI-UnlockLocalDist 1; BabyAI-UnlockPickup 1; BabyAI-UnlockPickupDist 1; BabyAI-UnlockToUnlock 1; MiniGrid-BlockedUnlockPickup 1; MiniGrid-LockedRoom 1; MiniGrid-Playground 1; MiniGrid-PutNear 1; MiniGrid-Unlock 1; MiniGrid-UnlockPickup 1 |
| minigrid | raw | all | A5 | 145 | BabyAI-GoToLocal 13; MiniGrid-ObstructedMaze 9; BabyAI-PutNext 8; BabyAI-KeyCorridor 7; BabyAI-GoToObjMaze 6; MiniGrid-KeyCorridor 6; MiniGrid-Dynamic-Obstacles 5; BabyAI-OpenDoorsOrder 4; MiniGrid-LavaCrossing 4; MiniGrid-SimpleCrossing 4; BabyAI-FindObj 3; BabyAI-GoToObj 3; BabyAI-PutNextLocal 3; MiniGrid-DoorKey 3; MiniGrid-Empty 3; MiniGrid-GoToDoor 3; MiniGrid-MultiRoom 3; BabyAI-GoToSeq 2; BabyAI-MoveTwoAcross 2; BabyAI-OneRoom 2; BabyAI-OpenDoor 2; BabyAI-OpenRedBlueDoors 2; BabyAI-PickupDist 2; MiniGrid-Fetch 2; MiniGrid-GoToObject 2; MiniGrid-LavaGap 2; MiniGrid-PutNear 2; BabyAI-ActionObjDoor 1; BabyAI-BlockedUnlockPickup 1; BabyAI-BossLevel 1; BabyAI-BossLevelNoUnlock 1; BabyAI-GoTo 1; BabyAI-GoToDoor 1; BabyAI-GoToImpUnlock 1; BabyAI-GoToObjDoor 1; BabyAI-GoToObjMazeOpen 1; BabyAI-GoToOpen 1; BabyAI-GoToRedBall 1; BabyAI-GoToRedBallNoDists 1; BabyAI-GoToRedBlueBall 1; BabyAI-KeyInBox 1; BabyAI-MiniBossLevel 1; BabyAI-OpenDoorColor 1; BabyAI-OpenDoorLoc 1; BabyAI-OpenRedDoor 1; BabyAI-OpenTwoDoors 1; BabyAI-Pickup 1; BabyAI-PickupAbove 1; BabyAI-PickupLoc 1; BabyAI-Synth 1; BabyAI-SynthLoc 1; BabyAI-SynthSeq 1; BabyAI-UnblockPickup 1; BabyAI-Unlock 1; BabyAI-UnlockLocal 1; BabyAI-UnlockLocalDist 1; BabyAI-UnlockPickup 1; BabyAI-UnlockPickupDist 1; BabyAI-UnlockToUnlock 1; MiniGrid-BlockedUnlockPickup 1; MiniGrid-LockedRoom 1; MiniGrid-Playground 1; MiniGrid-RedBlueDoors 1; MiniGrid-Unlock 1; MiniGrid-UnlockPickup 1 |
| minigrid | macro | all | A1 | 2 | BabyAI-KeyCorridor 1; MiniGrid-KeyCorridor 1 |
| minigrid | macro | all | A2 | 2 | BabyAI-KeyCorridor 1; MiniGrid-KeyCorridor 1 |
| minigrid | macro | all | A3 | 92 | BabyAI-KeyCorridor 5; MiniGrid-ObstructedMaze 5; BabyAI-OneRoom 4; BabyAI-OpenDoorsOrder 4; BabyAI-PutNext 4; MiniGrid-KeyCorridor 4; BabyAI-GoToLocal 3; BabyAI-GoToObjMaze 3; MiniGrid-GoToDoor 3; BabyAI-FindObj 2; BabyAI-OpenDoor 2; BabyAI-OpenRedBlueDoors 2; BabyAI-PickupDist 2; MiniGrid-Fetch 2; MiniGrid-GoToObject 2; MiniGrid-PutNear 2; MiniGrid-RedBlueDoors 2; BabyAI-ActionObjDoor 1; BabyAI-BlockedUnlockPickup 1; BabyAI-BossLevel 1; BabyAI-BossLevelNoUnlock 1; BabyAI-GoTo 1; BabyAI-GoToDoor 1; BabyAI-GoToImpUnlock 1; BabyAI-GoToObj 1; BabyAI-GoToObjMazeOpen 1; BabyAI-GoToOpen 1; BabyAI-GoToRedBall 1; BabyAI-GoToRedBallNoDists 1; BabyAI-GoToRedBlueBall 1; BabyAI-GoToSeq 1; BabyAI-KeyInBox 1; BabyAI-MoveTwoAcross 1; BabyAI-Open 1; BabyAI-OpenDoorColor 1; BabyAI-OpenDoorLoc 1; BabyAI-OpenTwoDoors 1; BabyAI-Pickup 1; BabyAI-PickupAbove 1; BabyAI-PickupLoc 1; BabyAI-PutNextLocal 1; BabyAI-Synth 1; BabyAI-SynthLoc 1; BabyAI-SynthSeq 1; BabyAI-UnblockPickup 1; BabyAI-Unlock 1; BabyAI-UnlockLocal 1; BabyAI-UnlockLocalDist 1; BabyAI-UnlockToUnlock 1; MiniGrid-BlockedUnlockPickup 1; MiniGrid-DistShift 1; MiniGrid-DoorKey 1; MiniGrid-Empty 1; MiniGrid-LockedRoom 1; MiniGrid-MultiRoom 1; MiniGrid-Playground 1; MiniGrid-Unlock 1; MiniGrid-UnlockPickup 1 |
| minigrid | macro | all | A4 | 107 | BabyAI-KeyCorridor 6; BabyAI-GoToLocal 5; MiniGrid-KeyCorridor 5; MiniGrid-ObstructedMaze 5; BabyAI-OneRoom 4; BabyAI-OpenDoorsOrder 4; BabyAI-PutNext 4; MiniGrid-Dynamic-Obstacles 4; BabyAI-GoToObjMaze 3; MiniGrid-DoorKey 3; MiniGrid-GoToDoor 3; BabyAI-FindObj 2; BabyAI-OpenDoor 2; BabyAI-OpenRedBlueDoors 2; BabyAI-PickupDist 2; BabyAI-Synth 2; MiniGrid-Fetch 2; MiniGrid-GoToObject 2; MiniGrid-PutNear 2; MiniGrid-RedBlueDoors 2; MiniGrid-SimpleCrossing 2; BabyAI-ActionObjDoor 1; BabyAI-BlockedUnlockPickup 1; BabyAI-BossLevel 1; BabyAI-BossLevelNoUnlock 1; BabyAI-GoTo 1; BabyAI-GoToDoor 1; BabyAI-GoToImpUnlock 1; BabyAI-GoToObj 1; BabyAI-GoToObjMazeOpen 1; BabyAI-GoToOpen 1; BabyAI-GoToRedBall 1; BabyAI-GoToRedBallNoDists 1; BabyAI-GoToRedBlueBall 1; BabyAI-GoToSeq 1; BabyAI-KeyInBox 1; BabyAI-MiniBossLevel 1; BabyAI-MoveTwoAcross 1; BabyAI-Open 1; BabyAI-OpenDoorColor 1; BabyAI-OpenDoorLoc 1; BabyAI-OpenTwoDoors 1; BabyAI-Pickup 1; BabyAI-PickupAbove 1; BabyAI-PickupLoc 1; BabyAI-PutNextLocal 1; BabyAI-SynthLoc 1; BabyAI-SynthSeq 1; BabyAI-UnblockPickup 1; BabyAI-Unlock 1; BabyAI-UnlockLocal 1; BabyAI-UnlockLocalDist 1; BabyAI-UnlockToUnlock 1; MiniGrid-BlockedUnlockPickup 1; MiniGrid-DistShift 1; MiniGrid-Empty 1; MiniGrid-LavaCrossing 1; MiniGrid-LockedRoom 1; MiniGrid-MultiRoom 1; MiniGrid-Playground 1; MiniGrid-Unlock 1; MiniGrid-UnlockPickup 1 |
| minigrid | macro | all | A5 | 118 | BabyAI-GoToLocal 13; MiniGrid-ObstructedMaze 9; BabyAI-PutNext 8; BabyAI-KeyCorridor 7; MiniGrid-KeyCorridor 6; MiniGrid-Dynamic-Obstacles 5; MiniGrid-Empty 5; MiniGrid-LavaCrossing 4; MiniGrid-Memory 4; MiniGrid-SimpleCrossing 4; BabyAI-GoToObj 3; BabyAI-GoToObjMaze 3; BabyAI-PutNextLocal 3; MiniGrid-DoorKey 3; MiniGrid-GoToDoor 3; MiniGrid-LavaGap 3; MiniGrid-MultiRoom 3; BabyAI-MoveTwoAcross 2; BabyAI-OpenDoorsOrder 2; BabyAI-Synth 2; MiniGrid-DistShift 2; MiniGrid-GoToObject 2; MiniGrid-PutNear 2; BabyAI-BlockedUnlockPickup 1; BabyAI-BossLevel 1; BabyAI-BossLevelNoUnlock 1; BabyAI-GoToDoor 1; BabyAI-GoToImpUnlock 1; BabyAI-GoToObjDoor 1; BabyAI-GoToRedBall 1; BabyAI-GoToRedBallNoDists 1; BabyAI-GoToRedBlueBall 1; BabyAI-GoToSeq 1; BabyAI-MiniBossLevel 1; BabyAI-SynthSeq 1; BabyAI-UnlockPickup 1; BabyAI-UnlockPickupDist 1; BabyAI-UnlockToUnlock 1; MiniGrid-BlockedUnlockPickup 1; MiniGrid-LockedRoom 1; MiniGrid-Playground 1; MiniGrid-Unlock 1; MiniGrid-UnlockPickup 1 |
| procgen | center_off | all | A1 | 1 | plunder 1 |
| procgen | center_off | all | A2 | 6 | bossfight 1; dodgeball 1; miner 1; ninja 1; plunder 1; starpilot 1 |
| procgen | center_off | all | A3 | 6 | heist 1; leaper 1; maze 1; miner 1; ninja 1; plunder 1 |
| procgen | center_off | all | A4 | 13 | bossfight 1; caveflyer 1; chaser 1; climber 1; dodgeball 1; fruitbot 1; heist 1; jumper 1; leaper 1; maze 1; ninja 1; plunder 1; starpilot 1 |
| procgen | center_off | all | A5 | 13 | bossfight 1; caveflyer 1; chaser 1; climber 1; dodgeball 1; fruitbot 1; heist 1; jumper 1; leaper 1; miner 1; ninja 1; plunder 1; starpilot 1 |
| procgen | center_off | in_range | A1 | 1 | plunder 1 |
| procgen | center_off | in_range | A2 | 5 | bossfight 1; dodgeball 1; miner 1; plunder 1; starpilot 1 |
| procgen | center_off | in_range | A3 | 5 | heist 1; leaper 1; maze 1; miner 1; plunder 1 |
| procgen | center_off | in_range | A4 | 8 | bossfight 1; chaser 1; dodgeball 1; heist 1; leaper 1; maze 1; plunder 1; starpilot 1 |
| procgen | center_off | in_range | A5 | 8 | bossfight 1; chaser 1; dodgeball 1; heist 1; leaper 1; miner 1; plunder 1; starpilot 1 |
| procgen | center_on | camera_distinct | A1 | 1 | fruitbot 1 |
| procgen | center_on | camera_distinct | A2 | 1 | fruitbot 1 |
| procgen | center_on | camera_distinct | A3 | 2 | fruitbot 1; jumper 1 |
| procgen | center_on | camera_distinct | A4 | 5 | caveflyer 1; climber 1; fruitbot 1; jumper 1; ninja 1 |
| procgen | center_on | camera_distinct | A5 | 5 | caveflyer 1; climber 1; fruitbot 1; jumper 1; ninja 1 |

## 4. Table 3 — seeds that disagree with their game's majority

*EXPLORATORY.*
- Per game and assumption: the number of its 10 seeds whose per-seed census verdict differs from the game's majority verdict.
- The histogram reads "seeds dissenting: number of games".

| suite | condition | subset | assumption | games with any dissenting seed | largest | histogram |
|---|---|---|---|---|---|---|
| minigrid | raw | all | A1 | 108 of 161 | 5 | 0: 53, 1: 36, 2: 31, 3: 19, 4: 18, 5: 4 |
| minigrid | raw | all | A2 | 134 of 161 | 5 | 0: 27, 1: 21, 2: 13, 3: 32, 4: 49, 5: 19 |
| minigrid | raw | all | A3 | 135 of 161 | 5 | 0: 26, 1: 21, 2: 12, 3: 33, 4: 50, 5: 19 |
| minigrid | raw | all | A4 | 74 of 161 | 5 | 0: 87, 1: 30, 2: 21, 3: 14, 4: 7, 5: 2 |
| minigrid | raw | all | A5 | 103 of 161 | 6 | 0: 58, 1: 25, 2: 13, 3: 17, 4: 26, 5: 19, 6: 3 |
| minigrid | macro | all | A1 | 3 of 161 | 3 | 0: 158, 1: 2, 3: 1 |
| minigrid | macro | all | A2 | 6 of 161 | 3 | 0: 155, 1: 3, 2: 2, 3: 1 |
| minigrid | macro | all | A3 | 111 of 161 | 5 | 0: 50, 1: 22, 2: 29, 3: 25, 4: 26, 5: 9 |
| minigrid | macro | all | A4 | 111 of 161 | 5 | 0: 50, 1: 18, 2: 30, 3: 28, 4: 25, 5: 10 |
| minigrid | macro | all | A5 | 74 of 161 | 5 | 0: 87, 1: 19, 2: 16, 3: 15, 4: 11, 5: 13 |
| procgen | center_off | all | A1 | 5 of 14 | 4 | 0: 9, 1: 3, 3: 1, 4: 1 |
| procgen | center_off | all | A2 | 5 of 14 | 3 | 0: 9, 1: 2, 3: 3 |
| procgen | center_off | all | A3 | 12 of 14 | 5 | 0: 2, 1: 1, 2: 4, 3: 4, 4: 2, 5: 1 |
| procgen | center_off | all | A4 | 2 of 14 | 3 | 0: 12, 1: 1, 3: 1 |
| procgen | center_off | all | A5 | 3 of 14 | 5 | 0: 11, 1: 1, 4: 1, 5: 1 |
| procgen | center_off | in_range | A1 | 3 of 9 | 4 | 0: 6, 1: 2, 4: 1 |
| procgen | center_off | in_range | A2 | 2 of 9 | 3 | 0: 7, 1: 1, 3: 1 |
| procgen | center_off | in_range | A3 | 8 of 9 | 5 | 0: 1, 1: 1, 2: 3, 3: 2, 4: 1, 5: 1 |
| procgen | center_off | in_range | A4 | 0 of 9 | 0 | 0: 9 |
| procgen | center_off | in_range | A5 | 3 of 9 | 5 | 0: 6, 1: 1, 4: 1, 5: 1 |
| procgen | center_on | camera_distinct | A1 | 2 of 5 | 2 | 0: 3, 2: 2 |
| procgen | center_on | camera_distinct | A2 | 4 of 5 | 4 | 0: 1, 2: 1, 3: 1, 4: 2 |
| procgen | center_on | camera_distinct | A3 | 4 of 5 | 5 | 0: 1, 2: 3, 5: 1 |
| procgen | center_on | camera_distinct | A4 | 0 of 5 | 0 | 0: 5 |
| procgen | center_on | camera_distinct | A5 | 1 of 5 | 1 | 0: 4, 1: 1 |

## 5. What the counters show, per assumption

*EXPLORATORY.*
- Each paragraph cites the table it reads from. Per-seed counts come from the evidence fields in runs/exploratory/v1_diagnosis.json (part1 → families → games → per_seed → evidence), counted with jq.
- The registered census rules are in PREREG.md v1 Section 5.3, and the truth definitions in Section 7.
- These are readings of counters, not tested statements.

**A1 (input coupling).**
- The census agrees with the truth on 151 of 161 games under raw, 159 of 161 under macro, 13 of 14 on suite C center_off and 4 of 5 on center_on (Table 1).
- Every disagreement is truth holds, census fails. The census A1 rule fails when no key's learned shift is non-null, or when all tried keys' shifts are equal.
- The ten raw disagreements are BabyAI-KeyCorridor and MiniGrid-KeyCorridor S3R1–S3R3, MiniGrid-DoorKey-5x5 and -6x6, BabyAI-GoToObjS4 and MiniGrid-LavaGapS5 (Table 2). On these games most seeds failed the per-seed rule. The split was 10/0, 6/4 or 7/3 fails/holds; DoorKey-5x5 was 9/1 (JSON, A1 evidence).
- A1 is the one assumption whose V1 lines passed on every "all" subset (docs/tables/v1.md).

**A2 (one controlled object), raw.**
- 87 of 161 games are truth holds, census fails (Table 1). They spread over 41 families (Table 2).
- On their 870 seeds, the learner recorded:
  - keys 1 and 2 (left, right) as `no_move` on all 870;
  - key 3 (forward) as `accepted` on 208 and `no_move` on 662;
  - keys 4, 5 and 7 (pickup, drop, toggle) as `no_move` on all 870.
- The 662 seeds without an accepted forward have avatar_found 0, so the per-seed A2 verdict is "fails". The 208 with it have avatar_found 1 and "holds". Forward was accepted on a minority of seeds, and the majority verdict is "fails".
- A turn changes the agent's orientation but not its cell. The suite-B adapter maps the four orientations of the agent tile to one palette index (PREREG v1 Section 3.2), so a turn changes nothing in the grid the census sees and produces no learned shift. The census A2 rule needs an accepted key and a located avatar, so under raw it depended on forward alone. The counters do not say why forward was accepted on some seeds and not on others.
- Under macro, every move key displaces the agent, and A2 agrees on 159 of 161 games (Table 1). The two exceptions are BabyAI-KeyCorridorS3R1 and MiniGrid-KeyCorridorS3R1 (Table 2).

**A2, suite C.**
- Six games are truth fails, census holds: bossfight, dodgeball, miner, ninja, plunder and starpilot (Table 2). On each, avatar_found = 1 on 9 or 10 of 10 seeds (JSON, A2 evidence).
- The census A2 rule has no clause for other entities responding to the action. The pixel-physics truth definition does have one, and the six "fails" entries are justified in docs/GROUND_TRUTH_procgen.md's A2 column.

**A3 (lattice motion), macro.**
- 92 of 161 games are truth holds, census fails (Table 1). The macro truth holds on all 161.
- On the 920 seeds of the 92:
  - the learner accepted four step vectors on 850, three on 30, two on 13, one on 7, and none on 20 (the no_avatar seeds);
  - the per-seed verdict is "fails" on 775 seeds. On 755 of them the level-1 fallback is `mispredicted`; on the other 20 it is `no_avatar`;
  - the 145 "holds" seeds have the fallback `frontier_exhausted` or none.
- So the macro A3 failures come from the level-1 fallback "mispredicted", not from the learned step vectors. Four vectors were accepted on most seeds, though not on every seed.
- The census A3 rule reads whether the planner's model mispredicted during level 1. The truth definition asks whether each macro's unblocked displacement is constant. A "mispredicted" fallback records that the planner's forecast of the next frame failed; the counters do not say which part of the frame was mispredicted.

**A3, raw.**
- The truth is "fails" on all 161 games, because forward's displacement depends on facing. The census says "holds" on 73 (Table 1).
- The census A3 rule requires A2, and census A2 holds on 74 games under raw. On the 73, the majority of seeds also had a level-1 fallback that was not a model failure.
- One step vector per key, learned from the starting facing, does not reveal a facing dependence while turns record no shift (A2 above). This is a reading of the rule, not a measured cause.

**A3, suite C.**
- Four games are truth fails, census holds: heist, leaper, ninja and plunder. Their fallbacks were mostly `frontier_exhausted` or none.
- Two are truth holds, census fails: maze (7 of 10 seeds `mispredicted`) and miner (4 `mispredicted`, 2 `localise_failed`) (Table 2; JSON, A3 evidence).
- The truth fails A3 for velocity that persists across steps, for gravity and for jump arcs. The census A3 rule has no test of persistence. Its only failure route is the fallback.

**A4 (blocking by a fixed obstacle set).**
- The census A4 rule is conditional on A3: A4 holds iff A3 holds and wall_contradicted = 0. Where A3 fails, A4 fails with it.
- The seeds of the truth-holds, census-fails games split as follows (JSON, A4 evidence). A seed is counted on the "A3 route" if its level-1 fallback is `mispredicted`, `localise_failed` or `no_avatar`, otherwise on the "wall route" if wall_contradicted > 0. The remainder fail on neither route in that seed: they hold, but are outvoted.

| suite, condition | truth holds / census fails | seeds | A3 route | wall route | neither |
|---|---|---|---|---|---|
| B macro | 103 games | 1,030 | 807 (759 + 18 mispredicted, 28 no_avatar, 2 localise_failed) | 61 | 162 |
| B raw | 151 games | 1,510 | 844 (no_avatar) | 507 | 159 |
| C center_off | 13 games | 130 | 79 | 46 | 5 |
| C center_on (5) | 5 games | 50 | 33 | 17 | 0 |

- On B macro, 18 of the 807 A3-route seeds and both localise_failed seeds also had wall_contradicted > 0. On suite C, 56 of the 79 A3-route seeds had it too.
- **On suite C, wall_contradicted is > 0 on at least some seeds of every one of the 13 truth-holds games.** It is > 0 on all 10 seeds of dodgeball, heist, maze, plunder and starpilot. On the others it is > 0 on 9 (bossfight, jumper), 8 (chaser, climber), 7 (leaper), 5 (ninja) and 3 (caveflyer, fruitbot) of 10 seeds.
- The 14th game, miner, has truth fails and census fails.
- The truth definition counts as blocking any zero-displacement move explained by a fixed obstacle set, and records lethal contact under the termination predicate. The census counter wall_contradicted rises when the avatar moves as predicted through cells of a colour the planner had classified as a wall ("was a 'wall' until walked on now", scripts/g_nav.py:556-560). So it counts a colour that blocked at one time and not at another, as seen by the planner. The counters do not say whether that came from the environment's obstacles, from momentum, or from the planner's colour classification.

**A5 (place goal).**
- Census A5 holds iff goal_confirmed ≥ 1. It fails iff goal_reached_no_end ≥ 1 and goal_confirmed = 0. It is undetermined otherwise (PREREG v1 Section 5.3).
- **Undetermined.** Across the games whose majority is undetermined, the undetermined seeds split as follows:

| suite, condition | undetermined seeds | goal_recorded = 0 | recorded place, never targeted | targeted |
|---|---|---|---|---|
| macro | 663 | 620 | 42 | 1 |
| raw | 1,074 | 986 | 85 | 3 |
| suite C center_off | 110 | 70 | 34 | 6 |

  A goal place is recorded at a level end (docs/census_v2.md, "goal recorded"). On most undetermined seeds, then, no level end with a recorded place occurred, and the census had nothing to test.
- **Census "holds" where the truth says fails** (Table 1, column "truth f: census h"):
  - macro, 23 games: BabyAI-GoToLocal 13, BabyAI-GoToObj 3, BabyAI-GoToRedBall, -GoToRedBallNoDists, -GoToRedBlueBall, -GoToObjMaze, -GoToObjDoor and -GoToDoor 1 each, and MiniGrid-Unlock 1;
  - raw, 15 games: BabyAI-GoToLocal 5, BabyAI-OpenDoor 2, BabyAI-OneRoom 2, and MiniGrid-Fetch, BabyAI-OpenDoorLoc, -OpenDoorColor, -GoToRedBallNoDists, -GoToObj and -GoToDoor 1 each;
  - suite C: none.
- On the 23 macro games, 195 of 230 seeds confirmed a goal, and 193 of those also reached the place at least once without a level end (JSON, A5 evidence).
- The truth fails A5 for these families because success needs facing (GoTo, GoToObj, GoToDoor), a toggle (OpenDoor, Unlock) or a pickup (OneRoom, Fetch). The level end then happens at a cell beside or in front of the target, and the census, reading place only, recorded that cell as a goal.
- **Census "fails" where the truth says holds** (macro, 25 games): MiniGrid-Empty ×5, -LavaCrossing ×4, -Memory ×4, -SimpleCrossing ×4, -DoorKey-16x16 and -6x6, -LavaGapS6 and -S7, -MultiRoom-N2-S4 and -N4-S5, -DistShift1 and -2.
  - On their 250 seeds, 211 are "fails" (a recorded place reached without a level end, never confirmed), 14 "holds" and 25 "undetermined" (JSON, A5 evidence).
  - The counters do not say why the recorded place failed to end the level.
- **The negative κ.** The registered κ maps "undetermined" to the value opposite the truth (PREREG v1 Section 10). For κ, the cell "truth fails, predicted holds" is therefore:
  - macro: 23 census holds + 61 undetermined = 84;
  - raw: 15 + 105 = 120;
  - suite C: 0 + 8 = 8.
  - On suite C the negative κ (−0.7843) comes entirely from undetermined games. On suite B the GoTo- and OpenDoor-family "holds" are a minority of that cell: 23 of 84 on macro, 15 of 120 on raw.
  - On macro the 25 "truth holds, census fails" games add to the other off-diagonal cell.

## 6. The ARC V2 reported line on the 17 held-out games

*EXPLORATORY. Reported, never tested* (PREREG v1 Section 10: "ARC held-out: reported, not tested").
- This uses the same functions as Section 1's 25-game check, applied to the 17 held-out games of PREREG Section 8.
- N: n = 17, positives 8, AUROC 0.3542, CI [0.1041, 0.6346], BA 0.5000, AUROC_B 0.5000.
- R: n = 17, positives 9, AUROC 0.3403, CI [0.0909, 0.6213], BA 0.5000, AUROC_B 0.5000.
- ARC rows carry no adapter field, so the nuisance features are constant and AUROC_B is 0.5 by construction.
- The frozen table's 25-game lines (0.4188, 0.4100) include the 8 train games, three of which are source-informed. These 17-game values replace neither the frozen table nor anything in it.

## 7. Where the census probes and the truth definitions part company

*EXPLORATORY. A description of the mismatch, not a proposed fix presented as a result.*

For A2 under raw, A3, A4 and A5, the census probes and the truth-table definitions are not the same constructs.
- The census A2 test asks whether some key moves exactly one located object. Under primitive actions it rests on forward alone (Section 5, A2). The truth asks whether exactly one object's displacement is a deterministic function of the action, turns included.
- The census A3 test asks whether the planner's level-1 model mispredicted (Section 5, A3). The truth asks whether each action's unblocked displacement is constant regardless of position, facing and history.
- The census A4 test is conditional on A3 and counts contradicted wall predictions (Section 5, A4). The truth asks whether every zero-displacement move is explained by a fixed obstacle set.
- The census A5 test asks whether a cell recorded at a level end later ends a level again, and it is silent when no level ends (Section 5, A5). The truth asks whether success is triggered by entering a cell, with no facing or non-move action.
- In each case the census reads a by-product of one planner's run, and the truth reads the environment's source. Where the planner never reaches the state the test needs, the census is silent or reads a different event.
- A1, input coupling, is closest to being measured in the same terms on both sides. It is the only assumption with no FAIL line in docs/tables/v1.md (PASS on every "all" subset, "neither" on the suite-C in-range subset), though it too disagrees on some games (Table 1).
- This was not measured before the registered runs, and nothing above changes the V1 verdicts, the V2 verdicts or the G3 outcome (docs/STATE.md amendment (k)).
