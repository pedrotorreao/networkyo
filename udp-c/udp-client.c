#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>

/*
--> argc - argument count:
      Number of command line arguments that are passed to the main() function, number of strings pointed to by argv.
--> argv- argument vector:
      Array of string arguments.
        argv[0]: it is always the name of the program.
        argv[1...n]: string arguments themselves.
*/
int main(int argc, char **argv) {
  if (argc != 2) {
    printf("Usage: %s <port>\n", argv[0]);
    exit(0);
  }
  // port number passed as argument:
  int port = atoi(argv[1]);
  // integer that will represent the file descriptor for the socket:
  int sockfd;
  // structures describing the socket addresses:
  struct sockaddr_in serverAddr;
  // buffer where the message will be stored:
  char buffer[1024];

  socklen_t addr_size;

  // create a new datagram (UDP) socket:
  sockfd = socket(PF_INET, SOCK_DGRAM, 0);

  // initialize the structure variables to NULL:
  memset(&serverAddr, '\0', sizeof(serverAddr));

  serverAddr.sin_family = AF_INET;   // address family.
  serverAddr.sin_port = htons(port); // get the 16-bit port # in network byte order
                                     // from the host byte order.

  // 32-bit IP addr. in Network Byte Order:
  serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

  //
  // strcpy(buffer, "Hello Server\n");

  //
  // sendto(sockfd, buffer, 1024, 0, (struct sockaddr *)&serverAddr, sizeof(serverAddr));
  // printf("[+]Data Send: %s", buffer);

  while (1) {
    char *message;
    size_t m_size = 1024;
    size_t m_chars;

    message = (char *)malloc(m_size * sizeof(char));

    if (message == NULL) {
      perror("Unable to allocate buffer\n");
      exit(1);
    }

    printf(">>:: ");

    m_chars = getline(&message, &m_size, stdin);

    // copy message to be sent into the buffer:
    strcpy(buffer, message);
    // if a '#' is entered, break out of the message loop:
    if (buffer[0] == '#')
      break;

    // send data over UNCONNECTED datagram sockets:
    sendto(sockfd, buffer, 1024, 0, (struct sockaddr *)&serverAddr, sizeof(serverAddr));
    printf("[+]Data Sent: %s", buffer);

    // clear the buffer for the next message:
    memset(buffer, '\0', sizeof buffer);

    // free heap allocated memory:
    free(message);
    message = NULL;
  }

  return 0;
}