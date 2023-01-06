//WATCH OUT ** PINS ARE DIFFERENT IN THIS PROJECT AS OF THE CIRCUIT DIAGRAM FOR PYSERVER
//REFER services/kalyantrast.service to create system service

import * as express from "express";
import routes from "./routes";
import espeak, { EspeakOptions } from "./utils/espeakcmd";
const ngrok = require('ngrok');
require('dotenv').config();

const main = async()=> {
  
    console.log("starting kalyantra")   

    const app = express();
    const server = require('http').Server(app); 
    
    app.use(express.json());
    app.use(express.text());
    app.use(express.urlencoded({extended: true}));   
    app.use("/", routes);  

    server.listen(3004,async()=>{
       console.log("started kalyantra node server at port: "+ process.env.PORT)
       try {
            await ngrok.kill();
            setTimeout(async()=>{
                const url = await ngrok.connect({addr:process.env.PORT,authtoken:process.env.NGROK_TOKEN,name:'decv1',region:'in'});
                console.log(url); 
                await espeak({speak:'I am ready'} as EspeakOptions);
            },400);
       } catch (error) {
        console.log("Unable to connect ngrok or espeak "+ error)
       }
        
    }); 

    process.on('SIGINT', _ => {  
        console.log("bye raspi"); 
        process.exit(1);
    });
}
  
main();
   