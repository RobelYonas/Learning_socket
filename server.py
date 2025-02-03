import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('127.0.0.1', 12345))

server_socket.listen(5)
print("Server is listening ....")

client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

client_socket.send("Hi From server")

msg = client_socket.recv(1024).decode()
print(f"Client says: {msg}")

client_socket.close()
server_socket.close()
