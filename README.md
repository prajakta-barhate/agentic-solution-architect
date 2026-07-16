# agentic-solution-architect
Multi-Agent AI Solution Architect built with LangGraph, FastAPI, React and PostgreSQL.

## Backend setup

### Prerequisites
- Python 3.12+
- A PostgreSQL or Neon database
- Virtual environment created in the backend folder

### Environment variables
Create a backend `.env` file with at least:

```env
DATABASE_URL=postgresql://<user>:<password>@<host>/<database>?sslmode=require
GEMINI_API_KEY=
SECRET_KEY=change-me-in-production
ENVIRONMENT=development
DEBUG=true
```

### Run the backend
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

### Database health check
```powershell
curl http://127.0.0.1:8000/health/db
```

### Alembic commands
Run Alembic from the backend folder using the project virtual environment:

```powershell
cd backend
.\.venv\Scripts\alembic.exe revision --autogenerate -m "initial"
```

This command is the working autogenerate command for the current setup.

### Alembic troubleshooting
If Alembic reports that the target database is not up to date, the issue is usually a revision mismatch between the migration scripts and the database's recorded revision.

In this project, the fix was:

```powershell
cd backend
.\.venv\Scripts\alembic.exe stamp <latest_revision_id>
.\.venv\Scripts\alembic.exe upgrade head
```

Then rerun the autogenerate command:

```powershell
cd backend
.\.venv\Scripts\alembic.exe revision --autogenerate -m "create project table"
```

This happened earlier because the database still pointed to an older revision while the migration scripts had a newer head. Stamping and upgrading the database brought it back into sync.
