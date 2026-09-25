# Ruthless audit of `TOG_PLAN.md`

**Audit date:** 25 September 2026  
**Evidence rule:** all `NEED` items in the supplied plan are treated as nonexistent. All `HAVE` numbers are treated as author-supplied results, not independently certified, because the underlying JSON/run archive was not attached.  
**Scope rule:** claims about the private ARC-AGI-3 evaluation, hidden games, or unverified agent internals are not accepted as evidence.  
**Confidence scale:** **High** = directly supported by a primary source or an explicit technical artifact; **Medium** = supported but dependent on interpretation or incomplete current-public evidence; **Low** = strategic inference, not a published acceptance rate or measured fact.

The supplied plan itself says that RQ4/E1 is load-bearing, that E4/E5 are still `NEED`, that the present study is one home-built frame-only family unless E1 succeeds, and that only the 25 public games can be measured. fileciteturn0file0L28-L40

---

## 1. Verdict in five sentences

As of **25 September 2026, this is not publishable at IEEE Transactions on Games, JAIR, or TMLR in its current form; it is a workshop-level measurement paper, with IEEE CoG only marginally viable after substantial reframing**. The central pieces are already substantially covered by the organisers and prior general-game-playing literature: ARC-AGI-3 itself publishes the squared relative-efficiency score, level weighting, completion cap, goal-acquisition framing, public/private split, and the warning that public-harness performance can fail to transfer, while GVGAI and Kaggle literature already establish the broader train/public-to-held-out selection problem. citeturn693629view2turn693629view4turn436091academia68turn970073search4turn970073search13 A more serious problem is that a 2025 ARC-AGI-3 paper already reported a **training-free graph-exploration agent using visual frames**, solving a median 30/52 preview levels across six games and reaching third place on that preview private leaderboard; that makes a generic title-level claim that “frame-only agents plateau” false unless the manuscript sharply restricts the claim to a specified current public snapshot, architecture family, and compute regime. citeturn468797academia3 ToG becomes defensible only if the paper adds a real claim of its own—most usefully a formal, measurable notion of **goal-identification cost/ambiguity**—and establishes that the observed behavior is not peculiar to one implementation; I estimate **5–10% ToG acceptance as-is versus 25–35% after the two highest-value additions**, where these are reviewer-strategy estimates, not published acceptance rates. The single weakness most likely to kill the paper is the current conversion of a weak planner's descriptive failure counters into the causal sentence **“the barrier is goal inference, not perception or search”** without an intervention that holds perception/search fixed while supplying or withholding goal information; that is a causal conclusion the present evidence does not identify.

---

## 2. Novelty audit table

| RQ / contribution | Closest prior work | Exact overlap | What is actually new | Likely reviewer reading |
|---|---|---|---|---|
| **RQ1 — scoring structure and analytic ceiling** | ARC-AGI-3 Technical Report and scoring definition. The report explicitly defines relative human action efficiency, squares the ratio, weights levels linearly, and caps each environment by the weighted share of completed levels. It also describes ARC-AGI-3 as explicitly rewarding efficient exploration, planning and goal acquisition. citeturn693629view2turn693629view3 | The plan's core verbal claims—squared efficiency, later-level weighting, incomplete-level zero, and a completion-weighted cap—are not discoveries. They are the benchmark's own published design. | A closed-form ceiling for an agent that completes the first `k` levels at a fixed agent/human cost ratio `r`, plus a measured decomposition over the author's runs. The mathematics is a consequence of the public score rule, not a new game-AI result. | **Supporting measurement / filler unless sharpened.** A ToG reviewer can accept benchmark analysis, but not if the paper's contribution is merely “we expanded the organisers' formula into a worked example.” ToG explicitly welcomes Dataset & Benchmark and Negative/Null Results papers, so the issue is contribution depth, not category fit. citeturn304785search0 |
| **RQ2 — selection transfer** | GVGAI learning/generalisation work evaluates knowledge selected on training levels against unseen levels; Balla et al. show substantial difficulty transferring across game/level properties. citeturn436091academia68 Kaggle overfitting work and the public/private leaderboard literature already establish that repeated selection against a public signal can create a hidden-set gap. citeturn970073search4turn970073search13 “Best Agent Identification for General Game Playing” (2025) formalises choosing the best agent/sub-task under limited trials and evaluates this on GVGAI/Ludii. citeturn436091academia74 | “Pick a mechanism on public games; test the pick on held-out games; compare to a per-game oracle” is an established experimental question. The plan's one observed split, `3/17`, does not establish a new phenomenon. | The only plausible novelty is **ARC-AGI-3-specific selection instability induced by its squared efficiency and level weighting**, if measured with a prespecified selection protocol and a proper repeated resampling analysis. The 20-mechanism oracle gap can be a useful empirical measurement, not a new theory. | **Supporting measurement.** Useful, but not a main contribution unless the paper demonstrates a scoring-specific selection law rather than generic benchmark overfitting. |
| **RQ3 — assumption census / self-diagnosis** | “Introspective Environment Modeling” uses explicit environment assumptions that are monitored at runtime. citeturn833489search121 “AgentRx” diagnoses failures from execution trajectories using evidence and failure categories, while 2026 self-correction evaluations also separate task success from diagnostic/correction behavior. citeturn833489search9turn833489academia122 ARC-AGI-3 itself frames goal acquisition and sparse feedback as central design features. citeturn693629view0 | The methodology “instrument an agent, log assumptions, detect which assumption fails, and classify environments by that failure” already exists as a general diagnostic pattern. | A complete per-game census for the ARC-AGI-3 public set, with concrete evidence fields such as key acceptance, controllability, and terminal outcome. | **Supporting measurement, not a new methodology.** It becomes novel only if the census protocol is benchmark-independent, formally defined before observing target games, validated against human/ground-truth annotations, or shown to transfer to another CPU-runnable benchmark. |
| **RQ4 — family study of frame-only agents** | ARC-AGI-3's own technical material says agents must work from frames/short sequences, infer mechanics and win conditions, and acquire goals. citeturn693629view0turn693629view2 More importantly, Rudakov et al. (2025) present **Graph-Based Exploration for ARC-AGI-3**, a training-free graph-based agent using visual frames, reporting a median of 30/52 solved levels over six preview games and third place on the preview private leaderboard. citeturn468797academia3 GVGAI's screen-capture/learning-track literature also establishes frame-driven, rule-free or forward-model-free general-game settings. citeturn436091academia67turn436091search9 | “Frame-only/prior-free agents have difficulty transferring and identifying goals” is not a blank literature space. There is already a directly relevant ARC-AGI-3 frame-based agent that substantially challenged a naive plateau narrative on the preview task. | A **current-competition, public-set, CPU-runnable replication across genuinely independent implementations**, with the exact same scorer/harness and predeclared criteria, would be useful evidence about a particular agent family under a particular compute constraint. | **Load-bearing empirical contribution if E1 is real. Filler if E1 fails.** With only one home-built agent, the paper is fundamentally a case study of that implementation. |
| **RQ5 — CPU-hosted LLM cost per action** | BALROG benchmarks LLM/VLM game agents and explicitly evaluates game interaction, partial success and agent weaknesses. citeturn426000academia98 ARC-AGI-3's own results discuss frontier agents and the role of tool/harness design. citeturn693629view4 | Measuring local model latency against a game-action budget is a systems feasibility calculation, not a new evaluation methodology. | A benchmark-specific lower-bound-style cost calculation showing that a CPU-local 7B/14B model cannot meet the observed per-action budget under the author's exact runtime. | **Filler / engineering note.** Keep it short. It cannot rescue the paper's novelty. Do not use it to infer how every leading competition system is implemented. |

### RQ1 technical correction that must happen before publication

The organisers' technical report contains an internal presentation inconsistency: the displayed scoring equations use a fixed `n=5` example while the same report describes variable-length environments and illustrates environments with more levels. citeturn693629view2turn693629view3 The plan says its formula comes from `arc_agi/scorecard.py`; **that reference implementation, not a prose equation in the report, must be the authority**. The analytic ceiling should be written from the actual implementation and validated against the scorecard on toy cases before any manuscript claim.

For the common case in which an agent completes only the first `k` sequential levels of a game with `N` levels and has a constant agent/human action ratio `r >= 1` on those won levels, the completed-level weight share is

`C(k,N) = [1 + 2 + ... + k] / [1 + 2 + ... + N] = k(k+1) / [N(N+1)]`,

and the efficiency factor is `r^-2` before the benchmark cap. Thus the simple ceiling is `C(k,N) * r^-2` for that restricted case. The cap and any ratio below one must be handled from the implementation, not hand-waved. That derivation is correct only for the specified restricted policy; it is **not** a general upper bound on arbitrary agents unless the completion pattern and cost model are defined carefully.

### The title currently overclaims

“**Why Frame-Only Agents Plateau on ARC-AGI-3**” reads as a benchmark-wide causal/general statement. The evidence available today does not support it. The 2025 graph-exploration paper is a direct published counterexample to a generic plateau claim on an ARC-AGI-3 preview setting, and the current plan has not yet shown E1. citeturn468797academia3 A defensible interim title is closer to **“Scoring, Selection, and Diagnostic Failure Modes of Frame-Only Agents on the ARC-AGI-3 Public Demonstration Set”**. Even that title should wait until the selection protocol and census validity are fixed.

---

## 3. Prior work the plan does not cite and must

### A. ARC-AGI-3 organiser material — mandatory, not optional

1. **ARC-AGI-3 Technical Report.** This is the primary source for the task definition, RHAE scoring, human baseline construction, level weighting, completion cap, public/semi-private/private splits, and the organisers' own discussion of overfitting. The report explicitly says the public set is a demonstration subset and discusses task-specific overfitting/harnesses. citeturn693629view0turn693629view2turn693629view4
2. **ARC-AGI-3 launch announcement.** It defines the benchmark as interactive environments with no instructions/rules/goals and emphasizes exploration, mechanism discovery and goal inference. citeturn730753search0
3. **ARC-AGI-3 Preview: 30-Day Learnings.** This is directly relevant to what was already learned before the current competition and to how much novelty remains in “public games do not generalize.” citeturn730753search3
4. **Measuring Human Performance on ARC-AGI-3.** Human-performance methodology matters because the whole score is human-relative; the paper needs to distinguish the benchmark's human baseline construction from its own empirical data. citeturn730753search5
5. **ARC Prize 2026 Milestone #1 / public winner write-ups.** The paper must discuss the published agent ecosystem, not treat one home-built planner as the only serious alternative. The milestone documentation names Tufa Labs' Duck, Reki and third place, and public code/write-ups exist for at least some winners. citeturn730753search2turn646462search1
6. **Current ARC-AGI-3 competition/leaderboard state.** The Kaggle competition explicitly says the leaderboard and final standings can differ because only part of the test is exposed during the competition. citeturn646462search0 Any manuscript sentence about “the leaders” must therefore be time-stamped and source-specific, not extrapolated from Milestone #1.

### B. ARC-AGI-3 agent literature the plan currently misses

7. **Rudakov, Shock & Cowley, “Graph-Based Exploration for ARC-AGI-3 Interactive Reasoning Tasks” (arXiv 2512.24156).** This is the single most damaging omission. It is directly on ARC-AGI-3, training-free, frame/vision based, and reports strong preview performance. The plan must explain the task-version difference and why the current study is not simply rediscovering a result that already exists. citeturn468797academia3

### C. General-game-playing transfer and frame-driven agents

8. **Balla et al., “Evaluating Generalisation in General Video Game Playing” (CoG 2020 / arXiv 2005.11247).** It evaluates transfer from training levels to hidden levels in the GVGAI learning track, without a forward model and using visual interaction/reward signals. This makes the public-to-held-out transfer framing in RQ2 clearly non-novel in general form. citeturn436091academia68
9. **Kunanusont et al., “General Video Game AI: Learning from Screen Capture.”** This establishes screen-capture learning as an explicit general-game setting. It is relevant background against any claim that frame-driven game learning is a new evaluation regime. citeturn436091academia67
10. **GVGAI Learning Competition / later Learning-track papers.** The learning track was deliberately designed around transfer to unseen levels without explicit game rules or a forward model. Any claim that the plan invented the “train on games/hold out games” experimental logic is false. citeturn436091search9turn436091search14
11. **Stephenson et al., “Best Agent Identification for General Game Playing” (2025).** This is an especially close precedent to RQ2 because it treats the problem of identifying the best agent for each game/sub-task under limited trials. citeturn436091academia74

### D. Public/private leaderboard and selection-overfitting literature

12. **Blum & Hardt, “The Ladder: A Reliable Leaderboard for Machine Learning Competitions” (2015).** Repeated evaluation against an adaptive public leaderboard can overfit; the paper formalises the issue. RQ2 must not be framed as discovering the generic existence of leaderboard overfitting. citeturn970073search13
13. **Roelofs et al., “A Meta-Analysis of Overfitting in Machine Learning” (NeurIPS 2019).** A large empirical study of Kaggle-style competitions found that leaderboard overfitting exists but is not uniformly dominant. This is important because the plan's hypothesis should be a measurable benchmark-specific effect, not an assumed universal phenomenon. citeturn970073search4

### E. Agent diagnosis / assumption verification

14. **“Introspective Environment Modeling.”** Explicitly constructs and monitors assumptions under which an agent's operation is valid. This makes the plan's phrase “verifies its own assumptions” non-novel at the methodological level. citeturn833489search121
15. **AgentRx: Diagnosing AI Agent Failures from Execution Trajectories (2026).** Uses execution traces and structured failure categories for agent diagnosis. A ToG reviewer will recognise the census idea as part of a broader trajectory-diagnosis literature. citeturn833489search9
16. **2026 work on evaluating self-correcting vision agents.** This similarly treats diagnosis as a measurable object rather than merely an informal narrative. The plan must distinguish its contribution from generic failure taxonomy. citeturn833489academia122

### F. Game-agent evaluation efficiency

17. **Atari efficiency/sample-efficiency literature.** Human-relative game scores and efficiency/sample-efficiency have a large prior literature; “humans as denominator” is not a new evaluation idea. See the human-efficiency Atari line of work such as BBF. citeturn460733academia2
18. **BALROG.** It benchmarks LLM/VLM agents over diverse games including NetHack and evaluates game interaction beyond a single scalar success rate. The CPU-LLM section should cite this and remain a feasibility subsection, not a novelty pillar. citeturn426000academia98
19. **NetHack Learning Environment / MiniHack.** These are relevant CPU-runnable candidates if a second-benchmark validation is added; they provide mature interactive environments with exploration/planning challenges and are much cheaper to execute than large GPU-centric benchmark suites. citeturn426000academia94turn426000academia95

### G. What I did **not** verify

- I did **not** locate a standalone ARC-AGI-3 scoring-methodology page that supersedes the technical report/reference implementation; the report and implementation are the evidence base I found.
- I did **not** verify the exact public repository/license/CPU runtime of the plan's unnamed “0.26–0.27” agent from the information supplied. Treat that agent as **not verified**, not as an established external replication.
- I did **not** verify a second current-competition CPU-only frame agent from the Kaggle code tab. Do not write “three public agents exist” until exact repository, commit, license and runtime evidence exists.
- I did **not** verify current 2026 IEEE CoG page/fee numbers from the call page in this audit. Do not import page limits from an older CoG edition.

---

## 4. Feasibility of E1 (the family study)

### E1 is currently **NO-GO**

The plan's own decision rule correctly identifies E1 as load-bearing: without independent agents, the manuscript reduces to a study of BRUTUS-G/hash-state/G-NAV behaviour. fileciteturn0file0L73-L86 The problem is that the candidate pool in the plan is not yet demonstrated to satisfy the three requirements that matter simultaneously: **independent implementation, current-task compatibility, and CPU-runnable/reusable under a disclosed licence**.

| Candidate | What is actually verified | Licence | CPU-runnable | Current 2026 competition compatibility | Verdict for E1 |
|---|---|---|---|---|---|
| **Graph-Based Exploration for ARC-AGI-3** (Rudakov et al.) | Yes: directly published as a training-free graph-based ARC-AGI-3 agent using visual frame processing; strong preview result and third-place preview private ranking are reported. citeturn468797academia3 | **Not verified in this audit.** | **Not verified in this audit.** The paper does not establish the CPU runtime needed by this plan. | **Not exact.** It targets the ARC-AGI-3 preview challenge, not the present 25-game public demonstration snapshot. | **Best candidate, but not yet admissible.** If the repository is licensed and actually runs on CPU in the current environment, it becomes the first genuine external family member. |
| **Official non-LLM template agents** referenced by the plan | The plan names an official repository, but the supplied plan does not contain the exact commit, licence or runtime. | **Not verified.** | **Likely testable, but not verified here.** | Potentially yes, but exact current API compatibility must be demonstrated. | **Baseline, not independent evidence.** An organiser template should not be counted as an “independent research implementation” unless the paper defines independence carefully. |
| **Public CPU-only 0.26–0.27 agent** | **Not verified.** The audit did not establish an exact repository/commit from the supplied citation. | **Not verified.** | **Not verified.** | **Not verified.** | **Do not count until traceable.** |
| **Third Kaggle code-tab notebook** | **Not found/verified.** | Unknown. | Unknown. | Unknown. | **No evidence yet.** |

### What the published record already does to E1's hypothesis

The 2025 graph-exploration result is not a minor nuisance. It means the manuscript cannot treat “frame-only” as synonymous with “doomed to level-1.” A reviewer can immediately ask: **why is the current study contradicting a published ARC-AGI-3 graph-exploration result?** The answer can be legitimate—different benchmark snapshot, different game subset, different compute envelope, different scorer, different architecture—but the paper must actually measure those differences. citeturn468797academia3

### E1 design changes required

1. **Pre-register the comparison before running external agents.** The current thresholds `<0.5`, `AT HUMAN / recorded > 5`, and `lv3+ = 0` appear to have been defined from the author's existing results. If the thresholds are adjusted after seeing external-agent results, the family claim becomes outcome-conditioned.
2. **Primary analysis must use one homogeneous evaluation matrix.** The plan proposes both 20 mechanisms × 1 seed and 6 mechanisms × 4 seeds for E5, which is not a clean selection matrix. E1 should likewise use identical game files, engine commit, budget, reset policy, score extraction and action accounting.
3. **Treat the 25 public games as a public demonstration set, not a random sample of ARC-AGI-3.** The organisers explicitly distinguish the public demonstration subset from the private evaluation. citeturn693629view2
4. **Do not call the result a “frame-only ceiling.”** At most it is an empirical plateau under a stated agent/compute family on the public set.
5. **Do not use organiser templates as the only external confirmation.** That would be a baseline replication, not an independent family study.

### Go / no-go decision

**No-go today.** Proceed with E1 only if, before 9 October, there are **at least two externally authored, licensed, runnable implementations** whose current action loop can be instrumented without altering their policy logic. If this fails, remove RQ4 from the central claim and recast the paper as a benchmark/scoring/diagnostic measurement note. Do not keep the family title and hope reviewers ignore the missing experiment.

---

## 5. What is missing, ranked, with cost and probability of completion

These are **strategic estimates**, not measured facts. Probability is the probability that one independent author with the stated CPU-only resources can finish the addition by approximately **23–31 October 2026**.

| Rank | Addition | Why it changes the paper | CPU / engineering cost | Calendar cost | Finish probability by late Oct. |
|---|---|---|---|---|---:|
| **1** | **A real E1: two or more independent, licensed frame-based agents on the current public 25 games** | Converts “my planner fails” into an externally replicated measurement and directly answers the single most obvious reviewer objection. It is also necessary to discuss the published graph-exploration counterexample honestly. citeturn468797academia3 | Integration dominates. Expect **10–80 CPU-hours per agent** if the code is lightweight; materially more if visual encoders are slow. GPU access is not acceptable as a hidden requirement. | **3–10 days** if repositories run; **2+ weeks** if adapters/licences/API changes are messy. | **35–50%**. The probability is low because candidate discovery, licensing and runtime are the bottleneck, not compute. |
| **2** | **Formal “goal-identification cost” / goal-ambiguity result, tied to black-box observations and actually measured** | Gives the paper a claim not already contained in the organiser report: a formal object that quantifies how many interactions are needed before candidate goal hypotheses become distinguishable. This is the cleanest route from a measurement paper to a paper with a conceptual contribution. | Mostly CPU-light. **20–80 CPU-hours** for hypothesis enumeration / trace analysis; the hard part is mathematical specification, not compute. | **10–18 days** including proof polishing and adversarial examples. | **45–60%**. Higher only if the definition is kept narrow enough to prove and implement. |
| **3** | **Benchmark-independent validation on a second CPU benchmark, preferably GVGAI Learning Track** | Converts “ARC-AGI-3 taxonomy” into a general diagnostic protocol. GVGAI already provides a transfer/generalisation environment with no explicit game rules/forward model in the learning track. citeturn436091academia68turn436091search9 | **20–60 CPU-hours** for a small, fixed study; Java/environment integration may dominate. | **7–14 days**. | **60–70%**. Feasible, but only if the diagnostic definitions transfer without ad hoc rewriting. |
| **4** | **Direct comparison to organiser baselines and published ARC-AGI-3 agents** | Prevents the paper from discussing “frame-only” in a vacuum and forces an honest explanation of where the result sits relative to existing ARC-AGI-3 work. citeturn730753search2turn468797academia3 | **2–8 CPU-hours** plus literature/data extraction; almost no new compute. | **1–3 days**. | **90–95%**. |
| **5** | **Repair E5 into a prespecified game-level selection protocol** | Makes the selection-transfer result statistically defensible. Use a fixed mechanism set, hierarchical seed handling, selection regret, rank stability and a simple holdout protocol rather than mixing heterogeneous one-seed and four-seed matrices. | **Seconds to a few hours** after logs are organised. | **1–3 days**. | **90–95%**. |
| **6** | **Source-access chronology + protocol lock + immutable pre-holdout code hash** | Converts the “I read three public training game sources” problem from a trust question into a documented experimental provenance question. | Near-zero compute. | **1–2 days**. | **95%+**. |
| **7** | **10-seed hierarchical analysis / exact game-level counts** | Removes the current pseudoreplication risk. Seeds are nested inside games; seed replication cannot be used to imply that 17 games are a large sample. | **10–30 CPU-hours** depending on re-runs. | **1–3 days**. | **90%**. |
| **8** | **14B CPU LLM section** | Improves the feasibility note but does almost nothing for the core novelty. | As planned, **2–4 hours per machine** if the model is already available and memory is adequate; longer if repeated. | **1–2 days**. | **85–95%**. |

### The single addition that most improves the paper

**Turn “goal inference” from an interpretation into a measurable scientific object.** Define a bounded set of goal hypotheses `G`, define the observable interaction history `H_t`, and define the **goal-identification cost** as the first interaction budget at which the observations distinguish one or more goal classes to a stated confidence/identifiability criterion. Then prove a restricted ambiguity result—e.g., that when two goal predicates induce the same observable terminal/non-terminal histories under the available action policy class, no black-box frame-only learner can identify the intended goal within that horizon—and measure the quantity on the 25 public games. This is the step that changes the manuscript from “we counted why our planner failed” into “we introduced and validated a quantitative property of sparse-feedback interactive benchmarks.” It must not be an elaborate new algorithm; the contribution is the definition, theorem, estimator, and evidence.

### The single weakness that most likely kills the paper

**The causal leap from census to mechanism.** The plan currently ends up saying “the barrier is goal inference, not perception or search,” but its measurements do not isolate those causes. A planner can fail to confirm a goal because its hypothesis set is wrong, because it cannot perceive the relevant object, because its exploration policy never visits the informative state, because its reset policy destroys evidence, or because the terminal condition was outside its heuristic language. Unless the experiment supplies goal information while keeping the perceptual/search stack unchanged—or otherwise proves an identifiability claim—the paper can say only **“goal identification is the dominant observed failure mode for this instrument on this public subset”**, not “the barrier is goal inference.”

---

## 6. Venue table

**Important:** the percentages below are **review-strategy estimates**, not venue acceptance rates. They are based on the supplied plan, the current evidence base, and the stated additions. They should not be read as statistical probabilities.

| Venue | Fit | As-is acceptance estimate | With top two additions* | Page / fee constraints | Review / decision timing | Desk-reject risk |
|---|---|---:|---:|---|---|---|
| **IEEE Transactions on Games** | **Direct topical fit.** ToG explicitly lists games for AI, AGI, evaluation, and it explicitly welcomes Dataset & Benchmark, Instrumentation & Infrastructure, Replication, and Negative/Null Results papers. citeturn304785search0turn304785search1 | **5–10%** | **25–35%** | Full papers **10–14 pages**; fees apply above 10 pages, with mandatory overlength charges above the 10-page threshold. The current plan's 12-page target therefore creates a fee problem for a no-budget author. Keep the archival paper to **10 pages + supplement** unless the fee policy changes. ToG states double-anonymous review for submissions from 2025 onward. citeturn304785search0 | ToG says the full review process is ordinarily targeted at **≤3 months** after initial vetting, with normally 3 reviewers. citeturn304785search0 | **High as-is.** The combination of one agent, public-only sample, organiser-overlap and causal overclaim is enough for prescreen rejection. |
| **JAIR** | AI-wide journal with strong expectations for new results/insights of broad AI interest. citeturn348968view1 | **1–3%** | **8–15%** | No publication fee stated by the current author information; reproducibility checklist is mandatory. No strict article page limit, but format rules are strict. citeturn348968view1 | Approx. **8–12 weeks** to decision is the journal's stated target. citeturn348968view1 | **Very high.** The current paper is too benchmark-specific and descriptive for JAIR's stated expectation of significant AI-community insight. |
| **TMLR** | Reasonable only if the paper becomes a methodological/evaluation contribution rather than an ARC-AGI case report. TMLR allows arbitrary length with justification and uses double-blind review. citeturn348968view2 | **5–10%** | **20–30%** | Any length, justified; supplementary material allowed. Current guide does not state an APC in the surfaced author-guide material; verify at submission time. Double blind. citeturn348968view2 | Open-ended review/rebuttal cycle; no simple fixed 8–12 week promise from the cited guide. citeturn348968view2 | **High.** The present contribution is not broad enough. |
| **Scientific Reports** | Scope can accommodate a technically sound benchmark/evaluation paper, and its review policy explicitly emphasises scientific validity/technical soundness rather than novelty alone; it can publish niche and negative results. citeturn329219search1turn329219search4 | **20–30%** | **35–50%** | Fully open access; exact current APC was **not verified in this audit**. That practical cost makes it a poor fit for the stated no-APC budget unless a waiver applies. | First editorial decision target around **45–48 days** in current guidance. citeturn329219search6 | **Medium.** Lower novelty risk than JAIR/ToG, but APC and the public-only benchmark limitation remain practical/technical problems. |
| **Applied Intelligence** | Broad AI fit, but current scope stresses new/original research and technological developments on complex real-life problems. citeturn348968view3 | **10–20%** | **25–40%** | Hybrid model. Exact current page/fee conditions were **not fully verified** from the surfaced journal material; confirm before submission. | Current site reports median first decision around **45 days**. citeturn348968view3 | **Medium–high.** A pure ARC-AGI-3 measurement note may look too narrow without a general diagnosis/goal-identification contribution. |
| **IEEE CoG** | **Strong topical fit** for game AI/benchmark evaluation. The publication record includes GVGAI learning/general-game papers. citeturn436091search14 | **15–25%** | **35–50%** | **2026 page limit/fee policy not verified in this audit.** Do not reuse ToG numbers. | Conference decision schedule depends on the specific 2026 call; **not verified here**. | **Medium.** Conference review is more plausible than journal review, but the same novelty problem remains. |
| **Workshop** | **Best fit as-is** for an early measurement/replication paper or negative result that cannot support a journal-level general claim. | **55–75%** | **75–90%** | Depends on the specific workshop; exact 2026 workshop not selected in the plan. Fees/page limits **not verified**. | Typically much faster than journal review, but workshop-specific. | **Low–medium** assuming the workshop is actually about AGI/game agents/benchmarking. |

\* **Top two additions:** (1) a genuine E1 with at least two independent licensed/runnable agents, and (2) a formal measurable goal-identification cost/ambiguity result with a restricted proof and empirical evaluation.

### Practical venue decision

For the stated resource constraint, **ToG is the only journal on this list whose scope is an obvious match and whose current policy explicitly welcomes benchmark/replication/negative-result categories—but the manuscript must fit 10 pages to avoid mandatory overlength charges.** citeturn304785search0 JAIR is free but is a poor match for the paper's current novelty level. TMLR is technically viable only after the paper becomes a general evaluation contribution. Scientific Reports is a technically realistic outlet for a careful negative/measurement paper, but the author's no-APC constraint makes it practically unsuitable unless a waiver is secured. Applied Intelligence is possible only after a general AI-methodology angle is added. IEEE CoG is a more realistic archival target than JAIR/TMLR if the conference accepts the benchmark framing, but the current 2026 call details were not verified.

---

## 7. Fatal flaws and disclosures

| Issue | Severity | Why a reviewer will care | Required handling |
|---|---|---|---|
| **Training-source code was read for `tu93`, `dc22`, `ls20`** | **Not inherently disqualifying; disqualifying if hidden.** | Kaggle discussion explicitly indicates that the public 25 environment files are open source and may be accessed. citeturn646462search8 So source access itself is not a rule violation. But a source-informed agent/taxonomy cannot be presented as an untouched observation of those games. | State the exact games, dates/commits if available, what source information was viewed, and whether any code/counters were changed afterward. Treat those games as **source-informed controls**, not as evidence for a source-independent held-out census. Preserve the pre-held-out code hash if the claim is that diagnostics were frozen before held-out execution. |
| **Public 25-game benchmark only** | **Fatal to broad generalisation, not fatal to a descriptive paper.** | The organisers distinguish the 25 public demonstration games from 110 private evaluation games and explicitly discuss public-set overfitting/task-specific harnesses. citeturn693629view2turn693629view4 | Every broad statement must say **“on the 25 public games”** or **“on the public-set held-out split.”** Never call 17 games “the unseen ARC-AGI-3 test set.” |
| **17-game census** | **Fatal if used for inferential generalisation.** | Seventeen authored public games are not an independent random sample of a larger distribution. Seeds do not turn 17 games into hundreds of independent observations. | Report exact counts. If CIs are shown, use a hierarchical design with games as the primary unit and seeds nested inside games. Do not use seed replication to imply population certainty. |
| **One home-built agent if E1 fails** | **Fatal to the family claim.** | The paper title and RQ4 say “frame-only agents,” but one implementation supports only “this implementation.” | If E1 fails, remove the family claim and rename the paper accordingly. Do not retain the current title. |
| **“The barrier is goal inference, not perception or search”** | **Fatal unless causal evidence is added or wording is downgraded.** | The census is diagnostic, not an intervention. Different planner weaknesses can create the same observations. | Replace with a descriptive statement unless A2—the formal goal-identification result—actually isolates the information bottleneck. |
| **“Every leaderboard leader runs a GPU-served vision model”** | **Unsupported; cut.** | The current competition leaderboard is dynamic, and the public milestone winners do not exhaust the set of current leading entries. Kaggle itself warns that standings can change between public and final scoring. citeturn646462search0 Published implementation details exist for some agents, not all leaders. citeturn730753search2turn646462search1 | Name only agents whose implementation/hardware is documented, and attribute the claim to the source. Never extrapolate from a few published systems to all leaders. |
| **Current 12-page ToG plan with no budget** | **Practical submission blocker.** | ToG currently states mandatory overlength charges above 10 pages for full papers. citeturn304785search0 | Target **10 pages exactly**, using supplement for full per-game tables/logs. Do not plan on a 12-page accepted paper under a zero-fee constraint. |
| **Live competition** | **Not fatal if snapshot is fixed.** | Results and leaderboard state will change before 2 Nov 2026. | Freeze game set/version, engine versions, scorer commit, date and leaderboard snapshot. Do not update the core claims opportunistically after seeing later leaderboard results. |
| **Public-set selection protocol** | **Serious methodological weakness.** | If mechanism selection is designed after seeing the same games used to evaluate it, the paper risks demonstrating its own tuning process rather than transfer failure. | Predeclare the mechanism set and selection statistic; use one homogeneous matrix for the primary analysis; report the exploratory larger mechanism set separately. |
| **Current E5 mixes 20 mechanisms × 1 seed with 6 mechanisms × 4 seeds** | **Serious.** | Selection performance and seed variance are confounded across the matrices. | Make the 6×4 matrix primary if complete; treat 20×1 as exploratory sensitivity analysis, or rerun the full fixed matrix if necessary. |
| **Use of `tu93` as “positive control” after its source was read** | **Not fatal if clearly labelled; fatal if passed off as blind evidence.** | The source-read status changes the information available to the researcher. | Label “source-informed positive control.” Keep it visually and statistically separate from the 17-game held-out census. |
| **No attached run JSONs** | **Fatal for external audit of HAVE numbers, but fixable.** | A reviewer cannot reproduce the author's 1,088-run claims from prose. | Include all raw scorecards, manifests, seeds, engine versions and SHA-256 hashes in the anonymised repository/supplement. The plan itself already proposes this; execute it. fileciteturn0file0L106-L108 |

### How the source-reading disclosure should read in substance

The manuscript should say, plainly, that the public environment source for `tu93`, `dc22`, and `ls20` was inspected while debugging; that no held-out public-set game source was intentionally opened; that those three games are therefore not independent source-blind evidence; and that the final taxonomy and evaluation protocol were frozen before the first held-out run if that is true. Do **not** imply that reading public source was forbidden—it was not, according to the competition discussion. citeturn646462search8

### What the single-author status changes

A single author is not a scientific flaw. The flaw is **single-implementation evidence presented as a family property**. The paper can survive solo authorship; it cannot survive a family claim unsupported by independent implementations.

### Statistical unit warning

The plan currently says “every mean over games is reported with a bootstrap 95% interval over seeds and, where the claim is about games, over games.” fileciteturn0file0L113-L121 That needs redesign. The correct conceptual hierarchy is approximately:

`games -> seeds within game -> actions within run`.

Action steps are not observations for game-level uncertainty; seeds are not new games. A paper that bootstraps 10 seeds and then implies that it has strong evidence about the 17-game population is vulnerable to an immediate pseudoreplication critique.

---

## 8. Rewritten abstracts

### 8A. Abstract supported by the evidence currently marked HAVE

> **Abstract — current evidence only.** ARC-AGI-3 is an interactive benchmark in which agents receive no explicit game instructions and are evaluated partly by action efficiency relative to human performance. We analyze the scoring rule and measure a frame-based, prior-free, CPU-runnable navigation system on the 25-game public demonstration set. The benchmark squares the human-to-agent action ratio, weights later levels more heavily, and caps environment credit by the weighted share of levels completed. From this rule we derive a closed-form ceiling for restricted policies that complete the first *k* levels at a fixed action-cost ratio. In 1,088 supplied runs, the measured system obtained its observed score from first-level successes, and increasing the action budget fivefold changed the reported mean score by 0.03. We also measure mechanism-selection transfer across a public-set split and use runtime counters to catalogue observed failure conditions on 17 public-set held-out games. These results are descriptive of the measured implementation and benchmark snapshot; they do not establish a limit for ARC-AGI-3 as a whole or make claims about the private evaluation. The scoring decomposition, diagnostic harness, and run records are released.

**Reviewer judgment:** this abstract is honest, but it describes a **measurement paper with no strong novel result**. That is the correct description of the current evidence.

### 8B. Abstract if the top two additions are actually completed

> **Abstract — after E1 + formal goal-identification contribution.** ARC-AGI-3 is an interactive benchmark in which agents must infer mechanics and objectives from interaction while being evaluated by human-relative action efficiency. We study the benchmark's public demonstration set using multiple independently authored frame-based agents under a common CPU-runnable evaluation harness. First, we derive the exact score ceiling for agents that complete only the first *k* levels at a fixed human-relative action cost and quantify how squared efficiency and level weighting amplify the cost of incomplete progression. Second, we introduce **goal-identification cost**, a black-box measure of the interaction required to distinguish competing goal hypotheses from observable frames, actions and terminal feedback, and prove a restricted ambiguity result for indistinguishable observation histories. We evaluate the measure across the 25 public games and compare it with the failure traces of independent frame-based agents. The resulting analysis separates failures attributable to unavailable control signals from failures attributable to unresolved goal hypotheses and from failures specific to a planner implementation. We additionally quantify public-set mechanism-selection regret. All claims are restricted to the measured public snapshot; no private-test performance is inferred. Code, scorecard decompositions and raw run records are released.

**Reviewer judgment:** this is the version that has a defensible central claim. It still needs careful language around what the theorem actually proves and must survive the published 2025 graph-exploration result. citeturn468797academia3

---

## 9. Checklist of yes/no questions before submission

Answer **YES** or **NO** to every item. A single **NO** in the “red” group means the paper is not ready.

### Red — submission blockers

- [ ] **YES/NO:** Can every number in the abstract be traced to an immutable JSON/run manifest and exact code commit?
- [ ] **YES/NO:** Is E1 backed by at least **two independent externally authored agents** that are licensed, runnable, and actually executed on CPU with the current benchmark API?
- [ ] **YES/NO:** If E1 is not complete, has every family-level statement and the current title been removed?
- [ ] **YES/NO:** Has the 2025 graph-exploration ARC-AGI-3 paper been discussed as a direct prior and explained rather than ignored? citeturn468797academia3
- [ ] **YES/NO:** Is the statement “goal inference, not perception or search” backed by an intervention or a formal identifiability result, rather than only planner counters?
- [ ] **YES/NO:** Is every broad conclusion explicitly limited to the **25 public demonstration games** and never the private evaluation?
- [ ] **YES/NO:** Are the 17-game public-set held-out games treated as a descriptive sample rather than a random sample of ARC-AGI-3?
- [ ] **YES/NO:** Is the 12-page ToG draft reduced to **10 pages or fewer** if the author cannot pay mandatory overlength charges? citeturn304785search0
- [ ] **YES/NO:** Are `tu93`, `dc22`, and `ls20` explicitly disclosed as source-read games and separated from source-blind held-out evidence? citeturn646462search8
- [ ] **YES/NO:** Does the final manuscript avoid the sentence or equivalent claim that every leaderboard leader uses a GPU-served vision model?

### Yellow — statistical and experimental integrity

- [ ] **YES/NO:** Was the selection protocol fixed before the held-out analyses were inspected?
- [ ] **YES/NO:** Is the primary E5 matrix homogeneous in mechanisms, seeds, score extraction and evaluation budget?
- [ ] **YES/NO:** Are seeds explicitly nested within games in the uncertainty analysis?
- [ ] **YES/NO:** Are game-level claims based on game-level replication rather than seed count?
- [ ] **YES/NO:** Are the E1 decision thresholds fixed before seeing external-agent outcomes?
- [ ] **YES/NO:** Is the scorer implementation versioned and archived?
- [ ] **YES/NO:** Has the analytic ceiling been checked against the actual `scorecard.py` implementation, including the environment cap and all boundary cases?
- [ ] **YES/NO:** Has the apparent `n=5` inconsistency in the organiser report been resolved by reference to the implementation rather than copied into the paper? citeturn693629view2
- [ ] **YES/NO:** Are any source-informed games labelled as such in tables and figures?
- [ ] **YES/NO:** Is the current leaderboard quoted only with an explicit date and source snapshot? citeturn646462search0

### Novelty gate

- [ ] **YES/NO:** Can the introduction state in one paragraph what the paper proves or establishes that the ARC organisers, GVGAI literature, Kaggle leaderboard literature, and agent-diagnostics literature did **not** already establish?
- [ ] **YES/NO:** Is that novelty still true if all claims about the private test set are deleted?
- [ ] **YES/NO:** Is the census protocol reusable on a second benchmark without rewriting its categories after looking at the target games?
- [ ] **YES/NO:** Does the paper contain at least one result whose validity does not depend on believing that the home-built planner is representative?
- [ ] **YES/NO:** Is the LLM latency section visibly secondary to the core scientific contribution?

### Reproducibility and anonymity

- [ ] **YES/NO:** Does the anonymised repository omit GitHub usernames, Kaggle handles, affiliation clues and self-identifying acknowledgements for double-anonymous review? The plan already recognises this requirement. fileciteturn0file0L143-L148
- [ ] **YES/NO:** Are all environment/engine versions, seeds, budgets, resets and scorer commits recorded?
- [ ] **YES/NO:** Does a fresh CPU machine reproduce every headline table from the repository without manual edits?
- [ ] **YES/NO:** Are all failure anomalies, including `ar25`, retained rather than silently removed? The supplied plan says they should be. fileciteturn0file0L55-L61
- [ ] **YES/NO:** Does the final discussion explicitly state that the public 25 games are a benchmark demonstration subset, not the private evaluation population? citeturn693629view2turn693629view4

---

## Bottom line

**Do not submit the current plan as a ToG paper.** The present evidence is enough for a rigorous public-set measurement note, not enough for the causal “why frame-only agents plateau” claim in the title. The organiser already published most of RQ1's conceptual content, general-game literature already contains the transfer question in RQ2, the diagnostic machinery in RQ3 is not methodologically new, RQ5 is ancillary, and RQ4—the one part that could make the family claim real—does not yet exist. citeturn693629view2turn436091academia68turn833489search121turn426000academia98

The route out is narrow but concrete: **first make E1 real with independent agents; then turn “goal inference” into a formal measurable information problem rather than an interpretation of one planner's counters.** A second CPU benchmark, organiser-baseline comparison, and cleaned-up selection analysis then strengthen that core. Without that sequence, the paper should stop at workshop level rather than spending weeks polishing a journal manuscript whose central novelty is already visible as derivative.
