import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="AccessHub API",
    version="6.0",
)

database_path = Path(__file__).parent / "accesshub.db"


class EmployeeData(BaseModel):
    """Employee information received by the API."""

    name: str
    role: str


def create_database():
    """Create the employee database and sample records."""

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )

    cursor.execute("SELECT COUNT(*) FROM employees")
    employee_count = cursor.fetchone()[0]

    if employee_count == 0:
        cursor.executemany(
            """
            INSERT INTO employees (name, role)
            VALUES (?, ?)
            """,
            [
                ("Ada", "Manager"),
                ("James", "Developer"),
                ("Sara", "Support"),
            ],
        )

    connection.commit()
    connection.close()


create_database()


@app.get("/employees")
def get_employees():
    """Return every employee."""

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    connection.close()

    return [dict(employee) for employee in employees]


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    """Return one employee using their ID."""

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee_id,),
    )

    employee = cursor.fetchone()
    connection.close()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return dict(employee)


@app.post("/employees", status_code=201)
def create_employee(employee: EmployeeData):
    """Create and save a new employee."""

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO employees (name, role)
        VALUES (?, ?)
        """,
        (
            employee.name,
            employee.role,
        ),
    )

    employee_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "id": employee_id,
        "name": employee.name,
        "role": employee.role,
    }


@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeData,
):
    """Update an existing employee."""

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE employees
        SET name = ?, role = ?
        WHERE id = ?
        """,
        (
            employee.name,
            employee.role,
            employee_id,
        ),
    )

    updated_rows = cursor.rowcount

    connection.commit()
    connection.close()

    if updated_rows == 0:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return {
        "id": employee_id,
        "name": employee.name,
        "role": employee.role,
    }


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    """Delete an existing employee."""

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id = ?",
        (employee_id,),
    )

    deleted_rows = cursor.rowcount

    connection.commit()
    connection.close()

    if deleted_rows == 0:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return {
        "message": "Employee deleted successfully",
        "employee_id": employee_id,
    }