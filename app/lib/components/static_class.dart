import 'package:app/enums.dart';
import 'package:flutter/material.dart'; 
import 'package:ionicons/ionicons.dart'; 

class BotSimulation {  

  final String bodyAutoOn = '''<svg xmlns="http://www.w3.org/2000/svg" width="217.468" height="254.459" viewBox="0 0 217.468 254.459">
  <g id="Body" data-name="Body m" transform="translate(1.92)">
    <g id="Group_14" data-name="Group 14" transform="translate(0 4.575)">
      <path id="Union_1" data-name="Union 1" d="M-37,2101.324H-2.412V1939.044H-37s30.012-42.9,112.649-41.589,101.332,41.589,101.332,41.589H141.32v162.281h35.662S158.288,2141.6,75.65,2142.914q-1.869.03-3.7.03C-7.885,2142.943-37,2101.324-37,2101.324Z" transform="translate(37 -1897.425)" fill="none" stroke="#FFC107" stroke-width="2.5"/>
    </g>''';

  final String bodyAutoOff = '''<svg xmlns="http://www.w3.org/2000/svg" width="217.468" height="254.459" viewBox="0 0 217.468 254.459">
  <g id="Body" data-name="Body m" transform="translate(1.92)">
    <g id="Group_14" data-name="Group 14" transform="translate(0 4.575)">
      <path id="Union_1" data-name="Union 1" d="M-37,2101.324H-2.412V1939.044H-37s30.012-42.9,112.649-41.589,101.332,41.589,101.332,41.589H141.32v162.281h35.662S158.288,2141.6,75.65,2142.914q-1.869.03-3.7.03C-7.885,2142.943-37,2101.324-37,2101.324Z" transform="translate(37 -1897.425)" fill="none" stroke="#7e7e7e" stroke-width="2"/>
    </g>''';

  final String frontSensorActive ='''
    <g id="Front_sensor" data-name="Front sensor" transform="translate(77.446 0)" stroke="#0aff13" stroke-width="3">
      <rect width="59" height="14" rx="6" stroke="none"/>
      <rect x="1" y="1" width="57" height="9.5" rx="5" fill="none"/>
    </g>''';

  final String frontSensorDeactive ='''
    <g id="Front_sensor" data-name="Front sensor" transform="translate(77.446 0)" stroke="#FF0A0A" stroke-width="3.5">
      <rect width="59" height="14" rx="6" stroke="none"/>
      <rect x="1" y="1" width="57" height="9.5" rx="5" fill="none"/>
    </g>''';
  
  final String backSensorActive='''
    <g id="Back_sensor" data-name="Back Sensor" transform="translate(79.549 242.542)" stroke="#0aff13" stroke-width="3">
      <rect width="59" height="14" rx="6" stroke="none"/>
      <rect x="1" y="1" width="57" height="9.5" rx="5" fill="none"/>
    </g>
  </g>''';

  final String backSensorDeactive='''
    <g id="Back_sensor" data-name="Back Sensor" transform="translate(79.549 242.542)" stroke="#FF0A0A" stroke-width="3.5">
      <rect width="59" height="14" rx="6" stroke="none"/>
      <rect x="1" y="1" width="57" height="9.5" rx="5" fill="none"/>
    </g>
  </g>''';
  
  final String wheelsMoving='''
  <g id="Wheels" data-name="Wheels" transform="translate(3.92 53.275)" fill="#080" stroke="#fff" stroke-width="2">''';

  final String wheelsHalt='''
  <g id="Wheels" data-name="Wheels" transform="translate(3.92 53.275)" fill="#474847" stroke="#fff" stroke-width="2">''';
  
  final String wheels='''
    <g id="Rectangle_18" data-name="Rectangle 18" transform="translate(29.442 0) rotate(90)" >
      <rect width="56.78" height="29.442" rx="10" stroke="none"/>
      <rect x="1" y="1" width="54.78" height="27.442" rx="9" fill="none"/>
    </g>
    <g id="Rectangle_19" data-name="Rectangle 19" transform="translate(29.442 91.829) rotate(90)" >
      <rect width="56.78" height="29.442" rx="10" stroke="none"/>
      <rect x="1" y="1" width="54.78" height="27.442" rx="9" fill="none"/>
    </g>
    <g id="Rectangle_20" data-name="Rectangle 20" transform="translate(208.895 0) rotate(90)" >
      <rect width="56.78" height="29.442" rx="10" stroke="none"/>
      <rect x="1" y="1" width="54.78" height="27.442" rx="9" fill="none"/>
    </g>
    <g id="Rectangle_21" data-name="Rectangle 21" transform="translate(208.895 91.829) rotate(90)" >
      <rect width="56.78" height="29.442" rx="10" stroke="none"/>
      <rect x="1" y="1" width="54.78" height="27.442" rx="9" fill="none"/>
    </g>
  </g>
</svg>
''';
  
   
   String getSvg({bool autoMode = false,bool frontClear= true, bool backClear=true,bool moving = false}){ 
     return [autoMode? bodyAutoOn : bodyAutoOff,
             frontClear? frontSensorActive: frontSensorDeactive,
             backClear? backSensorActive: backSensorDeactive,
             moving? wheelsMoving: wheelsHalt,
             wheels].join();
   }

}

class MovingArrows {

   final String halt = '''<svg xmlns="http://www.w3.org/2000/svg" width="31" height="32" viewBox="0 0 31 32">
  <g id="Group_24" data-name="Group 24" transform="translate(-159.75 -262.5)">
    <g id="Rectangle_33" data-name="Rectangle 33" transform="translate(159.75 262.5)" fill="#434343" stroke="#fff" stroke-width="1">
      <rect width="31" height="32" rx="8" stroke="none"/>
      <rect x="0.5" y="0.5" width="30" height="31" rx="7.5" fill="none"/>
    </g>
    <g id="Rectangle_34" data-name="Rectangle 34" transform="translate(165.75 268.5)" fill="#434343" stroke="#fff" stroke-width="1">
      <rect width="19" height="20" rx="4" stroke="none"/>
      <rect x="0.5" y="0.5" width="18" height="19" rx="3.5" fill="none"/>
    </g>
  </g>
</svg>
''';

  final String forwardMoving ='''<svg xmlns="http://www.w3.org/2000/svg" width="29.11" height="34.674" viewBox="0 0 29.11 34.674">
    <path id="Path_25" data-name="Path 25" d="M153.87-704.1l-9.839-.191,14.363-19.151,13.747,19.151h-9.849v14.523H153.67Z" transform="translate(-143.531 723.943)" fill="#0a8000" stroke="#0aff13" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" stroke-dasharray="2"/>
  </svg>''';

  final String forwardHalt ='''<svg xmlns="http://www.w3.org/2000/svg" width="29.11" height="34.674" viewBox="0 0 29.11 34.674">
    <path id="Path_25" data-name="Path 25" d="M153.87-704.1l-9.839-.191,14.363-19.151,13.747,19.151h-9.849v14.523H153.67Z" transform="translate(-143.531 723.943)" fill="#800000" stroke="#0aff13" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" stroke-dasharray="2"/>
  </svg>''';

  final String rightMoving ='''<svg xmlns="http://www.w3.org/2000/svg" width="37.396" height="31.382" viewBox="0 0 37.396 31.382">
  <path id="Path_33" data-name="Path 33" d="M154.665-702.538l-10.634-.206,15.524-20.7,14.858,20.7H163.768v15.7h-9.319Z" transform="translate(-686.547 -143.531) rotate(90)" fill="#0a8000" stroke="#0aff13" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" stroke-dasharray="2"/>
</svg>''';

  final String rightHalt ='''<svg xmlns="http://www.w3.org/2000/svg" width="37.396" height="31.382" viewBox="0 0 37.396 31.382">
  <path id="Path_33" data-name="Path 33" d="M154.665-702.538l-10.634-.206,15.524-20.7,14.858,20.7H163.768v15.7h-9.319Z" transform="translate(-686.547 -143.531) rotate(90)" fill="#800000" stroke="#0aff13" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" stroke-dasharray="2"/>
</svg>'''; 

  final String leftMoving ='''<svg xmlns="http://www.w3.org/2000/svg" width="37.396" height="31.382" viewBox="0 0 37.396 31.382">
  <path id="Path_33" data-name="Path 33" d="M10.634,15.491,0,15.7,15.524,36.4,30.382,15.7H19.738V0H10.419Z" transform="translate(36.896 0.5) rotate(90)" fill="#0a8000" stroke="#0aff13" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" stroke-dasharray="2"/>
</svg>''';

  final String leftHalt ='''<svg xmlns="http://www.w3.org/2000/svg" width="37.396" height="31.382" viewBox="0 0 37.396 31.382">
  <path id="Path_33" data-name="Path 33" d="M10.634,15.491,0,15.7,15.524,36.4,30.382,15.7H19.738V0H10.419Z" transform="translate(36.896 0.5) rotate(90)" fill="#800000" stroke="#0aff13" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" stroke-dasharray="2"/>
</svg>'''; 

  final String backwardMoving ='''<svg xmlns="http://www.w3.org/2000/svg" width="31.382" height="37.396" viewBox="0 0 31.382 37.396">
  <path id="Path_25" data-name="Path 25" d="M154.665-707.952l-10.634.206,15.524,20.7,14.858-20.7H163.768v-15.7h-9.319Z" transform="translate(-143.531 723.943)" fill="#0a8000" stroke="#0aff13" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" stroke-dasharray="2"/>
</svg>''';

  final String backwardHalt ='''<svg xmlns="http://www.w3.org/2000/svg" width="31.382" height="37.396" viewBox="0 0 31.382 37.396">
  <path id="Path_25" data-name="Path 25" d="M154.665-707.952l-10.634.206,15.524,20.7,14.858-20.7H163.768v-15.7h-9.319Z" transform="translate(-143.531 723.943)" fill="#800000" stroke="#0aff13" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" stroke-dasharray="2"/>
</svg>'''; 

 
   String getSvg({String move='halt',bool moving=false}){
     return move==BotMoves().forward && moving ? forwardMoving 
          : move==BotMoves().forward && !moving ? forwardHalt 
          : move==BotMoves().right && moving ? rightMoving 
          : move==BotMoves().right && !moving ? rightHalt 
          : move==BotMoves().left && moving ? leftMoving 
          : move==BotMoves().left && !moving ? leftHalt 
          : move==BotMoves().backward && moving ? backwardMoving 
          : move==BotMoves().backward && !moving ? backwardHalt 
          : halt;
   }

   Icon getIcon(String move,{Color color=Colors.amber,double size=18}){
     return Icon(
             move==BotMoves().forward ? Ionicons.caret_up_circle_outline
             : move==BotMoves().right? Ionicons.caret_forward_circle_outline
             : move==BotMoves().left? Ionicons.caret_back_circle_outline
             : move==BotMoves().backward? Ionicons.caret_down_circle_outline
             : Ionicons.stop_circle_outline,
            color:color ,size:size);
   }

}