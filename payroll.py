import calendar
import sqlite3
from datetime import datetime
from database import Database


class Payroll:

    def __init__(self):
        self.db = Database()

    def generate_salary_report(self):
        try:
            employee_id = int(input("Enter employee ID: "))
            month = input("Enter month (YYYY-MM): ").strip()

            datetime.strptime(month, "%Y-%m")

            year, month_number = map(int, month.split("-"))
            total_days = calendar.monthrange(year, month_number)[1]

            connection = self.db.connect()
            if connection is None:
                return

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT name, monthly_salary
                FROM employees
                WHERE employee_id = ?
                """,
                (employee_id,)
            )

            employee = cursor.fetchone()

            if not employee:
                print("Employee ID not found.")
                return

            cursor.execute(
                """
                SELECT
                    SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN status = 'Leave' THEN 1 ELSE 0 END)
                FROM attendance
                WHERE employee_id = ?
                AND strftime('%Y-%m', attendance_date) = ?
                """,
                (employee_id, month)
            )

            attendance = cursor.fetchone()

            present = attendance[0] or 0
            absent = attendance[1] or 0
            leave = attendance[2] or 0

            monthly_salary = employee[1]
            daily_salary = monthly_salary / total_days
            paid_days = present + leave
            salary = daily_salary * paid_days

            report = (
                "\n===== EMPLOYEE SALARY REPORT =====\n"
                f"Employee ID: {employee_id}\n"
                f"Employee Name: {employee[0]}\n"
                f"Month: {month}\n"
                f"Monthly Salary: {round(monthly_salary, 2)}\n"
                f"Present Days: {present}\n"
                f"Absent Days: {absent}\n"
                f"Leave Days: {leave}\n"
                f"Paid Days: {paid_days}\n"
                f"Calculated Salary: {round(salary, 2)}\n"
            )

            print(report)

            filename = f"salary_report_{employee_id}_{month}.txt"

            with open(filename, "w") as file:
                file.write(report)

            print("Salary report saved to:", filename)

        except ValueError:
            print("Enter a valid employee ID and month.")

        except sqlite3.Error as error:
            print("Payroll error:", error)

        except OSError as error:
            print("File error:", error)

        finally:
            if 'connection' in locals() and connection:
                connection.close()