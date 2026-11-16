import sqlite3


class Database:

    def connect(self):
        try:
            connection = sqlite3.connect("employee_payroll.db")
            connection.execute("PRAGMA foreign_keys = ON")
            return connection

        except sqlite3.Error as error:
            print("Database connection error:", error)
            return None

    def create_tables(self):
        connection = self.connect()

        if connection is None:
            return

        try:
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    monthly_salary REAL NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER NOT NULL,
                    attendance_date TEXT NOT NULL,
                    status TEXT NOT NULL
                        CHECK(status IN ('Present', 'Absent', 'Leave')),
                    FOREIGN KEY (employee_id)
                        REFERENCES employees(employee_id),
                    UNIQUE(employee_id, attendance_date)
                )
            """)

            connection.commit()
            print("Database and tables created successfully.")

        except sqlite3.Error as error:
            connection.rollback()
            print("Table creation error:", error)

        finally:
            connection.close()