
import time

import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685()


pwm.set_pwm_freq(60)

def shoulder_lf_center():
	first_quadrant=220
	second_quadrant=410
	center=305
	pin=7
	global pwm
	for i in range(first_quadrant,center,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)

def shoulder_rf_center():
	first_quadrant=220
	second_quadrant=410
	center=305
	pin=7
	global pwm
	for i in range(second_quadrant,center,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)

def shoulder_lf():
	first_quadrant=220
	second_quadrant=410
	center=305
	pin=7
	global pwm
	for i in range(center,first_quadrant,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)
	time.sleep(2)


def shoulder_rf():
	first_quadrant=220
	second_quadrant=410
	center=305
	pin=7
	global pwm
	for i in range(center,second_quadrant,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)
	time.sleep(2)


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
def wrist_bent_fh():
	straight=360
	bent=220
	pin=15
	global pwm
	for i in range(straight,bent,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)	
def wrist_bent_sh():
	straight=220
	bent=127
	pin=15
	global pwm
	for i in range(straight,bent,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)

def wrist_straight():
	straight=360
	bent=127
	pin=15
	global pwm
	'''for i in range(straight,bent,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)
	time.sleep(2)
	finger_open()
	time.sleep(2)
	finger_close()
	time.sleep(7)
	
	global pwm'''
	for i in range(bent,straight,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.02)
	time.sleep(2)
def elbow(quadrant):
	down=540
	up=130
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
	else: 
		pass
	time.sleep(2)
	global pwm
	wrist_bent_fh()
	time.sleep(2)
	
	for i in range(down,up,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)

	time.sleep(1)
	wrist_bent_sh()
	time.sleep(2)
	finger_open()
	time.sleep(2)
	finger_close()
	time.sleep(7)
	wrist_straight()

def flap(direction):
	center=300
	left=60
	right=500
	pin=0
	if direction=='l':
		for i in range(center,left,-1):
			pwm.set_pwm(pin,0,i)
			time.sleep(0.01)
		time.sleep(2)
		for i in range(left,center,1):
			pwm.set_pwm(pin,0,i)
			time.sleep(0.01)
	elif direction=='r':
		for i in range(center,right,-1):
			pwm.set_pwm(pin,0,i)
			time.sleep(0.01)
		time.sleep(2)
		for i in range(right,center,1):
			pwm.set_pwm(pin,0,i)
			time.sleep(0.01)

def quadrant1(binDir):
	shoulder_lf()
	elbow('1')
	time.sleep(2)
	flap(binDir)

def quadrant2(binDir):
	shoulder_rf()
	elbow('2')
	time.sleep(2)
	flap(binDir)

def quadrant12(binDir):
	elbow('3')
	time.sleep(2)
	flap(binDir)


