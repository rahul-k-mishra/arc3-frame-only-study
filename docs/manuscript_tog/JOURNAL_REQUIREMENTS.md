# IEEE Transactions on Games: requirements for this submission

All pages fetched on 2 November 2026. Quotations are from the page named on the same line. Where an item could not be fetched, the entry says so and says what is assumed instead.

Pages used:

- [G] https://www.transactions.games/submit/submission-guidelines (journal's own author guidelines)
- [O] https://www.transactions.games/submit/open-access (journal's open-access and posting page)
- [H] https://www.transactions.games/ (journal home: scope, Editor-in-Chief)
- [R] https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/resolution-and-size/
- [S] https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/prepare-supplementary-materials/
- [P] https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/
- [C] https://journals.ieeeauthorcenter.ieee.org/your-role-in-article-production/about-potential-article-processing-charges/
- [A] https://open.ieee.org/for-authors/article-processing-charges/
- [Y] https://open.ieee.org/publishing-options/hybrid-journals/
- [L] 2023 IEEE Publications Article Processing Charge (APC) List, PDF dated 12 April 2023, copy at https://www.tugraz.at/fileadmin/user_upload/tugrazExternal/b8089536-95ce-4fe0-b89d-18b5d761f5ea/Beilagen/IEEE-Article-Processing-Charges-List.pdf
- [T] https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/authoring-tools-and-templates/tools-for-ieee-authors/ieee-article-templates/

## 1. Article types and the one that fits

[G] lists five types: "Full papers (10-14 pages – fees apply for pages over 10)", "Letters (4 pages)", "Survey papers (15-20 pages - fees apply for pages over 15)", "Short papers (6-8 pages - fees apply for pages over 6)", and immersive papers. Under "Contributions" [G] also says the journal "explicitly welcomes" four kinds of paper, among them "Negative & Null Results Papers: Methodologically sound studies whose findings diverge from expected or previously published outcomes, contributing to transparency and cumulative knowledge." These are content categories, not separate length classes.

Fit: Full paper, in the Negative and Null Results category. A short paper is defined in [G] as one reporting "new theories and/or developments/results/simulations/experiments on previously published work", which this is not, and 6 pages cannot hold the registered results with the deviations subsection.

## 2. Length and overlength charge

[G]: "Full papers are limited to 10 pages in the journal's two column format, which will include all references and author biographies (note, author biographies are optional), but excluding supplementary material. Papers exceeding this length will be subject to a mandatory over-length page charge."

[G], Style: "Papers longer than 12 pages in the IEEE Transactions format will be considered only if the author can justify this length in the covering letter."

Target: at most 10 pages, references included, supplement excluded.

## 3. Fees found

- Voluntary page charge [G]: "a voluntary charge of $110 per printed page ... Page charges for this TRANSACTIONS ... are not obligatory, nor is their payment a prerequisite for publication." Avoidable.
- Mandatory overlength charge [G]: "If the voluntary page charge is not honoured, the IEEE will impose a mandatory over-length page charge of $200 USD per page for each page in excess of 10 pages for full papers". Avoidable by staying at 10 pages or fewer.
- Color in print [C]: online color is free; printing in color costs "$275 USD per color graphic". Assumed avoidable by declining color print. This is decided at the proof stage; not fetched from a ToG page.
- Open access APC: [A] "For hybrid journals, the open access article processing charge will be $2,800 USD" (2026), $2,995 for 2027. [Y]: a hybrid journal "permits both traditional subscription-based content as well as open access content", and "the review process is the same whether publishing an OA or traditional article". ToG's own pages [G], [O] name no APC. ToG's model is taken from [L], row "Games, IEEE Trans. TG Hybrid $2,345 $200 10 6 4 15 20" (2023 list). No current (2026) list naming ToG could be fetched: IEEE's hybrid title list is behind a Cloudflare check that blocked the fetch. Assumed: ToG is still hybrid, so open access is optional and publication under the standard IEEE copyright form carries no APC.

No charge was found that cannot be avoided. Open access is optional on the evidence above, with the caveat that the current hybrid list was not fetched.

## 4. Review model: double-anonymous

[G], Important Notice: "Starting January 1st, 2025, the reviewing process for IEEE Transactions on Games will adopt a double-anonymous format. This means that any manuscript submitted on or after January 1st, 2025 must be fully anonymized." "Author names, affiliations, biographies and even acknowledgments of funding must not appear in the manuscript." "Any other content that could reveal the authors' identities or affiliations must be removed prior to submission." "To ensure anonymity for data repositories and software submitted for review, please submit them through http://anonymous.4open.science/." For extensions of earlier work: "authors are asked to make sure anonymity is still maintained."

Consequence for this manuscript: the author block, the funding and conflicts statements as written, the GitHub URL, the OSF URLs and the Zenodo DOIs all identify the author. See Section 12.

## 5. Format and template

[G]: "TOG follows the standard format IEEE Transactions." "The preferred programs are TeX, LaTeX, and Microsoft Word." "please ensure your uploaded file prints without error on both 8.5×11 inch and A4 paper." "A list of 2-5 keywords are required for all manuscripts."

[T] gives no direct download links; it sends authors to the IEEE Template Selector (https://template-selector.ieee.org/), which refused the fetch (HTTP 418). The LaTeX bundle was downloaded from the Author Center's upload directory instead (see BUILD.md and the report).

Abstract [G]: "The abstract must be self-contained, without abbreviations, footnotes, or references." "The abstract must be between 150-200 words." "The abstract must be written as one paragraph, and should not contain displayed mathematical equations or tabular material." "The abstract should include three or four different keywords or phrases".

## 6. Reference style

[G]: "Put references on a separate page and provide them in IEEE style." This is a production instruction for final files; at review the IEEEtran layout with numbered references in IEEE style is used. IEEE style: numbered in order of first citation, in square brackets.

## 7. Figures

[R]: "IEEE standards for non-vector graphics for color and grayscale images are >300dpi." "IEEE standards for black and white line art are >600dpi." Vector formats (PS, EPS, PDF) are preferred. "One column width: 3.5 inches, 88.9 millimeters, or 21 picas"; "Two columns width: 7.16 inches, 182 millimeters, or 43 picas".

[G]: "Do not include captions on the illustrations themselves." "Figure captions should be sufficiently clear so that the figures can be understood without detailed reference to the accompanying text. Axes of graphs should have self-explanatory labels, not just symbols". "All line drawings and photos should be in black and white, unles specifically requested." "Letters should be large enough to be readily legible when the drawing is reduced to two or one-column width". For final files: "Figures, tables, and author photos may be submitted in .tiff, .eps, or .ps formats."

Consequence: figures redrawn at one-column (88.9 mm) or two-column (182 mm) width, 600 dpi, grayscale-safe, no title or caption inside the image.

## 8. Supplementary material

[G]: page limits exclude supplementary material; no further ToG rule. [S]: text supplements may be "TXT, DOC, DOCX, or PDF"; each file is labelled supplementary and uploaded as a separate file during submission. Nothing in [G] or [S] asks for the supplement to be merged with the paper. Plan: the supplement is a separate PDF, uploaded as supplementary material. It must be anonymized like the paper.

## 9. Graphical abstract and highlights

Not mentioned in [G]. [S] describes graphical abstracts as an option ("must undergo peer review along with the rest of your article" if supplied). Assumed: neither is required; none is supplied.

## 10. Portal and what it asks for

[G]: submission through Manuscript Central, https://mc.manuscriptcentral.com/tg-ieee. "All submissions should be accompanied by a covering letter or note indicating the type of the submission (letter, short paper, full paper or survey) and whether it is a candidate for a special issue." "Ensure that in 'Comments to Editor-in-Chief' you state that the work being submitted has not been published elsewhere, nor is it under review currently by another publication." [G] also mentions "a new data question ... that allows authors to select GitHub, Dryad, or Other". The portal itself was not opened (it needs an account), so its full list of fields is not recorded here.

## 11. Preprints, prior submissions, disclosures

- Preprints [O]: "Prior to submission to an IEEE publication: authors may post their article anywhere, including on preprint servers such as TechRxiv.org or arXiv.org. Posting on a preprint server does not count as prior publication". Upon acceptance [O]: "any previously posted versions on the author's personal website, the author's employer's website, TechRxiv.org, arXiv.org, or the funder's repository* must be replaced with the accepted version." "The posted article must be removed completely from any other third-party servers." Zenodo is not one of the named servers; a published Zenodo record under CC-BY 4.0 cannot be withdrawn by its author. This is a conflict to put to the Editor-in-Chief, not one the manuscript can solve.
- Prior and concurrent submissions [P]: authors must disclose "all prior publication(s) and current submissions when submitting an article"; [G]: work "not published or under review elsewhere".
- Disclosure of tool use [P], heading "Guidelines for Artificial Intelligence (AI)-Generated Content": use of such content "shall be disclosed in the acknowledgments section of any article submitted to an IEEE publication", naming the system and the sections; use "for editing and grammar enhancement ... is generally outside the intent of the above policy", disclosure there being recommended, not required. This conflicts with rule R2 of the prompt. It is the author's decision, recorded in Section 12.

## 12. Conflicts between the journal's rules and the task as written

1. Double-anonymous review (Section 4) against R1 (named author block, funding and conflicts statements) and against step 3 (keep the preprint sentence with both Zenodo DOIs and the data and code section with the GitHub and OSF URLs). All of these identify the author.
2. IEEE's disclosure policy (Section 11) against R2.
3. IEEE's posting policy upon acceptance (Section 11) against a Zenodo preprint that cannot be removed.

RKM decided on 2 November 2026:

1. The review version is anonymized. It has no author block. Repository and registration addresses, commit hashes and the two Zenodo identifiers are withheld in the manuscript and the supplement and given in the cover letter. The data section points to an anonymized copy on anonymous.4open.science, which RKM creates. The funding and conflicts statements stay, as statements of none, without names.
2. Rule R2 is kept as written.
3. The cover letter does not raise the posting policy for the Zenodo preprint. It gives no decline date for the JAGI submission.

The Editor-in-Chief named on [H] is Magy Seif El-Nasr.
