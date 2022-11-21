from multiprocessing import current_process
from venv import create
from xml.dom.pulldom import END_ELEMENT
from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://Gideon:University380@ges.gjzwqlv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["GES"]


# def get_all_employee_names():
#     cnxn = generate_db_connection()
#     cursor = cnxn.cursor()
#     cursor.execute("SELECT * FROM Employees")
#     employee_names = []
#     while 1:
#         row = cursor.fetchone()
#         if not row:
#             break
#         employee_names.append(row.FirstName)
#     cnxn.commit()
#     cnxn.close()
#     return employee_names

def get_all_shifts_for_employee(id: int):
    db.ShiftAssignments.find({'_id': id})
    shiftIDs = []
    row = cursor.fetchone()
    while row:
        shiftIDs.append(row.ShiftID)
        row = cursor.fetchone()

    shifts = []
    for id in shiftIDs:
        print('running command', "SELECT Shifts.DateTime FROM Shifts WHERE ShiftID =", id)
        cursor.execute("SELECT Shifts.DateTime FROM Shifts WHERE ShiftID = ?", id)
        shifts.append(str(cursor.fetchone().DateTime))
    
    cnxn.commit()
    cnxn.close()
    return shifts

# def create_shift_with_IDs(date: str, empID: int, shiftID: int):
#     cnxn = generate_db_connection()
#     cursor = cnxn.cursor()
#     cursor.execute("INSERT INTO ShiftAssignments(AssignmentDate, EmployeeID, ShiftID) VALUES (?,?,?)", date, empID, shiftID)
#     cnxn.commit()
#     cnxn.close()

# def create_shift_with_strings(date: str, empName: str, shiftTime: str):
#     cnxn = generate_db_connection()
#     cursor = cnxn.cursor()
#     cursor.execute("SELECT EmployeeID FROM Employees WHERE FirstName = \'" + empName + "\'")
#     empID = cursor.fetchone().EmployeeID
#     cursor.execute("SELECT ShiftID FROM Shifts WHERE ShiftTime = \'" + shiftTime + "\'")
#     shiftID = cursor.fetchone().ShiftID
#     cnxn.commit()
#     cnxn.close()
#     create_shift_with_IDs(date, empID, shiftID)

# def delete_shift(shiftDate: str, empID: int):
#     cnxn = generate_db_connection()
#     cursor = cnxn.cursor()
#     cursor.execute("SELECT Shifts.ShiftID FROM Shifts WHERE DATEDIFF(day, Shifts.DateTime, '{}') = 0".format(shiftDate))
#     row = cursor.fetchone()
#     if row:
#         shiftID = row.ShiftID
#         print('shiftID', shiftID)
#         cursor.execute("SELECT * FROM ShiftAssignments WHERE ShiftAssignments.ShiftID = ? AND ShiftAssignments.EmployeeID = ?", shiftID, empID)
#         row = cursor.fetchone()
#         if row:
#             cursor.execute("DELETE FROM ShiftAssignments WHERE ShiftAssignments.ShiftID = ? AND ShiftAssignments.EmployeeID = ?", shiftID, empID)
#             cnxn.commit()
#             cnxn.close()
#             return True
    

#     cnxn.commit()
#     cnxn.close()
#     return False

# this method creates a new employee with the specified parameters
def create_employee(f_name: str, l_name: str, e_id: int):
    existing = db.Employees.find_one({"_id": e_id})

    if (existing != None):
        print('Employee with id {} already exists under the name {} {}'.format(
            existing._id, 
            existing.first_name,
            existing.last_name
        ))
    else:
        print('Creating employee...')
        employee = {'_id': e_id, 'first_name': f_name, 'last_name': l_name}
        db.Employees.update_one(employee, {'$set': employee}, upsert=True)
        print('Employee created successfully')

# if (__name__ == '__main__'):
    # cnxn = generate_db_connection()
    # cursor = cnxn.cursor()
    # cursor.execute('INSERT INTO Employees (EmployeeID, FirstName, LastName) VALUES (1,\'d\',\'a\')')
    # cnxn.commit()

    # print(get_all_employee_names())

    # cursor.execute('DELETE FROM Employees WHERE Employees.FirstName=\'d\'')
    # cnxn.commit()
    # cnxn.close()