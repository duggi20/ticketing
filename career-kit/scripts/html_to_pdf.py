#!/usr/bin/env python3
"""Print career-kit HTML to 1-page PDFs with classic Chrome headless."""
import os
import signal
import subprocess
import time
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome-stable")
ARTIFACTS = Path("/opt/cursor/artifacts")

HTMLS = [
    ROOT / "resumes" / "Atul_Banyal_Resume_Handshake.html",
    ROOT / "resumes" / "Atul_Banyal_Resume_GitLab_AI.html",
    ROOT / "resumes" / "Atul_Banyal_Resume_Accenture_Python_BLR.html",
    ROOT / "resumes" / "Atul_Banyal_Resume_Amazon_DE.html",
    ROOT / "resumes" / "Atul_Banyal_Resume_Amazon_DB.html",
    ROOT / "resumes" / "Atul_Banyal_Resume_Accenture_Support_Mumbai.html",
    ROOT / "resumes" / "Atul_Banyal_Resume_Deloitte_Fullstack.html",
    ROOT / "resumes" / "Atul_Banyal_Resume_Amazon_SysDE.html",
    ROOT / "cover-letters" / "Atul_Banyal_Cover_Handshake.html",
    ROOT / "cover-letters" / "Atul_Banyal_Cover_GitLab_AI.html",
    ROOT / "cover-letters" / "Atul_Banyal_Cover_Accenture_Python_BLR.html",
    ROOT / "cover-letters" / "Atul_Banyal_Cover_Amazon_DE.html",
    ROOT / "cover-letters" / "Atul_Banyal_Cover_Amazon_DB.html",
    ROOT / "cover-letters" / "Atul_Banyal_Cover_Accenture_Support_Mumbai.html",
    ROOT / "cover-letters" / "Atul_Banyal_Cover_Deloitte_Fullstack.html",
    ROOT / "cover-letters" / "Atul_Banyal_Cover_Amazon_SysDE.html",
]


def wait_stable(path: Path, timeout=25):
    deadline = time.time() + timeout
    last = -1
    stable = 0
    while time.time() < deadline:
        if path.exists():
            size = path.stat().st_size
            if size > 1000 and size == last:
                stable += 1
                if stable >= 4:
                    return size
            else:
                stable = 0
            last = size
        time.sleep(0.25)
    return path.stat().st_size if path.exists() else 0


def html_to_pdf(html: Path, pdf: Path):
    pdf.parent.mkdir(parents=True, exist_ok=True)
    if pdf.exists():
        pdf.unlink()
    profile = Path(f"/tmp/chrome-pdf-{html.stem}-{os.getpid()}")
    profile.mkdir(parents=True, exist_ok=True)
    url = html.resolve().as_uri()
    cmd = [
        CHROME,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--no-pdf-header-footer",
        f"--user-data-dir={profile}",
        "--virtual-time-budget=8000",
        f"--print-to-pdf={pdf}",
        url,
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    size = wait_stable(pdf)
    try:
        proc.send_signal(signal.SIGTERM)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    except ProcessLookupError:
        pass
    if size < 1000:
        raise RuntimeError(f"PDF too small: {pdf} ({size} bytes)")
    return size


def check_pdf(pdf: Path):
    doc = pymupdf.open(pdf)
    pages = doc.page_count
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    lowered = text.lower()
    if "github.com" in lowered:
        raise RuntimeError(f"github.com leaked into {pdf.name}")
    return pages, text


def main():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    failures = []
    for html in HTMLS:
        if "Resume" in html.name:
            dest = ROOT / "resumes" / "pdf" / html.with_suffix(".pdf").name
        else:
            dest = ROOT / "cover-letters" / "pdf" / html.with_suffix(".pdf").name
        print(f"print {html.name} -> {dest.name}")
        html_to_pdf(html, dest)
        pages, text = check_pdf(dest)
        print(f"  pages={pages} bytes={dest.stat().st_size} name_ok={'Atul' in text}")
        if pages != 1:
            failures.append(f"{dest.name} has {pages} pages")
        art = ARTIFACTS / dest.name
        art.write_bytes(dest.read_bytes())
    if failures:
        raise SystemExit("PAGE COUNT:\n" + "\n".join(failures))
    print("all 1-page PDFs ok")


if __name__ == "__main__":
    main()
