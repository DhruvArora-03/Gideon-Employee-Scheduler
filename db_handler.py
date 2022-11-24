from datetime import datetime

from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://Gideon:University380@ges.gjzwqlv.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client["GES"]


'''
create_employee: Create a new employee in the database

Args:
    f_name (str): The employee's first name
    l_name (str): The employee's last name
    id (int): The employee's id #
'''
def create_employee(f_name: str, l_name: str, id: int):
    existing = db.Employees.find_one({"_id": id})

    if (existing != None):
        print('Employee with id {} already exists under the name {} {}'.format(
            existing._id, 
            existing.first_name,
            existing.last_name
        ))
    else:
        print('Creating employee...')
        employee = {'_id': id, 'first_name': f_name, 'last_name': l_name, 'manager': False}
        db.Employees.update_one(employee, {'$set': employee}, upsert=True)
        print('Employee created successfully')


def get_all_shifts_for_employee(id: int):
    return db.ShiftAssignments.find({'_id': id, 'manager': False}) != None

def is_manager(id: int):
    return db.Employees.find_one({'_id': id}) != None

def promote_employee(id: int):
    employee = db.Employees.find_one({'_id': id})
    if employee != None:
        employee['manager'] = True
        db.Employees.update_one(employee, {'$set': employee}, upsert=True)
    else:
        print('Employee with id {} does not exist'.format(id))

def create_shift(month: int, day: int, year: int, hour: int, minute: int, 
                length: float, num_staff: int, creator_id: int):
    id = int('{0}{1}{2}{3}{4:02d}'.format(year - 2000, month, day, hour, minute))
    dt = datetime(year, month, day, hour, minute)

    existing = db.Shifts.find_one({"_id": id})
    if existing != None:
        print('Shift with id {} already exists'.format(id))
        db.Shifts.delete_one(existing)
        print('Existing Shift deleted')
    shift = {
        '_id': id,
        'creator_id': creator_id,
        'date_time': dt,
        'length': length,
        'num_staff': num_staff
    }
    db.Shifts.update_one(shift, {'$set': shift}, upsert=True)

def delete_shift(id: int):
    shift = db.Shifts.find_one({'_id': id})
    if shift != None:
        db.Shifts.delete_one(shift)
        print('Shift deleted successfully')
        return True
    else:
        print('Shift with id {} does not exist'.format(id))
        return False

def populate_shift(id: int):
    shift = db.Shifts.find_one({'_id': id})
    if shift != None:
        for _ in range(shift['num_staff']):
            assignment = {
                '_id': id,
                'employee_id': employee_id
            }
            db.ShiftAssignments.update_one(assignment, {'$set': assignment}, upsert=True)
