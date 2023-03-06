import socket
import threading

# define the host and port to listen on
HOST = '127.0.0.1'
PORT = 5000

# create a TCP socket and bind it to the host and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# create a list to hold all connected clients
clients = []

def handle_client(client_socket, address):
    """Handle a single client connection"""
    # add the client to the list of connected clients
    clients.append((client_socket, address))

    # send a welcome message to the client
    client_socket.send(b"Welcome to the chatroom!\n")

    while True:
        try:
            # receive a message from the client
            message = client_socket.recv(1024)
            if not message:
                break
            # broadcast the message to all other connected clients
            for c in clients:
                if c[0] != client_socket:
                    c[0].send(message)
        except Exception as e:
            print("Error handling client:", e)
            break

    # remove the client from the list of connected clients
    clients.remove((client_socket, address))
    print("Client disconnected:", address)

def start_server():
    """Start the server"""
    server_socket.listen()

    print("Server listening on {}:{}".format(HOST, PORT))

    while True:
        # accept incoming connections
        client_socket, address = server_socket.accept()

        # start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.daemon = True
        client_thread.start()

if __name__ == '__main__':
    start_server()
