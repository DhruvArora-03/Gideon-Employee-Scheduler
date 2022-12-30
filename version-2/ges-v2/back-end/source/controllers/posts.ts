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
    // get posts using axios
    let result: AxiosResponse = await axios.get(`https://jsonplaceholder.typicode.com/posts`);
    let posts: Post[] = result.data;
    return res.status(200).json({
        message: posts
    });
}

// getting a single post
const getPost = async (req: Request, res: Response, next: NextFunction) => {
    // read post id from request
    let id: string = req.params.id;

    // get post using axios
    let result: AxiosResponse = await axios.get(`https://jsonplaceholder.typicode.com/posts/${id}`);
    let post: Post = result.data;
    return res.status(200).json({
        message: post
    });
}

// udpate an existing post
const updatePost = async (req: Request, res: Response, next: NextFunction) => {
    // read post id from request
    let id: string = req.params.id;

    // read post title and body from request if exists
    let title: string = req.body.title ?? null;
    let body: string = req.body.body ?? null;

    // get post using axios
    let result: AxiosResponse = await axios.put(`https://jsonplaceholder.typicode.com/posts/${id}`, {
        ...(title && { title }),
        ...(body && { body })
    });
}

export default {
    getPosts,
    getPost
};