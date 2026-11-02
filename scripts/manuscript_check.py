"""
manuscript_check.py -- checks docs/manuscript/manuscript.md against docs/manuscript/numbers.json.

Reports, with line numbers:
  (a) every numeral, hash, date, ORCID or URL in the manuscript that does not match a value in
      numbers.json;
  (b) every hit of the forbidden words and phrases (aid-related words and style words), outside the
      titles of cited papers in the reference list;
  (c) every in-text author-date citation without a reference entry, and every reference entry never
      cited;
  (d) every British spelling from a fixed list, outside quotations and code;
  (e) the word counts of the take-home message (at most 50 words, at most three sentences), the
      abstract (150 to 250 words) and the purpose section (at most 250 words);
  (f) every figure file referenced by the manuscript that does not exist;
  (g) whether Appendix C contains docs/manuscript/appendix_c.md exactly, as written by
      scripts/manuscript_numbers.py.
It also prints the word count of the main text (Introduction through Conclusion), for information.

What is not a numeral for (a): digits joined to letters (A1, D9b, v1.1, 8x8, fig1.png, ARC-AGI-3,
S3R1-v0), because they are names, not quantities; and the label numbers of "Figure k" and "Table k".
Every other digit run is checked, including those in the verbatim tables and references.
A numeral matches when it equals, character for character after removing thousands commas and
writing the minus sign as "-", a numeric value in numbers.json or a numeric part of a composite value
(a version, a ratio, a date).  Hashes (7 to 40 hex characters with a digit and a letter) must equal a
hash value; dates "d Month yyyy" must equal a date value; URLs must equal a URL value.

Run (working directory D:\\Research\\arc3\\repo), after scripts\\manuscript_numbers.py:
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\manuscript_check.py
An optional argument names another file in docs/manuscript to check instead of manuscript.md, for
example the preprint variant:
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\manuscript_check.py preprint_variant.md

The option --dir names another manuscript directory (for example docs/manuscript_jagi).  The file
argument is then a file in that directory, and numbers.json, appendix_c.md and the figures are read
from that directory:
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\manuscript_check.py --dir docs\\manuscript_jagi manuscript_jagi.md
In that mode only:
  - (e) checks the limits of the sections the file has (the take-home message and the purpose
    section are JOTE sections), and requires an abstract when the file has a reference list;
  - (g) runs only when the file has a level-2 heading containing "Provenance" (the supplement);
  - a reference entry that equals, character for character, a line "Printed: <entry>" of a file
    REFERENCES_CHECK*.md in that directory is exempt from (a), because its fields were verified
    against the publisher's page and recorded there;
  - a year inside an in-text citation is exempt from (a) when (c) finds the cited work in the
    reference list.
In both modes: section numbers at the start of a heading ("## 3 Method", "### 3.1 ...") are not
checked as numerals and are ignored when sections are looked up by name; lines that open or close a
pandoc div (":::") and a "**Keywords:**" line do not count toward the word limits; in-text
citations may use "and" as well as "&"; a reference entry's year may stand without parentheses
("Legg, S., and Hutter, M. 2007."), as in the JAGI reference style; family names may carry accented
letters; an organization may be the author ("ARC Prize Foundation. 2026." in the list, "(ARC Prize
Foundation, 2026)" or "ARC Prize Foundation (2026)" in the text), and is matched by its full name.

Option --ieee (after --dir; IEEE Transactions on Games version, docs/manuscript_tog/BUILD.md):
  - citations are IEEE numbered citations "[n]" in the text, and the reference list is a sequence of
    lines "[n] entry"; (c) reports every number cited without an entry, every entry never cited,
    every gap in the numbering, and any entry whose number is not in order of first citation;
  - (a) does not check citation numbers, the label numbers of "Fig. k" and "Figs. k and m", or the
    "[n] " label of a reference entry; the entry after its label is compared with the "Printed: "
    lines of REFERENCES_CHECK*.md as above;
  - (e) checks the abstract against the journal's limit of 150 to 200 words;
  - a "**Index Terms:**" line does not count toward the word limits (in every mode).
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\manuscript_check.py --dir docs\\manuscript_tog --ieee manuscript_tog.md

Option --bib FILE (after --dir; KI - Kuenstliche Intelligenz version, docs/manuscript_ki/BUILD.md): the
file is a pandoc source whose citations are keys in brackets ("[@key]", "[@a; @b]") and whose
reference list is typeset by BibTeX from FILE, a .bib file in the same directory, into the .bbl file
of the LaTeX build (the file's name with .bbl in place of .md; the LaTeX build must have run first):
  - (c) compares the cited keys with the entries of FILE, and both with the entries of the .bbl;
  - (a) does not read citation keys as numerals; each .bbl entry, written as plain text (the commands
    of the bibliography style removed, a DOI written as its https://doi.org/ link, "--" as an en dash),
    is accepted when it equals a "Printed: " line of REFERENCES_CHECK*.md in the directory, and is
    otherwise checked like any other line;
  - (b) also reads the .bbl entries, outside the titles in FILE;
  - (f) also checks every \\includegraphics{name} of a raw LaTeX block: name, name.pdf or name.eps must
    exist in the directory;
  - $...$ math is read as its text ("$-0.4125$" is the numeral -0.4125, "$\\kappa$" no numeral).
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe scripts\\manuscript_check.py --dir docs\\manuscript_ki --bib references_ki.bib manuscript_ki.md
  - a trailing pandoc attribute of a level-2 heading ("{#sec:intro}", "{-}") is ignored when sections
    are looked up by name.
Without the option the script behaves exactly as before.

Exit code 0 only when every count is zero and every limit holds; 1 otherwise.
Expected console output when the manuscript is clean: seven blocks (a) to (g), each ending in
"0 issues", the main-text word count, and "RESULT: PASS".
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MS_DIR = os.path.join(ROOT, "docs", "manuscript")
NAME = r"[A-Z][A-Za-z\u00c0-\u00ff\-]+"
ORG = r"[A-Z][A-Za-z\-]+(?: [A-Z][A-Za-z\-]+)* (?:Foundation|Society|Institute|Association|Prize)(?: [A-Z][A-Za-z\-]+)*"
HEADNUM = re.compile(r"^(#{1,6} )(\d+(?:\.\d+)*\.? )")
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"

FORBIDDEN = [r"delv\w*", r"leverag\w*", r"robust\w*", r"comprehensive\w*", r"novel", r"novelty", r"showcas\w*",
             r"underscor\w*", r"crucial\w*", r"pivotal\w*", r"landscape\w*", r"tapestr\w*", r"realms?",
             r"paradigm\w*", r"harness\w*", r"foster\w*", r"holistic\w*", r"seamless\w*", r"cutting-edge",
             r"state[ -]of[ -]the[ -]art", r"it is worth noting", r"importantly", r"notably", r"in this work",
             r"in conclusion", r"furthermore", r"moreover", r"additionally",
             r"assistants?", r"claude", r"language models?", r"llms?", r"generated"]
BRITISH = [r"licence\w*", r"colour\w*", r"centre\w*", r"behaviour\w*", r"modelling", r"analys(?:e|es|ed|ing)",
           r"summaris\w*", r"programme\w*", r"favour\w*", r"honour\w*", r"labelled", r"cancelled"]


def norm(tok):
    tok = tok.replace("−", "-")
    if re.fullmatch(r"-?\d{1,3}(,\d{3})+(\.\d+)?", tok):
        tok = tok.replace(",", "")
    return tok


def allowed_sets(numbers):
    nums, hashes, dates, urls = set(), set(), set(), set()
    for v in numbers.values():
        val, cls = v["value"], v["class"]
        s = str(val)
        if cls == "hash":
            hashes.add(s)
            continue
        if cls == "url":
            urls.add(s)
            continue
        if cls == "date":
            dates.add(s)
        if isinstance(val, (int, float)):
            nums.add(norm(str(val)))
            continue
        if re.fullmatch(r"[−-]?\d[\d,]*(\.\d+)*", s):
            nums.add(norm(s))
        for part in re.findall(r"[−-]?\d+(?:[.,]\d+)*", s):
            nums.add(norm(part))
            nums.add(norm(part.lstrip("-−")))
    return nums, hashes, dates, urls


def sections(lines, strip_attr=False):
    """{heading: (first line index, last line index)} for level-2 headings, section numbers removed, and,
    with strip_attr (--bib only), a trailing pandoc attribute ("{#sec:intro}", "{-}") removed."""
    idx = [(i, HEADNUM.sub(r"\1", l)[3:].strip()) for i, l in enumerate(lines) if l.startswith("## ")]
    if strip_attr:
        idx = [(i, re.sub(r"\s*\{[#.\-][^}]*\}\s*$", "", h)) for i, h in idx]
    out = {}
    for k, (i, h) in enumerate(idx):
        end = idx[k + 1][0] if k + 1 < len(idx) else len(lines)
        out[h] = (i + 1, end)
    return out


def words(txt):
    txt = "\n".join(l for l in txt.splitlines()
                    if not l.lstrip().startswith(":::") and not l.lstrip().startswith("**Keywords:**")
                    and not l.lstrip().startswith("**Index Terms:**"))
    txt = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", txt)
    txt = re.sub(r"[*_>#|`]", " ", txt)
    return [w for w in txt.split() if re.search(r"[\w]", w)]


def bib_titles():
    with open(os.path.join(ROOT, "docs", "preprint", "references.bib"), encoding="utf-8") as f:
        bib = f.read()
    return [re.sub(r"[{}]", "", t).lower().replace("--", "–")
            for t in re.findall(r"^\s*title\s*=\s*\{(.*)\},?\s*$", bib, re.M)]


def cited_and_refs(lines, ref_start, ref_end):
    """(cited works, reference entries), each a set of (family name, year)."""
    body = "\n".join(lines[:ref_start - 1] + lines[ref_end:])
    cited = set()
    for m in re.finditer(rf"({NAME})(?: et al\.| and {NAME})? \((\d{{4}})\)", body):
        cited.add((m.group(1), m.group(2)))
    for m in re.finditer(rf"({ORG}),? \(?(\d{{4}})\)?", body):
        cited.add((m.group(1), m.group(2)))
    for grp in re.findall(r"\(([^()]*?\d{4}[^()]*?)\)", body):
        for part in grp.split(";"):
            m = re.match(rf"\s*(?:see |e\.g\., )?({NAME})(?: et al\.| & {NAME}| and {NAME})?, (\d{{4}})\s*$", part)
            if m:
                cited.add((m.group(1), m.group(2)))
    refs = set()
    for line in lines[ref_start:ref_end]:
        m = re.match(rf"({NAME}), [A-Z]\..*?\(?(\d{{4}})\)?\.", line)
        if m:
            refs.add((m.group(1), m.group(2)))
            continue
        m = re.match(rf"({ORG})\. (\d{{4}})\.", line)
        if m:
            refs.add((m.group(1), m.group(2)))
    return cited, refs


def ieee_citations(lines, ref_start, ref_end):
    """IEEE numbered citations: (cited numbers, entry numbers, issues)."""
    order = []
    for i, line in enumerate(lines):
        if ref_start <= i < ref_end:
            continue
        for m in re.finditer(r"\[(\d+)\]", line):
            k = int(m.group(1))
            if k not in order:
                order.append(k)
    entries = []
    for line in lines[ref_start:ref_end]:
        m = re.match(r"\[(\d+)\] ", line)
        if m:
            entries.append(int(m.group(1)))
    cited, refs = set(order), set(entries)
    issues = [f"cited without entry: [{k}]" for k in sorted(cited - refs)]
    issues += [f"entry never cited: [{k}]" for k in sorted(refs - cited)]
    if entries != list(range(1, len(entries) + 1)):
        issues.append(f"entries not numbered 1 to {len(entries)} in sequence: {entries}")
    if order != sorted(order):
        issues.append(f"entries not in order of first citation: first citations in the order {order}")
    return cited, refs, issues


CITE = re.compile(r"\[[^\[\]]*?(?<![\w.])@[A-Za-z][^\[\]]*?\]")
ACCENTS = {"\\'e": "é", "\\'E": "É", '\\"u': "ü", '\\"o': "ö", '\\"a': "ä", "\\~a": "ã", "\\c{c}": "ç"}


def bib_keys_titles(path):
    """(keys in order, lower-case titles without braces) of a .bib file."""
    with open(path, encoding="utf-8") as f:
        bib = f.read()
    keys = re.findall(r"^@\w+\{([^,\s]+),", bib, re.M)
    titles = [re.sub(r"[{}]", "", t).replace("\\&", "&").lower()
              for t in re.findall(r"^\s*title\s*=\s*\{(.*)\},?\s*$", bib, re.M)]
    return keys, titles


def bbl_entries(path):
    """[(key, plain text)] of the entries of a BibTeX .bbl file, in their printed order."""
    with open(path, encoding="utf-8") as f:
        bbl = f.read()
    out = []
    for m in re.finditer(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})", bbl, re.S):
        t = m.group(2)
        t = re.sub(r"\\doi\{([^}]*)\}", r"https://doi.org/\1", t)
        t = re.sub(r"\\url\{([^}]*)\}", r"\1", t)
        t = t.replace("\\urlprefix", "").replace("\\newblock", " ").replace("\\relax ", "")
        for a, b in ACCENTS.items():
            t = t.replace("{" + a + "}", b).replace(a, b)
        t = re.sub(r"\\(?:textbf|emph|textit|em)\b", "", t)
        t = t.replace("\\&", "&").replace("--", "\u2013").replace("~", " ").replace("\\ ", " ")
        t = re.sub(r"[{}]", "", t)
        t = re.sub(r"\s+", " ", t).strip()
        out.append((m.group(1), t))
    return out


def main():
    args = sys.argv[1:]
    ms_dir, other_dir, ieee, bib = MS_DIR, False, False, None
    if args[:1] == ["--dir"]:
        ms_dir, other_dir = os.path.join(ROOT, args[1]), True
        args = args[2:]
        if args[:1] == ["--ieee"]:
            ieee = True
            args = args[1:]
        if args[:1] == ["--bib"]:
            bib = args[1]
            args = args[2:]
    ms_file = args[0] if args else "manuscript.md"
    rel_dir = os.path.relpath(ms_dir, ROOT).replace(os.sep, "/")
    print(f"checking {rel_dir}/{ms_file}")
    with open(os.path.join(ms_dir, ms_file), encoding="utf-8") as f:
        raw = f.read()
    with open(os.path.join(ms_dir, "numbers.json"), encoding="utf-8") as f:
        numbers = json.load(f)
    lines = raw.splitlines()
    nums, hashes, dates, urls = allowed_sets(numbers)
    secs = sections(lines, strip_attr=bool(bib))
    ref_start, ref_end = secs.get("References", (len(lines), len(lines)))
    if ieee:
        cited, refs, ieee_issues = ieee_citations(lines, ref_start, ref_end)
    else:
        cited, refs = cited_and_refs(lines, ref_start, ref_end)
    bbl, bib_titles_ki, bbl_path = [], [], None
    if bib:
        keys, bib_titles_ki = bib_keys_titles(os.path.join(ms_dir, bib))
        refs = set(keys)
        cited = set()
        for line in lines:
            for c in CITE.findall(line):
                cited |= set(re.findall(r"(?<![\w.])@([A-Za-z][\w:\-]*)", c))
        bbl_path = os.path.join(ms_dir, os.path.splitext(ms_file)[0] + ".bbl")
        if os.path.exists(bbl_path):
            bbl = bbl_entries(bbl_path)
        print(f"bibliography: {len(keys)} entries in {bib}, {len(bbl)} entries in "
              f"{os.path.basename(bbl_path)}" + ("" if bbl else " (missing: run the LaTeX build first)"))
    printed = set()
    if other_dir:
        for fn in sorted(os.listdir(ms_dir)):
            if fn.startswith("REFERENCES_CHECK") and fn.endswith(".md"):
                with open(os.path.join(ms_dir, fn), encoding="utf-8") as f:
                    printed |= {l[len("Printed: "):].strip() for l in f.read().splitlines()
                                if l.startswith("Printed: ")}
        print(f"verified reference entries read from REFERENCES_CHECK*.md: {len(printed)}")
    failed = False

    # (a) numerals, hashes, dates, URLs
    issues = []
    for n, line in enumerate(lines, 1):
        t = HEADNUM.sub(r"\1", line)
        in_refs = ref_start <= n - 1 < ref_end
        if ieee and in_refs:
            t = re.sub(r"^\[\d+\] ", "", t)
            if t.strip() in printed:
                continue
        if ieee and not in_refs:
            t = re.sub(r"\[\d+\]", " ", t)
            t = re.sub(r"\bFigs?\. \d+(?: and \d+)?", " ", t)
        if other_dir and in_refs and line.strip() in printed:
            continue
        if bib:
            t = CITE.sub(" ", t)
            t = re.sub(r"\$([^$]*)\$", lambda m: re.sub(r"\\[A-Za-z]+", " ", m.group(1)), t)
            t = re.sub(r"\\includegraphics(\[[^\]]*\])?\{[^}]*\}", " ", t)
        if other_dir and not in_refs and not ieee:
            t = re.sub(rf"({NAME})((?: et al\.| and {NAME}| & {NAME})?(?: \(|, ))(\d{{4}})(?=[);])",
                       lambda m: m.group(1) + m.group(2) + (" " if (m.group(1), m.group(3)) in refs
                                                            else m.group(3)), t)
        for u in re.findall(r"https?://\S+", t):
            u2 = u.rstrip(".,;")
            while u2.endswith(")") and u2.count(")") > u2.count("("):
                u2 = u2[:-1].rstrip(".,;")
            if u2 not in urls:
                issues.append((n, "URL", u2))
            t = t.replace(u, " ")
        t = re.sub(r"!\[[^\]]*\]\(([^)]*)\)", lambda m: m.group(0).replace(m.group(1), " "), t)
        for m in re.finditer(rf"\b(\d{{1,2}}) ({MONTHS}) (\d{{4}})\b", t):
            if m.group(0) not in dates:
                issues.append((n, "date", m.group(0)))
        t = re.sub(rf"\b\d{{1,2}} (?:{MONTHS}) \d{{4}}\b", " ", t)
        for m in re.finditer(r"\b\d{4}-\d{4}-\d{4}-\d{3}[\dX]\b", t):
            if m.group(0) not in {str(v["value"]) for v in numbers.values()}:
                issues.append((n, "ORCID", m.group(0)))
        t = re.sub(r"\b\d{4}-\d{4}-\d{4}-\d{3}[\dX]\b", " ", t)
        for m in re.finditer(r"\b[0-9a-f]{7,40}\b", t):
            h = m.group(0)
            if re.search(r"\d", h) and re.search(r"[a-f]", h):
                if h not in hashes:
                    issues.append((n, "hash", h))
        t = re.sub(r"\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b", " ", t)
        t = re.sub(r"\b(Figure|Table|Figures|Tables) \d+(?: and \d+)?", " ", t)
        for m in re.finditer(r"(?<![\w\-./])[−-]?\d+(?:[.,]\d+)*(?![\w])(?!\.[A-Za-z])", t):
            tok = norm(m.group(0))
            if tok not in nums and tok.lstrip("-") not in nums:
                issues.append((n, "numeral", m.group(0)))
    if bib:
        for k, (key, entry) in enumerate(bbl, 1):
            if entry in printed:
                continue
            t = entry
            for u in re.findall(r"https?://\S+", t):
                u2 = u.rstrip(".,;")
                if u2 not in urls:
                    issues.append((f"bbl {k} ({key})", "URL", u2))
                t = t.replace(u, " ")
            for m in re.finditer(r"(?<![\w\-./])[−-]?\d+(?:[.,]\d+)*(?![\w])(?!\.[A-Za-z])", t):
                tok = norm(m.group(0))
                if tok not in nums and tok.lstrip("-") not in nums:
                    issues.append((f"bbl {k} ({key})", "numeral", m.group(0)))
        if not bbl:
            issues.append((os.path.basename(bbl_path), "file", "missing .bbl"))
    print("(a) numerals, hashes, dates, ORCID and URLs not in numbers.json")
    for n, kind, tok in issues:
        print(f"    line {n}: {kind} {tok}")
    print(f"    {len(issues)} issues")
    failed |= bool(issues)

    # (b) forbidden words
    titles = bib_titles()
    issues = []
    for n, line in enumerate(lines, 1):
        for pat in FORBIDDEN:
            for m in re.finditer(rf"\b{pat}\b", line, re.I):
                if ref_start <= n - 1 < ref_end and any(m.group(0).lower() in t for t in titles):
                    continue
                issues.append((n, m.group(0)))
    for k, (key, entry) in enumerate(bbl, 1):
        for pat in FORBIDDEN:
            for m in re.finditer(rf"\b{pat}\b", entry, re.I):
                if any(m.group(0).lower() in t for t in bib_titles_ki):
                    continue
                issues.append((f"bbl {k} ({key})", m.group(0)))
    print("(b) forbidden words and phrases (outside cited titles)")
    for n, w in issues:
        print(f"    line {n}: {w}")
    print(f"    {len(issues)} issues")
    failed |= bool(issues)

    # (c) citations against the reference list
    if ieee:
        issues = ieee_issues
    elif bib:
        issues = [f"cited without entry: {k}" for k in sorted(cited - refs)]
        issues += [f"entry never cited: {k}" for k in sorted(refs - cited)]
        if bbl and {k for k, _ in bbl} != cited:
            issues.append(f".bbl entries differ from the cited keys: {sorted({k for k, _ in bbl} ^ cited)}")
    else:
        issues = [f"cited without entry: {a} ({y})" for a, y in sorted(cited - refs)]
        issues += [f"entry never cited: {a} ({y})" for a, y in sorted(refs - cited)]
    print(f"(c) citations: {len(cited)} cited works, {len(refs)} reference entries")
    for i in issues:
        print("    " + i)
    print(f"    {len(issues)} issues")
    failed |= bool(issues)

    # (d) British spellings outside quotations and code
    issues = []
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith(">"):
            continue
        t = re.sub(r"`[^`]*`", " ", line)
        t = re.sub(r"\"[^\"]*\"|“[^”]*”", " ", t)
        for pat in BRITISH:
            for m in re.finditer(rf"\b{pat}\b", t, re.I):
                issues.append((n, m.group(0)))
    print("(d) British spellings outside quotations and code")
    for n, w in issues:
        print(f"    line {n}: {w}")
    print(f"    {len(issues)} issues")
    failed |= bool(issues)

    # (e) word limits
    print("(e) word limits")
    n_issues = 0
    for name, lo, hi, max_sent in (("Take-home message", 0, 50, 3), ("Abstract", 150, 200 if ieee else 250, None),
                                   ("Purpose", 0, 250, None)):
        if other_dir and name not in secs and not (name == "Abstract" and "References" in secs):
            print(f"    {name}: not a section of this file, no limit applies")
            continue
        if name not in secs:
            print(f"    section '{name}' missing")
            n_issues += 1
            continue
        a, b = secs[name]
        txt = "\n".join(lines[a:b])
        w = len(words(txt))
        ok = lo <= w <= hi
        msg = f"    {name}: {w} words (limit {lo}-{hi})"
        if max_sent:
            s = len(re.findall(r"[.!?](?=\s|$)", txt.strip()))
            ok = ok and s <= max_sent
            msg += f", {s} sentences (limit {max_sent})"
        print(msg + ("" if ok else "  <-- OUT OF LIMIT"))
        n_issues += not ok
    print(f"    {n_issues} issues")
    failed |= bool(n_issues)

    # (f) figure files
    issues = []
    for n, line in enumerate(lines, 1):
        for m in re.finditer(r"!\[[^\]]*\]\(([^)\s]+)", line):
            if not os.path.exists(os.path.join(ms_dir, m.group(1))):
                issues.append((n, m.group(1)))
        if bib:
            for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", line):
                if not any(os.path.exists(os.path.join(ms_dir, m.group(1) + e)) for e in ("", ".pdf", ".eps")):
                    issues.append((n, m.group(1)))
    print("(f) figure files referenced but missing")
    for n, p in issues:
        print(f"    line {n}: {p}")
    print(f"    {len(issues)} issues")
    failed |= bool(issues)

    # (g) Appendix C equals appendix_c.md
    if other_dir and not any("Provenance" in h for h in secs):
        print(f"(g) no provenance section in this file; {rel_dir}/appendix_c.md is not looked for")
        print("    0 issues")
    else:
        with open(os.path.join(ms_dir, "appendix_c.md"), encoding="utf-8") as f:
            app = f.read().strip()
        ok = app in raw
        print(f"(g) Appendix C contains {rel_dir}/appendix_c.md exactly")
        print(f"    {0 if ok else 1} issues")
        failed |= not ok

    names = list(secs)
    if "Introduction" in secs and "Conclusion" in secs:
        a = secs["Introduction"][0]
        b = secs["Conclusion"][1]
        print(f"main text (Introduction through Conclusion): {len(words(chr(10).join(lines[a:b])))} words")
    print("sections:", "; ".join(names))
    print("RESULT:", "FAIL" if failed else "PASS")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
