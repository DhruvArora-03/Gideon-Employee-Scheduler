import { Request, Response, NextFunction } from 'express';

import { model, Schema } from 'mongoose';

// create schema and model
const managerSchema: Schema = new Schema({
    id: {type: Number, required: true},
    name: {type: String, required: true},
    permissions: {type: String, required: true, default: 'READ-ONLY'}
});
const Manager = model('Managers', managerSchema);

// getting all managers
const getManagers = async (req: Request, res: Response, next: NextFunction) => {
    // query mongodb
    const managers = await Manager.find({});

    // return response
    return res.status(200).json({
        message: managers
    });
}

// create a new manager
const addManager = async (req: Request, res: Response, next: NextFunction) => {
    let id: number = parseInt(req.body.id, 10);
    let name: string = req.body.name ?? null;
    let permissions: string = req.body.permissions ?? null;
    
    // check that id is valid an that name and permissions are non-null
    if (isNaN(id) || name === null || permissions === null) {
        return res.status(400).json({
            message: 'Invalid request'
        });
    }

    // create a new manager
    const manager = new Manager({
        id: id,
        name: name,
        permissions: permissions
    });

    // save manager to mongodb
    await manager.save();

    // return response
    return res.status(200).json({
        message: manager
    });
}

// get a specific manager
const getManager = async (req: Request, res: Response, next: NextFunction) => {
    // read manager id from request
    let id: number = parseInt(req.params.id, 10);

    // query mongodb
    const manager = await Manager.findOne(
        { id: id }
    );

    // return response
    return res.status(200).json({
        message: manager
    });

}

// update an existing manager
const updateManager = async (req: Request, res: Response, next: NextFunction) => {
    // read manager id from request
    let id: number = parseInt(req.params.id, 10);

    // read manager name from request if exists
    let name: string = req.body.name ?? null;
    // read manager permissions from request if exists
    let permissions: string = req.body.permissions ?? null;

    // query mongodb
    const manager = await Manager.findOneAndUpdate(
        { id: id },
        {
            ...(name && { name }),
            ...(permissions && { permissions })
        },
        { new: true }
    );

    // return response
    return res.status(200).json({
        message: manager
    });
}

// delete an existing manager
const deleteManager = async (req: Request, res: Response, next: NextFunction) => {
    // read manager id from request
    let id: number = parseInt(req.params.id, 10);

    // query mongodb
    const manager = await Manager.findOneAndDelete(
        { id: id }
    );

    // return response
    return res.status(200).json({
        message: manager
    });
}


export default {
    getManagers,
    addManager,
    getManager,
    updateManager,
    deleteManager
}