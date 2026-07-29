import { AbstractListener, OrderCreatedEvent, Subjects } from "@ddticketing/common";
import { Order } from "../models/orders";


export class OrderCreatedListener extends AbstractListener<OrderCreatedEvent> {
    subject: Subjects.OrderCreated = Subjects.OrderCreated
    queueGroupName = 'payments-service'

    async onMessage(data: OrderCreatedEvent['data'], msg: any) {
       const order = Order.build({
            id: data.id,
            version: data.version,
            price: data.ticket.price,
            userId: data.userId,
            status: data.status
       })
       await order.save()
    }
}