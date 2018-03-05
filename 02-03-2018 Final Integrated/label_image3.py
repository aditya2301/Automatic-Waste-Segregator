from label_image import identification
import socket,sys               

s = socket.socket()         
print("Socket successfully created")

port =80                

s.bind(('', port))        
print("socket binded to %s" %(port))
s.listen(5)     
print("socket is listening")            
#c,addr=s.accept()
while True:
   #counter=0
   try:
   	c, addr = s.accept()     
   	print('Got connection from', addr)
   	length=c.recv(10)
   	length=int(length.decode("utf-8"))
   	#print(length)
   	c.send(bytes('OK','utf-8'))
   	with open('imageNew.jpeg',"wb")as f:
   		for i in range(0,length):
   			data=c.recv(1)
   			f.write(data)
   	value=identification("imageNew.jpeg")
   	c.send(bytes(value,"utf-8"))
   	c.close()
   	#sys.exit()
   except Exception as e:
   	if type(e).__name__=="EOFError":
   		sys.exit()
   	print(type(e).__name__)
   	c.close()
   	continue
