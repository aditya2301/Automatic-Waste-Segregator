
import time

import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685()


pwm.set_pwm_freq(60)

def shoulder_lf_center():
	first_quadrant=220
	second_quadrant=410
	center=325
	pin=11
	global pwm
	for i in range(first_quadrant,center,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)

def shoulder_rf_center():
	first_quadrant=220
	second_quadrant=410
	center=325
	pin=11
	global pwm
	for i in range(first_quadrant,center,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)

def shoulder_lf():
	first_quadrant=220
	second_quadrant=410
	center=325
	pin=11
	global pwm
	for i in range(center,first_quadrant,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)
	time.sleep(2)
	#shoulder_lf_center()

def shoulder_rf():
	first_quadrant=220
	second_quadrant=410
	center=325
	pin=11
	global pwm
	for i in range(center,second_quadrant,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)
	#shoulder_lf_center()

def finger_open():
	expand=460
	contract=190
	pin=15
	global pwm
	for i in range(contract,expand,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(2)
	

def finger_close():
	expand=460
	contract=190
	pin=15
	global pwm
	for i in range(expand,contract,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(2)
	


def wrist():
	straight=360
	bent=127
	pin=3
	global pwm
	for i in range(straight,bent,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)
	time.sleep(2)
	finger_open()
	time.sleep(2)
	finger_close()
	time.sleep(7)
	global pwm
	for i in range(bent,straight,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)
	time.sleep(2)
def elbow():
	down=580
	up=143
	pin=7
	global pwm
	finger_open()
	time.sleep(7)
	for i in range(up,down,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(2)
	finger_close()
	time.sleep(5)
	global pwm
	for i in range(down,up,-1):
		pwm.set_pwm(pin,0,i)
		if i>160:
			time.sleep(0.01)
		else:
			time.sleep(0.07)

def quadrant1():
	shoulder_lf()
	time.sleep(2)
	#finger_open()
	#time.sleep(2)
	elbow()
	time.sleep(2)
	shoulder_lf_center()
	time.sleep(2)
	wrist()

def quadrant2():
	shoulder_rf()
	time.sleep(2)
	#finger_open()
	#time.sleep(2)
	elbow()
	time.sleep(2)
	shoulder_rf_center()
	time.sleep(2)
	wrist()

def quadrant12():
	#finger_open()
	#time.sleep(2)
	elbow()
	time.sleep(2)
	wrist()


def flap(direction):
	if direction=="l":
		pass
	elif direction=="r":
		pass
