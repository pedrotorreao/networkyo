// based on: https://github.com/nikhilroxtomar/UDP-Client-Server-Program-in-C

#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>

int main(int argc, char **argv) {
  // port number to be connected to.
  // note: All ports below 1024 are reserved, so we can set a port above 1024
  // and below 65535 unless they are being used by other programs.
  int port = 5550;
  // integer that will represent the file descriptor for the socket:
  int sockfd;
  // structures describing the socket addresses:
  struct sockaddr_in myaddr, remoteAddr;
  // buffer where the message will be stored:
  char buffer[1024];

  socklen_t addr_size;

  // create a new datagram (UDP) socket:
  sockfd = socket(AF_INET, SOCK_DGRAM, 0);

  // initialize the structure variables to NULL:
  memset(&myaddr, '\0', sizeof(myaddr));

  myaddr.sin_family = AF_INET;   // address family.
  myaddr.sin_port = htons(port); // get the 16-bit port # in network byte order
                                 // from the host byte order.
  // 32-bit IP addr. in Network Byte Order:
  myaddr.sin_addr.s_addr = inet_addr("127.0.0.1");

  // assign a local protocol address to a socket:
  bind(sockfd, (struct sockaddr *)&myaddr, sizeof(myaddr));

  addr_size = sizeof(remoteAddr);

  while (1) {
    // receive data from UNCONNECTED datagram sockets:
    recvfrom(sockfd, buffer, 1024, 0, (struct sockaddr *)&remoteAddr, &addr_size);

    if (buffer[0] == '#')
      break;

    printf("\n-- Buffer content: %s\n-- From: %d\n", buffer, remoteAddr.sin_addr.s_addr);

    memset(buffer, '\0', sizeof buffer);
  }

  return 0;
}

/*
# socket: create a new socket of FAMILY in domain TYPE, using
protocol PROTOCOL. If PROTOCOL is zero, one is chosen automatically.
Returns a file descriptor for the new socket, or -1 for errors.
  -> function prototype sample:
        int socket (int FAMILY, int TYPE, int PROTOCOL);

# sockaddr: structure describing a generic socket address.
  -> code sample:
        struct sockaddr {
          unsigned short    sa_family;    // -address family, i.e. AF_INET.
          char              sa_data[14];  // -address data (14 bytes),
                                          // protocol specific.
        };


# sockaddr_in: structure describing an Internet socket address.
  -> code sample:
        struct sockaddr_in {
          short int            sin_family;  // -address family, i.e. AF_INET.
          unsigned short int   sin_port;    // -16-bit port # in Network Byte Order.
          struct in_addr       sin_addr;    // -32-bit IP addr. in Network Byte Order.
          unsigned char        sin_zero[8]; // not used.
        };


# in_addr: 32 bit netid/hostid IP address.
  -> code sample:
        struct in_addr {
          unsigned long s_addr;   // A 32-bit IP address in Network Byte Order.
        };

# htons: function that converts 16-bit (2-byte) quantities from host byte order to network byte order.
  -> function prototype sample:
        unsigned short htons(unsigned short hostshort);

# bind: this function assigns a local protocol address to a socket. This call returns 0 if it successfully binds to the address, otherwise it returns -1 on error.
  -> function prototype sample:
        int bind(int sockfd, struct sockaddr *my_addr,int addrlen);

    - sockfd: socket file descriptor returned by the 'socket' function.
    - my_addr: pointer to struct 'sockaddr' that contains the local IP address and port.
    - addrlen: sizeof(struct sockaddr).

# recvfrom: function used to receive data from UNCONNECTED datagram sockets. This call returns the number of bytes read into the 'buf', otherwise it returns -1 on error. This function reads 'len' bytes into 'buf' through socket 'sockfd'. If address 'from' is not NULL, fill in 'fromlen' bytes of it with the address of
the sender, and store the actual size of the address in 'fromlen'. Return the number of bytes read or -1 for errors.
  -> function prototype sample:
        int recvfrom(
                      int sockfd, void *buf, int len,
                      unsigned int flags struct sockaddr *from, int *fromlen
                    );

    - sockfd: socket descriptor returned by the socket function.
    - buf: buffer to read the information into.
    - len: maximum length of the buffer.
    - flags: set to 0.
    - from: pointer to struct sockaddr for the host where data has to be read.
    - fromlen: sizeof(struct sockaddr).
*/