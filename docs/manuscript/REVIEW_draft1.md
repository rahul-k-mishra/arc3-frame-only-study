# Review of JOTE manuscript draft 1 (14 October 2026)

Object of review: docs/manuscript/manuscript.md and docs/manuscript/manuscript.docx at commit 350f68b, with cover_letter.md, JOTE_CHECKLIST.md, fig1.png to fig4.png and numbers.json. Sources read: docs/PREREG.md (v1, v1.1 diff D1 to D15, v1.2 diff D16), docs/STATE.md amendments (d) and (h) to (n), docs/OSF_REGISTRATION_final.txt, docs/OSF_REGISTRATION_v1_1_final.txt, docs/HELDOUT.md, docs/EXPLORATORY_V1_DIAGNOSIS.md, docs/GROUND_TRUTH_procgen.md, docs/tables/v1.md, v1.json, v2.md, v2.json, the frozen analysis code at prereg-v1.1 (git show), the three tag objects, numbers.json and scripts/manuscript_numbers.py. No experiment was run. The docx was converted to text with pandoc 3.12.1 and with python-docx and compared with the Markdown.

Severity: BLOCKING = the journal would return the manuscript, or a sentence is false or unsupported; MAJOR = misleading, incomplete, inconsistent or out of order; MINOR = style, wording, format. Location: section, paragraph number within the section (or subsection), first six words. Line numbers (L) refer to manuscript.md at 350f68b.

## 1. Findings

| ID | severity | location | problem | evidence | proposed fix |
|---|---|---|---|---|---|
| F01 | BLOCKING | Introduction ¶6, "The split between those eight and" (L41) | The sentence says the 8/17 split "was fixed before development began", but the record shows dc22 was moved from the held-out set to the development set on 21 September 2026 "to debug BRUTUS-G milestone 2 (wall learning failed on it)", i.e. during development, and the held-out set had 18 games until then. UNSUPPORTED. | docs/HELDOUT.md lines 23-24 and 31 | State that the split was fixed in a file before registration, that one game (dc22) was moved from held-out to development on 21 September 2026 during development, before its source was studied, and that the source of the remaining 17 was never opened; add the date and the count 18 to manuscript_numbers.py with HELDOUT.md as source. |
| F02 | BLOCKING | Method, Deviations ¶1 (L101); also Method "The instrument" ¶3 (L53) and Discussion "Why the failure could not show" (L257) | A sixth departure is missing: the registered protocol provided for an ARC-AGI-3 development truth table (docs/GROUND_TRUTH_arc_train.md, "W2") and for V1 on the eight development games "once its truth table exists"; the table was never written and ARC V1 was never computed. The manuscript says only that no truth table "was ever written", as if none had been planned, and lists the missing development check as a requirement for a second study. | PREREG.md v1 preface line 30, Section 8 line 265, Section 10 line 520; STATE.md amendment (h) line 465 ("Still outside v1.1 … docs/GROUND_TRUTH_arc_train.md") | Add the departure, dated by the v1 tag (27 September 2026) and by amendment (h), to the Deviations subsection, and say in the instrument and Discussion paragraphs that the protocol provided for this check and that it was not done. |
| F03 | BLOCKING | Method, Deviations (L101); Method "The instrument" ¶3 (L53) | A seventh departure is missing: the protocol registered I1 on ARC-AGI-3 ("Agents: R and N everywhere; I1 on ARC"), but the registered ARC baseline under the tag ran R and N only (500 rows = 25 games × 2 modes × 10 seeds). | PREREG.md v1 Section 9.1 line 466; STATE.md amendment (h) line 425 | Add it to the Deviations subsection as a registered run that was not made; ARC lines are reported, not tested, so no outcome clause depends on it. |
| F04 | BLOCKING | Method, Tests ¶3, "Test V3, parameter transfer, requires" (L81) | "It holds by construction" is unsupported as a statement of the registered test: V3 was registered as "checked from the adapter and code fields of every row", and no analysis script computes or writes it (no V3 line in docs/tables, no V3 code in analyze_v1.py or analyze_v2.py at prereg-v1.1). What the record shows is the runner's hash check ("frozen blob hashes: 6 of 6 match") at the start of each block. A further departure, not listed. | PREREG.md v1 Section 10 line 544; git show prereg-v1.1:scripts/analyze_v2.py (no V3); STATE.md (i) line 474, (j) line 515 | Say that the registered row-field check of V3 was not run by the analysis code, that the runner refused to start unless the six frozen hashes matched and its logs record that they did, and add the omission to the Deviations subsection. |
| F05 | BLOCKING | Method, "The instrument" ¶1, "It uses the frames of that" (L49); Introduction ¶1, "A frame-only game agent sees" (L31) | OVERCLAIM. The census and the agents receive, besides frames, a level-end and a game-end signal from each step (the registered environment contract), and the A5 rule depends on level ends. "Nothing else" and "sees nothing but the picture" are false. | PREREG.md v1 Section 3, lines 69-74 ("step(action) -> grid, level_end, game_end"); Section 5.3 (A5 uses goal_confirmed, set at a level end) | Say that the agent and the census receive the frame and a signal when a level or the game ends, and nothing else: no reward, no symbolic state, no text. |
| F06 | MAJOR | Purpose ¶1, "The initial hypothesis, as registered on" (L243-245) | The quoted claim is the OSF text. The git-tagged protocol words the claim differently ("together with a defined goal-identification cost G … in three suites"); the manuscript does not say which registered text it quotes or that the two differ. | docs/OSF_REGISTRATION_final.txt line 9; PREREG.md v1 Section 1 line 36; STATE.md amendment (g) line 344 | Name the OSF registration as the source of the quotation in the Purpose section, and add one sentence to the registration subsection noting the differing wording of the git-tagged claim. |
| F07 | MAJOR | Abstract (L27) "on every tested MiniGrid/BabyAI line"; Results ¶ nuisance (L192); Discussion "The nuisance baseline" (L265) | Inconsistent with the fifth deviation: the registered text tests V2 on MiniGrid/BabyAI under absolute moves only and reports the primitive-action lines, yet these sentences call all six primary lines "tested". | PREREG.md v1 Section 10 line 540; manuscript L79, L101 | Say "on all six primary MiniGrid/BabyAI lines (three under absolute moves, which the registered text tests, and three under primitive actions, which it reports)" and keep the numbers. |
| F08 | MAJOR | Results ¶ V2, "On the primitive-action lines R and" (L141) | States the printed FAIL verdicts of a condition that the registered text only reports as if they were test results; contradicts L79, L175 and the fifth deviation. | PREREG.md v1 Section 10 line 540 | Say that the frozen code prints FAIL for R and I1 on the primitive-action lines, which the registered text only reports. |
| F09 | MAJOR | Method, Deviations ¶1, "The fifth was found while" (L101) | The fifth deviation carries no date; the other four are dated. | STATE.md amendment (n), 14 October 2026, line 742 | Date it 14 October 2026. |
| F10 | MAJOR | Discussion "What the failure of V1 means" ¶2, "The second half of the" (L253) | SOFTENED and UNSUPPORTED. "That matters less than it might seem" softens the V2 result, and "The registered outcome table put V1 first for this reason" attributes a reason that the registered text does not give. | PREREG.md v1 Section 10 lines 548-557 (no reason stated) | State that V2 passed for no agent, that by the registered table a V1 failure on any suite decides the outcome by itself, and that a prediction from a score that does not measure what it names would be hard to interpret even if it had passed; drop the attributed reason. |
| F11 | MAJOR | Conclusion ¶1, "The instrument failed V1 on" (L291) | OVERCLAIM. "A baseline built from the size and variety of the environments ranked them better than the census did" holds on MiniGrid/BabyAI only; on Procgen the baseline is below the census on every line. | docs/tables/v2.md procgen rows (auroc_B 0.5104, 0.5667, 0.4750, 0.7000 against auroc 0.6458, 0.7222, 0.8750, 0.8000) | Restrict the clause to MiniGrid/BabyAI. |
| F12 | MAJOR | Exploratory diagnosis ¶3, "In this exploratory reading, for" (L214) | UNSUPPORTED. "on those games most seeds produced no learned shift for any key" names one of the two failure routes of the A1 rule; the diagnosis only reports that most seeds failed the per-seed rule. | EXPLORATORY_V1_DIAGNOSIS.md Section 5, A1, lines 133-134 | Say "most seeds failed the per-seed A1 rule (no learned shift for any key, or equal shifts for every tried key)". |
| F13 | MAJOR | Exploratory diagnosis ¶9, "In the same exploratory data," (L226) | Misleading. Dissent is said to be frequent "where the verdict depends on the planner's first-level outcome", but the first example, A2 under primitive actions, depends on the learning phase (an accepted key and a located avatar), not on the first-level outcome. | PREREG.md v1 Section 5.3 lines 157-159 | Say "where the verdict depends on the planner's run, its learning phase for A2 or its first-level outcome for A3 and A4". |
| F14 | MAJOR | Introduction ¶1, "They are also brittle in" (L31) | UNSUPPORTED generalizations: "most of them carry built-in assumptions" and "where they fail, the same planner wanders" are stated as facts about frame-only agents in general, with no source. | none in the record | Restrict to the agents studied here and state the second part as the idea the study tested. |
| F15 | MAJOR | Results ¶ V2, "The intervals on Procgen are" (L141) | Incomplete against the registered power note, which requires that a Procgen line that is not a PASS only because of the interval criterion be reported as such. No line is in that position: every Procgen line also has balanced accuracy 0.5000, below 0.80. The sentence implies the interval was the obstacle. | PREREG.md v1 Section 10 line 542; docs/tables/v2.md balanced_acc column | Add that every Procgen line also misses the balanced-accuracy condition, so none fails to pass on the interval alone. |
| F16 | MAJOR | Figure 2 (fig2.png) | The census point of "MiniGrid/BabyAI abs. moves, all games: I1" (0.7517) is drawn under the white-filled baseline square (0.7562) and cannot be seen; the figure does not show what the caption says it shows on that row. | docs/tables/v2.md row "minigrid macro all games I1"; fig2.png | Draw the baseline square unfilled and the census point above it (scripts/manuscript_figures.py). |
| F17 | MAJOR | Figure 2 caption (L143) | The caption says the ARC "FAIL" has no registered meaning but does not say the same of the three primitive-action primary verdicts, which the registered text only reports (fifth deviation). | PREREG.md v1 Section 10 line 540 | Add one sentence to the caption. |
| F18 | MAJOR | Table 2 (L147-173; docx table 2) | 13 columns; it overflows a portrait page in Word. | python-docx: table 2 has 13 columns | Keep Table 2 verbatim but split it into two tables with the same rows (identification columns, then statistics), or set the docx to landscape for that table; the split is done in draft 2. |
| F19 | MAJOR | Results, Exploratory diagnosis ¶1 (L208), Method "The instrument" ¶2 (L51), Results ¶ARC (L194) and Discussion | File paths, script names, commit hashes and section-style ids appear in running text (runs/exploratory/v1_diagnosis.json and f43526a in L208; scripts/g_nav.py:55 and ccc4d57 in the instrument subsection). | A3(iii) rule; B2 | Move them to the registration subsection, the data and code availability section or Appendix C; keep figure and table captions' source lines. |
| F20 | MAJOR | Tables 1 to 3 and Figure 2 labels | The identifiers macro, raw, center_off, center_on, all, in_range, camera_distinct, primary, "primary, D9b included", "all games" and auroc_B are not mapped anywhere in the text to the names used in the prose (absolute moves, primitive actions, whole-level view, …). | manuscript L113-190 | Add the mapping in the caption of Table 1 and Table 2. |
| F21 | MAJOR | Method: "The instrument" ¶1 (231 words), "The suites" ¶2 (226), "Tests" ¶2 (233), "Deviations" ¶1 (317) | Paragraphs over 220 words. | lang scan | Split each. |
| F22 | MINOR | L27, L37, L71, L73, L77, L79 (two), L85, L93, L101, L208, L220, L222 (two), L243, L261, L291, L295 | Sentences over 45 words (48 to 93 words). | lang scan | Split them. The quoted registered claim (70 words, L245) is verbatim and stays. |
| F23 | MINOR | L67, L71, L79, L228 | More than two semicolons in a paragraph. | lang scan | Replace with full stops. |
| F24 | MINOR | Method, Tests ¶2 (L79); front matter (L15) | AUROC is never spelled out; "OSF" is used in the required preprint line before the Open Science Framework is named, and the method never introduces the abbreviation. | manuscript | Spell out AUROC at first use and introduce "(OSF)" at first mention in the method; the J7 preprint line stays as prescribed. |
| F25 | MINOR | Method and Discussion, e.g. L51 "Every parameter of the census was frozen", L53 "These parameters were set", L71 "The protocol, version v1, was registered", L41 "the source code of the 17 was never opened"; L53, L67 "the author's agents", "the author's explorer" | Passive voice where the actor is the author, and third person "the author" in a text otherwise written in the first person. | manuscript | Use "I" and "my" where the author is the actor. |
| F26 | MINOR | Appendix C, Table C1 (L499-507) | Stale: docs/STATE.md was last changed in 350f68b, not f5d7591. | git log -1 -- docs/STATE.md | Rebuild numbers.json and appendix_c.md and copy the table. |
| F27 | MINOR | Method, Checks ¶1, "The analysis code passed 20" (L93) | Four of the 20 synthetic tests test the determinism check, not the analysis code. | PREREG.md v1.1 D11 lines 874-879 | "The analysis code and the determinism check passed 20 of 20 synthetic tests". |
| F28 | MINOR | Method, Seeds ¶1, "The MiniGrid/BabyAI block ran on" (L89) | "from 28 September 2026 to 13 October 2026" is more precise than the record, which says "finished by 13 Oct 2026". | STATE.md (j) line 513 | "started on 28 September 2026 and had finished by 13 October 2026". |
| F29 | MINOR | Results ¶ nuisance, "line : on 6 of 6" (L192) | Stray space before a colon. | manuscript | Remove. |
| F30 | MINOR | docx headings | Every section is Heading 2 and there is no Heading 1; the document outline starts one level down. | python-docx heading styles | Build with --shift-heading-level-by=-1 so sections are Heading 1 and subsections Heading 2. |
| F31 | MINOR | Same-length sentence runs at L33, L59, L63, L67 (three), L107, L141, L175, L218, L257 | Three consecutive sentences within five words of each other in length. | lang scan | Vary where the paragraph is rewritten for another finding; the rest are left as they are. |
| F32 | MINOR | Figure 2 labels | Labels use identifiers ("in_range", "camera_distinct") and abbreviations ("abs. moves", "primitive") while Figure 1 uses "in range" and "camera-distinct". | fig1.png, fig2.png | Use the words of Figure 1. |
| F33 | MINOR | Figures 1 and 3 captions | A bar of height zero is not drawn (Figure 1, camera-on A4 and A5, agreement 0.0000; Figure 3, every empty truth class); the captions do not say so. | docs/tables/v1.md; EXPLORATORY_V1_DIAGNOSIS.md Table 1 | Add "a missing bar is zero" to both captions. |
| F34 | MINOR | Discussion "The methodological mistake" ¶1, "I wrote the truth definitions" (L269) | "each with care" is a self-assessment of the author's own work. | none | Needs the author's decision (sentence about the author's own reasoning). |
| F35 | MINOR | JOTE_CHECKLIST.md, J4 line | "no other person or tool": docProps/app.xml carries pandoc's default template fields (Application "Microsoft Word 12.0.0", stale word counts). They name no person and no writing aid. | python-docx/zip read of app.xml | Reword the checklist line to say what the metadata holds. |
| F36 | MINOR | Abstract (244 words, one paragraph) | Over the 220-word paragraph rule; inside JOTE's 150-250 limit. | lang scan | No change: the abstract is one paragraph by convention and within the journal's limit. |
| F37 | MINOR | Results table captions (Tables 1 to 3) | Captions carry file names and commit bb0f1a1. | manuscript L111, L145, L177 | No change: kept as source lines, as for the figure captions (B2). |
| F38 | MINOR | Tables 1 and 2 | Negative κ values use a hyphen-minus ("-0.0435") while the text uses the minus sign (−0.0435). | docs/tables/v1.md | No change: the tables are verbatim copies. |
| F39 | MINOR | Section order | "Exploratory diagnosis" stands as its own section between Results and Purpose. J1 lists results, then purpose; the Purpose section is still immediately before the Discussion, and R6 requires a section so titled. | J1, R6 | No change; noted for the editor in case the journal prefers it as a Results subsection. |
| F40 | MINOR | Cover letter ¶3 and Data and code availability ¶1 | "All data and code are public" and the two OSF URLs: the repository is not yet public and both registrations are under embargo until 30 June 2030, so a reviewer cannot open them. | STATE.md (n) line 744 | Needs the author's decision (make the repository public and end the embargoes before submission, or reword). |
| F42 | BLOCKING | Introduction ¶6, "The reason is the problem of" (L41) | Roelofs et al. (2019) is cited in support of "it slowly turns into training data", but their meta-analysis found "little evidence of substantial overfitting" from test-set reuse. The citation contradicts the sentence. | Roelofs et al. (2019) abstract, NeurIPS proceedings page (Section 6) | Keep Blum and Hardt (2015) as the support and cite Roelofs et al. (2019) for what it found: in Kaggle competitions they found little such overfitting, which is no licence to reuse a held-out set during development. |
| F43 | MAJOR | Introduction ¶4, "The closest earlier attempt to predict" (L37); Discussion "Related work" ¶1 (L281) | PARTLY SUPPORTED. Bontrager et al. (2016) report the negative finding (the feature clustering agreed poorly with the performance clustering; "the features we have are not strong indicators of performance") but also a positive one: a selection agent built on two of the features beat its constituent controllers on the same games. The manuscript gives only the negative half. | Bontrager et al. (2016) full text (Section 6) | State both halves. |
| F44 | MAJOR | Introduction ¶5, "Bellemare et al. (2012) introduced contingency" (L39) | PARTLY SUPPORTED. Contingency awareness comes from developmental psychology; Bellemare et al. brought it into reinforcement learning and defined contingent regions. | Bellemare et al. (2012) full text (Section 6) | "brought contingency awareness into reinforcement learning, defining contingent regions as …". |
| F45 | MAJOR | Discussion "Related work" ¶3, "Its elimination steps are the" (L285) | PARTLY SUPPORTED. Goldman and Kearns give the class in complement form (one all-positive concept plus, for each instance, a concept negative only there), equivalent to singletons plus the empty set by complementing labels. | Goldman and Kearns, WUCS-92-28, Lemma 1 (Section 6) | Say "the singletons-plus-empty example of Goldman and Kearns (1995), which they state in complement form". |
| F46 | MAJOR | Discussion "Related work" ¶3, "Goal recognition design (Keren et al." (L285) | PARTLY SUPPORTED for Wayllace et al. (2016): their worst-case distinctiveness is an expected cost under stochastic action outcomes, not a worst-case length. | Wayllace et al. (2016) full text (Section 6) | Say Keren et al. bound the number of actions, and Wayllace et al. extend the measure to an expected cost under stochastic outcomes. |
| F47 | MAJOR | Discussion "Related work" ¶4, "Liew (2026) classifies the public" (L287) | PARTLY SUPPORTED. Not every tier of Liew's taxonomy is blind: five games need one probing action first and one needs diverse exploration. | Liew (2026) full text (Section 6) | "by the simplest strategy without reasoning that reaches a level". |
| F48 | MAJOR | Discussion "Related work" ¶4, "Skoutnev et al. (2026) identify goals" (L287) | PARTLY SUPPORTED. Twin is a frontier coding agent driven by a large pretrained model that writes an executable world model; its prior is that model's, not "visual priors". | Skoutnev et al. (2026) full text (Section 6) | "identify goals with a coding agent built on a large pretrained model, which writes an executable world model of each game and so brings a learned prior". |
| F49 | MINOR | Introduction ¶3, "Bertinetto et al. (2021) describe this" (L35) | The source speaks of the experimental protocol, not "the analysis". | Bertinetto et al. (2021) preface (Section 6) | "where the experimental protocol is fixed and reviewed before the experiments are run". |
| F50 | MINOR | References: Bellemare, Bontrager, Keren | AAAI-hosted proceedings are published in journal format; APA 7 sets them as periodicals (*Title*, *26*(1), 864–871), not "In … (Vol. 26, No. 1, pp. …)". | AAAI OJS pages (Section 6) | Reformat as periodical entries. |
| F51 | MINOR | References: Bertinetto, Blum, Cobbe, Roelofs, Wayllace, Choi, Chevalier-Boisvert | No DOI exists; APA 7 asks for the URL. The two ICLR papers have OpenReview pages, preferred to arXiv. Cobbe lacks the editors that Blum carries. | Section 6 (URLs below) | Add the URLs and the editors. |
| F52 | MINOR | Introduction ¶6 (L41) | MiniGrid is cited through the BabyAI paper only; the minigrid 3.1.0 package asks users to cite Chevalier-Boisvert et al. (2023). | minigrid README (Section 6) | Needs the author's decision (a new reference outside references.bib). |
| F41 | MINOR | Repository history | 88 commits before prereg-v1.2 carry attribution trailers in their messages; the manuscript points reviewers to this repository. | STATE.md (m) line 732 | Needs the author's decision, against the journal's policy on disclosure of writing and coding aids. |

## 2. A1, the hostile reviewer: every declarative sentence of the abstract, results, exploratory diagnosis, discussion and conclusion

Support is named by file and row. Sentences without a mark are SUPPORTED by the named source.

**Abstract.**
1. "I registered, before any confirmatory run, the claim …" — OSF_REGISTRATION_final.txt line 9; PREREG.md v1 Section 1.
2. "Every census parameter was frozen on eight ARC-AGI-3 games." — PREREG.md v1 Section 5.4.
3. "Test V1 compared …; test V2 compared …" — PREREG.md v1 Section 10.
4. "The census and the agents ran on 161 … 10,500 runs in all." — STATE.md (i), (j).
5. "By the registered outcome table the result is a refutation, under the clause 'V1 fails on any suite'." — STATE.md (k) lines 667-670; PREREG Section 10.
6. "V1 failed for three of five … four of five … four of five on Procgen." — docs/tables/v1.md.
7. "No agent passed V2 on any suite, and on every tested MiniGrid/BabyAI line a nuisance baseline … ranked the games better" — first half supported (v2.md); second half INCONSISTENT with the fifth deviation (F07).
8. "An exploratory reading made after the outcome suggests …" — labeled; EXPLORATORY_V1_DIAGNOSIS.md Section 7.
9. "The lesson is procedural …" — STATE.md (k) lines 678-682.

**Results.**
1. "The results in this section are the registered tests, exactly as the frozen analysis code wrote them." — the ARC lines and primitive-action verdicts are printed but not registered tests; covered by L175 and L194, acceptable once F08 is fixed.
2. V1 paragraph (L107): every clause matches v1.md; κ values match.
3. V2 paragraph (L141): void line, 101 of 112, 0.9018, I1 0.7187, N neither, Procgen I1 0.6458, R 0.7222, in-range "neither" — v2.md. "On the primitive-action lines R and I1 fail" — INCONSISTENT (F08). "which the protocol anticipated before any run" — supported (PREREG power note) but incomplete (F15).
4. Suite-line paragraph (L175): v2.json meta.suite_lines.
5. Nuisance paragraph (L192): numbers supported by v2.md; "every tested" INCONSISTENT (F07).
6. ARC paragraph (L194): STATE.md (k) lines 630-634.
7. Gate paragraph (L196): STATE.md (k) lines 667-671.

**Exploratory diagnosis.** Every count matches EXPLORATORY_V1_DIAGNOSIS.md Sections 1, 2, 4, 5 and 6 and the A2(i) table below, except L214 (UNSUPPORTED clause, F12) and L226 (misleading clause, F13). Every paragraph carries "exploratory". The closing sentence (L239) is correct.

**Discussion.**
1. L251: SUPPORTED; treats the truth table as the answer key and the census as the instrument under test.
2. L253: SOFTENED and UNSUPPORTED reason (F10).
3. L257: SUPPORTED in its facts; incomplete because the registered ARC truth table is not mentioned (F02).
4. L261: STATE.md (k) lines 678-682. "an early warning could not have rescued the registered claim" follows from the pilot rules (PREREG Section 12).
5. L265: "On every tested MiniGrid/BabyAI line" INCONSISTENT (F07); the rest supported by v2.md.
6. L269: "read from the exploratory diagnosis" — labeled; "each with care" (F34).
7. L273: written as requirements ("would have to"), not as results; the second requirement must be reworded once F02 is fixed, because the registered protocol already provided for it.
8. L277: SUPPORTED; non-claims.
9. Related work: see Section 5 (A5).

**Conclusion.** SUPPORTED except the baseline clause (F11, OVERCLAIM).

**Footing of truth and census.** No sentence puts the truth tables and the census on equal footing. L63 and L251 state the roles explicitly. Figure 1's axis reads "Agreement with the truth table".

**Exploratory material outside the exploratory section.** Abstract sentence 8 and Discussion L269 and L283 draw on it and say so. Nothing else.

**Future work.** None. The second-study paragraph is phrased as requirements.

**Deviations.** Five listed; the fifth is undated (F09). Missing, from the record: the ARC development truth table and ARC V1 (F02), I1 on ARC-AGI-3 (F03), the registered row-field check of V3 (F04). The differing claim wording (F06) is a disclosure, not a departure. dc22 (F01) predates registration and is not a deviation.

## 3. A2, the fact checker

### (i) Numbers in context

Every integer from 1 to 25 and every "X of Y" in the main text (take-home message to conclusion), with its source. All rows are CORRECT in value; the WRONG column marks a sentence whose wording misstates the row.

| line | sentence (abridged) | source | verdict |
|---|---|---|---|
| L27 | 161 environments, two conditions, 14 Procgen games, two camera settings, 10 seeds | PREREG v1 Sections 8, 9.1; STATE (i), (j) | CORRECT |
| L27 | three of five (macro), four of five (raw), four of five (Procgen) assumptions fail V1 | v1.md | CORRECT |
| L41 | eight of the 25 public games; the other 17 | PREREG v1 Section 8; HELDOUT.md | value CORRECT; "fixed before development began" WRONG (F01) |
| L49 | three agreeing presses, 2:1 margin, majority over 10 seeds, half the seeds | PREREG v1 Sections 5.3, 5.4 | CORRECT |
| L51 | LEARN_AGREE 3 at :55, margin at :756, LEARN_MAX 8 at :56, 40000 nodes at :54, min_cells 2 at g_motion.py:20 | PREREG v1 Section 5.4 | CORRECT |
| L53 | 25 games, 10 seeds, 500 runs, both agents | STATE (h) line 425 | CORRECT (I1 missing is F03) |
| L57 | six key identifiers, 8 × 8 tiles, four orientations, 64 × 64, rows 1 to 62 | PREREG v1 Sections 3.1, 3.2; v1.1 D1, D2 | CORRECT |
| L59 | 64 indices; at least 2 cells; at least 2 pixels; nine of the 14; ten games; nine confirmatory; 401 of 401; other six; five games | PREREG v1 Sections 3.3, 4; v1.1 D13; procgen_camera_check.json | CORRECT |
| L63 | 161; A4 fails on 5; A5 holds on 36; 14; A2 6, A3 2, A4 13, A5 6 | PREREG v1 Section 8 lines 271-275, 442-449 | CORRECT |
| L67 | three agents; five actions for I1 | PREREG v1 Section 2; v1.1 D7, D9b | CORRECT |
| L71 | six MiniGrid/BabyAI pilots, two Procgen pilots; dates 27 September 2026 (twice), 13 October 2026; embargo 30 June 2030 | PREREG v1 Section 8; tag objects; STATE (d), (h), (m) | CORRECT |
| L73 | 16 entries, D1 to D16 grouped as stated; eight ARC runs (D12) | PREREG v1.1 D1-D15, v1.2 D16 | CORRECT |
| L77 | at least 3 games for κ | PREREG v1 Section 10 | CORRECT |
| L79 | four conditions; at least half of 10 seeds; 17 held-out | PREREG v1 Section 10 | CORRECT |
| L85 | one environment with no success; 6 and 49; 155 and 112; 20 pilot runs; 57; 63 and 78; 98 and 83 | PREREG v1.1 D9, D9b; analyze_common.py | CORRECT |
| L89 | seeds 1000 to 1009; three times; 3300, 1081.6, 7500, 2481.5, 3600 s; 161, 2, 3, 10; 14, 2, 3, 10; 0 errors, 0 cut | PREREG v1.1 D5, D12; STATE (i), (j) | CORRECT; end date wording F28 |
| L93 | four checks; 200 actions; 334 of 334; 32 of 32; 480 = 360 + 120; 0 errors; 0 short; 0 over cap; nine games; 270 of 270; 0 missing; 20 of 20 | STATE (f); pilot_check.json; determinism_check.json; STATE (k) | CORRECT; "analysis code" for 20 tests F27 |
| L101 | five departures; dates 13 October (four times), 14 October; 25 and 17 games; eight development games; eight pilot games | STATE (k), (l), (m), (n) | CORRECT; fifth undated F09 |
| L107 | 14 games; nine in-range games; four fail | v1.md | CORRECT |
| L141 | 101 of 112; 14 games; nine; 95% interval | v2.md | CORRECT; F08, F15 |
| L175 | one verdict line per suite | v2.json meta.suite_lines | CORRECT |
| L192 | 6 of 6 primary lines; 12 of 14 lines; two exceptions | v2.md | values CORRECT; "tested" WRONG (F07) |
| L194 | 25 and 17 games | STATE (k) | CORRECT |
| L196 | three clauses; 13 October 2026 | STATE (k) | CORRECT |
| L208 | 3,500 planner rows; 0 mismatches; 25-game lines to four decimals | EXPLORATORY Section 1; STATE (l) | CORRECT |
| L214 | 151 of 161, 159 of 161, 13 of 14, 4 of 5 | EXPLORATORY Table 1 | CORRECT; clause F12 |
| L216 | 87 games; 870 seeds; 208; 159 of 161; 6 games; at least 9 of 10 seeds | EXPLORATORY Section 5 (A2) | CORRECT |
| L218 | 92 games; 850 of 920; 775; 755; 20; 73 games | EXPLORATORY Section 5 (A3) | CORRECT |
| L220 | all 13 games; all 10 seeds of 5 | EXPLORATORY Section 5 (A4) line 182 | CORRECT |
| L222 | 620 of 663; 986 of 1,074; 70 of 110; 23, 15, 0 games; 23 + 61 = 84; 15 + 105 = 120; 0 + 8 = 8 | EXPLORATORY Section 5 (A5) | CORRECT |
| L226 | 134 of 161; 135; 111 and 111; 3 and 6 games; 2 of 14 | EXPLORATORY Table 3 | CORRECT; clause F13 |
| L230-237 | 17 games; n 17, 8 and 9 positives | EXPLORATORY Section 6 | CORRECT |
| L261 | eight games; six and two; 10,500 runs | STATE (k) lines 679-681 | CORRECT |
| L291 | three or four of the five assumptions | v1.md | CORRECT; baseline clause F11 |

No WRONG value. Four sentences are WRONG in wording (L41, L192 and the abstract's "tested", L141 primitive-action "fail").

### (ii) Recurring counts

Every occurrence outside tables and references was listed (87 occurrences) and read. Each count keeps one meaning throughout: 161 confirmatory MiniGrid/BabyAI environments; 14 confirmatory Procgen games (and the date 14 October 2026, and the 14 MiniGrid/BabyAI V2 lines at L192, a different object stated with its noun); 5 camera-distinct games or A4-false environments, each with its noun; 9 in-range games (spelled "nine"); 8 development or pilot games, or 8 × 8 tiles, LEARN_MAX 8, 8 undetermined Procgen games, each with its noun; 17 held-out games; 25 public games; 10 seeds; 20,000 actions; 10,500 confirmatory runs or rows; 9,660 and 840 runs or rows; 500 ARC runs or rows; 3300, 7500 and 3600 s caps; 6 R/N raw exclusions, 6 MiniGrid/BabyAI pilots, 6 Procgen A2 truth-holds games, 6 primary lines, each with its noun; 49, 63, 78 exclusions; 155, 112, 98, 83 primary games; 270 pairs; 401 frames. No count changes meaning without its noun.

### (iii) Thresholds

Every statement of 0.75, 0.90, 0.70, 0.80, 0.60, 0.65, 0.10, the [0.10, 0.90] void band, 2,000 resamples and 95% (L77, L79, L141, Figure 1 and 2 captions and legends, Table 4) matches PREREG v1 Section 10 in meaning: V1 PASS agreement ≥ 0.90 and κ ≥ 0.70 (κ only with at least three games per truth value), FAIL below 0.75; V2 PASS AUROC ≥ 0.80, CI lower bound > 0.60, balanced accuracy ≥ 0.80, AUROC − AUROC_B ≥ 0.10; FAIL AUROC ≤ 0.65; VOID outside [0.10, 0.90]; 2,000 resamples, seed 20260927, 95% percentile interval. CORRECT.

### (iv) Tables 1 and 2

The table rows of manuscript.md lines 113-139 and 147-173 were diffed against the table rows of docs/tables/v1.md and docs/tables/v2.md: identical. Table 3 equals docs/tables/v2.json meta.suite_lines. Table 4 equals PREREG v1 Section 10 lines 549-557.

### (v) Dates and hashes

prereg-v1 → 19f2a9f25043997d1deffd5976f2f2150e5f086f, tagged 27 September 2026 (IST); prereg-v1.1 → 8b2b2b9b432dbea4ba5f62cfceb1aad5558d1ecc, 27 September 2026; prereg-v1.2 → 66e560645d9d98bca39ee7da9b1039ada1bc579b, 13 October 2026 (git rev-list and git cat-file -p on each tag). OSF https://osf.io/2znhw (STATE (d), 27 September 2026) and https://osf.io/zu5vq (STATE (h), 27 September 2026), embargo 30 June 2030 (STATE (d), (i)). Commits cited: bb0f1a1, f43526a, ccc4d57, 378345f, 66e5606 exist and match STATE.md. Blob hashes of Appendix D equal git ls-tree prereg-v1.1 (checked by manuscript_numbers.py). Run dates: suite B started 28 September 2026 and finished by 13 October 2026 (F28). All CORRECT.

### (vi) Figures

- Figure 1: all 25 bars, verdict words and the two threshold lines match docs/tables/v1.json; panel titles complete; axis label in words; nothing clipped; grayscale. The two zero bars (camera-on A4, A5) are invisible (F33).
- Figure 2: all 25 rows, intervals, baseline squares, verdict words and the two threshold lines match docs/tables/v2.json; the void line has no interval. One census point is hidden (F16); labels use identifiers (F32); caption incomplete on primitive-action verdicts (F17).
- Figure 3: every segment checked against EXPLORATORY_V1_DIAGNOSIS.md Table 1 (all 25 lines × 6 cells): CORRECT. Zero bars absent (F33).
- Figure 4: every histogram checked against EXPLORATORY_V1_DIAGNOSIS.md Table 3: CORRECT. Seven gray levels with black edges; adjacent levels 2 to 4 are close but separable.

### (vii) ARC lines

The 25-game lines are marked "reported" in Table 2, its caption, Figure 2's caption and L194, with the defect stated (L101). The 17-game line (Table 5) is marked exploratory, "Reported, never tested". CORRECT.

## 4. A3, the copy editor and the production desk

(i) Structure and limits: title; author block with affiliation, ORCID and email; five keywords; take-home message 49 words, 3 sentences; abstract 244 words; introduction; method; results; exploratory diagnosis (F39); purpose 183 words, immediately before the discussion, with the registered claim verbatim (F06); discussion; conclusion that refers to the purpose and states the failures; data and code availability with repository URL, three tags with full hashes, two OSF URLs, MIT license, the preprint line; funding; conflicts; references; appendices A to D. PASS.

(ii) APA 7: see Section 5. In-text citations are author-date; "et al." used from three authors; the list is alphabetical; every entry cited, every citation present (manuscript_check.py (c): 17 and 17).

(iii) Language: no forbidden word (check (b)); no British spelling (check (d)); no "we", "our" or "us"; "I" at most three times per paragraph; no body lists; no sentence starting with a bold phrase outside table captions; no parenthesis holding a full sentence. Findings F19 to F25, F29, F31.

(iv) The docx (python-docx 1.x on manuscript.docx at 350f68b): core properties creator "Rahul Kumar Mishra"; lastModifiedBy, subject, keywords, comments empty; title = the article title. Embedded images 4, inline drawings 4. Tables 8, with 9, 13, 4, 3, 7, 4, 2 and 3 columns: Table 2 has 13 (F18), Table 1 has 9 (at the limit). Headings carry Heading 2 and Heading 3 styles (F30). κ present 14 times; minus sign U+2212 4 times; en dash 11; curly quotes paired (33 and 33); no straight double quotes. Each image is followed directly by its Image Caption paragraph; 0 empty paragraphs. No leftover Markdown (asterisks, backticks, braces, "{width=100%}"). XML search for "assistant", "Claude", "Co-Authored", "language model", "generated": 0 hits in text, 0 in tag names. The pandoc plain-text conversion and the python-docx text agree with the Markdown on tables, κ, ×, en dashes, quotation marks, captions and identifiers (no hyphenation inserted into ids).

## 5. A4, the cover letter and the checklist

Cover letter against J8, line by line: addressed to the Editor-in-Chief, yes; Empirical Article, yes; the J7 preprint line, yes, verbatim; data and code links (repository, three tags with full hashes, two OSF URLs), yes; venue-clause statement with the quoted clause, the choice of a journal that publishes negative results, and "changes no analysis", yes; single author, no conflicts, no funding, yes; one paragraph on fit, yes; no other content, yes (the author block is the letterhead). The claim "All data and code are public" depends on the repository being public at submission (F40).

JOTE_CHECKLIST.md against the manuscript: J1 to J3, J5 to J8 and R1 to R7 are satisfied as stated, except: J4 "no other person or tool" needs rewording (F35); R7's "the truth tables are the answer key" is satisfied; R6 is satisfied once F12 and F13 are fixed (the paragraphs are labeled, but two clauses overstate the counts); the J1 and R5 word counts change with draft 2 and are updated.

## 6. A5, cited papers, and A3(ii) reference fields

Every source was fetched again on 14 October 2026: publisher pages, Crossref, PMLR, NeurIPS proceedings, OpenReview, the arXiv API, and the full text of Bontrager et al., Bellemare et al., Keren et al., Wayllace et al., Bertinetto et al., the Goldman and Kearns technical report WUCS-92-28, Skoutnev et al., Liew and Rudakov et al. ScienceDirect refused the full text of Goldman and Kearns (1995) and of Mitchell (1982) (HTTP 403); their bibliographic fields come from Crossref.

### 6.1 Reference fields

| entry | page fetched | result |
|---|---|---|
| Bellemare et al. 2012 | https://ojs.aaai.org/index.php/AAAI/article/view/8321 | CONFIRMED; periodical format (F50) |
| Bertinetto et al. 2021 | https://proceedings.mlr.press/v148/bertinetto21a.html | CONFIRMED: item "Preface", PMLR 148, p. i; authors exactly Bertinetto, Henriques, Albanie, Paganini, Varol; add URL (F51) |
| Blum & Hardt 2015 | https://proceedings.mlr.press/v37/blum15.html | CONFIRMED; add URL |
| Bontrager et al. 2016 | https://ojs.aaai.org/index.php/AIIDE/article/view/12884 | CONFIRMED; periodical format |
| Chevalier-Boisvert et al. 2019 | https://openreview.net/forum?id=rJeXCo0cYX ; arXiv 1810.08272 | CONFIRMED; OpenReview URL preferred |
| Choi et al. 2019 | https://openreview.net/forum?id=HyxGB2AcY7 ; arXiv 1811.01483 | CONFIRMED; OpenReview URL preferred |
| Cobbe et al. 2020 | https://proceedings.mlr.press/v119/cobbe20a.html | CONFIRMED; add editors H. Daumé III and A. Singh, and URL |
| Gaina et al. 2018 | Crossref 10.1109/CIG.2018.8490439 | CONFIRMED |
| Goldman & Kearns 1995 | Crossref 10.1006/jcss.1995.1003; technical report https://www.cis.upenn.edu/~mkearns/papers/teaching.pdf | CONFIRMED (bibliographic) |
| Keren et al. 2014 | https://ojs.aaai.org/index.php/ICAPS/article/view/13617 | CONFIRMED; periodical format |
| Laidlaw et al. 2023 | Crossref 10.52202/075280-2573 | CONFIRMED |
| Liew 2026 | arXiv 2605.25931 (API and PDF) | CONFIRMED |
| Mitchell 1982 | Crossref 10.1016/0004-3702(82)90040-6 | CONFIRMED (bibliographic) |
| Roelofs et al. 2019 | https://papers.nips.cc/paper_files/paper/2019/hash/ee39e503b6bedf0c98c388b7e8589aca-Abstract.html | CONFIRMED; no DOI exists; add URL |
| Rudakov et al. 2025 | arXiv 2512.24156 | CONFIRMED |
| Skoutnev et al. 2026 | arXiv 2608.14490 | CONFIRMED |
| Wayllace et al. 2016 | https://www.ijcai.org/Proceedings/16/Papers/464.pdf | CONFIRMED; add URL |

Every title is in sentence case; the list is alphabetical; in-text forms are correct. Optional, needing the author's decision: Chevalier-Boisvert, M., Towers, M., de Lazcano, R., et al. (2023), "Minigrid & Miniworld: Modular & customizable reinforcement learning environments for goal-oriented tasks", NeurIPS 36, 73383–73394, https://doi.org/10.52202/075280-3209, which the minigrid package asks users to cite (F52).

### 6.2 Sentences that characterize a cited paper

| manuscript sentence | source passage | verdict |
|---|---|---|
| L35 "Bertinetto et al. (2021) describe this model for machine learning research, where the analysis is fixed and reviewed before the experiments are run." | "A preregistered paper is a regular paper that is submitted for peer-review without any experimental results, describing instead an experimental protocol to be followed after the paper is accepted." | SUPPORTED; "protocol" is the exact word (F49) |
| L37 "Bontrager et al. (2016) read mechanics features from the rule files of general video game playing games and found that those features did not predict which controllers succeed." | "We analyzed the classes available in the VGDL file of all games and defined 14 features"; "Our data revealed only a 40.8% similarity between the two clusterings … the features we have are not strong indicators of performance"; but "In both cases, the algorithm selection agent was able to outperform its constituents" and "studying the features of games allow us to pick the best algorithm for different types of games" | PARTLY SUPPORTED: the positive selection result is missing (F43) |
| L37 "the target, the best controller from a portfolio, was not tied to any assumption the features express" | "a controller dominates a cluster of games if the controller wins more games in a particular cluster than any other controller" | SUPPORTED as a description of the target; the rest is the author's argument |
| L39 "Bellemare et al. (2012) introduced contingency awareness, the detection of screen regions whose appearance depends on the action" | "Within the cognitive science literature, contingency awareness is considered a crucial step … (Watson and Ramey 1972)"; "we formalize the notion of contingent regions: the parts of an observation whose immediate future value depends on the agent's choice" | PARTLY SUPPORTED (F44) |
| L39 "Choi et al. (2019) learned controllable regions with a neural network." | "an attentive dynamics model (ADM) that discovers controllable elements of the observations … trained in a self-supervised fashion" | SUPPORTED |
| L41 "… it slowly turns into training data (Blum & Hardt, 2015; Roelofs et al., 2019)" | Blum & Hardt: participants "may begin to overfit to the holdout data that supports the leaderboard"; Roelofs et al.: "Our study shows, somewhat surprisingly, little evidence of substantial overfitting" | Blum & Hardt SUPPORTED; Roelofs et al. NOT SUPPORTED (F42) |
| L41 "MiniGrid/BabyAI (Chevalier-Boisvert et al., 2019) and Procgen (Cobbe et al., 2020)" | "we introduce the BabyAI research platform"; "We introduce Procgen Benchmark, a suite of 16 procedurally generated game-like environments" | SUPPORTED (MiniGrid citation, F52) |
| L281 "Bontrager et al. (2016) are the closest prior attempt …; their features were exact by construction and failed at prediction." | Table 1 caption "Extracted game features from VGDL files"; the decision tree "was just memorizing the data, we therefore abandoned this effort"; and the selection result above | PARTLY SUPPORTED (F43) |
| L281 "Laidlaw et al. (2023) predict the sample complexity of deep reinforcement learning from a property of the full tabular decision process with its reward" | "155 deterministic MDPs … along with their corresponding tabular representations, which enables us to exactly compute instance-dependent bounds"; the effective-horizon bounds "are more closely reflective of the empirical performance of PPO and DQN" | SUPPORTED |
| L281 "Gaina et al. (2018) predict wins on held-out games from an agent's own experience during play, not before it." | "It is solely based on agent features … can be queried while playing the game … trained on 80 games … and tested on 20 new games" | SUPPORTED |
| L283 "The idea behind A1 and A2 … comes from Bellemare et al. (2012) and Choi et al. (2019)." | as above | SUPPORTED |
| L285 "Its elimination steps are the singletons-plus-empty example of Goldman and Kearns (1995)" | WUCS-92-28, Lemma 1: "a distinguished concept c classifies all instances as positive. In addition, for each x ∈ X there is a concept c_x ∈ C that classifies all instances but x as positive … td(C) = |C| − 1" | PARTLY SUPPORTED: complement form (F45); lemma number in the JCSS version not verified |
| L285 "version-space elimination in the sense of Mitchell (1982)" | full text not obtainable (HTTP 403); secondary sources attribute version spaces and candidate elimination to Mitchell | SUPPORTED by secondary sources only; the author should read the primary |
| L285 "Goal recognition design (Keren et al., 2014; Wayllace et al., 2016) … bounds how long an outside observer can remain unsure of an optimal actor's goal" | Keren: "an upper bound on the number of actions any optimal agent can perform in a model before revealing its goal"; Wayllace: "the largest expected cost to reach a boundary state … over all possible non-distinctive policy prefixes" | Keren SUPPORTED; Wayllace PARTLY SUPPORTED (F46) |
| L287 "Rudakov et al. (2025) published the graph-based explorer used here as I1." | "a training-free graph-based approach … maintains a directed graph of explored states and transitions … The code is open source" | SUPPORTED |
| L287 "Liew (2026) classifies the public games by the cheapest blind strategy that reaches a level; that classification concerns reachability rather than mechanics and makes no registered prediction." | "every one is reachable through non-intelligent strategies: 10 in a single blind step, 5 after one probing action, 1 via repeated ACTION1 presses, 1 via diverse exploration, and 8 via single repeated actions" | PARTLY SUPPORTED (F47); "no registered prediction" consistent with the text |
| L287 "Skoutnev et al. (2026) identify goals from frames using visual priors, outside the prior-free class for which G was defined." | "a frontier coding agent writes an executable world model … Its inductive prior over grid games is strong enough to recover the true transitions of the game and the goal on nearly all levels" | PARTLY SUPPORTED (F48); "outside the prior-free class" correct |

### 6.3 Bontrager et al. (2016)

Feature set: 14 features read from each game's VGDL description file (Table 1, "Extracted game features from VGDL files"): vertical movement, can use, player can die, is survival game, the shares of win and of lose termination conditions, the shares of solid, avatar, harmful, collectible, goal, other and spawned sprites, and the maximum number of interaction rules. Design: 23 controllers on 49 games, 25 plays each; the games clustered once by features and once by controller performance, and the two clusterings compared; then a selection agent built from a decision tree on the feature clusters. Negative finding: the two clusterings agreed on 40.8% ("the features we have are not strong indicators of performance"), and a tree from features to performance clusters was abandoned as memorization. Positive finding: a selection agent on two features ("can use", "can die") beat each of its constituent controllers on the same games (695 against 637 wins, and 326 against 300); the authors conclude that "studying the features of games allow us to pick the best algorithm". The manuscript's "read mechanics features from the rule files" and "exact by construction" match; "found that those features did not predict which controllers succeed" and "failed at prediction" give only the negative half.

### 6.4 Liew (2026) and Rudakov et al. (2025)

Liew: the arXiv metadata gives "Liew Keong Han", and the paper's own title block gives "Keong Han Liew". The linked GitHub account (github.com/farmountain) shows no display name, and no personal page, OpenReview or Scholar profile was found. Both forms make Liew the family name, so "Liew, K. H." and "Liew (2026)" are correct; the author's own page is inconclusive only in the sense that none exists beyond the paper.

Rudakov et al.: the workshop's call for papers (https://aclweb.org/portal/node/14293) says contributions are "non-archival and only will be hosted on our workshop website"; the workshop site (https://ai4research-workshop.github.io/) lists the paper as a poster. No proceedings page exists. The arXiv form stays.

## 7. Needs the author's decision

- F34: "each with care" in the Discussion, a sentence about the author's own work.
- F40: the repository must be public, and the OSF embargoes ended, before the sentences "All data and code are public" and the OSF links can be opened by reviewers.
- F41: the 88 commits with attribution trailers, against the journal's disclosure policy.
- F52: whether to add Chevalier-Boisvert et al. (2023) for MiniGrid.
- The title (draft 1 title kept).

## 8. Count of findings

BLOCKING 6 (F01 to F05, F42); MAJOR 22 (F06 to F21, F43 to F48); MINOR 24 (F22 to F41, F49 to F52). Total 52.
