import { AbstractListener, OrderCancelledEvent, Subjects } from "@ddticketing/common";
import { Ticket } from "../../models/ticket";
import { TicketUpdatedPublisher } from "../TicketUpdatedPublisher";


export class OrderCancelledListener extends AbstractListener<OrderCancelledEvent> {
    subject: Subjects.OrderCancelled = Subjects.OrderCancelled
    queueGroupName = 'ticket-service'

    async onMessage(data: OrderCancelledEvent['data'], msg: any): Promise<void> {
        console.log('Event data in ticket service!', data)
        const ticket = await Ticket.findById(data.ticket.id)
        console.log("Ticket found in ticket service!", ticket)
        if (!ticket) {
            throw new Error('Ticket not found')
        }
        ticket.set('orderId', undefined)
        await ticket.save()
        await new TicketUpdatedPublisher(this.client).publish({
       
                id: ticket.id,
                title: ticket.title,
                price: ticket.price,
                userId: ticket.userId,
                version: ticket.version,
                orderId: ticket.orderId,
        })
        msg.ack()
    }
}