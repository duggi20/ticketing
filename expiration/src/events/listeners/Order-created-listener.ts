import { AbstractListener, OrderCreatedEvent, Subjects } from "@ddticketing/common";
import { ExpirationQueue } from "../../queues/Expiration-queues";


export class OrderCreatedListener extends AbstractListener<OrderCreatedEvent> {
  subject: Subjects.OrderCreated = Subjects.OrderCreated
  queueGroupName = 'expiration-service'
  async onMessage(data: OrderCreatedEvent['data'], msg: any): Promise<void> {
    console.log('Event data in expiration service!', data)
    
    await ExpirationQueue.add({
      orderId: data.id
    }, {
      delay: 1 * 60 * 1000 // 1 minute
    })
    msg.ack()
  }
}