# Layer 3b — dbt: shaping raw replicated tables into marts

Airbyte lands raw tables that mirror MySQL, plus its own metadata columns
(`_airbyte_extracted_at` and similar). You do not want dashboards or API
endpoints querying those directly: the shape is dictated by the operational
schema, and it changes when the application changes.

dbt is the transform step. It is the `T` in ELT, and it is what real teams run
between the raw landing schema and BI. It is SQL plus templating, version
control and tests.

```
RAW (Airbyte lands here) -> STAGING (clean, renamed, typed) -> MARTS (aggregated, BI reads this)
```

## Setup

```bash
pip install dbt-snowflake
dbt init treecare_analytics
```

Point the profile at `TREECARE`, warehouse `COMPUTE_WH`, and target schema
`MARTS`.

## Layers to build

**Staging** — one model per source table. Rename columns to business language,
cast types, drop Airbyte metadata, filter soft-deleted rows. One-to-one with
source, no joins, no aggregation.

```sql
-- models/staging/stg_orders.sql
select
    id                as order_id,
    listing_id,
    buyer_company_id  as buyer_id,
    quantity,
    total_amount,
    status,
    placed_at
from {{ source('raw', 'orders') }}
where status != 'cancelled'
```

**Marts** — the aggregates BI actually reads. This is the same rollup that
`app/routers/analytics.py` queries, but precomputed and materialised as a table
so the API is reading a small result rather than scanning five years of orders
on every request.

```sql
-- models/marts/revenue_by_zip.sql
{{ config(materialized='table') }}

select
    c.zip_code,
    count(*)            as order_count,
    sum(o.total_amount) as total_revenue,
    avg(o.total_amount) as avg_order_value
from {{ ref('stg_orders') }} o
join {{ ref('stg_companies') }} c on c.company_id = o.buyer_id
where o.placed_at >= dateadd(year, -5, current_date())
group by c.zip_code
```

## Tests

The reason to use dbt rather than a pile of SQL scripts:

```yaml
# models/marts/schema.yml
models:
  - name: revenue_by_zip
    columns:
      - name: zip_code
        tests: [unique, not_null]
      - name: total_revenue
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
```

Run with `dbt build`, which executes models and their tests together.

## Checkpoint

Explain why the API should read `MARTS.revenue_by_zip` rather than aggregating
`RAW.orders` on demand. The answer covers query cost, warehouse resume latency,
and the fact that a materialised mart turns a five-year scan into a small
indexed-style read that is cheap to serve repeatedly.
