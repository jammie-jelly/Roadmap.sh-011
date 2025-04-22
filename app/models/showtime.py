from sqlalchemy import Column, Integer, ForeignKey, DateTime
from app.utils.database import Base

class Showtime(Base):
    __tablename__ = "showtimes"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    showtime = Column(DateTime)
