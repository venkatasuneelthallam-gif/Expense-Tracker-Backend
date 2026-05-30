# Expense Tracker Backend

This file describes the backend portion of the Expense Tracker project for a GitHub push.

## Backend Contents

- `app.py`
- `requirements.txt`
- `Dockerfile`
- `database/`
  - `db.py`
- `models/`
  - `expense.py`
- `routes/`
  - `expense_routes.py`

## What this backend includes

- Flask application entrypoint (`app.py`)
- Expense routes and blueprint registration
- SQLite database setup and model definitions
- Dockerfile for containerizing the backend service

## Run locally

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\\venv\\Scripts\\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   python app.py
   ```

## Build with Docker

```bash
docker build -t expense-tracker-backend .
docker run -p 5000:5000 expense-tracker-backend
```

## Frontend assets

The frontend assets are now stored in the separate `frontend/` folder and are not included in the backend-only deployment.

## GitHub push

```bash
git add app.py requirements.txt Dockerfile database models routes Expense-Tracker-Backend.md
git commit -m "Add backend-only Expense Tracker files"
git push origin main
```
