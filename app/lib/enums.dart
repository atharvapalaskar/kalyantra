 
enum MqConnectionState {
  connecting,
  connected,
  disconnected
}

enum BotStatus {
  checking,
  ready,
  notReady,
  ok
}

class BotMoves {

   String get halt => 'halt';
   String get forward => 'forward';
   String get backward => 'backward';
   String get right => 'right';
   String get left => 'left';

   String get rightfront => 'right-front';
   String get rightback => 'right-back';
   String get leftfront => 'left-front';
   String get leftback => 'left-back';

   List<String> get all => [halt,forward,backward,left,right];
}

class SubTopics {
   String get status => 'status'; 
   String get acks => 'acks'; 
   String get task => 'task';
   String get sensor => 'sensor';  
   String get cms => 'cms';  
   String get err => 'err'; 
   List<String> get all => [status,acks,task,sensor,cms,err]; 
} 

class PubTopics {
  String get base => 'base'; 
  String get move => 'move'; 
  String get picam => 'picam'; 
  String get vcmd => 'vcmd';
  List<String> get all => [base,move,picam,vcmd];
}

PubTopics pubTopic = PubTopics();
SubTopics subTopic = SubTopics();