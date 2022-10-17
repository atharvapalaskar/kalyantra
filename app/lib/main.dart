import 'package:flutter/material.dart';
import 'package:ionicons/ionicons.dart';
import 'package:http/http.dart' as http;
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
  int _counter = 0;

  move( String _movee) async {
    var res = await http.post(Uri.parse('https://6510-2405-201-10-7cfa-43e7-690-d536-69aa.in.ngrok.io/moves/${_movee}'));
    print(res);
  }

  @override
  Widget build(BuildContext context) {
     
     return Scaffold(
      backgroundColor: Colors.black,
      appBar: PreferredSize(  preferredSize: const Size.fromHeight(60.0),
          child:SafeArea( child: Container(height: 60,color: Colors.amber,child:const Center(child: Text('Kalyantra: Well-being bot',style: TextStyle(fontSize: 16,color: Colors.black, fontWeight: FontWeight.w700,) )),) ),
      ),
      body: Center( child: 
      
        Row( mainAxisAlignment: MainAxisAlignment.center,
           children: [
            Column( mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                 
                 GestureDetector(onTap:(){
                  print('left-front');
                  move('left-front');
                  },child: Transform.rotate(angle: 0.6,child: const Icon(Ionicons.arrow_undo_circle_outline,color: Colors.amber,size: 80,))),
                 
                 const SizedBox(height: 20,),
                 
                 GestureDetector(onTap:(){
                  print('left-back');move('left-back');
                 },child:Transform.rotate(angle: -10,child: const Icon(Ionicons.arrow_redo_circle_outline,color: Colors.amber,size: 80,))),  
               
              ],
            ),
            Column( mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                 GestureDetector(onTap:(){
                  print('forward');move('forward');
                 },child: const Icon(Ionicons.caret_up_circle_outline,color: Colors.amber,size: 80,)),
                 
                 const SizedBox(height: 20,),
                 
                 GestureDetector(onTap:(){
                  print('halt');move('halt');
                 },child: const Icon(Ionicons.stop_circle_outline,color: Colors.amber,size: 80,)),
                 
                 const SizedBox(height: 20,),

                 GestureDetector(onTap:(){
                  print('backward');move('backward');
                 },child: const Icon(Ionicons.caret_down_circle_outline,color: Colors.amber,size: 80,)), 
              ],
            ),

            Column( mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                 GestureDetector(onTap:(){
                  print('right-front');move('right-front');
                 },child:Transform.rotate(angle:-0.6,child:const Icon(Ionicons.arrow_redo_circle_outline,color: Colors.amber,size: 80,))),
                
                 const SizedBox(height: 20,),
                
                 GestureDetector(onTap:(){
                  print('right-back');move('right-back');
                 },child:Transform.rotate(angle: 10,child: const Icon(Ionicons.arrow_undo_circle_outline,color: Colors.amber,size: 80,),)),                    
              ],
            ),
          ],
        ),
      ),
      // floatingActionButton: FloatingActionButton(
      //   onPressed: _incrementCounter,
      //   tooltip: 'Increment',
      //   child: const Icon(Icons.add),
      // ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
