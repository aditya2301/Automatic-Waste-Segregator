from tensorFlow import identification
import socket,sys,os            
import datetime

s = socket.socket()         
port = 60000
host = socket.gethostname()
print(host)               
print(os.getcwd())
s.bind((host, port))        
s.listen(5)     
print("Socket is listening")            
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
