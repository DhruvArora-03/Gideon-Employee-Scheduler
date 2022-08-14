from multiprocessing import current_process
from venv import create
from xml.dom.pulldom import END_ELEMENT
import pyodbc

# stop deprecation warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

# cnxn = generate_db_connection()

def generate_db_connection():
    # return pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = 'DHRUV-ALIENWARE\SQLEXPRESS' , database = 'GES')
    return pyodbc.connect(Trusted_Connection='no', driver='{ODBC Driver 17 for SQL Server}', server='gideon-employee-scheduler.database.windows.net', database='GES', uid='Gideon', pwd='{University380}')

def get_all_employee_names():
    cnxn = generate_db_connection()
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
    cnxn = generate_db_connection()
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
    cnxn = generate_db_connection()
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO ShiftAssignments(AssignmentDate, EmployeeID, ShiftID) VALUES (?,?,?)", date, empID, shiftID)
    cnxn.commit()
    cnxn.close()

def create_shift_with_strings(date: str, empName: str, shiftTime: str):
    cnxn = generate_db_connection()
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
    cnxn = generate_db_connection()
    cursor = cnxn.cursor()
    
    # first check if an employee with this ID already exists
    cursor.execute("SELECT * FROM Employees WHERE Employees.EmployeeID={}".format(e_id))
    
    if (cursor.fetchone() != None):
        print('Employee with id {} already exists under the name {} {}'.format(e_id, f_name, l_name))
    else:
        print('Creating employee...')
        cursor.execute("INSERT INTO Employees(EmployeeID, FirstName, LastName) VALUES ({}, '{}', '{}')".format(e_id, f_name, l_name))
        cnxn.commit()

    cnxn.close()

if (__name__ == '__main__'):
    cnxn = generate_db_connection()
    cursor = cnxn.cursor()
    cursor.execute('INSERT INTO Employees (EmployeeID, FirstName, LastName) VALUES (1,\'d\',\'a\')')
    cnxn.commit()

    print(get_all_employee_names())

    cursor.execute('DELETE FROM Employees WHERE Employees.FirstName=\'d\'')
    cnxn.commit()
    cnxn.close()