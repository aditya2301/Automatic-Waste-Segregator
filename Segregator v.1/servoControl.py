'''
* This program contains functions useful for rotating the robotic arm.
* The following dependencies are imported.
* Adafruit_PCA9685 ---> Library to control the I2C servo controller.
'''
import time,Adafruit_PCA9685

# Set the pwm necessary for running the servo motors.
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

# finger_open() ---> It opens the finger of the robotic arm.
# contract ---> contracted finger position.
# expand ---> expanded finger position.
# The finger is moved from contracted position to expanded position.

def finger_open():
	expand=460
	contract=190
	pin=11
	global pwm
	for i in range(contract,expand,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(1)
	
# finger_close() ---> It closes the finger of the robotic arm.
# contract ---> contracted finger position.
# expand ---> expanded finger position.
# The finger is moved from expanded position to contracted position.

def finger_close():
	expand=460
	contract=190
	pin=11
	global pwm
	for i in range(expand,contract,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(1)

# shoulder_lf_center() ---> It moves the shoulder joint from left quadrant to centre.
# first_quadrant ---> first quadrant (left) extreme position.
# second_quadrant ---> second quadrant (right) extreme position.
# center ---> in between the 2 quadrants.
# The shoulder is moved from left qudrant to center position.

def shoulder_lf_center():
	first_quadrant=220
	second_quadrant=410
	center=315
	pin=7
	global pwm
	for i in range(first_quadrant,center,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)

# shoulder_rf_center() ---> It moves the shoulder joint from right quadrant to centre.
# first_quadrant ---> first quadrant (left) extreme position.
# second_quadrant ---> second quadrant (right) extreme position.
# center ---> in between the 2 quadrants.
# The shoulder is moved from right qudrant to center position.

def shoulder_rf_center():
	first_quadrant=220
	second_quadrant=410
	center=315
	pin=7
	global pwm
	for i in range(second_quadrant,center,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)

# shoulder_lf() ---> It moves the shoulder joint from centre to first quadrant.
# first_quadrant ---> first quadrant (left) extreme position.
# second_quadrant ---> second quadrant (right) extreme position.
# center ---> in between the 2 quadrants.
# The shoulder is moved from center to left qudrant.

def shoulder_lf():
	first_quadrant=220
	second_quadrant=410
	center=315
	pin=7
	global pwm
	for i in range(center,first_quadrant,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(1)

# shoulder_rf() ---> It moves the shoulder joint from centre to right quadrant.
# first_quadrant ---> first quadrant (left) extreme position.
# second_quadrant ---> second quadrant (right) extreme position.
# center ---> in between the 2 quadrants.
# The shoulder is moved from center to right qudrant.

def shoulder_rf():
	first_quadrant=220
	second_quadrant=410
	center=315
	pin=7
	global pwm
	for i in range(center,second_quadrant,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(1)

# wrist_bent_fh() ---> It moves the wrist joint from bent position to first breakpoint.
# straight ---> wrist position when it is straight.
# bent ---> wrist position when it is bent at the first breakpoint.
# The wrist joint is moved from straight to first breakpoint position.

def wrist_bent_fh():
	straight=127
	bent=220
	pin=15
	global pwm
	for i in range(straight,bent,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)	

# wrist_bent_sh() ---> It moves the wrist joint from  first breakpoint to second breakpoint.
# straight ---> wrist position when it is straight.
# bent ---> wrist position when it is bent at the second breakpoint.
# The wrist joint is moved from first breakpoint position to second breakpoint position.

def wrist_bent_sh():
	straight=220
	bent=360
	pin=15
	global pwm
	for i in range(straight,bent,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	
# wrist_straight() ---> It moves the wrist joint from second breakpoint to straight position.
# straight ---> wrist position when it is straight.
# bent ---> wrist position when it is bent at the second breakpoint.
# The wrist joint is moved from second breakpoint position to straight position.

def wrist_straight():
	straight=127
	bent=360
	pin=15
	global pwm
	for i in range(bent,straight,-1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.01)
	time.sleep(1)

# elbow()  ---> operates the elbow joint.
# up ---> shoulder raised position.
# down ---> shoulder lowered position. 

def elbow(quadrant):
	print("Operating elbow..")
	down=565
	up=145
	pin=3
	global pwm
	print("Operating elbow..")
	for i in range(up,down,1):
		pwm.set_pwm(pin,0,i)
		time.sleep(0.008)
	time.sleep(2)
	time.sleep(8)
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

	print("Operating wrist..")
	wrist_bent_sh()
	print("Operating finger..")
	time.sleep(1)
	print("Operating wrist..")
	wrist_straight()

# flap() ---> twists the flap in either left of right direction.
# center ---> flap resting position.
# left ---> left side twisted position.
# right ---> right side twisted position.

def flap(direction):
	print("Operating flap..")
	center=260
	left=60
	right=500
	pin=0
	if direction=='l':
		for i in range(center,left,-1):
			pwm.set_pwm(pin,0,i)
		time.sleep(2)
		for i in range(left,center,1):
			pwm.set_pwm(pin,0,i)
	elif direction=='r':
		center=350
		for i in range(center,right,1):
			pwm.set_pwm(pin,0,i)
		time.sleep(2)
		for i in range(right,center,-1):
			pwm.set_pwm(pin,0,i)

# quadrant1() --> it is invoked when object is detected in the quadrant 1.

def quadrant1(binDir):
	print("\n Operating shoulder..")
	shoulder_lf()
	elbow('1')
	flap(binDir)

# quadrant2() --> it is invoked when object is detected in the quadrant 2.

def quadrant2(binDir):
	print("\n Operating shoulder..")
	shoulder_rf()
	elbow('2')
	flap(binDir)

# quadrant12() --> it is invoked when object is detected inbetween both the quadrants.
def quadrant12(binDir):
	print("\n Operating shoulder..")
	elbow('3')
	flap(binDir)