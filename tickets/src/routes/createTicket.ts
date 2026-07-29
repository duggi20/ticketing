import Express,{Request,Response } from "express";
import { requireAuth,RequestValidation } from "@ddticketing/common";
import { body } from "express-validator";
import { Ticket } from "../models/ticket";
import { TicketCreatedPublisher } from "../events/TicketCreatedPublisher";
import { natsWrapper } from "../nats-wrapper";
const router=Express.Router();


router.post('/api/tickets/create',requireAuth,[
body('title').not().isEmpty().withMessage('Title is required'),
body('price').isFloat({ gt: 0 }).withMessage('Price must be greater than 0')

],RequestValidation,async(req:Request,res:Response)=>{
    const {title,price}=req.body;
    const ticket=Ticket.build({
        title,
        price,
        userId:req.currentUser!.id
    });

    await ticket.save();
    console.log('Inside create ticket route333',ticket); 
   await new TicketCreatedPublisher(natsWrapper.client).publish({
     id: ticket.id,
     title: ticket.title,
     price: ticket.price,
     userId: ticket.userId,
     version: ticket.version
   });
   res.status(201).json(ticket);
});

export {router as createTicketRouter};