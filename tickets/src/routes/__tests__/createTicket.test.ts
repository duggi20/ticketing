import request from 'supertest';
import express from 'express';
import cookieSession from 'cookie-session';
import { createTicketRouter } from '../createTicket';
import { errorHandler, currentUser } from '@ddticketing/common';
import { Ticket } from '../../models/ticket';
import { app as ticketApp } from '../../App';

const app = express();
app.use(
  cookieSession({
    signed: false,
    secure: false,
  })
);
app.use(express.json());
app.use(currentUser);
app.use(createTicketRouter);
app.use(errorHandler);

describe('Create Ticket route', () => {
  it('has a route handler listening to /api/tickets/create for POST requests', async () => {
    const response = await request(app).post('/api/tickets/create').send({});

    expect(response.status).not.toEqual(404);
  });

  it('handles the create ticket route through the main app', async () => {
    const response = await request(ticketApp).post('/api/tickets/create').send({});

    expect(response.status).not.toEqual(404);
  });

  it('returns 401 when the user is not signed in', async () => {
    await request(app)
      .post('/api/tickets/create')
      .send({
        title: 'concert',
        price: 20,
      })
      .expect(401);
  });

  it('returns 400 when the title or price is invalid', async () => {
    await request(app)
      .post('/api/tickets/create')
      .set('Cookie', global.signin())
      .send({
        title: '',
        price: 20,
      })
      .expect(400);

    await request(app)
      .post('/api/tickets/create')
      .set('Cookie', global.signin())
      .send({
        price: 20,
      })
      .expect(400);

    await request(app)
      .post('/api/tickets/create')
      .set('Cookie', global.signin())
      .send({
        title: 'concert',
        price: -5,
      })
      .expect(400);
  });

  it('creates a ticket with valid inputs', async () => {
    const title = 'concert';
    const price = 25;

    const ticketsBefore = await Ticket.find({});
    expect(ticketsBefore.length).toEqual(0);

    const response = await request(app)
      .post('/api/tickets/create')
      .set('Cookie', global.signin())
      .send({
        title,
        price,
      })
      .expect(201);

    expect(response.body.title).toEqual(title);
    expect(response.body.price).toEqual(price);

    const ticketsAfter = await Ticket.find({});
    expect(ticketsAfter.length).toEqual(1);
    expect(ticketsAfter[0].title).toEqual(title);
    expect(ticketsAfter[0].price).toEqual(price);
  });
});
