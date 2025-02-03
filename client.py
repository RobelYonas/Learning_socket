import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))

msg = client_socket.recv(1024).decode()
print(f"Server says: {message}")
