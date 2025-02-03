import socket
import threading
import json
import tkinter as tk

# Server configuration
HOST = '127.0.0.1'
PORT = 5060
clients = {}  # Stores connected clients
json_filename = "House.json"

# Create JSON file with initial state
def create_json_file():
    initial_data = {
        "light": "on",
        "door": "open",
        "window": "open"
    }
    with open(json_filename, "w") as f:
        json.dump(initial_data, f)

# Load JSON state
def load_json():
    with open(json_filename, "r") as f:
        return json.load(f)

# Update the JSON file and refresh the GUI
def update_json(key, value):
    house_state = load_json()
    
    if key in house_state:
        house_state[key] = value  # Update specific key
        with open(json_filename, "w") as f:
            json.dump(house_state, f)
        refresh_gui(house_state)
    else:
        print(f"Invalid update request: {key} is not a valid field")

# Function to refresh the graphical interface
def refresh_gui(state):
    canvas.itemconfig(light_circle, fill="yellow" if state["light"] == "on" else "gray")
    canvas.itemconfig(door_triangle, fill="green" if state["door"] == "open" else "red")
    canvas.itemconfig(window_square, fill="blue" if state["window"] == "open" else "white")

# Function to handle each client
def handle_client(client_socket, client_address):
    print(f"Client connected: {client_address}")

    try:
        client_socket.send(b"What is your name?")
        name = client_socket.recv(1024).decode().strip()

        if not name:
            name = f"Guest{len(clients) + 1}"
        clients[name] = client_socket

        welcome_msg = f"Welcome {name}!"
        client_socket.send(welcome_msg.encode())

        while True:
            msg = client_socket.recv(1024).decode().strip()
            if not msg or msg.lower() == "exit":
                break

            print(f"{name} says: {msg}")

            # Parse update commands (e.g., "update light off")
            if msg.startswith("update"):
                parts = msg.split()
                if len(parts) == 3:
                    _, key, value = parts
                    update_json(key, value)
                    client_socket.send(f"{key} updated to {value}".encode())
                else:
                    client_socket.send(b"Invalid update command. Use: update <key> <value>")
            else:
                broadcast(f"{name}: {msg}", sender_name=name)

    except Exception as e:
        print(f"Error with {name}: {e}")

    print(f"{name} has disconnected.")
    del clients[name]
    client_socket.close()
    broadcast(f"{name} has left the chat.")

# Function to broadcast messages to all clients
def broadcast(message, sender_name=None):
    for client_name, client_socket in clients.items():
        if client_name != sender_name:
            try:
                client_socket.send(message.encode())
            except:
                client_socket.close()
                del clients[client_name]

# GUI Initialization
def setup_gui():
    global canvas, light_circle, door_triangle, window_square

    root = tk.Tk()
    root.title("House State Visualization")

    canvas = tk.Canvas(root, width=300, height=300)
    canvas.pack()

    # Light (Circle)
    light_circle = canvas.create_oval(50, 50, 100, 100, fill="yellow")

    # Door (Triangle)
    door_triangle = canvas.create_polygon(150, 200, 130, 250, 170, 250, fill="green")

    # Window (Square)
    window_square = canvas.create_rectangle(200, 50, 250, 100, fill="blue")

    # Load initial state
    refresh_gui(load_json())

    threading.Thread(target=main, daemon=True).start()
    root.mainloop()

# Main server function
def main():
    create_json_file()  # Ensure JSON file exists
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

setup_gui()
