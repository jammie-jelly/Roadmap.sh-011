from sqlalchemy import Column, Integer, ForeignKey, String
from app.utils.database import Base

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    showtime_id = Column(Integer, ForeignKey("showtimes.id"))
    seat = Column(String)
