
from __future__ import division
import time

import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 116  # Min pulse length out of 4096
servo_max = 485  # Max pulse length out of 4096



pwm.set_pwm_freq(60)


def shoulder():
	first_quadrant=220
	second_quadrant=410
	center=325
	pin=11
	global pwm
	for i in range(center,first_quadrant,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)

	for i in range(first_quadrant,second_quadrant,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)
	global pwm
	for i in range(second_quadrant,first_quadrant,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)
	global pwm
	for i in range(first_quadrant,center,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)

def elbow():
	down=580
	up=143
	pin=7
	global pwm
	for i in range(up,down,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(2)
	finger()
	time.sleep(7)
	global pwm
	for i in range(down,up,-1):
		pwm.set_pwm(pin,0,i)
		if i>160:
			time.sleep(0.01)
		else:
			time.sleep(0.07)

def finger():
	expand=460
	contract=190
	pin=15
	global pwm
	for i in range(contract,expand,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(2)
	global pwm
	for i in range(expand,contract,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)




def wrist():
	straight=360
	bent=127
	pin=3
	global pwm
	for i in range(straight,bent,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)
	time.sleep(2)
	finger()
	time.sleep(5)
	global pwm
	for i in range(bent,straight,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)


shoulder()
elbow()
#finger()
wrist()