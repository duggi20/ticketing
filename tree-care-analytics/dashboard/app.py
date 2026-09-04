"""BI layer: analytics dashboard reading the dbt marts in Snowflake.

Run with:
    streamlit run dashboard/app.py

Credentials come from .streamlit/secrets.toml — see dashboard/README.md.

Every query goes through conn.query(..., ttl=...). The TTL is not a nicety: a
suspended warehouse takes seconds to resume and every statement is billed, so an
uncached dashboard that re-queries on each widget interaction is both slow and
expensive.
"""

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Tree Care Analytics", page_icon=None, layout="wide")

CACHE_TTL = "10m"


@st.cache_resource
def get_connection():
    return st.connection("snowflake")


def query(sql: str) -> pd.DataFrame:
    return get_connection().query(sql, ttl=CACHE_TTL)


st.title("Tree Care Analytics")
st.caption(
    "Served from Snowflake marts (OLAP). The operational MySQL database is not "
    "touched by anything on this page."
)

try:
    kpis = query(
        """
        select
            count(*)                as order_count,
            sum(total_revenue)      as total_revenue,
            avg(avg_order_value)    as avg_order_value,
            count(distinct zip_code) as zip_codes
        from marts.revenue_by_zip
        """
    )
except Exception as exc:  # noqa: BLE001 - surface config errors in the UI
    st.error(
        "Could not reach Snowflake. Check .streamlit/secrets.toml and that the "
        "dbt marts have been built.\n\n"
        f"{exc}"
    )
    st.stop()

row = kpis.iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Zip codes covered", f"{int(row['ZIP_CODES']):,}")
c2.metric("Orders", f"{int(row['ORDER_COUNT']):,}")
c3.metric("Total revenue", f"${float(row['TOTAL_REVENUE']):,.0f}")
c4.metric("Avg order value", f"${float(row['AVG_ORDER_VALUE']):,.0f}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Revenue by zip code")
    st.caption("Top 15 by total revenue, five-year window.")
    by_zip = query(
        """
        select zip_code, total_revenue, order_count
        from marts.revenue_by_zip
        order by total_revenue desc
        limit 15
        """
    )
    st.altair_chart(
        alt.Chart(by_zip)
        .mark_bar()
        .encode(
            x=alt.X("TOTAL_REVENUE:Q", title="Total revenue"),
            y=alt.Y("ZIP_CODE:N", sort="-x", title="Zip code"),
            tooltip=["ZIP_CODE", "TOTAL_REVENUE", "ORDER_COUNT"],
        ),
        use_container_width=True,
    )

with right:
    st.subheader("Orders over time")
    st.caption("Monthly order volume and revenue.")
    over_time = query(
        """
        select
            date_trunc('month', placed_at) as month,
            count(*)                       as order_count,
            sum(total_amount)              as revenue
        from staging.stg_orders
        where placed_at >= dateadd(year, -5, current_date())
        group by 1
        order by 1
        """
    )
    st.altair_chart(
        alt.Chart(over_time)
        .mark_line(point=False)
        .encode(
            x=alt.X("MONTH:T", title="Month"),
            y=alt.Y("REVENUE:Q", title="Revenue"),
            tooltip=["MONTH", "ORDER_COUNT", "REVENUE"],
        ),
        use_container_width=True,
    )

st.divider()
st.subheader("Service mix")
st.caption("Appointment volume and quoted value by service type.")

services = query(
    """
    select
        service_type,
        count(*)             as appointments,
        sum(quoted_amount)   as quoted_value
    from staging.stg_service_appointments
    group by service_type
    order by quoted_value desc
    """
)
st.dataframe(services, use_container_width=True, hide_index=True)

with st.expander("Why this page cannot slow down the API"):
    st.markdown(
        """
        Every query here runs on a Snowflake virtual warehouse, which is compute
        that is completely separate from the MySQL server handling order writes.
        A analyst running a five-year aggregate competes for nothing with a
        customer placing an order.

        That isolation is the entire point of replicating MySQL into Snowflake
        rather than pointing this dashboard at the production database.
        """
    )
