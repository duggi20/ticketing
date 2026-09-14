#!/usr/bin/env python3
"""Write batch-10 tailored one-page resume/cover HTML. Run from repo root."""
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
    <p class="skills"><b>Backend:</b> FastAPI, Ruby on Rails, RESTful APIs, microservices, Sidekiq, RabbitMQ</p>
    <p class="skills"><b>Frontend:</b> Vue.js, React.js, Next.js</p>
    <p class="skills"><b>Data:</b> MySQL, PostgreSQL, Redis, RabbitMQ, Snowflake, Airbyte CDC, dbt, SQL</p>
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

# 53 Handshake SWE I International Expansion
jobs.append(("resume", "Atul_Banyal_Resume_Handshake.html", resume(
    "Atul Banyal — Resume (Handshake Software Engineer I International Expansion Bengaluru)",
    "Software Engineer &nbsp;|&nbsp; Python · TypeScript · React.js · REST APIs · SQL",
    "Tailored for Handshake Software Engineer I, International Expansion, Bengaluru on-site. Posted 1–3+ years.",
    """Software Engineer with 2 years 2 months of production Python, TypeScript, React.js, REST APIs,
      SQL, and Docker/Kubernetes deploys. Applying for Handshake Software Engineer I, International
      Expansion (Bengaluru, on-site). Owns product APIs and UI end-to-end on live systems (1,000+ DAU),
      plus internal operator workflows on construction and tree-care products.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> 2y2m inside posted 1–3+, production systems end-to-end, Python/TS/React, REST APIs, SQL, Docker, CI/CD</p>""",
    [
        "Owned features end-to-end (requirements through production) on three live products: exchange, tree care, and construction.",
        "Built production Python FastAPI REST APIs and Vue.js UI; uses TypeScript with React.js / Next.js as professional frontend skill.",
        "Shipped Ruby on Rails REST APIs and PostgreSQL wallets on a live exchange serving 1,000+ daily users.",
        "Worked with operators on construction modules (tracking, contracts, payments, workforce, vendors) and turned process into product flows.",
        "Ran GitHub Actions CI/CD that built Docker images and deployed to Kubernetes.",
        "Wrote SQL against MySQL/PostgreSQL; followed data bugs from API to query.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Handshake.html", cover(
    "Atul Banyal — Cover Letter, Handshake Software Engineer I",
    "Mohali, Punjab · Open to Bengaluru (on-site)",
    "Software Engineer I, International Expansion, Bengaluru (Ashby 91733641)",
    "Handshake",
    [
        """I am applying for Software Engineer I, International Expansion in Bengaluru (on-site).
        You ask for 1–3+ years owning production systems end-to-end. I have 2 years 2 months of
        production Python FastAPI, TypeScript/React, REST APIs, SQL, and Docker/Kubernetes on live
        products. B.Tech CSE (AI), CGPA 7.7, 2020–2024.""",
        """I own features from requirements through production on product APIs, UI, and operator
        workflows. I am not claiming a prior player-coach or multi-contributor lead title. I will
        relocate to Bengaluru for on-site. Full-time.""",
    ],
)))

# 54 GitLab AI Engineer
jobs.append(("resume", "Atul_Banyal_Resume_GitLab_AI.html", resume(
    "Atul Banyal — Resume (GitLab AI Engineer Bangalore)",
    "Software Engineer &nbsp;|&nbsp; Python · TypeScript · REST APIs · Git · CI/CD",
    "Tailored for GitLab AI Engineer, Remote Bangalore, Greenhouse 8556658002. No numeric 3+ floor.",
    """Software Engineer with 2 years 2 months of production Python, TypeScript/JavaScript, REST APIs,
      Git, and GitHub Actions CI/CD. Applying for GitLab AI Engineer, Remote Bangalore (8556658002).
      Day-to-day production work is product APIs and deploys. Uses Cursor as an AI coding tool in the
      development workflow.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, JavaScript/TypeScript, REST APIs, Git, CI/CD, production debugging, Cursor in daily workflow</p>""",
    [
        "Built production Python FastAPI REST APIs with validation and SQL models; shipped independently from design to deploy.",
        "Uses TypeScript with React.js / Next.js as professional frontend skill; Vue.js is the production UI on tree care.",
        "Integrated third-party REST APIs (Binance/Kraken, ETH/BTC wallets) on a live exchange at 1,000+ DAU.",
        "Debugged failures from GitHub Actions CI logs through API and database errors before the next ship.",
        "Uses Cursor as an AI coding assistant in daily development (not LLM product engineering as the day job).",
        "Led a construction management Rails product with five modules: tracking, contracts, payments, workforce, vendors.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_GitLab_AI.html", cover(
    "Atul Banyal — Cover Letter, GitLab AI Engineer",
    "Mohali, Punjab · Open to Bengaluru / GitLab remote India",
    "AI Engineer, Remote Bangalore, Greenhouse 8556658002",
    "GitLab",
    [
        """I am applying for AI Engineer, Remote Bangalore (8556658002). You want solid coding in
        Python or JavaScript/TypeScript plus REST APIs. I have 2 years 2 months of production Python
        FastAPI and TypeScript/JavaScript REST work, Git, and CI/CD. B.Tech CSE (AI), CGPA 7.7.""",
        """Production work is product APIs and deploys. I use Cursor in the daily coding workflow.
        I am not presenting LLM/agent product engineering or GraphQL as my production stack. Full-time.
        Open to Bengaluru / GitLab remote India.""",
    ],
)))

# 55 Accenture Custom SWE Bengaluru Python min 2
jobs.append(("resume", "Atul_Banyal_Resume_Accenture_Python_BLR.html", resume(
    "Atul Banyal — Resume (Accenture Custom Software Engineer Python Bengaluru)",
    "Software Engineer &nbsp;|&nbsp; Python · REST APIs · SQL · React.js · Git",
    "Tailored for Accenture Custom Software Engineer ATCI-5383577-S1962511 Bengaluru. Minimum 2 years Python.",
    """Software Engineer with 2 years 2 months of production Python FastAPI REST APIs, SQL
      (MySQL/PostgreSQL), React.js, Git, and CI/CD. Applying for Accenture Custom Software Engineer,
      Bengaluru (ATCI-5383577-S1962511). Posted minimum 2 years Python. Good-to-have React.js is
      production skill. Production Python is FastAPI.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, 2y2m software development, Git, SQL, REST APIs, React.js</p>""",
    BULLETS_FS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_Accenture_Python_BLR.html", cover(
    "Atul Banyal — Cover Letter, Accenture Custom Software Engineer Bengaluru",
    "Mohali, Punjab · Open to Bengaluru (in-office)",
    "Custom Software Engineer (Python), ATCI-5383577-S1962511, Bengaluru",
    "Accenture",
    [
        """I am applying for Custom Software Engineer in Bengaluru (ATCI-5383577-S1962511). The
        posting requires a minimum of 2 years in Python and lists React.js as good-to-have. I have
        2 years 2 months of production Python FastAPI REST APIs, SQL, Git, and React.js/TypeScript.
        B.Tech CSE (AI), CGPA 7.7, 15 years of full-time education.""",
        """Production Python is FastAPI with REST APIs and SQL. I will relocate to Bengaluru.
        Full-time.""",
    ],
)))

# 56 Amazon Data Engineer I SmartCommerce
jobs.append(("resume", "Atul_Banyal_Resume_Amazon_DE.html", resume(
    "Atul Banyal — Resume (Amazon Data Engineer I SmartCommerce Bengaluru)",
    "Software Engineer &nbsp;|&nbsp; Python · SQL · Snowflake · Airbyte CDC · dbt",
    "Tailored for Amazon Data Engineer-I, SmartCommerce, 10506604 Bengaluru. Posted 1+ years data engineering.",
    """Software Engineer with 2 years 2 months of production Python, SQL, Airbyte CDC, Snowflake,
      and dbt. Applying for Amazon Data Engineer-I, SmartCommerce (10506604), Bengaluru. Built ETL-style
      pipelines that replicate operational MySQL into Snowflake and dbt marts so reporting stays off
      OLTP.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> 1+ years data/engineering, SQL, Python, ETL-style pipelines (Airbyte CDC), warehousing (Snowflake), dbt</p>""",
    [
        "Replicated operational MySQL into Snowflake with Airbyte CDC and dbt marts so reporting stayed off OLTP.",
        "Wrote production Python and SQL against MySQL/PostgreSQL; followed data bugs from API to query.",
        "Owned data quality of important operational datasets used by product and reporting.",
        "Shipped Ruby on Rails REST APIs and PostgreSQL wallets on a live exchange serving 1,000+ daily users.",
        "Ran GitHub Actions CI/CD that built Docker images and deployed to Kubernetes.",
        "Led a construction management Rails product with five modules: tracking, contracts, payments, workforce, vendors.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Amazon_DE.html", cover(
    "Atul Banyal — Cover Letter, Amazon Data Engineer I SmartCommerce",
    "Mohali, Punjab · Open to Bengaluru (in-office)",
    "Data Engineer-I, SmartCommerce, Job ID 10506604",
    "Amazon",
    [
        """I am applying for Data Engineer-I on SmartCommerce in Bengaluru (10506604). Basic
        qualifications ask for 1+ years of data engineering, SQL, ETL pipelines, and Python. I have
        2 years 2 months of production Python and SQL, plus Airbyte CDC into Snowflake and dbt marts
        off OLTP. B.Tech CSE (AI), CGPA 7.7.""",
        """Production data work is Python, SQL, Airbyte CDC, Snowflake, and dbt. I will relocate to
        Bengaluru. Full-time.""",
    ],
)))

# 57 Amazon Database Engineer I Hyderabad
jobs.append(("resume", "Atul_Banyal_Resume_Amazon_DB.html", resume(
    "Atul Banyal — Resume (Amazon Database Engineer I PESDB Hyderabad)",
    "Software Engineer &nbsp;|&nbsp; PostgreSQL · MySQL · Python · Ruby · SQL",
    "Tailored for Amazon Database Engineer-I, PESDB, 10469433 Hyderabad. Posted 1+ years RDS PostgreSQL/MySQL.",
    """Software Engineer with 2 years 2 months of production PostgreSQL, MySQL, Python, and Ruby.
      Applying for Amazon Database Engineer-I, PESDB (10469433), Hyderabad. Day-to-day work is
      schema, SQL, and persistence for live product APIs, including wallets on PostgreSQL.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> 1+ years PostgreSQL/MySQL, Python/Ruby, SQL, production support of live databases</p>""",
    [
        "Designed and operated MySQL and PostgreSQL schemas for live product APIs (tree care, construction, exchange wallets).",
        "Wrote production SQL and Python against those databases; reproduced data bugs before changing code.",
        "Shipped Ruby on Rails REST APIs and PostgreSQL wallets on a live exchange serving 1,000+ daily users.",
        "Ran GitHub Actions CI/CD that built Docker images and deployed to Kubernetes on Linux.",
        "Led a construction management Rails product with five modules: tracking, contracts, payments, workforce, vendors.",
        "Debugged persistence failures from CI logs through API and database errors.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Amazon_DB.html", cover(
    "Atul Banyal — Cover Letter, Amazon Database Engineer I PESDB",
    "Mohali, Punjab · Willing to relocate to Hyderabad",
    "Database Engineer-I, PESDB, Job ID 10469433, Hyderabad",
    "Amazon",
    [
        """I am applying for Database Engineer-I, PESDB in Hyderabad (10469433). Basic qualifications
        ask for 1+ years with RDS PostgreSQL/MySQL (or other RDBMS) and a procedural language such as
        Python or Ruby. I have 2 years 2 months of production PostgreSQL, MySQL, Python, and Ruby on
        live product APIs. B.Tech CSE (AI), CGPA 7.7.""",
        """I understand the office is Hyderabad and I will relocate. Full-time.""",
    ],
)))

# 58 Accenture Application Support Mumbai
jobs.append(("resume", "Atul_Banyal_Resume_Accenture_Support_Mumbai.html", resume(
    "Atul Banyal — Resume (Accenture Application Support Engineer Mumbai)",
    "Software Engineer &nbsp;|&nbsp; Python · Production debugging · SQL · Git",
    "Tailored for Accenture Application Support Engineer ATCI-5715393-S2063558 Mumbai. Posted 0–2 years Python. Support track.",
    """Software Engineer with 2 years 2 months of production Python, SQL, and CI-to-runtime debugging.
      Applying for Accenture Application Support Engineer, Mumbai (ATCI-5715393-S2063558). Posted 0–2
      years Python. This is an application-support seat — diagnosing issues across live systems — not
      a backend SWE req.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, production troubleshooting, SQL, Git, logs, documenting fixes</p>""",
    [
        "Debugged production FastAPI/Rails failures from GitHub Actions CI logs through API and database errors.",
        "Wrote production Python and SQL against MySQL/PostgreSQL; reproduced data bugs before changing code.",
        "Documented findings and fixes so the next engineer could rerun the same path.",
        "Ran Docker → Kubernetes deploys on Linux; followed runtime issues after ship.",
        "Shipped Ruby on Rails REST APIs and PostgreSQL wallets on a live exchange serving 1,000+ daily users.",
        "Led a construction management Rails product with five modules: tracking, contracts, payments, workforce, vendors.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Accenture_Support_Mumbai.html", cover(
    "Atul Banyal — Cover Letter, Accenture Application Support Engineer Mumbai",
    "Mohali, Punjab · Willing to relocate to Mumbai",
    "Application Support Engineer (Python), ATCI-5715393-S2063558, Mumbai",
    "Accenture",
    [
        """I am applying for Application Support Engineer in Mumbai (ATCI-5715393-S2063558). The
        posting lists 0–2 years in Python and asks for software detectives who diagnose issues in
        live systems. I have 2 years 2 months of production Python, SQL, and CI-to-runtime debugging.
        B.Tech CSE (AI), CGPA 7.7, 15 years of full-time education.""",
        """I am applying for the application-support track, not a backend SWE seat. I will relocate
        to Mumbai. Full-time.""",
    ],
)))

# 59 Deloitte DEC Executive fullstack Bengaluru
jobs.append(("resume", "Atul_Banyal_Resume_Deloitte_Fullstack.html", resume(
    "Atul Banyal — Resume (Deloitte DEC Executive Full stack Development Bengaluru)",
    "Software Engineer &nbsp;|&nbsp; Python FastAPI · TypeScript · React.js · SQL · REST",
    "Tailored for Deloitte DEC Executive Full stack Development, Bengaluru, req 107592. Posted 1–2 years.",
    """Software Engineer with 2 years 2 months of production Python FastAPI, JavaScript/TypeScript,
      SQL, REST APIs, and React.js. Applying for Deloitte Enabling Areas DEC Executive — Full stack
      Development, Bengaluru (req 107592). Posted 1–2 years. Production web stack is FastAPI +
      React/TypeScript (Vue.js on tree care).""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, JavaScript/TypeScript, SQL, REST APIs, React.js, FastAPI, AWS-adjacent Docker/K8s</p>""",
    [
        "Built production Python FastAPI REST APIs and Vue.js UI; uses TypeScript with React.js / Next.js as professional frontend skill.",
        "Wrote SQL against MySQL/PostgreSQL; integrated REST APIs across product modules.",
        "Shipped Ruby on Rails REST APIs and PostgreSQL wallets on a live exchange serving 1,000+ daily users.",
        "Ran GitHub Actions CI → Docker → Kubernetes on AWS-adjacent hosting.",
        "Led a construction management Rails product with five modules: tracking, contracts, payments, workforce, vendors.",
        "Debugged implementation and production issues from CI logs through API and SQL.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Deloitte_Fullstack.html", cover(
    "Atul Banyal — Cover Letter, Deloitte DEC Executive Full stack",
    "Mohali, Punjab · Open to Bengaluru (hybrid)",
    "Enabling Areas DEC Executive — Full stack Development, Bengaluru, req 107592",
    "Deloitte",
    [
        """I am applying for Enabling Areas — DEC — Executive — Full stack Development in Bengaluru
        (req 107592). You ask for 1–2 years plus Python, JavaScript/TypeScript, SQL, and REST, with
        React.js or FastAPI preferred. I have 2 years 2 months of production Python FastAPI, React.js /
        TypeScript, SQL, and REST APIs. B.Tech CSE (AI), CGPA 7.7.""",
        """Production backend is FastAPI (and Rails). React.js/TypeScript is professional frontend
        skill. I will relocate to Bengaluru. Full-time.""",
    ],
)))

# 60 Amazon System Development Engineer I Chennai
jobs.append(("resume", "Atul_Banyal_Resume_Amazon_SysDE.html", resume(
    "Atul Banyal — Resume (Amazon System Development Engineer I Chennai)",
    "Software Engineer &nbsp;|&nbsp; Python · Ruby · Linux · Docker · CI/CD",
    "Tailored for Amazon System Development Engineer I 10522139 Chennai. Python/Ruby/Linux. Office is Chennai.",
    """Software Engineer with 2 years 2 months of production Python, Ruby, Linux deploys (Docker/
      Kubernetes), and GitHub Actions CI/CD. Applying for Amazon System Development Engineer I
      (10522139), Chennai. Work includes software deployment support, troubleshooting live systems,
      and building tools that keep production packages shipping.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python/Ruby, Linux/Unix, automating deploy and support, CI/CD, Docker, Kubernetes</p>""",
    [
        "Ran GitHub Actions CI/CD that built Docker images and deployed to Kubernetes on Linux.",
        "Debugged production FastAPI/Rails failures from CI logs through API and runtime errors after ship.",
        "Wrote production Python and Ruby; followed tickets from staging deploys to production.",
        "Shipped Ruby on Rails REST APIs and PostgreSQL wallets on a live exchange serving 1,000+ daily users.",
        "Led a construction management Rails product with five modules: tracking, contracts, payments, workforce, vendors.",
        "Documented deploy and fix paths so the next engineer could rerun the same steps.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Amazon_SysDE.html", cover(
    "Atul Banyal — Cover Letter, Amazon System Development Engineer I",
    "Mohali, Punjab · Willing to relocate to Chennai",
    "System Development Engineer I, Job ID 10522139, Chennai",
    "Amazon",
    [
        """I am applying for System Development Engineer I in Chennai (10522139). Basic qualifications
        ask for programming in a language such as Python or Ruby, Linux/Unix, and experience automating,
        deploying, and supporting infrastructure. I have 2 years 2 months of production Python and Ruby,
        Linux Docker/Kubernetes deploys, and GitHub Actions CI/CD. B.Tech CSE (AI), CGPA 7.7.""",
        """I understand the office is Chennai and I will relocate. Full-time.""",
    ],
)))


def main():
    for kind, name, html in jobs:
        dest = (RES if kind == "resume" else COV) / name
        dest.write_text(html, encoding="utf-8")
        print("wrote", dest.relative_to(ROOT))


if __name__ == "__main__":
    main()
