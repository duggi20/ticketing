import Stripe from 'stripe'

const stripeKey = process.env.STRIPE_KEY
if (!stripeKey) {
  throw new Error('STRIPE_KEY must be defined')
}

export const stripe = new Stripe(stripeKey, {
  apiVersion: '2026-06-24.dahlia',
})
