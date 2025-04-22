from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_admin_user
from app.schemas.movie import MovieCreate, MovieUpdate, MovieOut
from app.models.movie import Movie
from app.models.user import User

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("/", response_model=MovieOut)
def create_movie(
    movie: MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)
):
    db_movie = Movie(**dict(movie))
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.get("/", response_model=List[MovieOut])
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.put("/{movie_id}", response_model=MovieOut)
def update_movie(
    movie_id: int,
    movie_update: MovieUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in {k: v for k, v in movie_update.model_dump().items() if v is not None}.items():
        setattr(db_movie, key, value)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.delete("/{movie_id}")
def delete_movie(
    movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)
):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(db_movie)
    db.commit()
    return {"detail": "Movie deleted"}
