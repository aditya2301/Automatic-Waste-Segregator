'''
* This program runs on the cloud machine where Machine Learning analysis takes place.
* The following dependencies are imported.
* tensorFlow --->  conatins the ML code.
* socket ---> makes the remote connection with the client running on Raspberry Pi.
'''

from tensorFlow import identification
import socket,sys,os            
import datetime

# s ---> initialised to socket class.
s = socket.socket()         
port = 60000
host = socket.gethostname()
print(host)               
print(os.getcwd())
s.bind((host, port))        
s.listen(5)     
print("Socket is listening")      

'''
* c ---> client device id.
* addr ---> client device address.
* length ---> gets the file size.
* The image is received one byte at a time and stored with name = name.
* value ---> receives the result of the ML analysis.
'''

while True:
   try:
      c, addr = s.accept()     
      print('Got connection from', addr)
      length=c.recv(10)
      length=int(length.decode("utf-8"))
      c.send(bytes('OK','utf-8'))
      name='Image-'+datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S")+'.jpeg'
      with open(name,"wb") as f:
         for i in range(0,length):
            data=c.recv(1)
            f.write(data)
      value=identification(name)
      c.send(bytes(value,"utf-8"))
      c.close()
   except Exception as e:
   	if type(e).__name__=="EOFError":
   		sys.exit()
   	print(e)
   	c.close()
   	continue