import express from 'express'
import 'express-async-errors'
import { errorHandler } from '@ddticketing/common'

const app = express()

app.set('trust proxy', true)
app.use(express.json())

app.all('*', (req, res) => {
  res.status(404).send({ message: 'Not found' })
})

app.use(errorHandler)

export { app }
