import { Request, Response, NextFunction } from 'express';
import axios, { AxiosResponse } from 'axios';
 
interface Post {
    userId: number;
    id: number;
    title: string;
    body: string;
}

// getting all posts
const getPosts = async (req: Request, res: Response, next: NextFunction) => {
    // GET request
    let result: AxiosResponse = await axios.get(`https://jsonplaceholder.typicode.com/posts`);
    
    return res.status(200).json({
        message: result.data as Post[]
    });
}

// getting a single post
const getPost = async (req: Request, res: Response, next: NextFunction) => {
    // read post id from request
    let id: string = req.params.id;

    // GET request
    let result: AxiosResponse = await axios.get(
        `https://jsonplaceholder.typicode.com/posts/${id}`
    );

    return res.status(200).json({
        message: result.data as Post
    });
}

// udpate an existing post
const updatePost = async (req: Request, res: Response, next: NextFunction) => {
    // read post id from request
    let id: string = req.params.id;

    // read post title and body from request if exists
    let title: string = req.body.title ?? null;
    let body: string = req.body.body ?? null;
    console.log('title: ', title);
    console.log('body: ', body);
    // PUT request
    let result: AxiosResponse = await axios.put(
        `https://jsonplaceholder.typicode.com/posts/${id}`,
        {
            ...(title && { title }),
            ...(body && { body })
        }
    );

    return res.status(200).json({
        message: result.data
    });
}

// delete an existing post
const deletePost = async (req: Request, res: Response, next: NextFunction) => {
    // read post id from request
    let id: string = req.params.id;

    // DELETE request
    let result: AxiosResponse = await axios.delete(
        `https://jsonplaceholder.typicode.com/posts/${id}`
    );

    return res.status(200).json({
        message: result.data
    });
}

// add a new post
const addPost = async (req: Request, res: Response, next: NextFunction) => {
    // read post title and body from request
    let data = {
        title: req.body.title,
        body: req.body.body
    };

    // POST request
    let result: AxiosResponse = await axios.post(
        `https://jsonplaceholder.typicode.com/posts`,
        data
    );

    return res.status(200).json({
        message: result.data,
    });
}


// export all functions
export default {
    getPosts,
    getPost,
    updatePost,
    deletePost,
    addPost
};