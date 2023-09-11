import socket
import threading

HOST = "127.0.0.1"
PORT = 21216

client_connections = []
client_usernames = []


def remove_client(client_connection, client_username):
    client_connections.remove(client_connection)
    client_connection.close()
    client_usernames.remove(client_username)


def broadcast_message(msg):
    for client in client_connections:
        client.send(msg)


def handle_client(c_sckt):
    while True:
        try:
            message_rcvd = c_sckt.recv(1024)
            if not message_rcvd:
                break

            broadcast_message(message_rcvd)
        except:
            client_username = client_usernames[client_connections.index(c_sckt)]

            remove_client(c_sckt, client_username)

            broadcast_message(f"_{client_username} has left the chat!".encode("ascii"))

            break


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    print(f"_SERVER RUNNING ON {HOST} : {PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"_CONNECTION ESTABLISHED WITH {client_address[0]} : {client_address[1]}")

        client_socket.sendall("_WELCOME TO THE CHAT SERVER!\n".encode("ascii"))

        client_socket.send("_USERNAME:".encode("ascii"))
        client_username = client_socket.recv(1024).decode("ascii")

        client_connections.append(client_socket)
        client_usernames.append(client_username)

        broadcast_message(
            f"_USER: {client_username} has joined the chat!".encode("ascii")
        )

        threading.Thread(target=handle_client, args=(client_socket,)).start()


# call the main function if this script is being run directly:
if __name__ == "__main__":
    main()
