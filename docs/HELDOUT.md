# The held-out set - the only honest proxy for the hidden games

## Why this exists

Every game BRUTUS wins outright was won by READING ITS SOURCE CODE: tu93's sentry, ls20's keys
and doors, vc33's reservoirs, m0r0's mirrored robots.  That is legitimate for the public set
and worth nothing on the leaderboard, where the 110 games have no source to read.

The evidence: the public 25-game mean went from 0.196 (v1) to about 24 (v10.1), a 120-fold
gain.  The leaderboard went from 0.32 to 0.38, a gain of 19%.  Almost nothing transferred.

So the public set is split in two, and the split is FROZEN here so it cannot be quietly moved
later:

## TRAIN - source reading allowed, already used

    tu93   the sentinel maze          (source read, family built)
    ls20   the key-and-door maze      (source read, family built)
    vc33   the reservoirs             (source read, family built)
    m0r0   the mirrored robots        (source read, family built)
    ft09   thumbnail/pattern game     (studied through the oracle)
    lp85   bracket search game        (studied through the oracle)
    lf52   partly studied (avatar deltas were read from it)
    dc22   MOVED FROM HELD-OUT on 21 Sep 2026, to debug BRUTUS-G milestone 2 (wall
           learning failed on it).  Moved BEFORE any detailed study, as the rule requires.

## HELD OUT - NEVER read the source of these, for any reason

    ar25  bp35  cd82  cn04  g50t  ka59  r11l  re86  s5i5
    sb26  sc25  sk48  sp80  su15  tn36  tr87  wa30

Seventeen games (eighteen until dc22 was moved to TRAIN on 21 Sep 2026).  Reading any of their source files - environment_files/<game>/*/ - destroys the
measurement permanently, because there is no way to un-know it.  If one of them ever has to be
opened, it moves to TRAIN in this file first, and the held-out number is recomputed without it.

## The rule for every future change

A change counts as progress only if the HELD-OUT number goes up.  The train number going up
means nothing for the leaderboard; that is exactly the mistake that produced 24 locally and
0.38 on Kaggle.

## How to measure

    python heldout_harness.py                 all eighteen, one process each
    python heldout_harness.py --workers 4     on a small machine
    python heldout_harness.py --games ar25,cd82 --max-actions 1000    a quick subset

It writes heldout_<tag>.json and prints a table plus one headline number.
