"""
Basic QR code-reading for the raspberry pi. Uses zbarlight, openCV, and the Image class.
Note: This is a work in progress, -m@.
"""
from PIL import Image
import io
import picamera

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
		time.sleep(1) # "warm-up" time for the camera.


	def run_once(self):
		"""
		Looks through camera once; if there's a QR code, returns it. Otherwise, returns -1.
		"""
		with self.cam as camera:
			stream = io.BytesIO()
			camera.capture(stream, format="jpeg", use_video_port=True)
			stream.truncate()
			stream.seek(0)
			img = Image.open(stream)
			img.load()
			grayscale_img = img.convert('L')
			img.close()
			raw = grayscale_img.tobytes()
			width, height = grayscale_img.size
			scan_results = zbarlight.qr_code_scanner(raw, width, height)
			try: 
				code = scan_results.decode()
				print "QR: ", code
				print "Truncating now"
				stream.truncate(0)
				return code
			except:
				print "No QR detected"
				stream.truncate(0)
				print "truncating"
				return -1


if __name__ == "__main__":
	qrd = QRDetector()
	for i in range(20):
		qrd.run_once()
		time.sleep(5)