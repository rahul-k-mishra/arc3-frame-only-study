# E9 goal table: the level-end predicates of tu93, dc22 and ls20

**Disclosure. These three games are source-informed.** Their environment source files were read on
24 September 2026 while debugging scripts/g_nav.py. They were read again on 26 September 2026 to
write this file, and only these three files were opened:

- `environment_files/tu93/0768757b/tu93.py`
- `environment_files/dc22/fdcac232/dc22.py`
- `environment_files/ls20/9607627b/ls20.py`

(under D:\Research\arc3\brutus\, the versions the runs use). **No held-out game's source has been
opened**, then or now. Nothing below concerns any held-out game.

This file records only the predicate each game checks to end a level. It records no strategies,
layouts, level contents, solutions or action sequences. One search on 26 September (dc22, for uses
of the target's name) displayed a few level-definition lines with sprite placements; they are not
recorded here and were not used. Sprite and variable names are the obfuscated identifiers in the
source, quoted as they are.

This is gate G1 of docs/E9_protocol.md. It is written before any E9 code.

## tu93

Where the level ends (`tu93.py`, lines 1236-1242, inside the step handler's third phase,
`elif self.kdkehgjrzq == 2:` at line 1235, reached after a move has resolved):

```
            if self.tnwgpjxbwe():
                ...
                ttauyadveo = self.current_level.get_sprites_by_tag("0017unajnymcki")
                onherbnfxo = self.current_level.get_sprites_by_tag("0015msvpvzxhqf")
                if ttauyadveo and all([any([libujymozt.x == exit.x and libujymozt.y == exit.y for exit in onherbnfxo]) for libujymozt in ttauyadveo]):
                    self.next_level()
```

What the tags are:
- `"0017unajnymcki"` is the object the arrow keys move. Line 1175:
  `libujymozt = self.current_level.get_sprites_by_tag("0017unajnymcki")[0]`, the sprite the key
  handler rotates and moves.
- `"0015msvpvzxhqf"` is the exit; the source names the loop variable `exit` (line 1241).

**Predicate:** the level ends when there is at least one sprite tagged `"0017unajnymcki"` and every
such sprite stands at exactly the position (x, y) of some sprite tagged `"0015msvpvzxhqf"`.
(Lines 1243-1244 are the losing branch: `self.lose()` when there is no such sprite or the step
counter is exhausted.)

**Expressible in G-NAV's language (reach a place): YES**, for any level with one controlled
sprite. The target is the exit sprite's position.
- Not checked: whether any level has more than one `"0017unajnymcki"` sprite, which would need
  every one of them on an exit. That is level content and was not read.
- The code controls sprite `[0]`, and G-NAV confirmed a colour goal on tu93 in all 4 seeds of its
  earlier runs (docs/HANDOFF_GNAV.md line 18), so levels 1-2 at least behave as single-object
  exits.
- If E9's validity check V2 (`oracle_reached_no_end = 0`) fails on a tu93 level, this is the first
  thing to check.

## dc22

Where the level ends (`dc22.py`, lines 10859-10860, at the end of a move action):

```
        if self.smxyfelexa():
            self.next_level()
```

The predicate (`dc22.py`, lines 10869-10870):

```
    def smxyfelexa(self) -> bool:
        return self.qnnpcoyzd.x == self.hfuqkxulm.x and self.qnnpcoyzd.y == self.hfuqkxulm.y
```

What the two sprites are:
- `self.qnnpcoyzd` is the object the move actions move: line 10844,
  `collisions = self.try_move_sprite(self.qnnpcoyzd, ...)`. It is the first sprite tagged `"jfva"`
  (lines 9996 and 10497: `self.qnnpcoyzd = self.current_level.get_sprites_by_tag("jfva")[0]`).
- `self.hfuqkxulm` is the first sprite tagged `"goknoi"` (lines 9995 and 10496:
  `self.hfuqkxulm = self.current_level.get_sprites_by_tag("goknoi")[0]`), set when a level loads.
  No play-time code sets its position; the only placements of `"goknoi"` sprites are in the level
  definitions, which are not recorded here.

**Predicate:** the level ends when the controlled sprite (tag `"jfva"`) stands at exactly the
position (x, y) of the target sprite (first sprite tagged `"goknoi"`).

**Expressible in G-NAV's language (reach a place): YES.** The target is the `"goknoi"` sprite's
position.

The same move handler contains other mechanics (lines 10849-10857: stepping onto a sprite tagged
`"piyqze"` makes matching `"buezna"` sprites intangible). These affect whether the target can be
reached, which is passability, not the level-end predicate. Under the E9 protocol the oracle
supplies only the place, and passability stays G-NAV's own.

## ls20

Where the level ends (`ls20.py`, lines 1956-1957, at the end of a move action):

```
        if self.pbznecvnfr():
            self.next_level()
```

The predicate (`ls20.py`, lines 2020-2038, abridged: the body of the `if` only records the target
as done and removes its sprites):

```
    def pbznecvnfr(self) -> bool:
        for i, spssohsnbq in enumerate(self.plrpelhym):
            if not self.lvrnuajbl[i] and self.gudziatsk.x == spssohsnbq.x and (self.gudziatsk.y == spssohsnbq.y) and self.bejndxqqzf(i):
                self.lvrnuajbl[i] = True
                ...
        for i in range(len(self.lvrnuajbl)):
            if not self.lvrnuajbl[i]:
                return False
        return True
```

and the extra condition (`ls20.py`, lines 2017-2018):

```
    def bejndxqqzf(self, wyhfvzxukh: int) -> bool:
        return self.fwckfzsyc == self.ldxlnycps[wyhfvzxukh] and self.hiaauhahz == self.yjdexjsoa[wyhfvzxukh] and (self.cklxociuu == self.ehwheiwsk[wyhfvzxukh])
```

What the parts are:
- `self.gudziatsk` is the object the arrow keys move (line 1944:
  `self.gudziatsk.set_position(juldcpkjse, ullicjtklz)` after the move).
- `self.plrpelhym` is a list of targets, one or more per level.
- The required values per target come from the level's data fields (lines 1802-1813):
  `"kvynsvxbpi"` → `ldxlnycps`, `"GoalRotation"` → `ehwheiwsk`, `"GoalColor"` → `yjdexjsoa`.
- The object's own state variables start from the level's `"StartShape"`, `"StartColor"` and
  `"StartRotation"` (lines 1995-1997) and **change during play**:
  - line 1872: `self.fwckfzsyc = (self.fwckfzsyc + 1) % len(self.ijessuuig)`
  - line 1880: `self.hiaauhahz = lwphyolnjb`
  - line 1884: `self.cklxociuu = (self.cklxociuu + 1) % 4`

**Predicate:** the level ends when every target of the level has been completed. A target is
completed when the controlled object stands at exactly its position **and**, at that moment, the
object's three state variables (a shape index, a colour index and a rotation index) equal that
target's required values.

**Expressible in G-NAV's language (reach a place): NO.** The predicate needs the object's state
(shape, colour, rotation) to match per target, and that state changes during play. With more than
one target it also needs every target completed. A place alone does not express it, and the E9
protocol does not allow a sequence of sub-goals.

This holds for every ls20 level as a matter of the predicate. Whether a particular level's start
state already equals its targets' required state is level content (the values of `"StartShape"`,
`"StartColor"`, `"StartRotation"` and the goal fields); it was not read and is not recorded. E9
therefore treats ls20 as **NOT TESTABLE** at every level, as the protocol provides.

## Summary for E9

| game | level-end predicate (source lines) | reach a place? | E9 status |
|---|---|---|---|
| tu93 | every arrow-controlled sprite (tag `0017unajnymcki`) at the position of an exit sprite (tag `0015msvpvzxhqf`) (1236-1242; controlled sprite, 1175) | yes (single controlled sprite) | testable |
| dc22 | controlled sprite (tag `jfva`) at the position of the target sprite (first tag `goknoi`) (10859-10860, 10869-10870; tags, 9995-9996) | yes | testable |
| ls20 | every target reached by the controlled sprite while its shape, colour and rotation indices equal that target's required values (1956-1957, 2017-2038; state changes, 1872-1884) | no | not testable |

With two testable games (tu93, dc22), the protocol's overall outcome can be "binding" only if both
are BINDING, and "not binding" only if both are NOT BINDING (docs/E9_protocol.md Section 5).

## A consequence for the protocol, for the author to decide

docs/E9_protocol.md Section 1 says the goal table gives each level's target as a list of (row,
col) cells. That would record layouts, which this file does not do. The consistent form is:
- this file gives the target by its rule: "the position of the sprite tagged X";
- the oracle arm reads that sprite's position from the running game at each level start, for
  these two train games only.

That is a change to the protocol's wording, not to its design: the oracle still supplies the true
goal cells and nothing else. It should be recorded in docs/E9_protocol.md before gate G2 if the
author accepts it.
