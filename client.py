from http import client
import socket
import sys
import errno

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
my_email = input("Email: ")

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare email and header and send them
# We need to encode email to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
email = my_email.encode('utf-8')
email_header = f"{len(email):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(email_header + email)

def receive_message(server_socket):
    try:
        # Receive our "header" containing message length, it's size is defined and constant
        message_header = server_socket.recv(HEADER_LENGTH)
        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False
        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())
        # Return an object of message header and message data
        return {'header': message_header, 'data': server_socket.recv(message_length)}
    except:
        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False

while True:
    # Wait for user to input a message
    message = input(f'{my_email} > ')
    # If message is not empty - send it
    if message:
        # Encode message to bytes, prepare header and convert to bytes, like for email above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    server_socket, server_adress = client_socket.accept()
    # server = receive_message(server_socket)
    # if server is False:
    #     continue
    # print(server['data'].decode('utf-8'))
    print(server_socket.recv(1024).decode('utf-8'))

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:
            # Receive our "header" containing email length, it's size is defined and constant
            email_header = client_socket.recv(HEADER_LENGTH)
            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(email_header):
                print('Connection closed by the server')
                sys.exit()
            # Convert header to int value
            email_length = int(email_header.decode('utf-8').strip())
            # Receive and decode email
            email = client_socket.recv(email_length).decode('utf-8')
            # Now do the same for message (as we received email, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            # Print message
            print(f'{email} > {message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()