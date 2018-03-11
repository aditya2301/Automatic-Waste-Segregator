
import time

import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685()


pwm.set_pwm_freq(60)

def shoulder_lf_center():
	first_quadrant=220
	second_quadrant=410
	center=325
	pin=7
	global pwm
	for i in range(first_quadrant,center,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)

def shoulder_rf_center():
	first_quadrant=220
	second_quadrant=410
	center=325
	pin=7
	global pwm
	for i in range(first_quadrant,center,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)

def shoulder_lf():
	first_quadrant=220
	second_quadrant=410
	center=325
	pin=7
	global pwm
	for i in range(center,first_quadrant,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)
	time.sleep(2)


def shoulder_rf():
	first_quadrant=220
	second_quadrant=410
	center=325
	pin=7
	global pwm
	for i in range(center,second_quadrant,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)


def finger_open():
	expand=460
	contract=190
	pin=11
	global pwm
	for i in range(contract,expand,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(2)
	

def finger_close():
	expand=460
	contract=190
	pin=11
	global pwm
	for i in range(expand,contract,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(2)
	


def wrist():
	straight=360
	bent=127
	pin=15
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
def elbow(quadrant):
	down=540
	up=135
	pin=3
	global pwm
	finger_open()
	time.sleep(2)
	for i in range(up,down,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(2)
	finger_close()
	time.sleep(10)
	if quadrant=='1':
		shoulder_lf_center()
	elif quadrant=='2':
		shoulder_rf_center()
	time.sleep(2)
	global pwm
	for i in range(down,up,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)


def quadrant1():
	shoulder_lf()
	elbow('1')
	time.sleep(2)
	wrist()

def quadrant2():
	shoulder_rf()
	elbow('2')
	time.sleep(2)
	wrist()

def quadrant12():
	elbow()
	time.sleep(2)
	wrist()


def flap(direction):
	if direction=="l":
		pass
	elif direction=="r":
		pass

#finger_close()
quadrant2()