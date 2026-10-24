# Review of JAGI manuscript draft 1 (24 October 2026)

Object: docs/manuscript_jagi/manuscript_jagi.md, supplement_jagi.md, cover_letter_jagi.md, manuscript_jagi.pdf, supplement_jagi.pdf, manuscript_jagi.docx, supplement_jagi.docx as committed at b93a700, and REFERENCES_CHECK_jagi.md. Line numbers are those of manuscript_jagi.md at b93a700 unless another file is named. Severity: BLOCKING = the journal would return it, or a sentence is false or unsupported, or the paper fails the journal's scope sentence; MAJOR = misleading, incomplete, inconsistent, out of order; MINOR = style, wording, format. Nothing in this review changes a file other than this one.

## 1. Findings

| ID | severity | location | problem | evidence | proposed fix |
|---|---|---|---|---|---|
| F01 | BLOCKING | 6.2, L232, last sentence | The sentence says the registered phrase that ARC-AGI-3 "does not count toward generality" kept the development games out of the check that would have exposed the instrument, which is false: the protocol itself provided for V1 on those games, labeled development, and I did not do it. | PREREG v1 preface and Sections 8, 10 (STATE.md (o), finding F02 of the JOTE review); manuscript L80 and L142 say the same | Replace with: "The protocol did provide for that check, labeled development, so the development games were not excluded from it; the check was simply not done." |
| F02 | BLOCKING | 6.4, L240, last sentence | "On Procgen the baseline did not rank the games better than the census on any line" is false for the camera-on lines. | docs/tables/v2.md: center_on I1 auroc 0.3333 against auroc_B 0.6667, N and R 0.3750 against 1.0000; Results L178 correctly says "every line of the whole-level view" | Add "of the whole-level view" after "any line". |
| F03 | BLOCKING | 2.3, L50, first sentence | ARC-AGI-3 is described ("a set of interactive games in which each game must be learned from interaction alone") with no citation and no source in the paper. | reference list has no ARC-AGI-3 source; CLAUDE.md must-cite list names the ARC-AGI-3 technical report and launch post | Restrict the sentence to what the study itself establishes (25 public games, played here from frames and level-end signals only); the citation is listed for the author's decision (Section 8). |
| F04 | BLOCKING | 1, L24 | "One widely cited definition" is not supported by any source; REFERENCES_CHECK_jagi.md already records "widely cited" as the author's wording. | REFERENCES_CHECK_jagi.md, Legg and Hutter, Sentence (1) | Delete "widely cited". |
| F05 | BLOCKING | 2.2, L46, sentence "All three treat the set of environments, and what an agent brings to them, as part of what a measurement means." | Only partly supported: Legg and Hutter tie the measure to a range of environments, Chollet to priors and experience; nothing fetched for Hernández-Orallo (2017) supports either half. | REFERENCES_CHECK_jagi.md passages for the three works | Replace with a sentence that attributes each half only to the work that supports it. |
| F06 | MAJOR | 2.2, L46, Hernández-Orallo sentence | The sentence is written as if from the book, but rests on the publisher's description only. | REFERENCES_CHECK_jagi.md, Hernández-Orallo (2017) | Reword to claim only what the publisher's description states, and say so (Section 6 of this review). |
| F07 | MAJOR | 6.1, L226, "The one assumption that held up across both benchmarks, A1, is the one whose probe and truth predicate say nearly the same thing." | A1 is "neither" on the Procgen in-range subset, so "held up across both benchmarks" overstates it, and the construct claim is an exploratory reading used outside Section 5 without the label (R6). | docs/tables/v1.md (procgen center_off in_range A1 neither); Section 5 L200 | Say "the one assumption with no failing V1 line" and label the construct clause as the exploratory reading of Section 5. |
| F08 | MAJOR | 6.1, L226, "The others depended on how one planner's run went, and that dependence did not carry over." | Exploratory reading outside Section 5 without the label, and "did not carry over" has no measured referent. | Section 5 L212, L214 | Rewrite as an exploratory-labeled sentence that says what Section 5 counted: the census verdicts for the others were by-products of one planner's run on each game. |
| F09 | MAJOR | 6, L220, first sentence | "its score did not predict first-level success there" overstates the registered result, which is that V2 passed for no agent; several lines are "neither". | docs/tables/v2.md | "and its score passed the registered prediction test for no agent there". |
| F10 | MAJOR | 7, L256, last sentence | "the check which would have shown the failure, a comparison with known truth on the development games and on the pilot games" asserts a counterfactual; neither comparison was made. | STATE.md (k) lesson; (o) F02 | "the check that could have shown it, …, was never run". |
| F11 | MAJOR | 6.3, L236; 3.10, L140 (fourth deviation) | "would have shown the disagreement / the failure" asserts the result of a comparison that was never made. | STATE.md (k): "not registered, and it was not done" | "could have shown". |
| F12 | MAJOR | Abstract L17; 6.4 L240 | The baseline-beats-census sentences omit that the baseline is fitted in-sample while the census score is not fitted, which favors the baseline. | PREREG v1 Section 10 ("logistic regression … fitted in-sample" in Section 3.6, L116) | Add "fitted in-sample" in the abstract and a clause in 6.4. |
| F13 | MAJOR | 6.1, L228, first sentence | "the study shows the mechanism working as designed" omits the eight recorded deviations, two of them registered checks never run. | Section 3.10 | Say that the registered decision rule worked as designed, and that the eight deviations change no test or outcome. |
| F14 | MINOR | Abstract L17, "on each suite and condition" | The camera-on condition is reported, not tested. | docs/tables/v1.md center_on rows | "on each tested suite and condition". |
| F15 | MAJOR | 5, L202, "On Procgen there are 6 games where the truth fails A2 because other entities also respond to the action." | Misleading: the truth fails A2 on 8 Procgen games; the 6 are those where the truth fails and the census holds. | docs/EXPLORATORY_V1_DIAGNOSIS.md L40, L146-149 | "On 6 Procgen games the truth fails A2, because other entities also respond to the action, and the census says it holds." |
| F16 | MAJOR | 2, L38 (section opening) | OFF SCOPE: lists lines of work without connecting them to generality across environments. | JAGI scope (Section 2 of this review) | Rewrite the opening sentence (Section 2 table). |
| F17 | MAJOR | 3, L70 (section opening) | OFF SCOPE: procedural outline only. | as above | Open with how the method makes the generality question answerable in advance. |
| F18 | MAJOR | 4, L146 (section opening) | OFF SCOPE: procedural. | as above | Open with the two halves of the generality question that V1 and V2 answer. |
| F19 | MAJOR | 5, L194 (section opening) | OFF SCOPE after the required first sentence. | as above | Keep "This section is exploratory." and add a second sentence tying the diagnosis to why the instrument did not carry its meaning across benchmarks. |
| F20 | MAJOR | 7, L256 | The conclusion restates the objective but never answers the generality question in its own words. | prompt A1; JAGI scope | Open the conclusion with the answer to the generality question. |
| F21 | MAJOR | 2.4 L54, 2.5 L58, 2.6 L62 (subsection openings) | OFF SCOPE: background subsections on technique, holdout reuse and preregistration do not say why they matter for a claim of generality. | JAGI scope | One lead sentence each (Section 2 table). |
| F22 | MINOR | 6.2 L232, 6.3 L236, 6.4 L240, 6.5 L244, 6.6 L248 (subsection openings) | OFF SCOPE openings inside the discussion. | JAGI scope | One lead clause or sentence each (Section 2 table). |
| F23 | MINOR | 3.1-3.10 (subsection openings) | OFF SCOPE by the letter of the test, as procedural subsections are. | JAGI scope | Not changed: the Section 3 opening (F17) carries the framing; procedural subsections stay procedural. |
| F24 | MAJOR | title, both PDFs, page 1 | The title breaks inside "ARC-AGI-3" ("ARC-AGI-" / "3"). | pdftotext page 1 of manuscript_jagi.pdf | Non-breaking hyphens inside ARC-AGI-3 in the title. |
| F25 | MAJOR | manuscript_jagi.pdf pages 10-11 (Table 1) and 12-13 (Table 2); supplement_jagi.pdf pages 1-2 (S1), 2-3 (S2b), 8-9 (S7) | Tables split across pages, captions separated from the start of their table. | layout check (Section 5 of this review) | Keep each table on one page (keep-with-next on table rows). |
| F26 | MINOR | first-page head of both PDFs | "Submitted 2026-10-24" is a fixed date; the date must be set on the day of submission. | jagi_reference.docx header3 | Placeholder "Submitted yyyy-mm-dd" until the submission day (BUILD.md step 5). |
| F27 | MINOR | both docx, figure alt text | The alt text in the docx is the full caption; the short alt text written for each figure (fig-alt) is not carried by pandoc's docx writer. | word/document.xml wp:docPr descr | Give each image a short alt text that reaches the docx. |
| F28 | MINOR | Figures 1-4 labels | The figures say "camera off", "camera on" and "level-1 completion"; the text says "whole-level view", "view centered on the agent" and "first-level". | fig1.png-fig4.png | Map the terms in the captions (the figure script is shared with the JOTE files and is not changed). |
| F29 | MINOR | Figure 2, ARC-AGI-3 rows | The image prints "FAIL" on the two ARC-AGI-3 rows with no "reported" marker; only the caption explains. | fig2.png | Not changed in the image (shared script); the caption already says it, and keeps saying it. |
| F30 | MINOR | page 1 author block | The Kit sets the e-mail address in small capitals; draft 1 sets it in the italic address style. | Kit, Instruction-word.docx, "Titles and Authors" | Not changed: small capitals are simulated in the Kit by font size and the journal re-typesets accepted papers. |
| F31 | MINOR | both PDFs | The Kit says final versions may not contain embedded external links; pandoc makes every URL a live link. | Kit, "Style and Format" | Not changed for review; for the camera-ready version only. |
| F32 | MINOR | Table 2 caption, L174 | "the lines that enter or could enter an outcome clause" includes the primitive-action line, which can enter none. | Section 3.6 L116 | "the tested lines, the reported primitive-action line and the reported ARC-AGI-3 line". |
| F33 | MINOR | supplement S.5, first paragraph | The only stated exception to the numbers check is the six new reference entries; the years of their in-text citations are also exempt. | scripts/manuscript_check.py docstring | Add the citation years. |
| F34 | MAJOR | supplement Table S5; JOTE Appendix C | Table S5 names docs/STATE.md (a224604); the commit of STATE.md (u), (v) (b585ab2) has made it stale, and check (g) fails on the next rebuild. | STATE.md (p), (s), (t), (v); Section 7 of this review | Implement A6 (--state-ref). |
| F35 | MINOR | REFERENCES_CHECK_jagi.md, Genesereth et al. (2005) | The end page 72 is still marked NOT VERIFIED; it is now confirmed by the Stanford faculty profile (fetched in this review) and by dblp per RKM (dblp served an anti-bot page to the fetch). | Section 6 of this review | Record the confirmation. |
| F36 | MINOR | cover letter, fourth paragraph | After the prior-submission sentence was removed, "The present version is rewritten …" has no stated referent. | cover_letter_jagi.md at b93a700 | "Compared with the Zenodo preprint, this version is rewritten …". |
| F37 | MINOR | 1, L30, last sentence | "The census either describes … or it does not" ignores the registered third verdict "neither". | PREREG v1 Section 10 | "The registered test V1 decides, per assumption, whether the census describes …". |
| F38 | MINOR | 2.1, L42, last sentence | "sit at the hard end of that range" is an evaluative claim with no source. | none | "sit at the end of that range with the least information". |
| F39 | MINOR | both docx, core.xml | dc:language "en-US" is set although the rule is "every other field empty"; the Kit's accessibility instructions ask for the document language. | docProps/core.xml; Kit, "Accessible Document Step-by-Step Instructions", item 8 | Not changed; recorded. |

## 2. A1, scope and framing

The journal's scope sentence (author guidelines, http://jagi.mindmakers.org/index.php/jagi/about/submissions, fetched 24 Oct 2026): "JAGI is different from conventional journals in artificial intelligence, in that it only publishes research results that make a recognizable attempt to contribute directly to the creation or analysis of general-purpose intelligent systems, rather than to the solution of a special type of problem, or the modeling of an isolated cognitive function."

The journal's aims (publisher page, https://reference-global.com/journal/JAGI, fetched 24 Oct 2026): "Articles focused on details of AGI systems are welcome, if they clearly indicate the relation between the special topics considered and intelligence as a whole, by addressing the generality, extensibility, and scalability of the techniques proposed or discussed."

| section | opening (first sentence, shortened) | verdict | rewrite if OFF |
|---|---|---|---|
| Abstract | "A general agent that meets an unseen game must learn from interaction how the game works." | ON SCOPE | |
| 1 Introduction | "A general agent has to cope with environments it has not seen." The first paragraph states the generality question. | ON SCOPE | |
| 2 Background | "Six lines of earlier work bear on the study: …" | OFF SCOPE (F16) | "Whether a description of game mechanics built on one set of environments holds on another touches six lines of earlier work: …" |
| 2.1 | "Genesereth et al. (2005) define a general game playing system …" | ON SCOPE | |
| 2.2 | "Legg and Hutter (2007) took as their informal working definition …" | ON SCOPE | |
| 2.3 | "ARC-AGI-3, which carries the ARC name, is a set of interactive games …" | ON SCOPE (but F03) | |
| 2.4 | "The census builds on earlier work on finding, from frames alone, the part of the screen that the actions control." | OFF SCOPE (F21) | "A general agent placed in an unseen game must first find what it controls, and earlier work has done this from frames alone." |
| 2.5 | "When the same held-out set is consulted again and again …" | OFF SCOPE (F21) | "A claim that a method carries across environments is only as good as the separation between the environments used to build it and those used to test it." |
| 2.6 | "Bertinetto et al. (2021) describe a model of preregistration …" | OFF SCOPE (F21) | "A claim of generality written after the data are in can be fitted to them, and preregistration removes that freedom." |
| 2.7 | "The closest earlier attempt to predict agent success from game mechanics …" | ON SCOPE | |
| 3 Method | "This section describes the instrument, the benchmarks …" | OFF SCOPE (F17) | "The method fixes the answer to the generality question in advance: an instrument frozen on one benchmark, two benchmarks it never saw, truth read from their source code, and tests registered before any run." |
| 3.1-3.10 | procedural openings | OFF SCOPE (F23, not changed) | none: the Section 3 opening carries the framing |
| 4 Results | "The results in this section are the registered tests …" | OFF SCOPE (F18) | "The registered tests answer the two halves of the generality question: whether the census describes games from the other benchmarks (V1), and whether its score predicts first-level success there (V2)." |
| 5 Exploratory Diagnosis | "This section is exploratory." | OFF SCOPE after the required first sentence (F19) | add: "It asks why an instrument whose parameters were held fixed across benchmarks did not keep its meaning across them." |
| 6 Discussion | "The registered answer is no on both counts: …" The first paragraph carries the generality question. | ON SCOPE (F09 applies to its wording) | |
| 6.1 | "V1 compares the census verdict …" (heading and second paragraph on generality claims) | ON SCOPE | |
| 6.2 | "I set the census constants while developing the planner …" | OFF SCOPE (F22) | "A failure to generalize can stay hidden on the benchmark where an instrument is built if nothing there scores it against truth." |
| 6.3 | "The pilot runs contained census verdicts for eight games …" | OFF SCOPE (F22) | "The same failure could have been seen on the first games of the new benchmarks, before the full runs." |
| 6.4 | "On all six primary MiniGrid/BabyAI lines, a logistic regression …" | OFF SCOPE (F22) | "On games from another benchmark, plain size and variety told more about first-level success than the census did." |
| 6.5 | "The mistake, stated plainly …" | OFF SCOPE (F22) | "The reason the census did not carry over from one benchmark to the others is a mistake of method, read from the exploratory diagnosis: …" |
| 6.6 | "What follows are requirements for a different study …" | OFF SCOPE (F22) | "A study that means to show that an instrument carries across benchmarks would have to meet requirements this one did not." |
| 6.7 | "This study does not show that frame-only agents cannot complete these games …" | ON SCOPE | |
| 7 Conclusion | "The registered objective was a frame-only census …" | does not answer the question in its own words (F20) | open with: "The answer to the generality question is no: a frame-only census of game mechanics built and frozen on ARC-AGI-3 neither described the mechanics of games from MiniGrid/BabyAI and Procgen as their source code states them nor passed the registered prediction test there." |

The introduction carries the generality question in its first paragraph; the discussion does in its first paragraph; the conclusion does not answer it explicitly (F20). With F16 to F22 applied, the paper meets the scope sentence as an analysis of whether a description of environments built for general agents carries across environments.

## 3. A2, the hostile reviewer

Every declarative sentence of the abstract, results, exploratory diagnosis, discussion and conclusion, with its source. Verdicts other than SUPPORTED point to a finding.

| ID | section | line | sentence | verdict | source |
|---|---|---|---|---|---|
| H001 | Abstract | 17 | A general agent that meets an unseen game must learn from interaction how the game works. | SUPPORTED | author's framing of the registered question (PREREG v1 Section 1) |
| H002 | Abstract | 17 | I asked whether a cheap description of an unseen game's mechanics, read from frames before any agent is chosen, carries over from the benchmark on which it w… | SUPPORTED | author's framing of the registered question (PREREG v1 Section 1) |
| H003 | Abstract | 17 | Before any confirmatory run, I registered the claim that a fixed battery of frame-only probes, the assumption census, with every parameter frozen on eight AR… | SUPPORTED | OSF registered claim (docs/OSF_REGISTRATION_final.txt) |
| H004 | Abstract | 17 | Test V1 compared the census with source-derived truth tables; test V2 compared a census score with first-level completion by three agents. | SUPPORTED | docs/PREREG.md v1 Section 10 |
| H005 | Abstract | 17 | The census and the agents ran on 161 MiniGrid/BabyAI environments under two action conditions and on 14 Procgen games, 10,500 runs in all. | SUPPORTED | STATE.md (j), (k); Section 3.8 |
| H006 | Abstract | 17 | By the registered outcome table the result is a refutation, under the clause "V1 fails on any suite". | SUPPORTED | PREREG v1 Section 10 outcome table; STATE.md (k) |
| H007 | Abstract | 17 | V1 failed for three or four of the five assumptions on each suite and condition, and no agent passed V2. | OVERCLAIM (minor) | the camera-on condition is reported, not tested (docs/tables/v1.md); see F14 |
| H008 | Abstract | 17 | On all six primary MiniGrid/BabyAI lines, a baseline built from grid area, action count and color count ranked the games better than the census did. | SOFTENED (incomplete) | docs/tables/v2.md; the baseline is fitted in-sample (docs/PREREG.md v1 Section 10), not said here; see F12 |
| H009 | Abstract | 17 | An exploratory reading suggests that for four assumptions the probes and the truth definitions were different constructs. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (labeled exploratory) |
| H010 | Abstract | 17 | An instrument never scored against known truth where its parameters were set brought no evidence of generality to the other benchmarks. | SUPPORTED | author's reading of Sections 3.1 and 6.2; no new fact |
| H011 | 4 Results | 146 | The results in this section are the registered tests, exactly as the frozen analysis code wrote them. | SUPPORTED | STATE.md (k); Supplement S.1, S.2 |
| H012 | 4 Results | 146 | Where the code prints a verdict that the registered text does not test, the text says so. | SUPPORTED | STATE.md (k); Supplement S.1, S.2 |
| H013 | 4 Results | 146 | The full tables, with every statistic, are in Supplement, Sections S.1 and S.2; Tables 1 and 2 here give only the verdict of each line. | SUPPORTED | STATE.md (k); Supplement S.1, S.2 |
| H014 | 4 Results | 148 | Figure 1 and Table 1 give V1. | SUPPORTED | docs/tables/v1.md |
| H015 | 4 Results | 148 | On MiniGrid/BabyAI under absolute moves, A1 and A2 pass and A3, A4 and A5 fail. | SUPPORTED | docs/tables/v1.md |
| H016 | 4 Results | 148 | Under primitive actions only A1 passes; A2, A3, A4 and A5 fail. | SUPPORTED | docs/tables/v1.md |
| H017 | 4 Results | 148 | On Procgen with the whole-level view, over all 14 games, A1 passes and the other four fail. | SUPPORTED | docs/tables/v1.md |
| H018 | 4 Results | 148 | On the nine in-range games, A1 is "neither", with agreement 0.8889, and A2 to A5 fail. | SUPPORTED | docs/tables/v1.md |
| H019 | 4 Results | 148 | The camera-on condition is reported and not tested. | SUPPORTED | docs/tables/v1.md |
| H020 | 4 Results | 148 | Cohen's κ is negative for A5 under absolute moves (−0.4125), under primitive actions (−0.3374) and on Procgen (−0.7843), and for A4 under absolute moves (−0.… | SUPPORTED | docs/tables/v1.md kappa column |
| H021 | 4 Results | 162 | Figure 2 and Table 2 give V2. | SUPPORTED | docs/tables/v2.md |
| H022 | 4 Results | 162 | No agent reached PASS on any benchmark or subset. | SUPPORTED | docs/tables/v2.md |
| H023 | 4 Results | 162 | On MiniGrid/BabyAI under absolute moves, the primary line of R is void, because R completed the first level on 101 of 112 games, a share of 0.9018, above the… | SUPPORTED | docs/tables/v2.md |
| H024 | 4 Results | 162 | I1 is "neither" there, with AUROC 0.7187, and so is N, the instrument check. | SUPPORTED | docs/tables/v2.md |
| H025 | 4 Results | 162 | On the primitive-action lines, which the registered text only reports, the frozen code prints FAIL for R and I1, with AUROC 0.5224 and 0.5370. | SUPPORTED | docs/tables/v2.md |
| H026 | 4 Results | 162 | On Procgen over all 14 games I1 fails, with AUROC 0.6458, and R is "neither", with 0.7222. | SUPPORTED | docs/tables/v2.md |
| H027 | 4 Results | 162 | On the nine in-range games every agent is "neither". | SUPPORTED | docs/tables/v2.md |
| H028 | 4 Results | 162 | The intervals on Procgen are wide: over 14 games, let alone nine, the lower end of the 95% interval does not reach 0.60 for any agent, which the protocol ant… | SUPPORTED | docs/tables/v2.md ci_low; docs/PREREG.md v1 Section 10 power note on suite C |
| H029 | 4 Results | 162 | The interval is not the only obstacle, though. | SUPPORTED | docs/tables/v2.md balanced_acc |
| H030 | 4 Results | 162 | Every Procgen line also has a balanced accuracy of 0.5000, below the registered 0.80, so no Procgen line misses a pass on the interval alone. | SUPPORTED | docs/tables/v2.md balanced_acc |
| H031 | 4 Results | 176 | Under absolute moves the MiniGrid/BabyAI benchmark line is "not failed", a verdict decided by I1 alone because R is void. | SUPPORTED | docs/tables/v2.json suite_lines |
| H032 | 4 Results | 176 | Procgen with the whole-level view is "not failed" over all games and over the in-range games. | SUPPORTED | docs/tables/v2.json suite_lines |
| H033 | 4 Results | 176 | The primitive-action line reads "suite FAIL", but the registered text only reports that condition, so this line enters no outcome clause (Section 3.10). | SUPPORTED | docs/tables/v2.json suite_lines |
| H034 | 4 Results | 178 | The nuisance baseline ranked the games better than the census on all six primary MiniGrid/BabyAI lines: the three under absolute moves, which the registered … | SUPPORTED | docs/tables/v2.md auroc against auroc_B, all 14 MiniGrid/BabyAI rows |
| H035 | 4 Results | 178 | Over all 14 MiniGrid/BabyAI lines, primary or not, the baseline is higher on 12. | SUPPORTED | docs/tables/v2.md auroc against auroc_B, all 14 MiniGrid/BabyAI rows |
| H036 | 4 Results | 178 | The two exceptions are reported lines under absolute moves with all games included, for N (census 0.6352, baseline 0.5752) and for R (census 0.6434, baseline… | SUPPORTED | docs/tables/v2.md auroc against auroc_B, all 14 MiniGrid/BabyAI rows |
| H037 | 4 Results | 178 | On Procgen the baseline is below the census on every line of the whole-level view. | SUPPORTED | docs/tables/v2.md auroc against auroc_B, all 14 MiniGrid/BabyAI rows |
| H038 | 4 Results | 180 | The two ARC-AGI-3 lines are reported and not tested, as registered. | SUPPORTED | STATE.md (k), ARC defect paragraph |
| H039 | 4 Results | 180 | Because of the defect recorded among the deviations, they are computed over all 25 public games rather than the 17 held-out games. | SUPPORTED | STATE.md (k), ARC defect paragraph |
| H040 | 4 Results | 180 | The "FAIL" printed on them has no registered meaning and enters no gate. | SUPPORTED | STATE.md (k), ARC defect paragraph |
| H041 | 4 Results | 180 | The line over the 17 held-out games is given, as exploratory, in Section 5. | SUPPORTED | STATE.md (k), ARC defect paragraph |
| H042 | 4 Results | 182 | Gate G3 applies the registered outcome table (Table 3). | SUPPORTED | PREREG v1 Section 10 outcome table; STATE.md (k) gate G3 |
| H043 | 4 Results | 182 | The outcome is a refutation, by the clause "V1 fails on any suite": V1 fails on MiniGrid/BabyAI in both conditions and on Procgen. | SUPPORTED | PREREG v1 Section 10 outcome table; STATE.md (k) gate G3 |
| H044 | 4 Results | 182 | The other two clauses of the refutation do not apply, since the V2 benchmark line under absolute moves is "not failed" and V2 is not void on every benchmark. | SUPPORTED | PREREG v1 Section 10 outcome table; STATE.md (k) gate G3 |
| H045 | 4 Results | 182 | One clause is enough. | SUPPORTED | PREREG v1 Section 10 outcome table; STATE.md (k) gate G3 |
| H046 | 4 Results | 182 | This classification was recorded on 13 October 2026, before any text about the results was written. | SUPPORTED | PREREG v1 Section 10 outcome table; STATE.md (k) gate G3 |
| H047 | 5 Exploratory | 194 | This section is exploratory. | SUPPORTED | STATE.md (l) |
| H048 | 5 Exploratory | 194 | It was written after the outcome was known, it tests nothing, and it changes nothing in the registered results above. | SUPPORTED | STATE.md (l) |
| H049 | 5 Exploratory | 194 | Its numbers come from an exploratory script that calls the frozen analysis functions unchanged (Supplement, Section S.5). | SUPPORTED | STATE.md (l) |
| H050 | 5 Exploratory | 194 | Two consistency checks come first, and both are exploratory. | SUPPORTED | STATE.md (l) |
| H051 | 5 Exploratory | 194 | The census verdict stored in each of the 3,500 planner rows equals the verdict recomputed from that row's report, with 0 mismatches. | SUPPORTED | STATE.md (l) |
| H052 | 5 Exploratory | 194 | The 25-game ARC-AGI-3 lines recomputed by the same functions equal those of the registered table to four decimals. | SUPPORTED | STATE.md (l) |
| H053 | 5 Exploratory | 196 | Figure 3 shows, for every V1 line, how the games split between truth and census, and Figure 4 shows how often single seeds disagree with their game's majority. | SUPPORTED | STATE.md (l) |
| H054 | 5 Exploratory | 196 | Both are exploratory. | SUPPORTED | STATE.md (l) |
| H055 | 5 Exploratory | 200 | In this exploratory reading, for A1 the census agrees with the truth on 151 of 161 games under primitive actions, 159 of 161 under absolute moves, 13 of 14 o… | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Table 1 and Section 5 (A1) |
| H056 | 5 Exploratory | 200 | Every disagreement is a game where the truth holds and the census fails. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Table 1 and Section 5 (A1) |
| H057 | 5 Exploratory | 200 | On those games most seeds failed the per-seed A1 rule, which fails when no key has a learned shift or when every tried key has the same shift. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Table 1 and Section 5 (A1) |
| H058 | 5 Exploratory | 200 | A1, input coupling, is the assumption that the census and the truth table describe in nearly the same terms, and it is the only one with no failing V1 line. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Table 1 and Section 5 (A1) |
| H059 | 5 Exploratory | 202 | The exploratory counts for A2 under primitive actions are these: 87 games have the truth holding and the census failing. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A2), lines 138-145 |
| H060 | 5 Exploratory | 202 | On their 870 seeds the two turn keys were recorded as producing no movement on all 870, and forward was accepted on 208. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A2), lines 138-145 |
| H061 | 5 Exploratory | 202 | A turn changes the agent's facing but not its cell, and the adapter merges the four facings into one tile index, so a turn changes nothing the census can see. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A2), lines 138-145 |
| H062 | 5 Exploratory | 202 | Under primitive actions the census's A2 therefore rested on forward alone. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A2), lines 138-145 |
| H063 | 5 Exploratory | 202 | Under absolute moves, where every move key displaces the agent, A2 agrees on 159 of 161 games. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A2), lines 138-145 |
| H064 | 5 Exploratory | 202 | On Procgen there are 6 games where the truth fails A2 because other entities also respond to the action. | MISLEADING | docs/EXPLORATORY_V1_DIAGNOSIS.md lines 40, 146: truth fails A2 on 8 Procgen games; the 6 are truth-fails/census-holds; see F15 |
| H065 | 5 Exploratory | 202 | The census rule has no clause for that, and on these games it found one controlled object on at least 9 of 10 seeds. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md line 148 (9 or 10 of 10 seeds) |
| H066 | 5 Exploratory | 204 | The exploratory counts for A3 under absolute moves are these: 92 games have the truth holding and the census failing. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A3), lines 152-161 |
| H067 | 5 Exploratory | 204 | Four step vectors were accepted on 850 of their 920 seeds, so the learned motion was mostly right. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A3), lines 152-161 |
| H068 | 5 Exploratory | 204 | Of the 775 seeds whose verdict is "fails", 755 carry the planner's first-level outcome "mispredicted" and the other 20 never located the agent. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A3), lines 152-161 |
| H069 | 5 Exploratory | 204 | The census's A3 failure therefore comes from the planner's prediction during play, not from the learned step vectors. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A3), lines 152-161 |
| H070 | 5 Exploratory | 204 | Under primitive actions the truth fails everywhere, because forward depends on facing, and the census says "holds" on 73 games. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A3), lines 152-161 |
| H071 | 5 Exploratory | 204 | One step vector per key, learned from the starting facing, cannot reveal a dependence on facing while the turns record no shift. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A3), lines 152-161 |
| H072 | 5 Exploratory | 206 | For A4 the exploratory reading is short. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A4); STATE.md (l) |
| H073 | 5 Exploratory | 206 | The census rule for A4 is conditional on A3, so most A4 failures on MiniGrid/BabyAI follow from those of A3. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A4); STATE.md (l) |
| H074 | 5 Exploratory | 206 | On Procgen the counter of walked-through "walls" is above zero on some seeds of all 13 games where the truth holds A4, and on all 10 seeds of 5 of them. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A4); STATE.md (l) |
| H075 | 5 Exploratory | 206 | That counter rises when the planner walks through a color it had classified as a wall. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A4); STATE.md (l) |
| H076 | 5 Exploratory | 206 | The counters do not say whether that came from the game's obstacles, from momentum or from the planner's classification. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 5 (A4); STATE.md (l) |
| H077 | 5 Exploratory | 208 | For A5, the exploratory counts show that most seeds with an undetermined verdict never recorded a goal place at all: 620 of 663 under absolute moves, 986 of … | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Table at lines 190-194; STATE.md (l) kappa decomposition |
| H078 | 5 Exploratory | 208 | A place is recorded only at a level end, so on these seeds the census had nothing to test. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Table at lines 190-194; STATE.md (l) kappa decomposition |
| H079 | 5 Exploratory | 208 | The census said "holds" where the truth fails on 23 games under absolute moves and 15 under primitive actions, and on 0 Procgen games. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Table at lines 190-194; STATE.md (l) kappa decomposition |
| H080 | 5 Exploratory | 208 | Success in each of those environments needs facing the target, a toggle or a pickup. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Table at lines 190-194; STATE.md (l) kappa decomposition |
| H081 | 5 Exploratory | 208 | They belong to the GoTo, GoToObj, OpenDoor, OneRoom, Fetch and Unlock families. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Table at lines 190-194; STATE.md (l) kappa decomposition |
| H082 | 5 Exploratory | 208 | The level then ends on a cell beside or in front of the target, and the census, reading places only, recorded that cell as a goal. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Table at lines 190-194; STATE.md (l) kappa decomposition |
| H083 | 5 Exploratory | 208 | In the same exploratory counts, the negative κ values for A5 come mostly from "undetermined", which the registered κ maps to the value opposite the truth. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Table at lines 190-194; STATE.md (l) kappa decomposition |
| H084 | 5 Exploratory | 208 | The cell "truth fails, census holds" used by κ therefore contains 23 census "holds" and 61 undetermined games under absolute moves (84 in all), 15 and 105 un… | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Table at lines 190-194; STATE.md (l) kappa decomposition |
| H085 | 5 Exploratory | 212 | In the same exploratory data, seeds often disagree with their game's majority where the verdict depends on the course of the planner's run: its learning phas… | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md dissent table, lines 96-115 |
| H086 | 5 Exploratory | 212 | At least one seed dissents on 134 of 161 games for A2 under primitive actions, 135 for A3 under primitive actions, and 111 each for A3 and A4 under absolute … | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md dissent table, lines 96-115 |
| H087 | 5 Exploratory | 212 | Dissent is rare for A1 and A2 under absolute moves, on 3 and 6 games, and for A4 on Procgen, on 2 of 14 games. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md dissent table, lines 96-115 |
| H088 | 5 Exploratory | 214 | The exploratory reading that ties these counts together concerns constructs. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (description, labeled) |
| H089 | 5 Exploratory | 214 | For A2 under primitive actions, and for A3, A4 and A5, the census probe and the truth definition are not the same construct. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (description, labeled) |
| H090 | 5 Exploratory | 214 | The census A2 asks whether some key moves one located object; the truth asks whether exactly one object's displacement is a fixed function of the action, tur… | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (description, labeled) |
| H091 | 5 Exploratory | 214 | The census A3 asks whether the planner's first-level model mispredicted; the truth asks whether each action's unblocked displacement is constant. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (description, labeled) |
| H092 | 5 Exploratory | 214 | The census A4 is conditional on A3 and counts walked-through "wall" colors; the truth asks whether every blocked move is explained by a fixed obstacle set. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (description, labeled) |
| H093 | 5 Exploratory | 214 | The census A5 asks whether a place recorded at a level end ended a level again, and it is silent when no level ends; the truth asks whether success is trigge… | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (description, labeled) |
| H094 | 5 Exploratory | 214 | In each case the census reads a by-product of one planner's run, while the truth reads the environment's step function. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (description, labeled) |
| H095 | 5 Exploratory | 214 | This is a description of the mismatch, made after the outcome. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (description, labeled) |
| H096 | 5 Exploratory | 214 | It is not a fix and not a result. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (description, labeled) |
| H097 | 5 Exploratory | 216 | On the 17 held-out ARC-AGI-3 games, the exploratory V2 line computed by the same frozen functions gives AUROC 0.3542 for N and 0.3403 for R, with the full li… | SUPPORTED | STATE.md (l); Supplement S.7 |
| H098 | 5 Exploratory | 216 | It is reported and never tested. | SUPPORTED | STATE.md (l); Supplement S.7 |
| H099 | 5 Exploratory | 216 | None of this exploratory material supports a causal claim. | SUPPORTED | STATE.md (l); Supplement S.7 |
| H100 | 5 Exploratory | 216 | These are counts of counters, read after the outcome was known. | SUPPORTED | STATE.md (l); Supplement S.7 |
| H101 | 6 Discussion | 220 | The registered answer is no on both counts: the census did not describe the mechanics of games from the two other benchmarks as their source code states them… | OVERCLAIM | docs/tables/v2.md: several lines are 'neither'; the registered result is that V2 passed for no agent; see F09 |
| H102 | 6 Discussion | 220 | This section says what that implies for claims of generality, why the failure was invisible where the instrument was built, what could have caught it earlier… | SUPPORTED | outline sentence |
| H103 | 6 Discussion | 224 | V1 compares the census verdict on each game with that game's entry in the source-derived truth table, and the two do not stand on equal footing. | SUPPORTED | PREREG v1 Section 10; truth tables committed before registration |
| H104 | 6 Discussion | 224 | The truth table is the registered answer key: it was committed before registration, and each entry names the source line that justifies it. | SUPPORTED | PREREG v1 Section 10; truth tables committed before registration |
| H105 | 6 Discussion | 224 | The census verdict is the instrument under test. | SUPPORTED | PREREG v1 Section 10; truth tables committed before registration |
| H106 | 6 Discussion | 224 | A failing V1 line therefore says that the instrument disagreed with the answer key too often, on the registered games and by the registered thresholds. | SUPPORTED | PREREG v1 Section 10; truth tables committed before registration |
| H107 | 6 Discussion | 224 | In plain terms, the census as registered does not measure that assumption on that benchmark. | SUPPORTED | PREREG v1 Section 10; truth tables committed before registration |
| H108 | 6 Discussion | 224 | By the registered outcome table, a V1 failure on any benchmark decides the outcome by itself, whatever V2 shows, and a prediction built on a score that does … | SUPPORTED | PREREG v1 Section 10; truth tables committed before registration |
| H109 | 6 Discussion | 226 | For generality the finding has a specific shape. | SUPPORTED | argument from Section 3.6 (V3) and Section 4; no new fact |
| H110 | 6 Discussion | 226 | The census kept every parameter fixed across benchmarks, which was the registered meaning of transfer, and it still failed. | SUPPORTED | argument from Section 3.6 (V3) and Section 4; no new fact |
| H111 | 6 Discussion | 226 | Holding an instrument's parameters fixed is a statement about the procedure. | SUPPORTED | argument from Section 3.6 (V3) and Section 4; no new fact |
| H112 | 6 Discussion | 226 | It says nothing about whether the procedure measures the same property on new games. | SUPPORTED | argument from Section 3.6 (V3) and Section 4; no new fact |
| H113 | 6 Discussion | 226 | Legg and Hutter (2007) define intelligence over a range of environments, so a claim that an instrument describes environments in general is a claim about a r… | SUPPORTED | Legg and Hutter (2007), Section 2.6 passage; rest is argument |
| H114 | 6 Discussion | 226 | Chollet (2019) asks that a benchmark of general intelligence control for priors and experience; an instrument that characterizes games carries priors of its … | SUPPORTED | Chollet (2019) abstract; rest is argument (census reads N's report, Section 3.1) |
| H115 | 6 Discussion | 226 | The one assumption that held up across both benchmarks, A1, is the one whose probe and truth predicate say nearly the same thing. | OVERCLAIM | docs/tables/v1.md: A1 is 'neither' on Procgen in range; construct claim is exploratory and unlabeled; see F07 |
| H116 | 6 Discussion | 226 | The others depended on how one planner's run went, and that dependence did not carry over. | UNSUPPORTED | exploratory reading outside Section 5, unlabeled; 'did not carry over' has no measured referent; see F08 |
| H117 | 6 Discussion | 228 | For registered claims in this area the study shows the mechanism working as designed. | OVERCLAIM | Section 3.10 records eight deviations, two of them registered checks never run; see F13 |
| H118 | 6 Discussion | 228 | The claim was stated before the data, the answer key was committed before the data, and the outcome followed from a clause written in advance. | SUPPORTED | tags prereg-v1/v1.1 dated 27 Sep 2026; STATE.md (k) |
| H119 | 6 Discussion | 228 | No reading of the results after the fact could turn the refutation into support, and none is offered here. | SUPPORTED | tags prereg-v1/v1.1 dated 27 Sep 2026; STATE.md (k) |
| H120 | 6 Discussion | 232 | I set the census constants while developing the planner on eight ARC-AGI-3 games, and I wrote the per-seed rules on top of the planner's report. | SUPPORTED | STATE.md (o) F02; PREREG v1 preface and Sections 8, 10 |
| H121 | 6 Discussion | 232 | The protocol provided for a truth table derived from source for those games and for V1 on them, labeled development. | SUPPORTED | STATE.md (o) F02; PREREG v1 preface and Sections 8, 10 |
| H122 | 6 Discussion | 232 | I never wrote that table, so V1 was never computed on the development instance. | SUPPORTED | STATE.md (o) F02; PREREG v1 preface and Sections 8, 10 |
| H123 | 6 Discussion | 232 | The census was tuned to make the planner work, and nothing on ARC-AGI-3 measured whether its verdicts matched the games' mechanics. | SUPPORTED | STATE.md (o) F02; PREREG v1 preface and Sections 8, 10 |
| H124 | 6 Discussion | 232 | A disagreement between census and truth could not show there, because nothing there was looking for it. | SUPPORTED | STATE.md (o) F02; PREREG v1 preface and Sections 8, 10 |
| H125 | 6 Discussion | 232 | The registered phrase that ARC-AGI-3 "does not count toward generality" was meant to keep the development games out of the evidence; in practice it also kept… | UNSUPPORTED (false) | PREREG v1 provided V1 on the development games (STATE.md (o) F02); the phrase did not exclude them; see F01 |
| H126 | 6 Discussion | 236 | The pilot runs contained census verdicts for eight games, six MiniGrid/BabyAI environments and two Procgen games, all of which have truth-table entries. | SUPPORTED | STATE.md (k) lesson |
| H127 | 6 Discussion | 236 | Comparing those verdicts with the truth before the v1.1 tag would have shown the disagreement before the 10,500 confirmatory runs were made. | OVERCLAIM | the comparison was never made (STATE.md (k)); 'would have shown' is a counterfactual; see F11 |
| H128 | 6 Discussion | 236 | The protocol did not register such a check, and I did not make one. | SUPPORTED | PREREG v1 pilot rules; STATE.md (k) lesson |
| H129 | 6 Discussion | 236 | The pilot rules allowed adapter code to change after the pilot, but no census constant, threshold or truth entry. | SUPPORTED | PREREG v1 pilot rules; STATE.md (k) lesson |
| H130 | 6 Discussion | 236 | An early warning could therefore not have rescued the registered claim. | SUPPORTED | PREREG v1 pilot rules; STATE.md (k) lesson |
| H131 | 6 Discussion | 236 | It would have changed what was run next, and how much machine time was spent finding out. | SUPPORTED | PREREG v1 pilot rules; STATE.md (k) lesson |
| H132 | 6 Discussion | 240 | On all six primary MiniGrid/BabyAI lines, a logistic regression on grid area, action count and color count ranked the games by first-level completion better … | SUPPORTED | docs/tables/v2.md |
| H133 | 6 Discussion | 240 | Three of those lines are tested by the registered text and three are reported. | SUPPORTED | docs/tables/v2.md |
| H134 | 6 Discussion | 240 | How large and how varied an environment is predicted completion better than the five assumptions as measured. | SOFTENED (incomplete) | baseline fitted in-sample, census score not fitted (docs/PREREG.md v1 Section 10); see F12 |
| H135 | 6 Discussion | 240 | This holds for the agents and conditions examined, and it is a statement about the measured census, not about the assumptions as properties of the games. | SUPPORTED | scope statement |
| H136 | 6 Discussion | 240 | On Procgen the baseline did not rank the games better than the census on any line. | WRONG | docs/tables/v2.md: camera-on lines have auroc_B 0.6667 and 1.0000 against census 0.3333 and 0.3750; see F02 |
| H137 | 6 Discussion | 244 | The mistake, stated plainly and read from the exploratory diagnosis, is that the probes and the truth predicates were not the same constructs, and that no te… | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (labeled 'read from the exploratory diagnosis') |
| H138 | 6 Discussion | 244 | The census decisions were by-products of one planner's run: whether it located an avatar from its first presses, whether its first-level model mispredicted, … | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (labeled 'read from the exploratory diagnosis') |
| H139 | 6 Discussion | 244 | The truth entries are properties of the environment's step function. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (labeled 'read from the exploratory diagnosis') |
| H140 | 6 Discussion | 244 | Only A1 is measured in nearly the same terms on both sides, and only A1 had no failing V1 line. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (labeled 'read from the exploratory diagnosis') |
| H141 | 6 Discussion | 244 | I wrote the truth definitions and the census rules separately and never checked on any game, before registration, that one estimated the other. | SUPPORTED | docs/EXPLORATORY_V1_DIAGNOSIS.md Section 7 (labeled 'read from the exploratory diagnosis') |
| H142 | 6 Discussion | 248 | What follows are requirements for a different study, not a result and not an existing instrument. | SUPPORTED | requirements, not claims (R6: not presented as results) |
| H143 | 6 Discussion | 248 | It would have to define each probe and its truth predicate as the same construct before registration, and show on development games that the two agree. | SUPPORTED | requirements, not claims (R6: not presented as results) |
| H144 | 6 Discussion | 248 | It would have to write a truth table for the development instance and compute V1 there before registration, rather than leave it for later as this protocol did. | SUPPORTED | requirements, not claims (R6: not presented as results) |
| H145 | 6 Discussion | 248 | It would have to register a V1 gate on the pilot games of every benchmark, with a stop rule, before any confirmatory run. | SUPPORTED | requirements, not claims (R6: not presented as results) |
| H146 | 6 Discussion | 248 | It would have to register how "undetermined" enters each test, rather than mapping it to the opposite of the truth for κ, so that a silent instrument and a w… | SUPPORTED | requirements, not claims (R6: not presented as results) |
| H147 | 6 Discussion | 248 | And it would have to name, before registration, a nuisance baseline that the census must beat on the development instance. | SUPPORTED | requirements, not claims (R6: not presented as results) |
| H148 | 6 Discussion | 252 | This study does not show that frame-only agents cannot complete these games, and it says nothing about their ability in general. | SUPPORTED | scope statements; truth tables |
| H149 | 6 Discussion | 252 | It does not show that A1 to A5 are poor descriptions of the games; the truth tables say how often each holds, and that is not in question. | SUPPORTED | scope statements; truth tables |
| H150 | 6 Discussion | 252 | It says nothing about the hidden ARC-AGI-3 games, which were not used, and nothing about agents that bring priors of any kind, visual or learned, to the games. | SUPPORTED | scope statements; truth tables |
| H151 | 6 Discussion | 252 | It does not show that a differently built census would fail, and it does not show that instruments built on one benchmark cannot transfer to others. | SUPPORTED | scope statements; truth tables |
| H152 | 6 Discussion | 252 | It shows that this instrument, registered with these thresholds, did not. | SUPPORTED | scope statements; truth tables |
| H153 | 7 Conclusion | 256 | The registered objective was a frame-only census, fitted on ARC-AGI-3, that would report the mechanics of games from other benchmarks at a registered accurac… | SUPPORTED | Sections 4, 3.6; STATE.md (k) |
| H154 | 7 Conclusion | 256 | It failed in each registered respect. | SUPPORTED | Sections 4, 3.6; STATE.md (k) |
| H155 | 7 Conclusion | 256 | The instrument failed V1 on both confirmatory benchmarks, for three or four of the five assumptions depending on the benchmark and condition. | SUPPORTED | Sections 4, 3.6; STATE.md (k) |
| H156 | 7 Conclusion | 256 | The prediction test V2 passed for no agent on any benchmark, and on MiniGrid/BabyAI a baseline built from the size and variety of the environments ranked the… | SUPPORTED | Sections 4, 3.6; STATE.md (k) |
| H157 | 7 Conclusion | 256 | The registered consequence followed: a refutation. | SUPPORTED | Sections 4, 3.6; STATE.md (k) |
| H158 | 7 Conclusion | 256 | For anyone who builds an instrument on one benchmark and means to use it on others, the record here is that freezing the parameters secured nothing about val… | OVERCLAIM | V1 on the development games was never computed, the pilot comparison never made; see F10 |

The other A2 checks:
- Outcome stated by its registered clause: yes, L182 ("by the clause 'V1 fails on any suite'"), the abstract and the conclusion; not argued around.
- Nothing exploratory outside the labeled section: two unlabeled sentences in 6.1 (F07, F08). The abstract's exploratory sentence is labeled; 6.5 says "read from the exploratory diagnosis"; Results L180 sends the 17-game line to Section 5 as exploratory.
- Truth tables as the answer key: L92, L224 ("the two do not stand on equal footing"). Yes.
- No "future work": 6.6 is written as requirements for a different study, "not a result and not an existing instrument". Yes.
- The eight deviations present and dated: L136-142; D16 13 Oct 2026, venue 13 and 14 Oct 2026, defect 13 Oct 2026, omission 13 Oct 2026, fifth 14 Oct 2026, sixth to eighth 14 Oct 2026. Yes.
- The venue deviation names JAGI and no other journal: L138. Yes.
- No sentence mentions the Journal of Trial and Error, a fee or a waiver: git grep -n -i "fee\|waiver\|trial and error\|jote" over the three files prints nothing at b93a700.

## 4. A3, the fact checker

### 4.1 Numbers in context (every integer from 1 to 25 and every "X of Y" in the main text)

| line | sentence (shortened) | value | source | verdict |
|---|---|---|---|---|
| L30 | eight of the 25 public games of ARC-AGI-3 | 8, 25 | docs/HELDOUT.md | CORRECT |
| L50 | Its 25 public games | 25 | docs/HELDOUT.md | CORRECT |
| L76 | the majority over its 10 seeds | 10 | PREREG v1 Section 5 | CORRECT |
| L78 | three agreeing presses, 2:1 margin, eight presses, at least 2 changed cells | 3, 2, 8, 2 | PREREG v1 Section 5.4 constants | CORRECT |
| L80 | the other 17 public games | 17 | docs/HELDOUT.md | CORRECT |
| L80 | held 18 games … until 21 September 2026 | 18, 21 | docs/HELDOUT.md (dc22 moved) | CORRECT |
| L80 | all 25 public games with 10 seeds | 25, 10 | STATE.md (e), (h); 500 rows | CORRECT |
| L84 | 8 × 8 pixel tiles; rows 1 to 62 | 8, 1 | PREREG v1.1 D2 | CORRECT |
| L86 | at least 2 cells; at least 2 pixels; Nine of the 14 | 2, 2, 9, 14 | PREREG v1 Section 3.3 operating range; docs/tables/v1.md n | CORRECT |
| L88 | Ten Procgen games … nine of them; 401 of 401; other six; five games | 10, 9, 401/401, 6, 5 | runs/pilot_checks/procgen_camera_check.json; D13 | CORRECT |
| L92 | A4 fails on 5 and A5 holds on 36 (of 161) | 5, 36 | docs/tables/v1.md truth_holds 156, 36 | CORRECT |
| L92 | of 14: A2 holds on 6, A3 on 2, A4 on 13, A5 on 6 | 6, 2, 13, 6 | docs/tables/v1.md truth_holds | CORRECT |
| L106 | six MiniGrid/BabyAI environments and two Procgen games | 6, 2 | PREREG v1 pilot set | CORRECT |
| L108 | 16 entries, D1 to D16 | 16 | PREREG v1.1, v1.2 diff sections | CORRECT |
| L112 | at least 3 games | 3 | PREREG v1 Section 10 | CORRECT |
| L114 | at least half of its 10 seeds; four conditions | 10, 4 | PREREG v1 Section 10 | CORRECT |
| L116 | 17 held-out games | 17 | PREREG v1 Section 10 | CORRECT |
| L118 | six frozen files; both blocks | 6 | PREREG v1 Section 5; runner logs (STATE.md (j)) | CORRECT |
| L124 | excludes 6 … and 49, leaving 155 and 112 | 6 | scripts/analyze_common.py at prereg-v1.1; Table S4 | CORRECT |
| L124 | any of its 20 runs | 20 | PREREG v1.1 D9b (pilot) | CORRECT |
| L124 | 57; 63 and 78; 98 and 83 | — | Table S4 | CORRECT |
| L128 | (161 environments, 2 conditions, 3 agents, 10 seeds); (14 games, 2 conditions, 3 agents, 10 seeds) | 2, 3, 10, 14 | 161×2×3×10 = 9,660; 14×2×3×10 = 840; sum 10,500 | CORRECT |
| L132 | 334 of 334; 32 of 32 | 334/334, 32/32 | fidelity check output (PREREG v1.1 D8; numbers.json) | CORRECT |
| L132 | 480 pilot runs, 360 and 120 | — | runs/pilot_checks/pilot_check.json; 360+120 = 480 | CORRECT |
| L132 | the nine Procgen games; 270 of 270 pairs | 9, 270/270 | runs/checks/determinism_check.json; 9×3×10 = 270 | CORRECT |
| L132 | 20 of 20 synthetic tests | 20/20 | STATE.md (k): 5+9+2+4 = 20 | CORRECT |
| L136-142 | Eight departures; the last three; 25 public games; 17 held-out; eight development games | 8, 3, 25, 17, 8 | Section 3.10; STATE.md (k), (o), (p) | CORRECT |
| L148 | over all 14 games; the nine in-range games | 14, 9 | docs/tables/v1.md | CORRECT |
| L154-158 | Table 1 game counts 161, 161, 14, 9, 5 | 14, 9, 5 | docs/tables/v1.md n | CORRECT |
| L162 | 101 of 112 games, share 0.9018 | 101/112 | docs/tables/v2.md minigrid macro primary R | CORRECT |
| L162 | over all 14 games; the nine in-range games | 14, 9 | docs/tables/v2.md | CORRECT |
| L172 | ARC-AGI-3, 25 public games | 25 | docs/tables/v2.md arc n | CORRECT |
| L178 | all six primary lines; the three … and the three | 6, 3 | docs/tables/v2.md | CORRECT |
| L178 | Over all 14 MiniGrid/BabyAI lines … higher on 12; two exceptions | 14, 12, 2 | docs/tables/v2.md: 7 macro + 7 raw rows; census higher only for macro all-games N and R | CORRECT |
| L180 | all 25 public games rather than the 17 held-out games | 25, 17 | STATE.md (k) defect | CORRECT |
| L182 | other two clauses | 2 | PREREG v1 Section 10 | CORRECT |
| L194 | 3,500 planner rows, 0 mismatches | — | STATE.md (l) | CORRECT |
| L200 | 151 of 161; 159 of 161; 13 of 14; 4 of 5 | — | docs/EXPLORATORY_V1_DIAGNOSIS.md Table 1 (A1 rows) | CORRECT |
| L202 | 87 games; 870 seeds; on all 870; accepted on 208 | — | EXPLORATORY L138-143 | CORRECT |
| L202 | A2 agrees on 159 of 161 | — | EXPLORATORY L145 | CORRECT |
| L202 | 6 games where the truth fails A2 … | 6 | EXPLORATORY L40, L146: truth fails on 8; 6 = truth fails, census holds | WRONG in context (F15) |
| L202 | at least 9 of 10 seeds | 9/10 | EXPLORATORY L146 ("9 or 10 of 10") | CORRECT |
| L204 | 92 games; 850 of their 920 seeds; 775; 755; other 20; 73 games | 20 | EXPLORATORY L152-161 | CORRECT |
| L206 | all 13 games; all 10 seeds of 5 of them | 13, 10, 5 | STATE.md (l); EXPLORATORY Section 5 (A4) | CORRECT |
| L208 | 620 of 663; 986 of 1,074; 70 of 110 | — | EXPLORATORY L192-194 | CORRECT |
| L208 | 23 … and 15 …, and on 0 | 23, 15 | EXPLORATORY Table 1 (A5 truth f: census h) | CORRECT |
| L208 | 23 and 61 (84); 15 and 105 (120); 0 and 8 (8) | 23, 15, 8 | EXPLORATORY Table 1; sums 84, 120, 8 | CORRECT |
| L210 | of their 10 seeds | 10 | design | CORRECT |
| L212 | 134 of 161; 135; 111 each; 3 and 6 games; 2 of 14 | 3, 6, 2/14 | EXPLORATORY dissent table L96-111 | CORRECT |
| L216 | the 17 held-out ARC-AGI-3 games | 17 | STATE.md (l) | CORRECT |
| L236 | eight games, six … and two …; 10,500 | 8, 6, 2 | STATE.md (k) lesson | CORRECT |

One row is WRONG in context (L202, F15). Recurring counts are consistent across the abstract, Method, Results and Discussion: 161, 14, 9, 5, 25, 17, 8, 10,500, 9,660, 840, 500, six primary lines, 12 of 14.

### 4.2 Thresholds

Against PREREG v1 Section 10 (git show prereg-v1:docs/PREREG.md): V1 PASS agreement ≥ 0.90 and κ ≥ 0.70, FAIL below 0.75, κ only with at least three games per truth value, undetermined never agrees and maps to the opposite of the truth for κ; V2 PASS AUROC ≥ 0.80, CI lower bound > 0.60, balanced accuracy ≥ 0.80, AUROC − AUROC_B ≥ 0.10, FAIL ≤ 0.65, void outside [0.10, 0.90], 2,000 resamples; outcome table rows. All as stated in Section 3.6 and Table 3. The power note on suite C supports L162 "which the protocol anticipated before any run".

### 4.3 Tables

- Table S1 equals docs/tables/v1.md cell for cell (scripted comparison: True).
- Tables S2a and S2b, recombined, equal docs/tables/v2.md cell for cell, 25 rows (True).
- Table S3 equals the suite_lines of docs/tables/v2.json, 10 of 10 rows.
- Table 1 of the paper against docs/tables/v1.md: 0 mismatches over 25 verdicts and 5 game counts.
- Table 2 of the paper against docs/tables/v2.md and Table S3: 0 mismatches over 15 agent verdicts (one "not run") and 5 benchmark lines.

### 4.4 Dates and hashes

prereg-v1 → 19f2a9f25043997d1deffd5976f2f2150e5f086f, tagged 2026-09-27; prereg-v1.1 → 8b2b2b9b432dbea4ba5f62cfceb1aad5558d1ecc, 2026-09-27; prereg-v1.2 → 66e560645d9d98bca39ee7da9b1039ada1bc579b, 2026-10-13 (git rev-parse and git for-each-ref). Each full hash appears twice in the paper and matches. 21 September 2026 (HELDOUT.md), 27 September 2026 (tags, OSF), 28 September and 13 October 2026 (STATE.md (i), (j)), 13 October 2026 (STATE.md (k), (l), (m)), 14 October 2026 (STATE.md (n), (o), (r)): all match. The OSF claim quoted at L102 equals docs/OSF_REGISTRATION_final.txt verbatim.

### 4.5 Figures

Each of the four PNG files was opened and read against its source.
- fig1.png (docs/tables/v1.json): 25 bars equal the agreement column of Table S1; verdict words equal its verdict column; dotted line 0.90 and dashed line 0.75 drawn; two zero bars on the camera-on panel are invisible, as the caption says; no clipping; y axis "Agreement with the truth table".
- fig2.png (docs/tables/v2.json): 25 rows, census AUROC with interval and baseline square equal Tables S2a and S2b; verdict words at the right; void line without interval; dashed 0.65 and dotted 0.80; no clipping. The ARC-AGI-3 rows print "FAIL" with no "reported" marker (F29).
- fig3.png (runs/exploratory/v1_diagnosis.json): stacked bars equal the confusion counts of docs/EXPLORATORY_V1_DIAGNOSIS.md Table 1 (checked: A1 raw 151/10, A2 Procgen 6 h, 6 f-h + 2 f-f, A5 macro 2/25/9 and 23/41/61); legend and h/f labels present.
- fig4.png (same source): histograms equal the dissent table (checked: A2 raw 27 at zero dissent, A4 Procgen 12 at zero).
- All four: 2007 px wide, placed at 6.0 in (docx extent 5486400 EMU), so 334 dpi, above the Kit's 266; maximum chroma 0, so pure grayscale; text at least about 9 pt at print size. Alt text is present but equals the full caption (F27). Terms in the labels differ from the text (F28).

### 4.6 ARC lines

The two ARC-AGI-3 lines are marked "reported" in Section 3.6, Table 2 ("(reported)", "reported, not tested"), L180, the Figure 2 caption and Table S2a. The 17-game line is marked exploratory in L216 and in Section S.7 ("This section is exploratory").

## 5. A4, the journal's format

From the Author's Kit (Instruction-word.docx and .pdf, jagi.sty) and the submissions page:
- US Letter, single column: pdfinfo 612 × 792 pt; one column. PASS.
- 1.25 inch side margins: reference document sectPr left and right 1800 twips. PASS.
- 11 pt Times: Normal style size 22 half-points, Times New Roman. PASS.
- Title 16 pt bold, title case: Article Title style, 32 half-points, bold; title in title case. PASS, but it breaks inside "ARC-AGI-3" (F24).
- Author block: name in Author Name style (bold 11 pt), affiliation, ORCID and e-mail in Author Address style (italic 10 pt); e-mail not in small capitals (F30).
- Abstract: centered bold "Abstract" (Abstract Title style), body in Abstract Text (10 pt, indented 0.25 in), bold "Keywords:" line inside it. PASS.
- Running heads: even pages "MISHRA", odd pages "A FRAME-ONLY CENSUS DID NOT GENERALIZE", from page 2 on, in simulated small capitals; page numbers centered in the footer from page 2. PASS (pdftotext, every page).
- First-page head: society logo with the licence notice "This is an open access article licensed under the Creative Commons BY-NC-ND 4.0 License." as the Kit prints it (it is part of the Kit's logo image), the journal name, and "Submitted 2026-10-24" (F26).
- References in the Kit's form with "(Author and Author, year)": yes; no "&" outside a cited title; manuscript_check.py (c) 24 cited, 24 entries.
- Appendices: none in the paper; the supplement uses S.1 to S.7. The Kit asks that online appendices be numbered "Online Appendix 1, …"; the supplement is a separate document cited as "Supplement, Section S.n" (listed for the author, Section 8).
- A single PDF for review: the paper is one PDF; the supplement is a second PDF (Section 8).
- Page by page (layout check of both PDFs at b93a700): title breaks inside "ARC-AGI-3" on page 1 of both (F24); tables split: paper Table 1 (pages 10-11), Table 2 (12-13); supplement S1 (1-2), S2b (2-3), S7 (8-9) (F25); every figure caption is on the same page as its figure (Figures 1-4 on pages 10, 12, 14, 16); no page ends with a heading; running heads correct on every page.
- docx metadata (both files): dc:creator "Rahul Kumar Mishra", dc:title the title, dc:language "en-US" (F39), cp:keywords empty, no subject, description or lastModifiedBy; app.xml holds only template, application, security, version flags. XML search over every part for "assistant", "Claude", "Co-Authored", "language model", "generated" and the Kit's sample names (Waser, Signorino, Pallai, Pei Wang, "Instructions for Formatting", Hewlett, Books International, Infinity Science): 0 hits in either file. PDF text search for the same: 0 hits in either PDF. PDF Author "Rahul Kumar Mishra"; Creator and Producer "Microsoft Word 2019".

## 6. A5, references

All 24 entries were fetched again on 24 October 2026 (Crossref API, arXiv API, PMLR, NeurIPS proceedings, IJCAI, AI Magazine article page, Stanford faculty profile). Every printed field was confirmed, with these notes:
- Bellemare et al. (2012): Crossref gives the OJS migration date (2021) as "issued"; volume 26, issue 1, pages 864-871 and the proceedings title confirm the 2012 AAAI-12 paper. The OJS page served an anti-bot page to this fetch; it was read on 14 Oct 2026 (docs/manuscript/REFERENCES_CHECK.md).
- Keren et al. (2014): Crossref has no issue number; issue 1 was read from the OJS page on 14 Oct 2026.
- Choi et al. (2019) and Chevalier-Boisvert et al. (2019): OpenReview served a verification page; arXiv comments "In ICLR 2019" and "Accepted at ICLR 2019" confirm the venue.
- Chevalier-Boisvert et al. (2023): pages 73383-73394 from Crossref; authors from the NeurIPS page (Perez-Vicente).
- Mitchell (1982): Crossref title in sentence case ("Generalization as search"); printed in title case per the Kit.
- Goldman and Kearns (1995): Crossref has initials only; full names from the 14 Oct record.
- Genesereth, Love and Pell (2005): the AI Magazine page confirms authors, title, DOI and 15 June 2005; the Stanford faculty profile of Genesereth (https://profiles.stanford.edu/michael-genesereth?tab=publications) gives "AI MAGAZINE … 2005; 26 (2): 62-72"; dblp (https://dblp.org/pid/53/1240) served an anti-bot page to the fetch, and RKM confirmed 62-72 from it. The end page is therefore confirmed (F35).

The six new references:

| work | sentence in the paper | supporting passage | verdict |
|---|---|---|---|
| Legg and Hutter (2007) | L24 "One widely cited definition takes intelligence to be an agent's ability to achieve goals in a wide range of environments" | "Intelligence measures an agent's ability to achieve goals in a wide range of environments." (arXiv full text, Section 2.6) | PARTLY: the definition SUPPORTED; "widely cited" NOT (F04) |
| Legg and Hutter (2007) | L46 "…took as their informal working definition that intelligence measures …, and turned it into a formal measure for arbitrary machines." | the passage above; abstract: "mathematically formalised to produce a general measure of intelligence for arbitrary machines" | SUPPORTED |
| Legg and Hutter (2007) | L226 "…define intelligence over a range of environments, so a claim …" | as above | SUPPORTED (first clause; the rest is argument) |
| Hernández-Orallo (2017) | L46 "…argues for a universal evaluation of cognition, in which living organisms are a special case, and uses algorithmic information theory as the foundation for questions such as whether the difficulty of a task can be derived from the task itself." | publisher's description (Crossref abstract): "offers a vision of the universal evaluation of cognition … where living organisms are considered as a special case … Can we derive task difficulty intrinsically? … Using algorithmic information theory as a foundation" | PARTLY: matches the publisher's description; the book was not read (F06) |
| Hernández-Orallo (2017), with the two others | L46 "All three treat the set of environments, and what an agent brings to them, as part of what a measurement means." | Legg and Hutter: environments; Chollet: priors and experience; nothing for Hernández-Orallo | NOT for Hernández-Orallo; PARTLY overall (F05) |
| Chollet (2019) | L46 "…argues that skill at any given task falls short of measuring intelligence, … presents the Abstraction and Reasoning Corpus (ARC) …" | abstract (arXiv 1911.01547) | SUPPORTED |
| Chollet (2019) | L226 "…asks that a benchmark of general intelligence control for priors and experience" | "we propose a set of guidelines for what a general AI benchmark should look like" with the passage on priors and experience | SUPPORTED (paraphrase) |
| Perez-Liebana et al. (2016) | L24 "The first General Video Game Playing Competition asked for a single agent … left it to the agents to discover the mechanics of each game" | abstract: "a single agent must be able to play many different games, some of them unknown to the participants … It is a responsibility of the agents to discover the mechanics of each game" | SUPPORTED (abstract via OpenAlex; IEEE page unreadable) |
| Perez-Liebana et al. (2016) | L42 "…an approximation of general artificial intelligence, because the amount of game-dependent heuristics had to be severely limited" | abstract: "This test can be seen as an approximation of general artificial intelligence, as the amount of game-dependent heuristics needs to be severely limited." | SUPPORTED (same source) |
| Perez-Liebana et al. (2019) | L42 "Five years after the framework was released, … describe it as games written in the Video Game Description Language and a set of tracks …" | arXiv abstract: "five years after its birth"; "play multiple unknown games with or without access to game simulations, or to design new game levels or rules" | SUPPORTED |
| Genesereth et al. (2005) | L42 "…define a general game playing system as one that can accept a formal description of a game and play it effectively without human intervention, and contrast it with specialized players …" | AI Magazine abstract | SUPPORTED |

**Hernández-Orallo (2017), decision.** The sentence that relies on the publisher's description is L46: "Hernández-Orallo (2017) argues for a universal evaluation of cognition, in which living organisms are a special case, and uses algorithmic information theory as the foundation for questions such as whether the difficulty of a task can be derived from the task itself." Proposed wording, claiming only what the description supports and saying where it comes from: "In its publisher's description, Hernández-Orallo (2017) sets out a universal evaluation of cognition in which living organisms are a special case, founded on algorithmic information theory." The alternative is to remove the sentence and the entry, which leaves Section 2.2 with Legg and Hutter and Chollet only. Stage B applies the proposed wording; reading the book, or removing it, is the author's decision (Section 8).

## 7. A6, the provenance loop

Table S5 of the supplement and Appendix C of the JOTE files name, for each source file, the commit that last changed it. docs/STATE.md is one of those files, and every STATE amendment changes its last commit, so every amendment makes the built files stale until they are rebuilt and the table recopied (STATE.md (p), (s), (t) record this for the JOTE files; (v) for the JAGI files, whose Table S5 names a224604 while STATE.md is now at b585ab2).

Proposed fix for Stage B: scripts/manuscript_numbers.py gains an option --state-ref TEXT. When it is given, the provenance table names docs/STATE.md with that text in place of a hash ("docs/STATE.md (at the commit tagged jagi-submission-v1)"), and the numbers.json entry for STATE.md's last commit carries the same text with class "identifier", so that no hash of STATE.md is checked. Without the option the script behaves as before. docs/manuscript_jagi/BUILD.md step 1 passes --state-ref "at the commit tagged jagi-submission-v1". The JOTE files are not rebuilt.

## 8. Needs the author's decision

- A citation for ARC-AGI-3 itself (technical report or launch post, as the CLAUDE.md must-cite list says). It needs a fetched, verified entry; draft 2 only narrows the sentence (F03).
- Hernández-Orallo (2017): keep the narrowed wording, read the book and restore a direct characterization, or remove the reference.
- The supplement as a second PDF: the Kit asks for a single PDF for review and calls online appendices "Online Appendix 1, …". Keep the supplement separate (on Zenodo, cited by the supplement-DOI placeholder), append it to the review PDF, or rename it "Online Appendix 1".
- The supplement-DOI placeholder: the Zenodo version with the supplement, and its DOI, before submission.
- The submission date in the first-page head, on the day of submission (BUILD.md step 5).
- F30 and F31 (small capitals for the e-mail; live links) for the camera-ready version.
- Whether to change the figure script so that the figure labels use the paper's terms (F28, F29); the script also draws the JOTE figures.

## 9. Count of findings

39 findings: BLOCKING 5 (F01, F02, F03, F04, F05); MAJOR 18 (F06, F07, F08, F09, F10, F11, F12, F13, F15, F16, F17, F18, F19, F20, F21, F24, F25, F34); MINOR 16 (F14, F22, F23, F26, F27, F28, F29, F30, F31, F32, F33, F35, F36, F37, F38, F39). Of the 158 sentences of Section 3, 146 are SUPPORTED and 12 carry a finding.
