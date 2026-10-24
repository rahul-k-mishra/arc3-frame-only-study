"""
make_reference_doc.py -- derive the pandoc reference document for the JAGI manuscript from the
journal's Word template (Author's Kit, Instruction-word.docx).

pandoc takes page size, margins, styles, headers and footers from a reference document and ignores
its body.  The kit template is used as it is, with four changes, all in the copy written here:
  1. its sample running heads are replaced: the even-page head becomes the short author name, the
     odd-page head the short title, and the first-page head keeps the AGI Society logo and the
     journal name and carries only the submission date, as the kit asks for a first submission;
  2. the automatic numbering is removed from Heading 1 to Heading 3, because the manuscript numbers
     its sections in the text and its unnumbered sections (Abstract, References, ...) must stay
     unnumbered;
  3. the style names pandoc writes (Title, Author, Body Text, First Paragraph, Compact, Image
     Caption, Table Caption, Captioned Figure, Figure, Table) are defined on top of the kit's own
     styles (Article Title, Author Name, Text, Abstract Text), so that pandoc's output takes the
     journal's fonts, sizes, spacing and indents; Compact, the style of every table cell, keeps
     with the next paragraph, so that a table stays on one page together with its caption below it; captions keep their lines
     together, and a figure keeps with its caption, so that a figure and its whole caption share a page;
  4. the template's document properties are cleared: title, creator and last modified by in
     core.xml, and app.xml (which named the template's title and company) is replaced by a minimal
     one with no title, company or statistics.
Nothing is read from the repository; the kit file is read only.

Run (working directory D:\\Research\\arc3\\repo):
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe -I docs\\manuscript_jagi\\make_reference_doc.py D:\\Research\\arc3\\jagi_kit\\JAGIAuthorKit\\Instruction-word.docx docs\\manuscript_jagi\\jagi_reference.docx --submitted yyyy-mm-dd

Expected console output:
    reference document written: docs\\manuscript_jagi\\jagi_reference.docx (headers 3, styles added 10, numbering removed 3)
"""
from __future__ import annotations

import argparse
import re
import zipfile

SHORT_AUTHOR = "Mishra"
SHORT_TITLE = "A Frame-Only Census Did Not Generalize"


def caps_runs(text, big=20, small=16):
    """Small capitals simulated as the kit does: capitals at 10 pt, the rest upper case at 8 pt."""
    runs = []
    for i, word in enumerate(text.split(" ")):
        if i:
            runs.append((" ", small))
        if word:
            runs.append((word[0].upper(), big))
            if len(word) > 1:
                runs.append((word[1:].upper(), small))
    return "".join(f'<w:r><w:rPr><w:b w:val="0"/><w:sz w:val="{s}"/><w:szCs w:val="{s}"/></w:rPr>'
                   f'<w:t xml:space="preserve">{t}</w:t></w:r>' for t, s in runs)


def replace_runs(par, new_runs):
    """Keep the paragraph's properties, replace all its runs."""
    m = re.match(r"(<w:p\b[^>]*>(?:<w:pPr>.*?</w:pPr>)?)(.*)(</w:p>)$", par, re.S)
    return m.group(1) + new_runs + m.group(3)


def paragraphs(xml):
    return re.findall(r"<w:p\b[^>]*>.*?</w:p>|<w:p\b[^>]*/>", xml, re.S)


def text_of(par):
    return "".join(re.findall(r"<w:t(?:\s[^>]*)?>([^<]*)</w:t>", par))


def fix_headers(files, submitted):
    out = dict(files)
    h1 = out["word/header1.xml"].decode("utf-8")      # even pages
    p = [q for q in paragraphs(h1) if text_of(q).strip()][0]
    out["word/header1.xml"] = h1.replace(p, replace_runs(p, caps_runs(SHORT_AUTHOR))).encode("utf-8")

    h2 = out["word/header2.xml"].decode("utf-8")      # odd pages
    p = [q for q in paragraphs(h2) if text_of(q).strip()][0]
    out["word/header2.xml"] = h2.replace(p, replace_runs(p, caps_runs(SHORT_TITLE))).encode("utf-8")

    h3 = out["word/header3.xml"].decode("utf-8")      # first page: logo, journal, submission date
    plain = '<w:r><w:t xml:space="preserve">{}</w:t></w:r>'
    for p in paragraphs(h3):
        t = text_of(p).strip()
        if t.startswith("Journal of Artificial General Intelligence"):
            h3 = h3.replace(p, replace_runs(p, plain.format("Journal of Artificial General Intelligence")))
        elif t.startswith("DOI") or t.startswith("Accepted"):
            h3 = h3.replace(p, replace_runs(p, ""))
        elif t.startswith("Submitted"):
            h3 = h3.replace(p, replace_runs(p, plain.format(f"Submitted {submitted}")))
    out["word/header3.xml"] = h3.encode("utf-8")
    return out


NEW_STYLES = {
    "Title": ('<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
              '<w:basedOn w:val="ArticleTitle"/><w:next w:val="Author"/><w:qFormat/></w:style>'),
    "Author": ('<w:style w:type="paragraph" w:styleId="Author"><w:name w:val="Author"/>'
               '<w:basedOn w:val="AuthorName"/><w:qFormat/></w:style>'),
    "BodyText": ('<w:style w:type="paragraph" w:styleId="BodyText"><w:name w:val="Body Text"/>'
                 '<w:basedOn w:val="Text"/><w:qFormat/></w:style>'),
    "FirstParagraph": ('<w:style w:type="paragraph" w:styleId="FirstParagraph"><w:name w:val="First Paragraph"/>'
                       '<w:basedOn w:val="Text"/><w:next w:val="BodyText"/><w:qFormat/>'
                       '<w:pPr><w:ind w:firstLine="0"/></w:pPr></w:style>'),
    "Compact": ('<w:style w:type="paragraph" w:styleId="Compact"><w:name w:val="Compact"/>'
                '<w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="0" w:after="0"/></w:pPr>'
                '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>'),
    "ImageCaption": ('<w:style w:type="paragraph" w:styleId="ImageCaption"><w:name w:val="Image Caption"/>'
                     '<w:basedOn w:val="Normal"/><w:pPr><w:keepLines/><w:spacing w:before="120" w:after="240"/><w:jc w:val="both"/></w:pPr>'
                     '<w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>'),
    "TableCaption": ('<w:style w:type="paragraph" w:styleId="TableCaption"><w:name w:val="Table Caption"/>'
                     '<w:basedOn w:val="Normal"/><w:pPr><w:keepLines/><w:spacing w:before="120" w:after="240"/><w:jc w:val="both"/></w:pPr>'
                     '<w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>'),
    "CaptionedFigure": ('<w:style w:type="paragraph" w:styleId="CaptionedFigure"><w:name w:val="Captioned Figure"/>'
                        '<w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240"/><w:jc w:val="center"/></w:pPr></w:style>'),
    "Figure": ('<w:style w:type="paragraph" w:styleId="Figure"><w:name w:val="Figure"/>'
               '<w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/></w:pPr></w:style>'),
    "Table": ('<w:style w:type="table" w:styleId="Table"><w:name w:val="Table"/><w:basedOn w:val="TableNormal"/>'
              '<w:tblPr><w:jc w:val="center"/><w:tblBorders>'
              '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
              '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
              '<w:insideH w:val="single" w:sz="2" w:space="0" w:color="808080"/>'
              '</w:tblBorders><w:tblCellMar><w:left w:w="60" w:type="dxa"/><w:right w:w="60" w:type="dxa"/></w:tblCellMar></w:tblPr>'
              '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>'),
}


def fix_styles(files):
    st = files["word/styles.xml"].decode("utf-8")
    removed = 0
    for sid in ("Heading1", "Heading2", "Heading3"):
        m = re.search(rf'<w:style [^>]*w:styleId="{sid}".*?</w:style>', st, re.S)
        new = re.sub(r"<w:numPr>.*?</w:numPr>", "", m.group(0), flags=re.S)
        removed += new != m.group(0)
        st = st.replace(m.group(0), new)
    added = 0
    for sid, xml in NEW_STYLES.items():
        if re.search(rf'w:styleId="{sid}"', st):
            raise SystemExit(f"style {sid} already in the template; not overwritten")
        st = st.replace("</w:styles>", xml + "</w:styles>")
        added += 1
    out = dict(files)
    out["word/styles.xml"] = st.encode("utf-8")
    return out, added, removed


def fix_props(files):
    core = files["docProps/core.xml"].decode("utf-8")
    for tag in ("dc:title", "dc:creator", "cp:lastModifiedBy"):
        core = re.sub(rf"<{tag}>[^<]*</{tag}>", f"<{tag}></{tag}>", core)
    out = dict(files)
    out["docProps/core.xml"] = core.encode("utf-8")
    out["docProps/app.xml"] = APP_XML.encode("utf-8")
    return out


APP_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           '<Template>Normal.dotm</Template><Application>Microsoft Office Word</Application>'
           '<DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><Company></Company>'
           '<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
           '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kit_docx")
    ap.add_argument("out_docx")
    ap.add_argument("--submitted", required=True,
                    help="submission date yyyy-mm-dd; the literal placeholder yyyy-mm-dd until the day of submission")
    a = ap.parse_args()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}|yyyy-mm-dd", a.submitted):
        raise SystemExit("--submitted must be a date yyyy-mm-dd, or the placeholder yyyy-mm-dd itself")
    with zipfile.ZipFile(a.kit_docx) as z:
        names = z.namelist()
        files = {n: z.read(n) for n in names}
    files = fix_headers(files, a.submitted)
    files, added, removed = fix_styles(files)
    files = fix_props(files)
    with zipfile.ZipFile(a.out_docx, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            z.writestr(n, files[n])
    print(f"reference document written: {a.out_docx} (headers 3, styles added {added}, numbering removed {removed})")


if __name__ == "__main__":
    main()
