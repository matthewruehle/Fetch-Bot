"""
right now, just keeps track of last-known-location; has the bot stop when it gets there.
"""
import serial
import qr_detector
import collections

class FetchBot(object):

	def __init__(self, serial_port="/dev/ttyACM0"):
		self.qrd = qr_detector.QRDetector()
		self.ser = serial.Serial(serial_port, 9600, timeout=2)
		self.target_queue = [1,3,2,4]
		self.hasObject = False

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
		STOP_COMMAND = "asdfadf"
		ser.write(STOP_COMMAND) # replace ofc.

	def mainloop(self):
		self.check_if_at_target()

	def do_something(self):
		pass

	def set_target(self, new_target):
		self.target_queue.extend(new_target)

	def flush_targets(self):
		self.target_queue = []

