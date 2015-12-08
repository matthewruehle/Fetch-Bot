import speech_recognition as sr

# def once():
# 	r = sr.Recognizer()
# 	m = sr.Microphone(
# 		# device_index=2, 
# 		sample_rate=44100, 
# 		chunk_size = 8192
# 		)

# 	with m as source:
# 		r.adjust_for_ambient_noise(source)

# 	r.pause_threshold=0.3
# 	r.non_speaking_duration=0

# 	with m as source:
# 		print "Running once!"
# 		audio = r.listen(source)

# 	try:
# 		print [str(i) for i in r.recognize_google(audio).split(' ')]
# 	except sr.UnknownValueError:
# 		print "Couldn't understand that!"
# 	except sr.RequestError as e:
# 		print "Couldn't get results from Google!"

# def loop():
# 	once()
# 	loop()

class Jank_speech_handler(object):
	def __init__(self, callback_function):
		print "Jank handler starting..."
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



def _print(n):
	print [str(i) for i in n]

if __name__ == "__main__":
	jh = Jank_speech_handler(_print)
	print "Jank loop starting..."
	jh.loop()