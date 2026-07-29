import Express,{Request,Response } from "express";
import { requireAuth,NotFoundError } from "@ddticketing/common";
import { body } from "express-validator";
import { Ticket } from "../models/ticket";


const router=Express.Router();

router.get('/api/tickets',async(req:Request,res:Response)=>{
    const tickets=await Ticket.find({});
    res.json(tickets);
});
export {router as getAllTicketsRouter};