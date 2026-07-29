import { AbstractPublisher, Subjects, OrderCancelledEvent } from '@ddticketing/common'

export class OrderCancelledPublisher extends AbstractPublisher<OrderCancelledEvent> {
  subject: Subjects.OrderCancelled = Subjects.OrderCancelled
}








