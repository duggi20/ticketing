import express from 'express';
import { errorHandler, NotFoundError,currentUser, } from '@ddticketing/common';
import cookieSession from 'cookie-session';
import { createTicketRouter } from './routes/createTicket';
import { getTicketRouter } from './routes/getTicket';
import { getAllTicketsRouter } from './routes/getAllTickets';
import { updateTicketRouter } from './routes/updateTickets';
const app = express();

app.set('trust proxy', true);

app.use(
  cookieSession({
    signed: false,
    secure: false,
  })
);

app.use(express.json());
app.use(currentUser);
app.use(createTicketRouter);
app.use(getTicketRouter);
app.use(getAllTicketsRouter);
app.use(updateTicketRouter);
app.all('*', (req, res) => {
  throw new NotFoundError();
});

app.use(errorHandler);
export { app };
