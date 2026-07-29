import { AbstractListener, Subjects, PaymentCreatedEvent, NotFoundError, OrderStatus } from '@ddticketing/common'
import {Order} from '../../models/orders'
export class PaymentCreatedListener extends AbstractListener<PaymentCreatedEvent> {
  subject: Subjects.PaymentCreated = Subjects.PaymentCreated
  queueGroupName = 'order-service'
  async onMessage(data: PaymentCreatedEvent['data'], msg: any) {
   const order = await Order.findById(data.orderId)

   if(!order){
    throw new NotFoundError()
   }
   order.set({status:OrderStatus.Complete})
   await order.save()
   msg.ack()
   

  }
}