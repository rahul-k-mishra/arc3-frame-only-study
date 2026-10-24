# References check, JAGI manuscript (24 October 2026)

The 18 entries of the JOTE manuscript are kept with every field unchanged; their verification is recorded in docs/manuscript/REFERENCES_CHECK.md and docs/manuscript/REVIEW_draft1.md Section 6. In this version they are set in the reference style of the JAGI Author's Kit (Instruction-word.docx, Appendix A: authors separated by semicolons, the year after the authors without parentheses, titles as the publisher prints them, then the venue, volume(issue): pages). The six entries below are new. Each was fetched on 24 October 2026; the page fetched, each field and its source, and the sentence of the manuscript that characterizes the paper, with the passage that supports it, are given per entry.

A line that begins "Printed: " is the entry exactly as it is printed in docs/manuscript_jagi/manuscript_jagi.md. scripts/manuscript_check.py, run with --dir docs/manuscript_jagi, accepts the numerals and the URL of a reference entry only if the entry equals one of these lines character for character, or if every numeral in it is a value in numbers.json.

## Legg and Hutter (2007)

Pages fetched: https://api.crossref.org/works/10.1007/s11023-007-9079-x (the publisher's deposited record; the Springer page redirected to a login and was not read) and https://arxiv.org/abs/0712.3329 with its full text https://arxiv.org/pdf/0712.3329v1.

Fields: authors Shane Legg, Marcus Hutter (Crossref, arXiv); title "Universal Intelligence: A Definition of Machine Intelligence" (Crossref, arXiv); journal Minds and Machines, volume 17, issue 4, pages 391–444 (Crossref; the arXiv journal-ref field reads "Minds & Machines, 17:4 (2007) pages 391-444"); year 2007 (Crossref, issued 10 November 2007, print 30 November 2007); DOI 10.1007/s11023-007-9079-x (Crossref).

Printed: Legg, S., and Hutter, M. 2007. Universal Intelligence: A Definition of Machine Intelligence. *Minds and Machines* 17(4): 391–444. https://doi.org/10.1007/s11023-007-9079-x

Sentence (2.2): "Legg and Hutter (2007) took as their informal working definition that intelligence measures an agent's ability to achieve goals in a wide range of environments, and turned it into a formal measure for arbitrary machines."
Passage (arXiv full text, Section 2.6): "Intelligence measures an agent's ability to achieve goals in a wide range of environments. We take this to be our informal working definition of intelligence." Abstract: "These are then mathematically formalised to produce a general measure of intelligence for arbitrary machines."
Verdict: SUPPORTED. The passage is read from the arXiv version, whose journal-ref names the journal article.

Sentence (1): "One widely cited definition takes intelligence to be an agent's ability to achieve goals in a wide range of environments (Legg and Hutter, 2007)."
Passage: as above.
Verdict: SUPPORTED for the definition. "Widely cited" is the author's characterization and is not drawn from the paper.

Sentence (6.1): "Legg and Hutter (2007) define intelligence over a range of environments, so a claim that an instrument describes environments in general is a claim about a range too, and it has to be tested on each part of the range it names."
Passage: as above.
Verdict: SUPPORTED for the first clause; the rest is the author's argument.

## Hernández-Orallo (2017)

Page fetched: https://api.crossref.org/works/10.1017/9781316594179 (the record deposited by Cambridge University Press, with the publisher's description of the book). The Cambridge Core book page returned HTTP 500 and was not read.

Fields: author José Hernández-Orallo (Crossref); title "The Measure of All Minds", subtitle "Evaluating Natural and Artificial Intelligence" (Crossref); publisher Cambridge University Press (Crossref); type monograph, edition 1 (Crossref); year 2017 (Crossref, issued 19 January 2017, print 31 January 2017); ISBN 9781107153011 (print), 9781316594179 (online) (Crossref); DOI 10.1017/9781316594179 (Crossref). No place of publication is given in the record, and none is printed.

Printed: Hernández-Orallo, J. 2017. *The Measure of All Minds: Evaluating Natural and Artificial Intelligence*. Cambridge University Press. https://doi.org/10.1017/9781316594179

Sentence (2.2): "Hernández-Orallo (2017) argues for a universal evaluation of cognition, in which living organisms are a special case, and uses algorithmic information theory as the foundation for questions such as whether the difficulty of a task can be derived from the task itself."
Passage (publisher's description, Crossref abstract field): "offers a vision of the universal evaluation of cognition. By replacing the dominant anthropocentric stance with a universal perspective where living organisms are considered as a special case, long-standing questions in the evaluation of behavior can be addressed in a wider landscape. Can we derive task difficulty intrinsically? ... Using algorithmic information theory as a foundation, the book elaborates on the evaluation of perceptual, developmental, social, verbal and collective features".
Verdict: SUPPORTED, from the publisher's description only; the book itself was not read for this check.

Sentence (6.1): "Hernández-Orallo (2017) asks for evaluation that does not take the measuring instrument's validity for granted when the population changes;"
Status: WITHDRAWN before printing. The publisher's description does not state this, so the sentence is not in the manuscript.

## Chollet (2019)

Page fetched: https://arxiv.org/abs/1911.01547 (arXiv API record, version 2).

Fields: author François Chollet; title "On the Measure of Intelligence"; first version 5 November 2019; no journal-ref and no DOI on arXiv; arXiv identifier 1911.01547.

Printed: Chollet, F. 2019. On the Measure of Intelligence. Preprint, arXiv. https://arxiv.org/abs/1911.01547

Sentence (2.2): "Chollet (2019) argues that skill at any given task falls short of measuring intelligence, because unlimited priors or training data can buy arbitrary levels of skill, defines intelligence as skill-acquisition efficiency, and presents the Abstraction and Reasoning Corpus (ARC), a benchmark built on an explicit set of priors designed to be close to innate human priors."
Passage (abstract): "We argue that solely measuring skill at any given task falls short of measuring intelligence, because skill is heavily modulated by prior knowledge and experience: unlimited priors or unlimited training data allow experimenters to "buy" arbitrary levels of skills for a system ... describing intelligence as skill-acquisition efficiency ... Finally, we present a benchmark closely following these guidelines, the Abstraction and Reasoning Corpus (ARC), built upon an explicit set of priors designed to be as close as possible to innate human priors."
Verdict: SUPPORTED.

Sentence (6.1): "Chollet (2019) asks that a benchmark of general intelligence control for priors and experience;"
Passage: "we propose a set of guidelines for what a general AI benchmark should look like" together with the passage above on priors and experience.
Verdict: SUPPORTED as a paraphrase of the guidelines' stated concern with priors and experience.

## Perez-Liebana et al. (2016)

Pages fetched: https://api.crossref.org/works/10.1109/TCIAIG.2015.2402393 (publisher's deposited record) for the fields; https://api.openalex.org/works/doi:10.1109/TCIAIG.2015.2402393 for the abstract text, because the IEEE Xplore page (https://ieeexplore.ieee.org/document/7038214) returned no content to the fetch and the University of Essex repository copy (https://repository.essex.ac.uk/14619/) refused the connection. The Semantic Scholar record agrees with Crossref on venue, volume and pages and says the publisher withholds the abstract.

Fields: authors Diego Perez-Liebana, Spyridon Samothrakis, Julian Togelius, Tom Schaul, Simon M. Lucas, Adrien Couetoux, Jerry Lee, Chong-U Lim, Tommy Thompson (Crossref, in this order; Crossref writes the first author without accents, as the existing entry Gaina et al. 2018 does); title "The 2014 General Video Game Playing Competition"; journal IEEE Transactions on Computational Intelligence and AI in Games, volume 8, issue 3, pages 229–243; year 2016 (issue of September 2016); DOI 10.1109/TCIAIG.2015.2402393.

Printed: Perez-Liebana, D.; Samothrakis, S.; Togelius, J.; Schaul, T.; Lucas, S. M.; Couetoux, A.; Lee, J.; Lim, C.-U.; and Thompson, T. 2016. The 2014 General Video Game Playing Competition. *IEEE Transactions on Computational Intelligence and AI in Games* 8(3): 229–243. https://doi.org/10.1109/TCIAIG.2015.2402393

Sentence (1): "The first General Video Game Playing Competition asked for a single agent that can play many different games, some of them unknown to the entrants when they submitted, and left it to the agents to discover the mechanics of each game (Perez-Liebana et al., 2016)."
Passage (abstract): "The competition proposes the challenge of creating controllers for general video game play, where a single agent must be able to play many different games, some of them unknown to the participants at the time of submitting their entries. ... It is a responsibility of the agents to discover the mechanics of each game, the requirements to obtain a high score and the requisites to finally achieve victory."
Verdict: SUPPORTED, from the abstract as indexed by OpenAlex; the publisher's page could not be read.

Sentence (2.1): "Its organizers presented the competition as an approximation of general artificial intelligence, because the amount of game-dependent heuristics had to be severely limited (Perez-Liebana et al., 2016)."
Passage (abstract): "This test can be seen as an approximation of general artificial intelligence, as the amount of game-dependent heuristics needs to be severely limited."
Verdict: SUPPORTED, same source.

## Perez-Liebana et al. (2019)

Pages fetched: https://api.crossref.org/works/10.1109/TG.2019.2901021 (publisher's deposited record) and https://arxiv.org/abs/1802.10363 (arXiv API record, version 4, comment "accepted by IEEE ToG").

Fields: authors Diego Perez-Liebana, Jialin Liu, Ahmed Khalifa, Raluca D. Gaina, Julian Togelius, Simon M. Lucas (Crossref and arXiv, same order); title as the publisher prints it, "General Video Game AI: A Multitrack Framework for Evaluating Agents, Games, and Content Generation Algorithms" (Crossref; the arXiv title differs in hyphenation and capitals); journal IEEE Transactions on Games, volume 11, issue 3, pages 195–214; year 2019 (issue of September 2019); DOI 10.1109/TG.2019.2901021.

Printed: Perez-Liebana, D.; Liu, J.; Khalifa, A.; Gaina, R. D.; Togelius, J.; and Lucas, S. M. 2019. General Video Game AI: A Multitrack Framework for Evaluating Agents, Games, and Content Generation Algorithms. *IEEE Transactions on Games* 11(3): 195–214. https://doi.org/10.1109/TG.2019.2901021

Sentence (2.1): "Five years after the framework was released, Perez-Liebana et al. (2019) describe it as games written in the Video Game Description Language and a set of tracks in which agents play unknown games with or without access to a simulation of the game, or design new levels or rules."
Passage (arXiv abstract): "This survey paper presents the VGDL, the GVGAI framework, existing tracks, and reviews the wide use of GVGAI framework in research, education and competitions five years after its birth." and "The agents are required either to play multiple unknown games with or without access to game simulations, or to design new game levels or rules." and "potentially infinity of games created using Video Game Description Language (VGDL)".
Verdict: SUPPORTED, from the arXiv abstract of the accepted version.

## Genesereth, Love and Pell (2005)

Pages fetched: https://ojs.aaai.org/index.php/aimagazine/article/view/1813 (the AI Magazine article page: authors, abstract, DOI, publication date 15 June 2005, and the page's own citation "AI Magazine, 26(2), 62"). The article PDF and the publisher's citation exports returned an anti-bot page or an empty reply, and the DOI is not registered with Crossref in a form the Crossref API returns ("Resource not found"). The end page 72 is taken from the Semantic Scholar record (https://api.semanticscholar.org/graph/v1/paper/DOI:10.1609/aimag.v26i2.1813, "pages": "62-72"), which also gives the DBLP key journals/aim/GeneserethLP05.

Fields: authors Michael Genesereth, Nathaniel Love, Barney Pell (publisher page); title "General Game Playing: Overview of the AAAI Competition" (publisher page); journal AI Magazine, volume 26, issue 2 (publisher page); first page 62 (publisher page); last page 72 (Semantic Scholar only: NOT VERIFIED against the publisher); year 2005 (publisher page); DOI 10.1609/aimag.v26i2.1813 (publisher page).

Printed: Genesereth, M.; Love, N.; and Pell, B. 2005. General Game Playing: Overview of the AAAI Competition. *AI Magazine* 26(2): 62–72. https://doi.org/10.1609/aimag.v26i2.1813

Sentence (2.1): "Genesereth et al. (2005) define a general game playing system as one that can accept a formal description of a game and play it effectively without human intervention, and contrast it with specialized players that rely on algorithms designed in advance for specific games."
Passage (abstract, publisher page): "A general game playing system is one that can accept a formal description of a game and play the game effectively without human intervention. Unlike specialized game players, such as Deep Blue, general game players do not rely on algorithms designed in advance for specific games".
Verdict: SUPPORTED.

## Summary

Six entries added, 24 in all. Every field of five entries was confirmed against the publisher's deposited record or page, or arXiv. One field is not: the last page of Genesereth et al. (2005), which comes from Semantic Scholar only; RKM to confirm it from the printed article. Two characterizations rest on secondary text: Perez-Liebana et al. (2016), whose abstract was read from OpenAlex because the IEEE page could not be read, and Hernández-Orallo (2017), characterized from the publisher's description, not from the book. One drafted sentence (Hernández-Orallo, Section 6.1) was withdrawn before printing because no fetched text supports it.
