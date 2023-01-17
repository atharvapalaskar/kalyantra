
import 'dart:async';
import 'dart:io';
import 'package:app/enums.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:mqtt_client/mqtt_server_client.dart';
import 'package:mqtt_client/mqtt_client.dart'; 
import 'package:flutter/services.dart' show rootBundle;
import 'dart:typed_data'; 
  
final mqClient = MqttServerClient.withPort(dotenv.get('aws_url'), 'kalfl', 8883);
   
Future<bool> mqttConnect() async { 

  print(dotenv.get('aws_url'));
  mqClient.secure = true; 
  mqClient.keepAlivePeriod = 20; 
  mqClient.setProtocolV311(); 
  mqClient.logging(on: false);
 
  ByteData rootCA = await rootBundle.load('assets/cert/awsiotca.pem');
  ByteData deviceCert = await rootBundle.load('assets/cert/test001a.cert.pem');
  ByteData privateKey = await rootBundle.load('assets/cert/test001a.private.key');
  
  SecurityContext context = SecurityContext.defaultContext;
  context.setClientAuthoritiesBytes(rootCA.buffer.asUint8List());
  context.useCertificateChainBytes(deviceCert.buffer.asUint8List());
  context.usePrivateKeyBytes(privateKey.buffer.asUint8List());
    
  mqClient.securityContext = context;

  // Setup the connection Message
  final connMess = MqttConnectMessage()
      .withClientIdentifier('flutterpubsub')
      .startClean();
  mqClient.connectionMessage = connMess;

  // Connect the client
  try {
    print('Connecting to AWS IOT');
    await mqClient.connect();
  } catch (e) {
    mqClient.disconnect(); 
    throw('AWS conect exception, e:$e');
  }

  if (mqClient.connectionStatus!.state == MqttConnectionState.connected) {
    print('Connected to AWS IoT');
    
    //sometimes subs won't work with AWS without a cold sec after connection
    await MqttUtilities.asyncSleep(1);
   
    final builder = MqttClientPayloadBuilder();
    builder.addString('Hello World');
    
    List<String> subTop = subTopic.all;
    for (var topic in subTop) {
      mqClient.subscribe(topic, MqttQos.atLeastOnce);  
    } 

  } else {
    mqClient.disconnect(); 
    throw('ERROR MQTT client connection failed - disconnecting, state is ${mqClient.connectionStatus!.state}');
  } 

  return true;
}
 