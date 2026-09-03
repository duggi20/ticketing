from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db

router = APIRouter(tags=["operations"])


@router.post(
    "/listings", response_model=schemas.ListingOut, status_code=status.HTTP_201_CREATED
)
def create_listing(payload: schemas.ListingCreate, db: Session = Depends(get_db)):
    if db.get(models.Company, payload.company_id) is None:
        raise HTTPException(status_code=404, detail="company not found")

    listing = models.TreeListing(**payload.model_dump())
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


@router.get("/listings", response_model=list[schemas.ListingOut])
def list_listings(
    species: str | None = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    query = db.query(models.TreeListing).filter(
        models.TreeListing.status == "available"
    )
    if species:
        query = query.filter(models.TreeListing.species == species)
    return query.order_by(models.TreeListing.id.desc()).limit(min(limit, 200)).all()


@router.post(
    "/orders", response_model=schemas.OrderOut, status_code=status.HTTP_201_CREATED
)
def place_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    listing = db.get(models.TreeListing, payload.listing_id)
    if listing is None:
        raise HTTPException(status_code=404, detail="listing not found")
    if listing.status != "available":
        raise HTTPException(status_code=409, detail="listing is not available")

    order = models.Order(
        listing_id=listing.id,
        buyer_company_id=payload.buyer_company_id,
        quantity=payload.quantity,
        total_amount=listing.asking_price * payload.quantity,
    )
    listing.status = "sold"
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.post(
    "/appointments",
    response_model=schemas.AppointmentOut,
    status_code=status.HTTP_201_CREATED,
)
def book_appointment(
    payload: schemas.AppointmentCreate, db: Session = Depends(get_db)
):
    appointment = models.ServiceAppointment(**payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
