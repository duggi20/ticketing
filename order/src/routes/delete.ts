import 'express-async-errors'
import express,{Request,Response} from 'express'
import { requireAuth, NotFoundError, OrderStatus, Subjects } from '@ddticketing/common'
import { Order } from '../models/orders'
import { OrderCancelledPublisher } from '../events/order-cancelled-publisher'
import { natsWrapper } from '../nats-wrapper'

const router = express.Router();

router.delete('/api/orders/:orderId', requireAuth, async (req: Request, res: Response) => {
    const order = await Order.findById(req.params.orderId).populate('ticket');

    if (!order) {
        throw new NotFoundError();
    }

    if (order.userId !== req.currentUser!.id) {
        throw new NotFoundError();
    }

    order.status = OrderStatus.Cancelled;
    await order.save();

    await new OrderCancelledPublisher(natsWrapper.client).publish({
        id: order.id,
        status: OrderStatus.Cancelled,
        version: order.version,
        ticket: {
          id: (order.ticket as any).id || order.ticket.toString(),
        }
    });

    res.status(204).send(order);
})

export {router as deleteOrderRouter}
