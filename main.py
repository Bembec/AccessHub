import os
import secrets
import sqlite3
from datetime import datetime
from pathlib import Path

from fastapi import (
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Query,
)
from pydantic import BaseModel


app = FastAPI(
    title="AccessHub API",
    version="7.0",
)

database_path = Path(__file__).parent / "accesshub.db"


class EmployeeData(BaseModel):
    """Employee information received by the API."""

    name: str
    role: str


def create_database():
    """Create the AccessHub database tables."""

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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            employee_id INTEGER,
            details TEXT NOT NULL
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


def verify_admin(
    x_api_key: str | None = Header(default=None),
):
    """Verify the administrator API key."""

    admin_key = os.getenv("ACCESSHUB_ADMIN_KEY")

    if not admin_key:
        raise HTTPException(
            status_code=503,
            detail="Administrator API key is not configured",
        )

    if (
        x_api_key is None
        or not secrets.compare_digest(
            x_api_key,
            admin_key,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid administrator API key",
        )


def record_audit_event(
    action,
    employee_id,
    details,
):
    """Store one administrative action."""

    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO audit_logs (
            timestamp,
            action,
            employee_id,
            details
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            timestamp,
            action,
            employee_id,
            details,
        ),
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


@app.post(
    "/employees",
    status_code=201,
    dependencies=[Depends(verify_admin)],
)
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

    record_audit_event(
        action="CREATE",
        employee_id=employee_id,
        details=(
            f"Created {employee.name} "
            f"with role {employee.role}"
        ),
    )

    return {
        "id": employee_id,
        "name": employee.name,
        "role": employee.role,
    }


@app.put(
    "/employees/{employee_id}",
    dependencies=[Depends(verify_admin)],
)
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

    record_audit_event(
        action="UPDATE",
        employee_id=employee_id,
        details=(
            f"Updated {employee.name} "
            f"to role {employee.role}"
        ),
    )

    return {
        "id": employee_id,
        "name": employee.name,
        "role": employee.role,
    }


@app.delete(
    "/employees/{employee_id}",
    dependencies=[Depends(verify_admin)],
)
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

    record_audit_event(
        action="DELETE",
        employee_id=employee_id,
        details="Deleted employee record",
    )

    return {
        "message": "Employee deleted successfully",
        "employee_id": employee_id,
    }


@app.get(
    "/audit-logs",
    dependencies=[Depends(verify_admin)],
)
def get_audit_logs(
    limit: int = Query(default=20, ge=1, le=100),
):
    """Return recent administrative actions."""

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT *
        FROM audit_logs
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )

    audit_logs = cursor.fetchall()
    connection.close()

    return [dict(audit_log) for audit_log in audit_logs]