import socket
import threading

HOST = '127.0.0.1'
PORT = 5060

def receive_messages(client_socket):
    """Function to continuously receive messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(message)
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Receive the name prompt and send name
print(client_socket.recv(1024).decode())
name = input("Enter your name: ").strip()
client_socket.send(name.encode())

# Receive welcome message
print(client_socket.recv(1024).decode())

# Start thread to receive messages
threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

while True:
    msg = input()
    if msg.lower() == "exit":
        client_socket.send(msg.encode())
        break
    client_socket.send(msg.encode())

client_socket.close()
