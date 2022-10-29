import 'dart:convert';

import 'package:app/components.dart';
import 'package:app/enums.dart';
import 'package:flutter/material.dart'; 
import 'package:http/http.dart' as http;

import 'env.dart';
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData( 
        primarySwatch: Colors.amber,
        backgroundColor: Colors.black,  
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key}); 

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  
  String? ngrokurl;
  NgConnectionState connectionState = NgConnectionState.disconnected;
  BotStatus botStatus = BotStatus.notReady;

  Future<void> connect() async {
    setState(() {connectionState = NgConnectionState.connecting;});
    try {
       var res = await http.get(Uri.parse('https://api.ngrok.com/tunnels'),headers:{'ngrok-version': '2',"authorization": "Bearer $ngrokApiKey"});
       var resBody = json.decode(res.body);

       if((resBody["tunnels"] as List).isEmpty){
         throw 'No url found' ;
       } else {//assuming you are using free plan only 1 tunnel can be opened 
          ngrokurl = resBody["tunnels"][0]['public_url'];
          print(ngrokurl);
          await botStatusApi('ready'); 
          if(botStatus == BotStatus.ready){  
             setState(() {connectionState = NgConnectionState.connected;});
          } else { throw 'Not ready';}
       }

    } catch (e) {
      print(e);
      setState(() {connectionState = NgConnectionState.disconnected;});
    } 
  }

  Future<void> move( String _movee) async {
     try { var res = await http.post(Uri.parse('$ngrokurl/moves/$_movee')); 
     if(json.decode(res.body)['msg']!='ok'){throw 'cant move';}
     } catch(e) { print(e); setState(() {connectionState = NgConnectionState.disconnected;});  }
   
  }
 
  Future<void> botStatusApi(String  _check) async {
      try {
         botStatus == BotStatus.checking;
         var res = await http.get(Uri.parse('$ngrokurl/bot-status/$_check'));
         if( json.decode(res.body)['msg'] == 'ready' ){botStatus = BotStatus.ready; return ; } 
          else{ throw 'Not ready';}
      } catch (e) {
        print(e); 
        return ;
      }
       
  }

  @override
  Widget build(BuildContext context) {
     
     return Scaffold(
      backgroundColor: Colors.black,
      appBar: PreferredSize(  preferredSize: const Size.fromHeight(60.0),
          child:SafeArea( child: Container(height: 60,color: Colors.amber,child:const Center(child: Text('Kalyantra: Well-being bot',style: TextStyle(fontSize: 16,color: Colors.black, fontWeight: FontWeight.w700,) )),) ),
      ),
      body: Center( child: 
       
          Stack(children: [
            
            MovesBox(move),

            connectionState != NgConnectionState.connected ?
            Container(width: MediaQuery.of(context).size.width,color: Colors.black.withOpacity(0.86),
             child:  
              
              connectionState == NgConnectionState.connecting?

               Column(crossAxisAlignment: CrossAxisAlignment.center,mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Text('Connecting',style: TextStyle(color: Colors.white),),
                  SizedBox(height: 12,),
                  CircularProgressIndicator()
              ],)
              
              : Column(crossAxisAlignment: CrossAxisAlignment.center,mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text('Not connected',style: TextStyle(color: Colors.white),),
                  TextButton(onPressed: ()async{ await connect();}, child: const Text('Tap to Connect :)'),)
              ],),
             
            )
            : const SizedBox()

          ],),
      
       )
    );
  }
}
 