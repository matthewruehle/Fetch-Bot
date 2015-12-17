import speech_recognition as sr
import time


class Background_speech_handler(object):
	"""
	This one is ideal, but might not be possible to implement on the RPi hardware.
	"""
	def __init__(self, callback_function):
		"""
		Needs to receive a callback function.
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
	NOTE: Do not run loop() in the main thread, it will block the program. 
	"""
	def __init__(self, callback_function):
		print "Loop handler starting..."
		self.r = sr.Recognizer()
		self.m = sr.Microphone(
			# device_index = 2,
			sample_rate = 48000, 
			chunk_size = 8192
			)
		print "Adjusting for ambient noise..."
		with self.m as source:
			self.r.adjust_for_ambient_noise(source)
		self.r.pause_threshold = 0.3
		self.r.non_speaking_duration = 0
		self.azimuth_callback = callback_function

	def once(self): 
		"""
		Runs once, and sends the results to self.azimuth_callback.
		"""
		with self.m as source:
			print "Listening..."
			audio = self.r.listen(source)
		try: 
			this_string = self.r.recognize_google(audio)
		except sr.UnknownValueError:
			print "Couldn't understand that..."
			return
		except sr.RequestError:
			print "Couldn't request results..."
			return
		word_list = this_string.split(' ')
		self.azimuth_callback(word_list)
		return

	def refresh(self):
		"""
		Refreshes the microphone, making self.m refer to a new instance of the sr.Microphone class.
		"""
		del self.m #might be a superfluous call.
		self.m = sr.Microphone(
			# device_index = 2,
			sample_rate = 44100, 
			chunk_size = 8192
			)
		print "Microphone lease refreshed."