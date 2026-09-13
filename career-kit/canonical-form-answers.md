# Canonical application boxes (paste as-is)

Use these on the Python / K8s forms (3752633 and 5703396). Type them yourself if you can — don’t run them through ChatGPT again. Don’t paste your resume in the same order as the PDF.

If a box has a low character limit, use the **short** version.

---

## 1. Describe your Python development experience

Most of my Python work is from Skyach, last two years. I built the backend for a tree care product in FastAPI — listings, orders, services. MySQL models, request validation, REST endpoints that a Vue.js screen actually calls. Not a course project. Companies use it to buy, sell, and cut trees.

I also wrote Python on the data side. We copy operational MySQL into Snowflake with Airbyte CDC and I work on the dbt models so reporting doesn’t sit on the live database. That’s ETL, not model training. I haven’t shipped Kubeflow or MLFlow at work.

The crypto exchange is mainly Rails, but I still reach for Python when a script or a small service is faster. I’m used to changing production FastAPI code, checking the API when a request comes back wrong, and not merging stuff I haven’t read.

**Short:** Two years of production FastAPI at Skyach — tree care APIs (listings/orders/services) on MySQL, plus Python around Airbyte CDC / Snowflake / dbt. Exchange work is mostly Rails; Python is the FastAPI product and scripts. No production MLOps.

---

## 2. Describe your devops, system administration, or site reliability engineering experience

I’m not a full-time SRE and I don’t maintain Ubuntu packages. What I do have is the pipeline for a live crypto exchange: GitHub Actions builds a Docker image, we deploy it, Kubernetes runs it, AWS is in that path. When CI breaks or a pod comes up and the API starts erroring, I look at the pipeline and the logs. We had 1,000+ people using that product daily, so a bad release was obvious.

Locally I run Docker so my machine isn’t lying about what we ship. Git and shell scripts every day. I have not owned Prometheus/Grafana or Debian packaging. I operate the services I help ship — failed builds, bad images, a deploy that looked green and then wasn’t.

**Short:** GitHub Actions → Docker → Kubernetes on AWS for a live exchange (1,000+ daily users). I debug failed pipelines and runtime errors. Not a Linux distro admin and not an SRE team of record.

---

## 3. Describe your software engineering qualification and experience

B.Tech CSE with an AI specialisation, ITM SLS Baroda University, 2020–2024, CGPA 7.7. Since June 2024 I’ve been a software developer at Skyach in Mohali — one company, about 2 years 2 months.

I write Rails and Python (FastAPI), REST APIs, SQL (MySQL and PostgreSQL). Three products: a crypto exchange on Openware/Rails (wallets, Binance/Kraken, Docker/Kubernetes), a construction management app with five modules (tracking, contracts, payments, workforce, vendors), and the tree care FastAPI + Vue app. The exchange is the one with real traffic.

I work over Git, code review, and I use Cursor to draft then I actually read the diff. I can work remote from India. Travelling a couple of times a year for a team meetup is fine.

**Short:** B.Tech CSE (AI), 7.7, 2020–2024. Software developer at Skyach since Jun 2024 (2y 2m). Rails + FastAPI, three products, exchange at 1,000+ DAU. Remote from India is OK.
