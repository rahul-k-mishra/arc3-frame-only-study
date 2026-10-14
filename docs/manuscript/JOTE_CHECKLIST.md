# JOTE submission checklist, manuscript draft 1

One line per requirement, with where in docs/manuscript/manuscript.md (or the named file) it is satisfied. The automatic checks are those of scripts/manuscript_check.py, labeled (a) to (g).

| requirement | where it is satisfied |
|---|---|
| J1 Empirical Article structure and order | Title (front matter), author block, Keywords (five), Take-home message, Abstract, Introduction, Method, Results, Exploratory diagnosis, Purpose (immediately before Discussion), Discussion, Conclusion (refers back to Purpose and states the failures), Data and code availability, Funding, Conflicts of interest, References, Appendices A to D; limits checked by (e): take-home 49 words and 3 sentences, abstract 244 words, purpose 183 words |
| J2 APA 7 citations and complete matching reference list | author-date citations throughout; References built from docs/preprint/references.bib as verified in docs/preprint/REFERENCES_CHECK.md; check (c): 17 cited works, 17 entries, 0 unmatched |
| J3 figures preferred, embedded at first reference, captions with content, source and status | Figures 1 and 2 (registered, Results) and Figures 3 and 4 (exploratory, Exploratory diagnosis), each placed after the paragraph that first cites it, each caption naming its source file and status; tables kept only where verbatim registered output or lists are required (Tables 1 to 5, B1, C1, D1); check (f) |
| J4 .docx built by pandoc, metadata author only the author's name | docs/manuscript/BUILD.md step 4; docProps/core.xml of manuscript.docx has dc:creator "Rahul Kumar Mishra" and no other person or tool |
| J5 open review, name and affiliation shown | author block at the top of the manuscript and of the cover letter |
| J6 data and code statement | Data and code availability: repository URL, MIT license, the 10,500 confirmatory rows, the 500-row ARC-AGI-3 baseline, pilot and check outputs, three tags with full commit hashes, the two OSF registration URLs, external/rudakov_just_explore keeping its upstream MIT notice |
| J7 preprint line with placeholder | below the author block and at the end of Data and code availability in the manuscript; in cover_letter.md |
| J8 cover letter | docs/manuscript/cover_letter.md: addressed to the Editor-in-Chief, Empirical Article, preprint line, data and code links, the venue-clause statement and the deviation, single author, no conflicts, no funding, one paragraph on fit |
| R1 single author, first person singular, funding and conflicts once each, no acknowledgements | author block; text in "I" (no "we", "our" or "us" in the manuscript); Funding and Conflicts of interest sections; no acknowledgement section |
| R2 no mention of any writing or coding aid | check (b) on the manuscript; the same word list run over cover_letter.md and BUILD.md and over the XML of both .docx files found no hit; file names and commit message carry none |
| R3 plain human tone, no body lists, forbidden words, American spelling | body is prose; lists only in Appendix B; check (b) 0 hits outside cited titles (the Cobbe et al. title keeps its own wording); check (d) 0 British spellings |
| R4 every number from numbers.json | scripts/manuscript_numbers.py writes docs/manuscript/numbers.json with a source for every value; check (a) 0 numerals, hashes, dates or URLs outside it; Appendix C (check (g)) |
| R5 the check script | scripts/manuscript_check.py, checks (a) to (g), exit code 0 on the committed text |
| R6 exploratory material confined and labeled | Exploratory diagnosis section, every paragraph and both figure captions (Figures 3 and 4) and Table 5 carry the word "exploratory"; the Discussion paragraphs that draw on it say so; no fix presented as a result; no future-work section |
| R7 outcome stated as registered | Results (Table 4 and the gate paragraph), Abstract and Conclusion state REFUTE by "V1 fails on any suite"; Method (Truth from source) and Discussion (first subsection) state that the truth tables are the answer key and the census is the instrument under test |
