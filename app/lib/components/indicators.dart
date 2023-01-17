import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:ionicons/ionicons.dart';

import '../enums.dart';
import 'static_class.dart';

class StatusIndicatorWidget extends StatelessWidget {
  final bool active; final double size; final IconData icon; final String text;final bool ml ;
  const StatusIndicatorWidget({this.active= false,this.size= 18,this.icon=Ionicons.ellipse_outline,this.text='',this.ml=false,super.key});

  @override
  Widget build(BuildContext context) {
  return Column( crossAxisAlignment: CrossAxisAlignment.center,
          children: [
              Icon(icon,color:active? Colors.amber:Colors.grey,size:size),
              const SizedBox(height:8),
              Container(alignment: Alignment.center,child: Text(text,style: TextStyle(color: Colors.white,fontSize: 7,letterSpacing: 0.3,height: ml?1.6:1),textAlign: TextAlign.center,)),
          ]);
  }
}


class TaskIndicatorWidget extends StatelessWidget {
  final bool main; final String task; final double cmProgress;final bool moving;
  const TaskIndicatorWidget({this.main= false,this.task='move forward',this.cmProgress=0,this.moving=false,super.key});

  @override
  Widget build(BuildContext context) { 
  final String move = task.split(' ')[0] == 'move' ? task.split(' ')[1] : 'halt';
  return Row( crossAxisAlignment: CrossAxisAlignment.center, children: [
          
          // Indicator
          main && task.split(' ')[0] == 'move' ? 
             SvgPicture.string(MovingArrows().getSvg(move:move,moving: moving), height: move == BotMoves().forward || move == BotMoves().backward ? 26 : move == BotMoves().halt ? 23 : 19)
          : !main && task.split(' ')[0] == 'move' ? 
             MovingArrows().getIcon(move,color: Colors.amber,size: 20,)  
          : task.split(' ')[0] == 'click' ? 
             Icon(Ionicons.camera_outline,color: Colors.amber ,size:  main ? 30 : 18)
          : task.split(' ')[0] == 'return'?
             Icon(Ionicons.reload_circle_outline,color: Colors.amber ,size:  main ? 30 : 18)
          : main ?
              SvgPicture.string(MovingArrows().getSvg(move:BotMoves().halt,moving: false),height: 23,)
          : const SizedBox(height: 1), 

          SizedBox(width: main? 8:6),
         
          // Main and Sub Text
          Column( crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(task.split(' ')[0] == 'move'? task.split(' ')[1] : task.split(' ')[0] == 'click'? 'click' : main? 'Standby' : '--', style: TextStyle(color: main ?Colors.amber : Colors.white,fontSize: main?9:6,letterSpacing: 0.2,height: 1.6,),textAlign: TextAlign.left,),
              const SizedBox(height:3),
              Text(task.split(' ')[0] == 'move' && task.split(' ').length > 2 && main ? '$cmProgress/${task.split(' ')[2]} cm' 
                  :task.split(' ')[0] == 'move' && task.split(' ').length > 2 && !main ? [task.split(' ')[2],task.split(' ')[3]].join() 
                  :'',style:TextStyle(color: Colors.white,fontSize: main? 7:6,height: 1.6,),textAlign: TextAlign.left,)
          ]),
      ]);
  }
}
