import { AbstractPublisher, Subjects, TicketUpdatedEvent } from '@ddticketing/common'

export class TicketUpdatedPublisher extends AbstractPublisher<TicketUpdatedEvent> {
  subject = Subjects.TicketUpdated
}
