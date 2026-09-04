# Layer 5 — BI: dashboards and analytics

Two ways to do this layer. Do both if you can: Metabase teaches you what a BI
tool feels like to an analyst, Streamlit teaches you how the warehouse is
queried from Python.

## Option A — Streamlit (this directory)

```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

Credentials go in `.streamlit/secrets.toml` at the repo root:

```toml
[connections.snowflake]
account = "abc12345.us-east-1"
user = "..."
password = "..."
warehouse = "COMPUTE_WH"
database = "TREECARE"
schema = "MARTS"
role = "..."
```

`app.py` reads the dbt marts and renders revenue by zip code, monthly order
trend, and service mix. Every query uses `conn.query(sql, ttl="10m")` — the TTL
is load-bearing, because a suspended warehouse takes seconds to resume and each
statement is billed. An uncached dashboard that re-queries on every widget
interaction is both slow and expensive.

Note that Snowflake returns column names uppercased, which is why the code reads
`row["TOTAL_REVENUE"]` rather than lowercase.

## Option B — Metabase (in docker-compose)

```bash
docker compose up -d metabase      # http://localhost:3000
```

Metabase needs **no Snowflake driver installation** — the driver ships in the
image and you configure everything through the admin UI, which makes it the
fastest of the options to get a real dashboard on screen.

Connect through **Admin > Databases > Add a database > Snowflake**:

| Field | Value |
| --- | --- |
| Account identifier | includes region, e.g. `az12345.ca-central-1.aws` |
| Warehouse | `COMPUTE_WH` |
| Database | `TREECARE` |
| Schema | `MARTS` |

Point it at `MARTS`, never `RAW`. Raw tables carry Airbyte metadata columns and
change shape whenever the application schema changes.

Dashboards worth building, because they exercise different query shapes:

1. Revenue by zip code, five-year window (large aggregate scan)
2. Monthly order volume trend (time-series rollup)
3. Service type breakdown (low-cardinality group-by)
4. Average order value by company, top 20 (join plus sort)

## The point of this layer

Run one of the heavier dashboards and, while it executes, place an order through
the FastAPI endpoint. The write returns in milliseconds regardless. That is the
whole architecture justifying itself: analytical compute and transactional
compute are physically different machines, so analysts cannot slow down
customers.

Try the same thing against `/analytics/revenue-by-zip-oltp`, which aggregates
directly on MySQL, and watch the difference.
