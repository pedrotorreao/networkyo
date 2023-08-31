import socket
import threading

HOST = "127.0.0.1"
PORT = 11223
LISTENER_LIMIT = 10

active_users = []


def message_handler(client_sckt, client_username):
    while 1:
        partial_message = client_sckt.recv(1024).decode("utf-8")
        if partial_message != "":
            final_message = client_username + " >> " + partial_message
            broadcast_message(final_message)
        else:
            bye_user_message = "SERVER >> " + f"{client_username} has left the chat"
            active_users.pop((client_username, client_sckt))
            # print(f"... empty message from {client_username}")
            break


def broadcast_message(message):
    for user in active_users:
        client_sckt = user[1]
        client_sckt.sendall(message.encode())


def client_handler(client_sckt):
    while 1:
        client_username = client_sckt.recv(1024).decode("utf-8")

        if client_username != "":
            active_users.append((client_username, client_sckt))
            new_user_message = "SERVER >> " + f"{client_username} has joined the chat"
            broadcast_message(new_user_message)
            break
        else:
            print("Unable to establish connection < client username is empty >")

    threading.Thread(
        target=message_handler,
        args=(
            client_sckt,
            client_username,
        ),
    ).start()


def main():
    server_sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_sckt.bind((HOST, PORT))
        print(f"Running the server {HOST} : {PORT}")
    except:
        print(f"Unable to bind to host {HOST} : {PORT}")

    server_sckt.listen(LISTENER_LIMIT)

    print("... waiting for a client connection")

    while 1:
        client_sckt, client_addr = server_sckt.accept()

        print(f"... connection established with {client_addr[0]} : {client_addr[1]}")

        client_sckt.send("< Welcome to the chat server! >".encode())

        threading.Thread(target=client_handler, args=(client_sckt,)).start()
        # client_sckt.close()


if __name__ == "__main__":
    main()
