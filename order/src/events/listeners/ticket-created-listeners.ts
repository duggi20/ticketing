import { AbstractListener, Subjects, TicketCreatedEvent } from '@ddticketing/common'
import { Ticket } from '../../models/ticket'

export class TicketCreatedListener extends AbstractListener<TicketCreatedEvent> {
  subject: Subjects.TicketCreated = Subjects.TicketCreated
  queueGroupName = 'order-service'

  async onMessage(data: TicketCreatedEvent['data'], msg: any): Promise<void> {
    const { id, title, price } = data

    const ticketObj = Ticket.build({
      id,
      title,
      price,
     
    })

    await ticketObj.save()
    console.log("ticket saved in orders===>", ticketObj)
    msg.ack()
  }
}