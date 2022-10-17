import {Request, Response} from 'express';
import { motorENA, motorENB, motorIN1, motorIN2, motorIN3, motorIN4 } from './gpios';
 
export const moves = async(req: Request,res:Response)=>{
        
     console.log(req.params.move);
    
     motorENA.writeSync(1);
     motorENB.writeSync(1);

     switch(req.params.move){ 

        case 'forward': //move forward (clockwise)
            motorIN1.writeSync(1);
            motorIN2.writeSync(0);
            motorIN3.writeSync(1);
            motorIN4.writeSync(0);
        break;

        case 'backward': 
            motorIN1.writeSync(0);
            motorIN2.writeSync(1);
            motorIN3.writeSync(0);
            motorIN4.writeSync(1);
        break;
        
        case 'right-front':  
            motorIN1.writeSync(1);
            motorIN2.writeSync(0);
            motorIN3.writeSync(0);
            motorIN4.writeSync(0);
        break;

        case 'left-front':  
            motorIN1.writeSync(0);
            motorIN2.writeSync(0);
            motorIN3.writeSync(1);
            motorIN4.writeSync(0);
        break;

        case 'right-back':  
            motorIN1.writeSync(0);
            motorIN2.writeSync(1);
            motorIN3.writeSync(0);
            motorIN4.writeSync(0);
        break;

        case 'left-back':  
            motorIN1.writeSync(0);
            motorIN2.writeSync(0);
            motorIN3.writeSync(0);
            motorIN4.writeSync(1);
        break;

        case 'halt': //or break
            motorIN1.writeSync(0);
            motorIN2.writeSync(0);
            motorIN3.writeSync(0);
            motorIN4.writeSync(0);
        break;

     }

     return res.status(200).send({
        'status': 'done'
     })

 }


