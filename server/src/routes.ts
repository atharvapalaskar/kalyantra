import { Router } from 'express';
import { moves } from './bot-moves';

let routes = Router();

routes.use('/moves/:move', moves)

export default routes;