from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.dependencies import get_db, get_current_user, get_admin_user
from app.schemas.reservation import ReservationCreate, ReservationOut, SeatAvailability, ReservationReport
from app.models.reservation import Reservation
from app.models.showtime import Showtime
from app.models.user import User

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.post("/", response_model=ReservationOut)
def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    valid_seats = [f"{row}{num}" for row in "ABCDE" for num in range(1, 11)]
    if reservation.seat not in valid_seats:
        raise HTTPException(status_code=400, detail="Invalid seat")

    showtime = db.query(Showtime).filter(Showtime.id == reservation.showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    if showtime.showtime < datetime.now():
        raise HTTPException(status_code=400, detail="Cannot reserve past showtime")

    existing = db.query(Reservation).filter(
        Reservation.showtime_id == reservation.showtime_id,
        Reservation.seat == reservation.seat
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Seat already reserved")

    db_reservation = Reservation(
        user_id=current_user.id, showtime_id=reservation.showtime_id, seat=reservation.seat
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    return db_reservation

@router.get("/my-reservations", response_model=List[ReservationOut])
def get_my_reservations(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return db.query(Reservation).filter(Reservation.user_id == current_user.id).all()

@router.delete("/{reservation_id}")
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your reservation")
    showtime = db.query(Showtime).filter(Showtime.id == reservation.showtime_id).first()
    if showtime.showtime < datetime.now():
        raise HTTPException(status_code=400, detail="Cannot cancel past reservation")
    db.delete(reservation)
    db.commit()
    return {"detail": "Reservation cancelled"}

@router.get("/seats/{showtime_id}", response_model=SeatAvailability)
def get_available_seats(showtime_id: int, db: Session = Depends(get_db)):
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    all_seats = [f"{row}{num}" for row in "ABCDE" for num in range(1, 11)]  # 50 seats
    reserved_seats = [
        r.seat for r in db.query(Reservation).filter(Reservation.showtime_id == showtime_id).all()
    ]
    available_seats = [seat for seat in all_seats if seat not in reserved_seats]
    return {"showtime_id": showtime_id, "available_seats": available_seats}

@router.get("/report", response_model=ReservationReport)
def get_reservation_report(
    db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)
):
    total_reservations = db.query(Reservation).count()
    total_seats = 50  # 50 seats per showtime
    showtimes = db.query(Showtime).count()
    total_capacity = total_seats * showtimes
    capacity = (total_reservations / total_capacity * 100) if total_capacity > 0 else 0
    revenue = total_reservations * 10.0  # Assume $10 per ticket
    return {
        "total_reservations": total_reservations,
        "capacity": f"{capacity:.2f}%",
        "revenue": revenue,
    }
