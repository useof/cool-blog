## What it does
Scaffolds the FastAPI backend project, including initial app structure, database setup with SQLAlchemy and SQLite, Alembic migrations, and CORS configuration to allow requests from the Angular development server.

## How to use it
Run the app with:

    uvicorn main:app --reload

The backend will be accessible, and CORS is configured for http://localhost:4200. No public API endpoints are available yet.

## Internals
- main.py: FastAPI entry point with CORS middleware for localhost:4200.
- models.py: Defines SQLAlchemy base and an example model for initial setup.
- database.py: Handles SQLite connection and session management.
- alembic.ini: Alembic configuration for database migrations.
- alembic/: Alembic migrations folder, initialized for future schema changes.
- requirements.txt: Lists FastAPI, uvicorn, sqlalchemy, alembic, and python-multipart as dependencies.
- blog.db: SQLite database file for development, created for initial setup.