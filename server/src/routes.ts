import { Router } from 'express';
import { moves } from './bot-moves';
import { statusCheck } from './bot-status';

let routes = Router();

routes.post('/moves/:move', moves); 
routes.get('/bot-status/:check', statusCheck);

export default routes;