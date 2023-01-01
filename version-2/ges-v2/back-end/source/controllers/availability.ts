import { Request, Response, NextFunction } from 'express';
import { model, Schema } from 'mongoose';

// create schema and model
const availabilitySchema: Schema = new Schema({
    id: {type: Number, required: true},
    monday: {type: Object, required: true, default: {start: "", end: ""}},
    tuesday: {type: Object, required: true, default: {start: "", end: ""}},
    wednesday: {type: Object, required: true, default: {start: "", end: ""}},
    thursday: {type: Object, required: true, default: {start: "", end: ""}},
    friday: {type: Object, required: true, default: {start: "", end: ""}},
    saturday: {type: Object, required: true, default: {start: "", end: ""}},
    sunday: {type: Object, required: true, default: {start: "", end: ""}}
});
const Availability = model('Availabilities', availabilitySchema);

// get specifc availability
const getAvailability = async (req: Request, res: Response, next: NextFunction) => {
    // read employee id from request
    let id: number = parseInt(req.params.id, 10);

    // check that id is valid
    if (isNaN(id)) {
        return res.status(400).json({
            message: 'Invalid request',
            id: id
        });
    }

    // query mongodb
    const availability = await Availability.findOne(
        { id: id }
    );

    // return response
    return res.status(200).json({
        message: availability
    });
}

// update a specific availability
const updateAvailability = async (req: Request, res: Response, next: NextFunction) => {
    // read employee id from request
    let id: number = parseInt(req.params.id, 10);

    // check that id is valid
    if (isNaN(id)) {
        return res.status(400).json({
            message: 'Invalid request',
            id: id
        });
    }

    // query mongodb
    const availability = await Availability.findOneAndUpdate(
        { id: id },
        {
            ...(req.body.monday && { monday: req.body.monday }),
            ...(req.body.tuesday && { tuesday: req.body.tuesday }),
            ...(req.body.wednesday && { wednesday: req.body.wednesday }),
            ...(req.body.thursday && { thursday: req.body.thursday }),
            ...(req.body.friday && { friday: req.body.friday }),
            ...(req.body.saturday && { saturday: req.body.saturday }),
            ...(req.body.sunday && { sunday: req.body.sunday })
        },
        { new: true }
    );

    // return response
    return res.status(200).json({
        message: availability
    });
}

export default {
    Availability,
    getAvailability,
    updateAvailability
};

// FOLLOWING IS ONLY FOR CREATING AND DELETING EMPLOYEES

// create new availability
const addAvailability = async (id: number) => {
    // create a new availability
    const availability = new Availability({
        id: id
    });

    // save availability to mongodb
    await availability.save();

    // return response
    return availability;
}

// delete a specific availability
const deleteAvailability = async (id: Number) => {
    // query mongodb
    const availability = await Availability.findOneAndDelete(
        { id: id }
    );

    // return response
    return availability;
}

export {
    addAvailability,
    deleteAvailability
}