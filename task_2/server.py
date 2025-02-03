import socket
import threading
import json

class ClientHandler(threading.Thread):
    def __init__(self, sock, address, client_number):
        super().__init__()
        self.sock = sock
        self.address = address
        self.client_number = client_number

    def run(self):
        print(f"[INFO] Client {self.client_number} connected from {self.address}")
        
        # Send a welcome message
        welcome = f"Hello from Server to Client {self.client_number}!"
        self.sock.sendall(welcome.encode())
        print(f"[DEBUG] Sent to Client {self.client_number}: {welcome}")
        
        try:
            # Wait for a message from the client
            message = self.sock.recv(1024).decode()
            print(f"[DEBUG] Received from Client {self.client_number}: {message}")
            
            # Check if the message is a JSON update
            if message.strip().startswith("{") and message.strip().endswith("}"):
                try:
                    update = json.loads(message)
                    with open("House.json", "w") as json_file:
                        json.dump(update, json_file, indent=4)
                    confirmation = "House.json updated successfully."
                    self.sock.sendall(confirmation.encode())
                    print(f"[DEBUG] JSON update from Client {self.client_number}: {update}")
                except json.JSONDecodeError:
                    error_msg = "Error: Provided JSON is invalid."
                    self.sock.sendall(error_msg.encode())
                    print(f"[ERROR] Invalid JSON received from Client {self.client_number}")
            else:
                print(f"[INFO] Message from Client {self.client_number}: {message}")

            # Send a final response
            goodbye = f"Goodbye Client {self.client_number}!"
            self.sock.sendall(goodbye.encode())
            print(f"[DEBUG] Sent final message to Client {self.client_number}: {goodbye}")
        
        except Exception as e:
            print(f"[ERROR] Exception with Client {self.client_number}: {e}")
        
        finally:
            self.sock.close()
            print(f"[INFO] Connection with Client {self.client_number} closed.")


class SocketServer:
    def __init__(self, host="localhost", port=12345, max_connections=5):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id_counter = 1

    def setup_house_file(self):
        # Initialize the House.json file with default values
        default_state = {
            "light": "on",
            "door": "open",
            "window": "open"
        }
        with open("House.json", "w") as json_file:
            json.dump(default_state, json_file, indent=4)
        print("[INFO] House.json initialized with default settings.")

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_connections)
        print(f"[INFO] Server listening on {self.host}:{self.port}")
        self.setup_house_file()
        
        try:
            while True:
                client_sock, client_addr = self.server_socket.accept()
                handler = ClientHandler(client_sock, client_addr, self.client_id_counter)
                handler.start()
                self.client_id_counter += 1
        except KeyboardInterrupt:
            print("\n[INFO] Server is shutting down.")
        finally:
            self.server_socket.close()


if __name__ == "__main__":
    server = SocketServer()
    server.start()
