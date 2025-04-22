from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ShowtimeCreate(BaseModel):
    movie_id: int
    showtime: datetime

class ShowtimeUpdate(BaseModel):
    movie_id: Optional[int] = None
    showtime: Optional[datetime] = None

class ShowtimeOut(BaseModel):
    id: int
    movie_id: int
    showtime: datetime
    title: Optional[str] = None

    class Config:
        from_attributes = True
