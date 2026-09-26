# E1c phase 0: search for a second independent frame-only agent

Searched 26 September 2026. Search only: nothing was cloned, adapted or run. Files were read from
GitHub (README, licence and dependency files, agent entry files) through raw.githubusercontent.com
and the public GitHub API. Latest commits came from `git ls-remote`, which reads one ref and does
not clone. Kaggle notebook sources were downloaded with the Kaggle CLI (`kaggle kernels pull`)
into a scratch folder, read only and never run. The admissibility items are those of
docs/TOG_PLAN_v2.md Section 3.1 (A1-A7); this document changes none of them. The author decides
what to pursue.

## 0. Outcome (recorded 26 September 2026)

- **ZubMono "Prometheus": REJECTED by the author.** Its `DIRECTION_PRIORS` were measured on all
  25 public games, which include the 17 held-out games, so it carries parameters fitted on our
  evaluation set, and A5 forbids removing them. Size is irrelevant; the contamination is the
  reason. Evidence: docs/E1c_prometheus_check.md.
- **The other candidates in Section 7 are not pursued.** E1c is closed in docs/TOG_PLAN_v2.md with
  no admissible second independent agent found.

## 1. Result in one paragraph

**No candidate is confirmed admissible.** Admissibility item A5 (the adapter changes I/O only),
A6 (fidelity) and A7 (cost) can only be settled by running an agent, which phase 0 does not do.
Three candidates pass every check that can be made without running them:
- **ZubMono "Prometheus":** MIT-0, standard library only, offline, no LLM. It is the most
  substantial of the three. Its agent file mentions all 25 public game ids in comments and
  docstrings, so a line-by-line check for game-specific code is needed first.
- **conchocon154's novelty agent:** MIT, a small baseline; its author reports it does not beat
  its own random control.
- **ReplicaWormhole's explorer:** MIT, a research harness.

Two more need an author decision:
- **garlictoday's Kaggle graph explorer** reimplements the Rudakov et al. method already measured
  in E1a.
- **poby7722's Kaggle graph explorer** contains a setting chosen for cn04, a held-out game.

The strongest non-LLM agents found (BDR-Pro "v79", the 0.26-0.27 agent the first plan could not
trace; Cryptic2-0's GraphExplorer; Curio; Hunter-Seeker v2) have **no licence file**, so under A2
they cannot be used. Most higher-scoring non-LLM Kaggle notebooks **load each game's source file
at play time**. That makes them not frame-only, and running them on held-out games would open
held-out source, which this project forbids. Every arXiv agent paper found uses an LLM or a
coding agent.

## 2. Sources searched (all on 26 September 2026)

| # | source | how | what it returned |
|---|---|---|---|
| S1 | GitHub repositories, query `arc-agi-3` | api.github.com/search/repositories?q=arc-agi-3&sort=updated&per_page=50 | 419 repositories; the 50 most recently updated were screened |
| S2 | GitHub, query `arc-agi-3 agent` | same, q=arc-agi-3+agent | 136; top 50 screened |
| S3 | GitHub, query `arc prize 2026` | same, q=arc+prize+2026 | 117; top 50 screened |
| S4 | GitHub, query `arcagi3` | same, q=arcagi3 | 7; all screened |
| S5 | Web search: "ARC-AGI-3 agent github graph exploration non-LLM" | WebSearch | 9 results (GitHub repositories, the Rudakov et al. paper) |
| S6 | Web search: "kaggle ARC Prize 2026 ARC-AGI-3 code notebook agent CPU" | WebSearch | 9 results (GitHub repositories, competition pages) |
| S7 | Web search: "arXiv ARC-AGI-3 agent code released 2026", "arxiv ARC-AGI-3 exploration agent without language model github code", "\"ARC-AGI-3\" arxiv 2026 agent world model training-free code available" | WebSearch | arXiv 2605.05138, 2607.28287, 2605.25931, 2608.14490, 2607.01531, 2603.24621 |
| S8 | arXiv abstract pages for the five agent papers | WebFetch of arxiv.org/abs/<id> | LLM use and code links (Section 5) |
| S9 | Kaggle code tab, https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/code | WebFetch | **not readable**: the page renders only with JavaScript |
| S10 | Kaggle code tab via CLI | `kaggle kernels list --competition arc-prize-2026-arc-agi-3 --sort-by voteCount --page-size 100` (author's Kaggle CLI 2.2.4, read-only listing) | 100 notebooks; the non-LLM-looking ones were downloaded and read (Section 4) |
| S11 | Kaggle discussion tab, https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/discussion | web search "kaggle arc-prize-2026-arc-agi-3 discussion non-LLM agent CPU graph search open source" | the tab itself is not readable without JavaScript; the search surfaced no agent not already found in S1-S10 |
| S12 | Official ARC-AGI-3-Agents repository, https://github.com/arcprize/ARC-AGI-3-Agents | WebFetch + raw files + `git ls-remote` | templates (Section 6) |
| S13 | Kaggle notebook licence | web search "This Notebook has been released under the Apache 2.0 open source license" kaggle | Kaggle public-notebook pages carry that statement; not confirmed on the specific pages below, which do not render without JavaScript |

Screen applied to S1-S6 before reading any code:
- **Shortlisted** if the description or README suggested a frame-based agent with no LLM.
- **Excluded** on the description alone if it named an LLM, an LLM harness or model serving
  (e.g. the Duck/Tufa harness forks, Qwen or Gemma agents, vLLM, Prime Agent, AREx, Retrodict,
  Claude-Code skills, Bedrock samples).

Shortlisted repositories were then read: README, licence file anywhere in the tree, dependency
files, and the agent's entry file (imports, header, any use of the 25 public game ids).

Not examined:
- GitHub repositories beyond the 50 most recently updated per query (S1-S3 returned 419, 136
  and 117, overlapping; only the top 50 of each were screened);
- Kaggle notebooks beyond the 100 most voted;
- the Kaggle discussion threads themselves;
- the full code of any candidate (only the files named above).

## 3. GitHub candidates

Commit = latest commit on the default branch on 26 September 2026 (`git ls-remote ... HEAD`).
"Game source" = the agent reads a game's `.py` file (the simulator) at play time. "Game-specific"
= the shipped agent branches on specific public games.

### 3.1 Pass the phase-0 screen (possible; A5-A7 need a run)

| repository | commit | licence | LLM / GPU / network | API target | evidence and open questions |
|---|---|---|---|---|---|
| [ZubMono/arc-prize-2026](https://github.com/ZubMono/arc-prize-2026) ("Prometheus") | d2d574a98ba17714d0ca4b17045afdb5bdb50d80 | MIT-0 (LICENSE at root and in the agent folder) | README: "An offline agent (Python stdlib only at inference time: no network, no LLM calls)". Entry file imports only the standard library, `arcengine`, and the framework's `agents.agent.Agent`. No GPU. | ARC-AGI-3-Agents framework `Agent` interface with `arcengine.FrameData`, i.e. the current API, not the preview `score` field. arc-agi version not pinned (Python >= 3.12). | **Open:** `agent/my_agent.py` (10,683 lines) mentions all 25 public game ids 55 times outside `#` comments (e.g. lp85 30, vc33 15, dc22 14, ft09 13, ar25 12). The scan found no branch on a game id; the mentions it inspected are docstring text recording measurements. A line-by-line check is needed before admission. |
| [conchocon154/arc-agi3-baseline](https://github.com/conchocon154/arc-agi3-baseline) | 238290624f35769fca2e9468a3cda15360a55e13 | MIT | A random control and a "novelty" agent; imports `random`, `collections`, `arcengine`. No LLM, GPU or network. | `arcengine` and `arc_agi.local_wrapper` (offline engine); framework `Agent` for Kaggle. | No game ids in the agent. Its README describes "a novelty-seeking agent that does not beat random", with a table in which the random control scored on a seed where the novelty agent did not. It is independent but likely to give little signal (probably INCONCLUSIVE with M1 near 0). |
| [ReplicaWormhole/arc-agi-3-agent](https://github.com/ReplicaWormhole/arc-agi-3-agent) | d3d78ae5672226aba7aecbcf28a4caf25c452360 | MIT | `explorer.py` imports only `numpy`, `hashlib` and `arcengine`. A separate `model_client.py` is "a provider-neutral development-only chat model adapter ... never called by the unit tests". | `arc_agi.Arcade` with `OperationMode` offline, the same engine path as ours. | No game ids in the explorer. It is a research workspace (`work/2026-08-local-agent-harness/`) that runs one exploration episode. Whether the explorer path ever calls the model client must be checked, and whether it is a complete agent that plays to a budget. |

### 3.2 Not admissible: no licence file (A2)

With no licence, the default is all rights reserved, so A2 fails. Each could become admissible
only if its author adds a licence.

| repository | commit | what it is | evidence |
|---|---|---|---|
| [BDR-Pro/arc-prize-2026-arc-agi-3](https://github.com/BDR-Pro/arc-prize-2026-arc-agi-3) | b6bd1dc1b6474aea5fbf82b55c6ae844ef140f1a | "v79", a CPU-only, no-LLM agent (learned transition model, volatility-masked hashing, object-centric navigation) reporting "0.26-0.27" on the public leaderboard. This is the agent the first plan cited as "the public CPU-only 0.26-0.27 agent" and the audit could not trace. The repository now also has a GPU LLM "rescue" track. | No licence file anywhere in its 163-file tree; the README has no licence statement. |
| [Cryptic2-0/arc-agi-3-agent](https://github.com/Cryptic2-0/arc-agi-3-agent) | 07a51db1cd5237ee281822939882667c46f8d2d5 | GraphExplorer, "a no-LLM agent", public leaderboard 0.23. Has an offline runner using the real scorecard. No game ids in the agent. | No licence file in its 19-file tree. |
| [atilavahedian/arc-agi-3-curio](https://github.com/atilavahedian/arc-agi-3-curio) | 8c74d57a595eebd731c21be87b32d9e1cecb5bc9 | Curio: "a single hand-written Python policy (CPU-only, no training)"; world-modelling explorer. Game ids appear 39 times outside comments, none found in a branch. | No licence file in its 90-file tree. |
| [VykosMolt/Hunter-Seeker-v2](https://github.com/VykosMolt/Hunter-Seeker-v2) | a5121903859755550c7bf57ee6ef58705c4a7a20 | "No LLM in the loop"; a student head distilled from a "teacher" in an explicit offline phase, and one ablation needs torch weights that are not in the repository. | No licence file in its 105-file tree. The teacher distillation would also need review against "prior-free". |

### 3.3 Not frame-only or not prior-free (no-go)

| repository | commit | licence | reason |
|---|---|---|---|
| [tantan0327/arc-agi-3-agent](https://github.com/tantan0327/arc-agi-3-agent) | 77ab2d911e13789ea39e058ac3ad6c788dbd88d3 | MIT-0 | **Reads game source at play time.** `agent/my_agent.py` globs `environment_files/{gid}/*/{gid}.py` and imports it with `importlib`. Not frame-only; running it on held-out games would open held-out source (forbidden, CLAUDE.md rule 1). |
| [rvats20/ARC-AGI-3-agent](https://github.com/rvats20/ARC-AGI-3-agent) | 5ff8595e7ac1d0368271fcdece667a24f9d5d886 | MIT | **Game-specific scripted paths:** `is_ls20` / `is_m0r0` flags and a "v33-ls20-scripted" action source. Removing them would edit the policy (A5). A separate `qwen_agent.py` uses an LLM. |
| [Sahasawatt/arc-agi-3-agent](https://github.com/Sahasawatt/arc-agi-3-agent) | cc164a7fd3dda8491999e1b3d1346f902df7912f | MIT-0 (LICENSE file; the API reports NOASSERTION) | **Game-specific:** the shipped `kaggle/my_agent.py` is "fourteen measured whole-game drivers ... behind their reset-frame signatures, a random fallback for everything else", i.e. solutions keyed to recognised public games. It also has an optional local-model goal ranker (`goal_llm.py`), and the README's active line B is an LLM harness. It requires arc-agi >= 0.9.9 (ours is 0.9.8). |
| [AR6420/arc-agi-3-agent](https://github.com/AR6420/arc-agi-3-agent) | cd97cfe847cb8482bc6051b510c09c390ebb38e4 | CC-BY 4.0 | A ResNet with a behaviour-cloning action head (trained on demonstrations); torch. Not prior-free. |
| [thylinao1/arc-agi-3-offline-agent](https://github.com/thylinao1/arc-agi-3-offline-agent) | b56fb0997488c3dccc19a06e9c2b9e0329526ce4 | MIT | A CNN warm-started from behaviour-cloned weights from an offline BFS teacher on public games; torch, run on a T4. Not prior-free; GPU-dependent for its reported play. |
| [SynaLinks/arcagi3-worldmodel](https://github.com/SynaLinks/arcagi3-worldmodel) | 1e05bfc1970a5e4cf342334fa27594cd061a0e8c | Apache-2.0 | A DreamerV3-style neural world model (torch, CUDA in its example); wraps the REST game API. A3 not met as documented. |
| [dcw06/ARC-AGI-3](https://github.com/dcw06/ARC-AGI-3) | 13ad6e00f81730f2dd0cb52b5477ef9504c1060b | Apache-2.0 | The main path is a GPU model ("private V2 GPU fixture"); only a "deterministic fallback" is non-ML. |
| [hyuki0130/Admorphiq](https://github.com/hyuki0130/Admorphiq) | 1dc5fb7941f33348eafb10f27d77d6dea8e279ef | MIT | Deployed policy is behaviour-cloned (`models/bc_policy.pt`); an offline-LLM track too. |
| [anandsingh8687/arc-prize-2026-arc-agi-3-agent](https://github.com/anandsingh8687/arc-prize-2026-arc-agi-3-agent) | e1f4563c7229d5ea615e2cb0fbb40d157a446e7b | none found | A model on "one 96GB Blackwell GPU"; "the entire budget is model time". |

### 3.4 No agent code, or LLM-based

| repository | commit | reason |
|---|---|---|
| [mubquaidian/arc-agi-3-bayesian-exploration](https://github.com/mubquaidian/arc-agi-3-bayesian-exploration) | a3d3aca6a66e926d5acbc2f0819abdaf0c9f1f75 | The repository holds 2 files, README and LICENSE; the described `src/agent.py` does not exist. Results "[TBD]". |
| [kanishkpaul/arc-agi3-world-models](https://github.com/kanishkpaul/arc-agi3-world-models) | 01ae2e0dc7e6fb592c17c0f9628f5fe3087e2eb0 | The README describes three agents (`iwm`, `categorical-cat`, `tcca`; best 4 of 183 levels), but the tree holds only a perception/verification substrate and tests; the agents are not in the repository. It requires arc-agi 0.9.9. |
| Dr-starck66/AION-ARC | not found | Listed by the GitHub API, but `git ls-remote` found no repository (removed or private). |
| [pomagrenate/dsg-ewm-arc-agi-3-agent](https://github.com/pomagrenate/dsg-ewm-arc-agi-3-agent) | cfbefaa52511260ea617226ada8eff13b0bcdba5 | The README is a competition overview; no licence file; no agent described. |
| [arodmor/arc-agi-3](https://github.com/arodmor/arc-agi-3) | c50f7e5ef54da8687e5b61752140b04ca652be7c | An essay about the track, not an agent. |
| [dp-web4/ARC-SAGE](https://github.com/dp-web4/ARC-SAGE) | 12139884f7d111f55bb8300905900fe343a79559 | Harness around Claude Opus 4.6 (LLM). |
| [jvilladuque90/arc-prize-2026-arc-agi-3](https://github.com/jvilladuque90/arc-prize-2026-arc-agi-3) | b1664dffe6b8de1e1cec1d050ef089dcec29ce65 | Model-driven with vLLM on an RTX Pro 6000 (LLM). |
| [Shih-Yu-Yeh/arc3-dev-agi-journal](https://github.com/Shih-Yu-Yeh/arc3-dev-agi-journal) | 0dfe8f577d59f44c6ab2776e978d2208dee3c711 | Qwen3.8-27B on vLLM (LLM). |
| [zedarvates/cogniarc](https://github.com/zedarvates/cogniarc) | f863d16c301ae888dd2cea87812f6dce73dbdf31 | "Accompany LLMs in their reflection"; ollama (LLM). |

## 4. Kaggle code tab (S10: the 100 most-voted notebooks)

Many of the 100 are LLM harnesses by title (Duck/Tufa forks with Qwen 3.6/3.8, a Gemma-4-31B
reflection agent, GPT-OSS-120B, a Milestone-1 solution); these were not downloaded. The non-LLM-looking ones were
downloaded and read. Licence: Kaggle public notebooks show "This Notebook has been released under
the Apache 2.0 open source license" (S13). This was not confirmed on these specific pages, which do
not render without JavaScript, and must be checked in a browser before any is used.
"lastRunTime" is from the listing.

| notebook (author/slug) | last run | LLM / GPU | reason |
|---|---|---|---|
| garlictoday/arc-agi-3-explorer-agent-graph-based | 2026-04-02 | none; numpy/pandas; GPU flag set but no torch | **Possible, author decision.** Frame-only graph explorer with no game ids in branches. Its code says the state graph is "from Dolphin" (the Rudakov et al. repository's owner), and its classes (`NodeInfo`, `StateGraph`, `_maybe_advance_group`, `_rebuild_distances`, status-bar detection) reimplement the E1a method. It meets the plan's letter of "independent" (different author, not our code, not an organiser template), but as evidence it would largely repeat E1a. |
| poby7722/versrion-47-is-bset-score-0-54 | 2026-06-27 | "no LLM, no GPU training", CPU | **Possible only with a caveat, author decision.** A frontier graph explorer with a learned counter mask. It ships `GAME_CONFIG = {"cn04": {"USE_REORDER": False}}`, added after a "cn04 regression" on the public set. cn04 is one of our held-out games, so running it unchanged is not prior-free on cn04, and A5 forbids removing the setting. Its origin ("explore2 ... see PLAN.md") is not stated further. |
| nihilisticneuralnet/0-46-arc-agi-3-persistent-memory-bfs-arc-solver | 2026-05-29 | torch/CNN | **Reads game source** (globs `environment_files/**/{gid}.py`, `importlib`). No-go. |
| nihilisticneuralnet/arc-agi-3-monte-carlo-tree-search-solver | 2026-04-01 | torch/CNN | **Reads game source** (`importlib`). No-go. |
| projectforty2/forge-arc-agi-3-agent | 2026-03-31 | torch/CNN | **Reads game source** (`spec_from_file_location(... self.game_path)`). No-go. |
| itsyoursumit/0-35-forge-v16-trigger-aware-bfs-submi3 | 2026-04-06 | torch/CNN | **Reads game source.** No-go. |
| marynaborovska/hybrid-search-and-learn-agent-0-35-lb | 2026-04-20 | torch/CNN | **Reads game source.** No-go. |
| gourabr0y555/arc-agi-3-graph-based-exploration-agent | 2026-04-07 | torch/CNN | **Reads game source.** No-go. |
| ashvinsingh/ash-s-arc-agi-3-agent | 2026-06-10 | torch CNN, prefers CUDA | **Loads pretrained weights** (`/kaggle/input/forge-pretrained-weights/pretrained_weights.pt`). Not prior-free. No-go. |
| mbmmurad/arc-agi-3-lb-0-86-3rd-place-candidate-milestone | 2026-06-30 | Gemma / GPT-OSS / vLLM | LLM. No-go. |

## 5. arXiv (S7, S8)

| paper | LLM at play time | code | verdict |
|---|---|---|---|
| arXiv 2512.24156, Rudakov, Shock, Cowley, graph-based exploration | no | github.com/dolphin-in-a-coma/arc-agi-3-just-explore | already E1a (INCONCLUSIVE, docs/E1_result.md) |
| arXiv 2605.05138, Executable World Models for ARC-AGI-3 in the Era of Coding Agents | yes (a coding agent builds the world model) | github.com/astroseger/arc-3-agents-baseline1 ("released publicly after acceptance" per the search result) | no-go (LLM) |
| arXiv 2607.28287, Tycho | yes ("a coding-agent system"; tested with Claude Opus and GPT models) | github.com/NIMI-research/Tycho | no-go (LLM) |
| arXiv 2605.25931, Explore Before You Solve (AERA) | yes (Qwen2.5-0.5B) | github.com/farmountain/aera-arc3-paper (CC0) | no-go (LLM) |
| arXiv 2608.14490, Twin | yes ("a frontier coding agent writes an executable world model") | github.com/Alexyskoutnev/TWIN-ARC-AGI-3 | no-go (LLM) |
| arXiv 2607.01531, OPINE-World | yes ("an LLM agent") | none found | no-go (LLM) |
| arXiv 2603.24621, ARC-AGI-3 technical report | not an agent | - | cited, not a candidate |

No arXiv paper found presents a non-LLM ARC-AGI-3 agent with released code, other than E1a's.

## 6. Organiser templates: baselines, not independent agents (Section 3.4)

| template | commit / version | LLM / GPU | status |
|---|---|---|---|
| arcprize/ARC-AGI-3-Agents, random agent template | 4743e7d0aaae0ded0d98a89a7e282e63564cd58b (MIT; the changelog's latest is 0.9.3, 2026-01-29; arc-agi >= 0.9.1) | none | **baseline (E1b).** It also holds LLM templates (langchain, openai), which are not baselines here. |
| Kaggle "ARC3 Sample Submission - Random Agent" (inversion) | last run 2026-03-24 | none, CPU | baseline |
| Kaggle "ARC3 Sample Submission - Stochastic Goose" (inversion) | last run 2026-03-24 | torch CNN, GPU flag | baseline; as packaged it is GPU-oriented (A3) |
| Kaggle "ARC3 Sample Submission - Just Explore" (inversion) | last run 2026-03-24 | none | the organisers' packaging of the Rudakov et al. agent, i.e. E1a again; not a new agent |

## 7. What the author can decide from this list

Candidates that could become the second admissible independent agent, in the order the evidence
favours:
1. **ZubMono "Prometheus"** (MIT-0, standard library only, offline, no LLM, current API). First
   step: a line-by-line check of `agent/my_agent.py` for game-specific branches on the 25 public
   game ids; then A5-A7 as for E1a. **Checked and REJECTED (Section 0;
   docs/E1c_prometheus_check.md):** direction priors measured on all 25 public games.
2. **ReplicaWormhole explorer** (MIT). First step: confirm the explorer never calls the model
   client and plays to a fixed budget.
3. **conchocon154 novelty agent** (MIT). Admissible on everything checkable, but its author reports
   it does not beat its random control, so it is probably INCONCLUSIVE; low information.
4. **garlictoday graph explorer** (Kaggle, licence to confirm): a reimplementation of E1a's method;
   the author decides whether it counts as independent evidence.
5. **poby7722 graph explorer** (Kaggle, licence to confirm): carries a cn04-specific setting chosen
   on the public set; the author decides whether that is acceptable (for example, reporting cn04
   apart) or disqualifying.

Could become admissible if their authors add a licence: BDR-Pro v79, Cryptic2-0 GraphExplorer,
Curio, Hunter-Seeker v2.

Deadline for E1c (plan Section 3.4 and CLAUDE.md): 9 October 2026.

## 8. Finding for the related-work section: many high-scoring non-LLM agents use the game's simulator

Most of the higher-scoring non-LLM public agents found load each game's environment source file
(`environment_files/<game>/<version>/<game>.py`) at play time. They instantiate the game class and
search over copies of the live game (`copy.deepcopy`), trying actions on the simulator before
committing to them. They are therefore **not frame-only agents**. Their leaderboard scores are
not comparable with a frame-only measurement such as ours (our agents and E1a see only frames).

This is a statement about what the agents do, from their code; it makes no claim about the
competition's rules.

Evidence, from the sources as downloaded on 26 September 2026 (Kaggle notebooks: the version
current on that date; cell and line numbers count code cells from 0 and lines within the cell
from 1; "last run" is from the Kaggle listing):

| agent | URL | where it finds the source | where it loads it | where it runs the simulator |
|---|---|---|---|---|
| "[0.46] ARC-AGI-3: Persistent Memory BFS ARC Solver" (last run 2026-05-29) | https://www.kaggle.com/code/nihilisticneuralnet/0-46-arc-agi-3-persistent-memory-bfs-arc-solver | cell 1 line 1054: `f"**/environment_files/**/{gid}.py",`; line 1058: `hits = glob.glob(pat, recursive=True)` | cell 1 line 1097: `spec = importlib.util.spec_from_file_location('_arc_game', self.game_path)` | cell 1 line 1108: `return self.game_cls()`; line 874: `g2 = copy.deepcopy(node.game)` |
| "FORGE ARC-AGI-3 Agent" (last run 2026-03-31) | https://www.kaggle.com/code/projectforty2/forge-arc-agi-3-agent | cell 1 line 424: `matches = glob.glob(pattern, recursive=True)` | cell 1 line 55: `spec = importlib.util.spec_from_file_location('game_mod', self.game_path)`; line 58: `self.game_cls = getattr(mod, self.class_name)` | cell 1 line 168: `game = self.game_cls()`; line 96: `g = copy.deepcopy(game)` |
| "[0.35] FORGE v16 Trigger-aware BFS submi3" (last run 2026-04-06) | https://www.kaggle.com/code/itsyoursumit/0-35-forge-v16-trigger-aware-bfs-submi3 | cell 1 line 804: `matches = glob.glob(pattern, recursive=True)` | cell 1 line 59: `spec = importlib.util.spec_from_file_location('game_mod', self.game_path)` | cell 1 line 203: `game = self.game_cls()`; line 113: `g = copy.deepcopy(game)` |
| "ARC-AGI-3: Monte Carlo Tree Search Solver" (last run 2026-04-01) | https://www.kaggle.com/code/nihilisticneuralnet/arc-agi-3-monte-carlo-tree-search-solver | cell 1 line 428: `matches = glob.glob(pattern, recursive=True)` | cell 1 line 436: `spec = importlib.util.spec_from_file_location('_arc_game_mod', src)` | cell 1 line 184: `g = self.game_cls()`; line 283: `g = copy.deepcopy(root.game_ref)` |
| "Hybrid Search-and-Learn Agent / 0.35+ LB" (last run 2026-04-20) | https://www.kaggle.com/code/marynaborovska/hybrid-search-and-learn-agent-0-35-lb | cell 2 line 616: `matches = glob.glob(pattern, recursive=True)` | cell 2 line 45: `spec = importlib.util.spec_from_file_location('game_mod', self.game_path)` | cell 2 line 174: `game = self.game_cls()`; line 109: `g = copy.deepcopy(game)` |
| "ARC-AGI-3 / Graph-Based Exploration Agent" (last run 2026-04-07) | https://www.kaggle.com/code/gourabr0y555/arc-agi-3-graph-based-exploration-agent | cell 1 line 633: `matches = glob.glob(pattern, recursive=True)` | cell 1 line 71: `spec = importlib.util.spec_from_file_location("game_mod", self.game_path)` | cell 1 line 210: `game = self.game_cls()`; line 124: `g = copy.deepcopy(game)` |
| tantan0327/arc-agi-3-agent, `agent/my_agent.py` at commit 77ab2d911e13789ea39e058ac3ad6c788dbd88d3 | https://github.com/tantan0327/arc-agi-3-agent | lines 933-936: `"environment_files/{gid}/*/{gid}.py",` (and Kaggle and /tmp variants); line 946: `hits = glob.glob(pattern.format(gid=gid), recursive=True)` | line 1010: `text = Path(source).read_text(encoding="utf-8")`; line 1017: `exec(text, module.__dict__)` | line 1139: `return copy.deepcopy(game)`; line 981 (comment): "Cost measured on ls20: `deepcopy` 11.7 ms, a simulated action 0.6 ms" |

Not in this group, for contrast: the non-LLM agents in Sections 3.1-3.2 and garlictoday's and
poby7722's notebooks. My searches found no such source loading in them; Cryptic2-0, conchocon154
and ReplicaWormhole's explorer contain no `importlib`/`glob` source loading in the files read.

How to use this in the manuscript: in related work, when public leaderboard scores of non-LLM
entries are mentioned, say that several of the higher-scoring ones search on the game's own
simulator loaded from its source file, name them with these links, and say that such scores are
not comparable with frame-only agents. Do not generalise beyond the agents listed; these are the
100 most-voted notebooks plus the GitHub screen, not all entries.
