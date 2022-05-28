import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    clientsocket, adress = s.accept()
    print(f"Conexão com o endereço {adress} estabelecida")
    clientsocket.send(bytes("Bem vindo à casa de leilões.\n", "utf-8"))
    clientsocket.send(bytes("Digite (1) para vendedor, ou (2) para comprador", "utf-8"))
    # clientsocket.close()
    