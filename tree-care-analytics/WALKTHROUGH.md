# End-to-end walkthrough: FastAPI to MySQL to ETL to Snowflake to BI

The whole pipeline, layer by layer, with versions that actually install together.

```
[User / Website]
      |
      v
[FastAPI]  ---writes--->  [MySQL 8.0  (OLTP)]
                                |
                                | binlog (ROW, GTID)
                                v
                          [Airbyte CDC]
                                |
                                v
                        [Snowflake (OLAP)]
                                |
                    +-----------+-----------+
                    |                       |
                    v                       v
              [dbt marts]            [Metabase / Streamlit]
                    |                       |
                    +-----------> BI dashboards
```

Read [README.md](README.md) first for why the two-store split exists. This
document is the build order and the version detail.

---

## 0. Version compatibility

Verified against package metadata in September 2026 by resolving these
requirement files with `pip install --dry-run`, not by reading release notes.
There is **one hard conflict** in this stack plus two softer constraints.

### Recommended baseline

| Component | Version | Notes |
| --- | --- | --- |
| Python | **3.12** | Safest choice. Every library here ships wheels for it. |
| MySQL | **8.0** | Not 8.4 — see the CDC warning below. |
| FastAPI | 0.115+ | |
| SQLAlchemy | 2.0.x | 2.0.52 current as of Aug 2026. |
| PyMySQL | 1.1+ | Pure-Python MySQL driver, no build step. |
| snowflake-connector-python | **4.7.x** (`>=4.2.0,<5.0.0`) | Requires Python 3.10+. |
| dbt-snowflake | 1.12.0 | Requires Python 3.10+. |
| Airbyte | via `abctl`, platform 0.58.0+ | Needed for MySQL 8.4 support. |
| Metabase | latest Docker image | No Snowflake driver install required. |

Python 3.12 rather than 3.13/3.14 because the Snowflake ecosystem's support for
the newest interpreters lands unevenly across packages, and
`snowflake-snowpark-python` (needed for Streamlit) has historically carried an
upper bound on the Python version. Check the ceiling on whichever snowpark
version you install before upgrading the interpreter.

### Hard conflict: do not install the 5.x connector

`snowflake-connector-python` 5.0.0rc1 (Aug 2026) is a public preview rebuilt on
a Rust core. It adds `snowflake.connector.aio` for native asyncio, which is
genuinely attractive for FastAPI. **Do not install it here.**

- It only installs via `pip install --pre`, so you will not get it by accident.
- `dbt-snowflake` 1.12.0 pins `snowflake-connector-python >=4.2.0,<5.0.0`.
- Snowflake's own Python libraries also declare `<5.0.0` and cannot be installed
  alongside 5.x.

Stay on 4.7.x. This project reaches asyncio by running the blocking driver in a
worker thread instead — see `app/snowflake_client.py`.

### Not a conflict: snowflake-sqlalchemy and SQLAlchemy 2.0

Widely repeated online and no longer true, so worth stating plainly.
`snowflake-sqlalchemy` 1.11.1 declares:

```
sqlalchemy>=1.4.19
snowflake-connector-python<5.0.0
```

No upper bound on SQLAlchemy, so it installs happily alongside SQLAlchemy 2.0.
Confirmed by resolving both together. The confusing part is the 2.0.0aX release
note saying "users still on SQLAlchemy 1.4 should pin to
`snowflake-sqlalchemy<2.0.0`" — that means the 1.x line supports *both* 1.4 and
2.x, and the 2.0 line drops 1.4. It does not mean 1.x requires 1.4.

This project still does not use `snowflake-sqlalchemy`, but for a design reason
rather than a packaging one: analytical queries here are hand-written SQL
aggregates, and an ORM adds nothing to a `GROUP BY` you are tuning by hand. MySQL
uses the SQLAlchemy ORM because that side is row-at-a-time CRUD, where it earns
its keep.

### Soft constraint: dbt drags certifi backwards

`requirements.txt` and `requirements-dbt.txt` **do** resolve together — verified.
But `dbt-snowflake` pins `certifi <2025.4.26`, so a combined install pulls
certifi down to 2025.1.31 for the whole environment, web app included. Pinning a
year-old CA bundle across your API to satisfy a transform tool is a poor trade,
and the constraint will get more awkward as dbt's pins age.

So: separate virtualenvs, because of dependency *pressure* rather than outright
breakage.

```bash
python -m venv .venv        && .venv/bin/pip install -r requirements.txt
python -m venv .venv-dbt    && .venv-dbt/bin/pip install -r requirements-dbt.txt
```

### The MySQL 8.4 CDC warning

MySQL 8.4 **removed `SHOW MASTER STATUS`**, replacing it with
`SHOW BINARY LOG STATUS`. Debezium (which Airbyte's MySQL source uses under the
hood) probes for the binlog position at startup, and older versions fall back to
the removed command, failing with a confusing SQL syntax error:

```
java.sql.SQLSyntaxErrorException: You have an error in your SQL syntax;
... near 'MASTER STATUS' at line 1
```

`docker-compose.yml` pins `mysql:8.0` to sidestep this entirely. If you do move
to 8.4, you need a current Airbyte platform (0.58.0+) and a Debezium build that
resolves the statement by server version.

---

## 1. Operational layer: FastAPI + MySQL

```bash
docker compose up -d mysql
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Port 8001 because Airbyte's UI claims 8000.

Seed enough data that the comparison at the end is real. A few hundred rows will
make MySQL and Snowflake look identical and teach you nothing:

```bash
python -m scripts.seed --companies 500 --listings 60000 --orders 150000
```

Sanity check the API without MySQL or Snowflake (runs on a temp SQLite file):

```bash
python -m scripts.smoke_test
```

Time the aggregate on MySQL now, and keep the number:

```bash
curl -s localhost:8001/analytics/revenue-by-zip-oltp | python -m json.tool | head
```

Then look at why it is slow:

```sql
EXPLAIN SELECT c.zip_code, COUNT(*), SUM(o.total_amount)
FROM orders o JOIN companies c ON c.id = o.buyer_company_id
GROUP BY c.zip_code;
```

You are looking for a full scan over `orders`. That scan, running on the same
server taking checkout traffic, is the entire justification for everything below.

**Checkpoint:** explain why `POST /orders` returns in milliseconds while the
aggregate above does not.

---

## 2. Ingestion layer: Airbyte CDC

Full detail and the failure exercises are in [airbyte/README.md](airbyte/README.md).
Build order:

```bash
curl -LsfS https://get.airbyte.com | bash -
abctl local install            # UI at http://localhost:8000
```

Confirm the MySQL prerequisites are live before configuring anything:

```sql
SHOW VARIABLES LIKE 'log_bin';                     -- ON
SHOW VARIABLES LIKE 'binlog_format';               -- ROW
SHOW VARIABLES LIKE 'binlog_row_image';            -- FULL
SHOW VARIABLES LIKE 'gtid_mode';                   -- ON
SHOW BINARY LOGS;
```

All of these are already set by `docker-compose.yml`, and
`mysql/init/01-cdc-user.sql` creates the `airbyte` user with `REPLICATION SLAVE`
and `REPLICATION CLIENT`. Knowing *why* each is required is the lesson.

Source config: host `host.docker.internal`, port `3307`, database `treecare`,
user `airbyte`, replication method **Read Changes using Binary Log (CDC)**.

Destination config: Snowflake, landing in `TREECARE.RAW`, schedule every 15–60
minutes.

**Checkpoint:** explain what happens when a sync is paused longer than
`binlog-expire-logs-seconds`. Then actually cause it — exercise 4 in the Airbyte
guide.

---

## 3. Analytical layer: Snowflake

A trial account gives 30 days and enough credits for this project. Create the
objects first:

```sql
CREATE DATABASE IF NOT EXISTS TREECARE;
CREATE SCHEMA IF NOT EXISTS TREECARE.RAW;
CREATE SCHEMA IF NOT EXISTS TREECARE.MARTS;

CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
  WAREHOUSE_SIZE = XSMALL
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;
```

`AUTO_SUSPEND = 60` is what stops a trial account burning its credits on an idle
warehouse. Set it before you do anything else.

Point the app at Snowflake via `.env`:

```
SNOWFLAKE_ACCOUNT=abc12345.us-east-1
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=TREECARE
SNOWFLAKE_SCHEMA=MARTS
```

Snowflake has been moving away from single-factor password auth. Key-pair auth is
preferred for anything long-lived, including the Airbyte service user.

Now run the same aggregate against both stores and compare:

```bash
curl -s localhost:8001/analytics/revenue-by-zip-oltp   # MySQL
curl -s localhost:8001/analytics/revenue-by-zip        # Snowflake
```

Two deliberate details in `app/snowflake_client.py` worth understanding, because
they are what an interviewer will probe:

1. The blocking driver runs via `asyncio.to_thread`, so a slow warehouse query
   does not block the event loop and stall unrelated requests.
2. Results are cached. A suspended warehouse takes seconds to resume and every
   statement is billed, so **an uncached Snowflake call must never sit on a
   user-facing request path.**

**Checkpoint:** explain why the rollup is fast here. Columnar storage reads only
the queried columns, micro-partition pruning skips irrelevant data, and the
analyst's warehouse is not the one serving your API.

---

## 4. Transform layer: dbt

Separate virtualenv, per the certifi note in section 0.

```bash
python -m venv .venv-dbt && source .venv-dbt/bin/activate
pip install -r requirements-dbt.txt
dbt init treecare_analytics
```

Airbyte lands raw tables mirroring MySQL plus its own metadata columns
(`_airbyte_extracted_at` and friends). You do not want dashboards querying those
directly. Model them:

```
RAW (Airbyte lands here) -> STAGING (clean, typed) -> MARTS (aggregated, BI reads this)
```

Model SQL and tests are in [dbt/README.md](dbt/README.md). Run with `dbt build`,
which executes models and their tests together.

**Checkpoint:** explain why the API should read `MARTS.revenue_by_zip` rather
than aggregating `RAW.orders` on demand — query cost, warehouse resume latency,
and turning a five-year scan into a small cheap read.

---

## 5. BI layer: dashboards and analytics

Two options. They serve different purposes and it is worth doing both.

### Metabase (recommended for the BI experience)

Already wired into `docker-compose.yml`:

```bash
docker compose up -d metabase     # http://localhost:3000
```

Metabase needs **no driver installation** for Snowflake, which is why it is the
quickest of the three to get running — the driver ships in the image and you
configure it entirely through the admin UI.

Connect via **Admin > Databases > Add a database > Snowflake**, supplying:

- Account identifier including region, e.g. `az12345.ca-central-1.aws`
- Warehouse `COMPUTE_WH`, database `TREECARE`, schema `MARTS`

Point it at `MARTS`, not `RAW`. Then build a dashboard: revenue by zip code,
orders over time, service type breakdown, average order value by company. This
is the layer where the whole architecture pays off — an analyst dragging fields
around cannot slow down your checkout endpoint, because they are on a different
compute cluster entirely.

### Streamlit (Python-native, in this repo)

`dashboard/app.py` is a working analytics dashboard reading the dbt marts:

```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

It uses `st.connection("snowflake")`, which reads credentials from
`.streamlit/secrets.toml` and gives you `conn.query(sql, ttl=...)` with caching
built in. `ttl` matters for the same cost reason as above.

Version note: `st.connection("snowflake")` wants `snowflake-snowpark-python`
present, and snowpark has historically carried an upper bound on the Python
version. If installation fights you on Python 3.13+, that is the cause. Another
reason for the 3.12 baseline.

### Superset, if you want it

Superset needs the SQLAlchemy dialect added to its image:

```bash
echo "snowflake-sqlalchemy" >> ./docker/requirements-local.txt
```

Connection string:

```
snowflake://{user}:{password}@{account}.{region}/{database}?role={role}&warehouse={warehouse}
```

Run it in its own container, as its dependency tree is large and unrelated to
your app's — not because the dialect itself would conflict.

---

## What to be able to explain at the end

The pipeline is only worth putting on a CV if you can answer these without notes:

1. Why two databases instead of one, in terms of row versus columnar storage.
2. What the binlog is, why `ROW` format is required, and why CDC costs the source
   database far less than polling.
3. What happens when the binlog position a sync needs has been purged.
4. Why a query-based pipeline cannot capture deletes.
5. Why an uncached Snowflake query has no business on a user-facing endpoint.
6. Why BI reads dbt marts rather than the raw replicated tables.
