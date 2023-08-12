# Reference:
# - https://realpython.com/python-sockets/#multi-connection-server
# - https://docs.python.org/3/library/socket.html#

#!/usr/bin/env python3

import sys
import socket
import selectors
import types

# The default selector class uses the most efficient implementation available
# on the current platform:
sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    # Establishes the connection and returns a new socket object representing the
    # connection, and the address of the client. For IP sockets, the address info
    # is a pair (hostaddr, port):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    # Put the socket in non-blocking mode. If it blocks, then the entire server
    # is stalled until it returns. That means other sockets are left waiting even
    # though the server isn’t actively working:
    conn.setblocking(False)
    # Create an object to hold the data that you want packed along with the socket:
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    # To know when the client connection is ready for reading and writing, set both
    # events with the bitwise OR operator:
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    # Register a file object for selection, monitoring it for I/O events, by passing
    # the events mask, socket and data objects to sel.register():
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    # key is the namedtuple returned from .select() that contains the socket object
    # (fileobj) and data object. mask contains the events that are ready.
    sock = key.fileobj
    data = key.data
    # If the socket is ready for reading, then mask & selectors.EVENT_READ will
    # evaluate to True, so sock.recv() is called. Any data that’s read is appended
    # to data.outb so that it can be sent later:
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        # Data was received, append it to data.outb:
        if recv_data:
            data.outb += recv_data
        # No data received, the client has closed their socket, so the server
        # should close it too:
        else:
            print(f"Closing connection to {data.addr}")
            # Unregister a file object from selection, removing it from monitoring:
            sel.unregister(sock)
            sock.close()
    # If the socket is ready for writing, which should always be the case for a
    # healthy socket, any received data stored in data.outb is echoed to the client
    # using sock.send(). The bytes sent are then removed from the send buffer:
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            # .send() returns the number of bytes sent, which can then be used with
            # slice notation on the .outb buffer to discard the bytes sent:
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


# Usage: multiconn-server.py <host> <port>
# sys.argv[0]:  multiconn-server.py
# sys.argv[1]:  <host>
# sys.argv[2]:  <port>
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
# Create new socket object:
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind address pair (hostname, port number) to socket:
lsock.bind((host, port))
# Set up and start TCP listener. It listens for connections from clients. When a
# client connects, it calls .accept() to accept, or complete, the connection:
lsock.listen()
print(f"Listening on {(host, port)}")
# Configure the socket in non-blocking mode. When used alongside sel.select(),
# you can wait for events on one or more sockets and then read and write data
# when it's ready:
lsock.setblocking(False)
# Register the socket to be monitored with sel.select() for the events that
# you’re interested in. For the listening socket, you want read events:
# selectors.EVENT_READ:
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        # Check for I/O completion on more than one socket. Call .select() to see
        # which sockets have I/O ready for reading/writing. It blocks until there
        # are sockets ready for I/O. It returns a list of tuples, one for each
        # socket. Each tuple contains a key and an event mask:
        events = sel.select(timeout=None)
        for key, mask in events:
            # It's a listening socket and you need to accept the connection by
            # calling the accept_wrapper() function to get the new socket object
            # and register it with the selector:
            if key.data is None:
                accept_wrapper(key.fileobj)
            # It's a client socket that's already been accepted and you need to
            # service it by calling service_connection() with key and mask as
            # arguments:
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
