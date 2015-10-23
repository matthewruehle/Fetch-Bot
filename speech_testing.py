import speech_recognition as sr
# import threading
import time

print "STARTING"
r = sr.Recognizer()
# r.non_speaking_duration=0.1

# with sr.Microphone() as source:
# 	print "Adjusting"
# 	r.adjust_for
# 	print "Say something!"
# 	audio = r.listen(source)

# try:
# 	print r.recognize_google(audio)
# except sr.UnknownValueError:
# 	print "couldn't understand"
# except sr.RequestError as e:
# 	print "couldn't request from google: ", e

def callback(recognizer, audio):

	try:
		this_string = recognizer.recognize_google(audio)
	except sr.UnknownValueError:
		print "Couldn't understand"
		return
	except sr.RequestError:
		print "Couldn't request results"
		return
	word_list = this_string.split(' ')

print "MIC-ing"
m = sr.Microphone()

with m as source:
	r.adjust_for_ambient_noise(source)

r.pause_threshold=0.3
r.non_speaking_duration=0

print "LOOP STARTING"
stop_listening = r.listen_in_background(m, callback)

i = 0

while i<5000:
	i += 1
	time.sleep(.01)

print "DONE"



# for i = 1:1:N
# 	while asdfasdf
# 		if asdfasdf
# 			x = x - 1
# 			etc
# 		else
# 			x = x + 1
# 			etc
# 		end
# 	end
# 	if x == 1
# 		uno++
# 		x = 20
# 	else
# 		hundred++
# 		x = 20
# 	end
# end