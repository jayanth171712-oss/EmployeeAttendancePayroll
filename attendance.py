import sqlite3
from datetime import datetime
from database import Database


class Attendance:

    def __init__(self):
        self.db = Database()

    def record_attendance(self):
        try:
            employee_id = int(input("Enter employee ID: "))
            attendance_date = input("Enter date (YYYY-MM-DD): ").strip()
            status = input("Enter status (Present/Absent/Leave): ").strip().capitalize()

            datetime.strptime(attendance_date, "%Y-%m-%d")

            if status not in ["Present", "Absent", "Leave"]:
                print("Invalid attendance status.")
                return

            connection = self.db.connect()
            if connection is None:
                return

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO attendance
                (employee_id, attendance_date, status)
                VALUES (?, ?, ?)
                """,
                (employee_id, attendance_date, status)
            )

            connection.commit()
            print("Attendance recorded successfully.")

        except ValueError:
            print("Enter a valid employee ID or date.")

        except sqlite3.IntegrityError:
            print("Invalid employee ID or attendance already recorded for this date.")

        except sqlite3.Error as error:
            print("Attendance error:", error)

        finally:
            if 'connection' in locals() and connection:
                connection.close()

    def monthly_attendance(self):
        try:
            employee_id = int(input("Enter employee ID: "))
            month = input("Enter month (YYYY-MM): ").strip()

            datetime.strptime(month, "%Y-%m")

            connection = self.db.connect()
            if connection is None:
                return

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(*),
                    SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN status = 'Leave' THEN 1 ELSE 0 END)
                FROM attendance
                WHERE employee_id = ?
                AND strftime('%Y-%m', attendance_date) = ?
                """,
                (employee_id, month)
            )

            result = cursor.fetchone()

            print("\n--- Monthly Attendance Report ---")
            print("Total Recorded Days:", result[0])
            print("Present:", result[1] or 0)
            print("Absent:", result[2] or 0)
            print("Leave:", result[3] or 0)

        except ValueError:
            print("Enter a valid employee ID and month.")

        except sqlite3.Error as error:
            print("Attendance report error:", error)

        finally:
            if 'connection' in locals() and connection:
                connection.close()

    def employee_attendance_report(self):
        try:
            employee_id = int(input("Enter employee ID: "))

            connection = self.db.connect()
            if connection is None:
                return

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT attendance_date, status
                FROM attendance
                WHERE employee_id = ?
                ORDER BY attendance_date
                """,
                (employee_id,)
            )

            records = cursor.fetchall()

            if not records:
                print("No attendance records found.")
                return

            print("\n--- Employee Attendance Report ---")

            for record in records:
                print("Date:", record[0], "| Status:", record[1])

        except ValueError:
            print("Employee ID must be a number.")

        except sqlite3.Error as error:
            print("Attendance report error:", error)

        finally:
            if 'connection' in locals() and connection:
                connection.close()