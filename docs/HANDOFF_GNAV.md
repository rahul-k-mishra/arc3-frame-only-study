# G-NAV: built 24 Sep 2026, measured 24 Sep 2026, NOT shipped

All numbers below are from Rahul's runs on the lenovo (arc-agi 0.9.8, arcengine 0.9.3), 4 seeds
(1000-1003), 20,000 actions, hash_state and nav on the same seeds, files
navrun_train_full.json and navrun_heldout_full.json in D:\Research\arc3\kaggle_g.

## What it was
A navigation planner as a policy hook on the hash_state explorer (g_nav.py + g_agent.py hook
points; g_agent.py with hook=None is byte-equivalent to the original, g_nav_equiv.py 16/16).
Learn step vectors by pressing keys; plan over avatar positions on an optimistic lattice with
learned wall/deadly colours and expiring bump-blocks; explore to the nearest unvisited position;
at a level end record the colours stepped onto and plan straight to them on the next level.
Every assumption had a counter.

## Result
    TRAIN    (8 games)  hash_state 0.1840   nav 0.7012   REJECT by rule (m0r0 lost 0.25 level/seed, worth 0.0000)
                        the whole gain is tu93: L1 81/19 (explorer 287-432), L2 16-18/16 (explorer 85-217),
                        goal_confirmed on all 4 seeds; L3+ never won by nav (sentinel mirrors the player)
    HELD-OUT (17 games) hash_state 0.3329   nav 0.2419   levels/seed 11.2 -> 10.8
                        goal_confirmed: 0 of 17 games
                        sp80 alone: 1.6147 -> 0.0313 (nav walks 309-390 steps on L1, level needs key 5)

## Census of the 17 unseen games, from the counters (level 1, all seeds unless noted)
    no keys (click games; nav inert, identical to hash_state)   r11l s5i5 tn36
    no avatar found (cd82 despite the M1 probe finding a cursor)  cd82 sb26 su15
    avatar found, movement model wrong within 15 steps            cn04 re86 wa30   (wa30: 3 up / 4 down; re86: co-mover colour 11)
    walked to exhaustion, no level end                            bp35 g50t ka59 sk48 sp80
        goal recorded at L1 and falsified on retry (goal_reached_no_end): bp35 5/seed, ka59 4, sk48 6, sp80 6
    junk step vectors from one press (handed over within 2 steps) ar25 sc25 tr87
The assumption "one avatar reaches a place and the level ends" holds on 0 of 17 unseen games.

## Defects found in G-NAV (own bugs, each caught by a counter)
- floor voted as a wall (982 contradictions); fixed: wall = bumped and never walked on
- bump-blocks permanent, so a moving sentinel sealed the exit; fixed: blocks tied to colours, expire
- key written off after 3 blocked presses; fixed: retry from new positions, symmetric-direction guess
- 12-cell pusher throw (ls20) recorded as a bump; fixed: bump only if the avatar is still there
- avatar colours also in ls20's key panel; fixed: component of the avatar's shape
- sentinel colours absorbed into the avatar set when both moved together; fixed: own cells only
- sentinel's shift reported as an avatar misprediction; fixed: displacement from own cells
- goal read from the new level's frame; fixed: predicted destination in the old frame
- OPEN: single-press step learning accepts whatever moved (m0r0 [28,4]; lf52; ar25/sc25/tr87 junk).
  The M1 probe demanded 4 agreeing presses. Fixable on train; would not change the goal finding.
- OPEN: ar25 L1 won 4/4 nav seeds vs 0/8 hash_state (2,646-10,795 actions, worth 0.0001); cause unknown.
- OPEN: nav's presses change the explorer's RNG path after fallback, so the arms differ on every
  keyboard game even where nav did nothing useful (cd82 +0.119 is this).

## Why it is not pursued
The score is efficiency (100*(human/agent)^2 per level, level-index weighted). A planner buys
efficiency only with a goal. On the unseen games the goal is not "reach a colour", and nothing
in the frames says what it is. tu93 is the one game in 25 where it is. The mechanism list:
searching settings, click ranking, repeat_key, state abstraction, seeking rare objects, push
detection, per-game adaptation, goal reading, action budget, give-up (Kaggle 100k: identical
scores, 0.3615 vs 0.3329 at 20k), and now G-NAV.

## Kept from this session
g_decompose.py (score decomposition; dedupes duplicate runs; counts WON games' last level),
g_nav_run.py (A/B harness with scorecard per-level counts; works for any hook-based mechanism),
g_nav_equiv.py, build_kaggle_navrun.py (untested on Kaggle).
