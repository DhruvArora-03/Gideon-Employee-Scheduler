import { Request, Response, NextFunction } from 'express';
import axios, { AxiosResponse } from 'axios';

import { MongoClient, ServerApi } from 'mongodb';

const uri = "mongodb+srv://Gideon:University380@ges.gjzwqlv.mongodb.net/?retryWrites=true&w=majority";
const client = new MongoClient(uri);

interface Manager {
    id: number;
    name: string;
    access: string;
}

// getting all managers
const getManagers = async (req: Request, res: Response, next: NextFunction) => {
    // GET request
    let result: AxiosResponse = await axios.get(`http://localhost:380/managers`);

    return res.status(200).json({
        message: result.data as Manager[]
    });
}