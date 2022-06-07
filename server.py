import socket
import select
from mensagens import *

SIZE = 1024
IP = "127.0.0.1"
PORTA = 5000

def send_msg(socket, message):
    message = message.encode('utf-8')
    message_header = f"{len(message):<{SIZE}}".encode('utf-8')
    socket.send(message_header + message)

udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp.bind((IP, PORTA))
udp.listen()

sockets_list = [udp]
clientes = {}
artigos = {}

print(f'Bem vindo ao sistema de leilão! Aguardando conexões ({IP}:{PORTA})...')

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(SIZE)
        
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False

def get_artigos_vendedor(nome):
    string = ""
    tem_artigos = False
    for key, value in artigos.items():
        if value['nome'] == nome:
            tem_artigos = True
            maior_lance = "Nenhum" if value['maior_lance'] == 0 else value['maior_lance']
            
            string += 'ID: {}. Descrição: {}. Maior lance até o momento: {}.\n'.format(key, value['descricao'], maior_lance)
            send_msg(notified_socket, string)
    if not tem_artigos:
        send_msg(notified_socket, "Você não tem artigos registrados.")
        
def get_artigos_string():
    string = ""
    tem_aberto = False
    for key, value in artigos.items():
        if value['aberto']:
            tem_aberto = True
            
            maior_lance = "Nenhum" if value['maior_lance'] == 0 else value['maior_lance']

            string += 'ID: {}. Descrição: {}. Maior lance até o momento: {}.\n'.format(key, value['descricao'], maior_lance)
            send_msg(notified_socket, string)
    if not tem_aberto:
        send_msg(notified_socket, "Não há artigos em leilão.")

def novo_artigo():

    nome = {
        "start": aux_msg.find("nome:"),
        "end": aux_msg.find("nome:") + len("nome:"),
    }
    desc = {
        "start": aux_msg.find(" descricao:"),
        "end": aux_msg.find(" descricao:") + len(" descricao:"),
    }
    valor = {
        "start": aux_msg.find(" valor:"),
        "end": aux_msg.find(" valor:") + len(" valor:"),
    }
    artigo = {
        "id": len(artigos),
        "nome": aux_msg[nome['end'] : desc['start']],
        "descricao": aux_msg[desc['end'] : valor['start']],
        "valor": aux_msg[valor['end'] : ],
        "aberto": True,
        "cliente_maior_lance": None,
        "maior_lance": 0,
    }

    artigos[(len(artigos))] = artigo
    send_msg(notified_socket, "     Artigo adicionado com sucesso.")

def encerrar_leilao(id):    
    id = int(id)
    if (id not in artigos):
        send_msg(notified_socket, "ID inválido.")
    else: 
        maior_lance = artigos[id]["maior_lance"]
        descricao = artigos[id]["descricao"]
        artigos[id]["aberto"] = False
        if (float(maior_lance) > 0):
            send_msg(notified_socket, "Leilão do item \"" + artigos[id]["nome"] + "\" encerrado.\n Vencedor: " + artigos[id]["cliente_maior_lance"] + ".\n Maior lance: " + str(maior_lance) + ".")
        elif(maior_lance == "Nenhum" or maior_lance == 0):
            send_msg(notified_socket, "Leilão do item \"" + descricao + "\" encerrado. Não houveram lances para o item em questão.")

def registra_lance():
    artigo = {
        "start": aux_msg.find("artigo:"),
        "end": aux_msg.find("artigo:") + len("artigo:"),
    }
    valor = {
        "start": aux_msg.find(" valor:"),
        "end": aux_msg.find(" valor:") + len(" valor:"),
    }
    email = {
        "start": aux_msg.find(" email:"),
        "end": aux_msg.find(" email:") + len(" email:"),
    }

    lance = {
        "artigo": int(aux_msg[artigo["end"] : valor["start"]]),
        "valor": aux_msg[valor["end"] : email["start"]], 
        "email": aux_msg[email["end"] : ], 
    }

    id_artigo = lance["artigo"]
    if (id_artigo not in artigos):
        send_msg(notified_socket, "ID inválido.")
    else:
        if artigos[id_artigo]["aberto"]:
            maior_lance = float(artigos[id_artigo]["maior_lance"])
            if(float(artigos[id_artigo]["valor"]) > float(lance["valor"])):
                send_msg(notified_socket, "Lance mínimo: " + artigos[id_artigo]["valor"] + ".")
            else :
                if (float(lance["valor"]) > maior_lance):
                    artigos[id_artigo]["maior_lance"] = lance["valor"]
                    artigos[id_artigo]["cliente_maior_lance"] = lance["email"]
                    send_msg(notified_socket, "Lance confirmado. É o maior lance até então!")
                else:
                    send_msg(notified_socket, "Lance confirmado. Não é o maior lance até então.")
        else:
            send_msg(notified_socket, "O leilão deste artigo já fechou.")
            
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    for notified_socket in read_sockets:
        if notified_socket == udp:

            client_socket, client_address = udp.accept()
            # user = receive_message(client_socket)

            # if user is False:
            #     continue

            sockets_list.append(client_socket)
            clientes[client_socket] = client_socket
            print('Nova conexão. Endereço: {}:{}'.format(*client_address))
        
        else:
            message = receive_message(notified_socket)
            if message is False:
                print('Conexão encerrada: {}:{}'.format(*client_address))
                
                sockets_list.remove(notified_socket)
                
                del clientes[notified_socket]
                continue
            
            client_socket = clientes[notified_socket]
            aux_msg = message["data"].decode("utf-8")

            print(f'{aux_msg}')
            
            if(aux_msg[0 : 10] == "artigonovo"):
                novo_artigo()
            
            if(aux_msg[0 : 13] == "lista_artigos"):
                get_artigos_string()

            if(aux_msg.startswith("encerrar")):
                encerrar_leilao(aux_msg[len("encerrar") : ])

            if(aux_msg.startswith("listar_meus_artigos")):
                get_artigos_vendedor(aux_msg[len("listar_meus_artigos") : ])

            if(aux_msg.startswith("novo_lance")):
                registra_lance()

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clientes[notified_socket]