import 'dart:convert';

import 'package:app/components.dart';
import 'package:app/enums.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart'; 
import 'package:http/http.dart' as http;
import 'package:speech_to_text/speech_recognition_result.dart';
import 'package:speech_to_text/speech_to_text.dart';

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
        fontFamily: GoogleFonts.pressStart2p().fontFamily,
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
 
  // speech
  SpeechToText _speechToText = SpeechToText();
  bool _speechEnabled = false;
  String recWords = '--';String lastrecWords = '--';

  @override
  void initState() {
    super.initState();
    _initSpeech();
  }
 
  void _initSpeech() async {
    _speechEnabled = await _speechToText.initialize(
      onStatus: (status) {
        switch (status) {
          case 'listening':
            setState(() { recWords = 'listening...';}); 
            break;
          case 'done':
             _onDone();
            break;
        } 
      },
    );
    setState(() {});
  }
 
  void _startListening() async {
    setState(() {lastrecWords = recWords;});
    await _speechToText.listen(onResult: _onSpeechResult);
    setState(() {});
  }
 
  void _stopListening() async {
    await _speechToText.stop();
    setState((){});
  }
 
  void _onSpeechResult(SpeechRecognitionResult result) { 
    setState(() { recWords = result.recognizedWords; });
    print('recWr $recWords');
  }
  
  void _onDone(){
     print('done');
     if(recWords.startsWith('move')){
        print('movess');
        print(recWords.split(' ')[1]);
        print(recWords.split(' ').length > 2);
        move(recWords.split(' ').length > 2? '${recWords.split(' ')[1]}-${recWords.split(' ')[2]}' : recWords.split(' ')[1] );
     }
  }

  //kalyantra apis
  String? ngrokurl;
  NgConnectionState connectionState = NgConnectionState.disconnected;

  BotStatus botStatus = BotStatus.notReady;
  String botMove = BotMoves().halt;
  String lastbotMove = '--';

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
      setState(() {lastbotMove = botMove; botMove = _movee; });
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
          child:SafeArea( child: Container(height: 60,color: Colors.amber,child:const Center(child: Text('Kalyantra: Well-being bot',style: TextStyle(fontSize: 12,color: Colors.black, fontWeight: FontWeight.w700,) )),) ),
      ),
      body: Padding(padding: const EdgeInsets.all(30), child: 
       
          Stack(children: [
            
            Column( mainAxisAlignment: MainAxisAlignment.spaceEvenly, children: [
                
                RichText( maxLines: 3,text: TextSpan(style: TextStyle(color: Colors.white,fontSize: 12,letterSpacing: 0.4,height: 2.6,fontFamily: GoogleFonts.pressStart2p().fontFamily),
                  children:[ 
                    TextSpan(text: 'Bot Move : $botMove',style:const TextStyle(color: Colors.amber,)),
                    TextSpan(text: '\n Last Move : $lastbotMove',style:const TextStyle(fontSize: 10,)),                  
                ])),
                
                MovesBox(move),

                Align(alignment: Alignment.centerLeft,child: Text('Voice cmd: $recWords',style:const TextStyle(color: Colors.amber,fontSize: 10,letterSpacing: 0.4,height: 1.6,),textAlign: TextAlign.left,)),
                Align(alignment: Alignment.centerLeft,child: Text('Last V-cmd: $lastrecWords ',style:const TextStyle(color: Colors.white,fontSize: 8,height: 1.6,),textAlign: TextAlign.left,)),
             
                // const SizedBox(height: 1,)
              ],),

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
      
       ),
       floatingActionButton: FloatingActionButton( 
        onPressed:
            // If not yet listening for speech start, otherwise stop
            _speechToText.isNotListening ? _startListening : _stopListening,
        tooltip: 'Listen',backgroundColor:  connectionState != NgConnectionState.connected ? Colors.amber.withOpacity(0.3) : Colors.amber,
        child: Icon(_speechToText.isNotListening ? Icons.mic_off : Icons.mic),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.miniCenterFloat,
    );
  }
}
 