import socket
import threading
import json
import tkinter as tk


def update_graphics(data, canvas, light, door, window):
    # Update light: yellow for "on", gray for "off"
    if data.get("light", "").lower() == "on":
        canvas.itemconfig(light, fill="yellow")
    else:
        canvas.itemconfig(light, fill="gray")

    # Update door: green for "open", red for "closed"
    if data.get("door", "").lower() == "open":
        canvas.itemconfig(door, fill="green")
    else:
        canvas.itemconfig(door, fill="red")

    # Update window: blue for "open", black for "closed"
    if data.get("window", "").lower() == "open":
        canvas.itemconfig(window, fill="blue")
    else:
        canvas.itemconfig(window, fill="black")


def handle_client(client_socket, client_address, root, canvas, light, door, window):
    print(f"Connection established with {client_address}")
    while True:
        try:
            message = client_socket.recv(1024).decode().strip()
            if not message:
                break

            # If message looks like JSON, update House.json and GUI.
            if message.startswith("{") and message.endswith("}"):
                update_data = json.loads(message)
                with open("House.json", "w") as f:
                    json.dump(update_data, f, indent=4)
                print("Updated House.json with:", update_data)
                # Schedule the GUI update on the main thread.
                root.after(0, update_graphics, update_data, canvas, light, door, window)
            # Send an acknowledgment.
            client_socket.sendall(b"Update received and applied!")
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break

    client_socket.close()
    print(f"Connection with {client_address} closed.")


def accept_clients(server_socket, root, canvas, light, door, window):
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(
            target=handle_client,
            args=(client_socket, client_address, root, canvas, light, door, window)
        ).start()


def setup_gui():
    root = tk.Tk()
    root.title("House State")
    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()
    # Draw graphical objects.
    light = canvas.create_oval(50, 50, 150, 150, fill="yellow")   # Light
    door = canvas.create_polygon(200, 200, 250, 300, 150, 300, fill="green")  # Door
    window = canvas.create_rectangle(300, 50, 350, 100, fill="blue")   # Window
    return root, canvas, light, door, window


def setup_house_file():
    default_state = {"light": "on", "door": "open", "window": "open"}
    with open("House.json", "w") as f:
        json.dump(default_state, f, indent=4)
    print("House.json initialized with default settings.")


def start_server():
    host = "0.0.0.0"
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    setup_house_file()
    root, canvas, light, door, window = setup_gui()

    # Start accepting clients in a separate daemon thread.
    threading.Thread(
        target=accept_clients,
        args=(server_socket, root, canvas, light, door, window),
        daemon=True
    ).start()

    print("Server thread started. Launching GUI.")
    root.mainloop()
    server_socket.close()


if __name__ == "__main__":
    start_server()
