# Tree Care Platform — OLTP to OLAP study project

A runnable version of this architecture:

```
[User / Website] -> [FastAPI] -> [MySQL (OLTP)] -> [Airbyte CDC] -> [Snowflake (OLAP)] -> [BI / dashboards]
```

The point of the project is to build each layer yourself so the architecture is
something you have operated rather than something you have read about. Work
through the layers in order; each one has a checkpoint you should be able to
answer out loud before moving on.

**Start with [WALKTHROUGH.md](WALKTHROUGH.md)** for the full build order and the
version compatibility matrix, which was checked by resolving the requirement
files rather than by reading release notes. It covers the one hard conflict in
this stack (the 5.x Snowflake connector against dbt), the MySQL 8.4 CDC trap, and
one widely repeated compatibility claim that turns out to be false.

## Why the split exists

MySQL is row-oriented and tuned for transactions: fetch or modify a handful of
rows, identified by an index, in single-digit milliseconds. Snowflake is
column-oriented and tuned for scans: read one column across hundreds of
millions of rows and aggregate it. Each is bad at the other's job. Running a
five-year revenue rollup on the database that is also taking checkout traffic is
how you get a slow checkout, which is the entire reason this two-store pattern
is standard.

## Layer 1 — Operational (FastAPI + MySQL)

```bash
docker compose up -d                 # MySQL 8 with binlog enabled for CDC
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload        # http://127.0.0.1:8000/docs
```

Seed enough data that the comparison in Layer 3 is meaningful. A few hundred
rows will make MySQL and Snowflake look identical and teach you nothing:

```bash
python -m scripts.seed --companies 500 --listings 60000 --orders 150000
```

Verify the API without needing MySQL at all (runs on a throwaway SQLite file):

```bash
python -m scripts.smoke_test
```

What is here: SQLAlchemy models for companies, listings, orders, service
appointments and invoices (`app/models.py`); Pydantic request/response
validation (`app/schemas.py`); and the write paths in
`app/routers/operations.py`, including the conflict check that stops a listing
being sold twice.

**Checkpoint:** explain why `POST /orders` returns in milliseconds. The answer
should mention the index on the primary key, the fact that only a few rows are
touched, and that the row is written to a page rather than a scanned table.

## Layer 2 — Ingestion (Airbyte CDC)

This is the layer worth the most in an interview, because it is where things go
wrong in production. Full walkthrough in [airbyte/README.md](airbyte/README.md).

The short version: MySQL writes every committed change to a binary log so that
replicas can follow along. Airbyte's MySQL source registers as a replication
client and reads that log, which means it discovers changes without running
`SELECT` polls against your tables. That is the difference between an ingestion
tool that costs your production database nothing and one that competes with
your users for query capacity.

`docker-compose.yml` already sets `log_bin`, `binlog_format=ROW`,
`binlog_row_image=FULL`, a unique `server_id` and GTIDs, and
`mysql/init/01-cdc-user.sql` creates an `airbyte` user with `REPLICATION SLAVE`
and `REPLICATION CLIENT`. Those settings are the prerequisites; knowing why each
one is required is the actual lesson.

**Checkpoint:** explain what happens when a sync is paused for longer than
`binlog-expire-logs-seconds`. (The position Airbyte needs has been purged, so it
cannot resume incrementally and has to re-snapshot the table from scratch.)

## Layer 3 — Analytical (Snowflake)

A Snowflake trial gives you 30 days and enough credits for this project. Set
credentials in `.env`:

```
SNOWFLAKE_ACCOUNT=abc12345.us-east-1
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=TREECARE
SNOWFLAKE_SCHEMA=MARTS
```

Then compare the same aggregate against both stores:

```bash
curl localhost:8000/analytics/revenue-by-zip-oltp   # MySQL scan
curl localhost:8000/analytics/revenue-by-zip        # Snowflake
```

Both routes exist so you can time them on a seeded dataset. Run the MySQL one
with `EXPLAIN` and watch it scan; that number is the justification for the
warehouse.

`app/snowflake_client.py` connects with `snowflake-connector-python`, which is a
DB-API 2.0 driver and needs Python 3.10+. Recent 4.x releases also expose
`snowflake.connector.aio` for native asyncio if you want to move off the thread
pool. Two deliberate details in that file:

- The blocking driver runs via `asyncio.to_thread`, so a slow warehouse query
  does not block the event loop and stall unrelated requests.
- Results are cached. A suspended virtual warehouse takes seconds to resume and
  every statement is billed, so **never put an uncached Snowflake call on a
  user-facing request path.** Serve dashboards from cached or pre-aggregated
  results. This is the detail that most obviously separates people who have run
  this stack from people who have only read about it.

Modelling raw replicated tables into clean marts is dbt's job; see
[dbt/README.md](dbt/README.md). Install dbt in a **separate virtualenv** —
`dbt-snowflake` pins `certifi <2025.4.26`, which would otherwise apply to your
whole app environment.

**Checkpoint:** explain why the zip-code rollup is fast in Snowflake. The answer
is columnar storage (only the columns in the query are read), micro-partition
pruning, and compute isolation — the analyst's warehouse is not the one serving
your API.

## Layer 4 — BI (dashboards and analytics)

The layer that makes the architecture visible. Full detail in
[dashboard/README.md](dashboard/README.md).

```bash
docker compose up -d metabase          # http://localhost:3000
# or, Python-native:
streamlit run dashboard/app.py
```

`dashboard/app.py` is a working Streamlit dashboard reading the dbt marts —
revenue by zip code, monthly order trend, service mix. Metabase is the
recommended option for feeling what a BI tool is like to an analyst, and its
Snowflake driver ships in the image, so there is nothing to install.

**Checkpoint:** run a heavy dashboard query and place an order through the API at
the same time. The write still returns in milliseconds. Explain why, then do the
same against `/analytics/revenue-by-zip-oltp` and explain the difference.

## Where this leaves your resume

Once you have run all three layers, this is a project you built, and it belongs
under **Key Projects** with an honest description. At that point adding Snowflake
to the skills list is accurate, and you will be able to answer the follow-up
questions an interviewer asks about binlog retention, schema drift and warehouse
cost — which is the part that fabricated experience cannot survive.
