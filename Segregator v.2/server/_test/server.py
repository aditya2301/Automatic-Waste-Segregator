'''
* This script contains code which applies the ML analysis on the detected image in Cloud platform.
* The following dependencies are imported.
* tensorFlow --->  conatins the ML code.
* socket ---> makes the remote connection with the client running on Raspberry Pi.
'''

from tensorFlow import identification
import socket,sys,os,shutil    
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
      name='Image-'+datetime.datetime.now().strftime("%d-%m-%y-%I-%M-%S")+'.jpeg'
      
      directory=datetime.datetime.now().strftime("%d-%m-%Y")
      if not os.path.exists(os.path.join(os.getcwd(),'static',directory)):
         os.makedirs(os.path.join(os.getcwd(),'static',directory))

      with open(name,"wb") as f:
         for i in range(0,length):
            data=c.recv(1)
            f.write(data)

      value=identification(name)
      verdict=""
      direction=""
      if value['bio']>value['nonbio']:
        verdict='bio'
        direction='l'#rotate left for bio
      else:
        verdict='nonbio' #rotate right for nonbio
        direction='r'
      new_name=datetime.datetime.now().strftime("%d-%m-%y_%I-%M-%S %p_{}_{}_{}_.jpeg".format(format(value['bio'],'f'),format(value['nonbio'],'f'),verdict))
      os.rename(name,new_name)
      shutil.move(new_name,os.path.join(os.getcwd(),'static',directory))
      print(verdict)
      c.send(bytes(direction,"utf-8"))
      c.close()

   except KeyboardInterrupt:
      c.close()
      s.close()
      break
      
   except Exception as e:
    if type(e).__name__=="EOFError":
      sys.exit()
    print(e)
    c.close()
    continue