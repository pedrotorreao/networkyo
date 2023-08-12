# The “client” creates/establishes a connection with the server,
# retrieves the welcome message, and then closes the connection.

import socket

# create new socket object:
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# get current hostname:
host = socket.gethostname()
# define port number:
port = 8080

# initiate TCP server connection. Establish a connection to the server
# and initiate the three-way handshake:
client_socket.connect((host, port))

message = client_socket.recv(1024)  # 1024: buffer size

print(message.decode())

client_socket.close()
