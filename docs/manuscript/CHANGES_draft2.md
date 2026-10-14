# Changes from draft 1 to draft 2 of the JOTE manuscript

One row per edit, keyed to the finding IDs of docs/manuscript/REVIEW_draft1.md. No registered number, verdict or quoted registered text was changed. New values entered the text only after scripts/manuscript_numbers.py read them from a committed file: the date 21 September 2026 and the count 18 from docs/HELDOUT.md, the date of the fifth deviation from docs/STATE.md amendment (n), and seven reference URLs from REVIEW_draft1.md Section 6.1. Old and new text are given when shorter than three lines.

| finding | what changed | old → new (when short) |
|---|---|---|
| F01 | Introduction ¶6 rewritten: the split is fixed in a file; it held 18 held-out games until 21 September 2026, when dc22 was moved to development to debug the agent's wall learning, before detailed study; the 17 sources never opened. | "The split between those eight and the other 17 was fixed before development began" → "That file held 18 games in the held-out set until 21 September 2026, when I moved one of them, dc22, to the development set …" |
| F02 | Method, instrument ¶4: the protocol provided for an ARC development truth table and V1; it was never written. Deviations: sixth departure added. Discussion "Why the failure could not show": same fact added. Second-study requirement reworded. | "It would have to write a truth table for the development instance, so that V1 is measured where the parameters are set." → "… and compute V1 there before registration, rather than leave it for later as this protocol did." |
| F03 | Method, instrument ¶4 and Deviations: seventh departure added (I1 registered on ARC-AGI-3, not run under the registered code). | — |
| F04 | Method, Tests: V3 paragraph rewritten (registered row-field check not computed; runner hash check and its logs); Deviations: eighth departure added. | "It holds by construction, because the runner refused to run with any changed file." → "The analysis code does not compute that check, and no V3 line exists among its outputs. …" |
| F05 | Introduction ¶1 and Method, instrument ¶1: the level-end and game-end signals named as inputs. | "It uses the frames of that run and nothing else" → "It uses the frames of that run and the signals that a level or the game has ended, and nothing else" |
| F06 | Purpose: "as registered on the Open Science Framework on 27 September 2026"; Method, preregistration: new paragraph on the differing claim wording of the git-tagged text. | "as registered on 27 September 2026" → "as registered on the Open Science Framework on 27 September 2026" |
| F07 | Abstract, Results nuisance ¶, Discussion nuisance ¶: "every tested line" replaced by "all six primary lines", with the tested/reported split stated. | "on every tested MiniGrid/BabyAI line" → "On all six primary MiniGrid/BabyAI lines" |
| F08 | Results V2 ¶: primitive-action verdicts described as printed, in a reported condition. | "On the primitive-action lines R and I1 fail" → "On the primitive-action lines, which the registered text only reports, the frozen code prints FAIL for R and I1" |
| F09 | Deviations: fifth deviation dated 14 October 2026. | "The fifth was found while this article was written" → "The fifth I found on 14 October 2026, while writing this article." |
| F10 | Discussion ¶2 rewritten; softening and attributed reason removed. | "That matters less than it might seem, because …" → "By the registered outcome table, a V1 failure on any suite decides the outcome by itself, whatever V2 shows." |
| F11 | Conclusion: baseline clause restricted to MiniGrid/BabyAI; long sentence split. | "and a baseline built from …" → "and on MiniGrid/BabyAI a baseline built from …" |
| F12 | Exploratory A1 ¶: both failure routes of the A1 rule named. | "most seeds produced no learned shift for any key" → "most seeds failed the per-seed A1 rule, which fails when no key has a learned shift or when every tried key has the same shift" |
| F13 | Exploratory dissent ¶: learning phase for A2, first-level outcome for A3 and A4. | "where the verdict depends on the planner's first-level outcome" → "where the verdict depends on the course of the planner's run: its learning phase for A2, or its first-level outcome for A3 and A4" |
| F14 | Introduction ¶1: generalizations restricted to the agents studied and stated as the idea tested. | "most of them carry built-in assumptions …; where they fail, the same planner wanders" → "The agents studied here carry built-in assumptions …" and "The idea this study tested is that such an agent does well where its assumptions hold and poorly where they fail." |
| F15 | Results V2 ¶: two sentences added; every Procgen line also misses balanced accuracy (0.5000 against 0.80). | — |
| F16 | scripts/manuscript_figures.py: baseline square unfilled and drawn beneath the census point; fig2.png redrawn. | — |
| F17 | Figure 2 caption: sentence added on the primitive-action FAIL verdicts. | — |
| F18 | Table 2 split into Table 2a (line and verdict, 8 columns) and Table 2b (statistics, 9 columns), same rows and values, with a common caption. | — |
| F19 | Paths, script names and commits removed from the instrument subsection and the exploratory section's first paragraph; constants' file:line moved to the preregistration subsection; the exploratory script, its output and HELDOUT.md named in Data and code availability. Table and figure captions keep their source lines. | — |
| F20 | Table 1 and Table 2 captions map the code identifiers to the prose names. | — |
| F21 | Method: the instrument, suites, tests and deviations paragraphs each split into two or three paragraphs. | — |
| F22 | Long sentences split at L27, L37, L71, L73, L77, L79, L85, L93, L101, L208, L220, L222, L243, L261, L291, L295 (draft 1 lines); the quoted registered claim is unchanged. | — |
| F23 | Semicolons reduced in the Agents, preregistration, Tests and construct paragraphs, and in the Table 1 and 2 captions. | — |
| F24 | AUROC spelled out at first use in the Method; "Open Science Framework (OSF)" introduced in the preregistration subsection. | — |
| F25 | First person where the author is the actor (froze, set, registered, read, tagged, opened, wrote); "my explorer", "my planner", "my agents". | "Every parameter of the census was frozen …" → "I froze every parameter of the census …" |
| F26 | numbers.json and appendix_c.md rebuilt; Table C1 copied unchanged (now lists docs/HELDOUT.md and REVIEW_draft1.md, and STATE.md at its current commit). | — |
| F27 | Method, checks ¶. | "The analysis code passed 20 of 20" → "The analysis code and the determinism check passed 20 of 20" |
| F28 | Method, seeds ¶. | "ran … from 28 September 2026 to 13 October 2026" → "started on 28 September 2026 and had finished by 13 October 2026" |
| F29 | Results nuisance ¶ rewritten; the stray space is gone. | "line : on 6 of 6" → "lines: the three under absolute moves …" |
| F30 | BUILD.md step 4 and the build: --shift-heading-level-by=-1; sections are Heading 1, subsections Heading 2. | — |
| F31 | Same-length runs varied where paragraphs were rewritten for other findings; others left. | — |
| F32 | Figure 2 labels: "absolute moves", "primitive actions", "in range", "camera-distinct". | — |
| F33 | Figure 1 and Figure 3 captions: a sentence on bars of zero. | — |
| F35 | JOTE_CHECKLIST.md J4 line reworded to say what core.xml and app.xml hold; J1 word counts and J3 table list updated. | — |
| F42 | Introduction ¶6: Blum and Hardt (2015) kept as support; Roelofs et al. (2019) cited for what it found. | "it slowly turns into training data (Blum & Hardt, 2015; Roelofs et al., 2019)" → "choices can come to fit it (Blum & Hardt, 2015). Roelofs et al. (2019) measured this effect across many machine learning competitions and found little of it." |
| F43 | Introduction ¶4 and Related work ¶1: both halves of Bontrager et al. (2016) stated. | "found that those features did not predict which controllers succeed" → "A clustering of the games by those features agreed poorly with a clustering by controller performance, … A selection agent built on two of the features did beat each of its constituent controllers on the same games." |
| F44 | Introduction ¶5. | "Bellemare et al. (2012) introduced contingency awareness" → "Bellemare et al. (2012) brought contingency awareness into reinforcement learning, defining contingent regions …" |
| F45 | Related work ¶3: "which they state in complement form"; elimination over places and over features separated. | — |
| F46 | Related work ¶3: Keren et al. bound the number of actions; Wayllace et al. extend it to an expected cost under stochastic outcomes. | — |
| F47 | Related work ¶4. | "the cheapest blind strategy" → "the simplest strategy without reasoning" |
| F48 | Related work ¶4. | "identify goals from frames using visual priors" → "identify goals with a coding agent built on a large pretrained model, which writes an executable world model of each game and so brings a learned prior" |
| F49 | Introduction ¶3. | "where the analysis is fixed" → "where the experimental protocol is fixed" |
| F50 | References: Bellemare, Bontrager, Keren set as periodicals. | "In *Proceedings …* (Vol. 26, No. 1, pp. 864–871)" → "*Proceedings …*, *26*(1), 864–871" |
| F51 | References: URLs added to Bertinetto (with editors), Blum, Cobbe (with editors Daumé III and Singh), Roelofs, Wayllace; OpenReview URLs replace arXiv for Choi and Chevalier-Boisvert. | — |
| — | Exploratory diagnosis: the κ paragraph, split off for F22, opens with "In the same exploratory counts" so that it carries the word (R6). | — |

Not changed, with the reason:

- F34 ("each with care"), F40 (repository public, embargoes), F41 (commit trailers), F52 (MiniGrid 2023 citation) and the title: they need the author's decision (REVIEW_draft1.md Section 7).
- F36 (abstract one paragraph of 240 words), F37 (source lines in table captions), F38 (hyphen-minus in verbatim tables), F39 (section order): no change, for the reasons given in the review.
- The cover letter: no finding required a change.
