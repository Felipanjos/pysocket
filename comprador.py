from mensagens import *
import socket
import errno
import sys

SIZE = 1024
IP = '127.0.0.1'
PORT = 5000
udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp.connect((IP, PORT))
udp.setblocking(True)

meu_email = ''

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

def lista_artigos():
    send_msg("lista_artigos")
    try_receive()

def faz_lance():
    meu_email = input("Informe seu e-mail para contato: ")
    artigo = input(artigo_lance)
    valor = input(valor_lance)
    send_msg("novo_lance" + "artigo:" + artigo +" valor:" + valor + " email:" + meu_email)
    try_receive()

def receive_msg(client_socket):
    message_header = client_socket.recv(SIZE)
    message_length = int(message_header.decode('utf-8').strip())
    message = client_socket.recv(message_length).decode('utf-8')
    print(message)
    return message

send_msg(meu_email)
print(opcoesComprador)

rodar = True
while rodar == True:
    message = input(f'-> ')
    match message:
        case "1":
            lista_artigos()
        case "2":
            faz_lance()
        case "3":
            rodar = False
    if message:
        send_msg(message)
udp.close()