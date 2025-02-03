import socket

HOST = '127.0.0.1'
PORT = 5060

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

server_message = client_socket.recv(1024).decode()
print(f"Server says: {server_message}")

client_socket.send(b"Hi from Client 1")

final_message = client_socket.recv(1024).decode()
print(f"Server says: {final_message}")

client_socket.close()
