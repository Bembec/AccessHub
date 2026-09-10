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


## Version 3 — Individual Employee Retrieval

* Added `GET /employees/{employee_id}`
* Retrieves one employee using their ID
* Returns `404 Not Found` when the employee does not exist
* Uses parameterized SQL queries

## Version 4 — Employee Creation

* Added `POST /employees`
* Validates request data with Pydantic
* Creates new employee records
* Returns HTTP `201 Created`
* Stores new employees permanently in SQLite

## Version 5 — Employee Updates

* Added `PUT /employees/{employee_id}`
* Updates an employee’s name and role
* Returns the updated employee
* Returns `404 Not Found` for an unknown employee

## Version 6 — Employee Deletion

* Added `DELETE /employees/{employee_id}`
* Permanently removes an employee from SQLite
* Returns a successful deletion message
* Returns `404 Not Found` for an unknown employee

## CRUD Endpoints

* `POST /employees` — create an employee
* `GET /employees` — retrieve all employees
* `GET /employees/{employee_id}` — retrieve one employee
* `PUT /employees/{employee_id}` — update an employee
* `DELETE /employees/{employee_id}` — delete an employee


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

