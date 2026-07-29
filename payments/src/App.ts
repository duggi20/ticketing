import express from 'express'
import 'express-async-errors'
import { errorHandler, NotFoundError,currentUser } from '@ddticketing/common'
import { createChargeRouter } from './routes/new'
import cookieSession from 'cookie-session'
const app = express()

app.set('trust proxy', true)
app.use(express.json())


app.use(
  cookieSession({
    signed: false,
    secure: false,
  })
);
app.use(currentUser);
app.use(createChargeRouter)

app.get('/api/payments/health', (req, res) => {
  res.send({ status: 'ok' })
})

app.all('*', async () => {
  throw new NotFoundError()
})

app.use(errorHandler)

export { app }
