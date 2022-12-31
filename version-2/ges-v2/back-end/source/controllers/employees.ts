import { Request, Response, NextFunction } from 'express';
import { model, connect, Schema } from 'mongoose';

// create schema and model
const employeeSchema = new Schema({
    id: {type: Number, required: true},
    name: {type: String, required: true},
    default_availability: {type: Object, required: true},
    exceptions: {type: Object, required: true, default: {}}
});
const Employee = model('Employees', employeeSchema);

// getting all employees
const getEmployees = async (req: Request, res: Response, next: NextFunction) => {
    // query mongodb
    const employees = await Employee.find({});
    
    // return response
    return res.status(200).json({
        message: employees
    });
}

// create a new employee
const addEmployee = async (req: Request, res: Response, next: NextFunction) => {
    let id: number = parseInt(req.body.id, 10);
    let name: string = req.body.name ?? null;
    let default_availability = req.body.default_availability ?? null;

    // check that id is valid an that name and default_availability are non-null
    if (isNaN(id) || name === null || default_availability === null) {
        return res.status(400).json({
            message: 'Invalid request',
            id: id,
            name: name,
            default_availability: default_availability,
        });
    }

    // create a new employee
    const employee = new Employee({
        id: id,
        name: name,
        default_availability: default_availability,
        ...(req.body.exceptions && { exceptions: req.body.exceptions })
    });

    // save employee to mongodb
    await employee.save();

    // return response
    return res.status(200).json({
        message: employee
    });
}

// get a specific employee
const getEmployee = async (req: Request, res: Response, next: NextFunction) => {
    // read employee id from request
    let id: number = parseInt(req.params.id, 10);
    
    // query mongodb
    const employee = await Employee.findOne(
        { id: id }
    );

    // return response
    return res.status(200).json({
        message: employee
    });
}

// add an exception to an employee
const addException = async (req: Request, res: Response, next: NextFunction) => {
    // read employee id from request
    let id: number = parseInt(req.params.id, 10);

    // query mongodb
    const employee = await Employee.findOne(
        { id: id }
    );
    
    // check if found an employee
    if (!employee) {
        return res.status(404).json({
            message: "Employee not found"
        });
    }

    // add exception to employee
    employee.exceptions.push(req.body.exception);

    // save employee to mongodb
    await employee.save();

    // return response
    return res.status(200).json({
        message: employee
    });
}

// update an existing employee
const updateEmployee = async (req: Request, res: Response, next: NextFunction) => {
    // read employee id from request
    let id: number = parseInt(req.params.id, 10);
    
    // query mongodb
    const employee = await Employee.findOneAndUpdate(
        { id: id },
        {
            ...(req.body.name && { name: req.body.name }),
            ...(req.body.default_availability && { default_availability: req.body.default_availability }),
            ...(req.body.exceptions && { exceptions: req.body.exceptions })
        },
        { new: true }
    );

    // return response
    return res.status(200).json({
        message: employee
    });
}

// delete an existing employee
const deleteEmployee = async (req: Request, res: Response, next: NextFunction) => {
    // read employee id from request
    let id: number = parseInt(req.params.id, 10);
    
    // query mongodb
    const employee = await Employee.findOneAndDelete(
        { id: id }
    );

    // return response
    return res.status(200).json({
        message: employee
    });
}

export default {
    getEmployees,
    addEmployee,
    getEmployee,
    addException,
    updateEmployee,
    deleteEmployee
}