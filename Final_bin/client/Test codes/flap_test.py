import time,Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

def flap(direction):
    print("Operating flap..")
    center=185
    left=80
    right=360
    pin=0
    if direction=='l':
        for i in range(center,left,-1):
            pwm.set_pwm(pin,0,i)
            #time.sleep(0.01)
        time.sleep(2)
        for i in range(left,215,1):
            pwm.set_pwm(pin,0,i)
            #time.sleep(0.01)
    elif direction=='r':
        center=170
        for i in range(center,right,1):
            pwm.set_pwm(pin,0,i)
            #time.sleep(0.01)
        time.sleep(2)
        for i in range(right,center,-1):
            pwm.set_pwm(pin,0,i)
            #time.sleep(0.01)

flap('l')
time.sleep(2)
flap('r')