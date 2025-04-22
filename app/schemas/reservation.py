from pydantic import BaseModel
from typing import List

class ReservationCreate(BaseModel):
    showtime_id: int
    seat: str

class ReservationOut(BaseModel):
    id: int
    user_id: int
    showtime_id: int
    seat: str

    class Config:
        from_attributes = True

class ReservationReport(BaseModel):
    total_reservations: int
    capacity: str
    revenue: float

class SeatAvailability(BaseModel):
    showtime_id: int
    available_seats: List[str]
