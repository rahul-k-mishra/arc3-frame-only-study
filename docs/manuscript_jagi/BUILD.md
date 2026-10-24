# Building the JAGI manuscript and supplement

Every command runs in PowerShell from D:\Research\arc3\repo, in this order. Nothing here plays a game or reads runs/suites. The Author's Kit must be unpacked at D:\Research\arc3\jagi_kit\JAGIAuthorKit (outside the repository); it is downloaded from http://www.cis.temple.edu/~wangp/JAGIAuthorKit.zip.

Step 1. Write numbers.json and appendix_c.md (ARC venv). The script writes into docs\manuscript; step 3 copies its output here and puts docs\manuscript back as committed.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_numbers.py --state-ref "at the commit tagged jagi-submission-v1"
```

Expected: one "check ok:" line per cross-check, then "numbers.json: 1113 values written", "appendix_c.md: 9 number classes written", "docs/STATE.md named as: at the commit tagged jagi-submission-v1" and "all cross-checks passed". With --state-ref, the provenance table names docs/STATE.md by that text instead of by the commit that last changed it, so a later STATE.md amendment does not make Table S5 stale.

Step 2. Draw the four figures, one worker per figure (written into docs\manuscript).

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_figures.py
```

Expected: four blocks "fig<k>.png from <source>", each listing every number drawn, then "4 figures written to docs/manuscript".

Step 3. Copy the outputs into docs\manuscript_jagi, and restore the two files of docs\manuscript that step 1 rewrites (they name the commit that last changed docs\STATE.md, so they change whenever STATE.md does). The figures are byte-identical to the committed ones.

```powershell
cd D:\Research\arc3\repo
Copy-Item docs\manuscript\numbers.json, docs\manuscript\appendix_c.md, docs\manuscript\fig1.png, docs\manuscript\fig2.png, docs\manuscript\fig3.png, docs\manuscript\fig4.png docs\manuscript_jagi\
git restore docs\manuscript\numbers.json docs\manuscript\appendix_c.md
git status --short docs\manuscript
```

Expected: no output from the last command (docs\manuscript unchanged). If Table S5 in supplement_jagi.md no longer equals the new appendix_c.md, step 4 reports it under (g); copy appendix_c.md into Section S.5 unchanged.

Step 4. Check the paper and the supplement.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_check.py --dir docs\manuscript_jagi manuscript_jagi.md
echo "exit code: $LASTEXITCODE"
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_check.py --dir docs\manuscript_jagi supplement_jagi.md
echo "exit code: $LASTEXITCODE"
```

Expected: blocks (a) to (g), each ending "0 issues", the abstract within 150 to 250 words, "RESULT: PASS" and "exit code: 0", twice. Do not build or commit unless both exit codes are 0.

Step 5. Build the reference document from the kit's Word template (journal styles, page size and margins; sample running heads replaced; see the docstring of make_reference_doc.py). Until the day of submission, --submitted is the placeholder yyyy-mm-dd and the first-page head reads "Submitted yyyy-mm-dd"; on the day of submission, run this step with the date (for example --submitted 2026-11-02) and then steps 6 and 7. Table cells use the style Compact, which keeps with the next paragraph, so each table stays on one page with its caption.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe -I docs\manuscript_jagi\make_reference_doc.py D:\Research\arc3\jagi_kit\JAGIAuthorKit\Instruction-word.docx docs\manuscript_jagi\jagi_reference.docx --submitted yyyy-mm-dd
```

Expected: "reference document written: docs\manuscript_jagi\jagi_reference.docx (headers 3, styles added 10, numbering removed 3)".

Step 6. Build the two .docx files with pandoc. The only metadata author is the author's name.

```powershell
cd D:\Research\arc3\repo
$pd = "C:\Users\Shivani Mishra\AppData\Local\Pandoc\pandoc.exe"
& $pd docs\manuscript_jagi\manuscript_jagi.md -o docs\manuscript_jagi\manuscript_jagi.docx --reference-doc=docs\manuscript_jagi\jagi_reference.docx --resource-path=docs\manuscript_jagi --shift-heading-level-by=-1 --lua-filter=docs\manuscript_jagi\jagi.lua --table-caption-position=below -M author="Rahul Kumar Mishra"
& $pd docs\manuscript_jagi\supplement_jagi.md -o docs\manuscript_jagi\supplement_jagi.docx --reference-doc=docs\manuscript_jagi\jagi_reference.docx --resource-path=docs\manuscript_jagi --shift-heading-level-by=-1 --lua-filter=docs\manuscript_jagi\jagi.lua --table-caption-position=below -M author="Rahul Kumar Mishra"
```

Expected: no output, and the two .docx files in docs\manuscript_jagi.

Step 7. Convert both to PDF with docx2pdf (Microsoft Word must be installed), and print the page counts.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe -c "from docx2pdf import convert; convert(r'docs\manuscript_jagi\manuscript_jagi.docx', r'docs\manuscript_jagi\manuscript_jagi.pdf')"
D:\Research\arc3\brutus\.venv\Scripts\python.exe -c "from docx2pdf import convert; convert(r'docs\manuscript_jagi\supplement_jagi.docx', r'docs\manuscript_jagi\supplement_jagi.pdf')"
pdfinfo docs\manuscript_jagi\manuscript_jagi.pdf | Select-String "Pages|Page size|Author|Creator"
pdfinfo docs\manuscript_jagi\supplement_jagi.pdf | Select-String "Pages|Page size|Author|Creator"
```

Expected: manuscript_jagi.pdf 21 pages, supplement_jagi.pdf 10 pages, page size 612 x 792 pts (letter), Author "Rahul Kumar Mishra".

Step 8. Metadata and forbidden-word checks on the built files.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe -I -c "import zipfile,re,sys; [print(f, re.findall(r'<(dc:creator|cp:lastModifiedBy|dc:title|dc:subject|cp:keywords|dc:description)>([^<]*)<', zipfile.ZipFile(f).read('docProps/core.xml').decode()), sum(len(re.findall(r'(?i)assistant|claude|language model|\bllms?\b|generated|co-authored', zipfile.ZipFile(f).read(n).decode('utf-8','ignore'))) for n in zipfile.ZipFile(f).namelist() if n.endswith('.xml'))) for f in sys.argv[1:]]" docs\manuscript_jagi\manuscript_jagi.docx docs\manuscript_jagi\supplement_jagi.docx
foreach ($f in "manuscript_jagi","supplement_jagi") { pdftotext docs\manuscript_jagi\$f.pdf "$env:TEMP\$f.txt"; $n = (Select-String -Path "$env:TEMP\$f.txt" -Pattern 'assistant|claude|language model|\bLLMs?\b|generated|delve|leverag|robust|comprehensive|\bnovel|showcas|underscor|crucial|pivotal|landscape|tapestr|\brealms?\b|paradigm|harness|foster|holistic|seamless|cutting-edge|state of the art|it is worth noting|importantly|notably|in this work|in conclusion|furthermore|moreover|additionally').Count; "$f.pdf forbidden-word hits: $n" }
```

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe -I -c "import zipfile,re,sys; [print(f, 'app.xml:', re.sub(r'<[^>]+>',' ',zipfile.ZipFile(f).read('docProps/app.xml').decode()).split(), 'template-name hits:', sum(len(re.findall(r'(?i)waser|pei wang|instructions for formatting|hewlett', zipfile.ZipFile(f).read(n).decode('utf-8','ignore'))) for n in zipfile.ZipFile(f).namelist() if n.endswith('.xml'))) for f in sys.argv[1:]]" docs\manuscript_jagi\manuscript_jagi.docx docs\manuscript_jagi\supplement_jagi.docx
```

Expected: for each docx, the creator "Rahul Kumar Mishra", the title, every other field empty, and 0 hits; for each PDF, its hit count. The only allowed hit is "Leveraging" in the title of Cobbe et al. (2020) in the reference list of manuscript_jagi.pdf. For each docx, app.xml holds only the template, application and version fields, and 0 template-name hits.
