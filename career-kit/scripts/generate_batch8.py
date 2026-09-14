#!/usr/bin/env python3
"""Write batch-8 tailored one-page resume/cover HTML. Run from repo root."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "resumes"
COV = ROOT / "cover-letters"

CONTACT = """      Mohali, Punjab, India · Open to Bengaluru / remote India<br />
      +91 63518 06327 ·
      <a href="mailto:atulbanyalreal@gmail.com">atulbanyalreal@gmail.com</a> ·
      <a href="https://www.linkedin.com/in/atul-banyal-6629a2185">linkedin.com/in/atul-banyal-6629a2185</a>"""

EDU = """    <h2>Education</h2>
    <h3>B.Tech, Computer Science and Engineering (AI specialization)</h3>
    <div class="meta">
      <span>ITM SLS Baroda University, Vadodara, Gujarat · CGPA 7.7</span>
      <span>2020 – 2024</span>
    </div>"""

EXP_HEAD = """    <h2>Professional Experience</h2>
    <h3>Software Developer — Skyach Software Solutions Pvt. Ltd.</h3>
    <div class="meta">
      <span>Mohali, India</span>
      <span>June 2024 – August 2026</span>
    </div>"""

PROJECTS_STD = """    <h2>Key Projects</h2>
    <h3>Crypto Exchange — Rails, PostgreSQL, Docker, Kubernetes, GitHub Actions</h3>
    <ul>
      <li>Live exchange for 1,000+ DAU: REST APIs, wallets, Binance/Kraken integrations, CI → Docker → Kubernetes.</li>
    </ul>
    <h3>Tree Care Platform — Python FastAPI, Vue.js, MySQL, Snowflake, dbt</h3>
    <ul>
      <li>Production FastAPI REST APIs plus Vue.js UI; Airbyte CDC to Snowflake and dbt marts off OLTP.</li>
    </ul>
    <h3>Construction Management — Ruby on Rails, PostgreSQL</h3>
    <ul>
      <li>Five modules: project tracking, contracts, payments, workforce, vendor management.</li>
    </ul>"""


def resume(title, headline, tailor, summary, skills, bullets):
    lis = "\n".join(f"      <li>{b}</li>" for b in bullets)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <link rel="stylesheet" href="../css/resume.css" />
</head>
<body>
  <div class="page">
    <h1>Atul Banyal</h1>
    <p class="headline">{headline}</p>
    <p class="contact">
{CONTACT}
    </p>
    <p class="tailor-note">{tailor}</p>

    <h2>Professional Summary</h2>
    <p class="summary">
      {summary}
    </p>

    <h2>Technical Skills</h2>
{skills}

{EXP_HEAD}
    <ul>
{lis}
    </ul>

{PROJECTS_STD}

{EDU}
  </div>
</body>
</html>
"""


def cover(title, loc_line, re_line, company, body_ps):
    paras = "\n".join(f"      <p>\n        {p}\n      </p>" for p in body_ps)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <link rel="stylesheet" href="../css/cover-letter.css" />
</head>
<body>
  <div class="page">
    <div class="sender">
      <p class="name">Atul Banyal</p>
      <p class="meta">{loc_line}</p>
      <p class="meta">
        +91 63518 06327 ·
        <a href="mailto:atulbanyalreal@gmail.com">atulbanyalreal@gmail.com</a> ·
        <a href="https://www.linkedin.com/in/atul-banyal-6629a2185">linkedin.com/in/atul-banyal-6629a2185</a>
      </p>
    </div>
    <p class="date">14 September 2026</p>
    <div class="recipient">
      <p>Hiring Team</p>
      <p>{company}</p>
      <p>Re: {re_line}</p>
    </div>
    <p class="salutation">Dear {company} Hiring Team,</p>
    <div class="body">
{paras}
    </div>
    <div class="closing">
      <p>Sincerely,</p>
      <p class="sign">Atul Banyal</p>
      <p>atulbanyalreal@gmail.com · +91 63518 06327</p>
    </div>
  </div>
</body>
</html>
"""


SKILLS_CORE = """    <p class="skills"><b>Languages:</b> Python, Ruby, JavaScript, TypeScript, Shell Script</p>
    <p class="skills"><b>Backend:</b> FastAPI, Ruby on Rails, RESTful APIs, microservices, Sidekiq</p>
    <p class="skills"><b>Frontend:</b> Vue.js, React.js, Next.js</p>
    <p class="skills"><b>Data:</b> MySQL, PostgreSQL, Redis, Snowflake, Airbyte CDC, dbt, SQL</p>
    <p class="skills"><b>DevOps:</b> Docker, Kubernetes, GitHub Actions (CI/CD), Git, AWS</p>"""

BULLETS_FS = [
    "Built production Python FastAPI REST APIs and Vue.js UI for a tree care platform (listings, orders, services) with MySQL models and request validation.",
    "Shipped Ruby on Rails REST APIs and PostgreSQL wallets on a live cryptocurrency exchange serving 1,000+ daily users; integrated Ethereum/Bitcoin and Binance/Kraken APIs.",
    "Ran GitHub Actions CI/CD that built Docker images and deployed to Kubernetes.",
    "Led a construction management Rails product with five modules: tracking, contracts, payments, workforce, and vendors.",
    "Replicated operational MySQL into Snowflake with Airbyte CDC and dbt marts so reporting stayed off OLTP.",
    "Uses TypeScript with React.js / Next.js as professional frontend skill; Vue.js is the production UI on tree care.",
]

jobs = []

# 32 Barclays resume only
jobs.append(("resume", "Atul_Banyal_Resume_Barclays.html", resume(
    "Atul Banyal — Resume (Barclays Software Engineer BA4 Bengaluru)",
    "Software Engineer &nbsp;|&nbsp; React · JavaScript · REST APIs · Docker · Kubernetes · AWS",
    "Tailored for Barclays Software Engineer BA4 Bengaluru 97476073696. Analyst.",
    """Software Engineer with 2 years 2 months of production React/JavaScript, REST APIs, relational SQL,
      Docker, Kubernetes, GitHub Actions CI/CD, and AWS. Ships fullstack product APIs and UI used by
      1,000+ daily users. Applying for Barclays Software Engineer BA4, Bengaluru. Java 17, Spring Boot,
      React, JavaScript, REST, SQL, Docker, Kubernetes, and AWS.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> React, JavaScript, REST APIs, SQL, Docker, Kubernetes, AWS, Git, CI/CD</p>""",
    [
        "Built React.js / Next.js / TypeScript and Vue.js user-facing flows on production product APIs.",
        "Designed and shipped RESTful services (FastAPI and Rails) with PostgreSQL/MySQL and request validation.",
        "Shipped GitHub Actions CI/CD → Docker images → Kubernetes; used AWS-adjacent hosting and Git reviews.",
        "Wrote SQL against PostgreSQL and MySQL; followed failures from CI logs to API/runtime errors.",
        "Led a construction management Rails product (five modules: tracking, contracts, payments, workforce, vendors).",
        "Integrated third-party APIs (Binance, Kraken, Ethereum/Bitcoin wallets) on a live exchange at 1,000+ DAU.",
    ],
)))

# 33 Aiprise
jobs.append(("resume", "Atul_Banyal_Resume_Aiprise.html", resume(
    "Atul Banyal — Resume (AiPrise Software Engineer I Bangalore)",
    "Software Engineer &nbsp;|&nbsp; Python · REST APIs · PostgreSQL · Docker · CI/CD",
    "Tailored for AiPrise Software Engineer I Bangalore. Posted 0–2 years.",
    """Software Engineer with 2 years 2 months of production Python, REST APIs, PostgreSQL/MySQL,
      Docker, GitHub Actions CI/CD, and React/TypeScript. Owns features from API to deploy on live
      products (1,000+ DAU). Applying for AiPrise Software Engineer I, Bengaluru. Kafka, MongoDB,
      REST APIs, PostgreSQL/MySQL, Docker, and CI/CD.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, REST APIs, PostgreSQL, MySQL, Docker, Git, CI/CD, production debugging</p>
    <p class="skills"><b>Nice-to-have (real):</b> React, TypeScript, Kubernetes, third-party API integrations</p>""",
    BULLETS_FS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_Aiprise.html", cover(
    "Atul Banyal — Cover Letter, AiPrise Software Engineer I",
    "Mohali, Punjab · Open to Bengaluru (in-office)",
    "Software Engineer I (Bangalore), Ashby 3763c791",
    "AiPrise",
    [
        """I am applying for Software Engineer I in Bengaluru. The posting asks for 0–2 years shipping
        production systems, a backend language, REST APIs, PostgreSQL/MySQL, and Docker/CI. I have
        2 years 2 months of production Python FastAPI REST APIs, PostgreSQL and MySQL, Docker, and
        GitHub Actions CI/CD, plus React/TypeScript. B.Tech CSE (AI), CGPA 7.7, 2020–2024.""",
        """Go, Java, Node, Kafka, MongoDB, and KYC/AML/sanctions workflows are ramps. I am not claiming
        a compliance-vendor orchestration background. I will relocate to Bengaluru. Full-time.""",
    ],
)))

# 34 LG Ads
jobs.append(("resume", "Atul_Banyal_Resume_LGAds.html", resume(
    "Atul Banyal — Resume (LG Ad Solutions Software Engineer I Bangalore)",
    "Software Engineer &nbsp;|&nbsp; Python · JavaScript · MySQL · Redis · AWS · Kubernetes",
    "Tailored for LG Ad Solutions Software Engineer I Bangalore. Early career.",
    """Software Engineer with 2 years 2 months of production Python, JavaScript/TypeScript, MySQL,
      Redis, REST APIs, Docker, Kubernetes, AWS, and React. Ships APIs and UI used by 1,000+ daily
      users. Applying for LG Ad Solutions Software Engineer I, Bangalore. Scala, Spark/Databricks,
      Python, JavaScript, MySQL, Redis, AWS, and Kubernetes.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, JavaScript, MySQL, Redis, data structures, AWS, Kubernetes, Git</p>
    <p class="skills"><b>Preferred (real):</b> React.js, REST APIs, Docker, CI/CD, production data pipelines (Airbyte CDC, dbt)</p>""",
    BULLETS_FS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_LGAds.html", cover(
    "Atul Banyal — Cover Letter, LG Ad Solutions Software Engineer I",
    "Mohali, Punjab · Open to Bengaluru",
    "Software Engineer I, Bangalore, Ashby 02b11bae",
    "LG Ad Solutions",
    [
        """I am applying for Software Engineer I in Bangalore. The posting is early-career: Python or
        JavaScript, MySQL/Redis, AWS/Kubernetes curiosity, and React as a plus. I have 2 years 2
        months of production Python, JavaScript/TypeScript, MySQL, Redis, REST APIs, Docker,
        Kubernetes, AWS, and React. B.Tech CSE (AI), 2020–2024.""",
        """Scala, Spark/Databricks, and connected-TV ad serving are ramps. I will relocate to Bengaluru.
        Full-time.""",
    ],
)))

# 35 Infineon
jobs.append(("resume", "Atul_Banyal_Resume_Infineon.html", resume(
    "Atul Banyal — Resume (Infineon Young Graduate Trainee Automation Engineer)",
    "Software Engineer &nbsp;|&nbsp; Python · REST APIs · CI/CD · Docker",
    "Tailored for Infineon Young Graduate Trainee HRC1715365, Bangalore BTP. Posted 0–2 years. Temporary trainee.",
    """Software Engineer with 2 years 2 months of production Python, REST APIs, Git, Docker, and
      GitHub Actions CI/CD. Writes scripts and services, not only notebooks. Applying for Infineon
      Young Graduate Trainee — Automation Engineer (HRC1715365), Bangalore BTP. The posting is a
      temporary trainee track. Production Python, REST APIs, Git, and CI.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, software design, OOP, web/REST APIs, Git, collaboration</p>""",
    [
        "Wrote production Python (FastAPI) REST APIs with MySQL models, validation, and Vue.js integration.",
        "Automated CI with GitHub Actions: tests, Docker image builds, Kubernetes deploys for a live exchange.",
        "Used Shell Script and Git daily; debugged failed pipelines and API errors instead of stopping at merge.",
        "Designed OOP Rails and FastAPI services (crypto wallets, construction modules, tree-care orders).",
        "Integrated third-party HTTP APIs (Binance, Kraken, Ethereum/Bitcoin) with failure handling.",
        "Worked across a small product team with written updates and code review.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Infineon.html", cover(
    "Atul Banyal — Cover Letter, Infineon Young Graduate Trainee",
    "Mohali, Punjab · Open to Bengaluru BTP (on-site)",
    "Young Graduate Trainee / Automation Engineer, HRC1715365",
    "Infineon",
    [
        """I am applying for Young Graduate Trainee — Automation Engineer (HRC1715365) at Bangalore BTP.
        The posting asks for a CS degree and 0–2 years with Python scripting and software design. I have
        2 years 2 months of production Python, REST APIs, Git, and CI/CD. B.Tech CSE (AI), CGPA 7.7.""",
        """I understand this is a temporary trainee role, not a senior IC seat. Wi-Fi/IoT device validation
        and semiconductor lab tooling are ramps. I will work on-site at Bangalore BTP. Full-time.""",
    ],
)))

CANON_BULLETS = [
    "Wrote production Python (FastAPI) REST APIs with MySQL models and request validation for a tree care platform.",
    "Shipped GitHub Actions CI/CD that built Docker images and rolled them to Kubernetes for a live cryptocurrency exchange (1,000+ DAU).",
    "Debugged deploy and runtime failures on containerized services (failed pipelines, API errors, SQL) rather than handing off after merge.",
    "Integrated third-party APIs (Binance, Kraken, Ethereum/Bitcoin) with attention to correctness and failure modes.",
    "Led a construction management Rails product (five modules) in a Git-review team; comfortable with async written updates.",
    "Used Shell Script, Git, and AWS-adjacent hosting daily; open to Canonical’s twice-yearly travel for internal events.",
]

# 36 Canonical Python Engineer
jobs.append(("resume", "Atul_Banyal_Resume_Canonical_Python.html", resume(
    "Atul Banyal — Resume (Canonical Python Engineer 5143074)",
    "Software Engineer &nbsp;|&nbsp; Python · Docker · Kubernetes · Linux · CI/CD",
    "Tailored for Canonical Python Engineer 5143074. Home-based worldwide. No 3+ floor.",
    """Software Engineer with 2 years 2 months of production Python, Docker, Kubernetes, GitHub
      Actions CI/CD, and Linux-hosted services. Ships maintainable Python APIs used in production
      every day. Applying for Canonical Python Engineer (5143074), home-based worldwide.
      Production Python, Docker, Kubernetes, and CI/CD.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, Linux, Git, CI/CD, Docker, Kubernetes, REST APIs</p>""",
    CANON_BULLETS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_Canonical_Python.html", cover(
    "Atul Banyal — Cover Letter, Canonical Python Engineer",
    "Mohali, Punjab · Open to remote India (home-based worldwide)",
    "Python Engineer, 5143074",
    "Canonical",
    [
        """I am applying for Python Engineer (5143074), home-based worldwide. The posting wants designed,
        modern, maintainable Python and Linux (Debian/Ubuntu preferred). I have 2 years 2 months of
        production Python FastAPI, Docker, Kubernetes, and GitHub Actions on Linux-hosted services.
        B.Tech CSE (AI), CGPA 7.7.""",
        """Debian/Ubuntu package administration is a ramp — I am not claiming distro packaging work.
        I can travel twice a year for Canonical events. Full-time, remote from India.""",
    ],
)))

# 37 Canonical Frontend
jobs.append(("resume", "Atul_Banyal_Resume_Canonical_Frontend.html", resume(
    "Atul Banyal — Resume (Canonical Web Frontend Engineer 5150422)",
    "Software Engineer &nbsp;|&nbsp; TypeScript · React · JavaScript · CSS · REST APIs",
    "Tailored for Canonical Web Frontend Engineer 5150422. Home-based worldwide.",
    """Software Engineer with 2 years 2 months of production TypeScript, React.js, Next.js, Vue.js,
      JavaScript, and CSS against REST APIs. Ships UI used on live products. Applying for Canonical
      Web Frontend Engineer — JS, CSS, React, Flutter (5150422).""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> TypeScript, React, JavaScript, CSS, REST APIs, Git, Linux-hosted deploys</p>
    <p class="skills"><b>Also real:</b> Vue.js, Next.js, FastAPI/Rails backends that those UIs call</p>""",
    [
        "Built Vue.js dashboards wired to FastAPI REST APIs (listings, orders, services) on a production tree care product.",
        "Uses TypeScript with React.js and Next.js as professional frontend skill alongside JavaScript and CSS.",
        "Shipped GitHub Actions CI/CD → Docker → Kubernetes so frontend/API changes reached production.",
        "Wrote REST clients against PostgreSQL/MySQL-backed APIs; handled validation and error states in the UI.",
        "Led a construction management Rails product with five operational modules and Git reviews.",
        "Comfortable with async written collaboration and twice-yearly travel for team events.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Canonical_Frontend.html", cover(
    "Atul Banyal — Cover Letter, Canonical Web Frontend Engineer",
    "Mohali, Punjab · Open to remote India (home-based worldwide)",
    "Web Frontend Engineer — JS, CSS, React, Flutter, 5150422",
    "Canonical",
    [
        """I am applying for Web Frontend Engineer (5150422). The posting wants TypeScript, React or
        Flutter, and high-quality web work. I have 2 years 2 months of production Vue.js plus
        TypeScript/React.js/Next.js against REST APIs. B.Tech CSE (AI), 2020–2024.""",
        """Flutter is a ramp. I am not claiming a Flutter production app. Remote from India; travel
        twice a year is fine. Full-time.""",
    ],
)))

# 38 Canonical containers
jobs.append(("resume", "Atul_Banyal_Resume_Canonical_Containers.html", resume(
    "Atul Banyal — Resume (Canonical Python Container Images 6222476)",
    "Software Engineer &nbsp;|&nbsp; Python · Docker · Kubernetes · GitHub Actions · Linux",
    "Tailored for Canonical Software Engineer Python Container Images 6222476. Home-based APAC. No 3+ floor.",
    """Software Engineer with 2 years 2 months of production Python, Docker image builds, Kubernetes
      deploys, and GitHub Actions CI/CD. Applying for Canonical Software Engineer — Python —
      Container Images (6222476), home-based APAC. Distro package management and GitOps-as-primary
      job are not claimed as production.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, Docker, Kubernetes, GitHub Actions / CI/CD, Git, Linux</p>""",
    CANON_BULLETS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_Canonical_Containers.html", cover(
    "Atul Banyal — Cover Letter, Canonical Python Container Images",
    "Mohali, Punjab · Open to remote India (home-based APAC)",
    "Software Engineer — Python — Container Images, 6222476",
    "Canonical",
    [
        """I am applying for Software Engineer — Python — Container Images (6222476), home-based APAC.
        You want Python, Docker/Kubernetes, and CI/CD (GitHub Actions listed). That is my production
        path: GitHub Actions builds Docker images and rolls them to Kubernetes on a live exchange.
        2 years 2 months. B.Tech CSE (AI).""",
        """Publishing Ubuntu container images and GitOps-as-a-job are ramps. Remote from India. Full-time.""",
    ],
)))

# 39 Canonical App Stores
jobs.append(("resume", "Atul_Banyal_Resume_Canonical_AppStores.html", resume(
    "Atul Banyal — Resume (Canonical Software Engineer App Stores 3159992)",
    "Software Engineer &nbsp;|&nbsp; Python · REST APIs · PostgreSQL · Docker · Kubernetes",
    "Tailored for Canonical Software Engineer App Stores 3159992. Home-based worldwide.",
    """Software Engineer with 2 years 2 months of production Python REST APIs, PostgreSQL, Docker,
      and Kubernetes. Applying for Canonical Software Engineer — App Stores (3159992): public-facing
      APIs in Python for CLI and web clients.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, public REST APIs, PostgreSQL, Docker, Kubernetes, Git, CI/CD</p>""",
    CANON_BULLETS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_Canonical_AppStores.html", cover(
    "Atul Banyal — Cover Letter, Canonical App Stores",
    "Mohali, Punjab · Open to remote India (home-based worldwide)",
    "Software Engineer — App Stores, 3159992",
    "Canonical",
    [
        """I am applying for Software Engineer — App Stores (3159992). The JD asks for professional
        proficiency in public-facing APIs in Python (Golang optional). I have 2 years 2 months of
        production FastAPI and Rails REST APIs, PostgreSQL, Docker, and Kubernetes. B.Tech CSE (AI).""",
        """Golang and Snap Store product internals are ramps. Remote from India; travel 2–4 weeks a
        year is fine. Full-time.""",
    ],
)))

# 40 Canonical Solutions
jobs.append(("resume", "Atul_Banyal_Resume_Canonical_Solutions.html", resume(
    "Atul Banyal — Resume (Canonical Software Engineer Solutions Engineering 3290946)",
    "Software Engineer &nbsp;|&nbsp; Python · Docker · Kubernetes · Linux · CI/CD",
    "Tailored for Canonical Software Engineer Solutions Engineering 3290946. Home-based worldwide.",
    """Software Engineer with 2 years 2 months of production Python, Docker, Kubernetes, and Linux-
      hosted operations code (CI, deploys, follow-up). Applying for Canonical Software Engineer —
      Solutions Engineering (3290946). Production Python, Docker, Kubernetes, and Linux deploys.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, Linux, Docker, Kubernetes, Git, CI/CD, testing</p>""",
    CANON_BULLETS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_Canonical_Solutions.html", cover(
    "Atul Banyal — Cover Letter, Canonical Solutions Engineering",
    "Mohali, Punjab · Open to remote India (home-based worldwide)",
    "Software Engineer — Solutions Engineering, 3290946",
    "Canonical",
    [
        """I am applying for Software Engineer — Solutions Engineering (3290946). You want a Python
        developer who can work with Linux from services up. I have 2 years 2 months of production
        Python, Docker, Kubernetes, and GitHub Actions on Linux-hosted products. B.Tech CSE (AI).""",
        """Golang and deep kernel/networking/storage work are ramps. Remote from India. Full-time.""",
    ],
)))

# 41 Canonical Cloud Sustaining
jobs.append(("resume", "Atul_Banyal_Resume_Canonical_CloudSustaining.html", resume(
    "Atul Banyal — Resume (Canonical Cloud Sustaining Engineering 3062022)",
    "Software Engineer &nbsp;|&nbsp; Python · Kubernetes · Docker · Linux · CI/CD",
    "Tailored for Canonical Software Engineer Cloud Sustaining 3062022. Home-based worldwide.",
    """Software Engineer with 2 years 2 months of production Python, Kubernetes, Docker, and Linux
      service operations. Applying for Canonical Software Engineer, Cloud — Sustaining Engineering
      (3062022). Production Python, Docker, Kubernetes, and CI/CD.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, Kubernetes, Docker, Linux, Git, CI/CD, production debugging</p>""",
    CANON_BULLETS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_Canonical_CloudSustaining.html", cover(
    "Atul Banyal — Cover Letter, Canonical Cloud Sustaining",
    "Mohali, Punjab · Open to remote India (home-based worldwide)",
    "Software Engineer, Cloud — Sustaining Engineering, 3062022",
    "Canonical",
    [
        """I am applying for Software Engineer, Cloud — Sustaining Engineering (3062022). You want
        professional software-engineer experience plus Python and Kubernetes or other cloud tech.
        I have 2 years 2 months of production Python, Docker, Kubernetes, and CI follow-up. B.Tech
        CSE (AI).""",
        """OpenStack, gdb, C/C++, and Go are ramps. Travel up to four times a year is fine. Remote
        from India. Full-time.""",
    ],
)))

# 42 Canonical Sustaining
jobs.append(("resume", "Atul_Banyal_Resume_Canonical_Sustaining.html", resume(
    "Atul Banyal — Resume (Canonical Sustaining Engineering 3326693)",
    "Software Engineer &nbsp;|&nbsp; Python · Kubernetes · Docker · Linux · Git",
    "Tailored for Canonical Software Engineer Sustaining Engineering 3326693. Home-based worldwide.",
    """Software Engineer with 2 years 2 months of production Python on Linux, plus Docker and
      Kubernetes. Applying for Canonical Software Engineer, Sustaining Engineering (3326693).
      Production Python, Docker, Kubernetes, and CI/CD.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, Linux, Kubernetes, Docker, Git, production debugging</p>""",
    CANON_BULLETS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_Canonical_Sustaining.html", cover(
    "Atul Banyal — Cover Letter, Canonical Sustaining Engineering",
    "Mohali, Punjab · Open to remote India (home-based worldwide)",
    "Software Engineer, Sustaining Engineering, 3326693",
    "Canonical",
    [
        """I am applying for Software Engineer, Sustaining Engineering (3326693). You want professional
        software-engineer experience, Linux, and at least one of Ceph/OpenStack/Kubernetes plus one of
        Python/Go/C/C++. My production language is Python; my cloud runtime is Docker/Kubernetes.
        2 years 2 months. B.Tech CSE (AI).""",
        """Ceph, OpenStack, gdb, C, and Go are ramps. Remote from India. Full-time.""",
    ],
)))


def main():
    for kind, name, html in jobs:
        dest = (RES if kind == "resume" else COV) / name
        dest.write_text(html, encoding="utf-8")
        print("wrote", dest.relative_to(ROOT))


if __name__ == "__main__":
    main()
