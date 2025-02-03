import socket
import threading
import json


def handle_client(conn, addr):
    try:
        # First, receive the client ID from the client.
        client_id = conn.recv(1024).decode().strip()
        print(f"Connected with Client {client_id} from {addr}")

        # Send a welcome message using the provided client ID.
        welcome = f"Hello from Server to Client {client_id}!"
        conn.sendall(welcome.encode())

        # Now wait for the next message (the payload update or simple text).
        message = conn.recv(1024).decode().strip()

        # If the message looks like a JSON update, process it.
        if message.startswith("{") and message.endswith("}"):
            try:
                update = json.loads(message)
                with open("House.json", "w") as json_file:
                    json.dump(update, json_file, indent=4)
                response = "House.json updated successfully."
            except json.JSONDecodeError:
                response = "Error: Provided JSON is invalid."
            conn.sendall(response.encode())
        else:
            print(f"Client {client_id} says: {message}")
            conn.sendall("Message received.".encode())

        # Finally, send a goodbye message.
        goodbye = f"Goodbye Client {client_id}!"
        conn.sendall(goodbye.encode())

    except Exception as e:
        print(f"Error with Client {client_id}: {e}")
    finally:
        conn.close()


def setup_house_file():
    # Initialize House.json with default values.
    default_state = {"light": "on", "door": "open", "window": "open"}
    with open("House.json", "w") as json_file:
        json.dump(default_state, json_file, indent=4)
    print("House.json initialized with default settings.")


def start_server(host="0.0.0.0", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    setup_house_file()

    try:
        while True:
            conn, addr = server_socket.accept()
            # Handle each client connection in a new thread.
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
