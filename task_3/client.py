import socket
import json

class HouseClient:
    def __init__(self, server_ip, server_port=12345):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.sock.connect((self.server_ip, self.server_port))
            print(f"[INFO] Connected to server at {self.server_ip}:{self.server_port}")
        except Exception as e:
            print(f"[ERROR] Could not connect to server: {e}")
            exit(1)

    def send_update(self):
        try:
            # Prompt the user for input on the house state
            light_state = input("Enter light state (on/off): ").strip().lower()
            door_state = input("Enter door state (open/closed): ").strip().lower()
            window_state = input("Enter window state (open/closed): ").strip().lower()

            # Build a dictionary and convert it to a JSON string
            update_data = {
                "light": light_state,
                "door": door_state,
                "window": window_state
            }
            update_message = json.dumps(update_data)
            print(f"[INFO] Sending JSON update to server: {update_message}")

            # Send the JSON update to the server
            self.sock.sendall(update_message.encode())

            # Wait for the server's acknowledgment
            response = self.sock.recv(1024).decode()
            print(f"[INFO] Server response: {response}")
        except Exception as e:
            print(f"[ERROR] Error during communication: {e}")
        finally:
            self.sock.close()

    def run(self):
        self.connect()
        self.send_update()

if __name__ == "__main__":
    # Prompt for the server's IP address (allowing remote connection)
    server_ip = input("Enter the server IP address: ").strip()
    client = HouseClient(server_ip)
    client.run()
