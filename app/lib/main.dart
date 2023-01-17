import 'dart:convert';
 
import 'package:app/components/indicators.dart';
import 'package:app/components/photo_viewer.dart'; 
import 'package:app/enums.dart';
import 'package:app/kalbot_ent.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:google_fonts/google_fonts.dart';  
import 'package:ionicons/ionicons.dart';
import 'package:line_icons/line_icons.dart'; 
import 'package:speech_to_text/speech_to_text.dart';
import 'package:mqtt_client/mqtt_client.dart'; 
import 'package:flutter_svg/flutter_svg.dart';

import 'components/movesbox.dart';
import 'components/static_class.dart'; 
import 'firebase_options.dart';
import 'mqtt_util.dart';

void main() async{
  await dotenv.load(fileName: ".env"); 
  await Firebase.initializeApp(
  options: DefaultFirebaseOptions.currentPlatform,
  );
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
  SpeechToText speechToText = SpeechToText();
  bool speechEnabled = false;
  String recWords = '--'; 

  @override
  void initState() {
    super.initState();
    _initSpeech(); 
  }
 
  void _initSpeech() async {
    speechEnabled = await speechToText.initialize(
      onStatus: (status) {
        switch (status) {
          case 'listening':
            setState(() { recWords = 'listening...';}); 
            break;
          case 'done':
            srHandler('done');
            break;
        } 
      },
    );
    setState(() {});
  }
 
  void srHandler(evnt) async{
     switch (evnt) {
       case 'start':
         await speechToText.listen(onResult: (result) {
           setState((){recWords = result.recognizedWords;});
           print('recWr $recWords');
         });
         break;
         
      case 'stop':
         await speechToText.stop(); 
         setState((){});
         break; 
        
      case 'done':
        print('Done sr');
        if(recWords == 'listening...'){ setState(() {recWords = '--';});} 
        else { mqPublisher(pubTopic.vcmd, recWords);}
     }
  }  
   
  // MQ and Bot
  MqConnectionState connectionState = MqConnectionState.disconnected; 
  Kalyantra kalyantra = Kalyantra();
  String botSvg = BotSimulation().getSvg(); 
  bool showControls = false;

  void updateKalBotUi(){  
     botSvg = BotSimulation().getSvg(autoMode: kalyantra.pilot,moving: false);
  }

  Future<void> connect() async { 
    setState((){connectionState = MqConnectionState.connecting;}); 
    try {
       await mqttConnect();
       kalyantra.status == BotStatus.checking;
       mqPublisher(pubTopic.base,'check');      
       setState((){connectionState = MqConnectionState.connected; kalyantra.status = BotStatus.checking; }); 
       mqHandler();
    } catch (e) {
      print(e);
      setState((){connectionState = MqConnectionState.disconnected;});
      return;
    }   
  }
  
  mqHandler(){
      
    mqClient.updates!.listen((List<MqttReceivedMessage<MqttMessage>> c) {
      final recMess = c[0].payload as MqttPublishMessage; 
      final topic = c[0].topic;
      final payload = MqttPublishPayload.bytesToStringAsString(recMess.payload.message);
      print('topic:$topic, payload:$payload');  
      try{
        switch (topic) {
          case 'status':
            // eg {"data":"ready"}
            kalyantra.status = jsonDecode(payload)["data"] == 'ready' ? BotStatus.ready : BotStatus.notReady;
            print(kalyantra.status);
            break;

          case 'task':
            // eg {"data":{"taskName":"move forward 20 cm","currentTask":"move forward 20 cm","nextTask":"--","lastTask":"move right 20 cm","move":"forward","moving":true,"pilot":false}}
            dynamic data = jsonDecode(payload)["data"];
            kalyantra.taskName = data["taskName"];
            kalyantra.currentTask = data["currentTask"];
            kalyantra.nextTask = data["nextTask"];
            kalyantra.lastTask = data["lastTask"];
            kalyantra.move = data["move"];
            kalyantra.moving = data["moving"] as bool;
            kalyantra.pilot = data["pilot"] as bool;   
            // kalyantra.pilotCM = data["pilotCM"]; 
            break;

          case 'sensor':
            // eg {"data":{"frontClear":true,"backClear":false}}
            dynamic data = jsonDecode(payload)["data"];
            kalyantra.frontClear = data["frontClear"] as bool;
            kalyantra.backClear = data["backClear"] as bool; 
            // kalyantra.moving =  data["moving"] as bool;
            break;

          case 'cms':
            //eg {"data":{"pilotCMprog":2}}
            dynamic data = jsonDecode(payload)["data"];
            kalyantra.pilotCMprog = data["pilotCMprog"]; 
            break;

          case 'acks':
            print("event-acks: $payload");
            if (payload.startsWith('uploaded:')){
               kalyantra.recentPhoto = payload.split('uploaded:')[1].trim();
               print('recent Photo: ${kalyantra.recentPhoto} ');
               kalyantra.clickingPic = false;
            }
            break;
          case 'err':
            print("event-err: $payload");
            break; 
        } 

        setState(() { 
          botSvg = BotSimulation().getSvg(autoMode: kalyantra.pilot,frontClear: kalyantra.frontClear,backClear:kalyantra.backClear ,moving: kalyantra.moving);
        }); 

      }catch(e){
        print("err at mqHandler($topic): $e");
      }
    });

     //   mqClient.published!.listen((MqttPublishMessage message) {
    //   print( Published notification: topic is ${message.variableHeader!.topicName});
    // });

    mqClient.onDisconnected = (){
       setState(() { connectionState = MqConnectionState.disconnected; kalyantra.status = BotStatus.notReady;});
    };

  }
 
  mqPublisher(String topic,String msg){
       final builder = MqttClientPayloadBuilder();
       builder.addString(msg);
       mqClient.publishMessage(topic, MqttQos.atLeastOnce, builder.payload!); 
       if( topic == pubTopic.picam ){
         setState(() {
           kalyantra.clickingPic = true;
         });
       }  
  }
  
  Future<void> move( String movee) async { 
       mqPublisher(pubTopic.move,movee);
  }
  
  
  @override
  Widget build(BuildContext context) {
   
     return Scaffold(
      backgroundColor: Colors.black,
      appBar: PreferredSize( preferredSize: const Size.fromHeight(60.0),
          child:SafeArea(child: Container(height: 60,color: Colors.amber,child:const Center(child: Text('Kalyantra: Well-being bot',style: TextStyle(fontSize: 12,color: Colors.black, fontWeight: FontWeight.w700,) )),) ),
      ),
      body: Padding(padding: const EdgeInsets.all(30), child: 
       
          Stack(children: [
            
            Column( mainAxisAlignment: MainAxisAlignment.spaceAround, children: [ 
               Text('Hi: ${kalyantra.myName}',style:const TextStyle(color: Colors.amber,fontSize: 8,letterSpacing: 0.4,),textAlign: TextAlign.left,),
                // Bot Simulation and Indicators
                Row(mainAxisAlignment: MainAxisAlignment.spaceBetween,children:[ 
                    // Bot Simulation
                    Stack(alignment: Alignment.center,children: [ 
                      // Bot svg
                      SvgPicture.string(botSvg,height: 230,width: 190,),
                      // Task indicators
                      SizedBox(height: 190,
                        child: Column( mainAxisAlignment: MainAxisAlignment.spaceAround,children: [
                            
                            Column(children: [
                                Container(alignment: Alignment.center,child:const Text('Next',style: TextStyle(color: Colors.white,fontSize: 8,letterSpacing: 0.2,height: 1.6,),textAlign: TextAlign.left,)),
                                const SizedBox(height:6), 
                                TaskIndicatorWidget(task:kalyantra.nextTask,moving: kalyantra.moving), 
                            ]), 
                             
                            TaskIndicatorWidget(main: true,task: kalyantra.currentTask,moving: kalyantra.moving, cmProgress: kalyantra.pilotCMprog,),
                
                            Column(children: [
                                Container(alignment: Alignment.center,child:const Text('Last',style: TextStyle(color: Colors.white,fontSize: 8,letterSpacing: 0.2,height: 1.6,),textAlign: TextAlign.left,)),
                                const SizedBox(height:6), 
                                TaskIndicatorWidget(task:kalyantra.lastTask,moving: kalyantra.moving,), 
                            ]),
                
                          ]),
                      ), 
                    ]),
                    // Status Indicators
                    SizedBox(height: 210,
                      child: Column(mainAxisAlignment: MainAxisAlignment.spaceBetween, children:[
                          StatusIndicatorWidget(text:'Camera',active: kalyantra.camera,size: 25,icon: Ionicons.camera_outline,),
                          StatusIndicatorWidget(text:'Bot Mic',active: kalyantra.botMic,size: 25,icon: Ionicons.mic_circle_outline,),
                          StatusIndicatorWidget(text:'Auto Pilot',active: kalyantra.pilot,size: 25,icon: Ionicons.person_circle_outline,),
                          StatusIndicatorWidget(text:'Returning',active: kalyantra.returning,size: 25,icon: Ionicons.reload_circle_outline,),
                      ],),
                    )  
                ]), 

                Divider(thickness: 0.5, color: Colors.amber,),
              
                SizedBox(height: 60,
                  child: Column(mainAxisAlignment: MainAxisAlignment.spaceEvenly,children: [
                    Align(alignment: Alignment.centerLeft,child: Text('Total travel: ${kalyantra.totalCm}',style:const TextStyle(color: Colors.amber,fontSize: 8,letterSpacing: 0.4,),textAlign: TextAlign.left,)),
                    Align(alignment: Alignment.centerLeft,child: Text('Away from origin: ${kalyantra.cmAway}',style:const TextStyle(color: Colors.amber,fontSize: 8,letterSpacing: 0.4,),textAlign: TextAlign.left,)),
                    Align(alignment: Alignment.centerLeft,child: Text('Task initated by: ${kalyantra.taskBy}',style:const TextStyle(color: Colors.amber,fontSize: 8,letterSpacing: 0.4,),textAlign: TextAlign.left,)),
                    Align(alignment: Alignment.centerLeft,child: Text('Task name: ${kalyantra.taskName}',style:const TextStyle(color: Colors.amber,fontSize: 8,letterSpacing: 0.4,height: 1.6),textAlign: TextAlign.left,)),

                  ],),
                ),

                Row( mainAxisAlignment: MainAxisAlignment.spaceAround,crossAxisAlignment: CrossAxisAlignment.start,children: [
                    GestureDetector(onTap: (){ kalyantra.clickingPic? (){} : mqPublisher(pubTopic.picam, 'click');}, 
                       child: StatusIndicatorWidget(active: !kalyantra.clickingPic, size: 30,text: 'Click',icon: LineIcons.retroCamera,)),
                    GestureDetector(onTap: kalyantra.clickingPic? (){}: ()async{    
                         setState(() { kalyantra.photoViewerActive = true;});
                         final imgUrl = await FirebaseStorage.instance.refFromURL("gs://${dotenv.get('fib_gs')}/${kalyantra.recentPhoto}").getDownloadURL();
                         print(imgUrl); 
                         kalyantra.photoViewerActive =  await photoViewer(context,imgUrl);
                         setState(() {});
                       },child: StatusIndicatorWidget(active: !kalyantra.photoViewerActive, size: 30,text: 'Recent \nPhoto',icon: LineIcons.photoVideo,ml: true,)),
                    const StatusIndicatorWidget(active: true, size: 30,text: 'Pilot \ntask +',icon: LineIcons.userEdit,ml: true,),  
                ],),

                SizedBox(height: 130,
                child:showControls ? 
              
                Column( children:[
                    MovesBox(move),const SizedBox(height: 20),
                    Row( mainAxisAlignment: MainAxisAlignment.spaceAround,children:[ 
                      StatusIndicatorWidget(active: true, size: 35,text: 'Return',icon: Ionicons.reload),
                      GestureDetector(onDoubleTap:()=> setState(() { showControls = false;}),child: StatusIndicatorWidget(active: true, size: 35,text: 'Exit',icon: LineIcons.alternateSignOut)),
                     ] )
                ])

                : Column(children: [
                    Align(alignment: Alignment.centerLeft,child: Text('App V-cmd: $recWords',style:const TextStyle(color: Colors.amber,fontSize: 8,letterSpacing: 0.4,height: 1.6,),textAlign: TextAlign.left,)),
                   
                    const SizedBox(height: 40,),
                    Row( mainAxisAlignment: MainAxisAlignment.spaceAround,crossAxisAlignment: CrossAxisAlignment.start,children: [
                        TextButton(style:TextButton.styleFrom( padding: EdgeInsets.zero,), onPressed: (){speechToText.isNotListening ? srHandler('start') : srHandler('stop');},
                          child:StatusIndicatorWidget(active: true, size: 30,text: 'Voice \nCmd',icon: speechToText.isNotListening ? Icons.mic_off : Icons.mic, ml: true,)),  
                        StatusIndicatorWidget(active: true, size: 30,text: 'Return',icon: Ionicons.reload,),  
                        TextButton(style:TextButton.styleFrom( padding: EdgeInsets.zero,), onPressed: ()=> setState(() { showControls = true;}),
                          child:StatusIndicatorWidget(active: true, size: 30,text: 'Control',icon: LineIcons.dharmachakra,ml: true,)) 
                    ],), 
                ]),
                )
            ],),

            // Overlay Screen
            kalyantra.status != BotStatus.ready ?
            Container(width: MediaQuery.of(context).size.width,color: Colors.black.withOpacity(0.86),
             child:  
                 
               connectionState == MqConnectionState.connecting?

               Column(crossAxisAlignment: CrossAxisAlignment.center,mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Text('Connecting',style: TextStyle(color: Colors.white),),
                  SizedBox(height: 12,),
                  CircularProgressIndicator()
              ],) 
             
              : connectionState == MqConnectionState.connected && kalyantra.status == BotStatus.checking ?
                 Column(crossAxisAlignment: CrossAxisAlignment.center,mainAxisAlignment: MainAxisAlignment.center,
                  children: const [
                    Text('Checking Bot status',style: TextStyle(color: Colors.white),),
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
    );
  }
}
 