'''import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18,GPIO.HIGH)
time.sleep(5)
GPIO.output(18,GPIO.LOW)
GPIO.cleanup()


t=["hello world","my name","khan"]
temp=[]
for i in t:
	#print("i.split()-%S , [i]-%S",str(i.split()),str([i]))
	if len(i.split())>1:
		i=i.split()
		for z in i:
			temp.append(z)
		continue
	temp.append(i)

print(temp)
'''
import os
textfile=open("biodegradable.txt","r")
textfile=textfile.readlines()
images=os.listdir("img")
#print(images)
for text in textfile:
	#print(text[:-1])
	text=text[:-1]
	#image=image+"\n"
	if not text+".jpg" in images  :
		if not text+".jpeg" in images  :
			print(text+".jpg")