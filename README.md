# NEXUS — Smart Task Management REST API

An advanced learning project built with **FastAPI + SQLAlchemy + SQLite**. It demonstrates REST API design, authentication, validation, database persistence, CRUD operations, filtering, analytics and automated tests.

## Features
- User registration and login with JWT bearer tokens
- Password hashing using PBKDF2-HMAC-SHA256
- SQLite persistence through SQLAlchemy ORM
- Task CRUD endpoints with ownership checks
- Pydantic request and response validation
- Search, status/priority filters and pagination
- Analytics summary endpoint
- Interactive Swagger documentation
- Automated API tests using pytest

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Set a strong `SECRET_KEY` environment variable before running outside a local demo. The default key is for development only.

## Run
```bash
uvicorn app.main:app --reload
```
Open:
- API home: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Main endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Health check |
| POST | `/auth/register` | Create user |
| POST | `/auth/login` | Get JWT token (form fields: username, password) |
| GET | `/users/me` | Current user profile |
| POST | `/tasks` | Create task |
| GET | `/tasks` | List/search/filter tasks |
| GET | `/tasks/{task_id}` | Get one task |
| PATCH | `/tasks/{task_id}` | Update task |
| DELETE | `/tasks/{task_id}` | Delete task |
| GET | `/analytics/summary` | Task statistics |

## Quick API workflow
1. Register at `/auth/register`.
2. Use `/auth/login` with username and password to receive a bearer token.
3. In Swagger UI, click **Authorize** and enter the token.
4. Create and manage tasks through `/tasks`.

## Run tests
```bash
pytest -q
```

## Architecture
`app/main.py` defines API routes; `schemas.py` validates inputs/outputs; `models.py` defines database tables; `database.py` manages SQLite sessions; `security.py` handles password hashing and JWT tokens.

## Security and scope
This is an educational starter project, not a production-ready commercial service. Before production use, add HTTPS, managed secrets, rate limiting, refresh-token rotation, audit logging, migrations, backups and security review. Do not use real sensitive personal data.
