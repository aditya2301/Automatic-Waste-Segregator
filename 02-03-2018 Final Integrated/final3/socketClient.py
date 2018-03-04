import socket  ,sys ,time            

# Create a socket object
s = socket.socket()         

# Define the port on which you want to connect
port = 80              

# connect to the server on local computer
s.connect(('IP addr of the server', port))


f=open("7.jpeg","rb")
data=f.read()
f.close()
length=str(len(data))
s.send(bytes(length,"utf-8"))

status=s.recv(10)
print("Length Received status - "+str(status.decode("utf-8")))

f=open("7.jpeg","rb")
data=f.read(1)
while d:
	s.send(data)
	data=f.read(1)
f.close()

binFlag=s.recv(20)
print("Left/Right side of the bin - ",str(binFlag.decode("utf-8")))
s.close()
