import { AbstractListener, Subjects , OrderCreatedEvent, OrderStatus,} from "@ddticketing/common";
import {Ticket} from '../../models/ticket'
import {TicketUpdatedPublisher} from '../TicketUpdatedPublisher'

export class OrderCreatedListener extends AbstractListener<OrderCreatedEvent> {
  subject: Subjects.OrderCreated = Subjects.OrderCreated
    queueGroupName = 'ticket-service'
    async onMessage(data: OrderCreatedEvent['data'], msg?: any): Promise<void> {
        const ticket=await Ticket.findById(data.ticket.id)
        if(!ticket){
            throw new Error('Ticket not found')
        }
        ticket.set('orderId', data.id);
        await ticket.save();

      await new TicketUpdatedPublisher(this.client).publish({
        id: ticket.id,
        title: ticket.title,
        price: ticket.price,
        userId: ticket.userId,
        version: ticket.version,
        orderId: ticket.orderId,
      })
        if (typeof msg?.ack === 'function') {
        msg.ack()
        }
    }
}