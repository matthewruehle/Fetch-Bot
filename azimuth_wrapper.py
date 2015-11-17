"""
right now, just keeps track of last-known-location; has the bot stop when it gets there.
"""
import serial
import qr_detector
import collections
import speech_testing #needs to be set up correctly

class FetchBot(object):

	def __init__(self, serial_port="/dev/ttyACM0"):
		self.qrd = qr_detector.QRDetector()
		self.ser = serial.Serial(serial_port, 9600, timeout=2)
		self.target_queue = [1,3,2,4]
		self.hasObject = False
		recognizedCommands = [salt, pepper, one, two, three]
		if speechTester.word_list in reconizedCommands:
			self.set_target(speechTester.word_list) #needs to be changed once speech_testing is set up like a class
		else:
			print "Unrecognized Command"
	def check_if_at_target(self):
		if len(self.target_queue) == 0:
			return
		qr_val = self.qrd.run_once()
		if str(qr_val) == str(self.target_queue[0]):
			print "arrived at ", self.target_queue[0]
			self.stop_robot()
			self.do_something()
			self.target_queue.pop(0)

	def stop_robot(self):
		STOP_COMMAND = "S"
		ser.write(STOP_COMMAND)

	def mainloop(self):
		self.check_if_at_target()

	def do_something(self):
		PICKUP_COMMAND = "G" #sets the command to pickup the object
		ser.write(PICKUP_COMMAND)
		return
	
	def set_target(self, new_target):
		self.target_queue.extend(new_target)

	def flush_targets(self):
		self.target_queue = []

if __name__ == "__main__":
	FetchBot.mainloop()
