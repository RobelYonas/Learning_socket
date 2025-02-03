import socket
import json


def start_client():
    # Get client ID and server IP address from the user.
    client_id = input("Enter Client ID (e.g., 1 or 2): ").strip()
    server_ip = input("Enter the server IP address: ").strip()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((server_ip, 12345))
        print(f"Connected to server at {server_ip}:12345")

        # Send the client ID to the server.
        sock.sendall(client_id.encode())

        # Receive and display the welcome message.
        welcome = sock.recv(1024).decode()
        print("Server:", welcome)

        # If the client is '2', prompt the user for device states.
        if client_id == "2":
            light_state = input("Enter light state (on/off): ").strip().lower()
            door_state = input("Enter door state (open/closed): ").strip().lower()
            window_state = input("Enter window state (open/closed): ").strip().lower()
            update_data = {"light": light_state, "door": door_state, "window": window_state}
            message = json.dumps(update_data)
        else:
            message = f"Hello from Client {client_id}"

        sock.sendall(message.encode())

        # Receive and display the server's response.
        response = sock.recv(1024).decode()
        print("Server:", response)

        # Receive and display the goodbye message.
        goodbye = sock.recv(1024).decode()
        print("Server:", goodbye)
    except Exception as e:
        print("Error:", e)
    finally:
        sock.close()
        print("Disconnected from server.")


if __name__ == "__main__":
    start_client()
