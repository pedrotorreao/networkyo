import socket
import threading

HOST = "127.0.0.1"
PORT = 11223


def message_handler(client_sckt):
    while 1:
        message = client_sckt.recv(1024).decode("utf-8")
        if message != "":
            message_components = message.split(" >> ")

            username = message_components[0]
            content = message_components[1]

            print(f"[{username}] {content}")
        else:
            print("... empty message from server")


def send_message(username, client_sckt):
    while 1:
        message = input(f"{username}: ")
        if message != "":
            client_sckt.send(message.encode())
        else:
            print("Empty message")
            exit(0)


def service_connection(client_sckt):
    client_username = input("Please enter a username: ")
    if client_username != "":
        client_sckt.sendall(client_username.encode())
    else:
        print("!! Username cannot be empty !!")
        exit(0)

    threading.Thread(target=message_handler, args=(client_sckt,)).start()

    send_message(client_username, client_sckt)


def main():
    client_sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_sckt.connect((HOST, PORT))
        print(f"Connecting to server {HOST} : {PORT}")

        message = client_sckt.recv(1024)
        print(message.decode())
    except:
        print(f"Unable to connect to server {HOST} : {PORT}")

    service_connection(client_sckt)
    # client_sckt.close()


if __name__ == "__main__":
    main()
