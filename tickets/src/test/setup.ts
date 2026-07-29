import { beforeAll, beforeEach, afterAll } from '@jest/globals';
import { MongoMemoryServer } from 'mongodb-memory-server';
import mongoose from 'mongoose';
import jwt from 'jsonwebtoken';

process.env.JWT_KEY = 'test_jwt_secret';
let mongoServer: any;


declare global {
  var signin: () => string[];
}

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  const mongoUri = mongoServer.getUri();
  await mongoose.connect(mongoUri);
});

beforeEach(async () => {
  if (mongoose.connection.db) {
    const collections = await mongoose.connection.db.collections();
    for (const collection of collections) {
      await collection.deleteMany({});
    }
  }
});

afterAll(async () => {
  await mongoose.connection.close();
  await mongoServer.stop();
});


global.signin=()=>{
  // Build a JWT payload.  { id, email }
  const payload = {
    id: new mongoose.Types.ObjectId().toHexString(),
    email: 'test@example.com'
  };
  // Sign the JWT
  const token = jwt.sign(payload, process.env.JWT_KEY!);
  const sessionToken= { jwt: token };
  // Turn that session into JSON
  const sessionJSON = JSON.stringify(sessionToken);
  const base64 = Buffer.from(sessionJSON).toString('base64');
  // Return the cookie string
  return [`session=${base64}`];
};
