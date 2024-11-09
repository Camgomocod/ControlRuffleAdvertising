import socket
import threading
import time
from control_interface.settings import CHARTREUSE, AQUAMARINE, NEON_ORANGE, COOL_GRAY, BLACK

class Server:
    def __init__(self, app, host='0.0.0.0', port=9999):
        """
        Initializes the server with host and port settings, along with a reference to the
        application interface. Sets up the server socket and starts a thread to listen
        for incoming connections.

        Args:
            app: The application interface object that interacts with this server.
            host (str): The host address for the server. Defaults to '0.0.0.0'.
            port (int): The port on which the server listens for connections. Defaults to 9999.
        """
        self.host = host  # The host address for the server (default is all interfaces)
        self.port = port  # The port on which the server listens for connections
        self.client_socket = None  # Placeholder for the client socket
        self.server_socket = None  # Placeholder for the server socket
        self.server_thread = threading.Thread(target=self.start_server)  # Thread to run the server
        self.server_thread.daemon = True  # Set the thread as a daemon
        self.server_thread.start()  # Start the server thread
        self.command = None  # Placeholder for commands
        self.app = app  # Reference to the application using this server

    def start_server(self):
        """
        Sets up and starts the server socket, binding it to the specified host and port.
        Listens for incoming client connections and starts a new thread to handle each
        connected client.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
        self.server_socket.bind((self.host, self.port))  # Bind the socket to the host and port
        self.server_socket.listen(5)  # Listen for incoming connections with a backlog of 5
        print(f"Servidor escuchando en el puerto {self.port}")  # Print server listening message

        while True:
            # Accept incoming client connections
            self.client_socket, addr = self.server_socket.accept()  # Accept a connection
            if addr:
                # Update the application label to show connection status
                self.app.label_state.config(text='>  CONECTADO  <', bg=AQUAMARINE, fg=COOL_GRAY)

            self.app.enable_button(self.app.button_advertising)
            self.app.enable_button(self.app.button_slot)
            print(f"Conexión aceptada de {addr}")  # Print the address of the connected client
            threading.Thread(target=self.handle_client, args=(self.client_socket,)).start()  # Handle client in a new thread

    def handle_client(self, client_socket):
        """
        Receives and processes messages from the client. Based on the received command, it updates
        the application's state by modifying the UI and enabling/disabling buttons accordingly.

        Args:
            client_socket: The socket object for the connected client.
        """
        while True:
            try:
                # Receive and handle messages from the client
                message = client_socket.recv(1024).decode()  # Receive message from client
                if message:
                    
                    # Update the application state based on the received message
                    if message == 'True B':
                        # change advertising to slot 
                        self.app.change_color(self.app.button_advertising, COOL_GRAY, CHARTREUSE)
                        self.app.enable_button(self.app.button_state_slot)
                        self.app.enable_button(self.app.button_advertising)
                        self.app.disable_button(self.app.button_slot)
                        self.app.change_color(self.app.button_slot, NEON_ORANGE, NEON_ORANGE)
                        self.app.change_color(self.app.button_state_slot, NEON_ORANGE, COOL_GRAY)
                    if message == 'True A':
                        # change slot to advertising
                        self.app.change_color(self.app.button_slot, NEON_ORANGE, COOL_GRAY)
                        self.app.enable_button(self.app.button_slot)
                        self.app.disable_button(self.app.button_advertising)
                        self.app.disable_button(self.app.button_state_slot)
                        self.app.disable_hover(self.app.button_state_slot)
                        self.app.change_color(self.app.button_advertising, NEON_ORANGE, NEON_ORANGE)
                        self.app.update_label(self.app.label, 'ESTADO')
                        self.app.label.config(bg=COOL_GRAY)
                    if message == 'GANADOR':
                        self.app.update_label(self.app.label, message)
                        self.app.label.config(bg=CHARTREUSE)
                        time.sleep(4)  # Wait for 4 seconds before enabling the button again
                        self.app.enable_button(self.app.button_state_slot)
                    if message == 'PERDEDOR':
                        self.app.update_label(self.app.label, message)
                        time.sleep(4)  # Wait for 4 seconds before enabling the button again
                        self.app.enable_button(self.app.button_state_slot)
                    if message == 'PROCESANDO...':
                        self.app.update_label(self.app.label, message)
                        self.app.disable_button(self.app.button_state_slot)

                    # Acknowledge the received command
                    client_socket.send(f"Comando {message} recibido en el PC".encode())

            except Exception as e:
                
                # Handle disconnection and update the application state
                self.app.label_state.config(text='  DESCONECTADO  ', bg=NEON_ORANGE, fg=BLACK)
                self.app.disable_button(self.app.button_slot)
                self.app.disable_button(self.app.button_advertising)
                print(f"Error en la conexión: {e}")  # Print the error
                client_socket.close()  # Close the client socket
                break  # Exit the loop

    def send_command(self, command):
        """
        Sends a command to the connected client.

        Args:
            command (str): The command message to send to the client.
        """
        if self.client_socket:
            try:
                self.client_socket.send(command.encode())  # Send the command as bytes
            except Exception as e:
                print(f"Error enviando comando: {e}")  # Print any error during sending
