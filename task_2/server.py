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
        # Send a welcome message to the client
        self.sock.sendall(f"Hello from Server to Client {self.client_number}!".encode())
        try:
            message = self.sock.recv(1024).decode().strip()
            # If the message looks like JSON, update the House.json file
            if message.startswith("{") and message.endswith("}"):
                try:
                    update = json.loads(message)
                    with open("House.json", "w") as json_file:
                        json.dump(update, json_file, indent=4)
                    self.sock.sendall("House.json updated successfully.".encode())
                except json.JSONDecodeError:
                    self.sock.sendall("Error: Provided JSON is invalid.".encode())
            else:
                print(f"Client {self.client_number}: {message}")
            # Send a final goodbye message
            self.sock.sendall(f"Goodbye Client {self.client_number}!".encode())
        except Exception as e:
            print(f"Error with Client {self.client_number}: {e}")
        finally:
            self.sock.close()

class SocketServer:
    def __init__(self, host="localhost", port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id_counter = 1

    def setup_house_file(self):
        # Initialize House.json with default values
        default_state = {"light": "on", "door": "open", "window": "open"}
        with open("House.json", "w") as json_file:
            json.dump(default_state, json_file, indent=4)
        print("House.json initialized with default settings.")

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        self.setup_house_file()
        try:
            while True:
                client_sock, client_addr = self.server_socket.accept()
                handler = ClientHandler(client_sock, client_addr, self.client_id_counter)
                handler.start()
                self.client_id_counter += 1
        except KeyboardInterrupt:
            print("Server is shutting down.")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = SocketServer()
    server.start()
