# KI - Künstliche Intelligenz (Springer, journal 13218): requirements for this submission

Every page below was fetched on 2 November 2026 with curl (a plain browser request; the Springer pages redirect a script fetch through a cookie check). Quotations are copied from the page named on the same line. Where an item could not be fetched, the entry says so and says what is assumed.

Pages:

- [SG] https://link.springer.com/journal/13218/submission-guidelines (Instructions for Authors)
- [ED] https://link.springer.com/journal/13218/ethics-and-disclosures
- [HP] https://link.springer.com/journal/13218/how-to-publish-with-us (publishing options, fees, licenses)
- [AS] https://link.springer.com/journal/13218/aims-and-scope
- [JP] https://link.springer.com/brands/springer/journal-policies (Springer journal policies; the address https://www.springer.com/gp/editorial-policies/preprint-sharing redirects to its section "Preprint sharing")
- Not reachable: https://www.kuenstliche-intelligenz.de/ (and the http and bare-domain forms): no connection within 30 s on each of three attempts. https://link.springer.com/journal/13218/editorial-policies, fees-and-funding and pre-submission-checklist returned Springer's "Page not found". Assumed: the Springer pages above are the journal's instructions; nothing from the society's site is used.

## 1. Article types, and the one that fits

[SG], "Types of Papers", lists: Technical Contribution; Systems Description; Project Reports; Dissertation and Habilitation Abstracts; AI Transfer; Discussion; News; Interviews. None is a dedicated negative-results or registered-report type.

[SG], Technical Contribution: "Submissions should be interesting to the general AI audience. Special terms should be introduced and explained in the context in which they are used. Articles must be original and should not have been submitted or published elsewhere. All submitted contributions will be reviewed by at least two technical experts. A typical contribution has up to 20 printed pages in the KI journal (including graphics and references). It must be written in English and can be submitted at any time."

Fit: Technical Contribution. A preregistered empirical study with a negative result is a research article; the other types are for systems, funded projects, theses, products, opinion, news and interviews. "Discussion" asks for "scientifically argued personal opinions", which this is not. The sentence "should not have been submitted ... elsewhere" is read with [SG], "Manuscript Submission" ("that it is not under consideration for publication anywhere else") and [JP] on preprints (item 9): the manuscript is not under consideration elsewhere, and the two earlier submissions were declined without review (docs/STATE.md amendments (u) and (x); the JAGI decision is not yet recorded in STATE.md).

## 2. Length

[SG], Technical Contribution: "A typical contribution has up to 20 printed pages in the KI journal (including graphics and references)." This is a typical size, not a stated limit; no word limit is given. Target: at most 20 pages in the journal's two-column layout, references and figures included. Draft 1 has 16 pages.

## 3. Required structure and mandatory sections

- [SG], "Title Page": the title, "The name(s) of the author(s)", "The affiliation(s) of the author(s), i.e. institution, (department), city, (state), country", "A clear indication and an active e-mail address of the corresponding author", "If available, the 16-digit ORCID of the author(s)". "For authors that are (temporarily) unaffiliated we will only capture their city and country of residence, not their e-mail address unless specifically requested."
- [SG], "Abstract": "Please provide an abstract of 150 to 250 words. The abstract should not contain any undefined abbreviations or unspecified references."
- [SG], "Statements and Declarations": "The following statements should be included under the heading "Statements and Declarations" for inclusion in the published paper. Please note that submissions that do not include relevant declarations will be returned as incomplete." Competing interests are required; "funding information ... should be included in the 'Declarations' section"; "Other declarations include Ethics approval, Consent, Data, Material and/or Code availability and Authors' contribution statements." No-funding and no-interest wordings are given as examples.
- [SG], "Headings": "Please use the decimal system of headings with no more than three levels."
- [SG], "Abbreviations": "Abbreviations should be defined at first mention and used consistently thereafter."
- [SG], "Footnotes": footnotes, not endnotes; never a footnote that is only a citation.
- [SG], "Acknowledgments": "should be placed in a separate section on the title page". None in this manuscript.
- [SG], "Source Files": "Please ensure you provide all relevant editable source files at every submission and revision. Failing to submit a complete set of editable source files will result in your article not being considered for review."
- [SG], "Text Formatting": "Manuscripts should be submitted in LaTeX. We recommend using Springer Nature's LaTeX template and choosing the formatting option "[iicol]". The submission should include the original source (including all style files and figures) and a PDF version of the compiled output. Word files are also accepted." and, under "Types of Papers": "Please use Springer's LaTeX macro package and choose the formatting option "twocolumn". (LaTeX marco package, https://media.springer.com/full/springer-instructions-for-authors-assets/zip/468198_LaTeX_DL_468198_220518.zip)". The two sentences name two different packages (the newer Springer Nature template with option iicol, and the older svjour3 macro package with option twocolumn). The author's download (item 2 of the report, D:\Research\arc3\ki_template) is the svjour3 package, the one the journal's own paragraph links; the manuscript uses it with "twocolumn".
- Keywords: [SG] does not state a number; the svjour3 template has a \keywords field. Six are given.

## 4. Reference style

[SG], "Citation": "Reference citations in the text should be identified by numbers in square brackets." "Reference list": "The list of references should only include works that are cited in the text and that have been published or accepted for publication. Personal communications and unpublished works should only be mentioned in the text." "The entries in the list should be numbered consecutively." "If available, please always include DOIs as full DOI links in your reference list (e.g. "https://doi.org/abc")." Example: "Gamelin FX, Baquet G, Berthoin S, Thevenet D, Nourry C, Nottin S, Bosquet L (2009) Effect of high intensity intermittent training on heart rate variability in prepubescent children. Eur J Appl Physiol 105:731-738. https://doi.org/10.1007/s00421-008-0955-8". "Always use the standard abbreviation of a journal's name according to the ISSN List of Title Word Abbreviations ... If you are unsure, please use the full journal title." "Authors preparing their manuscript in LaTeX can use the bibliography style file sn-basic.bst which is included in the Springer Nature Article Template."

Done: the svjour3 package's numbered style spmpsci.bst (sn-basic.bst belongs to the other template and is not in the author's download), DOIs as full links, full journal titles. The restyling is recorded in REFERENCES_CHECK_ki.md. Preprints (arXiv) are cited; [JP] allows citing preprints (item 9), and the line on "unpublished works" is read as excluding personal communications and manuscripts, not public preprints with identifiers.

## 5. Figures

[SG], "Artwork and Illustrations Guidelines" (quoted in part): "For vector graphics, the preferred format is EPS; for halftones, please use TIFF format." "Vector graphics containing fonts must have the fonts embedded in the files." "Name your figure files with "Fig" and the figure number, e.g., Fig1.eps." "All lines should be at least 0.1 mm (0.3 pt) wide." "Combination artwork should have a minimum resolution of 600 dpi." "Color art is free of charge for online publication." "If the figures will be printed in black and white, do not refer to color in the captions." "To add lettering, it is best to use Helvetica or Arial (sans serif fonts)." "Keep lettering consistently sized throughout your final-sized artwork, usually about 2-3 mm (8-12 pt)." "Do not include titles or captions within your illustrations." "Figure captions begin with the term Fig. in bold type, followed by the figure number, also in bold type." "No punctuation is to be included after the number, nor is any punctuation to be placed at the end of the caption." "For large-sized journals the figures should be 84 mm (for double-column text areas), or 174 mm (for single-column text areas) wide and not higher than 234 mm." "Figures should be submitted within the body of the text." Accessibility: "Patterns are used instead of or in addition to colors".

Done: the four figures are redrawn by scripts/manuscript_figures.py --ki as vector PDF (for the build) and EPS (for upload), named Fig1 to Fig4, 174 mm wide (the full text width, set as two-column-wide floats), all lettering 8 pt Arial, fonts embedded, grayscale with hatching, no title inside, captions without final punctuation, figures inside the text. The drawn numbers are unchanged.

## 6. Supplementary material

[SG], "Supplementary Information (SI)": accepted ("Springer accepts electronic multimedia files ... and other supplementary files to be published online along with an article"). "Text and Presentations: Submit your material in PDF format". "Please include in each file the following information: article title, journal name, author names; affiliation and e-mail address of the corresponding author." "Refer to the supplementary files as "Online Resource", e.g., "... as shown in the animation (Online Resource 3)"". "Name the files consecutively, e.g. "ESM_3.mpg", "ESM_4.pdf"." "For each supplementary material, please supply a concise caption describing the content of the file." "Supplementary Information (SI) will be published as received from the author without any conversion, editing, or reformatting."

Done: ESM_1.pdf, cited as "Online Resource 1", with the article title, journal, author, affiliation and e-mail in its first paragraph; a caption-like description is in the section "Supplementary Information" of the paper.

## 7. Peer-review model

[ED]: "Research content published in this journal is peer reviewed (single-anonymous)." [AS]: "Content published in this journal is peer reviewed." [JP], "Peer review": "Most journals use a single-anonymized peer review process; that is, author identities are known to peer reviewers, but peer reviewers identities are not revealed to the authors."

Consequence: the review is not double-anonymous. The author's name, affiliation, ORCID and e-mail, the preprint and supplement DOIs, the repository and the two OSF registrations stay in the paper, as instructed.

## 8. Use of writing aids: the journal's policy (for the author's decision before submission)

[SG], "Title Page": "Large Language Models (LLMs), such as ChatGPT, do not currently satisfy our authorship criteria. ... Use of an LLM should be properly documented in the Methods section (and if a Methods section is not available, in a suitable alternative part) of the manuscript. The use of an LLM (or other AI-tool) for "AI assisted copy editing" purposes does not need to be declared. In this context, we define the term "AI assisted copy editing" as AI-assisted improvements to human-generated texts for readability and style, and to ensure that the texts are free of errors in grammar, spelling, punctuation and tone. These AI-assisted improvements may include wording and formatting changes to the texts, but do not include generative editorial work and autonomous content creation. In all cases, there must be human accountability for the final version of the text and agreement from the authors that the edits reflect their original work."

The manuscript follows rule R2 of the author's instructions and contains no such statement. The journal requires one in the Methods section for any use beyond copy editing as it defines it. Whether a statement is needed, and its wording, is the author's decision before submission; nothing in the draft pre-empts it.

## 9. Preprint policy

[JP], "Preprint sharing": "Springer Nature journals encourage posting of preprints of primary research manuscripts on preprint servers of the authors' choice". "Posting of preprints is not considered prior publication and will not jeopardize consideration at Springer Nature journals." "Authors should disclose details of preprint posting, including DOI and licensing terms, upon submission of the manuscript". "Authors may choose any license of their choice for the preprint including Creative Commons licenses." "Once the preprint is published, it is the author's responsibility to ensure that the preprint record is updated with a publication reference".

Done: the preprint DOI and its CC-BY 4.0 license are in the paper (Data and Code Availability; second deviation) and in the cover letter. After publication the Zenodo record should be updated with the article's DOI.

## 10. Submission system

[SG], "Online Submission": "Please follow the hyperlink "Submit manuscript" and upload all of your manuscript files following the instructions given on the screen." The "Submit your manuscript" link on [SG] points to Editorial Manager, https://www.editorialmanager.com/kuin. The system itself was not opened.

## 11. Fees

- Subscription route: [HP]: "KI - Künstliche Intelligenz is a hybrid journal." "Authors can also choose to publish under the subscription publishing model (no APC charges apply); both options will be offered after the paper has been accepted." Publishing is free in the subscription track.
- Open access: optional. [HP]: "Authors who publish open access in KI - Künstliche Intelligenz are required to pay an article processing charge (APC)." "The current APC for KI - Künstliche Intelligenz is £2390.00 GBP / $3290.00 USD / €2690.00 EUR. This fee is subject to VAT or local taxes where applicable." Open access articles are under CC BY 4.0.
- Color: [SG]: "Color art is free of charge for online publication." [SG], "After acceptance": "Online publication of color illustrations is free of charge. For color in the print version, authors will be expected to make a contribution towards the extra costs." The figures are grayscale, so no color charge arises.
- No submission fee and no page charge are mentioned on any page fetched. [SG] mentions offprints, which "can be ordered", and language editing services; both are optional.

No unavoidable charge was found: in the subscription route with grayscale figures, publication costs nothing.

## 12. Other requirements met or noted

- [SG]: "Please guarantee that the quality of English in all document sources will meet the standards required by the international publishing industry." The manuscript uses American spelling throughout (rule R3).
- [SG], "Data transparency" and the research data policy: the data and code are public (Data and Code Availability). The journal's research data policy page was not fetched.
- [SG], "Ethical Responsibilities of Authors": "Concurrent or secondary publication is sometimes justifiable, provided certain conditions are met." Not applicable: the earlier versions were not published, only posted as a preprint.
- [SG], "Suggesting / excluding reviewers": optional; nothing is suggested in draft 1.
