r"""
How much does one game action cost with a LOCAL model?  Measured on real frames, not guessed.

Opens a train game with the engine (offline), renders each frame as text, sends it to an Ollama
model in a persistent chat (so the prompt prefix is cached and only the new frame is read each
step), takes the model's JSON action, steps the game, repeats.  Reports per step: prompt tokens,
prompt-read seconds, generated tokens, generation seconds, and whether the reply parsed.  Then the
arithmetic that decides the question: seconds per action, hours per 200-action game, days per
25-game evaluation.  Two frame encodings are timed: FULL (64 rows of 64 digits) and RLE
(run-length rows, much shorter).

    python local_llm_speed.py --model qwen2.5:7b --game tu93 --steps 4 --env-dir D:\Research\arc3\brutus\environment_files
    python local_llm_speed.py --model qwen2.5:14b --game tu93 --steps 3 --encoding rle --env-dir ...

Needs Ollama running (it starts itself on Windows when installed as a service) and the arc-agi
venv (requests is already a dependency of arc-agi).  Set --gpu-layers 0 to keep Ollama entirely on
the CPU, which on a 2 GB GPU is usually faster than a partial offload.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import time

import numpy as np
import requests

logging.disable(logging.CRITICAL)

OLLAMA = "http://localhost:11434/api/chat"

SYSTEM = ("You are playing an unknown 64x64 grid game. Each cell is a digit 0-15 (colour). "
          "Available actions: 1=up 2=down 3=left 4=right 5=action-5 7=action-7, or 6 with x,y for a click. "
          "Reply with ONE JSON object only, no prose: {\"action\": <int>, \"x\": <int or null>, "
          "\"y\": <int or null>, \"why\": \"<10 words max>\"}")


def enc_full(g):
    return "\n".join("".join(format(int(v), "x") for v in row) for row in g)


def enc_rle(g):
    out = []
    for y, row in enumerate(g):
        parts, prev, n = [], None, 0
        for v in row:
            v = int(v)
            if v == prev:
                n += 1
            else:
                if prev is not None:
                    parts.append(f"{format(prev, 'x')}x{n}" if n > 1 else format(prev, "x"))
                prev, n = v, 1
        parts.append(f"{format(prev, 'x')}x{n}" if n > 1 else format(prev, "x"))
        out.append(f"r{y:02d} " + " ".join(parts))
    return "\n".join(out)


def parse_action(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
        a = int(d.get("action"))
        return a, d.get("x"), d.get("y")
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen2.5:7b")
    ap.add_argument("--game", default="tu93")
    ap.add_argument("--steps", type=int, default=4)
    ap.add_argument("--encoding", default="both", help="full | rle | both")
    ap.add_argument("--env-dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "environment_files"))
    ap.add_argument("--gpu-layers", type=int, default=0, help="Ollama num_gpu; 0 = CPU only")
    ap.add_argument("--ctx", type=int, default=16384)
    args = ap.parse_args()

    from arc_agi import Arcade
    from arcengine import GameAction
    encs = ["full", "rle"] if args.encoding == "both" else [args.encoding]
    summary = {}
    for enc_name in encs:
        enc = enc_full if enc_name == "full" else enc_rle
        arc = Arcade(operation_mode="offline", environments_dir=args.env_dir)
        env = arc.make(args.game)
        raw = env.observation_space
        messages = [{"role": "system", "content": SYSTEM}]
        rows = []
        print(f"\n=== {args.model} on {args.game}, encoding {enc_name}, {args.steps} steps (first step includes model load) ===")
        for step in range(args.steps):
            g = np.asarray(raw.frame[-1])
            frame_text = enc(g)
            messages.append({"role": "user", "content": f"Step {step}. Level {raw.levels_completed}. Frame:\n{frame_text}\nNext action?"})
            t0 = time.time()
            r = requests.post(OLLAMA, json=dict(model=args.model, messages=messages, stream=False,
                                                keep_alive="15m",
                                                options=dict(num_ctx=args.ctx, num_gpu=args.gpu_layers,
                                                             temperature=0.2, num_predict=80)),
                              timeout=3600)
            wall = time.time() - t0
            j = r.json()
            reply = j.get("message", {}).get("content", "")
            messages.append({"role": "assistant", "content": reply})
            pe, pd = j.get("prompt_eval_count", 0), j.get("prompt_eval_duration", 0) / 1e9
            ec, ed = j.get("eval_count", 0), j.get("eval_duration", 0) / 1e9
            act = parse_action(reply)
            rows.append(dict(step=step, frame_chars=len(frame_text), prompt_tokens=pe, prompt_s=pd,
                             gen_tokens=ec, gen_s=ed, wall_s=wall, parsed=act is not None))
            print(f"step {step}: frame {len(frame_text)} chars | prompt {pe} tok in {pd:.1f}s "
                  f"({pe / pd if pd else 0:.1f} tok/s) | gen {ec} tok in {ed:.1f}s ({ec / ed if ed else 0:.1f} tok/s) "
                  f"| wall {wall:.1f}s | reply {reply.strip()[:90]!r} | parsed={act is not None}", flush=True)
            if act is None:
                raw = env.step(GameAction.from_id(1))
            else:
                a, x, y = act
                try:
                    if a == 6 and x is not None and y is not None:
                        raw = env.step(GameAction.from_id(6), data={"x": int(x), "y": int(y)})
                    else:
                        raw = env.step(GameAction.from_id(a if a in (1, 2, 3, 4, 5, 7) else 1))
                except Exception as e:
                    print(f"   engine rejected {act}: {e!r}; stepping 1")
                    raw = env.step(GameAction.from_id(1))
            if raw.state.name != "NOT_FINISHED":
                raw = env.step(GameAction.RESET)
        # steady state = all steps but the first (which carries the model load and the system prompt)
        st = rows[1:] if len(rows) > 1 else rows
        sec = sum(x["wall_s"] for x in st) / len(st)
        ptok = sum(x["prompt_tokens"] for x in st) / len(st)
        summary[enc_name] = dict(sec_per_action=sec, prompt_tokens_per_step=ptok,
                                 parsed=sum(x["parsed"] for x in rows), steps=len(rows))
        print(f"steady state: {sec:.1f} s per action, {ptok:.0f} new prompt tokens per step, "
              f"{summary[enc_name]['parsed']}/{len(rows)} replies parsed")
        print(f"  -> a 200-action game: {sec * 200 / 3600:.1f} h;  25 public games x 1 seed: "
              f"{sec * 200 * 25 / 86400:.1f} days;  17 held-out games x 4 seeds: {sec * 200 * 17 * 4 / 86400:.1f} days")
        print(f"  -> the Kaggle rerun plays 55 hidden games inside 9 h: that needs <= {9 * 3600 / (55 * 200):.1f} s per action")
    json.dump(summary, open("local_llm_speed.json", "w"), indent=1)


if __name__ == "__main__":
    main()
