import Express,{Request,Response } from "express";
import { requireAuth,NotFoundError ,NotAuthorizedError, BadRequestError} from "@ddticketing/common";
import { body } from "express-validator";
import { Ticket } from "../models/ticket";
import { TicketUpdatedPublisher } from "../events/TicketUpdatedPublisher";
import { natsWrapper } from "../nats-wrapper";


const router=Express.Router();

router.put('/api/tickets/:id',requireAuth,[
body('title').not().isEmpty().withMessage('Title is required'),
body('price').isFloat({ gt: 0 }).withMessage('Price must be greater than 0')
],async(req:Request,res:Response)=>{
    const ticket=await Ticket.findById(req.params.id);
    if(!ticket){
        throw new NotFoundError();
    }

    if(ticket.orderId){
        throw new BadRequestError('Cannot edit a reserved ticket');
    }
    
    if(ticket.userId!==req.currentUser!.id){
        throw new NotAuthorizedError();
    }
    const {title,price}=req.body;
    ticket.set({
        title,
        price
    });
   await ticket.save();

   await new TicketUpdatedPublisher(natsWrapper.client).publish({
     id: ticket.id,
     title: ticket.title,
     price: ticket.price,
     userId: ticket.userId,
     version: ticket.version
   });

    res.json(ticket);
});
export {router as updateTicketRouter};