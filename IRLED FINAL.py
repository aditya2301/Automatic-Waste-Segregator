import RPi.GPIO as IO
import os
import time
from twilio.rest import Client
IO.setmode(IO.BCM)
IO.setup(14,IO.IN) #GPIO 14 -> IR sensor as input for bio degradable 
IO.setup(2,IO.IN) #GPIO 2 -> IR sensor as input for non bio degradable bin
while True:
	if (IO.input(14)==False): #object is near
		flag=1
		x="NON-BIODEGRADABLE"
		break

	if (IO.input(2)==False): #object is near
		flag=1
		x="BIODEGRABLE"
		break

	if(flag==1):
		mess="ALERT!!!"+x+" bin is full"
		account_sid = "AC3b65d4b08b4242625715cb559f5410b0"
		auth_token = "a4f4e1298494f1e9f166df22e48912f2"
		client = Client(account_sid, auth_token)
		client.api.account.messages.create(
			to="+918147661833",
			from_="+18043125524",
			 body=mess)
		os.echo("message sent")
		break
