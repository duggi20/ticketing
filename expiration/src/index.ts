import { app } from './App'
import { natsWrapper } from './nats-wrapper'
import {OrderCreatedListener} from './events/listeners/Order-created-listener'
const PORT = process.env.PORT || 3000

const start = async () => {
  try {
    await natsWrapper.connect('ticketing', 'expiration-service', 'http://nats-srv:4222')
    await new OrderCreatedListener(natsWrapper.client).listen()
    console.log('Expiration service connected to NATS')
    app.listen(PORT, () => {

      console.log(`Expiration service listening on http://localhost:${PORT}`)
    })
  } catch (err) {
    console.error('Failed to start expiration service', err)
  }
}

start()

export default app
