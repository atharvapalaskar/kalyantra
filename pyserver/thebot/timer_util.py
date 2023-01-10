
from threading import Timer, Thread
import sys  

# class which creates a resettable timer as a thread
class ResetTimer(object):
	def __init__(self, time, function, daemon=None):
		self.__time = time
		self.__function = function
		self.__set()
		self.__running = False
		self.__killed = False
		Thread.__init__(self)
		self.__daemon = daemon
	def __set(self):
		self.__timer = Timer(self.__time, self.__function)
	def stop(self):
		self.__daemon = True
	def run(self):
		self.__running = True
		self.__timer.start()
		if self.__daemon == True:
			sys.exit(0)
	def cancel(self):
		self.__running = False
		self.__timer.cancel()
	def reset(self, start = False):
		if self.__running:
			self.__timer.cancel()
		self.__set()
		if self.__running or start:
			self.start()

  