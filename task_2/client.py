import socket
import json

class SocketClient:
    def __init__(self, client_id, server_host="localhost", server_port=12345):
        self.client_id = client_id
        self.server_host = server_host
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.sock.connect((self.server_host, self.server_port))
            print(f"[INFO] Client {self.client_id} connected to {self.server_host}:{self.server_port}")
        except Exception as e:
            print(f"[ERROR] Client {self.client_id} failed to connect: {e}")
            exit(1)

    def exchange_messages(self):
        try:
            # Receive the welcome message from the server
            welcome = self.sock.recv(1024).decode()
            print(f"[SERVER -> Client {self.client_id}]: {welcome}")

            # If client_id is 2, prompt the user to type in the update values
            if self.client_id == 2:
                # Ask the user to input the states manually
                light_state = input("Enter light state (on/off): ").strip().lower()
                door_state = input("Enter door state (open/closed): ").strip().lower()
                window_state = input("Enter window state (open/closed): ").strip().lower()
                
                # Build a dictionary with the user's input and convert it to JSON
                update_data = {
                    "light": light_state,
                    "door": door_state,
                    "window": window_state
                }
                message = json.dumps(update_data)
                print(f"[CLIENT {self.client_id} -> SERVER]: Sending JSON update: {message}")
            else:
                # For other clients, send a simple text message
                message = f"Hello from Client {self.client_id}"
                print(f"[CLIENT {self.client_id} -> SERVER]: Sending message: {message}")

            self.sock.sendall(message.encode())

            # Receive a confirmation or error message from the server
            server_response = self.sock.recv(1024).decode()
            print(f"[SERVER -> Client {self.client_id}]: {server_response}")

            # Receive the final message from the server
            final_msg = self.sock.recv(1024).decode()
            print(f"[SERVER -> Client {self.client_id}]: {final_msg}")

        except Exception as e:
            print(f"[ERROR] Client {self.client_id} encountered an error: {e}")
        finally:
            self.sock.close()
            print(f"[INFO] Client {self.client_id} disconnected.")

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
