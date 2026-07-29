import 'express-async-errors'
import express, { Request, Response } from 'express'
import { requireAuth, RequestValidation, NotFoundError, OrderStatus, BadRequestError, Subjects } from '@ddticketing/common'
import { body } from 'express-validator'
import mongoose from 'mongoose';
import { Ticket } from '../models/ticket';
import { Order } from '../models/orders';
import { OrderCreatedPublisher } from '../events/order-created-publisher';
import { natsWrapper } from '../nats-wrapper';
const router = express.Router();

router.post('/api/orders', requireAuth, [
    body('ticketId').not().isEmpty().custom((input: string) => mongoose.Types.ObjectId.isValid(input)).withMessage('TicketId is required')
], RequestValidation, async (req: Request, res: Response) => {
    const { ticketId } = req.body;
    const ticket = await Ticket.findById(ticketId);
    if (!ticket) {
        throw new NotFoundError();
    }

    const isReserved = await ticket.isReserved();
    if (isReserved) {
        throw new BadRequestError('ticket already reserved');
    }
    let expiration = new Date();
    expiration.setSeconds(expiration.getSeconds() + 1 * 60);
    const order = Order.build({
        userId: req.currentUser!.id,
        status: OrderStatus.Created,
        expiresAt: expiration,
        ticket: ticket
    })
    await order.save();
    await new OrderCreatedPublisher(natsWrapper.client).publish({
        id: order.id,
        status: OrderStatus.Created,
        userId: order.userId,
        expiresAt: order.expiresAt.toISOString(),
        version: order.version,
        ticket: {
          id: ticket.id,
          price: ticket.price,
        }
    });
    res.status(201).send(order);
})

export { router as newOrderRouter }
