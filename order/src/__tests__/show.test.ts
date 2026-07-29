import request from 'supertest';
import express from 'express';
import mongoose from 'mongoose';
import { MongoMemoryServer } from 'mongodb-memory-server';
import { OrderStatus } from '@ddticketing/common';
import { errorHandler } from '@ddticketing/common';
import { showOrderRouter } from '../show';
import { Order } from '../models/orders';
import { Ticket } from '../models/ticket';

let mongo: MongoMemoryServer;

const app = express();
app.use(express.json());
app.use((req, _res, next) => {
  req.currentUser = { id: 'user-1', email: 'test@test.com' };
  next();
});
app.use(showOrderRouter);
app.use(errorHandler);

describe('Show order route', () => {
  beforeAll(async () => {
    mongo = await MongoMemoryServer.create();
    await mongoose.connect(mongo.getUri());
  });

  afterAll(async () => {
    await mongoose.disconnect();
    await mongo.stop();
  });

  beforeEach(async () => {
    await Order.deleteMany({});
    await Ticket.deleteMany({});
  });

  it('returns the order when the signed-in user owns it', async () => {
    const ticket = Ticket.build({ title: 'concert', price: 20, id: 'ticket-1' });
    await ticket.save();

    const order = Order.build({
      userId: 'user-1',
      status: OrderStatus.Created,
      expiresAt: new Date(),
      ticket: ticket as any,
    });
    await order.save();

    const response = await request(app)
      .get(`/api/orders/${(order as any).id}`)
      .expect(200);

    expect(response.body.userId).toEqual('user-1');
    expect(response.body.ticket.id).toEqual((ticket as any).id);
  });
});
