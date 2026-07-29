
import {MongoMemoryServer} from 'mongodb-memory-server';
import mongoose from 'mongoose';
import { app } from '../App';
import { beforeAll, describe, it, expect, beforeEach ,afterAll} from '@jest/globals';


process.env.JWT_KEY = 'test_jwt_secret';
let mongoServer:any;

beforeAll(async () => {
     mongoServer = await MongoMemoryServer.create();
    const mongoUri = mongoServer.getUri();
    await mongoose.connect(mongoUri);
})


beforeEach(async () => {
if (mongoose.connection.db) {
    const collections = await mongoose.connection.db.collections();
    for (let collection of collections) {
        await collection.deleteMany({});
    }
}
})

afterAll(async () => {
    await mongoose.connection.close();
    await mongoServer.stop();
})