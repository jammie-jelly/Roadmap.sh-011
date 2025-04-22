from pydantic import BaseModel
from typing import Optional

class MovieBase(BaseModel):
    title: str
    description: str
    poster_url: str
    genre: str
    year: int

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    poster_url: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None

class MovieOut(MovieBase):
    id: int

    class Config:
        from_attributes = True
