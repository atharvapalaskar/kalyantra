
enum NgConnectionState {
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
   String get rightfront => 'right-front';
   String get rightback => 'right-back';
   String get leftfront => 'left-front';
   String get leftback => 'left-back';
}