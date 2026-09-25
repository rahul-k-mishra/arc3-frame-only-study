"""
Build a PLAIN Kaggle CPU notebook - not a submission - that measures what a local LLM costs per
game action on Kaggle's CPU machine: install Ollama in the session, pull the model from the
internet (internet ON, so nothing is pushed from the laptop), install the competition wheels,
then run local_llm_speed.py on a train game for a few real steps and print seconds per action
and the hours per game / days per evaluation that follow.  Writes into its OWN folder
(kaggle_llmspeed/) with its OWN kernel id, so it can never touch a submission kernel.

    python build_kaggle_llmspeed.py --model qwen2.5:7b --game tu93 --steps 4
    kaggle kernels push -p kaggle_llmspeed
    kaggle kernels status ericsom/arc3-llm-speed
    (when complete)  kaggle kernels output ericsom/arc3-llm-speed -p kaggle_llmspeed/out

Needs: local_llm_speed.py next to this file.  The notebook prints the machine's cores and RAM
first, so the numbers are Kaggle's, not assumed.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["local_llm_speed.py"]
COMP = "arc-prize-2026-arc-agi-3"


def cell(src, kind="code"):
    return {"cell_type": kind, "metadata": {"trusted": True}, "outputs": [],
            "execution_count": None, "source": src} if kind == "code" else \
           {"cell_type": "markdown", "metadata": {}, "source": src}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "kaggle_llmspeed", "llmspeed.ipynb"))
    ap.add_argument("--id", default="ericsom/arc3-llm-speed")
    ap.add_argument("--title", default="arc3-llm-speed")
    ap.add_argument("--model", default="qwen2.5:7b", help="comma list of Ollama models to pull and time")
    ap.add_argument("--game", default="tu93")
    ap.add_argument("--steps", type=int, default=4)
    ap.add_argument("--encoding", default="both")
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    models = [m.strip() for m in args.model.split(",") if m.strip()]

    payload = {}
    for name in FILES:
        raw = open(os.path.join(HERE, name), "rb").read()
        payload[name] = base64.b64encode(gzip.compress(raw, 9)).decode()
        print(f"{name}: {len(raw)} bytes")

    head = "# LLM speed on Kaggle CPU - plain notebook, nothing submitted.\nPAYLOAD = {\n"
    for name, blob in payload.items():
        head += f"    {name!r}: (\n"
        for i in range(0, len(blob), 120):
            head += f"        {blob[i:i + 120]!r}\n"
        head += "    ),\n"
    head += "}\nPAYLOAD = {k: (''.join(v) if isinstance(v, tuple) else v) for k, v in PAYLOAD.items()}\n"
    head += "print('payload:', {k: len(v) for k, v in PAYLOAD.items()})\n"

    machine = ("import os, subprocess\n"
               "print('cpu count:', os.cpu_count(), '| usable:', len(os.sched_getaffinity(0)))\n"
               "print(subprocess.run(['free', '-g'], capture_output=True, text=True).stdout)\n"
               "print(subprocess.run(['lscpu'], capture_output=True, text=True).stdout[:1500])\n"
               "print(subprocess.run(['df', '-h', '/kaggle/working', '/root'], capture_output=True, text=True).stdout)")

    install = ("!pip install --no-index --find-links \\\n"
               f"    /kaggle/input/competitions/{COMP}/arc_agi_3_wheels \\\n"
               "    arc-agi python-dotenv\n"
               "# MEASURED (Kaggle, 25 Sep 2026): the Ollama installer needs the zstd binary, which the image lacks\n"
               "!apt-get update -qq > /dev/null 2>&1; apt-get install -y -qq zstd > /dev/null 2>&1; zstd --version\n"
               "!curl -fsSL https://ollama.com/install.sh | sh\n"
               "!ls -la /usr/local/bin/ollama /usr/bin/ollama 2>/dev/null; which ollama; ollama --version")

    serve = ("import subprocess, time, requests, os, shutil\n"
             "OLLAMA_BIN = shutil.which('ollama') or '/usr/local/bin/ollama'\n"
             "assert os.path.exists(OLLAMA_BIN), 'ollama binary not found - the install cell failed; send its output'\n"
             "os.environ['PATH'] = os.path.dirname(OLLAMA_BIN) + ':' + os.environ['PATH']\n"
             "os.environ['OLLAMA_MODELS'] = '/kaggle/working/ollama_models'\n"
             "os.environ['OLLAMA_NUM_PARALLEL'] = '1'\n"
             "srv = subprocess.Popen([OLLAMA_BIN, 'serve'], stdout=open('/kaggle/working/ollama_serve.log', 'w'),\n"
             "                       stderr=subprocess.STDOUT, env=os.environ.copy())\n"
             "for i in range(60):\n"
             "    try:\n"
             "        requests.get('http://localhost:11434/api/tags', timeout=2); print('ollama up after', i, 's'); break\n"
             "    except Exception:\n"
             "        time.sleep(1)\n"
             "else:\n"
             "    print(open('/kaggle/working/ollama_serve.log').read()); raise SystemExit('ollama did not start')\n")

    pull = "\n".join(f"!ollama pull {m}" for m in models) + "\n!ollama list"

    unpack = ("import base64, gzip, os, glob\n"
              "os.makedirs('/kaggle/working/lab', exist_ok=True)\n"
              "for _n, _b in PAYLOAD.items():\n"
              "    open('/kaggle/working/lab/' + _n, 'wb').write(gzip.decompress(base64.b64decode(_b)))\n"
              f"ENV = '/kaggle/input/competitions/{COMP}/environment_files'\n"
              "print('games:', len(glob.glob(ENV + '/*')))")

    runs = []
    for m in models:
        runs.append(f'''import os, sys, importlib
sys.path.insert(0, "/kaggle/working/lab")
os.environ["MPLBACKEND"] = "agg"
os.chdir("/kaggle/working/lab")
sys.argv = ["local_llm_speed.py", "--model", "{m}", "--game", "{args.game}", "--steps", "{args.steps}",
            "--encoding", "{args.encoding}", "--gpu-layers", "0",
            "--env-dir", "/kaggle/input/competitions/{COMP}/environment_files"]
import local_llm_speed
importlib.reload(local_llm_speed)
local_llm_speed.main()
import shutil
shutil.copy("/kaggle/working/lab/local_llm_speed.json", "/kaggle/working/llm_speed_{m.replace(':', '_').replace('/', '_')}.json")
''')

    nb = {"metadata": {"kernelspec": {"language": "python", "display_name": "Python 3", "name": "python3"},
                       "language_info": {"name": "python", "mimetype": "text/x-python",
                                         "file_extension": ".py", "pygments_lexer": "ipython3"},
                       "kaggle": {"accelerator": "none", "isInternetEnabled": True,
                                  "isGpuEnabled": False, "language": "python",
                                  "sourceType": "notebook"}},
          "nbformat_minor": 4, "nbformat": 4,
          "cells": [cell("# LLM speed on Kaggle CPU\n\nPlain CPU notebook, internet on, nothing submitted. "
                         "Installs Ollama, pulls the model, plays a few real steps of a public game "
                         "with the model choosing actions, and prints seconds per action.", "markdown"),
                    cell(machine), cell(head), cell(install), cell(serve), cell(pull), cell(unpack)]
                   + [cell(r) for r in runs]}
    json.dump(nb, open(args.out, "w"), indent=1)
    meta = {"id": args.id, "title": args.title, "code_file": os.path.basename(args.out),
            "language": "python", "kernel_type": "notebook", "is_private": True,
            "enable_gpu": False, "enable_tpu": False, "enable_internet": True, "keywords": [],
            "dataset_sources": [], "kernel_sources": [], "competition_sources": [COMP],
            "model_sources": []}
    json.dump(meta, open(os.path.join(os.path.dirname(args.out), "kernel-metadata.json"), "w"), indent=2)
    print("wrote", args.out, os.path.getsize(args.out), "bytes | gpu off, internet ON, not a submission")
    print("models:", models, "| game:", args.game, "| steps:", args.steps)


if __name__ == "__main__":
    main()
