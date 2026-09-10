import sqlite3
from pathlib import Path
from fastapi import FastAPI

app = FastAPI()

database_path = Path(__file__).parent / "accesshub.db"


def create_database():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM employees")
    employee_count = cursor.fetchone()[0]

    if employee_count == 0:
        cursor.executemany(
            "INSERT INTO employees (name, role) VALUES (?, ?)",
            [
                ("Ada", "Manager"),
                ("James", "Developer"),
                ("Sara", "Support")
            ]
        )

    connection.commit()
    connection.close()


create_database()


@app.get("/employees")
def get_employees():
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    connection.close()

    return [dict(employee) for employee in employees]