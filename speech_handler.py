import speech_recognition as sr
import time


class Background_speech_handler(object):
	"""
		This one is ideal, but might not be possible to implement on the RPi hardware.
	"""
	def __init__(self, callback_function):
		"""
		needs to receive a callback function.
		"""
		print "Speech_handler starting..."
		self.r = sr.Recognizer()
		print "Setting up microphone..."
		self.m = sr.Microphone(device_index=2, sample_rate=48000, chunk_size=8192)
		print "Adjusting for ambient noise..."
		with self.m as source:
			self.r.adjust_for_ambient_noise(source)
		self.r.pause_threshold = 0.3
		self.r.non_speaking_duration = 0
		print "Speech_handler loop starting..."
		self.stop_listening = self.r.listen_in_background(self.m, self.convert_audio_to_wordlist)
		self.azimuth_callback = callback_function

	def convert_audio_to_wordlist(self, recognizer, audio):
		try:
			this_string = recognizer.recognize_google(audio)
		except sr.UnknownValueError:
			print "Couldn't understand that!"
			return
		except sr.RequestError:
			print "Couldn't request results..."
			return
		word_list = this_string.split(' ')
		self.azimuth_callback(word_list)
		return

class Loop_speech_handler(object):
	"""
	This one might hang the processor. You've been warned.
	TODO: Threading.
	"""
	def __init__(self, callback_function):
		print "Loop handler starting..."
		self.r = sr.Recognizer()
		self.m = sr.Microphone(
			# device_index = 2,
			sample_rate = 44100, 
			chunk_size = 8192
			)
		print "Adjusting for ambient noise..."
		with self.m as source:
			self.r.adjust_for_ambient_noise(source)
		self.r.pause_threshold = 0.3
		self.r.non_speaking_duration = 0
		self.cb = callback_function

	def once(self): 
		with self.m as source:
			print "Running once!"
			audio = self.r.listen(source)
		try: 
			this_string = self.r.recognize_google(audio)
		except sr.UnknownValueError:
			this_string = "Couldn't understand that!"
		except sr.RequestError:
			print "Couldn't request results..."
		word_list = this_string.split(' ')
		self.cb(word_list)
		return

	def loop(self):
		self.once()
		self.loop()