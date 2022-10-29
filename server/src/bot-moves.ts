import {Request, Response} from 'express';
import {espeak,EspeakOptions} from './utils/espeakcmd';
import { motorENA, motorENB, motorIN1, motorIN2, motorIN3, motorIN4 } from './utils/gpios';
 
export const moves = async(req: Request,res:Response)=>{
        
    console.log(req.params.move);
    
    try {
        
        motorENA.writeSync(1);
        motorENB.writeSync(1);

        switch(req.params.move){ 

            case 'forward': 
            //all motors forward 
                motorIN1.writeSync(1);
                motorIN2.writeSync(0);
                motorIN3.writeSync(1);
                motorIN4.writeSync(0);
                espeak({speak:'Moving forward'} as EspeakOptions);
            break;

            case 'backward': 
                //all motors backward
                motorIN1.writeSync(0);
                motorIN2.writeSync(1);
                motorIN3.writeSync(0);
                motorIN4.writeSync(1);
                espeak({speak:'Moving backward'} as EspeakOptions);
            break;
            
            case 'left-front':  
                //right motors front
                motorIN1.writeSync(1);
                motorIN2.writeSync(0);
                motorIN3.writeSync(0);
                motorIN4.writeSync(0);
                espeak({speak:'Moving left-front'} as EspeakOptions);
            break;

            case 'right-front':  
                //left motors front
                motorIN1.writeSync(0);
                motorIN2.writeSync(0);
                motorIN3.writeSync(1);
                motorIN4.writeSync(0);
                espeak({speak:'Moving right-front'} as EspeakOptions);
            break;

            case 'left-back':  
                //right motors back
                motorIN1.writeSync(0);
                motorIN2.writeSync(1);
                motorIN3.writeSync(0);
                motorIN4.writeSync(0);
                espeak({speak:'Moving left-back'} as EspeakOptions);
            break;

            case 'right-back':  
                //left motors back
                motorIN1.writeSync(0);
                motorIN2.writeSync(0);
                motorIN3.writeSync(0);
                motorIN4.writeSync(1);
                espeak({speak:'Moving right-back'} as EspeakOptions);
            break;

            case 'halt': //or break
                motorIN1.writeSync(0);
                motorIN2.writeSync(0);
                motorIN3.writeSync(0);
                motorIN4.writeSync(0);
                espeak({speak:'Halt'} as EspeakOptions);
            break;

            default:
                throw 'unknown move';
        }

     } catch (error) { 
        return res.status(400).send({
            'status': 'error',
            'msg': "can't move",
            'err': error 
         })
     }

     return res.status(200).send({
        'status': 'success',
        'msg': 'ok'
     })

 }


