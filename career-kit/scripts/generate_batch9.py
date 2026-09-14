#!/usr/bin/env python3
"""Write batch-9 tailored one-page resume/cover HTML. Run from repo root."""
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

# 43 Amazon SDE-1 FTC Cross Border
jobs.append(("resume", "Atul_Banyal_Resume_Amazon_FTC_CrossBorder.html", resume(
    "Atul Banyal — Resume (Amazon SDE-1 FTC Cross Border Tech Bengaluru)",
    "Software Engineer &nbsp;|&nbsp; Python · REST APIs · SQL · Docker · Kubernetes",
    "Tailored for Amazon SDE-1 FTC 10525643 Bengaluru. Posted 1+ years. Fixed-term contract.",
    """Software Engineer with 2 years 2 months of production Python, REST APIs, SQL, Docker,
      Kubernetes, and GitHub Actions CI/CD. Owns features from API to deploy on live products
      (1,000+ DAU). Applying for Amazon SDE-1 (FTC), Cross Border Tech, Bengaluru. This posting
      is a contractual / fixed-term seat — not claimed as a permanent FTE req.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> 1+ years professional software development, one production language (Python/Ruby/JS), REST APIs, SQL, Git, CI/CD</p>""",
    BULLETS_FS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_Amazon_FTC_CrossBorder.html", cover(
    "Atul Banyal — Cover Letter, Amazon SDE-1 FTC Cross Border",
    "Mohali, Punjab · Open to Bengaluru (in-office)",
    "SDE-1 (FTC), Cross Border Tech, Job ID 10525643",
    "Amazon",
    [
        """I am applying for SDE-1 (FTC) on Cross Border Tech in Bengaluru (10525643). The posting
        asks for 1+ years of non-internship professional software development and one programming
        language. I have 2 years 2 months of production Python FastAPI and Ruby on Rails REST APIs,
        SQL, Docker, Kubernetes, and GitHub Actions CI/CD. B.Tech CSE (AI), CGPA 7.7, 2020–2024.""",
        """I understand this is a contractual / fixed-term role, not a permanent SDE I req. I will
        relocate to Bengaluru. Full-time.""",
    ],
)))

# 44 Amazon FBA FTC
jobs.append(("resume", "Atul_Banyal_Resume_Amazon_FTC_FBA.html", resume(
    "Atul Banyal — Resume (Amazon SDE Fixed Term International FBA Tech Bengaluru)",
    "Software Engineer &nbsp;|&nbsp; Python · REST APIs · SQL · Docker · CI/CD",
    "Tailored for Amazon SDE FTC International FBA Tech 10492771. Posted 1+ years. Fixed-term contract.",
    """Software Engineer with 2 years 2 months of production Python, REST APIs, SQL, Docker,
      Kubernetes, and GitHub Actions CI/CD. Applying for Amazon Software Development Engineer
      (Fixed Term Contract), International FBA Tech, Bengaluru (10492771). Contractual seat —
      not claimed as a permanent FTE req.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> 1+ years professional software development, one production language, REST APIs, SQL, Git, CI/CD</p>""",
    BULLETS_FS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_Amazon_FTC_FBA.html", cover(
    "Atul Banyal — Cover Letter, Amazon SDE FTC International FBA",
    "Mohali, Punjab · Open to Bengaluru (in-office)",
    "Software Development Engineer (Fixed Term Contract), International FBA Tech, 10492771",
    "Amazon",
    [
        """I am applying for Software Development Engineer (Fixed Term Contract), International FBA
        Tech in Bengaluru (10492771). The posting asks for 1+ years of non-internship professional
        software development and one programming language. I have 2 years 2 months of production
        Python and Rails REST APIs, SQL, Docker, Kubernetes, and CI/CD. B.Tech CSE (AI), CGPA 7.7.""",
        """This is a contractual / fixed-term role, not a permanent SDE I req. I will relocate to
        Bengaluru. Full-time.""",
    ],
)))

# 45 Amazon Programmer Analyst I
jobs.append(("resume", "Atul_Banyal_Resume_Amazon_PAI.html", resume(
    "Atul Banyal — Resume (Amazon Programmer Analyst I Bengaluru)",
    "Software Engineer &nbsp;|&nbsp; Python · SQL · REST APIs · Git · AWS",
    "Tailored for Amazon Programmer Analyst I 10375986. Preferred 1+ years. Python/SQL/Git.",
    """Software Engineer with 2 years 2 months of production Python, SQL, REST APIs, Git, and
      AWS-adjacent Docker/Kubernetes deploys. Applying for Amazon Programmer Analyst I (10375986),
      Bengaluru / Hyderabad / Gurugram. Production languages are Python, Ruby, and
      JavaScript/TypeScript; SQL and Git are day-to-day.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> CS fundamentals, Python/Ruby/SQL scripting, clean code, Git, version control, documentation</p>
    <p class="skills"><b>Preferred (real):</b> 2 years 2 months software development, AWS (Docker/K8s on AWS-style hosting), troubleshooting production APIs</p>""",
    [
        "Wrote production Python and SQL against MySQL/PostgreSQL; debugged API and data issues from logs to query.",
        "Shipped Ruby on Rails REST APIs and PostgreSQL wallets on a live exchange serving 1,000+ daily users.",
        "Used Git and GitHub Actions CI/CD; documented coding details and test outcomes for assigned work.",
        "Deployed Docker images to Kubernetes on AWS-adjacent hosting; followed failures from CI to runtime.",
        "Led a construction management Rails product with five modules: tracking, contracts, payments, workforce, vendors.",
        "Uses TypeScript with React.js / Next.js as professional frontend skill; Vue.js is the production UI on tree care.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Amazon_PAI.html", cover(
    "Atul Banyal — Cover Letter, Amazon Programmer Analyst I",
    "Mohali, Punjab · Open to Bengaluru / Hyderabad",
    "Programmer Analyst I, Job ID 10375986",
    "Amazon",
    [
        """I am applying for Programmer Analyst I (10375986). Locations include Bengaluru, Hyderabad,
        and Gurugram. Preferred qualifications list 1+ year of software development plus Python/SQL
        or similar scripting. I have 2 years 2 months of production Python, SQL, REST APIs, Git, and
        CI/CD. B.Tech CSE (AI), CGPA 7.7, 2020–2024.""",
        """Preferred qualifications list Python/SQL scripting, which I use in production. I will
        relocate. Full-time.""",
    ],
)))

# 46 Accenture Mumbai React associate
jobs.append(("resume", "Atul_Banyal_Resume_Accenture_Web_Mumbai.html", resume(
    "Atul Banyal — Resume (Accenture Web Developer Associate Mumbai)",
    "Software Engineer &nbsp;|&nbsp; React.js · JavaScript · HTML/CSS · TypeScript",
    "Tailored for Accenture Web Developer Associate AIOC-S01652011 Mumbai. Posted 0–2 / 1–3 years. Office is Mumbai.",
    """Software Engineer with 2 years 2 months of production React.js, JavaScript, TypeScript,
      HTML/CSS, and REST API integration. Applying for Accenture Web Developer Associate
      (AIOC-S01652011), Mumbai. Production React.js, JavaScript, TypeScript, HTML/CSS, and REST.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> React.js, JavaScript, HTML5, CSS, problem-solving, quality, written/verbal communication</p>""",
    [
        "Built React.js / Next.js / TypeScript user-facing flows on production product APIs.",
        "Shipped Vue.js UI on a tree care platform (listings, orders, services) against FastAPI REST APIs.",
        "Wrote HTML/CSS/JavaScript for production pages; kept UI aligned with REST payloads and validation.",
        "Used Git reviews and GitHub Actions CI so frontend and API changes shipped together.",
        "Integrated third-party APIs on a live exchange at 1,000+ DAU.",
        "Led a construction management Rails product (five modules: tracking, contracts, payments, workforce, vendors).",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Accenture_Web_Mumbai.html", cover(
    "Atul Banyal — Cover Letter, Accenture Web Developer Associate Mumbai",
    "Mohali, Punjab · Willing to relocate to Mumbai",
    "Web Developer Associate, AIOC-S01652011, Mumbai",
    "Accenture",
    [
        """I am applying for Web Developer Associate in Mumbai (AIOC-S01652011). The posting lists
        0–2 years (and 1–3 years) plus React.js, HTML5, CSS, and JavaScript. I have 2 years 2 months
        of production React.js / TypeScript / JavaScript and Vue.js on live product UIs. B.Tech CSE
        (AI), CGPA 7.7, 15 years of full-time education.""",
        """I can work rotational shifts if required. I will relocate to Mumbai. Full-time.""",
    ],
)))

# 47 Accenture Pune Python
jobs.append(("resume", "Atul_Banyal_Resume_Accenture_Python_Pune.html", resume(
    "Atul Banyal — Resume (Accenture Application Developer Python Pune)",
    "Software Engineer &nbsp;|&nbsp; Python · REST APIs · SQL · Git",
    "Tailored for Accenture Application Developer ATCI-5180677-S1905710 Pune. Minimum 2 years Python. Office is Pune.",
    """Software Engineer with 2 years 2 months of production Python FastAPI REST APIs, SQL
      (MySQL/PostgreSQL), Git, and CI/CD. Applying for Accenture Application Developer,
      Pune (ATCI-5180677-S1905710). Posted minimum 2 years Python. Production Python is FastAPI.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Python, 2+ years software development, Git, SQL, REST APIs, debugging</p>
    <p class="skills"><b>Nice-to-have (real):</b> MySQL, PostgreSQL, REST APIs</p>""",
    BULLETS_FS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_Accenture_Python_Pune.html", cover(
    "Atul Banyal — Cover Letter, Accenture Application Developer Pune",
    "Mohali, Punjab · Willing to relocate to Pune",
    "Application Developer (Python), ATCI-5180677-S1905710, Pune",
    "Accenture",
    [
        """I am applying for Application Developer in Pune (ATCI-5180677-S1905710). The posting
        requires a minimum of 2 years in Python. I have 2 years 2 months of production Python
        FastAPI REST APIs, MySQL/PostgreSQL, Git, and GitHub Actions CI/CD. B.Tech CSE (AI),
        CGPA 7.7, 15 years of full-time education.""",
        """My production Python web framework is FastAPI, with REST APIs, SQL, and Git. I will
        relocate to Pune. Full-time.""",
    ],
)))

# 48 GitLab Intermediate Support
jobs.append(("resume", "Atul_Banyal_Resume_GitLab_Support.html", resume(
    "Atul Banyal — Resume (GitLab Intermediate Support Engineer Bangalore)",
    "Software Engineer &nbsp;|&nbsp; Ruby on Rails · Linux · Git · Production debugging",
    "Tailored for GitLab Intermediate Support Engineer Bangalore 8687026002. Intermediate. Support track, not backend SWE.",
    """Software Engineer with 2 years 2 months of production Ruby on Rails, PostgreSQL, Linux
      deploys (Docker/Kubernetes), Git, and CI log debugging. Applying for GitLab Intermediate
      Support Engineer, Bangalore (8687026002). This is a customer-facing Support role embedded
      with Engineering — not the Intermediate Backend SWE reqs already applied.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> Ruby on Rails, Linux, Git, production logs, REST APIs, PostgreSQL, CI/CD</p>""",
    [
        "Debugged production Rails/FastAPI failures from GitHub Actions CI logs through API and database errors.",
        "Shipped Ruby on Rails REST APIs and PostgreSQL wallets on a live exchange serving 1,000+ daily users.",
        "Ran Docker → Kubernetes deploys on Linux; followed runtime issues after ship.",
        "Wrote SQL against PostgreSQL and MySQL; reproduced data bugs before changing code.",
        "Led a construction management Rails product with five modules: tracking, contracts, payments, workforce, vendors.",
        "Documented fixes and process so the next engineer could rerun the same path.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_GitLab_Support.html", cover(
    "Atul Banyal — Cover Letter, GitLab Intermediate Support Engineer",
    "Mohali, Punjab · Open to Bengaluru / GitLab remote India",
    "Intermediate Support Engineer, Bangalore, Greenhouse 8687026002",
    "GitLab",
    [
        """I am applying for Intermediate Support Engineer in Bangalore (8687026002). You want
        engineers who debug Linux systems, logs, and the Ruby on Rails codebase and who can
        contribute merge requests. I have 2 years 2 months of production Rails, PostgreSQL, Linux
        Docker/Kubernetes deploys, and CI-to-runtime debugging. B.Tech CSE (AI), CGPA 7.7.""",
        """I am applying for the Intermediate Support Engineer track (8687026002), not the
        Intermediate Backend Engineer reqs. Full-time. Open to Bengaluru.""",
    ],
)))

# 49 Amazon SDE I L4 (permanent, 1–3 years) — test-automation-leaning JD
jobs.append(("resume", "Atul_Banyal_Resume_Amazon_SDEI_L4.html", resume(
    "Atul Banyal — Resume (Amazon Software Dev Engineer I L4 Bengaluru)",
    "Software Engineer &nbsp;|&nbsp; Python · REST APIs · SQL · Git · CI/CD",
    "Tailored for Amazon Software Dev Engineer I, L4, 10531567 Bengaluru. Posted 1 to 3 years as an SDE. Permanent.",
    """Software Engineer with 2 years 2 months of production Python, REST APIs, SQL, Git, and
      GitHub Actions CI/CD. Applying for Amazon Software Dev Engineer I, L4 (10531567), Bengaluru.
      Posted experience is 1 to 3 years as an SDE. Production work is product APIs, tests in CI,
      and deploys.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> B.Tech CSE, 2 years 2 months as an SDE (inside posted 1–3), production code, Git, CI</p>""",
    [
        "Wrote production Python FastAPI and Rails REST APIs with automated GitHub Actions checks before Docker/Kubernetes deploys.",
        "Debugged failures from CI logs through API and SQL (MySQL/PostgreSQL) so the next ship stayed green.",
        "Shipped Ruby on Rails REST APIs and PostgreSQL wallets on a live exchange serving 1,000+ daily users.",
        "Used Git reviews and documented test outcomes for assigned work.",
        "Led a construction management Rails product with five modules: tracking, contracts, payments, workforce, vendors.",
        "Uses TypeScript with React.js / Next.js as professional frontend skill; Vue.js is the production UI on tree care.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Amazon_SDEI_L4.html", cover(
    "Atul Banyal — Cover Letter, Amazon Software Dev Engineer I L4",
    "Mohali, Punjab · Open to Bengaluru (in-office)",
    "Software Dev Engineer I, L4, Job ID 10531567",
    "Amazon",
    [
        """I am applying for Software Dev Engineer I, L4 in Bengaluru (10531567). Basic qualifications
        ask for a CS/Engineering bachelor’s and 1 to 3 years as an SDE. I have B.Tech CSE (AI),
        CGPA 7.7, and 2 years 2 months of production Python FastAPI and Rails REST APIs, SQL, Git,
        and CI/CD.""",
        """I write tests in CI and debug from logs through API and SQL before ship. I will relocate
        to Bengaluru. Full-time. Permanent req — not the FTC seats.""",
    ],
)))

# 50 CUBE RegTech FastAPI (fintech-adjacent product)
jobs.append(("resume", "Atul_Banyal_Resume_Cube.html", resume(
    "Atul Banyal — Resume (CUBE Software Engineer Bangalore)",
    "Software Engineer &nbsp;|&nbsp; Python FastAPI · REST APIs · PostgreSQL · Docker",
    "Tailored for CUBE Software Engineer, Bangalore. Posted 2–3 years Python with FastAPI/Django.",
    """Software Engineer with 2 years 2 months of production Python FastAPI REST APIs, PostgreSQL,
      Docker, Kubernetes, and GitHub Actions CI/CD. Applying for CUBE Software Engineer (Bangalore).
      Posted 2–3 years Python with FastAPI, Django, or similar. Production framework is FastAPI,
      with REST APIs, PostgreSQL, Docker, and CI/CD.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> 2y2m Python FastAPI (inside 2–3), REST APIs, PostgreSQL, Docker, CI/CD, AWS</p>""",
    [
        "Built production Python FastAPI REST APIs for a tree care platform with MySQL models, validation, and Vue.js UI.",
        "Replicated operational MySQL into Snowflake with Airbyte CDC and dbt marts so reporting stayed off OLTP.",
        "Ran GitHub Actions CI/CD that built Docker images and deployed to Kubernetes.",
        "Shipped Ruby on Rails REST APIs and PostgreSQL wallets on a live exchange serving 1,000+ daily users.",
        "Wrote SQL against PostgreSQL and MySQL; followed data bugs from API to query.",
        "Led a construction management Rails product with five modules: tracking, contracts, payments, workforce, vendors.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Cube.html", cover(
    "Atul Banyal — Cover Letter, CUBE Software Engineer Bangalore",
    "Mohali, Punjab · Open to Bengaluru (in-office)",
    "Software Engineer, Bangalore (Ashby 39e748ee)",
    "CUBE",
    [
        """I am applying for Software Engineer in Bangalore. You ask for 2–3 years of Python with
        FastAPI, Django, or similar, plus REST APIs, PostgreSQL, Docker, and CI/CD. I have 2 years
        2 months of production Python FastAPI REST APIs, PostgreSQL/MySQL, Docker, Kubernetes, and
        GitHub Actions. B.Tech CSE (AI), CGPA 7.7.""",
        """Production work is Python FastAPI REST APIs, PostgreSQL/MySQL, Docker, Kubernetes, and
        CI/CD. I will relocate to Bengaluru. Full-time.""",
    ],
)))

# 51 Nanonets FDE (Indian product, on-site Bangalore)
jobs.append(("resume", "Atul_Banyal_Resume_Nanonets.html", resume(
    "Atul Banyal — Resume (Nanonets Forward Deployed Engineer Bangalore)",
    "Software Engineer &nbsp;|&nbsp; Python FastAPI · REST APIs · React.js · TypeScript",
    "Tailored for Nanonets Forward Deployed Engineer, Bangalore. Posted 2+ years SWE. On-site.",
    """Software Engineer with 2 years 2 months of production Python FastAPI REST APIs, React.js /
      TypeScript, and Docker/Kubernetes deploys. Applying for Nanonets Forward Deployed Engineer,
      Bangalore (on-site). Posted 2+ years as SWE or equivalent. Production FastAPI, React/TypeScript,
      REST APIs, and end-to-end product ownership.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> 2y2m software engineering, Python FastAPI, REST APIs, React/TypeScript, Git, CI/CD</p>""",
    [
        "Built production Python FastAPI REST APIs and Vue.js UI; uses TypeScript with React.js / Next.js as professional frontend skill.",
        "Shipped Ruby on Rails REST APIs and PostgreSQL wallets on a live exchange serving 1,000+ daily users; integrated third-party APIs.",
        "Ran GitHub Actions CI → Docker → Kubernetes; debugged from CI logs to runtime.",
        "Owned features end-to-end on three live products (exchange, tree care, construction) without a separate deployment team.",
        "Wrote SQL against MySQL/PostgreSQL; followed data bugs from API to query.",
        "Led a construction management Rails product with five modules: tracking, contracts, payments, workforce, vendors.",
    ],
)))
jobs.append(("cover", "Atul_Banyal_Cover_Nanonets.html", cover(
    "Atul Banyal — Cover Letter, Nanonets Forward Deployed Engineer",
    "Mohali, Punjab · Open to Bengaluru (on-site)",
    "Forward Deployed Engineer, Bangalore (Ashby c3715ba7)",
    "Nanonets",
    [
        """I am applying for Forward Deployed Engineer in Bangalore (on-site). You ask for 2+ years
        as a software engineer (or equivalent) plus APIs and the ability to own work end-to-end.
        I have 2 years 2 months of production Python FastAPI REST APIs, React.js/TypeScript, and
        Docker/Kubernetes deploys on live products. B.Tech CSE (AI), CGPA 7.7.""",
        """I own features end-to-end on live products (API, UI, deploy). I will relocate to Bengaluru
        for an on-site start. Full-time.""",
    ],
)))

# 52 Amazon Rewards SDE I (permanent, 1+)
jobs.append(("resume", "Atul_Banyal_Resume_Amazon_Rewards.html", resume(
    "Atul Banyal — Resume (Amazon SDE I Amazon Rewards Bengaluru)",
    "Software Engineer &nbsp;|&nbsp; Python · REST APIs · SQL · Docker · Kubernetes",
    "Tailored for Amazon Software Development Engineer I, Amazon Rewards, 10523331. Posted 1+ years. Permanent.",
    """Software Engineer with 2 years 2 months of production Python, REST APIs, SQL, Docker,
      Kubernetes, and GitHub Actions CI/CD. Applying for Amazon Software Development Engineer I,
      Amazon Rewards (10523331), Bengaluru. Posted 1+ years of non-internship professional software
      development. Permanent SDE I — not an FTC seat.""",
    SKILLS_CORE + """
    <p class="skills"><b>Must-have alignment:</b> 1+ years professional software development, one production language (Python/Ruby/JS), REST APIs, SQL, Git, CI/CD</p>""",
    BULLETS_FS,
)))
jobs.append(("cover", "Atul_Banyal_Cover_Amazon_Rewards.html", cover(
    "Atul Banyal — Cover Letter, Amazon SDE I Amazon Rewards",
    "Mohali, Punjab · Open to Bengaluru (in-office)",
    "Software Development Engineer I, Amazon Rewards, Job ID 10523331",
    "Amazon",
    [
        """I am applying for Software Development Engineer I on Amazon Rewards in Bengaluru
        (10523331). The posting asks for 1+ years of non-internship professional software
        development and one programming language. I have 2 years 2 months of production Python
        FastAPI and Rails REST APIs, SQL, Docker, Kubernetes, and CI/CD. B.Tech CSE (AI), CGPA 7.7.""",
        """This is a permanent SDE I req, not the FTC seats. I will relocate to Bengaluru. Full-time.""",
    ],
)))


def main():
    for kind, name, html in jobs:
        dest = (RES if kind == "resume" else COV) / name
        dest.write_text(html, encoding="utf-8")
        print("wrote", dest.relative_to(ROOT))


if __name__ == "__main__":
    main()
