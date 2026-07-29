import { AbstractPublisher, Subjects, TicketCreatedEvent } from '@ddticketing/common'

export class TicketCreatedPublisher extends AbstractPublisher<TicketCreatedEvent> {
  subject = Subjects.TicketCreated
}