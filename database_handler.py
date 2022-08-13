from venv import create
import pyodbc

# stop deprecation warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

# cnxn = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = 'DHRUV-ALIENWARE\SQLEXPRESS' , database = 'GES')

def get_all_employee_names():
    cnxn = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = 'DHRUV-ALIENWARE\SQLEXPRESS' , database = 'GES')
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM Employees")
    employee_names = []
    while 1:
        row = cursor.fetchone()
        if not row:
            break
        employee_names.append(row.FirstName)
    cnxn.commit()
    cnxn.close()
    return employee_names

def get_all_shifts_for_employee(id: int):
    cnxn = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = 'DHRUV-ALIENWARE\SQLEXPRESS' , database = 'GES')
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM ShiftAssignments WHERE EmployeeID = ?", id)
    shifts = list()
    while 1:
        row = cursor.fetchone()
        if not row:
            break
        cursor.execute("SELECT * FROM Shifts WHERE ShiftID = ?", row.ShiftID)
        shifts.append('{} - {}'.format(row.AssignmentDate, cursor.fetchone().ShiftTime))
    cnxn.commit()
    cnxn.close()
    return shifts

def create_shift_with_IDs(date: str, empID: int, shiftID: int):
    cnxn = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = 'DHRUV-ALIENWARE\SQLEXPRESS' , database = 'GES')
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO ShiftAssignments(AssignmentDate, EmployeeID, ShiftID) VALUES (?,?,?)", date, empID, shiftID)
    cnxn.commit()
    cnxn.close()

def create_shift_with_strings(date: str, empName: str, shiftTime: str):
    cnxn = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = 'DHRUV-ALIENWARE\SQLEXPRESS' , database = 'GES')
    cursor = cnxn.cursor()
    cursor.execute("SELECT EmployeeID FROM Employees WHERE FirstName = \'" + empName + "\'")
    empID = cursor.fetchone().EmployeeID
    cursor.execute("SELECT ShiftID FROM Shifts WHERE ShiftTime = \'" + shiftTime + "\'")
    shiftID = cursor.fetchone().ShiftID
    cnxn.commit()
    cnxn.close()
    create_shift_with_IDs(date, empID, shiftID)

# this method creates a new employee with the specified parameters
def create_employee(f_name: str, l_name: str, e_id: int):
    cnxn = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = 'DHRUV-ALIENWARE\SQLEXPRESS' , database = 'GES')
    cursor = cnxn.cursor()
    cursor.execute('INSERT INTO Employees(EmployeeID, FirstName, LastName) '

# cnxn = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = 'DHRUV-ALIENWARE\SQLEXPRESS' , database = 'GES')
# cursor = cnxn.cursor()
# cursor.execute()
# cnxn.commit()

# print(get_all_employee_names())

# cnxn.close()