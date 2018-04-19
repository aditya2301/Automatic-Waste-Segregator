import socket                   # Import socket module

s = socket.socket()             # Create a socket object
#host = input("enter your server IP address")    # Get local machine name
port = 60000                 # Reserve a port for your service.
#
s.connect(("192.168.2.4", port))
s.send("Hello server!")

data = s.recv(2)
s.close()
print(data.decode("utf-8"))