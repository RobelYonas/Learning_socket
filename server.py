import socket
import threading

HOST = '127.0.0.1'
PORT = 5060

# Dictionary to store {name: socket}
clients = {}


def handle_client(client_socket, client_address):
    print(f"Client connected: {client_address}")

    # Ask for client's name
    client_socket.send(b"What is your name?")
    name = client_socket.recv(1024).decode().strip()

    if not name:
        name = f"Guest{len(clients)+1}"

    # Store the client in dictionary
    clients[name] = client_socket

    # Send welcome message
    welcome_msg = f"Welcome {name}!"
    client_socket.send(welcome_msg.encode())

    # Notify other clients
    broadcast(f"{name} has joined the chat!", sender_name=name)

    while True:
        try:
            msg = client_socket.recv(1024).decode().strip()
            if msg.lower() == "exit":
                break
            print(f"{name} says: {msg}")

            # Check for private message format "/msg <user> <message>"
            if msg.startswith("/msg "):
                parts = msg.split(" ", 2)  # Split into 3 parts: "/msg", username, message
                if len(parts) < 3:
                    client_socket.send(b"Invalid private message format. Use: /msg <user> <message>")
                    continue

                recipient_name, private_msg = parts[1], parts[2]

                if recipient_name in clients:
                    recipient_socket = clients[recipient_name]
                    recipient_socket.send(f"[Private] {name}: {private_msg}".encode())
                else:
                    client_socket.send(f"User {recipient_name} not found.".encode())

            else:
                broadcast(f"{name}: {msg}", sender_name=name)

        except Exception as e:
            print(f"Error with {name}: {e}")
            break

    # Remove client from dictionary and close connection
    print(f"{name} has disconnected.")
    del clients[name]
    client_socket.close()
    broadcast(f"{name} has left the chat.")


def broadcast(message, sender_name=None):
    """Send a message to all connected clients, except the sender."""
    for client_name, client_socket in clients.items():
        if client_name != sender_name:
            try:
                client_socket.send(message.encode())
            except:
                # Remove client if sending fails
                client_socket.close()
                del clients[client_name]


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        server_socket.close()


main()
