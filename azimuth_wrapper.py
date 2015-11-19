"""
right now, just keeps track of last-known-location; has the bot stop when it gets there.

TODO: probably, add some try-catches.

"""
import serial
import qr_detector
# import collections
import speech_handler #needs to be set up correctly

class FetchBot(object):

	def __init__(self, serial_port="/dev/ttyACM0"):
		self.qrd = qr_detector.QRDetector()
		self.ser = serial.Serial(serial_port, 9600, timeout=2)
		self.target_queue = []
		self.hasObject = False
		self.words_to_targets_dict = {"one": "1", "1": "1", "2":"2", "3":"3", "two": "2", "three": "3", "salt": "salt", "pepper": "pepper"} # Do we want these strings as the values encoded by the QR codes? Or are we going for coordinates?
		self.sr = speech_handler.Speech_handler(self.set_target)

	def check_if_at_target(self):
		if len(self.target_queue) == 0:
			return
		qr_val = "asdf"
		qr_val = self.qrd.scan()
		if str(qr_val) == str(self.target_queue[0]):
			print "arrived at ", self.target_queue[0]
			self.stop_robot()
			self.do_something() # also needs to make the robot start moving again.
			self.target_queue.pop(0)
			
	def grab(self):
		GRAB_COMMAND = "G"
		self.ser.write(GRAB_COMMAND)
		
	def stop_robot(self):
		STOP_COMMAND = "S"
		self.ser.write(STOP_COMMAND)

	def mainloop(self): #First checks the list of found voice commands and compares them to what it has heard. If there is a match and it isn't "azimuth", it appends the command list. If it is "azimuth" it recognizes its own name. Else, it returns a false command
		self.check_if_at_target()
		#should probably also have it move/go, if it doesn't default to moving forward.

	def do_something(self):
		TURN_COMMAND = "<" #sets the command to pickup the object
		self.ser.write(TURN_COMMAND)
		
	
	def set_target(self, new_targets):
		for i in new_targets:
			i = str(i)
			if i in self.words_to_targets_dict.keys():
				self.target_queue.append(self.words_to_targets_dict[i])
				print "Added target: ", i
			elif i == "azimuth":
				print "Recognized name. Bark, bark!"
				#this might be a good thing to map to "stop & flush targets"
			else:
				print "Not recognized target: ", i

	def flush_targets(self):
		self.target_queue = []

if __name__ == "__main__":
	fb = FetchBot()
	while True:
		fb.mainloop()

