import { AbstractPublisher, Subjects, OrderCreatedEvent } from '@ddticketing/common'

export class OrderCreatedPublisher extends AbstractPublisher<OrderCreatedEvent> {
  subject: Subjects.OrderCreated = Subjects.OrderCreated
}
