import 'express-async-errors'
import mongoose from 'mongoose'
import { app } from './App'
import { natsWrapper } from './nats-wrapper'
import { TicketCreatedListener } from './events/listeners/ticket-created-listeners'
import { TicketUpdatedListener } from './events/listeners/ticket-updated-listener'
import { PaymentCreatedListener } from './events/listeners/Payment-created-listener'
import { ExpirationCompletedListener } from './events/listeners/expiration-completed-listener'
const PORT = process.env.PORT || 3000

const start = async () => {
  try {
    await natsWrapper.connect('ticketing', 'orders-service', 'http://nats-srv:4222')
    await mongoose.connect('mongodb://orders-mongo-srv:27017/orders')
    console.log('Connected to MongoDB')
    await new TicketCreatedListener(natsWrapper.client).listen()
    await new TicketUpdatedListener(natsWrapper.client).listen()
    await new PaymentCreatedListener(natsWrapper.client).listen()
    await new ExpirationCompletedListener(natsWrapper.client).listen()
    app.listen(PORT, () => {
      console.log(`Orders service listening on http://localhost:${PORT}`)
    })
  } catch (err) {
    console.error('Failed to start orders service', err)
  }
}

start()

export default app
