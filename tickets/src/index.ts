import 'express-async-errors';
import mongoose from 'mongoose';
import { app } from './App';
import {natsWrapper} from './nats-wrapper';
import { OrderCreatedListener } from './events/listeners/Order-created-listener';
import { OrderCancelledListener } from './events/listeners/Order-cancelled-listener';
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Tickets service listening on http://localhost:${PORT}`);
});

const start = async () => {
  try {
    await natsWrapper.connect("ticketing", "ticketing-service", "http://nats-srv:4222");
    await mongoose.connect('mongodb://tickets-mongo-srv:27017/tickets');
    await new OrderCreatedListener(natsWrapper.client).listen();
    await new OrderCancelledListener(natsWrapper.client).listen();
    console.log('Connected to MongoDB');
  } catch (err) {
    console.error('Failed to connect to MongoDB', err);
  }
};

start();

export default app;
