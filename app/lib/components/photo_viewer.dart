import 'package:flutter/material.dart';

Future photoViewer(BuildContext ctx, String imgUrl){
   var mh = MediaQuery.of(ctx).size.height;
    Future<bool> exitV(){ 
      Navigator.pop(ctx,false);return Future<bool>.value(true);
    }
   return showDialog<bool>(context: ctx, builder: 
    (BuildContext context) {
      return  WillPopScope(onWillPop: ()=> exitV(),
        child: Dialog(backgroundColor: Colors.transparent, 
               child: Center(child: Image.network(imgUrl,height:300,width: 300,))
               ),
      );
    }
  );
}