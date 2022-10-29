import 'package:flutter/material.dart';
import 'package:ionicons/ionicons.dart';

class MovesBox extends StatefulWidget {
  final Function move;
  const MovesBox(this.move,{super.key});

  @override
  State<MovesBox> createState() => _MovesBoxState();
}

class _MovesBoxState extends State<MovesBox> {


  @override
  Widget build(BuildContext context) {
    return Row( mainAxisAlignment: MainAxisAlignment.center,
           children: [
            Column( mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                 
                 GestureDetector(onTap:(){
                   widget.move('left-front');
                  },child: Transform.rotate(angle: 0.6,child: const Icon(Ionicons.arrow_undo_circle_outline,color: Colors.amber,size: 80,))),
                 
                 const SizedBox(height: 20,),
                 
                 GestureDetector(onTap:(){
                   widget.move('left-back');
                 },child:Transform.rotate(angle: -10,child: const Icon(Ionicons.arrow_redo_circle_outline,color: Colors.amber,size: 80,))),  
               
              ],
            ),
            Column( mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                 GestureDetector(onTap:(){
                  widget.move('forward');
                 },child: const Icon(Ionicons.caret_up_circle_outline,color: Colors.amber,size: 80,)),
                 
                 const SizedBox(height: 20,),
                 
                 GestureDetector(onTap:(){
                  widget.move('halt');
                 },child: const Icon(Ionicons.stop_circle_outline,color: Colors.amber,size: 80,)),
                 
                 const SizedBox(height: 20,),

                 GestureDetector(onTap:(){
                  widget.move('backward');
                 },child: const Icon(Ionicons.caret_down_circle_outline,color: Colors.amber,size: 80,)), 
              ],
            ),

            Column( mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                 GestureDetector(onTap:(){
                  widget.move('right-front');
                 },child:Transform.rotate(angle:-0.6,child:const Icon(Ionicons.arrow_redo_circle_outline,color: Colors.amber,size: 80,))),
                
                 const SizedBox(height: 20,),
                
                 GestureDetector(onTap:(){
                  widget.move('right-back');
                 },child:Transform.rotate(angle: 10,child: const Icon(Ionicons.arrow_undo_circle_outline,color: Colors.amber,size: 80,),)),                    
              ],
            ),
          ],
        );
  }
}