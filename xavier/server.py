import socket
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
msg = "chegou"

udp.bind(orig)
# udp.sendto(str.encode(msg), orig)

while True:
    msgCliente, cliente = udp.recvfrom(1024)
    
    if not msgCliente:
        break

    print(msgCliente.decode('utf-8'))
    
    if (msgCliente.decode('utf-8') == 'teste'):
        udp.sendto(str.encode(msg), orig)
cliente.close()