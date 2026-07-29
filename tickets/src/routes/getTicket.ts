import Express,{Request,Response } from "express";
import { requireAuth,NotFoundError } from "@ddticketing/common";
import { body } from "express-validator";
import { Ticket } from "../models/ticket";


const router=Express.Router();
router.get('/api/tickets/:id',async(req:Request,res:Response)=>{
    const ticket=await Ticket.findById(req.params.id);
    if(!ticket){
        throw new NotFoundError();
    }
    res.json(ticket);
});
export {router as getTicketRouter};