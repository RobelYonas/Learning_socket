import socket

HOST = '127.0.0.1'
PORT = 5060

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Server is listening on port 5060...")

client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

client_socket.send(b"Hi from Server")
client_message = client_socket.recv(1024).decode()
print(f"Client says: {client_message}")
client_socket.send(b"Welcome Client 1!")

client_socket.close()
server_socket.close()
