#!/usr/bin/env python3
"""Remove ramp / gap-showcase lines from resume HTML. Run from repo root."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "resumes"

# Whole skill rows that exist only to list gaps.
SKILL_ROW = re.compile(
    r'^[ \t]*<p class="skills"><b>(?:Ramps[^<]*|Good-to-have \(ramp\)|Not yet):</b>.*?</p>\s*\n',
    re.I | re.M,
)
AI_HONEST = re.compile(
    r'(<p class="skills"><b>AI \(honest\):</b> Cursor / AI-assisted coding; B\.Tech AI specialization\.)[^<]*</p>',
    re.I,
)
AI_HONEST_SHORT = re.compile(
    r'(<p class="skills"><b>AI \(honest\):</b> Cursor / AI-assisted coding; academic AI specialization\.)[^<]*</p>',
    re.I,
)
PROD_UI = re.compile(
    r'<p class="skills"><b>Production UI:</b> React\.js, Next\.js \(Angular 2\+ is a ramp, not production\)</p>',
)
PYTHON_RAMP = re.compile(
    r'<p class="skills"><b>Python:</b> personal ML scripts \(churn scoring, demand models\) — FastAPI/Django/Flask is a ramp</p>',
)
IBM_LANG = re.compile(
    r'<p class="skills"><b>Languages in production / personal:</b> Ruby, JavaScript/TypeScript, Node\.js — not Java or Go yet</p>',
)


def clean_tailor(text: str) -> str:
    text = re.sub(r"\.? ?[^.]*\bramps?\b[^.]*\.", ".", text, flags=re.I)
    text = re.sub(r"\.? ?[^.]*\ba ramp\b[^.]*\.", ".", text, flags=re.I)
    text = re.sub(r"\.? ?[^.]*optional/ramp[^.]*\.", ".", text, flags=re.I)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r" \.", ".", text)
    text = re.sub(r"\.\.+", ".", text)
    return text.strip()


def clean_summary(html: str) -> str:
    def repl(m):
        inner = m.group(1)
        # Drop sentences whose only job is to name a gap.
        parts = re.split(r"(?<=[.])\s+", inner)
        keep = []
        for p in parts:
            low = p.lower()
            if re.search(r"\bramp", low):
                continue
            if "not claimed as" in low and "production" in low:
                continue
            if "not claiming" in low:
                continue
            if "learning edge" in low:
                continue
            if "would be a ramp" in low:
                continue
            keep.append(p)
        return f'<p class="summary">\n      {" ".join(keep).strip()}\n    </p>'

    return re.sub(
        r'<p class="summary">\s*(.*?)\s*</p>',
        repl,
        html,
        count=1,
        flags=re.S,
    )


def clean_file(path: Path) -> bool:
    orig = path.read_text(encoding="utf-8")
    html = orig
    html = SKILL_ROW.sub("", html)
    html = AI_HONEST.sub(r"\1</p>", html)
    html = AI_HONEST_SHORT.sub(r"\1</p>", html)
    html = PROD_UI.sub(
        '<p class="skills"><b>Production UI:</b> React.js, Next.js</p>', html
    )
    html = PYTHON_RAMP.sub(
        '<p class="skills"><b>Python:</b> production FastAPI REST APIs; also personal ML scripts</p>',
        html,
    )
    html = IBM_LANG.sub(
        '<p class="skills"><b>Languages:</b> Ruby, Python, JavaScript, TypeScript</p>',
        html,
    )

    def tailor_repl(m):
        return f'<p class="tailor-note">{clean_tailor(m.group(1))}</p>'

    html = re.sub(
        r'<p class="tailor-note">(.*?)</p>', tailor_repl, html, flags=re.S
    )
    html = clean_summary(html)
    # leftover "ramp" in resume body
    if re.search(r"ramp", html, re.I) and path.name != "Atul_Banyal_Resume_Master.html":
        # last-pass: strip remaining ramp clauses in tailor/summary/skills
        html = re.sub(r" — ramp", "", html)
        html = re.sub(r" / ramp", "", html)
        html = re.sub(r"\(ramp\)", "", html)
        html = re.sub(r"Ready to ramp Angular 2\+ from a component-UI\s+and Node\.js base\. ", "", html)
    if html != orig:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main():
    changed = []
    for path in sorted(RES.glob("Atul_Banyal_Resume_*.html")):
        if clean_file(path):
            changed.append(path.name)
            leftover = re.findall(r".{0,40}ramp.{0,40}", path.read_text(encoding="utf-8"), re.I)
            if leftover:
                print("LEFTOVER", path.name, leftover[:3])
    print("changed", len(changed))
    for n in changed:
        print(" ", n)


if __name__ == "__main__":
    main()
