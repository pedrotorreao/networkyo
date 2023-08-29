# The “server” waits for a client connection, generates a welcome notification
# to the client, and then closes the connection.

import socket

# create new socket object:
# -- AF_INET: Internet address family for IPv4.
# -- SOCK_STREAM: socket type for the TCP protocol.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get current hostname:
host = "127.0.0.1"  # socket.gethostname()

# define port number (non-privileged ports are > 1023):
port = 8080

# bind address (hostname, port number) pair to socket:
server_socket.bind((host, port))

# set up and start TCP listener. It listens for connections
# from clients. When a client connects, the server calls .accept()
# to accept, or complete, the connection:
# -- 1:  backlog parameter, it specifies the number of unaccepted
# connections that the system will allow before refusing new connections.
server_socket.listen(1)

print("... waiting for a client connection ...")

# Wait for an incoming connection. Then, once established the connection,
# return a new socket object representing the connection, and the address
# of the client. For IP sockets, the address info is a pair (hostaddr, port).
client_socket, addr = server_socket.accept()

print("... connection established with: ", addr)

message = "[[ Heey, welcome to the server! ]]"

client_socket.send(message.encode())
client_socket.close()
