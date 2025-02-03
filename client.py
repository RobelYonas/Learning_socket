import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5060))

msg = client_socket.recv(1024).decode()
print(f"Server says: {msg}")

name = input("what is your name")
client_socket.send(name.encode())

response = client_socket.recv(1024).decode()
print(f"server sent: {response}")

client_socket.close()
