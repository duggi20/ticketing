
import 'express-async-errors';

import mongoose from 'mongoose';
import { app } from './App';

const PORT = process.env.PORT || 3000;


    app.listen(PORT, () => {
        console.log(`Auth service listening on http://localhost:${PORT}`);
    });


  const start = async () => {
    try {
        await mongoose.connect('mongodb://auth-mongo-srv:27017/auth');   
        console.log('Connected to MongoDB');
    } catch (err) {
        console.error('Failed to connect to MongoDB', err);
    }
};

start();

export default app;