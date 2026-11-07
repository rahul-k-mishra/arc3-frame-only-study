"""Set a .docx file's document properties: creator = the given name, every other field empty.

Usage (from D:\\Research\\arc3\\repo):
    python scripts\\docx_metadata.py docs\\manuscript_tog\\title_page.docx --creator "Rahul Kumar Mishra"

Rewrites, inside the docx package and nothing else:
  docProps/core.xml    dc:creator = the name; dc:title, dc:subject, dc:description, cp:keywords,
                       cp:lastModifiedBy empty; no created or modified date;
  docProps/app.xml     an empty Properties element (no application name, template or statistics);
  docProps/custom.xml  an empty Properties element, if present.
Every other part is copied byte for byte, in the original order. Standard library only.

Expected output:
    <path>: creator "<name>", every other property empty
followed by the properties read back from the written file.
"""
import argparse
import os
import re
import shutil
import tempfile
import zipfile
from xml.sax.saxutils import escape

CORE = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title></dc:title><dc:subject></dc:subject><dc:creator>{creator}</dc:creator>'
        '<cp:keywords></cp:keywords><dc:description></dc:description><cp:lastModifiedBy></cp:lastModifiedBy>'
        '</cp:coreProperties>')
APP = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
       '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
       'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"></Properties>')
CUSTOM = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties" '
          'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"></Properties>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--creator", required=True)
    a = ap.parse_args()
    repl = {"docProps/core.xml": CORE.format(creator=escape(a.creator)),
            "docProps/app.xml": APP, "docProps/custom.xml": CUSTOM}
    fd, tmp = tempfile.mkstemp(suffix=".docx", dir=os.path.dirname(os.path.abspath(a.path)))
    os.close(fd)
    with zipfile.ZipFile(a.path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = repl[info.filename].encode("utf-8") if info.filename in repl else zin.read(info)
            zout.writestr(info, data)
    shutil.move(tmp, a.path)
    print(f'{a.path}: creator "{a.creator}", every other property empty')
    with zipfile.ZipFile(a.path) as z:
        for part in ("docProps/core.xml", "docProps/app.xml", "docProps/custom.xml"):
            if part in z.namelist():
                body = z.read(part).decode("utf-8")
                fields = re.findall(r"<([\w:]+)(?:\s[^>]*)?>([^<]*)</\1>", body)
                print(f"  {part}: " + ("; ".join(f"{k} = \"{v}\"" for k, v in fields) or "no fields"))


if __name__ == "__main__":
    main()
