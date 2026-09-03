"""Seed enough rows that the OLTP/OLAP difference is measurable.

Usage:
    python -m scripts.seed --companies 500 --listings 60000 --orders 150000
"""

import argparse
import random
from datetime import UTC, datetime, timedelta

from sqlalchemy import insert

from app.db import SessionLocal, engine
from app.models import (
    Base,
    Company,
    Invoice,
    Order,
    ServiceAppointment,
    TreeListing,
)

SPECIES = [
    "Oak", "Maple", "Pine", "Birch", "Cedar", "Spruce", "Teak",
    "Mahogany", "Walnut", "Ash", "Eucalyptus", "Neem",
]
SERVICES = ["trimming", "removal", "stump_grinding", "health_inspection", "planting"]
BATCH = 5_000


def chunked(rows: list[dict], size: int = BATCH):
    for i in range(0, len(rows), size):
        yield rows[i : i + size]


def bulk_insert(session, table, rows: list[dict]) -> None:
    for chunk in chunked(rows):
        session.execute(insert(table), chunk)
    session.commit()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--companies", type=int, default=500)
    parser.add_argument("--listings", type=int, default=60_000)
    parser.add_argument("--orders", type=int, default=150_000)
    parser.add_argument("--appointments", type=int, default=80_000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    Base.metadata.create_all(bind=engine)

    now = datetime.now(UTC).replace(tzinfo=None)
    five_years_days = 365 * 5

    with SessionLocal() as session:
        print(f"companies: {args.companies}")
        bulk_insert(
            session,
            Company,
            [
                {
                    "name": f"TreeCo {i:05d}",
                    "zip_code": f"{random.randint(10000, 99999)}",
                }
                for i in range(args.companies)
            ],
        )
        company_ids = [c[0] for c in session.query(Company.id).all()]

        print(f"listings: {args.listings}")
        bulk_insert(
            session,
            TreeListing,
            [
                {
                    "company_id": random.choice(company_ids),
                    "species": random.choice(SPECIES),
                    "height_m": round(random.uniform(2, 45), 2),
                    "asking_price": round(random.uniform(80, 9000), 2),
                    "status": random.choice(["available", "sold", "withdrawn"]),
                    "created_at": now - timedelta(days=random.randint(0, five_years_days)),
                }
                for _ in range(args.listings)
            ],
        )
        listing_ids = [r[0] for r in session.query(TreeListing.id).all()]

        print(f"orders: {args.orders}")
        bulk_insert(
            session,
            Order,
            [
                {
                    "listing_id": random.choice(listing_ids),
                    "buyer_company_id": random.choice(company_ids),
                    "quantity": random.randint(1, 40),
                    "total_amount": round(random.uniform(120, 65000), 2),
                    "status": random.choice(["placed", "fulfilled", "cancelled"]),
                    "placed_at": now
                    - timedelta(days=random.randint(0, five_years_days)),
                }
                for _ in range(args.orders)
            ],
        )

        print(f"appointments: {args.appointments}")
        bulk_insert(
            session,
            ServiceAppointment,
            [
                {
                    "company_id": random.choice(company_ids),
                    "service_type": random.choice(SERVICES),
                    "scheduled_for": (
                        now - timedelta(days=random.randint(0, five_years_days))
                    ).date(),
                    "crew_size": random.randint(1, 12),
                    "status": random.choice(["scheduled", "completed", "no_show"]),
                    "quoted_amount": round(random.uniform(90, 12000), 2),
                    "created_at": now
                    - timedelta(days=random.randint(0, five_years_days)),
                }
                for _ in range(args.appointments)
            ],
        )

        order_ids = [r[0] for r in session.query(Order.id).limit(args.orders).all()]
        print(f"invoices: {len(order_ids)}")
        bulk_insert(
            session,
            Invoice,
            [
                {
                    "company_id": random.choice(company_ids),
                    "order_id": oid,
                    "appointment_id": None,
                    "amount": round(random.uniform(120, 65000), 2),
                    "paid_at": None if random.random() < 0.2 else now,
                    "issued_at": now
                    - timedelta(days=random.randint(0, five_years_days)),
                }
                for oid in order_ids
            ],
        )

    print("done")


if __name__ == "__main__":
    main()
