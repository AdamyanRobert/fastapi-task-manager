🚀FastAPI Task Manager API

Description:
A simple API for task management (CRUD: create, read, update, delete) using FastAPI and PostgreSQL.
Each task has: uuid, title, description, status (created, in_progress, completed).

🛠️Technologies

Backend: FastAPI

Database: PostgreSQL

Tests: pytest

Documentation: Swagger (/docs)

Containerization: Docker + Docker Compose

⚡ Quick Start

1. Create .env file:

HOST=db

DB_NAME=db_name

USER=postgres

PASSWORD=your_password

2. Run with Docker Compose:

docker-compose up --build

🧪 Running Unit Tests

docker-compose run --rm app pytest tests/unit/test_tasks.py -v  

⚠️ Notes

Tables are auto-created on startup.

Sensitive credentials are stored in .env (not in repo).
