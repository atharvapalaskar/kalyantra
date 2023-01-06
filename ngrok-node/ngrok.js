// ONLY REQUIRED IF WORKING WITH FLASK APPLICATION AND PYNGROK IS NOT WORKING
// REFER services/ngrokn.service to create system service

const ngrok = require('ngrok');
require('dotenv').config();

main = async()=>{
    try {
        await ngrok.kill();
        setTimeout(async()=>{
            const url = await ngrok.connect({addr:3004,authtoken:process.env.NGROK_TOKEN,name:'decv1',region:'in'});
            console.log(url);
            const api = ngrok.getApi();
            const tunnels = await api.listTunnels();
            console.log(tunnels["tunnels"][0]["public_url"]);
            console.log(tunnels["tunnels"][0]["config"])  
        },400);
    } catch (error) {
        console.log("Unable to connect ngrok or espeak "+ error)
    }
}

main();
