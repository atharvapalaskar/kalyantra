const main = async()=> {
  
    console.log("starting node server") 

    function routesHandler (req, res) {  
        if (req.url == '/a'){
            res.writeHead(200, {'Content-Type': 'text/plain'}); 
            res.write('Hi found a route');  
            return res.end(); 
        } else if (req.url == '/'){ 
            res.writeHead(200, {'Content-Type': 'text/plain'}); 
            res.write('Hi from raspi');  
            return res.end(); 
        } else {
            res.writeHead(404, {'Content-Type': 'text/plain'});
            return res.end("404 Not Found") 
        } 
    }

    const server = require('http').Server(routesHandler); 
        server.listen(3004,()=>{
        console.log("started raspi node server at port 3004")
    }); 

    process.on('SIGINT', _ => {  
        console.log("bye raspi"); 
        process.exit(1);
    });
}
  
main();
   