from sqlalchemy import Column, Integer, String
from app.utils.database import Base

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    poster_url = Column(String)
    genre = Column(String)
    year = Column(Integer)