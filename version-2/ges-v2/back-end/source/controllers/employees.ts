import { Request, Response, NextFunction } from 'express';
import { model, Schema } from 'mongoose';
import axios, { AxiosResponse } from 'axios';
import { addAvailability, deleteAvailability } from './availability';

// create schema and model
const employeeSchema: Schema = new Schema({
    id: {type: Number, required: true},
    name: {type: String, required: true},
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

    // check that id is valid an that name is non-null
    if (isNaN(id) || name === null) {
        return res.status(400).json({
            message: 'Invalid request',
            id: id,
            name: name
        });
    }

    // create a new employee
    const employee = new Employee({
        id: id,
        name: name,
        ...(req.body.exceptions && { exceptions: req.body.exceptions })
    });

    // save employee to mongodb
    await employee.save();

    // request a new default_availability
    let default_availability = await addAvailability(id);

    // return response
    return res.status(200).json({
        message: employee,
        default_availability: default_availability
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

// update an existing employee
const updateEmployee = async (req: Request, res: Response, next: NextFunction) => {
    // read employee id from request
    let id: number = parseInt(req.params.id, 10);
    
    // query mongodb
    const employee = await Employee.findOneAndUpdate(
        { id: id },
        {
            ...(req.body.name && { name: req.body.name })
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

    // delete employee's availability
    let availability = await deleteAvailability(id);

    // return response
    return res.status(200).json({
        message: employee,
        availability: availability
    });
}

export default {
    getEmployees,
    addEmployee,
    getEmployee,
    updateEmployee,
    deleteEmployee
}