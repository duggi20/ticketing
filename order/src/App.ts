import express from 'express'
import { newOrderRouter } from './routes/new'
import { showOrderRouter } from './routes/show'
import { deleteOrderRouter } from './routes/delete'
import cookieSession from 'cookie-session'
import { errorHandler, NotFoundError, requireAuth, currentUser } from '@ddticketing/common'
const app = express()

app.set('trust proxy', true);
app.use(
  cookieSession({
    signed: false,
    secure: false,
  })
);
app.use(express.json())
app.use(currentUser);
app.use(newOrderRouter)
app.use(showOrderRouter)
app.use(deleteOrderRouter)

app.get('/api/orders/health',requireAuth, (req, res) => {
  res.send({ status: 'ok' })
})

app.all('*', () => {
  throw new NotFoundError()
})

app.use(errorHandler)

export { app }
