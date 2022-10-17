import * as express from "express";
import routes from "./routes";

const main = async()=> {
  
    console.log("starting node server")   

    const app = express();
    const server = require('http').Server(app); 
    
    app.use(express.json());
    app.use(express.text());
    app.use(express.urlencoded({extended: true}));   
    app.use("/", routes);  

    server.listen(3004,()=>{
        console.log("started raspi node server at port 3004")
    }); 

    process.on('SIGINT', _ => {  
        console.log("bye raspi"); 
        process.exit(1);
    });
}
  
main();
   