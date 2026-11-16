from database import Database


class EmployeeManagement:

    def __init__(self):
        self.db = Database()

    def add_employee(self):
        name = input("Enter employee name: ").strip()
        email = input("Enter employee email: ").strip()

        try:
            salary = float(input("Enter monthly salary: "))

            if not name or not email or salary <= 0:
                print("Invalid employee details.")
                return

            connection = self.db.connect()
            if connection is None:
                return

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO employees (name, email, monthly_salary)
                VALUES (?, ?, ?)
                """,
                (name, email, salary)
            )

            connection.commit()

            print("Employee added successfully!")
            print("Employee ID:", cursor.lastrowid)

        except ValueError:
            print("Salary must be a valid positive number.")

        except Exception as error:
            print("Error adding employee:", error)

        finally:
            if 'connection' in locals() and connection:
                connection.close()

    def view_employees(self):
        connection = self.db.connect()

        if connection is None:
            return

        try:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT * FROM employees ORDER BY employee_id"
            )

            employees = cursor.fetchall()

            if not employees:
                print("No employees found.")
                return

            print("\n--- Employee Details ---")

            for employee in employees:
                print("\nEmployee ID:", employee[0])
                print("Name:", employee[1])
                print("Email:", employee[2])
                print("Monthly Salary:", employee[3])

        except Exception as error:
            print("Error viewing employees:", error)

        finally:
            connection.close()

    def update_employee(self):
        try:
            employee_id = int(input("Enter employee ID: "))
            name = input("Enter new employee name: ").strip()
            email = input("Enter new employee email: ").strip()
            salary = float(input("Enter new monthly salary: "))

            if not name or not email or salary <= 0:
                print("Invalid employee details.")
                return

            connection = self.db.connect()
            if connection is None:
                return

            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE employees
                SET name = ?, email = ?, monthly_salary = ?
                WHERE employee_id = ?
                """,
                (name, email, salary, employee_id)
            )

            if cursor.rowcount == 0:
                print("Employee ID not found.")
            else:
                connection.commit()
                print("Employee updated successfully.")

        except ValueError:
            print("Please enter valid employee ID and salary.")

        except Exception as error:
            print("Error updating employee:", error)

        finally:
            if 'connection' in locals() and connection:
                connection.close()

    def delete_employee(self):
        try:
            employee_id = int(input("Enter employee ID: "))

            connection = self.db.connect()
            if connection is None:
                return

            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM employees WHERE employee_id = ?",
                (employee_id,)
            )

            if cursor.rowcount == 0:
                print("Employee ID not found.")
            else:
                connection.commit()
                print("Employee deleted successfully.")

        except ValueError:
            print("Employee ID must be a number.")

        except Exception as error:
            print("Error deleting employee:", error)

        finally:
            if 'connection' in locals() and connection:
                connection.close()