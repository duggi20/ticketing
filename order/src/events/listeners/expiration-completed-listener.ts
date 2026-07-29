import { AbstractListener, ExpirationCompletedEvent, OrderStatus, Subjects } from "@ddticketing/common";
import { Message } from "node-nats-streaming";
import { Order } from "../../models/orders";
import { OrderCancelledPublisher } from '../order-cancelled-publisher'

export class ExpirationCompletedListener extends AbstractListener<ExpirationCompletedEvent> {
  subject: Subjects.ExpirationCompleted = Subjects.ExpirationCompleted
  queueGroupName = 'order-service'
  async onMessage(data: ExpirationCompletedEvent['data'], msg: any): Promise<void> {
    const order = await Order.findById(data.orderId).populate('ticket')
    
    if (!order) {
      throw new Error('Order not found')
    }
    if (order.status === OrderStatus.Complete) {
      return msg.ack()
    }
    order.set({ status: OrderStatus.Cancelled })
    await order.save()
    console.log("order cancelled!")
    await new OrderCancelledPublisher(this.client).publish({
      id: order.id,
      status: OrderStatus.Cancelled,
      version: order.version,
      ticket: {
        id: order.ticket.id.toString(),
      }
    })
    msg.ack()

  }

}