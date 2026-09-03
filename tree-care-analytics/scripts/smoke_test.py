"""End-to-end check of the operational layer without needing MySQL.

Runs against a throwaway SQLite file so the models, routes and validation can
be exercised anywhere. The CDC and Snowflake layers still need Docker and a
Snowflake account; see the README.

Usage:
    MYSQL_URL="sqlite:///./smoke.db" python -m scripts.smoke_test
"""

import os
import pathlib
import sys

DB_PATH = pathlib.Path("./smoke.db")
os.environ.setdefault("MYSQL_URL", f"sqlite:///{DB_PATH}")

if DB_PATH.exists():
    DB_PATH.unlink()

from fastapi.testclient import TestClient  # noqa: E402

from app.db import SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Base, Company  # noqa: E402

failures: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}{f' :: {detail}' if detail and not condition else ''}")
    if not condition:
        failures.append(label)


Base.metadata.create_all(bind=engine)
with SessionLocal() as session:
    session.add_all(
        [
            Company(name="Northwood Timber", zip_code="90210"),
            Company(name="Valley Arborists", zip_code="90210"),
            Company(name="Cedar Ridge Co", zip_code="10001"),
        ]
    )
    session.commit()

with TestClient(app) as client:
    r = client.get("/health")
    check("health returns ok", r.status_code == 200 and r.json()["status"] == "ok", r.text)
    check(
        "snowflake reported unconfigured",
        r.json()["snowflake_configured"] is False,
        r.text,
    )

    r = client.post(
        "/listings",
        json={
            "company_id": 1,
            "species": "Oak",
            "height_m": "18.5",
            "asking_price": "2400.00",
        },
    )
    check("create listing -> 201", r.status_code == 201, r.text)
    listing_id = r.json().get("id") if r.status_code == 201 else None
    check("new listing is available", r.json().get("status") == "available", r.text)

    r = client.post(
        "/listings",
        json={"company_id": 999, "species": "Oak", "height_m": "5", "asking_price": "10"},
    )
    check("unknown company -> 404", r.status_code == 404, r.text)

    r = client.post(
        "/listings",
        json={"company_id": 1, "species": "X", "height_m": "-3", "asking_price": "10"},
    )
    check("invalid payload -> 422", r.status_code == 422, r.text)

    r = client.get("/listings")
    check("list listings returns the new row", r.status_code == 200 and len(r.json()) >= 1, r.text)

    r = client.post(
        "/orders",
        json={"listing_id": listing_id, "buyer_company_id": 2, "quantity": 3},
    )
    check("place order -> 201", r.status_code == 201, r.text)
    check(
        "order total = price * quantity",
        r.status_code == 201 and float(r.json()["total_amount"]) == 7200.0,
        r.text,
    )

    r = client.post(
        "/orders",
        json={"listing_id": listing_id, "buyer_company_id": 2, "quantity": 1},
    )
    check("double-selling a listing -> 409", r.status_code == 409, r.text)

    r = client.post(
        "/appointments",
        json={
            "company_id": 1,
            "service_type": "trimming",
            "scheduled_for": "2026-10-01",
            "crew_size": 4,
            "quoted_amount": "850.00",
        },
    )
    check("book appointment -> 201", r.status_code == 201, r.text)

    r = client.get("/analytics/revenue-by-zip-oltp")
    check("OLTP aggregate runs", r.status_code == 200, r.text)
    if r.status_code == 200:
        body = r.json()
        check("OLTP aggregate groups by zip", len(body["rows"]) >= 1, r.text)
        print(f"       mysql-path aggregate took {body['elapsed_ms']}ms")

    r = client.get("/analytics/revenue-by-zip")
    check(
        "Snowflake route degrades to 503 without creds",
        r.status_code == 503,
        r.text,
    )

DB_PATH.unlink(missing_ok=True)

print()
if failures:
    print(f"{len(failures)} check(s) failed: {', '.join(failures)}")
    sys.exit(1)
print("all checks passed")
