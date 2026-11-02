"""layout_check.py -- page-by-page layout check of a PDF built for the KI manuscript.

Every page is rendered at 72 dpi with pdftoppm (one pixel per point) into a temporary directory, and
the extent of its ink (any pixel darker than light gray) is measured: leftmost, rightmost, top and
bottom inked pixel.  The text block is taken as the median extent over all pages; a page whose ink
reaches more than 2 pt beyond that block on the left or the right (text or a figure running into the
margin) is reported.  The script also reports pages with less than a tenth of the median ink, so that
an almost empty page is seen.  With the LaTeX log of the build as a second argument it counts the
"Overfull \\hbox" warnings in it.  It reads the PDF only; it changes nothing.

Run (working directory D:\\Research\\arc3\\repo):
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe -I docs\\manuscript_ki\\layout_check.py docs\\manuscript_ki\\manuscript_ki.pdf docs\\manuscript_ki\\manuscript_ki.log
    D:\\Research\\arc3\\brutus\\.venv\\Scripts\\python.exe -I docs\\manuscript_ki\\layout_check.py docs\\manuscript_ki\\ESM_1.pdf
Expected console output: one line per page with its ink extent in points, then "pages with ink in
the side margins: 0", the overfull count (0) when the log is given, and "LAYOUT: PASS".  Nearly empty
pages are listed for information and do not fail the check.
"""
import glob
import os
import statistics
import subprocess
import sys
import tempfile

from PIL import Image


def extent(path):
    im = Image.open(path).convert("L")
    mask = im.point(lambda v: 255 if v < 200 else 0)
    box = mask.getbbox()
    ink = mask.histogram()[255]
    return im.size, box, ink


def main():
    pdf = sys.argv[1]
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", "72", "-png", pdf, os.path.join(tmp, "p")],
                       check=True, capture_output=True)
        files = sorted(glob.glob(os.path.join(tmp, "p-*.png")))
        pages = [extent(f) for f in files]
    lefts = [b[0] for _, b, _ in pages if b]
    rights = [b[2] for _, b, _ in pages if b]
    left, right = statistics.median(lefts), statistics.median(rights)
    med_ink = statistics.median(i for _, _, i in pages)
    (w, h) = pages[0][0]
    print(f"{pdf}: {len(pages)} pages, {w} x {h} pt; text block (median ink extent) x {left} to {right}")
    bad, sparse = [], []
    for n, (size, box, ink) in enumerate(pages, 1):
        if not box:
            print(f"  page {n}: empty")
            sparse.append(n)
            continue
        flag = box[0] < left - 2 or box[2] > right + 2
        if flag:
            bad.append(n)
        if ink < med_ink / 10:
            sparse.append(n)
        print(f"  page {n}: ink x {box[0]} to {box[2]}, y {box[1]} to {box[3]}"
              + ("  <-- INTO THE SIDE MARGIN" if flag else ""))
    print(f"pages with ink in the side margins: {len(bad)}" + (f" {bad}" if bad else ""))
    print(f"nearly empty pages (for information): {sparse if sparse else 'none'}")
    overfull = 0
    if len(sys.argv) > 2:
        with open(sys.argv[2], encoding="latin-1") as f:
            overfull = f.read().count("Overfull \\hbox")
        print(f"overfull lines in the log: {overfull}")
    ok = not bad and overfull == 0
    print("LAYOUT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
