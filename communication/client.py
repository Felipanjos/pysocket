import socket

sock = None
try:
    print ("Creating socket")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print ("Connecting to localhost on port 9900")
    sock.connect(('127.0.0.1', 9900))
    print ("Connection success!")
except socket.error as msg:
    print ("Failed to create and connect. Error code: " + str(msg[0]) + " , Error message : " + msg[1]) 
    exit()

data = input("Enter data to send to server: ")  
print ('Attempting to send data over the socket...')
sock.sendall(data.encode('utf-8'))
print ('Data sent to server! Now waiting for response...')
data = sock.recv(4096)
print ("Received response:" + str(data)) 
