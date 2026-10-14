# Building the JOTE manuscript

Every command runs in PowerShell from D:\Research\arc3\repo, in this order. Nothing here plays a game or reads runs/suites; the three scripts read committed files only.

Step 1. Write docs/manuscript/numbers.json and docs/manuscript/appendix_c.md from the committed tables, JSON files, protocol and log (ARC venv).

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_numbers.py
```

Expected: one "check ok:" line per cross-check, then "numbers.json: ... values written", "appendix_c.md: 9 number classes written" and "all cross-checks passed". If Table C1 in manuscript.md differs from the new appendix_c.md, step 3 reports it under (g); copy appendix_c.md into Appendix C unchanged.

Step 2. Draw the four figures (docs/manuscript/fig1.png to fig4.png), one worker per figure.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_figures.py
```

Expected: four blocks "fig<k>.png from <source>", each listing every number drawn, then "4 figures written to docs/manuscript". The numbers printed can be matched against numbers.json.

Step 3. Check the manuscript against numbers.json and the journal's limits.

```powershell
cd D:\Research\arc3\repo
D:\Research\arc3\brutus\.venv\Scripts\python.exe scripts\manuscript_check.py
echo "exit code: $LASTEXITCODE"
```

Expected: blocks (a) to (g), each ending "0 issues", the word counts of the take-home message, abstract and purpose section within their limits, "RESULT: PASS" and "exit code: 0". Do not build or commit the manuscript unless the exit code is 0.

Step 4. Build the submission file and the cover letter with pandoc. The only metadata author is the author's name.

```powershell
cd D:\Research\arc3\repo
& "C:\Users\Shivani Mishra\AppData\Local\Pandoc\pandoc.exe" docs\manuscript\manuscript.md -o docs\manuscript\manuscript.docx --resource-path=docs\manuscript --shift-heading-level-by=-1 -M author="Rahul Kumar Mishra"
& "C:\Users\Shivani Mishra\AppData\Local\Pandoc\pandoc.exe" docs\manuscript\cover_letter.md -o docs\manuscript\cover_letter.docx -M author="Rahul Kumar Mishra" -M title="Cover letter"
```

Expected: no output, and the two .docx files in docs\manuscript. The figures are embedded in manuscript.docx at the point of first reference. The option --shift-heading-level-by=-1 makes the sections Heading 1 and the subsections Heading 2 in Word.
