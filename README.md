# AccessHub
A secure employee-management REST API built with Python and FastAPI.

# AccessHub

AccessHub is a secure employee-management REST API built with Python, FastAPI, and SQLite.

## Version 2 — SQLite Employee Storage

AccessHub V2 stores employee information in a local SQLite database and exposes it through a FastAPI endpoint.

### Features

* Automatically creates the SQLite database
* Automatically creates the `employees` table
* Adds sample employees when the database is empty
* Retrieves employee records from SQLite
* Returns employee information as JSON
* Keeps the local database out of GitHub

### Current Endpoint

* `GET /employees` — returns all employees

### Run the Project

```powershell
python -m uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/employees
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Current Technologies

* Python
* FastAPI
* Uvicorn
* SQLite

