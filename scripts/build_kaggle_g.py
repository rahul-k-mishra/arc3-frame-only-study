"""
Build the Kaggle submission notebook for BRUTUS.

This follows the ARC Prize starter kit's own pattern (ARC-AGI-3-Kaggle-Starter,
scripts/build_notebook.py), which is what the competition actually expects:

  1. install the arc-agi wheels from the offline competition dataset;
  2. write the agent files to /tmp - NOT to /kaggle/working, or they would show up in the
     Submit to Competition file dropdown beside submission.parquet;
  3. IF the notebook is running as the competition rerun (KAGGLE_IS_COMPETITION_RERUN is set):
     wait for the gateway sidecar at http://gateway:8001, copy the framework into a writable
     place, drop the agent in as agents/templates/my_agent.py, rewrite agents/__init__.py,
     point .env at the gateway, and run `python main.py --agent myagent`.  The GATEWAY writes
     submission.parquet - the agent does not;
  4. OTHERWISE (an ordinary Save and Run All): write a dummy submission.parquet so the commit
     is accepted, exactly as the starter does.

BRUTUS ships as three files rather than one, so the payload is carried gzipped and
base64-encoded inside the notebook and unpacked in step 2; verify_kaggle_notebook.py checks
byte-for-byte that what is carried is what was tested.

    python build_kaggle_notebook.py                        writes submission.ipynb
    python build_kaggle_notebook.py --accelerator cpu --hours 8
"""
from __future__ import annotations

import argparse
import base64
import gzip
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["brutus_g_agent.py"]
COMP = "arc-prize-2026-arc-agi-3"

# The agent is pure-Python symbolic search and the framework plays games as THREADS in one
# process, so extra cores cannot be used and a GPU would sit idle while burning quota.
ACCELERATORS = {
    "cpu": {"name": "none", "gpu": False},
    "t4": {"name": "nvidiaTeslaT4", "gpu": True},
    "p100": {"name": "nvidiaTeslaP100", "gpu": True},
    "rtx6000": {"name": "nvidiaRtx6000", "gpu": True},
}


def code_cell(source):
    return {"cell_type": "code", "metadata": {"trusted": True}, "outputs": [],
            "execution_count": None, "source": source}


def markdown_cell(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "submission.ipynb"))
    ap.add_argument("--hours-agent", type=float, default=8.5)
    ap.add_argument("--id", default=None)
    ap.add_argument("--title", default=None)
    ap.add_argument("--competition", default=None)
    ap.add_argument("--accelerator", default="cpu", choices=sorted(ACCELERATORS))
    ap.add_argument("--hours", type=float, default=8.0)
    ap.add_argument("--max-actions", type=int, default=20000)
    args = ap.parse_args()

    payload = {}
    for name in FILES:
        with open(os.path.join(HERE, name), "rb") as f:
            raw = f.read()
        payload[name] = base64.b64encode(gzip.compress(raw, 9)).decode()
        print(f"{name}: {len(raw)} bytes -> {len(payload[name])} chars packed")

    head = "# BRUTUS-G - ARC-AGI-3.  The agent file is carried inside this notebook,\n"
    head += "# gzipped and base64-encoded, so what runs here is byte-for-byte what passed the\n"
    head += "# local seven-game regression.\n"
    head += "PAYLOAD = {\n"
    for name, blob in payload.items():
        head += f"    {name!r}: (\n"
        for i in range(0, len(blob), 120):
            head += f"        {blob[i:i + 120]!r}\n"
        head += "    ),\n"
    head += "}\n"
    head += "PAYLOAD = {k: (''.join(v) if isinstance(v, tuple) else v) for k, v in PAYLOAD.items()}\n"
    head += "print('payload:', {k: len(v) for k, v in PAYLOAD.items()})\n"

    install = ("!pip install --no-index --find-links \\\n"
               f"    /kaggle/input/competitions/{COMP}/arc_agi_3_wheels \\\n"
               "    arc-agi python-dotenv")

    unpack = (
        "# Unpack the three agent files to /tmp.  NOT to /kaggle/working: anything written\n"
        "# there is offered in the Submit to Competition file dropdown beside\n"
        "# submission.parquet, and an unlucky default selection rejects the submission.\n"
        "import base64, gzip, os\n"
        "for _name, _blob in PAYLOAD.items():\n"
        "    _data = gzip.decompress(base64.b64decode(_blob))\n"
        "    with open('/tmp/' + ('my_agent.py' if _name == 'brutus_agent_v7.py' else _name), 'wb') as _f:\n"
        "        _f.write(_data)\n"
        "    print(_name, len(_data), 'bytes')\n"
    )

    init_py = (
        "from typing import Type\\n"
        "from dotenv import load_dotenv\\n"
        "from .agent import Agent, Playback\\n"
        "from .swarm import Swarm\\n"
        "from .templates.random_agent import Random\\n"
        "from .templates.my_agent import MyAgent\\n"
        "\\n"
        "load_dotenv()\\n"
        "\\n"
        "AVAILABLE_AGENTS: dict[str, Type[Agent]] = {\\n"
        "    'random': Random,\\n"
        "    'myagent': MyAgent,\\n"
        "}\\n"
    )
    env_txt = (
        "SCHEME=http\\n"
        "HOST=gateway\\n"
        "PORT=8001\\n"
        "ARC_API_KEY=test-key-123\\n"
        "ARC_BASE_URL=http://gateway:8001/\\n"
        "OPERATION_MODE=online\\n"
        "ENVIRONMENTS_DIR=\\n"
        "RECORDINGS_DIR=/kaggle/working/server_recording\\n"
    )

    run = f"""import os

if os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
    # Wait for the gateway sidecar to come up.
    !curl --fail --retry 999 --retry-all-errors --retry-delay 5 --retry-max-time 600 http://gateway:8001/api/games

    !cp -r /kaggle/input/competitions/{COMP}/ARC-AGI-3-Agents /kaggle/working/ARC-AGI-3-Agents
    !cp /tmp/my_agent.py /kaggle/working/ARC-AGI-3-Agents/agents/templates/

    with open('/kaggle/working/ARC-AGI-3-Agents/agents/__init__.py', 'w') as f:
        f.write("{init_py}")

    with open('/kaggle/working/ARC-AGI-3-Agents/.env', 'w') as f:
        f.write("{env_txt}")

    # The gateway records every action and emits submission.parquet.
    !cd /kaggle/working/ARC-AGI-3-Agents && MPLBACKEND=agg BRUTUS_MAX_ACTIONS={args.max_actions} BRUTUS_WALL_SECONDS={int(args.hours * 3600)} python main.py --agent myagent
else:
    print('not the competition rerun - nothing is played here; see the next cell')
"""

    dummy = """import os
if not os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
    # Save-and-run-all (commit) mode: emit a dummy submission so the commit succeeds.  The
    # real submission.parquet is produced by the gateway during the competition rerun.
    import pandas as pd
    submission = pd.DataFrame(
        data=[['1_0', '1', True, 1]],
        columns=['row_id', 'game_id', 'end_of_game', 'score'])
    submission.to_parquet('/kaggle/working/submission.parquet', index=False)
    print(submission)
"""

    accel = ACCELERATORS[args.accelerator]
    nb = {
        "metadata": {
            "kernelspec": {"language": "python", "display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python", "mimetype": "text/x-python",
                              "file_extension": ".py", "pygments_lexer": "ipython3"},
            "kaggle": {"accelerator": accel["name"], "isInternetEnabled": False,
                       "isGpuEnabled": accel["gpu"], "language": "python",
                       "sourceType": "notebook"},
        },
        "nbformat_minor": 4,
        "nbformat": 4,
        "cells": [
            markdown_cell("# BRUTUS-G - ARC Prize 2026, ARC-AGI-3\n\nGeneric agent, frames only. Built by "
                          "build_kaggle_notebook.py, following the ARC Prize starter kit's "
                          "pattern. Do not edit cells here - rebuild instead."),
            code_cell(head),
            code_cell(install),
            code_cell(unpack),
            code_cell(run),
            code_cell(dummy),
        ],
    }
    with open(args.out, "w") as f:
        json.dump(nb, f, indent=1)
    print("wrote", args.out, os.path.getsize(args.out), "bytes,",
          "accelerator", args.accelerator)

    meta_path = os.path.join(os.path.dirname(args.out), "kernel-metadata.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    meta_id = args.id or meta.get("id") or "USERNAME/arc3-brutus-v101"
    title = args.title or meta.get("title") or meta_id.split("/")[-1]
    meta = {
        "id": meta_id,
        "title": title,
        "code_file": os.path.basename(args.out),
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": accel["gpu"],
        "enable_tpu": False,
        "enable_internet": False,
        "keywords": [],
        "dataset_sources": meta.get("dataset_sources", []),
        "kernel_sources": [],
        "competition_sources": [args.competition or
                                (meta.get("competition_sources") or [COMP])[0]],
        "model_sources": [],
    }
    json.dump(meta, open(meta_path, "w"), indent=2)
    print("wrote", meta_path, "- id", meta["id"], "title", meta["title"],
          "gpu", meta["enable_gpu"])


if __name__ == "__main__":
    main()
