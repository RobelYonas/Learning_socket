import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 5060))

server_socket.listen(5)
print("Server is listening ....")

client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

client_socket.send(b"What is your name")
name = client_socket.recv(1024).decode()

client_socket.send(str.encode(f"Hi {name}"))
msg = client_socket.recv(1024).decode()


client_socket.close()
server_socket.close()
