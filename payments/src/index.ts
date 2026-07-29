import 'express-async-errors'
import mongoose from 'mongoose'
import { app } from './App'
import { natsWrapper } from './nats-wrapper'
import { OrderCreatedListener } from './listeners/Order-created-listener'
import { OrderCancelledListener } from './listeners/Order-cancelled-listener'
const PORT = process.env.PORT || 3000

const start = async () => {
  try {
    await mongoose.connect('mongodb://payments-mongo-svc:27017/payments')
    console.log('Connected to MongoDB')

    await natsWrapper.connect('ticketing', 'payments-service', 'http://nats-srv:4222')
    await new OrderCreatedListener(natsWrapper.client).listen()
    await new OrderCancelledListener(natsWrapper.client).listen()
    app.listen(PORT, () => {
      console.log(`Payments service listening on http://localhost:${PORT}`)
    })
  } catch (err) {
    console.error('Failed to start payments service', err)
  }
}

start()

export default app
