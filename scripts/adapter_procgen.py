"""
Suite-C adapter (Procgen 0.10.7), docs/PREREG.md v1 Section 3.3.  Runs in .venv_procgen (Python
3.10).  Plays no game on import.

    construction   ProcgenGym3Env(num=1, env_name=game, distribution_mode="easy",
                   use_backgrounds=False, use_monochrome_assets=True, center_agent=<condition>,
                   use_sequential_levels=True, num_levels=0, start_level=seed, rand_seed=seed,
                   num_threads=1).  With num_levels 0, start_level is not read by procgen
                   (vecgame.cpp:287-289); the level sequence is fixed by rand_seed.
    conditions     center_off (center_agent False, primary) and center_on (True, secondary)
    frame          obs["rgb"][0], 64 x 64 x 3; no crop; grid 64 x 64
    palette        exact RGB, online: each new RGB triple gets the next index from 1, capped at 64
                   entries; from the 65th distinct colour on, a colour maps to the existing index
                   with the smallest squared RGB distance, ties to the lowest index.  The number of
                   distinct RGB triples seen is recorded.
    actions        all 15, 0-14 (duplicates and no-ops kept; docs/GROUND_TRUTH_procgen.md)
    level_end      info["prev_level_complete"] == 1 (game.cpp:163; vecgame.cpp:250)
    game_end       the gym3 `first` flag after a step without a level end: death or timeout
                   (with use_sequential_levels a completion clears done, game.cpp:148-150)
    restart()      the ARC RESET: procgen cannot restart a level, so it takes no step and returns
                   the current grid (PREREG v1 is silent; recorded in docs/ADAPTER_FEASIBILITY.md
                   as needing PREREG v1.1)
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import env_frame as EF  # noqa: E402

CAP = 64
GAMES = ["bigfish", "bossfight", "caveflyer", "chaser", "climber", "coinrun", "dodgeball", "fruitbot",
         "heist", "jumper", "leaper", "maze", "miner", "ninja", "plunder", "starpilot"]


class ProcgenAdapter(EF.FrameEnv):
    suite = "procgen"

    def __init__(self, game, condition):
        if condition not in ("center_off", "center_on"):
            raise ValueError(condition)
        self.game, self.condition = game, condition
        self.actions = list(range(15))
        self.env = None
        self.seed = None
        self.pal_keys = []                 # packed RGB of each palette entry, index = position + 1
        self.pal_rgb = np.zeros((0, 3), dtype=np.int64)
        self.pal_map = {}                  # packed RGB -> index (including overflow mappings)
        self.seen = set()                  # distinct packed RGB seen
        self.kw = None

    def _build(self, seed):
        from procgen import ProcgenGym3Env
        self.kw = dict(num=1, env_name=self.game, distribution_mode="easy", use_backgrounds=False,
                       use_monochrome_assets=True, center_agent=self.condition == "center_on",
                       use_sequential_levels=True, num_levels=0, start_level=int(seed), rand_seed=int(seed),
                       num_threads=1)
        self.env = ProcgenGym3Env(**self.kw)

    def _index(self, packed):
        if packed in self.pal_map:
            return self.pal_map[packed]
        rgb = np.array([(packed >> 16) & 255, (packed >> 8) & 255, packed & 255], dtype=np.int64)
        if len(self.pal_keys) < CAP:
            self.pal_keys.append(packed)
            self.pal_rgb = np.vstack([self.pal_rgb, rgb[None, :]])
            idx = len(self.pal_keys)
        else:
            d = ((self.pal_rgb - rgb[None, :]) ** 2).sum(axis=1)
            idx = int(np.argmin(d)) + 1               # argmin returns the first (lowest) on ties
        self.pal_map[packed] = idx
        return idx

    def _grid(self, obs):
        f = np.asarray(obs["rgb"][0]).astype(np.uint32)
        packed = (f[..., 0] << 16) | (f[..., 1] << 8) | f[..., 2]
        # first-appearance order is row-major over the frame, so new colours are indexed in that order
        flat = packed.ravel()
        _, first = np.unique(flat, return_index=True)
        for p in flat[np.sort(first)]:
            p = int(p)
            self.seen.add(p)
            self._index(p)
        lut = {p: self.pal_map[p] for p in set(flat.tolist())}
        return np.vectorize(lut.__getitem__, otypes=[np.int16])(packed)

    def reset(self, seed):
        self.seed = int(seed)
        self._build(seed)
        _rew, obs, _first = self.env.observe()
        self._last = self._grid(obs)
        return self._last

    def restart(self):
        return self._last

    def step(self, i):
        self.env.act(np.array([int(self.actions[i])], dtype=np.int32))
        _rew, obs, first = self.env.observe()
        info = self.env.get_info()[0]
        level_end = bool(info.get("prev_level_complete", 0))
        game_end = bool(first[0]) and not level_end
        self._last = self._grid(obs)
        return self._last, level_end, game_end

    def record(self):
        kw = dict(self.kw or {})
        return dict(suite="procgen", game=self.game, condition=self.condition, palette="rgb64",
                    n_colours=len(self.seen), palette_entries=len(self.pal_keys), crop=None, grid=[64, 64],
                    action_list=list(self.actions), camera=dict(center_agent=kw.get("center_agent")),
                    levels=dict(use_sequential_levels=True, num_levels=0, start_level=kw.get("start_level"),
                                rand_seed=kw.get("rand_seed")),
                    settings=dict(distribution_mode="easy", use_backgrounds=False, use_monochrome_assets=True),
                    adapter_blob=EF.git_blob_hash("scripts/adapter_procgen.py"),
                    env_frame_blob=EF.git_blob_hash("scripts/env_frame.py"), frozen=EF.frozen_hashes())

    def close(self):
        try:
            self.env.close()
        except Exception:
            pass
