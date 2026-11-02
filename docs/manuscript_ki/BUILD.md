# Building the KI manuscript, its supplement and the submission files

Every command runs in PowerShell, in this order, from D:\Research\arc3\repo unless a step says otherwise. Nothing here plays a game or reads runs/suites. Tools: the ARC venv python (D:\Research\arc3\brutus\.venv), pandoc (C:\Users\Shivani Mishra\AppData\Local\Pandoc\pandoc.exe), MiKTeX (pdflatex and bibtex on the PATH) and the xpdf tools (pdfinfo, pdffonts, pdftotext, pdftoppm on the PATH). The Springer class files svjour3.cls, svglov3.clo and spmpsci.bst are copied unchanged into docs\manuscript_ki from the author's download, D:\Research\arc3\ki_template\LaTeX_DL_468198_240419, because the journal asks for the source with all style files.

Step 1. Write numbers.json and appendix_c.md (ARC venv). The script writes into docs\manuscript; the copy below moves its output here and the restore puts docs\manuscript back as committed.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_numbers.py --state-ref "as of amendment (x)"
Copy-Item docs\manuscript\numbers.json, docs\manuscript\appendix_c.md docs\manuscript_ki\
git restore docs\manuscript\numbers.json docs\manuscript\appendix_c.md
git status --short docs\manuscript
```

Expected: one "check ok:" line per cross-check, then "numbers.json: 1128 values written to docs/manuscript/numbers.json", "appendix_c.md: 9 number classes written to docs/manuscript/appendix_c.md", "docs/STATE.md named as: as of amendment (x)", "all cross-checks passed"; no output from git status. With --state-ref, Table S5 names docs/STATE.md by that text, so a later STATE.md amendment does not make it stale. If Table S5 of supplement_ki.md no longer equals appendix_c.md, step 4 reports it under (g); copy appendix_c.md into Section S.5 unchanged.

Step 2. Draw the four figures for the journal (vector PDF for the build, EPS for upload, 174 mm wide, 8 pt Arial), one worker per figure.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_figures.py --ki
```

Expected: four blocks "Fig<k> from <source>", each listing every number drawn (the same lines as the default build), then "4 figures written to docs/manuscript_ki".

Step 3. Set the paper in the journal's class: pandoc writes manuscript_ki.tex from manuscript_ki.md through ki_template.tex and ki.lua; pdflatex, bibtex and two more pdflatex runs write manuscript_ki.pdf and manuscript_ki.bbl.

```powershell
cd D:\Research\arc3\repo\docs\manuscript_ki
$pd = "C:\Users\Shivani Mishra\AppData\Local\Pandoc\pandoc.exe"
& $pd -f markdown+autolink_bare_uris manuscript_ki.md -t latex --template=ki_template.tex --lua-filter=ki.lua --shift-heading-level-by=-1 --natbib -o manuscript_ki.tex
pdflatex -interaction=nonstopmode -halt-on-error manuscript_ki.tex | Out-Null
bibtex manuscript_ki
pdflatex -interaction=nonstopmode -halt-on-error manuscript_ki.tex | Out-Null
pdflatex -interaction=nonstopmode -halt-on-error manuscript_ki.tex | Out-Null
echo "pdflatex exit code: $LASTEXITCODE"
Select-String -Path manuscript_ki.log -Pattern "^!|Overfull|undefined" | Measure-Object | Select-Object -ExpandProperty Count
pdfinfo manuscript_ki.pdf | Select-String "Title|Author|Creator|Producer|Pages|Page size"
cd D:\Research\arc3\repo
```

Expected: bibtex reads spmpsci.bst and references_ki.bib with no warning; "pdflatex exit code: 0"; the count 0 (no error, no overfull line, no undefined reference); Title the article's title, Author "Rahul Kumar Mishra", Creator and Producer empty, 16 pages, A4.

Step 4. Check the paper, the supplement and the cover letter against numbers.json. The paper is checked in its pandoc source; the option --bib reads its citation keys, references_ki.bib and the manuscript_ki.bbl of step 3.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_check.py --dir docs\manuscript_ki --bib references_ki.bib manuscript_ki.md
echo "exit code: $LASTEXITCODE"
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_check.py --dir docs\manuscript_ki supplement_ki.md
echo "exit code: $LASTEXITCODE"
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_check.py --dir docs\manuscript_ki cover_letter_ki.md
echo "exit code: $LASTEXITCODE"
```

Expected, three times: blocks (a) to (g), each ending "0 issues", "RESULT: PASS" and "exit code: 0". For the paper also "bibliography: 24 entries in references_ki.bib, 24 entries in manuscript_ki.bbl", "verified reference entries read from REFERENCES_CHECK*.md: 24", "(c) citations: 24 cited works, 24 reference entries", the abstract within 150 to 250 words and the main-text word count. Do not commit unless all three exit codes are 0.

Step 5. Build the supplement, Online Resource 1, as ESM_1.pdf (the journal's file name for electronic supplementary material).

```powershell
cd D:\Research\arc3\repo\docs\manuscript_ki
$pd = "C:\Users\Shivani Mishra\AppData\Local\Pandoc\pandoc.exe"
& $pd -f markdown+autolink_bare_uris supplement_ki.md -o ESM_1.pdf --pdf-engine=pdflatex --lua-filter=ki.lua -H supplement_header.tex -V papersize=a4 -V geometry:margin=22mm -V fontsize=10pt -V fontfamily=mathptmx -V colorlinks=false --shift-heading-level-by=-1 -M pdftitle="Online Resource 1"
pdfinfo ESM_1.pdf | Select-String "Title|Author|Pages|Page size"
cd D:\Research\arc3\repo
```

Expected: no output from pandoc; Title "Online Resource 1", Author "Rahul Kumar Mishra", 7 pages, A4.

Step 6. Metadata, fonts and forbidden words in the built files.

```powershell
cd D:\Research\arc3\repo\docs\manuscript_ki
pdffonts manuscript_ki.pdf
pdffonts ESM_1.pdf
$pat = 'assistant|claude|language model|\bLLMs?\b|generated|delve|leverag|robust|comprehensive|\bnovel|showcas|underscor|crucial|pivotal|landscape|tapestr|\brealms?\b|paradigm|harness|foster|holistic|seamless|cutting-edge|state of the art|it is worth noting|importantly|notably|in this work|in conclusion|furthermore|moreover|additionally'
foreach ($f in "manuscript_ki","ESM_1") { pdftotext -enc UTF-8 "$f.pdf" "$env:TEMP\$f.txt"; $hits = Select-String -Path "$env:TEMP\$f.txt" -Pattern $pat -AllMatches | ForEach-Object { $_.Matches.Value }; "$f.pdf forbidden-word hits: $(@($hits).Count) $($hits -join ', ')" }
foreach ($f in "manuscript_ki.tex","cover_letter_ki.md","supplement_ki.md") { "$f forbidden-word hits: $((Select-String -Path $f -Pattern $pat -AllMatches | Measure-Object).Count)" }
foreach ($f in "manuscript_ki.pdf","ESM_1.pdf","Fig1.pdf","Fig2.pdf","Fig3.pdf","Fig4.pdf") { "== $f"; pdfinfo $f | Select-String "^(Title|Subject|Keywords|Author|Creator|Producer):" }
cd D:\Research\arc3\repo
```

Expected: every font embedded ("emb yes"), and no Type 3 (bitmap) font: the text in Times (NimbusRomNo9L, Type 1), typewriter text in Courier (NimbusMonL, Type 1), math symbols in CMSY and CMMI (Type 1), and the figure lettering in Arial (TrueType, embedded). One forbidden-word hit in manuscript_ki.pdf, "Leverag" from "Leveraging" in the title of Cobbe et al. (2020) in the reference list, which the rules allow (a cited title); 0 in ESM_1.pdf and in the three sources. Metadata: the paper's Title and Author only (Creator and Producer empty); ESM_1.pdf Title "Online Resource 1", Author "Rahul Kumar Mishra", Creator "LaTeX via pandoc", Producer the pdfTeX version; the figures name Matplotlib as creator, which is the graphics program the journal asks authors to state.

Step 7. Page-by-page layout check of both PDFs.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe -I docs\manuscript_ki\layout_check.py docs\manuscript_ki\manuscript_ki.pdf docs\manuscript_ki\manuscript_ki.log
D:\Research\arc3\brutus\.venv\Scripts\python.exe -I docs\manuscript_ki\layout_check.py docs\manuscript_ki\ESM_1.pdf
```

Expected: one line per page with its ink extent, "pages with ink in the side margins: 0", "overfull lines in the log: 0" for the paper, and "LAYOUT: PASS" twice. Then open both PDFs and look at every page: each figure and table on or after the page of its first mention, no caption separated from its float, the reference list complete.

Step 8. Remove the LaTeX intermediate files (they are not committed).

```powershell
cd D:\Research\arc3\repo\docs\manuscript_ki
Remove-Item manuscript_ki.aux, manuscript_ki.log, manuscript_ki.out, manuscript_ki.blg -ErrorAction SilentlyContinue
cd D:\Research\arc3\repo
```

## What is uploaded to Editorial Manager (https://www.editorialmanager.com/kuin)

The journal asks for "the original source (including all style files and figures) and a PDF version of the compiled output".

- Manuscript source: manuscript_ki.tex, manuscript_ki.bbl, references_ki.bib, svjour3.cls, svglov3.clo, spmpsci.bst.
- Figures: Fig1.eps, Fig2.eps, Fig3.eps, Fig4.eps (the build uses the PDF copies of the same drawings; the graphics program is Matplotlib).
- Compiled manuscript: manuscript_ki.pdf.
- Electronic supplementary material: ESM_1.pdf (Online Resource 1).
- Cover letter: the text of cover_letter_ki.md, once the date of the JAGI decision is put in place of its placeholder.

manuscript_ki.md, ki_template.tex, ki.lua, supplement_ki.md, supplement_header.tex, layout_check.py, numbers.json, appendix_c.md and the two REFERENCES_CHECK files are the repository's record of how the files were made; they are not uploaded.
