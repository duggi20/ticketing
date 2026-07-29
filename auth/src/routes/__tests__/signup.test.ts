import request from 'supertest';
import { app } from '../../App';


it('returns a 201 on successful signup', async () => {

    return request(app)
        .post('/api/users/signup')
        .send({
            email: 'ddogra@gmail.com',
            password: 'password'
        })
        .expect(201);
})