# References check, KI manuscript draft 1 (2 November 2026)

The KI manuscript keeps the 24 entries of the JAGI manuscript, no more and no fewer. No entry was added: the new framing (general video game playing, the evaluation of agents on unseen games, Bontrager et al. as the closest earlier attempt) is carried by entries that were already in the list, and every sentence that characterizes a cited work is a sentence of the JAGI text, moved into the new order of the background, with its verdict as recorded in docs/manuscript_jagi/REFERENCES_CHECK_jagi.md (six entries) and in docs/manuscript/REFERENCES_CHECK.md with docs/manuscript/REVIEW_draft1.md Section 6 (the other 18). Nothing was retyped from memory: every field of docs/manuscript_ki/references_ki.bib is copied from those verified entries.

## The restyling

KI's submission guidelines (fetched 2 November 2026; docs/manuscript_ki/JOURNAL_REQUIREMENTS.md) ask for citations "identified by numbers in square brackets", entries "numbered consecutively", and DOIs "as full DOI links". The template's numbered style is spmpsci.bst from the Springer LaTeX package; the entries are typeset by BibTeX from references_ki.bib. What the style does, and what was done about it:

- Numbering. spmpsci sorts the list alphabetically by first author and numbers it in that order; a citation carries the number of its entry. The list is therefore numbered consecutively, but not in order of first citation.
- Author names. Family name, then initials, separated by commas, with a colon after the last author. Initials are written by BibTeX from the given names in the verified records. One name needed protection: the hyphenated initials of Chong-U Lim, which BibTeX would print as "C.U."; the field is written so that it prints "C.-U.", as in the verified entry.
- Titles. The style sets titles in sentence case. Proper nouns are protected with braces in the .bib file so that they keep their capitals (Atari, AAAI, ARC-AGI-3, BabyAI, Minigrid, Miniworld, General Video Game Playing Competition, General Video Game AI, IEEE, CIG, IJCAI, NeurIPS, RL, Twin, Ladder).
- Journal names. The guidelines ask for the ISSN abbreviation of a journal's name and accept the full title where the author is unsure. The full titles are kept, as in the verified entries.
- Proceedings published as numbered volumes by AAAI (AAAI, AIIDE, ICAPS) keep the periodical form decided in the JOTE review (volume(issue), pages), as in the JAGI list.
- DOIs. The style writes "DOI 10.xxxx"; the template redefines that command so that each DOI is printed as its full link, https://doi.org/10.xxxx, as the guidelines ask. URLs are printed without a "URL" label.
- The ARC Prize Foundation report has no DOI; it is printed with its date, its URL and "Accessed 24 October 2026", the guidelines' form for an online document. The JAGI list wrote "(fetched 24 October 2026)".
- Liew (2026). The title is set with an en dash, "Speed–Depth", as in the verified record docs/preprint/references.bib ("Speed--Depth"). The JAGI list printed a hyphen, because that journal's PDF rules excluded the en dash (CHANGES_jagi_draft3.md, F40); KI has no such rule.
- Page ranges are set with an en dash by the style; the JAGI list used a hyphen for the same reason.

## How the check uses this file

A line that begins "Printed: " is an entry exactly as the build prints it: the entry of manuscript_ki.bbl written as plain text by scripts/manuscript_check.py (function bbl_entries; the style's commands removed, each DOI as its link, "--" as an en dash). manuscript_check.py, run with --dir docs/manuscript_ki --bib references_ki.bib, accepts the numerals and the links of a printed entry only if it equals one of these lines character for character, and otherwise checks every numeral in it against numbers.json. Each entry below gives the verified JAGI entry, the printed KI entry, and a comparison made by script on 2 November 2026: the numerals of the two (years, volumes, issues, pages, editions; URLs excluded) as sorted lists, the DOI or URL, and the words of the verified entry that are absent from the printed one (case and accents ignored). All 24 entries have equal numerals, equal links and no missing word.

## The 24 entries, in printed order

### [1] arcprize2026arcagi3

Verified entry (JAGI list): ARC Prize Foundation. 2026. ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence. Technical report, 22 April 2026. https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf (fetched 24 October 2026).

Printed: ARC Prize Foundation: ARC-AGI-3: A new challenge for frontier agentic intelligence. Technical report, 22 April 2026 (2026). https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf. Accessed 24 October 2026

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [2] bellemare2012contingency

Verified entry (JAGI list): Bellemare, M. G.; Veness, J.; and Bowling, M. 2012. Investigating Contingency Awareness Using Atari 2600 Games. *Proceedings of the AAAI Conference on Artificial Intelligence* 26(1): 864-871. https://doi.org/10.1609/aaai.v26i1.8321

Printed: Bellemare, M.G., Veness, J., Bowling, M.: Investigating contingency awareness using Atari 2600 games. Proceedings of the AAAI Conference on Artificial Intelligence 26(1), 864–871 (2012). https://doi.org/10.1609/aaai.v26i1.8321

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [3] bertinetto2021preregistration

Verified entry (JAGI list): Bertinetto, L.; Henriques, J. F.; Albanie, S.; Paganini, M.; and Varol, G. 2021. Preface. In Bertinetto, L.; Henriques, J. F.; Albanie, S.; Paganini, M.; and Varol, G., eds., *NeurIPS 2020 Workshop on Pre-registration in Machine Learning*, Proceedings of Machine Learning Research 148, i. PMLR. https://proceedings.mlr.press/v148/bertinetto21a.html

Printed: Bertinetto, L., Henriques, J.F., Albanie, S., Paganini, M., Varol, G.: Preface. In: L. Bertinetto, J.F. Henriques, S. Albanie, M. Paganini, G. Varol (eds.) NeurIPS 2020 Workshop on Pre-registration in Machine Learning, Proceedings of Machine Learning Research, vol. 148, p. i. PMLR (2021). https://proceedings.mlr.press/v148/bertinetto21a.html

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [4] blum2015ladder

Verified entry (JAGI list): Blum, A., and Hardt, M. 2015. The Ladder: A Reliable Leaderboard for Machine Learning Competitions. In Bach, F., and Blei, D., eds., *Proceedings of the 32nd International Conference on Machine Learning*, Proceedings of Machine Learning Research 37, 1006-1014. PMLR. https://proceedings.mlr.press/v37/blum15.html

Printed: Blum, A., Hardt, M.: The Ladder: A reliable leaderboard for machine learning competitions. In: F. Bach, D. Blei (eds.) Proceedings of the 32nd International Conference on Machine Learning, Proceedings of Machine Learning Research, vol. 37, pp. 1006–1014. PMLR (2015). https://proceedings.mlr.press/v37/blum15.html

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [5] bontrager2016matching

Verified entry (JAGI list): Bontrager, P.; Khalifa, A.; Mendes, A.; and Togelius, J. 2016. Matching Games and Algorithms for General Video Game Playing. *Proceedings of the AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment* 12(1): 122-128. https://doi.org/10.1609/aiide.v12i1.12884

Printed: Bontrager, P., Khalifa, A., Mendes, A., Togelius, J.: Matching games and algorithms for general video game playing. Proceedings of the AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment 12(1), 122–128 (2016). https://doi.org/10.1609/aiide.v12i1.12884

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [6] chevalierboisvert2019babyai

Verified entry (JAGI list): Chevalier-Boisvert, M.; Bahdanau, D.; Lahlou, S.; Willems, L.; Saharia, C.; Nguyen, T. H.; and Bengio, Y. 2019. BabyAI: A Platform to Study the Sample Efficiency of Grounded Language Learning. In *International Conference on Learning Representations*. https://openreview.net/forum?id=rJeXCo0cYX

Printed: Chevalier-Boisvert, M., Bahdanau, D., Lahlou, S., Willems, L., Saharia, C., Nguyen, T.H., Bengio, Y.: BabyAI: A platform to study the sample efficiency of grounded language learning. In: International Conference on Learning Representations (2019). https://openreview.net/forum?id=rJeXCo0cYX

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [7] chevalierboisvert2023minigrid

Verified entry (JAGI list): Chevalier-Boisvert, M.; Dai, B.; Towers, M.; Perez-Vicente, R.; Willems, L.; Lahlou, S.; Pal, S.; Castro, P. S.; and Terry, J. 2023. Minigrid & Miniworld: Modular & Customizable Reinforcement Learning Environments for Goal-Oriented Tasks. In *Advances in Neural Information Processing Systems 36*, 73383-73394. https://doi.org/10.52202/075280-3209

Printed: Chevalier-Boisvert, M., Dai, B., Towers, M., Perez-Vicente, R., Willems, L., Lahlou, S., Pal, S., Castro, P.S., Terry, J.: Minigrid & Miniworld: Modular & customizable reinforcement learning environments for goal-oriented tasks. In: Advances in Neural Information Processing Systems 36, pp. 73383–73394 (2023). https://doi.org/10.52202/075280-3209

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [8] choi2019contingency

Verified entry (JAGI list): Choi, J.; Guo, Y.; Moczulski, M.; Oh, J.; Wu, N.; Norouzi, M.; and Lee, H. 2019. Contingency-Aware Exploration in Reinforcement Learning. In *International Conference on Learning Representations*. https://openreview.net/forum?id=HyxGB2AcY7

Printed: Choi, J., Guo, Y., Moczulski, M., Oh, J., Wu, N., Norouzi, M., Lee, H.: Contingency-aware exploration in reinforcement learning. In: International Conference on Learning Representations (2019). https://openreview.net/forum?id=HyxGB2AcY7

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [9] chollet2019measure

Verified entry (JAGI list): Chollet, F. 2019. On the Measure of Intelligence. Preprint, arXiv. https://arxiv.org/abs/1911.01547

Printed: Chollet, F.: On the measure of intelligence. Preprint, arXiv (2019). https://arxiv.org/abs/1911.01547

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [10] cobbe2020procgen

Verified entry (JAGI list): Cobbe, K.; Hesse, C.; Hilton, J.; and Schulman, J. 2020. Leveraging Procedural Generation to Benchmark Reinforcement Learning. In Daumé III, H., and Singh, A., eds., *Proceedings of the 37th International Conference on Machine Learning*, Proceedings of Machine Learning Research 119, 2048-2056. PMLR. https://proceedings.mlr.press/v119/cobbe20a.html

Printed: Cobbe, K., Hesse, C., Hilton, J., Schulman, J.: Leveraging procedural generation to benchmark reinforcement learning. In: H. Daumé III, A. Singh (eds.) Proceedings of the 37th International Conference on Machine Learning, Proceedings of Machine Learning Research, vol. 119, pp. 2048–2056. PMLR (2020). https://proceedings.mlr.press/v119/cobbe20a.html

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [11] gaina2018winprediction

Verified entry (JAGI list): Gaina, R. D.; Lucas, S. M.; and Perez-Liebana, D. 2018. General Win Prediction from Agent Experience. In *2018 IEEE Conference on Computational Intelligence and Games (CIG)*, 1-8. https://doi.org/10.1109/CIG.2018.8490439

Printed: Gaina, R.D., Lucas, S.M., Perez-Liebana, D.: General win prediction from agent experience. In: 2018 IEEE Conference on Computational Intelligence and Games (CIG), pp. 1–8 (2018). https://doi.org/10.1109/CIG.2018.8490439

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [12] genesereth2005ggp

Verified entry (JAGI list): Genesereth, M.; Love, N.; and Pell, B. 2005. General Game Playing: Overview of the AAAI Competition. *AI Magazine* 26(2): 62-72. https://doi.org/10.1609/aimag.v26i2.1813

Printed: Genesereth, M., Love, N., Pell, B.: General game playing: Overview of the AAAI competition. AI Magazine 26(2), 62–72 (2005). https://doi.org/10.1609/aimag.v26i2.1813

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [13] goldman1995teaching

Verified entry (JAGI list): Goldman, S. A., and Kearns, M. J. 1995. On the Complexity of Teaching. *Journal of Computer and System Sciences* 50(1): 20-31. https://doi.org/10.1006/jcss.1995.1003

Printed: Goldman, S.A., Kearns, M.J.: On the complexity of teaching. Journal of Computer and System Sciences 50(1), 20–31 (1995). https://doi.org/10.1006/jcss.1995.1003

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [14] keren2014grd

Verified entry (JAGI list): Keren, S.; Gal, A.; and Karpas, E. 2014. Goal Recognition Design. *Proceedings of the International Conference on Automated Planning and Scheduling* 24(1): 154-162. https://doi.org/10.1609/icaps.v24i1.13617

Printed: Keren, S., Gal, A., Karpas, E.: Goal recognition design. Proceedings of the International Conference on Automated Planning and Scheduling 24(1), 154–162 (2014). https://doi.org/10.1609/icaps.v24i1.13617

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [15] laidlaw2023horizon

Verified entry (JAGI list): Laidlaw, C.; Russell, S. J.; and Dragan, A. 2023. Bridging RL Theory and Practice with the Effective Horizon. In *Advances in Neural Information Processing Systems 36*, 58953-59007. https://doi.org/10.52202/075280-2573

Printed: Laidlaw, C., Russell, S.J., Dragan, A.: Bridging RL theory and practice with the effective horizon. In: Advances in Neural Information Processing Systems 36, pp. 58953–59007 (2023). https://doi.org/10.52202/075280-2573

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [16] legg2007universal

Verified entry (JAGI list): Legg, S., and Hutter, M. 2007. Universal Intelligence: A Definition of Machine Intelligence. *Minds and Machines* 17(4): 391-444. https://doi.org/10.1007/s11023-007-9079-x

Printed: Legg, S., Hutter, M.: Universal intelligence: A definition of machine intelligence. Minds and Machines 17(4), 391–444 (2007). https://doi.org/10.1007/s11023-007-9079-x

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [17] liew2026explore

Verified entry (JAGI list): Liew, K. H. 2026. Explore Before You Solve: The Speed-Depth Trade-off in Epistemic Agents for ARC-AGI-3. Preprint, arXiv. https://arxiv.org/abs/2605.25931

Printed: Liew, K.H.: Explore before you solve: The speed–depth trade-off in epistemic agents for ARC-AGI-3. Preprint, arXiv (2026). https://arxiv.org/abs/2605.25931

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [18] mitchell1982generalization

Verified entry (JAGI list): Mitchell, T. M. 1982. Generalization as Search. *Artificial Intelligence* 18(2): 203-226. https://doi.org/10.1016/0004-3702(82)90040-6

Printed: Mitchell, T.M.: Generalization as search. Artificial Intelligence 18(2), 203–226 (1982). https://doi.org/10.1016/0004-3702(82)90040-6

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [19] perezliebana2019gvgai

Verified entry (JAGI list): Perez-Liebana, D.; Liu, J.; Khalifa, A.; Gaina, R. D.; Togelius, J.; and Lucas, S. M. 2019. General Video Game AI: A Multitrack Framework for Evaluating Agents, Games, and Content Generation Algorithms. *IEEE Transactions on Games* 11(3): 195-214. https://doi.org/10.1109/TG.2019.2901021

Printed: Perez-Liebana, D., Liu, J., Khalifa, A., Gaina, R.D., Togelius, J., Lucas, S.M.: General Video Game AI: A multitrack framework for evaluating agents, games, and content generation algorithms. IEEE Transactions on Games 11(3), 195–214 (2019). https://doi.org/10.1109/TG.2019.2901021

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [20] perezliebana2016gvgp

Verified entry (JAGI list): Perez-Liebana, D.; Samothrakis, S.; Togelius, J.; Schaul, T.; Lucas, S. M.; Couetoux, A.; Lee, J.; Lim, C.-U.; and Thompson, T. 2016. The 2014 General Video Game Playing Competition. *IEEE Transactions on Computational Intelligence and AI in Games* 8(3): 229-243. https://doi.org/10.1109/TCIAIG.2015.2402393

Printed: Perez-Liebana, D., Samothrakis, S., Togelius, J., Schaul, T., Lucas, S.M., Couetoux, A., Lee, J., Lim, C.-U., Thompson, T.: The 2014 General Video Game Playing Competition. IEEE Transactions on Computational Intelligence and AI in Games 8(3), 229–243 (2016). https://doi.org/10.1109/TCIAIG.2015.2402393

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [21] roelofs2019metaanalysis

Verified entry (JAGI list): Roelofs, R.; Shankar, V.; Recht, B.; Fridovich-Keil, S.; Hardt, M.; Miller, J.; and Schmidt, L. 2019. A Meta-Analysis of Overfitting in Machine Learning. In *Advances in Neural Information Processing Systems 32*. https://papers.nips.cc/paper_files/paper/2019/hash/ee39e503b6bedf0c98c388b7e8589aca-Abstract.html

Printed: Roelofs, R., Shankar, V., Recht, B., Fridovich-Keil, S., Hardt, M., Miller, J., Schmidt, L.: A meta-analysis of overfitting in machine learning. In: Advances in Neural Information Processing Systems 32 (2019). https://papers.nips.cc/paper_files/paper/2019/hash/ee39e503b6bedf0c98c388b7e8589aca-Abstract.html

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [22] rudakov2025graph

Verified entry (JAGI list): Rudakov, E.; Shock, J.; and Cowley, B. U. 2025. Graph-Based Exploration for ARC-AGI-3 Interactive Reasoning Tasks. Preprint, arXiv. https://arxiv.org/abs/2512.24156

Printed: Rudakov, E., Shock, J., Cowley, B.U.: Graph-based exploration for ARC-AGI-3 interactive reasoning tasks. Preprint, arXiv (2025). https://arxiv.org/abs/2512.24156

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [23] skoutnev2026twin

Verified entry (JAGI list): Skoutnev, A.; Acharya, K.; Longhitano, G.; Udell, M.; Ellis, K.; and Drori, I. 2026. Twin: Playing an Unknown Game with a Test-Time Digital Twin. Preprint, arXiv. https://arxiv.org/abs/2608.14490

Printed: Skoutnev, A., Acharya, K., Longhitano, G., Udell, M., Ellis, K., Drori, I.: Twin: Playing an unknown game with a test-time digital twin. Preprint, arXiv (2026). https://arxiv.org/abs/2608.14490

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.

### [24] wayllace2016grd

Verified entry (JAGI list): Wayllace, C.; Hou, P.; Yeoh, W.; and Son, T. C. 2016. Goal Recognition Design with Stochastic Agent Action Outcomes. In *Proceedings of the Twenty-Fifth International Joint Conference on Artificial Intelligence (IJCAI-16)*, 3279-3285. https://www.ijcai.org/Proceedings/16/Papers/464.pdf

Printed: Wayllace, C., Hou, P., Yeoh, W., Son, T.C.: Goal recognition design with stochastic agent action outcomes. In: Proceedings of the Twenty-Fifth International Joint Conference on Artificial Intelligence (IJCAI-16), pp. 3279–3285 (2016). https://www.ijcai.org/Proceedings/16/Papers/464.pdf

Comparison: numerals equal; DOI or URL equal; words of the verified entry missing from the printed one: none.
