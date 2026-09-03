# Layer 2 — Airbyte CDC from MySQL to Snowflake

## Why Airbyte and not the alternatives

| Tool | Mechanism | Why not / why yes |
| --- | --- | --- |
| **Airbyte** | Log-based CDC via Debezium, reads the MySQL binlog | Open source, runs locally in Docker, real CDC. Pick this. |
| Fivetran | Managed log-based CDC | Same architecture, but SaaS with limited free usage. Hard to practice on. |
| Airflow | Scheduled Python tasks | Excellent orchestrator, but a DAG that runs `SELECT ... WHERE updated_at > ?` is batch polling, not CDC. You would still need Debezium underneath for log-based capture. |

Airbyte is the recommendation because you can install it, break it, and fix it.
That is what makes the knowledge yours.

## How log-based CDC actually works

MySQL appends every committed change to a binary log so replicas can replay it.
With `binlog_format=ROW`, the log contains the before and after image of each
changed row rather than the SQL statement, which makes it unambiguous to replay.

Airbyte's MySQL source connects as a replication client and reads that stream.
Two consequences worth understanding:

1. **It costs MySQL almost nothing.** The server is writing the binlog anyway for
   durability and replication. Reading it does not run queries against your
   tables, so it does not compete with production traffic for buffer pool or CPU.
   A polling pipeline would.
2. **It captures deletes.** A query-based pipeline comparing `updated_at` cannot
   see a row that no longer exists. The binlog has an explicit delete event.

The first sync is a full snapshot of existing rows, after which Airbyte stores
the binlog coordinate (or GTID) it reached and resumes incrementally from there.

## Setup

Start MySQL with the settings already configured in `docker-compose.yml`:

```bash
docker compose up -d
```

Confirm the prerequisites are live:

```sql
SHOW VARIABLES LIKE 'log_bin';                     -- ON
SHOW VARIABLES LIKE 'binlog_format';               -- ROW
SHOW VARIABLES LIKE 'binlog_row_image';            -- FULL
SHOW VARIABLES LIKE 'binlog_expire_logs_seconds';  -- 604800
SHOW BINARY LOGS;
```

Install Airbyte locally:

```bash
curl -LsSf https://get.airbyte.com | bash -   # installs abctl
abctl local install                            # UI at http://localhost:8000
```

Airbyte's UI and this API both default to port 8000. Run the API on another port
while you work on this layer: `uvicorn app.main:app --port 8001`.

### Source: MySQL

- Host `host.docker.internal` (Airbyte runs in its own container), port `3307`
- Database `treecare`, username `airbyte`, password `airbytepw`
- Replication method: **Read Changes using Binary Log (CDC)**
- Select all five tables; sync mode `Incremental | Append + Deduped`

### Destination: Snowflake

Create the landing objects first:

```sql
CREATE DATABASE IF NOT EXISTS TREECARE;
CREATE SCHEMA IF NOT EXISTS TREECARE.RAW;
CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
  WAREHOUSE_SIZE = XSMALL
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;
```

`AUTO_SUSPEND` is the setting that keeps a trial account from burning its
credits on an idle warehouse. Point the destination at `TREECARE.RAW` and set
the sync schedule to every 15–60 minutes.

Snowflake has been moving away from single-factor password auth, so prefer
key-pair authentication for the Airbyte service user if the option is offered.

## Exercises — this is the part that teaches you

Do not stop once one sync succeeds. Deliberately break it:

1. **Watch an update propagate.** `UPDATE orders SET status='fulfilled' WHERE id=1;`
   then trigger a sync and confirm the change lands in Snowflake.
2. **Watch a delete propagate.** Delete a row and confirm it is reflected. Ask
   yourself how a polling pipeline would have missed this.
3. **Cause schema drift.** `ALTER TABLE orders ADD COLUMN discount DECIMAL(8,2);`
   Sync again and observe how the new column is handled and whether the
   connection needs its schema refreshed.
4. **Expire the binlog.** Stop the connection, run `FLUSH BINARY LOGS;` and
   `PURGE BINARY LOGS BEFORE NOW();`, then resume. The sync should fail to
   continue incrementally and fall back to a full re-snapshot. Understanding
   this failure is the single most useful thing in this layer.
5. **Measure the load.** Run `SHOW PROCESSLIST` during a sync and note that the
   CDC connection is a replication client, not a query hammering your tables.

## Checkpoint

You should be able to explain, without notes: what the binlog is, why
`ROW` format matters, why CDC is cheaper than polling, what a GTID is for, and
what happens when the binlog position you need has been purged.
