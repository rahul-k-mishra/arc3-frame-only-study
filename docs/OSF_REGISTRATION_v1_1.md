# OSF_REGISTRATION_v1_1.md — text for the second OSF open-ended registration (protocol v1.1)

RKM pastes the text between the two rules into a new OSF open-ended registration, after creating the git tag `prereg-v1.1`.
- The commit hash is filled in from the output of `git rev-parse prereg-v1.1^{commit}`.
- The analysis blob hashes in item D11 are checked against `git ls-files -s` at that commit before pasting.
- This file names no person. The registration links only to the anonymised view of the first registration.

---

**Title:** Amendment v1.1 to the registered protocol "An assumption census for frame-only game agents" (amends OSF registration osf.io/2znhw)

**What this registration is.**
- It amends the open-ended registration osf.io/2znhw (protocol v1, git tag `prereg-v1`).
- The amended protocol is docs/PREREG.md v1.1 at git tag `prereg-v1.1`, commit `<fill: output of git rev-parse prereg-v1.1^{commit}>`, in the project repository (released with the paper; anonymised for review).
- Everything in v1 that is not changed below stands as registered.
- The changes were written after the tag `prereg-v1` and after a pilot on the registered pilot games only (six MiniGrid/BabyAI environments, two Procgen games). **No confirmatory MiniGrid, BabyAI or Procgen game had been played by any agent when this amendment was written.**
- The only earlier contact with confirmatory games was infrastructure checks that play random actions and compute no census, agent or test statistic (items D8 and D13).

**The claim (unchanged from v1).** A fixed, cheap, frame-only probe battery (the assumption census) together with a defined goal-identification cost G, with every parameter frozen on eight ARC-AGI-3 training games, (i) reports the ground-truth mechanics of unseen games in three suites at a registered accuracy, and (ii) predicts, before any agent is run, on which unseen games assumption-driven frame-only agents complete the first level.

**The changes, D1 to D14.**

**D1. Six actions at most.**
- The frozen census code presses only six action ids (ARC ids 1, 2, 3, 4, 5 and 7). Every suite is therefore presented through a key map of at most six actions:
  - MiniGrid/BabyAI, primitive-action condition: left, right, forward, pickup, drop, toggle. "done" is not offered.
  - MiniGrid/BabyAI, absolute-move condition: north, south, west, east, pickup, toggle. "drop" and "done" are not offered.
  - Procgen: up, down, left, right, special 1, special 2. The four diagonals, the no-op and specials 3–6 are not offered.
- An environment with fewer actions than the map offers only the ones it has. MiniGrid-Dynamic-Obstacles has three primitive actions, so its map has three entries in the primitive condition (left, right, forward) and four in the absolute-move condition (the four moves).

**D2. Placement on the canvas.** A MiniGrid/BabyAI grid is placed at the top left of a 64 × 64 canvas, one row down. The rest of the canvas holds a reserved padding value. The frozen code reads rows 1 to 62 only.

**D3. Procgen top and bottom rows.** The 64 × 64 Procgen frame fills the canvas, so the frozen code does not see its top and bottom pixel rows. This is recorded, not corrected.

**D4. What "reset" does.**
- On MiniGrid/BabyAI, a reset replays the current layout. Episode k uses the seed seed × 100,000 + k, and k advances only on a success.
- Procgen cannot restart a level, so a reset there takes no step and returns the current frame. It still counts as an action.
- The paper states: "The ARC RESET restarts the current level on ARC-AGI-3 and replays the current layout on MiniGrid/BabyAI, but is a no-op on Procgen, which cannot restart a level; on Procgen a failed level is followed by a new level."

**D5. Wall-clock cap per run.**
- The cap per suite is three times the longest pilot run's wall time in that suite, rounded up to a whole minute. It is computed by a script from the pilot rows. The pilot itself ran with no practical cap.
- Values:
  - MiniGrid/BabyAI: **3,300 s**. The longest pilot run was 1,081.6 s: MiniGrid-FourRooms-v0, primitive actions, the independent agent I1, seed 1003.
  - Procgen: **7,500 s**. The longest pilot run was 2,481.5 s: bigfish, center_agent off, I1, seed 1003.
- An infrastructure projection found no confirmatory (game, condition, agent) expected to exceed its cap. It adds the random-action speed of each game to the largest agent overhead seen in the pilot. The largest projections were 1,517.8 s and 2,550.0 s. This is not a guarantee.
- A run cut by the cap is kept, marked as cut, and reported as cut.

**D6. The runner.**
- One registered script runs both suites. It calls the agents exactly as the ARC runner does.
- It refuses to start if any of the six frozen census files differs from its registered hash.
- It writes one row per (suite, condition, agent, game, seed).

**D7. The independent agent I1 outside ARC.**
- I1 runs unchanged behind a boundary adapter. It sees the key map restricted to ids 1 to 5, because its code maps only five actions. Palette values that collide with its status-bar marker are shifted, and the level count it sees is capped at 254.
- As a consequence, I1 has no "toggle" in either MiniGrid/BabyAI condition and no "special 2" on Procgen.

**D8. Infrastructure checks.** Three scripts are registered as infrastructure checks. They play random actions or read existing rows, and they produce no census, agent decision or test statistic:
- a fidelity check: 200 random actions twice per game, to confirm determinism and measure speed;
- a pilot row check: inventory, cross-condition identity, wall time and the D5 projection;
- a Procgen camera check (see D13).

**D9. V2 exclusions for all agents.**
- The primary V2 analysis excludes a confirmatory environment for an agent when, on every seed, success cannot be reached without an action that is missing from that agent's key map.
- "Cannot be reached without" means that the action either triggers success itself or is a precondition of every successful episode. Examples of a precondition: a locked or closed door on every path to the target, or a carried key that must be put down before the target can be picked up (MiniGrid picks up only with empty hands).
- A secondary line reports V2 with these environments included, and is not tested.
- Environments that draw their instruction per seed (BabyAI LevelGen levels) stay in, as do levels whose target may lie in the agent's own room.
- For the author's agents (explorer R, planner N), from the environments' source code:
  - Primitive condition ("done" missing), 5 excluded: MiniGrid-GoToDoor-5x5-v0, -6x6-v0, -8x8-v0; MiniGrid-GoToObject-6x6-N2-v0, -8x8-N2-v0. Their success is a "done" beside the target.
  - Absolute-move condition ("drop" and "done" missing), 48 excluded:
    - the 5 above;
    - 15 whose success is a "drop": MiniGrid-PutNear-6x6-N2-v0, -8x8-N3-v0; BabyAI-PutNextLocal-v0, -PutNextLocalS5N3-v0, -PutNextLocalS6N4-v0, -PutNextS4N1-v0, -PutNextS5N1-v0, -PutNextS5N2-v0, -PutNextS5N2Carrying-v0, -PutNextS6N3-v0, -PutNextS6N3Carrying-v0, -PutNextS7N4-v0, -PutNextS7N4Carrying-v0, -MoveTwoAcrossS5N2-v0, -MoveTwoAcrossS8N9-v0;
    - 28 where the key used on a locked door must be put down before the target can be picked up: MiniGrid-KeyCorridorS3R1-v0, S3R2-v0, S3R3-v0, S4R3-v0, S5R3-v0, S6R3-v0; MiniGrid-UnlockPickup-v0; MiniGrid-BlockedUnlockPickup-v0; MiniGrid-ObstructedMaze-1Dl-v0, -1Dlh-v0, -1Dlhb-v0, -1Q-v1, -2Dl-v0, -2Dlh-v0, -2Dlhb-v1, -2Q-v1, -Full-v1; BabyAI-KeyCorridor-v0, -KeyCorridorS3R1-v0, S3R2-v0, S3R3-v0, S4R3-v0, S5R3-v0, S6R3-v0; BabyAI-UnlockPickup-v0, -UnlockPickupDist-v0, -BlockedUnlockPickup-v0, -UnlockToUnlock-v0.
  - Procgen: none.

**D9b. V2 exclusions for the independent agent I1** (decided after the pilot).
- The pilot showed the effect of I1's narrower key map. On MiniGrid-DoorKey-8x8-v0, I1 completed no level in any of its 20 runs, while R and N completed at least one level in every one of theirs.
- I1's key map stays as it is. The D9 rule is applied to I1's own map. I1's primary V2 line excludes the D9 environments of the condition and, in addition, every environment where success needs "toggle" on every seed. A secondary line reports I1 on R's game set, with these included, and is not tested.
- **"toggle" is the success action (20):** MiniGrid-Unlock-v0; MiniGrid-RedBlueDoors-6x6-v0, -8x8-v0; BabyAI-Open-v0, -OpenDoor-v0, -OpenDoorColor-v0, -OpenDoorDebug-v0, -OpenDoorLoc-v0, -OpenDoorsOrderN2-v0, -OpenDoorsOrderN2Debug-v0, -OpenDoorsOrderN4-v0, -OpenDoorsOrderN4Debug-v0, -OpenRedBlueDoors-v0, -OpenRedBlueDoorsDebug-v0, -OpenRedDoor-v0, -OpenTwoDoors-v0, -Unlock-v0, -UnlockLocal-v0, -UnlockLocalDist-v0, -KeyInBox-v0. Their success is opening a door, which only "toggle" does.
- **"toggle" is a precondition (37):**
  - MiniGrid-DoorKey-5x5-v0, -6x6-v0, -16x16-v0: the goal is beyond a locked door.
  - MiniGrid-LockedRoom-v0: the goal is in the locked room.
  - MiniGrid-MultiRoom-N2-S4-v0, -N4-S5-v1, -N6-v0: the goal is behind closed doors.
  - BabyAI-GoToImpUnlock-v0: the target is in a locked room.
  - BabyAI-PickupAbove-v0: the target is in another room, behind closed doors.
  - The 28 key-and-door environments listed under D9.
- **Counts of excluded environments in the primary line:**

| agent | primitive condition | absolute-move condition |
|---|---|---|
| R and N | 5 | 48 |
| I1 | 62 | 77 |

  The primary line then covers 156, 113, 99 and 84 of the 161 confirmatory environments respectively.
- **Procgen: no exclusion.** "Special 2" throws a star diagonally in ninja and fires backwards in starpilot; in every other confirmatory game it does nothing. No Procgen level end needs it.

**D10.** The v1 seeding text for MiniGrid/BabyAI is replaced by D4, and the protocol gains the runner's commands.

**D11. Analysis code.**
- The V2 script and its shared module changed only to implement D9 and D9b. Blob hashes at `prereg-v1.1`: analyze_v2.py `<fill: fd68354e2c5a20c9ddcad9713178a575c4355f1c unless changed before the tag>`, analyze_common.py `<fill: ddb807171046c0c10b5f7fd2839f4cbccff04600 unless changed before the tag>`. The V1 and G scripts are unchanged from v1, except as listed in D13 if implemented before the tag.
- Synthetic tests with hand-computed expected values cover the exclusions and the registered lists. All pass; they read no run file.

**D12. ARC-AGI-3 wall-clock cap.**
- The v1 ARC run (E6) inherited an unregistered 900 s per-run clock, which cut eight runs short.
- The registered ARC cap is 3,600 s per run. The eight runs were repeated under the v1 tag with that cap. Runs are deterministic given the seed, and the repeated runs replace the cut ones.
- After the repetition:
  - no run is below the 20,000-action budget;
  - the 250 explorer runs are identical to the earlier reference run except for timing;
  - the planner's 68 overlapping runs are identical to the earlier census run except for timing.

**D13. Procgen camera condition.**
- In the Procgen source (tag 0.10.7), ten games set the camera option themselves at every level start: bigfish, bossfight, chaser, leaper, plunder, starpilot always to "off"; dodgeball, heist, maze, miner to "off" in easy mode. For these games the secondary condition ("center_agent" on) draws exactly the same frames as the primary one. A camera check confirmed it: all 401 compared frames identical on those ten, and different from the first frame on the other six.
- **The secondary condition is therefore distinct only on caveflyer, climber, fruitbot, jumper and ninja** among the 14 confirmatory Procgen games. V1's and V2's secondary line is reported on those five.
- On the other nine the secondary runs are still made. They are required to equal the primary runs in every non-timing field, and this is recorded as a determinism check, not as evidence.
- These nine are exactly the games inside the registered operating range of the instrument (v1 Section 4). Within that range, the results are the same under both camera settings.

**D14. No adapter change after the pilot.** The pilot produced no errors and no cut runs. Cross-condition identity was as the source predicts, and runs were deterministic given the seed. No adapter was changed and the tile-size scaling rule was not used.

---
