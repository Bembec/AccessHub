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


## Version 7 — Administrator Security and Audit Logs

AccessHub V7 protects sensitive employee-management operations and records administrative activity.

### Security Features

* Protects employee creation with an administrator API key
* Protects employee updates and deletions
* Protects access to administrative audit logs
* Reads the secret key from an environment variable
* Uses secure key comparison
* Returns `401 Unauthorized` for an invalid key
* Returns `503 Service Unavailable` when no administrator key is configured

### Audit Features

* Automatically creates an `audit_logs` table
* Records employee creation events
* Records employee update events
* Records employee deletion events
* Stores timestamps, action types, employee IDs, and event details
* Returns recent activity through `GET /audit-logs`
* Supports an audit result limit between 1 and 100

### Protected Endpoints

The following endpoints require the `x-api-key` header:

* `POST /employees`
* `PUT /employees/{employee_id}`
* `DELETE /employees/{employee_id}`
* `GET /audit-logs`

### Configure the Administrator Key

Set an administrator key before starting AccessHub:

```powershell
$env:ACCESSHUB_ADMIN_KEY = "your-private-administrator-key"
```

Start the API:

```powershell
python -m uvicorn main:app --reload
```

The administrator key must never be hardcoded in `main.py` or uploaded to GitHub.

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

