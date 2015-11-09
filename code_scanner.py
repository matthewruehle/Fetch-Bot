"""
Basic QR code-reading for the raspberry pi. Uses zbarlight, openCV, and the Image class.
Note: This is a work in progress, -m@.
"""

from PIL import Image
import io
from picamera.array import PiRGBArray
import picamera
import cv2
import zbarlight
import time

class QRDetector(object):
	"""
	Instantiates a QR-detector/camera-handler.
	"""

	def __init__(self):
		self.cam = picamera.PiCamera()
		self.cam.resolution = (640, 480) # reducing resolution with the onboard GPU, to speed calculation elsewhere.
		self.cam.framerate = 32
		self.cam.start_preview()
		time.sleep(1) # "warm-up" time for the camera.
		# self.stream = PiRGBArray(self.cam)
		self.stream = io.BytesIO()

	def run_continuous(self):
		if True:
			return # don't use this function right now! just testing.
		for i in self.cam.capture_continuous(self.stream):
			self.stream.truncate()
			self.stream.seek(0) # gets image

			# converts to a PIL image for processing

	def run_once(self):
		"""
		Looks through camera once; if there's a QR code, returns it. Otherwise, returns -1.
		"""
		self.cam.capture(self.stream, format="jpeg")
		self.stream.truncate()
		self.stream.seek(0)
		img = Image.open(self.stream)
		img.load()
		grayscale_img = img.convert('L')
		img.close()
		raw = grayscale_img.tobytes()
		width, height = grayscale_img.size
		scan_results = zbarlight.qr_code_scanner(raw, width, height)
		try: 
			code = scan_results.decode()
			print "QR: ", code
			return code
		except:
			print "No QR detected"
			return -1

if __name__ == "__main__":
	qrd = QRDetector()
	for i in range(20):
		time.sleep(.5)
		qrd.run_once()
