import {Request, Response} from 'express';

export const statusCheck = async(req: Request,res:Response)=>{
        
    //currently basic device connection ready added can add 
    //multiple check for seprate components through gpio interactions
      
    try {

      switch (req.params.check) {
        case 'ready':
            res.status(200).send({
                'status': 'success',
                'msg': 'ready'
            });
        break;  
      } 
      
     } catch (error) { 
        return res.status(400).send({
            'status': 'error',
            'msg': "not ready",
            'err': error.data
         })
     }
 
 }


