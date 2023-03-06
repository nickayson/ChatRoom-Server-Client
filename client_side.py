import socket
import threading

# define the host and port to connect to
HOST = '127.0.0.1'
PORT = 5000

def receive_messages(sock):
    """Receive messages from the server and print them to the console"""
    while True:
        try:
            # receive a message from the server
            message = sock.recv(1024)
            if not message:
                break
            print(message.decode(), end='')
        except Exception as e:
            print("Error receiving message:", e)
            break

def start_client():
    """Start the client"""
    # create a TCP socket and connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # prompt the user to enter their name
    name = input("Enter your name: ")

    # send the user's name to the server
    sock.send(name.encode() + b" has joined the chat.\n")

    # start a new thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        try:
            # prompt the user to enter a message
            message = input()
            if message == "/quit":
                break
            # send the message to the server
            sock.send("{}: {}\n".format(name, message).encode())
        except Exception as e:
            print("Error sending message:", e)
            break

    # send a disconnect message to the server
    sock.send(name.encode() + b" has left the chat.\n")
    sock.close()

if __name__ == '__main__':
    start_client()
