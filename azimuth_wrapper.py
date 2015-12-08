"""
TODO: probably, add some try-catches.
"""
import serial
import qr_detector
import speech_handler #needs to be set up correctly
import threading

class FetchBot(object):

	def __init__(self, serial_port="/dev/ttyACM0"):
		self.qrd = qr_detector.QRDetector()
		self.ser = serial.Serial(serial_port, 9600, timeout=2)
		self.target_queue = []
		# self.target_queue = ["1", "salt", "2", "pepper", "3"] # setting at start, for testing purposes.
		self.hasObject = False
		self.words_to_targets_dict = {"one": "1", "1": "1", "won": "1", "2":"2", "3":"3", "two": "2", "to": "2", "too": "2", "three": "3", "tree": "3", "salt": "salt", "pepper": "pepper", "rapper":"pepper"} # Do we want these strings as the values encoded by the QR codes? Or are we going for coordinates?
		self.sr = speech_handler.Loop_speech_handler(self.set_target)
		self.main_loops_so_far = 0 # for debugging.


	def check_if_at_target(self):
		if len(self.target_queue) == 0:
			STOP_COMMAND = "S"
			self.ser.write(STOP_COMMAND)
			return
		qr_val = ""
		qr_val = self.qrd.scan()
		if str(qr_val) == str(self.target_queue[0]):
			t = self.target_queue[0]
			print "arrived at ", t, "|\t", target_queue
			if t in ["1", "2", "3"]:
				if self.hasObject:
					DROP_COMMAND = "D" # TODO ofc.
					self.ser.write(DROP_COMMAND)
					self.hasObject = False
					time.sleep(1)
					TURN_COMMAND = "<"
					self.ser.write(TURN_COMMAND)
					time.sleep(1)
			elif t in ["salt", "pepper"]:
				if not self.hasObject:
					TURN_COMMAND = "<"
					self.ser.write(TURN_COMMAND)
					time.sleep(1)
					FWD_COMMAND = "F"
					self.ser.write(FWD_COMMAND)
					time.sleep(2)
					GRAB_COMMAND = "G"
					self.ser.write(GRAB_COMMAND)
					time.sleep(1) # lets it finish
					self.hasObject = True
					TURN_COMMAND = "<"
					self.ser.write(TURN_COMMAND)
					time.sleep(1)
					self.ser.write(FWD_COMMAND)
					time.sleep(2)
					self.ser.write(TURN_COMMAND)
					time.sleep(1)
			FWD_COMMAND = "F"
			self.ser.write(FWD_COMMAND)
			self.target_queue.pop(0)
			
	def run(self):
		"""
		main loop
		"""
		self.main_loops_so_far += 1
		if self.main_loops_so_far%10000 == 0:
			print "main loop running 10kx" 
		self.check_if_at_target()

	def set_target(self, new_targets):
		for i in new_targets:
			i = str(i).lower()
			if i in self.words_to_targets_dict.keys():
				self.target_queue.append(self.words_to_targets_dict[i])
				print "Added target: ", i
			elif i == "azimuth":
				print "Recognized name. Bark, bark!"
				#this might be a good thing to map to "stop & flush targets"
			elif i == "print":
				print self.target_queue
			elif i == "clear":
				self.flush_targets()
			else:
				print "Not recognized target: ", i

	def flush_targets(self):
		self.target_queue = []

	def run_loop(self):
		try:
			while True:
				self.run()
		except KeyboardInterrupt:
			print "run_loop terminated"

	def listen_loop(self):
		try:
			while True:
				self.sr.once()
		except KeyboardInterrupt:
			print "listen_loop terminated"


if __name__ == "__main__":
	fb = FetchBot()
	run_thread = threading.Thread(target=fb.run_loop)
	listen_thread = threading.Thread(target=fb.listen_loop)
	run_thread.start()
	rumble_thread.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		time.sleep(1)
		exit()