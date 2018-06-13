'''
This script tests the IR sensor module.
'''

import RPi.GPIO as GPIO
import time
def binStatus():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(37,GPIO.IN) #GPIO 16 bio degradable 
	GPIO.setup(38,GPIO.IN) #GPIO 18 non bio degradable bin
	
	while True:
		bio = GPIO.input(38)
		nonbio= button_state = GPIO.input(37)
		if bio != False : #object is near  
			time.sleep(2)
			if nonbio==False : 
				msg="Biodegradable bin is full. Please replace."
				print(msg)
		if nonbio != False : #object is near  
			time.sleep(2)
			if nonbio!=False :
				msg="Non-biodegradable bin is full. Please replace."
				print(msg)


binStatus()