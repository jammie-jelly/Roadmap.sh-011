# Roadmap.sh-011

#### Requirements:
  - Docker

This is a REST api server for a movie ticketing system. Developed with FastAPI and uses Postgres for the database storage.

Most endpoints are locked behind JWT authentication. An admin user is seeded that can edit reservations, request for a summary report of the revenue/ booked tickets and much more. A regular user can access movies available, seats available for a showtime etc.


# API Documentation

An overview of the available API endpoints for authentication, user management, movies, showtimes, and reservations.

## Authentication

### Signup
- **Method**: POST
- **Endpoint**: `/auth/signup`
- **Description**: Register a new user.

### Login
- **Method**: POST
- **Endpoint**: `/auth/login`
- **Description**: Authenticate a user and return a token.

## Users

### Update User
- **Method**: PUT
- **Endpoint**: `/users/{user_id}`
- **Description**: Update user information for the specified user ID.

## Movies

### Get Movies
- **Method**: GET
- **Endpoint**: `/movies/`
- **Description**: Retrieve a list of all movies.

### Create Movie
- **Method**: POST
- **Endpoint**: `/movies/`
- **Description**: Add a new movie.

### Get Movie
- **Method**: GET
- **Endpoint**: `/movies/{movie_id}`
- **Description**: Retrieve details of a specific movie by ID.

### Update Movie
- **Method**: PUT
- **Endpoint**: `/movies/{movie_id}`
- **Description**: Update details of a specific movie by ID.

### Delete Movie
- **Method**: DELETE
- **Endpoint**: `/movies/{movie_id}`
- **Description**: Remove a specific movie by ID.

## Showtimes

### Create Showtime
- **Method**: POST
- **Endpoint**: `/showtimes/`
- **Description**: Schedule a new showtime.

### Get Showtimes
- **Method**: GET
- **Endpoint**: `/showtimes/`
- **Description**: Retrieve a list of all showtimes.

### Get Showtime
- **Method**: GET
- **Endpoint**: `/showtimes/{showtime_id}`
- **Description**: Retrieve details of a specific showtime by ID.

### Update Showtime
- **Method**: PUT
- **Endpoint**: `/showtimes/{showtime_id}`
- **Description**: Update details of a specific showtime by ID.

### Delete Showtime
- **Method**: DELETE
- **Endpoint**: `/showtimes/{showtime_id}`
- **Description**: Remove a specific showtime by ID.

## Reservations

### Create Reservation
- **Method**: POST
- **Endpoint**: `/reservations/`
- **Description**: Create a new reservation for a showtime.

### Get My Reservations
- **Method**: GET
- **Endpoint**: `/reservations/my-reservations`
- **Description**: Retrieve a list of the authenticated user's reservations.

### Cancel Reservation
- **Method**: DELETE
- **Endpoint**: `/reservations/{reservation_id}`
- **Description**: Cancel a specific reservation by ID.

### Get Available Seats
- **Method**: GET
- **Endpoint**: `/reservations/seats/{showtime_id}`
- **Description**: Retrieve available seats for a specific showtime by ID.

### Get Reservation Report
- **Method**: GET
- **Endpoint**: `/reservations/report`
- **Description**: Retrieve a report of reservations.

---


Part of this challenge: https://roadmap.sh/projects/movie-reservation-system
