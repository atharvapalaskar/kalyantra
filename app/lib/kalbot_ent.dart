import 'enums.dart';

class Kalyantra {

 
  String myName = 'Atharva'; 
  BotStatus status = BotStatus.notReady;
  String taskBy = '--';
  String taskName = '--';   
  String recentPhoto = '--'; 
  String move = BotMoves().halt; 
  String currentTask = '--';
  String lastTask = '--';
  String nextTask = '--';
  
  double totalCm = 0;
  double cmAway = 0;
  double pilotCM = 0;
  double pilotCMprog = 0;

  bool frontClear = true;
  bool backClear = true;
  bool moving = false;
  bool pilot = false;
  bool mic = true;
  bool returning = false; 
  bool camera = true;
  bool botMic = true;

  bool clickingPic = false;  
  bool photoViewerActive = false;
}