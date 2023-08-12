# References:
# - https://realpython.com/python-sockets/#multi-connection-client
# - https://docs.python.org/3/library/socket.html#

#!/usr/bin/env python3

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]


def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        # Create new socket object:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Put the socket in non-blocking mode:
        sock.setblocking(False)
        # Similar to .connect(address), but returns an error indicator instead of
        # raising an exception for errors returned by the C-level connect() call.
        # The error indicator is 0 if the operation succeeded, otherwise the value
        # of the errno variable. This is useful to support, for example
        # asynchronous connects. Once the connection is completed, the socket is
        # ready for reading and writing and is returned by .select().
        sock.connect_ex(server_addr)
        # To know when the client connection is ready for reading and writing, set
        # both events with the bitwise OR operator:
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # Create the data you want to store with the socket using SimpleNamespace
        data = types.SimpleNamespace(
            # connection id:
            connid=connid,
            # total number of messages:
            msg_total=sum(len(m) for m in messages),
            # total number of received messages:
            recv_total=0,
            # Messages that the client will send to the server are copied using
            # messages.copy() because each connection will call socket.send() and
            # modify the list:
            messages=messages.copy(),
            outb=b"",
        )
        # Register a file object for selection, monitoring it for I/O events, by
        # passing the events mask, socket and data objects to sel.register():
        sel.register(sock, events, data=data)


def service_connection(key, mask):
    # key is the namedtuple returned from .select() that contains the socket object
    # (fileobj) and data object. mask contains the events that are ready.
    sock = key.fileobj
    data = key.data
    # If the socket is ready for reading, then mask & selectors.EVENT_READ will
    # evaluate to True, so sock.recv() is called.
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        # If data was received, it is printed out and its total number of bytes is
        # added to data.recv_total to keep track of what has been received so far:
        if recv_data:
            print(f"Received {recv_data!r} from connection {data.connid}")
            data.recv_total += len(recv_data)
        # The client keeps track of the number of bytes it’s received from the
        # server (data.recv_total) so that it can close its side of the connection.
        # When the server detects this, it closes its side of the connection too.
        if not recv_data or data.recv_total == data.msg_total:
            print(f"Closing connection {data.connid}")
            # Unregister a file object from selection, removing it from monitoring:
            sel.unregister(sock)
            # Close socket:
            sock.close()
    # If the socket is ready for writing, any data stored in data.outb is sent to
    # the server using sock.send(). The bytes sent are then removed from the outb
    # buffer:
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <host> <port> <num_connections>")
    sys.exit(1)

# arguments read from the command-line:
# - host: host IP address;
# - port: host port number;
# - num_conns: umber of connections to create to the server.
host, port, num_conns = sys.argv[1:4]

# initiate connections:
start_connections(host, int(port), int(num_conns))

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
