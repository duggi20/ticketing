import 'express-async-errors'
import express,{Request,Response} from 'express'
import {requireAuth} from '@ddticketing/common'
import { Order } from '../models/orders';
const router=express.Router();




router.get('/api/orders',requireAuth,(req:Request,res:Response)=>{
    const orders=Order.find({userId:req.currentUser!.id}).populate('ticket');
    res.send(orders);
})

export {router as orderRouter}


