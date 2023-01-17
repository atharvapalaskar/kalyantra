import 'package:app/components/static_class.dart';
import 'package:app/enums.dart';
import 'package:flutter/material.dart'; 

class MovesBox extends StatefulWidget {
  final Function move;
  const MovesBox(this.move,{super.key});

  @override
  State<MovesBox> createState() => _MovesBoxState();
}

class _MovesBoxState extends State<MovesBox> { 
  @override
  Widget build(BuildContext context) {
    List<String> mvs  = BotMoves().all;
    List<Widget> ctrs = []; 
    for (String mv in  mvs) {
       ctrs.add(GestureDetector(onTap:()=> widget.move(mv),
                 child: MovingArrows().getIcon(mv,size: 45)),
                );
    }

    return Row( mainAxisAlignment: MainAxisAlignment.spaceAround,children: ctrs );
  }
}