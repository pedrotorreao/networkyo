### TABLE OF CONTENTS

- [OSI MODEL](#osi-model-open-systems-interconnection)
- [INTERNET PROTOCOL (IP)](#internet-protocol-ip)
- [USER DATAGRAM PROTOCOL (UDP)](#user-datagram-protocol-udp)
- [TRANSMISSION CONTROL PROTOCOL (TCP)](#transmission-control-protocol-tcp)

# NETWORKING FUNDAMENTALS

## OSI MODEL (OPEN SYSTEMS INTERCONNECTION)

Conceptual model which enables different communication systems to communicate with each other using standard protocols. This model consists in splitting up a communication system into 7 abstract layers.

### Layer 7 - Application (HTTP, FTP, gRPC, SMTP)

Human-computer interaction layer, where applications can access the network services. Software applications like web browsers and email clients rely on the application layer to initiate communications. However, client software applications are not part of the Application Layer; rather this Layer is responsible for the protocols and data manipulation that the software relies on to present meaningful data to the user.

```
          request
        +-------->
WEBSITE             APPLICATION LAYER
        <--------+
          response
```

### Layer 6 - Presentation (Encoding, Serialization)

Ensures that data is in an usable format and is where data encryption works. Layer responsible for preparing data so that it can be used by the Application layer, i.e. this layer makes the data presentable for applications to consume. It is also responsible for translation (`encoding`), encryption (`encrypt/unencrypt`) and compression (`speed/efficiency`) of data.

```
ENCRYPTION +--------> COMPRESSION +--------> TRANSLATION
```

### Layer 5 - Session (Connection establishment, TLS)

Maintains connections and is responsible for controlling ports and sessions. The time between the opening and closing of a connection is known as session. This Layer also ensures that the session stays open long enough to transfer all the data being exchanged, and finishes the session to avoid wasting resources. The session layer also synchronizes data tranfers with checkpoints. For example, if a `100MB` file is being transferred, the Session Layer could set a checkpoint every `5MB`. This way, in the event that some error happens during the transference when `58MB` have already been transferred, the session could be resumed from the last checkpoint, i.e. `55MB`, and only `45MB` would be left to transfer instead of having to transfer the whole file again.

### Layer 4 - Transport (UDP, TCP)

Transmits data using transmission protocols such as TCP and UDP. Layer responsible for end-to-end communication between two devices. This includes taking data from the Session Layer and breaking it up into chunks called _**segments**_ before sending it to the Network layer. The Transport layer on the receiving end is responsible for reassembling the _**segments**_ into data that the Session layer can consume. This layer also performs flow control and error control. Flow control determines an optimal speed of transmission to ensure that one device do not overwhelm the other. Error control makes sure that the data received is complete, and request a retransmission if it isn't.

```
SEGMENTATION +--------> TRANSPORT +--------> REASSEMBLY
```

### Layer 3 - Network (IP - Internet Protocol)

Decides which physical path the data will take. It is responsible for facilitating data transfer between two different networks. If the two devices communicating are on the same network, then the Network layer is unnecessary. This layer breaks up _**segments**_ from the Transport layer into smaller units called **_packets_** on the sender's device and reassembles them on the receiver's device. It also finds the best physical path for the data to reach its destination, which is knows as **routing**.

### Layer 2 - Datalink (Frames, MAC Address)

Defines the format of the data in the network. Similar to the Network layer, except that the Datalink layer facilitates data transfer between two devices on the same network. It takes packets from the Network layer and breaks them into smaller pieces called **_frames_**. Also, it is responsible from flow control and error control in intra-network communication.

### Layer 1 - Physical (Electric signals, fiber, radio waves)

Transmits raw bit streams over the physical medium. It includes the physical equipment involved in the data transfer, such as cables and switches. This is also the layer where data gets converted into a bit stream. The Physical layer of both devices must also agree on a signal convention so that the `1`s can be distinguished from the `0`s on both devices.

[TABLE OF CONTENTS](#table-of-contents)

# INTERNET PROTOCOL (IP)

... [TABLE OF CONTENTS](#table-of-contents)

# USER DATAGRAM PROTOCOL (UDP)

... [TABLE OF CONTENTS](#table-of-contents)

# TRANSMISSION CONTROL PROTOCOL (TCP)

... [TABLE OF CONTENTS](#table-of-contents)

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

# USEFUL COMMAND LINE TOOLS

### `ping`

### `tcpdump`

### `netcat`

# REFERENCES

- [Socket Programming in Python (Guide)](https://realpython.com/python-sockets/)
- [Berkeley sockets](https://en.wikipedia.org/wiki/Berkeley_sockets)
- [Unix domain socket](https://en.wikipedia.org/wiki/Unix_domain_socket)
- [Inter-process communication](https://en.wikipedia.org/wiki/Inter-process_communication)
- [OSI Model](https://osi-model.com/)
