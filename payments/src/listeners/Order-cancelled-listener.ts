import { AbstractListener, OrderCancelledEvent, OrderStatus, Subjects } from '@ddticketing/common'
import { Order } from '../models/orders'

export class OrderCancelledListener extends AbstractListener<OrderCancelledEvent> {
    subject: Subjects.OrderCancelled = Subjects.OrderCancelled
    queueGroupName = 'payments-service'
    onMessage(data: OrderCancelledEvent['data'], msg: any) {

        const order = Order.findOne({
            _id: data.id,
            version: data.version - 1
        })
        if (!order) {
            throw new Error('Order not found')
        }
        order.set({ status: OrderStatus.Cancelled })
        msg.ack()

    }
}