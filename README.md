# TaskFlow Backend API

TaskFlow is a backend API built with FastAPI and PostgreSQL.  
It implements JWT-based authentication and follows a clean, layered project structure.

This project was developed to practice real-world backend architecture, authentication flows, and database integration.

---

## Features

- User registration (`POST /auth/register`)
- User login with JWT authentication (`POST /auth/login`)
- Protected endpoint example (`GET /users/me`)
- Password hashing (no plaintext passwords stored)
- PostgreSQL database
- Alembic migrations
- Docker-based database setup
- Clean project structure (api / db / schemas / services)

---

## Tech Stack

- Python 3.12
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- Alembic
- JWT (HS256)
- Docker

---

## Project Structure

```text
taskflow/
  app/
    api/          # API routers (auth, users)
    db/           # database models, session, dependencies
    schemas/      # request & response models (Pydantic)
    services/     # password hashing & JWT logic
    main.py       # FastAPI application entry point
  alembic/        # database migrations
  docker-compose.yml
  alembic.ini
```

---

## Getting Started

### 1) Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Start PostgreSQL (Docker)

```bash
docker compose up -d
```

### 4) Run database migrations

```bash
alembic upgrade head
```

### 5) Start the server

```bash
uvicorn app.main:app --reload
```

API will be available at:

- http://127.0.0.1:8000  
- Swagger UI: http://127.0.0.1:8000/docs  

---

## Example Usage

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

### Register

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"12345678","full_name":"Test User"}'
```

### Login

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"12345678"}'
```

Response:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### Access Protected Route

```bash
curl http://127.0.0.1:8000/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Security Notes

- Passwords are hashed before being stored in the database.
- JWT tokens are signed and validated on protected endpoints.
- Only minimal user data is included in the token payload.

---

## Author

Mohammad Shebahati  
Python Backend Developer (FastAPI)
