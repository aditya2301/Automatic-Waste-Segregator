
import time,Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(10)

def finger_open():
	expand=460
	contract=190
	pin=11
	global pwm
	for i in range(contract,expand,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(1)
	

def finger_close():
	expand=460
	contract=190
	pin=11
	global pwm
	for i in range(expand,contract,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(1)

def shoulder_lf_center():
	first_quadrant=220
	second_quadrant=410
	center=315
	pin=7
	global pwm
	for i in range(first_quadrant,center,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)

def shoulder_rf_center():
	first_quadrant=220
	second_quadrant=410
	center=315
	pin=7
	global pwm
	for i in range(second_quadrant,center,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)

def shoulder_lf():
	print("Operating finger..")
	finger_open()
	first_quadrant=220
	second_quadrant=410
	center=315
	pin=7
	global pwm
	for i in range(center,first_quadrant,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(1)


def shoulder_rf():
	print("Operating finger..")
	finger_open()
	first_quadrant=220
	second_quadrant=410
	center=315
	pin=7
	global pwm
	for i in range(center,second_quadrant,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(1)


def wrist_bent_fh():
	straight=127
	bent=220
	pin=15
	global pwm
	for i in range(straight,bent,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)	

def wrist_bent_sh():
	straight=220
	bent=360
	pin=15
	global pwm
	for i in range(straight,bent,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	

def wrist_straight():
	straight=127
	bent=360
	pin=15
	global pwm
	for i in range(bent,straight,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(1)
def elbow(quadrant):
	print("Operating elbow..")
	down=565
	up=145
	pin=3
	global pwm
	for i in range(up,down,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.008)
	print("Operating finger..")
	time.sleep(2)
	finger_close()
	time.sleep(8)
	print("Operating elbow..")
	if quadrant=='1':
		shoulder_lf_center()
	elif quadrant=='2':
		shoulder_rf_center()
	else: 
		pass
	print("Operating wrist..")
	time.sleep(1)
	wrist_bent_fh()
	time.sleep(1)
	global pwm
	print("Operating elbow..")
	for i in range(down,up,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)

	#time.sleep(1)
	print("Operating wrist..")
	wrist_bent_sh()
	#time.sleep(2)
	print("Operating finger..")
	finger_open()
	time.sleep(1)
	finger_close()
	#time.sleep(5)
	print("Operating wrist..")
	wrist_straight()

def flap(direction):
	print("Operating flap..")
	center=260
	left=60
	right=500
	pin=0
	if direction=='l':
		for i in range(center,left,-1):
			pwm.set_pwm(pin,0,i)
			#time.sleep(0.01)
		time.sleep(2)
		for i in range(left,center,1):
			pwm.set_pwm(pin,0,i)
			#time.sleep(0.01)
	elif direction=='r':
		center=350
		for i in range(center,right,1):
			pwm.set_pwm(pin,0,i)
			#time.sleep(0.01)
		time.sleep(2)
		for i in range(right,center,-1):
			pwm.set_pwm(pin,0,i)
			#time.sleep(0.01)

def quadrant1(binDir):
	print("\n Operating shoulder..")
	shoulder_lf()
	elbow('1')
	#time.sleep(1)
	flap(binDir)

def quadrant2(binDir):
	print("\n Operating shoulder..")
	shoulder_rf()
	elbow('2')
	#time.sleep(1)
	flap(binDir)

def quadrant12(binDir):
	print("\n Operating shoulder..")
	elbow('3')
	#time.sleep(1)
	flap(binDir)


