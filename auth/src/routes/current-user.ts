import express from 'express';
import { currentUser, requireAuth } from '@ddticketing/common';
const router = express.Router();

router.get('/api/users/currentUser',currentUser,requireAuth, (req, res) => {
 res.send({ currentUser: req.currentUser || null });
   
});

export {router as currentUserRouter};