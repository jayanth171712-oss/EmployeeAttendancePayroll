from database import Database
from employee_management import EmployeeManagement
from attendance import Attendance
from payroll import Payroll


def main():

    database = Database()
    database.create_tables()

    employees = EmployeeManagement()
    attendance = Attendance()
    payroll = Payroll()

    while True:

        print("\n======================================")
        print(" EMPLOYEE ATTENDANCE & PAYROLL SYSTEM")
        print("======================================")
        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. View Employees")
        print("5. Record Attendance")
        print("6. Calculate Monthly Attendance")
        print("7. Generate Salary Report")
        print("8. Display Employee Attendance Report")
        print("9. Exit")
        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            employees.add_employee()

        elif choice == "2":
            employees.update_employee()

        elif choice == "3":
            employees.delete_employee()

        elif choice == "4":
            employees.view_employees()

        elif choice == "5":
            attendance.record_attendance()

        elif choice == "6":
            attendance.monthly_attendance()

        elif choice == "7":
            payroll.generate_salary_report()

        elif choice == "8":
            attendance.employee_attendance_report()

        elif choice == "9":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice. Please select 1 to 9.")


if __name__ == "__main__":
    main()