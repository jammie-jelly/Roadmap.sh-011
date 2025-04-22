from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, movies, showtimes, reservations
from app.seed import seed_db

# Create database tables and seed data on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_db()
    yield

app = FastAPI(title="Movie Reservation Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(movies.router)
app.include_router(showtimes.router)
app.include_router(reservations.router)

@app.get("/")
def read_root():
    return {"message": "Movie Reservation Service"}
