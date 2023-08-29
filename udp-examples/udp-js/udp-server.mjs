// this module provides an implementation of UDP datagram sockets:
import dgram from 'dgram';

// create socket:
const server_socket = dgram.createSocket('udp4');

// port number:
const port = 5555;

// host address (localhost):
const hostaddr = '127.0.0.1';

// bind address (port number, hostname) to socket:
server_socket.bind(port, hostaddr);

// start UDP listener:
server_socket.on('message', (msg, info) => {
  console.log(
    `Server received datagram:\n --message: ${msg}, \nfrom:\n --address: ${info.address},\n --family: ${info.family},\n --port: ${info.port}\n\n`
  );
});

/*
to test this, we can use built-in utility netcat:
    -> nc -u ip port  [Enter]
    -> your_message   [Enter]
*/
