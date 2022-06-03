# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252
import socket
import sys
import errno
from mensagens import *

def iniciar_leilao():
    print(start_auction)
    nome = str(input("Nome: "))
    desc = str(input("Descrição: "))
    valor = float(input("Valor: ")) 

    send_msg("lancenovo " + "nome:" + nome + " descricao:" + desc + " valor:" + str(valor))

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

cliente = checa_cliente(str(input(menu_definir_cliente)))

while not (cliente):
    cliente = checa_cliente(str(input(menu_definir_cliente)))

if (cliente == "Vendedor"):
    print(opcoesVendedor)
elif (cliente == "Comprador"):
    print(opcoesComprador)

my_email = input("Email: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

client_socket.setblocking(False)

send_msg(my_email)

while True:
    message = input(f'{my_email} > ')

    match cliente:
        case "Comprador":
            match message:
                case "1":
                    print("comprador escolheu 1")
                case "2":
                    print("comprador escolheu 2")
        case "Vendedor":
            match message:
                case "1":
                    # send_msg(iniciar_leilao())
                    teste = iniciar_leilao()
                case "2":
                    print("vendedor escolheu 2")

    if message:
        send_msg(message)

    try:
        # first_msg = receive_msg(client_socket, 1)
        # print(first_msg)
        msg = receive_msg(client_socket, None)
        print(msg)

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Erro na leitura: {}'.format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        print('Erro na leitura: {}'.format(str(e)))
        sys.exit()