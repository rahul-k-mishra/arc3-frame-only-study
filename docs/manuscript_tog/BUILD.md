# Building the IEEE Transactions on Games version

Every command below runs in PowerShell, in order, from the working directory each block names. Nothing here plays a game or reads runs/suites.

Route: LaTeX. A MiKTeX distribution (MiKTeX 26.5, pdfTeX 4.27) is installed on the machine, and its IEEEtran package is the same class (IEEEtran.cls V1.8b, 2015/08/26) as IEEE's LaTeX bundle. IEEE's bundle was downloaded on 2 November 2026 from https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE-Transactions-LaTeX2e-templates-and-instructions.zip into D:\Research\arc3\ieee_template, outside the repository. docs/manuscript_tog/tog_template.tex is a pandoc template after bare_jrnl.tex of that bundle. docs/manuscript_tog/tog.lua turns the Markdown into IEEE form:

- the Abstract section becomes the abstract;
- the "Index Terms" line becomes IEEEkeywords;
- the numbered reference list becomes thebibliography;
- figures and tables become full-width floats, with table captions above the table.

pdflatex is run with --disable-installer, so no package is installed during a build.

Sources: manuscript_tog.md, supplement_tog.md and cover_letter_tog.md are the edited sources. The references in manuscript_tog.md are numbered in order of first citation; check (c) verifies that order.

## Step 1. numbers.json and the provenance table (ARC venv)

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_numbers.py --out docs/manuscript_tog --anonymous
```

Expected:

- one "check ok:" line per cross-check;
- "numbers.json: 1113 values written to docs/manuscript_tog/numbers.json";
- "appendix_c.md: 9 number classes written to docs/manuscript_tog/appendix_c.md (anonymous: no commits)";
- "all cross-checks passed".

docs\manuscript is not touched. With --anonymous the provenance table names files without commits, so a later STATE.md amendment does not make it stale, and it describes the three source files kept in the directories of earlier versions of the article instead of naming their paths.

## Step 2. The four figures

The figures are drawn at IEEE's two-column width, 182 mm, at 600 dpi.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_figures.py --tog
```

Expected: four blocks "fig<k>.png from <source>", each listing every number drawn and identical to the blocks printed without --tog, then "4 figures written to docs/manuscript_tog".

## Step 3. Checks: the paper, the supplement, the cover letter

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_check.py --dir docs\manuscript_tog --ieee manuscript_tog.md
echo "exit code: $LASTEXITCODE"
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_check.py --dir docs\manuscript_tog --ieee supplement_tog.md
echo "exit code: $LASTEXITCODE"
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_check.py --dir docs\manuscript_tog --ieee cover_letter_tog.md
echo "exit code: $LASTEXITCODE"
```

Expected for each file: blocks (a) to (g), each ending "0 issues", then "RESULT: PASS" and "exit code: 0".

- For the paper, the abstract must be within 150 to 200 words (the journal's limit). It is 196.
- For the supplement, (g) finds appendix_c.md in Section S.5.

Do not build or commit unless all three exit codes are 0.

## Step 4. LaTeX sources with pandoc

```powershell
cd D:\Research\arc3\repo\docs\manuscript_tog
$pd = "C:\Users\Shivani Mishra\AppData\Local\Pandoc\pandoc.exe"
& $pd -f markdown+autolink_bare_uris manuscript_tog.md -t latex -s --template=tog_template.tex --lua-filter=tog.lua --shift-heading-level-by=-1 -M figscale=0.95 -M runninghead="Manuscript submitted to IEEE Transactions on Games" -M pdfauthor="" -o manuscript_tog.tex
& $pd -f markdown+autolink_bare_uris supplement_tog.md -t latex -s --template=tog_template.tex --lua-filter=tog.lua --shift-heading-level-by=-1 -M classoption="journal,onecolumn" -M sloppy=true -M floatpos="!htbp" -M runninghead="Supplement, manuscript submitted to IEEE Transactions on Games" -M pdfauthor="" -o supplement_tog.tex
```

Expected: no output, and the two .tex files.

In the paper the figures are set at 0.95 of the text width (figscale), which keeps it at 10 pages since Table I carries the agreement and kappa of each line; the supplement keeps the full width.

## Step 5. PDFs with pdflatex (two runs each)

```powershell
cd D:\Research\arc3\repo\docs\manuscript_tog
$tex = "C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe"
& $tex --disable-installer -interaction=nonstopmode manuscript_tog.tex | Out-Null
& $tex --disable-installer -interaction=nonstopmode manuscript_tog.tex | Out-Null
& $tex --disable-installer -interaction=nonstopmode supplement_tog.tex | Out-Null
& $tex --disable-installer -interaction=nonstopmode supplement_tog.tex | Out-Null
Select-String -Path manuscript_tog.log, supplement_tog.log -Pattern "^!"
pdfinfo manuscript_tog.pdf | Select-String "Title|Author|Creator|Producer|Pages|Page size"
pdfinfo supplement_tog.pdf | Select-String "Title|Author|Creator|Producer|Pages|Page size"
Remove-Item *.aux, *.log, *.out
```

Expected:

- no line from Select-String;
- manuscript_tog.pdf 10 pages, supplement_tog.pdf 6 pages;
- page size 612 x 792 pts (letter), which prints on A4 without loss;
- Author "Anonymous Author", Creator and Producer empty;
- CreationDate and ModDate the build day only, with no time of day and no time-zone offset, and no PTEX entries in the Info dictionary (tog_template.tex sets both).

The journal's limit for a full paper is 10 pages, references included, supplementary material excluded. At 11 pages or more a mandatory over-length charge applies (JOURNAL_REQUIREMENTS.md, Section 3).

## Step 6. Fonts, forbidden words, anonymity

```powershell
cd D:\Research\arc3\repo\docs\manuscript_tog
pdffonts manuscript_tog.pdf
pdffonts supplement_tog.pdf
foreach ($f in "manuscript_tog","supplement_tog") { pdftotext "$f.pdf" "$env:TEMP\$f.txt"; $n = (Select-String -Path "$env:TEMP\$f.txt" -Pattern 'assistant|claude|language model|\bLLMs?\b|generated|delve|leverag|robust|comprehensive|\bnovel|showcas|underscor|crucial|pivotal|landscape|tapestr|\brealms?\b|paradigm|harness|foster|holistic|seamless|cutting-edge|state of the art|it is worth noting|importantly|notably|in this work|in conclusion|furthermore|moreover|additionally').Count; $a = (Select-String -Path "$env:TEMP\$f.txt" -Pattern 'mishra|rahul|ranchi|jharkhand|0009-0004|github|osf\.io|zenodo\.2|19f2a9f|8b2b2b9|66e5606|bb0f1a1|f43526a|ccc4d57|378345f|gmail|Trial and Error|Artificial General Intelligence').Count; "$f.pdf forbidden-word hits: $n; identifying hits: $a" }
```

Expected:

- Every font is Type 1 with encoding Custom. There is no Identity-H font and no Type 3 font; the figures are PNG and embed no fonts.
- manuscript_tog.pdf: 1 forbidden-word hit, "Leveraging" in the title of Cobbe et al. in the reference list, and 0 identifying hits.
- supplement_tog.pdf: 0 forbidden-word hits and 0 identifying hits.

The word "ORCID" in Table S5 is the name of a number class, and the path docs/manuscript_jagi names a directory. Neither is matched by the pattern.

## Step 7. Page-by-page layout check

```powershell
cd D:\Research\arc3\repo\docs\manuscript_tog
pdftoppm -r 60 -png manuscript_tog.pdf "$env:TEMP\tog_page"
pdftoppm -r 60 -png supplement_tog.pdf "$env:TEMP\tog_supp"
```

Open each image and check the following:

- every figure and table is inside the margins, with its caption;
- no text runs into a margin or over another element;
- the references end on page 10;
- in the supplement, the title is on page 1 above Table S1.

## Step 8. Title page (not seen by reviewers)

title_page.md holds the identity that the anonymous manuscript withholds: the title, the author with affiliation and ORCID, the correspondence block, the acknowledgments sentence and the conflicts line. It has no repository address, DOI, registration address or commit hash. pandoc writes the docx; scripts/docx_metadata.py then sets its document properties: creator the author's name, every other field empty (no title, subject, keywords, description, last-modified-by, dates, application or template).

```powershell
cd D:\Research\arc3\repo
$pd = "C:\Users\Shivani Mishra\AppData\Local\Pandoc\pandoc.exe"
& $pd docs\manuscript_tog\title_page.md -o docs\manuscript_tog\title_page.docx
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\docx_metadata.py docs\manuscript_tog\title_page.docx --creator "Rahul Kumar Mishra"
& $pd docs\manuscript_tog\title_page.docx -t plain --wrap=none
```

Expected:

- "docs\manuscript_tog\title_page.docx: creator "Rahul Kumar Mishra", every other property empty";
- "docProps/core.xml: dc:title = ""; dc:subject = ""; dc:creator = "Rahul Kumar Mishra"; cp:keywords = ""; dc:description = ""; cp:lastModifiedBy = """;
- "docProps/app.xml: Properties = """ and "docProps/custom.xml: Properties = """;
- the text of the title page, in the order above.

## Before submission (author)

- Upload manuscript_tog.pdf as the main document, title_page.docx as the title page (not for review), supplement_tog.pdf as supplementary material, and the cover letter text as the covering letter and in "Comments to Editor-in-Chief".
