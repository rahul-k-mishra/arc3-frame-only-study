# References check, IEEE Transactions on Games version (2 November 2026)

The 24 entries of the JAGI version (docs/manuscript_jagi/manuscript_jagi.md) are kept, none added and none removed. They are reset here in IEEE style. No field was retyped from memory: every author list, title, venue, volume, issue, page range, year, DOI and URL was taken from the records listed under each entry. Those records are docs/manuscript/REFERENCES_CHECK.md, docs/manuscript/REVIEW_draft1.md Section 6 and docs/preprint/references.bib for the 18 entries of the JOTE version, and docs/manuscript_jagi/REFERENCES_CHECK_jagi.md for the six entries added for JAGI.

## The style applied

The rules are from the IEEE Reference Guide, V 3.28.2025, fetched on 2 November 2026 from the Author Center link https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE_Reference_Guide.pdf, which redirects to a Google document that was exported as text.

- Entries are numbered in order of first citation and cited in the text as [n].
- Initials come before the family name. All authors are listed up to six. For more than six, the first author is followed by "et al.". The guide says: "If there are more than six names listed, use the primary author's name followed by 'et al.'"
- Article titles are in quotation marks and in sentence case, as in the guide's examples. Proper names and acronyms keep their capitals: Atari, BabyAI, Minigrid, Miniworld, ARC-AGI-3, AAAI, RL, Twin, the Ladder, General Video Game AI, and the 2014 General Video Game Playing Competition. For the 18 JOTE entries the sentence-case titles are those of the verified APA list in docs/manuscript/manuscript.md. For the six JAGI entries they are the verified titles with only the capitals changed.
- Journal and proceedings names are in italics. They are abbreviated with the word list of the guide: Artificial to Artif., Computer and Computational to Comput., Conference to Conf., Digital to Digit., Information to Inf., Intelligence to Intell., International to Int., Journal to J., Learning to Learn., Machine to Mach., Magazine to Mag., Proceedings to Proc., Processing to Process., Research to Res., Science(s) to Sci., Systems to Syst., Transactions to Trans. Words that are not on the list stay in full: Advances, Neural, Representations, Games, Entertainment, Interactive, Automated, Planning, Scheduling, Joint, Minds and Machines.
- Journal articles take the form vol. x, no. x, pp. x–y, month (where the record gives the issue month), year, doi: x. Proceedings take the form in *Proc. ...*, editors where the record gives them, vol. x, no. x, year, pp. x–y, then the doi or "[Online]. Available: URL". Preprints take the form "Title," year, arXiv:id, as the guide's "Preprint arXiv" format. The ARC-AGI-3 report follows the guide's "Report Online" form: Tech. Rep., date, "Accessed:" date, "[Online]. Available:" URL.
- Months are given only where the verified record names the issue month: September 2016 and September 2019 for the two IEEE journal articles. No other month was recorded, and none was supplied.

## Field cross-check

A comparison script (kept outside the repository, run on 2 November 2026) set each IEEE entry against the verified JAGI entry for the same work. For every numeral, DOI and URL, and for the family names of all authors, it found no difference except the restyling below:

- arXiv entries: the JAGI URL https://arxiv.org/abs/<id> is written arXiv:<id>, with the same identifier, for Chollet, Liew, Rudakov et al. and Skoutnev et al.
- Wayllace et al.: "Twenty-Fifth" is written "25th".
- Entries with more than six authors (BabyAI, Minigrid, Choi et al., Perez-Liebana et al. 2016, Roelofs et al.): the first family name matches and the rest are replaced by "et al.".

The characterizing sentences of the manuscript are the JAGI sentences, shortened, and no new characterization was added. Two changes in wording were checked against the passages recorded in the earlier checks:

- Goal recognition design [23], [24] "concerns an outside observer of an actor's goal". This is supported by Keren et al., "an upper bound on the number of actions any optimal agent can perform in a model before revealing its goal", and by Wayllace et al., "the largest expected cost to reach a boundary state ... over all possible non-distinctive policy prefixes" (docs/manuscript/REVIEW_draft1.md, Section 6.2).
- Legg and Hutter [8] "take intelligence to measure an agent's ability to achieve goals in a wide range of environments". This is supported by "Intelligence measures an agent's ability to achieve goals in a wide range of environments. We take this to be our informal working definition of intelligence." (docs/manuscript_jagi/REFERENCES_CHECK_jagi.md).

## The entries as printed

A line that begins "Printed: " is the entry exactly as it stands in docs/manuscript_tog/manuscript_tog.md, without its "[n] " label. scripts/manuscript_check.py, run with --dir docs/manuscript_tog --ieee, accepts the numerals and URLs of a reference entry only if the entry equals one of these lines character for character.

### [1]

Fields from: docs/manuscript_jagi/REFERENCES_CHECK_jagi.md (Crossref: volume 8, issue 3, pages 229-243, issue of September 2016). Nine authors, so "et al.".

Printed: D. Perez-Liebana *et al.*, "The 2014 General Video Game Playing Competition," *IEEE Trans. Comput. Intell. AI Games*, vol. 8, no. 3, pp. 229–243, Sep. 2016, doi: 10.1109/TCIAIG.2015.2402393.

### [2]

Fields from: docs/manuscript_jagi/REFERENCES_CHECK_jagi.md (ARC Prize Foundation 2026): report fetched 24 October 2026; organization author, title, date 22 April 2026, URL.

Printed: ARC Prize Foundation, "ARC-AGI-3: A new challenge for frontier agentic intelligence," Tech. Rep., Apr. 22, 2026. Accessed: Oct. 24, 2026. [Online]. Available: https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf

### [3]

Fields from: docs/manuscript/REFERENCES_CHECK.md (NeurIPS proceedings page: volume 36, pages 73383-73394, DOI 10.52202/075280-3209). Nine authors, so "et al.".

Printed: M. Chevalier-Boisvert *et al.*, "Minigrid & Miniworld: Modular & customizable reinforcement learning environments for goal-oriented tasks," in *Advances in Neural Inf. Process. Syst.*, vol. 36, 2023, pp. 73383–73394, doi: 10.52202/075280-3209.

### [4]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (OpenReview) and references.bib. Seven authors, so the first followed by "et al.".

Printed: M. Chevalier-Boisvert *et al.*, "BabyAI: A platform to study the sample efficiency of grounded language learning," in *Proc. Int. Conf. Learn. Representations*, 2019. [Online]. Available: https://openreview.net/forum?id=rJeXCo0cYX

### [5]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (PMLR page; editors H. Daume III and A. Singh) and references.bib.

Printed: K. Cobbe, C. Hesse, J. Hilton, and J. Schulman, "Leveraging procedural generation to benchmark reinforcement learning," in *Proc. 37th Int. Conf. Mach. Learn.*, H. Daumé III and A. Singh, Eds., Proc. Mach. Learn. Res., vol. 119, 2020, pp. 2048–2056. [Online]. Available: https://proceedings.mlr.press/v119/cobbe20a.html

### [6]

Fields from: docs/manuscript_jagi/REFERENCES_CHECK_jagi.md (AI Magazine page; end page 72 from the Stanford faculty profile and dblp).

Printed: M. Genesereth, N. Love, and B. Pell, "General game playing: Overview of the AAAI competition," *AI Mag.*, vol. 26, no. 2, pp. 62–72, 2005, doi: 10.1609/aimag.v26i2.1813.

### [7]

Fields from: docs/manuscript_jagi/REFERENCES_CHECK_jagi.md (Crossref: volume 11, issue 3, pages 195-214, issue of September 2019). Six authors, all listed.

Printed: D. Perez-Liebana, J. Liu, A. Khalifa, R. D. Gaina, J. Togelius, and S. M. Lucas, "General Video Game AI: A multitrack framework for evaluating agents, games, and content generation algorithms," *IEEE Trans. Games*, vol. 11, no. 3, pp. 195–214, Sep. 2019, doi: 10.1109/TG.2019.2901021.

### [8]

Fields from: docs/manuscript_jagi/REFERENCES_CHECK_jagi.md (Crossref and arXiv).

Printed: S. Legg and M. Hutter, "Universal intelligence: A definition of machine intelligence," *Minds and Machines*, vol. 17, no. 4, pp. 391–444, 2007, doi: 10.1007/s11023-007-9079-x.

### [9]

Fields from: docs/manuscript_jagi/REFERENCES_CHECK_jagi.md (arXiv record 1911.01547).

Printed: F. Chollet, "On the measure of intelligence," 2019, arXiv:1911.01547.

### [10]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (AIIDE page) and references.bib.

Printed: P. Bontrager, A. Khalifa, A. Mendes, and J. Togelius, "Matching games and algorithms for general video game playing," in *Proc. AAAI Conf. Artif. Intell. Interactive Digit. Entertainment*, vol. 12, no. 1, 2016, pp. 122–128, doi: 10.1609/aiide.v12i1.12884.

### [11]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (Crossref) and references.bib.

Printed: R. D. Gaina, S. M. Lucas, and D. Perez-Liebana, "General win prediction from agent experience," in *Proc. 2018 IEEE Conf. Comput. Intell. Games (CIG)*, 2018, pp. 1–8, doi: 10.1109/CIG.2018.8490439.

### [12]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (Crossref) and references.bib.

Printed: C. Laidlaw, S. J. Russell, and A. Dragan, "Bridging RL theory and practice with the effective horizon," in *Advances in Neural Inf. Process. Syst.*, vol. 36, 2023, pp. 58953–59007, doi: 10.52202/075280-2573.

### [13]

Fields from: docs/manuscript/REVIEW_draft1.md Sections 6.1 and 6.4 (arXiv; the workshop is non-archival, so the arXiv form stays) and references.bib.

Printed: E. Rudakov, J. Shock, and B. U. Cowley, "Graph-based exploration for ARC-AGI-3 interactive reasoning tasks," 2025, arXiv:2512.24156.

### [14]

Fields from: docs/manuscript/REVIEW_draft1.md Sections 6.1 and 6.4 (arXiv; the family name is Liew) and references.bib.

Printed: K. H. Liew, "Explore before you solve: The speed–depth trade-off in epistemic agents for ARC-AGI-3," 2026, arXiv:2605.25931.

### [15]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (arXiv) and references.bib. Six authors, all listed.

Printed: A. Skoutnev, K. Acharya, G. Longhitano, M. Udell, K. Ellis, and I. Drori, "Twin: Playing an unknown game with a test-time digital twin," 2026, arXiv:2608.14490.

### [16]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (AAAI page) and docs/preprint/references.bib.

Printed: M. G. Bellemare, J. Veness, and M. Bowling, "Investigating contingency awareness using Atari 2600 games," in *Proc. AAAI Conf. Artif. Intell.*, vol. 26, no. 1, 2012, pp. 864–871, doi: 10.1609/aaai.v26i1.8321.

### [17]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (OpenReview) and references.bib. Seven authors, so "et al.".

Printed: J. Choi *et al.*, "Contingency-aware exploration in reinforcement learning," in *Proc. Int. Conf. Learn. Representations*, 2019. [Online]. Available: https://openreview.net/forum?id=HyxGB2AcY7

### [18]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (PMLR page) and references.bib (editors F. Bach and D. Blei).

Printed: A. Blum and M. Hardt, "The Ladder: A reliable leaderboard for machine learning competitions," in *Proc. 32nd Int. Conf. Mach. Learn.*, F. Bach and D. Blei, Eds., Proc. Mach. Learn. Res., vol. 37, 2015, pp. 1006–1014. [Online]. Available: https://proceedings.mlr.press/v37/blum15.html

### [19]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (NeurIPS page; no DOI exists) and references.bib. Seven authors, so "et al.".

Printed: R. Roelofs *et al.*, "A meta-analysis of overfitting in machine learning," in *Advances in Neural Inf. Process. Syst.*, vol. 32, 2019. [Online]. Available: https://papers.nips.cc/paper_files/paper/2019/hash/ee39e503b6bedf0c98c388b7e8589aca-Abstract.html

### [20]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (PMLR page: item "Preface", PMLR 148, p. i; the editors are the authors) and references.bib.

Printed: L. Bertinetto, J. F. Henriques, S. Albanie, M. Paganini, and G. Varol, "Preface," in *NeurIPS 2020 Workshop on Pre-registration in Machine Learning*, L. Bertinetto, J. F. Henriques, S. Albanie, M. Paganini, and G. Varol, Eds., Proc. Mach. Learn. Res., vol. 148, 2021, p. i. [Online]. Available: https://proceedings.mlr.press/v148/bertinetto21a.html

### [21]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (Crossref) and references.bib.

Printed: S. A. Goldman and M. J. Kearns, "On the complexity of teaching," *J. Comput. Syst. Sci.*, vol. 50, no. 1, pp. 20–31, 1995, doi: 10.1006/jcss.1995.1003.

### [22]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (Crossref) and references.bib.

Printed: T. M. Mitchell, "Generalization as search," *Artif. Intell.*, vol. 18, no. 2, pp. 203–226, 1982, doi: 10.1016/0004-3702(82)90040-6.

### [23]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (ICAPS page) and references.bib.

Printed: S. Keren, A. Gal, and E. Karpas, "Goal recognition design," in *Proc. Int. Conf. Automated Planning and Scheduling*, vol. 24, no. 1, 2014, pp. 154–162, doi: 10.1609/icaps.v24i1.13617.

### [24]

Fields from: docs/manuscript/REVIEW_draft1.md Section 6.1 (IJCAI PDF) and references.bib. "Twenty-Fifth" is written "25th", as IEEE writes ordinals in conference names.

Printed: C. Wayllace, P. Hou, W. Yeoh, and T. C. Son, "Goal recognition design with stochastic agent action outcomes," in *Proc. 25th Int. Joint Conf. Artif. Intell. (IJCAI-16)*, 2016, pp. 3279–3285. [Online]. Available: https://www.ijcai.org/Proceedings/16/Papers/464.pdf
