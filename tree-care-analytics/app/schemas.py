from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ListingCreate(BaseModel):
    company_id: int
    species: str = Field(min_length=2, max_length=80)
    height_m: Decimal = Field(gt=0, le=120)
    asking_price: Decimal = Field(gt=0)


class ListingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    species: str
    height_m: Decimal
    asking_price: Decimal
    status: str
    created_at: datetime


class OrderCreate(BaseModel):
    listing_id: int
    buyer_company_id: int
    quantity: int = Field(default=1, ge=1, le=500)


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    listing_id: int
    buyer_company_id: int
    quantity: int
    total_amount: Decimal
    status: str
    placed_at: datetime


class AppointmentCreate(BaseModel):
    company_id: int
    service_type: str = Field(max_length=40)
    scheduled_for: date
    crew_size: int = Field(default=2, ge=1, le=20)
    quoted_amount: Decimal = Field(gt=0)


class AppointmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    service_type: str
    scheduled_for: date
    crew_size: int
    status: str
    quoted_amount: Decimal


class RevenueByZip(BaseModel):
    zip_code: str
    order_count: int
    total_revenue: Decimal
    avg_order_value: Decimal
