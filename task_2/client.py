import socket
import json

class SocketClient:
    def __init__(self, client_id, server_host="localhost", server_port=12345):
        self.client_id = client_id
        self.server_host = server_host
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        self.sock.connect((self.server_host, self.server_port))
        print(f"Client {self.client_id} connected to {self.server_host}:{self.server_port}")

    def exchange_messages(self):
        try:
            # Receive the welcome message from the server
            welcome = self.sock.recv(1024).decode()
            print("Server:", welcome)

            # For Client 2, prompt the user for device states; otherwise, send a simple message.
            if self.client_id == 2:
                light_state = input("Enter light state (on/off): ").strip().lower()
                door_state = input("Enter door state (open/closed): ").strip().lower()
                window_state = input("Enter window state (open/closed): ").strip().lower()
                update_data = {"light": light_state, "door": door_state, "window": window_state}
                message = json.dumps(update_data)
            else:
                message = f"Hello from Client {self.client_id}"
            
            self.sock.sendall(message.encode())

            # Receive the server's response
            response = self.sock.recv(1024).decode()
            print("Server:", response)

            final_msg = self.sock.recv(1024).decode()
            print("Server:", final_msg)
        except Exception as e:
            print("Error:", e)
        finally:
            self.sock.close()
            print(f"Client {self.client_id} disconnected.")

    def run(self):
        self.connect_to_server()
        self.exchange_messages()

if __name__ == "__main__":
    try:
        client_number = int(input("Enter Client ID (e.g., 1 or 2): "))
    except ValueError:
        print("Invalid input. Please enter a numeric Client ID.")
        exit(1)
        
    client = SocketClient(client_id=client_number)
    client.run()
