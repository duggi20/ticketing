import { AbstractListener, Subjects, TicketUpdatedEvent } from '@ddticketing/common'
import { Ticket } from '../../models/ticket'


export class TicketUpdatedListener extends AbstractListener<TicketUpdatedEvent> {
  subject: Subjects.TicketUpdated = Subjects.TicketUpdated
  queueGroupName = 'order-service'
  async onMessage(data: TicketUpdatedEvent['data'], msg: any): Promise<void> {
  console.log("ticket updated event ==>",data)
    const ticket=await Ticket.updateOne({
        _id:data.id,
        version:data.version-1
    }, {
        $set: {
            title: data.title,
            price: data.price,
            version: data.version
        }
    })
    console.log("ticket updated===>",ticket)
    if(ticket.modifiedCount==0){
      throw new Error('Ticket not found')
    }
 
    if (typeof msg?.ack === 'function')
     {
      msg.ack()
    }
}
}