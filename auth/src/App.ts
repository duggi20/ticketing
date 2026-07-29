import express from 'express';
import { currentUserRouter } from './routes/current-user';
import { signInRouter } from './routes/signin';
import { signOutRouter } from './routes/signout';
import { signUpRouter } from './routes/signup';
import { errorHandler, NotFoundError } from '@ddticketing/common';
import cookieSession from 'cookie-session';

const app = express();
app.set('trust proxy', true); // Trust the first proxy (e.g., ingress-nginx)
app.use(
    cookieSession({
        signed: false,
        secure: false, // Use secure cookies in production
    })
);
// Use Express built-in JSON body parser instead of importing from 'body-parser'
app.use(express.json());

app.use(currentUserRouter);
app.use(signInRouter);
app.use(signOutRouter);
app.use(signUpRouter);
app.all('*', (req, res) => {
    throw new NotFoundError();
});

app.use(errorHandler);

app.use((req, res) => {
    res.status(200).json({ message: 'hi there' });
});


export { app };
