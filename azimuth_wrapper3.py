"""
TODO: probably, add some try-catches.
"""
import serial
import qr_detector3 as qr_detector
import speech_handler3 as speech_handler #needs to be set up correctly
import threading
import time

class FetchBot(object):

	def __init__(self, serial_port="/dev/ttyAMA0"):
		self.qrd = qr_detector.QRDetector()
		try:
			self.ser = serial.Serial(serial_port, 9600, timeout=2)
		except:
			try:
				self.ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=2)
			except:
				self.ser = serial.Serial("/dev/ttyACM0", 9600, timeout=2)
		self.target_queue = []
		self.target_queue = ["1", "salt", "2", "pepper", "3"] # setting at start, for testing purposes.
		self.hasObject = False
		self.words_to_targets_dict = {"one": "1", "1": "1", "won": "1", "2":"2", "3":"3", "two": "2", "to": "2", "too": "2", "three": "3", "tree": "3", "salt": "salt", "alt": "salt", "pepper": "pepper", "rapper":"pepper"} # Do we want these strings as the values encoded by the QR codes? Or are we going for coordinates?

		GRAB_COMMAND = bytes("G", 'UTF-8')
		self.ser.write(GRAB_COMMAND) # no idea


	def check_if_at_target(self):
		if len(self.target_queue) == 0:
			STOP_COMMAND = bytes("S", 'UTF-8') # bytes(plaintext, 'UTF-8')
			self.ser.write(STOP_COMMAND)
			return
		else:
			qr_val = ""
			qr_val = self.qrd.scan()
			if str(qr_val) == str(self.target_queue[0]):
				t = self.target_queue[0]
				print("arrived at ", t, "|\t", self.target_queue)
				if t in ["1", "2", "3"]:
					if self.hasObject:
						RIGHT_COMMAND = bytes(">", 'UTF-8')
						DROP_COMMAND = bytes("D", 'UTF-8')
						TURN_COMMAND = bytes("<", 'UTF-8')
						BACK_COMMAND = bytes("B", 'UTF-8')
						self.ser.write(RIGHT_COMMAND)
						time.sleep(1)
						self.ser.write(DROP_COMMAND)
						self.hasObject = False
						time.sleep(1)
						self.ser.write(BACK_COMMAND)
						time.sleep(0.5)
						self.ser.write(TURN_COMMAND)
						time.sleep(1)
				elif t in ["salt", "pepper"]:
					if not self.hasObject:
						TURN_COMMAND = bytes("<", 'UTF-8')
						self.ser.write(TURN_COMMAND)
						time.sleep(1)
						FWD_COMMAND = bytes("F", 'UTF-8')
						self.ser.write(FWD_COMMAND)
						time.sleep(1)
						GRAB_COMMAND = bytes("G", 'UTF-8')
						self.ser.write(GRAB_COMMAND)
						time.sleep(1) # lets it finish
						self.hasObject = True
						TURN_COMMAND = bytes("<", 'UTF-8')
						self.ser.write(TURN_COMMAND)
						time.sleep(1)
						self.ser.write(FWD_COMMAND)
						time.sleep(1)
						self.ser.write(TURN_COMMAND)
						time.sleep(1)
				FWD_COMMAND = bytes("F", 'UTF-8')
				self.ser.write(FWD_COMMAND)
				self.target_queue.pop(0)
			else:
				FWD_COMMAND = bytes("F", 'UTF-8')
				self.ser.write(FWD_COMMAND)
			
	def run(self):
		"""
		main loop
		"""
		self.check_if_at_target()

	def set_target(self, new_targets):
		for i in new_targets:
			i = str(i).lower()
			if i in self.words_to_targets_dict.keys():
				self.target_queue.append(self.words_to_targets_dict[i])
				print("Added target: ", i)
			elif i in ["azimuth", "azmyth"]:
				print("Recognized name. Bark, bark!")
				#this might be a good thing to map to "stop & flush targets"
			elif i in ["sprint", "print"]:
				print(self.target_queue)
			elif i in ["here", "clear"]:
				print("Clearing targets")
				self.flush_targets()
			elif i == "abort":
				print("shutting down...")
				import subprocess
				cmd = "sudo shutdown -H now"
				popen = subprocess.Popen(cmd, shell=True)
				popen.communicate()
			else:
				print("Not recognized target: ", i)

	def flush_targets(self):
		self.target_queue = []

	def run_loop(self):
		while True:
			self.run()
		# try:
		# 	while True:
		# 		self.run()
		# except KeyboardInterrupt:
		# 	print "run_loop terminated"

	def listen_loop(self):
		try:
			self.sr = speech_handler.Background_speech_handler(self.set_target)

		# 	while True:
		# 		self.sr.once()
		# # except KeyboardInterrupt:
		# 	# print "listen_loop terminated"
		except IOError:
			print("Got ioerror; resetting speech handler.")
			
			# self.sr = speech_handler.Background_speech_handler(self.set_target)

			# self.sr = speech_handler.Loop_speech_handler(self.set_target)
			#Not sure if this actually fixes the problem we're getting - persistent, hard-to-figure-out-why IOError keeps showing up occasionally.
			#Specifically, IOError: stream closed. Refreshing the microphone might reopen the stream?
			#Maybe find some way to pre-emptively "save" the audio? Not sure if that's possible.
			#Also, not sure if it's the microphone that's having the problem. Might be the recognizer, or something else.
			#Googling the error code just gets unrelated IOErrors. Googling it in quotes gets 4 results, none resolved. :|
			self.listen_loop()

if __name__ == "__main__":
	fb = FetchBot()
	run_thread = threading.Thread(target=fb.run_loop)
	listen_thread = threading.Thread(target=fb.listen_loop)
	run_thread.start()
	listen_thread.start()
	try:
		while True:
			time.sleep(1)
	except:
		print("exiting...")
		exit()

	# try:
	# 	while True:
	# 		time.sleep(1)
	# except KeyboardInterrupt:
	# 	time.sleep(1)
	# 	print "Exiting..."
	# 	exit()
