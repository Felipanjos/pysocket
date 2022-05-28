import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

mensagem_completa = ''
while True:
    mensagem = s.recv(8)
    if len(mensagem) <= 0:
        break
    mensagem_completa += mensagem.decode("utf-8")
print(mensagem_completa)