import { AbstractPublisher, Subjects, PaymentCreatedEvent } from '@ddticketing/common'

export class PaymentCreatedPublisher extends AbstractPublisher<PaymentCreatedEvent> {
  subject: Subjects.PaymentCreated = Subjects.PaymentCreated
}