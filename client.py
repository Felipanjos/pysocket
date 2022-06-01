# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

from http import client
import socket
import sys
import errno
from mensagens import *

def send_msg(message):
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

def receive_msg(client_socket, number):
    message_header = client_socket.recv(HEADER_LENGTH)
    
    if (number == 1):
        if not len(message_header):
            print('Connection closed by the server')
            sys.exit()
    
    message_length = int(message_header.decode('utf-8').strip())
    message = client_socket.recv(message_length).decode('utf-8')
    return message

HEADER_LENGTH = 30
IP = "127.0.0.1"
PORT = 1234
my_email = input("Email: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

client_socket.setblocking(False)

send_msg(my_email)

print(menu)

while True:
    message = input(f'{my_email} > ')
    match message:
        case "1":
            print(welcomeComprador)
        case "2":
            print(welcomeVendedor)
        case "3":
            break
        
    if message:
        send_msg(message)

    try:
        while True:
            first_msg = receive_msg(client_socket, 1)
            print(first_msg)
            msg = receive_msg(client_socket, None)
            print(msg)
            print(f'{first_msg} > {message}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Erro na leitura: {}'.format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        print('Erro na leitura: {}'.format(str(e)))
        sys.exit()