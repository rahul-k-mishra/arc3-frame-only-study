"""
Build a PLAIN Kaggle notebook - not a competition submission - that runs the G-NAV A/B
(g_nav_run.py) on Kaggle's free CPU machines, so the held-out run can go in parallel with the
train run on the lenovo.  No GPU, no internet, nothing submitted.  Writes into its OWN folder
(kaggle_navrun/) with its OWN kernel id, so it can never touch the submission kernel's metadata.

    python build_kaggle_navrun.py --games heldout --seeds 4 --budget 20000 --hours 9
    kaggle kernels push -p kaggle_navrun
    (later)  kaggle kernels output ericsom/arc3-brutus-navrun -p kaggle_navrun/out
"""
from __future__ import annotations

import argparse
import base64
import gzip
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["g_agent.py", "g_motion.py", "g_control_probe.py", "g_nav.py", "g_nav_run.py"]
COMP = "arc-prize-2026-arc-agi-3"


def cell(src, kind="code"):
    return {"cell_type": kind, "metadata": {"trusted": True}, "outputs": [],
            "execution_count": None, "source": src} if kind == "code" else \
           {"cell_type": "markdown", "metadata": {}, "source": src}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "kaggle_navrun", "navrun.ipynb"))
    ap.add_argument("--id", default="ericsom/arc3-brutus-navrun")
    ap.add_argument("--title", default="arc3-brutus-navrun")
    ap.add_argument("--games", default="heldout")
    ap.add_argument("--modes", default="hash_state,nav")
    ap.add_argument("--hours", type=float, default=9.0)
    ap.add_argument("--budget", type=int, default=20000)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--game-seconds", type=float, default=1800)
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    payload = {}
    for name in FILES:
        raw = open(os.path.join(HERE, name), "rb").read()
        payload[name] = base64.b64encode(gzip.compress(raw, 9)).decode()
        print(f"{name}: {len(raw)} bytes")

    head = "# BRUTUS-G laboratory - plain CPU notebook, nothing submitted.\nPAYLOAD = {\n"
    for name, blob in payload.items():
        head += f"    {name!r}: (\n"
        for i in range(0, len(blob), 120):
            head += f"        {blob[i:i + 120]!r}\n"
        head += "    ),\n"
    head += "}\nPAYLOAD = {k: (''.join(v) if isinstance(v, tuple) else v) for k, v in PAYLOAD.items()}\n"
    head += "print('payload:', {k: len(v) for k, v in PAYLOAD.items()})\n"

    install = ("!pip install --no-index --find-links \\\n"
               f"    /kaggle/input/competitions/{COMP}/arc_agi_3_wheels \\\n"
               "    arc-agi python-dotenv")

    unpack = ("import base64, gzip, os, glob\n"
              "os.makedirs('/kaggle/working/lab', exist_ok=True)\n"
              "for _n, _b in PAYLOAD.items():\n"
              "    open('/kaggle/working/lab/' + _n, 'wb').write(gzip.decompress(base64.b64decode(_b)))\n"
              f"ENV = '/kaggle/input/competitions/{COMP}/environment_files'\n"
              "print('games:', len(glob.glob(ENV + '/*')))\n"
              "print(sorted(os.path.basename(p) for p in glob.glob(ENV + '/*'))[:30])")

    run = f'''import os, sys
sys.path.insert(0, "/kaggle/working/lab")
os.environ["MPLBACKEND"] = "agg"
print("cpu count:", os.cpu_count(), "| usable:",
      len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else "?")
sys.argv = ["g_nav_run.py", "--games", "{args.games}", "--modes", "{args.modes}",
            "--seeds", "{args.seeds}", "--budget", "{args.budget}",
            "--workers", "{args.workers}", "--game-seconds", "{args.game_seconds}",
            "--hours", "{args.hours}",
            "--env-dir", "/kaggle/input/competitions/{COMP}/environment_files",
            "--tag", "kaggle"]
import g_nav_run
g_nav_run.main()
import shutil, os.path
if os.path.exists("/kaggle/working/lab/navrun_kaggle.json"):
    shutil.copy("/kaggle/working/lab/navrun_kaggle.json", "/kaggle/working/navrun_kaggle.json")
print("results in /kaggle/working/navrun_kaggle.json")
'''

    nb = {"metadata": {"kernelspec": {"language": "python", "display_name": "Python 3", "name": "python3"},
                       "language_info": {"name": "python", "mimetype": "text/x-python",
                                         "file_extension": ".py", "pygments_lexer": "ipython3"},
                       "kaggle": {"accelerator": "none", "isInternetEnabled": False,
                                  "isGpuEnabled": False, "language": "python",
                                  "sourceType": "notebook"}},
          "nbformat_minor": 4, "nbformat": 4,
          "cells": [cell("# BRUTUS-G: G-NAV against hash_state\n\nPlain CPU notebook. No GPU, no internet, "
                         "nothing submitted to the competition. Plays the public games with the "
                         "navigation planner and with the plain explorer on the same seeds and "
                         "prints, per level, the scorecard's action count against the human count.",
                         "markdown"),
                    cell(head), cell(install), cell(unpack), cell(run)]}
    json.dump(nb, open(args.out, "w"), indent=1)
    meta = {"id": args.id, "title": args.title, "code_file": os.path.basename(args.out),
            "language": "python", "kernel_type": "notebook", "is_private": True,
            "enable_gpu": False, "enable_tpu": False, "enable_internet": False, "keywords": [],
            "dataset_sources": [], "kernel_sources": [], "competition_sources": [COMP],
            "model_sources": []}
    json.dump(meta, open(os.path.join(os.path.dirname(args.out), "kernel-metadata.json"), "w"), indent=2)
    print("wrote", args.out, os.path.getsize(args.out), "bytes | gpu off, internet off, not a submission")


if __name__ == "__main__":
    main()
