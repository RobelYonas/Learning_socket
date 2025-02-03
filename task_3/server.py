import socket
import threading
import json
import tkinter as tk

class HouseServer:
    def __init__(self, host="0.0.0.0", port=12345):
        self.host = host
        self.port = port
        
        # Create and bind the server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[INFO] Server listening on {self.host}:{self.port}")
        
        # Set up the Tkinter GUI for graphical representation
        self.root = tk.Tk()
        self.root.title("House State")
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        
        # Draw graphical objects for the house devices
        self.light = self.canvas.create_oval(50, 50, 150, 150, fill="yellow")   # Circle for light
        self.door = self.canvas.create_polygon(200, 200, 250, 300, 150, 300, fill="green")  # Triangle for door
        self.window = self.canvas.create_rectangle(300, 50, 350, 100, fill="blue")   # Square for window

    def update_graphics(self, data):
        # Update light color: yellow for "on", gray for "off"
        if data.get("light", "").lower() == "on":
            self.canvas.itemconfig(self.light, fill="yellow")
        else:
            self.canvas.itemconfig(self.light, fill="gray")

        # Update door color: green for "open", red for "closed"
        if data.get("door", "").lower() == "open":
            self.canvas.itemconfig(self.door, fill="green")
        else:
            self.canvas.itemconfig(self.door, fill="red")

        # Update window color: blue for "open", black for "closed"
        if data.get("window", "").lower() == "open":
            self.canvas.itemconfig(self.window, fill="blue")
        else:
            self.canvas.itemconfig(self.window, fill="black")

    def handle_client(self, client_socket, client_address):
        print(f"[INFO] Connection established with {client_address}")
        while True:
            try:
                # Receive data from the client
                client_message = client_socket.recv(1024).decode()
                if not client_message:
                    break  # No data, exit the loop

                print(f"[DEBUG] Received from {client_address}: {client_message}")
                
                # If the message looks like JSON, parse and process it
                if client_message.strip().startswith("{") and client_message.strip().endswith("}"):
                    update_data = json.loads(client_message)
                    
                    # Update the JSON file with new house state
                    with open("House.json", "w") as json_file:
                        json.dump(update_data, json_file, indent=4)
                    print(f"[INFO] Updated House.json with: {update_data}")

                    # Tkinter should be updated from the main thread
                    self.root.after(0, self.update_graphics, update_data)

                # Send an acknowledgment back to the client
                client_socket.sendall(b"Update received and applied!")
            except Exception as e:
                print(f"[ERROR] Error handling client {client_address}: {e}")
                break

        client_socket.close()
        print(f"[INFO] Connection with {client_address} closed.")

    def accept_clients(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(
                target=self.handle_client, args=(client_socket, client_address)
            )
            client_thread.start()

    def start(self):
        # Start the client-accepting thread as a daemon
        threading.Thread(target=self.accept_clients, daemon=True).start()
        print("[INFO] Server thread started. Launching GUI.")
        self.root.mainloop()

if __name__ == "__main__":
    server = HouseServer()
    server.start()
