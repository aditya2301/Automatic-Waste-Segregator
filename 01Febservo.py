# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 305  # Min pulse length out of 4096
servo_max = 455  # Max pulse length out of 4096



# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

for i in range(305,455,1):
    print(i)
    # Move servo on channel O between extremes.
    pwm.set_pwm(0, 0, i)
    time.sleep(0.01)
    pwm.set_pwm(0, 0, i)
    time.sleep(0.01)

for i in range(455,345,-1):
    print(i)
    pwm.set_pwm(0, 0, i)
    time.sleep(0.01)
    pwm.set_pwm(0, 0, i)
    time.sleep(0.01)


for i in range(133,530,1):
    print(i)
    # Move servo on channel O between extremes.
    pwm.set_pwm(15, 0, i)
    time.sleep(0.01)
    pwm.set_pwm(15, 0, i)
    time.sleep(0.01)

    


print('Moving servo on channel 0, press Ctrl-C to quit...')
for i in range(150,250,1):
    print(i)
    # Move servo on channel O between extremes.
    pwm.set_pwm(11, 0, i)
    time.sleep(0.01)
    pwm.set_pwm(11, 0, i)
    time.sleep(0.01)

for i in range(250,120,-1):
    print(i)
    pwm.set_pwm(11, 0, i)
    time.sleep(0.01)
    pwm.set_pwm(11, 0, i)
    time.sleep(0.01)


for i in range(530,132,-1):
    print(i)
    pwm.set_pwm(15, 0, i)
    time.sleep(0.01)
    pwm.set_pwm(15, 0, i)
    time.sleep(0.01)
