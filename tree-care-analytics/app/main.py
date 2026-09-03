from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.db import engine
from app.models import Base
from app.routers import analytics, operations


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()


app = FastAPI(
    title="Tree Care Platform",
    description=(
        "Operational API on MySQL (OLTP) with analytical reads served from "
        "Snowflake (OLAP) after Airbyte CDC replication."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(operations.router)
app.include_router(analytics.router)


@app.get("/health")
def health() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "snowflake_configured": settings.snowflake_configured,
    }
