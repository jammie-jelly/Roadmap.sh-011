from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime
from app.dependencies import get_db, get_admin_user
from app.schemas.showtime import ShowtimeCreate, ShowtimeUpdate, ShowtimeOut
from app.models.showtime import Showtime
from app.models.user import User
from app.models.movie import Movie

router = APIRouter(prefix="/showtimes", tags=["showtimes"])

@router.post("/", response_model=ShowtimeOut)
def create_showtime(
    showtime: ShowtimeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    movie = db.query(Movie).filter(Movie.id == showtime.movie_id).first()
    if not movie:
        raise HTTPException(status_code=400, detail="Movie id not found.")

    existing = db.query(Showtime).filter(
        Showtime.movie_id == showtime.movie_id,
        Showtime.showtime == showtime.showtime
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Showtime already exists for this movie.")

    db_showtime = Showtime(**showtime.model_dump())
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)

    return ShowtimeOut(
        id=db_showtime.id,
        showtime=db_showtime.showtime,
        movie_id=db_showtime.movie_id,
        title=movie.title
    )


@router.get("/", response_model=List[ShowtimeOut])
def get_showtimes(date: date, db: Session = Depends(get_db)):
    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())

    showtimes = (
        db.query(Showtime)
        .filter(Showtime.showtime >= start_of_day, Showtime.showtime <= end_of_day)
        .all()
    )

    movies = {movie.id: movie.title for movie in db.query(Movie).all()}

    for showtime in showtimes:
        showtime.title = movies.get(showtime.movie_id)

    return showtimes

@router.get("/{showtime_id}", response_model=ShowtimeOut)
def get_showtime(showtime_id: int, db: Session = Depends(get_db)):
    showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    movie = db.query(Movie).filter(Movie.id == showtime.movie_id).first()
    title = movie.title if movie else None

    return ShowtimeOut(
        id=showtime.id,
        showtime=showtime.showtime,
        movie_id=showtime.movie_id,
        title=title
    )

@router.put("/{showtime_id}", response_model=ShowtimeOut)
def update_showtime(
    showtime_id: int,
    showtime_update: ShowtimeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    db_showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not db_showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")

    updates = {k: v for k, v in showtime_update.model_dump().items() if v is not None}

    new_movie_id = updates.get("movie_id", db_showtime.movie_id)
    new_showtime = updates.get("showtime", db_showtime.showtime)

    existing = db.query(Showtime).filter(
        Showtime.movie_id == new_movie_id,
        Showtime.showtime == new_showtime,
        Showtime.id != showtime_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="A similar showtime already exists for this movie title.")


    for key, value in updates.items():
        setattr(db_showtime, key, value)

    db.commit()
    db.refresh(db_showtime)

    movie = db.query(Movie).filter(Movie.id == db_showtime.movie_id).first()

    return ShowtimeOut(
        id=db_showtime.id,
        showtime=db_showtime.showtime,
        movie_id=db_showtime.movie_id,
        title=movie.title if movie else None
    )


@router.delete("/{showtime_id}")
def delete_showtime(
    showtime_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)
):
    db_showtime = db.query(Showtime).filter(Showtime.id == showtime_id).first()
    if not db_showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    db.delete(db_showtime)
    db.commit()
    return {"detail": "Showtime deleted"}
