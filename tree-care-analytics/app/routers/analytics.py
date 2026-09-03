import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, snowflake_client
from app.config import Settings, get_settings
from app.db import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])

REVENUE_BY_ZIP_SQL = """
select
    c.zip_code                     as zip_code,
    count(*)                       as order_count,
    sum(o.total_amount)            as total_revenue,
    avg(o.total_amount)            as avg_order_value
from orders o
join companies c on c.id = o.buyer_company_id
where o.placed_at >= dateadd(year, -5, current_date())
group by c.zip_code
order by total_revenue desc
limit 50
"""


@router.get("/revenue-by-zip")
async def revenue_by_zip(settings: Settings = Depends(get_settings)):
    started = time.perf_counter()
    try:
        rows = await snowflake_client.query(settings, REVENUE_BY_ZIP_SQL)
    except snowflake_client.SnowflakeUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {
        "source": "snowflake",
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 1),
        "rows": rows,
    }


@router.get("/revenue-by-zip-oltp")
def revenue_by_zip_from_mysql(db: Session = Depends(get_db)):
    """The same aggregate straight off MySQL, for comparison.

    Kept deliberately so you can time both against a seeded dataset and see
    why this scan is the reason the warehouse exists.
    """
    started = time.perf_counter()
    rows = (
        db.query(
            models.Company.zip_code.label("zip_code"),
            func.count().label("order_count"),
            func.sum(models.Order.total_amount).label("total_revenue"),
            func.avg(models.Order.total_amount).label("avg_order_value"),
        )
        .join(models.Company, models.Company.id == models.Order.buyer_company_id)
        .group_by(models.Company.zip_code)
        .order_by(func.sum(models.Order.total_amount).desc())
        .limit(50)
        .all()
    )

    return {
        "source": "mysql",
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 1),
        "rows": [
            {
                "zip_code": r.zip_code,
                "order_count": r.order_count,
                "total_revenue": float(r.total_revenue or 0),
                "avg_order_value": float(r.avg_order_value or 0),
            }
            for r in rows
        ],
    }
