import speech_recognition as sr

def once():
	r = sr.Recognizer()
	m = sr.Microphone(
		# device_index=2, 
		sample_rate=44100, 
		chunk_size = 8192
		)

	with m as source:
		r.adjust_for_ambient_noise(source)

	r.pause_threshold=0.3
	r.non_speaking_duration=0

	with m as source:
		print "Running once!"
		audio = r.listen(source)

	try:
		print [str(i) for i in r.recognize_google(audio).split(' ')]
	except sr.UnknownValueError:
		print "Couldn't understand that!"
	except sr.RequestError as e:
		print "Couldn't get results from Google!"

def loop():
	once()
	loop()

if __name__ == "__main__":
	loop()