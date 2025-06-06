# Ticket Management System (Simplified)

This repository contains a minimal skeleton for a ticket management system using FastAPI and React. Only the user management and role-based WebSocket channels are implemented.

## Backend

Located in `backend/`. To initialize the database and run the API:

```bash
cd backend
python db_init.py
uvicorn main:app --reload
```

## Frontend

A placeholder React application lives in `frontend/`.

## Docker Compose

Run both services (backend and frontend) using:

```bash
docker compose up
```

## Tests

Backend tests use pytest. From the `backend` folder run:

```bash
pytest
```
