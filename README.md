# UNIX SOCKET PROGRAMMING

### DEFINITION

Sockets are the endpoints of a two-way communications channel and allow communication between two different processes on the same or different machines. Sockets are communication points on the same or different computers to exchange data. Sockets are supported by Unix, Windows, Mac, and many other operating systems.

### SOCKET TYPES

- **Stream sockets - SOCK_STREAM**: delivery is guaranteed in a networked environment. If you send through the stream socket three items `A`, `B` and `C`, they will arrive in the same order. These sockets use _**TCP**_ (Transmission Control Protocol) for data transmission. If delivery is impossible, the sender receives an error indicator. Data records do not have any boundaries.
- **Datagram sockets - SOCK_DGRAM**: delivery is not guaranteed in a networked environment. They're connectionless because you don't need to have an open connection as in Stream Sockets − you build a packet with the destination information and send it out. They use _**UDP**_ (User Datagram Protocol).
- **Raw sockets**: provide users access to the underlying communication protocols, which support socket abstractions. These sockets are normally datagram oriented, though their exact characteristics are dependent on the interface provided by the protocol.
- **Sequenced Packet sockets**: similar to a stream socket, with the exception that record boundaries are preserved. This interface is provided only as a part of the Network Systems (NS) socket abstraction, and is very important in most serious NS applications. Sequenced-packet sockets allow the user to manipulate the Sequence Packet Protocol (SPP) or Internet Datagram Protocol (IDP) headers on a packet or a group of packets.

---

# NETWORKING IN PYTHON

### SOCKET PROGRAMMING WITH PYTHON

- Socket: Low-level networking interface that makes it possible for two devices to communicate over a network. Sockets are the endpoints of communication links between two devices that provide a two-way flow of information between them. Sockets may communicate within a process, between processes on the same machine, or between processes on different continents. The `socket` library provides specific classes for handling the common transports as well as a generic interface for handling the rest. Devices are identified by an Internet Protocol (IP) address and a Port Number.

- Client-Server model: A server listens and responds to incoming requests from clients, and a client send requests to servers.

- TCP vs UDP: Two main transport protocols used in socket programming. UDP is a simple non-connection oriented protocol, whereas TCP is reliable, connection-oriented.

- Blocking vs Non-Blocking Sockets: With “blocking” sockets, the program waits for a response from the other device before continuing. With “non-blocking” sockets, the program continues to run as long as a response is received.

- Socket Methods:
  - socket(): create new socket object.
  - bind(): binds address (hostname, port number pair) to socket.
  - listen(): sets up and start TCP listener.
  - accept(): passively accept TCP client connection, waiting until connection arrives (blocking).
  - connect(): initiates TCP server connection.
  - send(): transmits TCP message.
  - recv(): receives TCP message.
  - recvfrom(): receives UDP message.
  - sendto(): transmits UDP message.
  - close(): closes socket.
  - gethostname(): returns the hostname.

---

## ADDITIONAL NOTES:

#### File descriptor:

In Unix and Unix-like computer operating systems, a file descriptor (FD, less frequently fildes) is a process-unique identifier (handle) for a file or other input/output resource, such as a pipe or network socket.

File descriptors typically have non-negative integer values, with negative values being reserved to indicate "no value" or error conditions.[source](https://en.wikipedia.org/wiki/File_descriptor)

#### TCP - Transmission Control Protocol:

Why should you use TCP?

- _Is reliable_: Packets dropped in the network are detected and retransmitted by the sender.
- _Has in-order data delivery_: Data is read by your application in the order it was written by the sender.

#### IPC - Inter Process Communication:

Mechanisms provided by an operating system for processes to manage shared data. Typically, applications can use IPC, categorized as clients and servers, where the client requests data and the server responds to client requests. Many applications are both clients and servers, as commonly seen in distributed computing.[source](https://en.wikipedia.org/wiki/Inter-process_communication)

# REFERENCES

- [Socket Programming in Python (Guide)](https://realpython.com/python-sockets/)
- [Berkeley sockets](https://en.wikipedia.org/wiki/Berkeley_sockets)
- [Unix domain socket](https://en.wikipedia.org/wiki/Unix_domain_socket)
- [Inter-process communication](https://en.wikipedia.org/wiki/Inter-process_communication)
