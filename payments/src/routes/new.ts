import { requireAuth,RequestValidation, NotFoundError, NotAuthorizedError, OrderStatus, BadRequestError } from "@ddticketing/common";
import { Router } from "express";
import {body} from 'express-validator'
import { Order } from "../models/orders";
import { stripe } from "../Stripe";
import { Payment } from "../models/payments";
import { PaymentCreatedPublisher } from "../publishers/Payment-created-publisher";
import { natsWrapper } from "../nats-wrapper";
const router = Router()

router.post('/api/payments', requireAuth,
body('token').not().isEmpty().withMessage('Token is required'),
body('orderId').not().isEmpty().withMessage('OrderId is required'),   
RequestValidation,
    async (req, res) => {
  const { token, orderId } = req.body;
  const order=await Order.findById(orderId)
  if(!order){
    throw new NotFoundError()
  }
  if(order.userId !== req.currentUser!.id){
    throw new NotAuthorizedError()
  }
  if(order.status === OrderStatus.Cancelled){
    throw new BadRequestError('Cannot pay for a cancelled order')
  }


 const charge= await stripe.charges.create({
    amount: order.price * 100,
    currency: 'usd',
    source: token
  })
  console.log("charge===>",charge)
   const payment = Payment.build({
    orderId,
    stripeId: charge.id
   })
    console.log("payment===>",payment)
    await payment.save()
    await new PaymentCreatedPublisher(natsWrapper.client).publish({
        id: payment.id,
      orderId: payment.orderId,
      stripeId: payment.stripeId
    })
    res.send({id: payment.id})
})

export  {router as createChargeRouter}