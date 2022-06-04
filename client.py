# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
import socket
from mensagens import *
import errno
import sys

HEADER_LENGTH = 1024
IP = '127.0.0.1'
PORT = 5000
udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp.connect((IP, PORT))
udp.setblocking(True)

artigos = {}

def qtd_artigos():
    return len(artigos)

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
    receive_msg(udp)

def iniciar_leilao():
    print(start_auction)
    nome = str(input("Nome: "))
    desc = str(input("Descrição: "))
    valor = float(input("Valor: ")) 
    send_msg("artigonovo " + "nome:" + nome + " descricao:" + desc + " valor:" + str(valor))
    try_receive()

    
def checa_cliente(cliente):
    if (cliente == '1'):
        return "Comprador"
    elif (cliente == '2'):
        return "Vendedor"
    else:
        return False

def send_msg(message):
    message = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    udp.send(message_header + message)

def receive_msg(client_socket):
    message_header = client_socket.recv(HEADER_LENGTH)
    message_length = int(message_header.decode('utf-8').strip())
    message = client_socket.recv(message_length).decode('utf-8')
    print(message)
    return message

cliente = checa_cliente(str(input(menu_definir_cliente)))
while not (cliente):
    cliente = checa_cliente(str(input(menu_definir_cliente)))

my_email = input("Email: ")
send_msg(my_email)

if (cliente == "Vendedor"):
    print(opcoesVendedor)
elif (cliente == "Comprador"):
    print(opcoesComprador)

rodar = True
while rodar == True:
    message = input(f'{my_email} > ')
    match cliente:
        case "Comprador":
            match message:
                case "1":
                    lista_artigos()
                case "2":
                    print("comprador escolheu 2")
        case "Vendedor":
            match message:
                case "1":
                    iniciar_leilao()
                case "2":
                    print("vendedor escolheu 2")
                case "3":
                    rodar = False
    if message:
        send_msg(message)
    if (message == "salve"):
        try_receive()
udp.close()