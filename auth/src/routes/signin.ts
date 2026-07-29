
import express,{Request,Response} from 'express';
const router= express.Router();
import jwt from 'jsonwebtoken';
import { body } from 'express-validator';
import { User } from '../models/user';
import { BadRequestError, RequestValidation } from '@ddticketing/common';
import { PasswordHashing } from '../services/PasswordHashing';


router.post('/api/users/signin',[
 body('email')
      .isEmail()
      .withMessage('Email must be valid'),   
   body('password')
      .trim()
      .notEmpty()
      .withMessage('Password must be provided')
],RequestValidation, async(req:Request, res:Response) => {
const { email, password } = req.body;
const existingUser = await User.findOne({ email });
if (!existingUser) {
  throw new BadRequestError('Invalid credentials');   
}

const passwordMatch = await PasswordHashing.compare(existingUser.password, password);
if (!passwordMatch) {
  throw new BadRequestError('Invalid credentials');     
} 

const userJwt = jwt.sign(
  {
    id: existingUser.id,   
      email: existingUser.email
   },
   process.env.JWT_KEY!
);
req.session = {
  jwt: userJwt
};
res.status(200).send(existingUser);

});

export {router as signInRouter};