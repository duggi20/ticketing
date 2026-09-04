from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    Date,
    ForeignKey,
    Index,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    zip_code: Mapped[str] = mapped_column(String(12), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    listings: Mapped[list["TreeListing"]] = relationship(back_populates="company")


class TreeListing(Base):
    __tablename__ = "tree_listings"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    species: Mapped[str] = mapped_column(String(80), index=True)
    height_m: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    asking_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(String(24), default="available", index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    company: Mapped[Company] = relationship(back_populates="listings")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("tree_listings.id"), index=True)
    buyer_company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"), index=True
    )
    quantity: Mapped[int] = mapped_column(default=1)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(String(24), default="placed", index=True)
    placed_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, index=True
    )

    __table_args__ = (Index("ix_orders_status_placed_at", "status", "placed_at"),)


class ServiceAppointment(Base):
    __tablename__ = "service_appointments"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    service_type: Mapped[str] = mapped_column(String(40), index=True)
    scheduled_for: Mapped[date] = mapped_column(Date, index=True)
    crew_size: Mapped[int] = mapped_column(default=2)
    status: Mapped[str] = mapped_column(String(24), default="scheduled", index=True)
    quoted_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    order_id: Mapped[int | None] = mapped_column(
        ForeignKey("orders.id"), nullable=True, index=True
    )
    appointment_id: Mapped[int | None] = mapped_column(
        ForeignKey("service_appointments.id"), nullable=True, index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    issued_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, index=True
    )
