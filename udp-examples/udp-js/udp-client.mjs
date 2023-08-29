// this module provides an implementation of UDP datagram sockets:
import dgram from 'dgram';

// import { Buffer } from 'buffer';

// create socket:
const client_socket = dgram.createSocket('udp4');

// port number:
const port = 5555;

// host address (localhost):
const hostaddr = '127.0.0.1';

// message:
const message = 'Hello, server!';

// connect sockets and send message:
client_socket.send(message, port, hostaddr, (err) => {
  console.log('...bad news');
  client_socket.close();
});
