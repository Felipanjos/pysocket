from socket import *

print('Attempting to start server on port 9900..')
sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('127.0.0.1', 9900)) 
sock.listen(SOMAXCONN) 

print ('Server is now listening on port 9900!')
client, addr = sock.accept() 
print (client)
print ('Waiting for data...')
data = client.recv(4096) 
print ('Received data from client: ' + str(data)) 
print ("ok")
client.sendall(data)
print ("Sent the same data back to the client!")
