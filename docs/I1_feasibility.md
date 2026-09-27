# I1_feasibility.md — can the Rudakov et al. agent run on suites B and C?

Written 27 September 2026 (W2). Agent: Rudakov, Shock & Cowley, "Graph-Based Exploration for ARC-AGI-3 Interactive Reasoning Tasks" (arXiv:2512.24156), MIT licence, code in external/rudakov_just_explore (commit and file hashes in its PROVENANCE.md). The E1 adapter is scripts/e1_rudakov_adapter.py, and its boundary changes B1–B7 are in docs/E1_rudakov_feasibility.md Section 5.

**Verdict: adaptable through the same contract, with boundary changes only and none inside their files.** Whether it plays usefully on B and C is not known and is not claimed. That is what the runs measure.

## What it hard-codes (read from source)

| # | hard-coded | where | effect on B and C |
|---|---|---|---|
| H1 | frame shape 64 × 64 | agents/heuristic_agent.py:501 (`self.frame_shape = (64, 64)`), used by the status-bar rules 616-622, 707-719 | needs a 64 × 64 frame: suite B through the canvas (ADAPTER_FEASIBILITY item 12); suite C natively |
| H2 | colour 16 is their status-bar marker: status-bar cells are set to 16, and 16 is set back to 0 before hashing | heuristic_agent.py:216, 248, 503 | a palette index 16 would be merged with the marker and then with 0. Suite C (indices up to 64) and larger suite-B palettes reach 16 |
| H3 | 16-colour ARC palette for click salience: colours 6–15 are "salient" | heuristic_agent.py:507 (priority tiers for clicks) | clicks are not offered on B or C (ACTION6 absent), so the tiers never run |
| H4 | keys: only ACTION1–ACTION5 are mapped; no ACTION7 | heuristic_agent.py:54-58; agents/structs.py (their enum ends at ACTION6) | it can press five mapped actions per suite, one fewer than R and N |
| H5 | frame fields of the preview API: `FrameData.frame` (list of 2-D grids), `state`, `score` (levels), `available_actions` | agents/structs.py:206-214 | built by the E1 adapter's `to_their_frame` from the arc_agi observation (e1_rudakov_adapter.py:148-155), which the shim supplies unchanged |
| H6 | `score` is bounded 0–254 by pydantic (`Field(0, ge=0, le=254)`) | agents/structs.py:210 | a run with more than 254 level ends (possible on short MiniGrid tasks) would fail validation |
| H7 | the level-up rule resets their graph and status-bar mask when `score` changes | heuristic_agent.py:472-478 | works as on ARC once `score` = levels_completed (B2) |
| H8 | the environment is created by `from arc_agi import Arcade` in the E1 adapter | e1_rudakov_adapter.py:216-221 | the ARC shim (scripts/env_frame.py) replaces arc_agi, so their adapter's own calls reach suite B or C |

## Boundary changes needed (as in docs/E1_rudakov_feasibility.md Section 5; none inside their files)

| # | change | where | why |
|---|---|---|---|
| C1 | install the ARC shim before the E1 adapter imports `arc_agi` | a new runner wrapping scripts/e1_rudakov_adapter.py's play function | presents suite B or C as an arc_agi environment (ADAPTER_FEASIBILITY Section 1) |
| C2 | key map: their ACTION1–5 → the first five entries of the suite's key map (ADAPTER_FEASIBILITY items 9–11) | the shim's key map | H4. On suite B raw: left, right, forward, pickup, drop (no toggle). On macro: north, south, west, east, pickup. On C: up, down, left, right, special 1 |
| C3 | palette index k ≥ 16 presented as k + 1, for I1 only | the shim's frame conversion for I1 runs | H2: no game colour may equal their marker 16 |
| C4 | `score` = min(levels_completed, 254) | the E1 adapter's `to_their_frame` input, via the shim | H6. After 254 level ends I1 no longer sees level ends; the count reached is recorded in the row |
| C5 | B1–B7 of the E1 adapter unchanged | scripts/e1_rudakov_adapter.py | as on ARC |

C2–C4 are parameters PREREG v1 did not register. They are listed in docs/ADAPTER_FEASIBILITY.md item 18 for PREREG v1.1.

## Limits stated with the result

- **It has five actions where R and N have six.** On suite B raw it lacks toggle, so doors cannot be opened; this depresses its completion on door environments. On the other conditions it lacks the sixth mapped action.
- **Its preview-era assumptions (H2, H3) were built for ARC.** A poor showing on B or C may reflect them rather than the census's prediction. V2 reports I1 per suite with this caveat.
- **If the I1 runs fail for a technical reason in the pilot** (not for poor play), the sentence the paper carries is PREREG Section 2's: *"No independent agent could be run outside ARC-AGI-3; on suites B and C, V2 rests on the author's explorer R alone, and the predictive claim there is narrowed to 'predicts the author's explorer'."*
