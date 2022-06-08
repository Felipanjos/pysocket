# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
import socket
from mensagens import *
import errno
import sys

SIZE = 4096
IP = '127.0.0.1'
PORT = 5000
udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp.connect((IP, PORT))
udp.setblocking(True)

nome = None
meus_artigos = {}
print(opcoesVendedor)

def send_msg(message):
    message = message.encode('utf-8')
    message_header = f"{len(message):<{SIZE}}".encode('utf-8')
    udp.send(message_header + message)

def try_receive():
    try:
        receive_msg(udp)

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Erro na leitura: {}'.format(str(e)))
            sys.exit()

    except Exception as e:
        print('Erro na leitura: {}'.format(str(e)))
        sys.exit()


def iniciar_leilao():
    print(start_auction)
    desc = str(input("Descrição: "))
    valor = float(input("Lance mínimo: ")) 
    artigo = {
        "id": len(meus_artigos),
        "descricao": desc,
        "valor": valor,
        "aberto": True
    }
    meus_artigos[(len(meus_artigos))] = artigo
    send_msg("artigonovo " + "nome:" + nome + " descricao:" + desc + " valor:" + str(valor))
    try_receive()

def encerrar_leilao():
    id = input(end_auction)
    send_msg("encerrar" + id)
    try_receive()

def listar_meus_artigos():
    send_msg("listar_meus_artigos" + nome)
    try_receive()

def receive_msg(client_socket):
    message_header = client_socket.recv(SIZE)
    message_length = int(message_header.decode('utf-8').strip())
    message = client_socket.recv(message_length).decode('utf-8')
    print(message)
    return message

rodar = True
while rodar == True:
    message = input(f'-> ')
    match message:
        case "1":
            if (nome is None):
                nome = input("Informe seu nome: ")
            iniciar_leilao()
        case "2":
            encerrar_leilao()
        case "3":
            if (nome is None):
                nome = input("Informe seu nome: ")
            listar_meus_artigos()
        case "4":
            rodar = False
    if message:
        send_msg(message)
    if (message == "salve"):
        try_receive()
udp.close()