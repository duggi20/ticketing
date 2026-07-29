import { AbstractPublisher, Subjects, ExpirationCompletedEvent } from '@ddticketing/common'


export class ExpirationCompletedPublisher extends AbstractPublisher<ExpirationCompletedEvent> {
  subject: Subjects.ExpirationCompleted = Subjects.ExpirationCompleted
}