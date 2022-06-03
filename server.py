# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

import socket
import select
from mensagens import *
import json

HEADER_LENGTH = 1024
IP = "127.0.0.1"
PORT = 5000

def send_msg(socket, message):
    message = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    socket.send(message_header + message)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {}

print(f'Bem vindo ao sistema de leilão! Aguardando conexões ({IP}:{PORT})...')

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False

def get_lances():
    with open('lances.txt', 'r') as arquivo:
        return str(len(arquivo.readlines())) 
qtd_lances = get_lances()
def novo_lance():
    nome = {
        "start": decoded['message'].find("nome:"),
        "end": decoded['message'].find("nome:") + len("nome:"),
    }
    desc = {
        "start": decoded['message'].find(" descricao:"),
        "end": decoded['message'].find(" descricao:") + len(" descricao:"),
    }
    valor = {
        "start": decoded['message'].find(" valor:"),
        "end": decoded['message'].find(" valor:") + len(" valor:"),
    }
    lance = {
        "nome": decoded['message'][nome['end'] : desc['start']],
        "descricao": decoded['message'][desc['end'] : valor['start']],
        "valor": decoded['message'][valor['end'] : ]
    }

    lance = get_lances() + " " + lance['nome'] + " " + lance['descricao'] + " " + str(lance['valor'])

    with open('lances.txt', 'a') as arquivo:
        arquivo.write(json.dumps(lance) + '\n')

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    for notified_socket in read_sockets:
        if notified_socket == server_socket:

            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            user['adress'] = client_address

            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user
            print('Cliente conectado. Email: {}. Endereço: {}:{}'.format(user['data'].decode('utf-8'), *client_address))
        
        else:
            message = receive_message(notified_socket)
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                
                sockets_list.remove(notified_socket)
                
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            
            decoded = {
                "email": user["data"].decode("utf-8"),
                "message": message["data"].decode("utf-8")
            }
            
            print(f'{decoded["email"]}: {decoded["message"]}')
            
            if (decoded['message'] == "salve"): send_msg(notified_socket, NOME + "Resposta do servidor")
            if(decoded['message'][0 : 9] == "lancenovo"):
                antes = int(get_lances())
                novo_lance()
                if (int(get_lances()) == antes + 1):
                    send_msg(notified_socket, "Artigo adicionado com sucesso.")

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]