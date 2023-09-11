import socket
import threading

HOST = "127.0.0.1"
PORT = 21216


def define_username():
    valid_username = False

    while not valid_username:
        username = input("Please choose a non-empty username: ")
        if username != "":
            valid_username = True

    return username


def receive_messages(c_sckt, usr):
    while True:
        try:
            message_rcvd = c_sckt.recv(1024).decode("ascii")
            if message_rcvd == "_USERNAME:":
                c_sckt.send(usr.encode("ascii"))
            else:  #
                print(message_rcvd)
        except:
            print("-> Connection has been closed!")
            c_sckt.close()
            break


def send_messages(c_sckt, username):
    while True:
        user_message = input()

        final_message = "<" + username + ">" + ":: " + user_message

        c_sckt.send(final_message.encode("ascii"))


def main():
    username = define_username()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print(f"CONNECTED TO SERVER {HOST} : {PORT}")
    print(client_socket.recv(1024).decode())

    threading.Thread(target=receive_messages, args=(client_socket, username)).start()
    threading.Thread(target=send_messages, args=(client_socket, username)).start()


if __name__ == "__main__":
    main()
