import socket
def clientResponse():
	#os.system("clear")
	s = socket.socket()         
	port = 60000              
	s.connect(('192.168.2.4', port))
	print("connected")
	f=open("newimg.jpg","rb")
	data=f.read()
	f.close()
	print("\nSending Length information..")
	length=str(len(data))
	s.send(bytes(length,"utf-8"))
	
	status=s.recv(2)
	print("Length Reception Acknowledgement - "+str(status.decode("utf-8")))
	print("Sending the image to server for Tensorflow processing. . .")
	f=open("newimg.jpg","rb")
	data=f.read(1)
	# Progress bar to indicate status of sending the image.
	length=int(length)
	count=0
	counter=0
	slab=int(length/10)
	print("\nProgress-")
	while data:
		s.send(data)
		data=f.read(1)
		count+=1
		if count==slab:
		    counter+=1
		    sys.stdout.write('\r')
		    sys.stdout.write('['+"#"*counter+" "*(10-counter)+']'+" "+str(counter*10)+"%")
		    sys.stdout.flush()
		    count=0
	sys.stdout.write("\n")
	sys.stdout.flush()
	print("Sent sucessfully!")
	f.close()
	
	binFlag=s.recv(20)
	print("Server response received.")
	if str(binFlag.decode("utf-8"))=="l":
		print("Object is biodegradable. Rotating bin on the left side.")
	elif str(binFlag.decode("utf-8"))=="r":
		print("Object is non-biodegradable. Rotating bin on the right side.")
	s.close()


clientResponse()