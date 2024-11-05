import socket
import threading
import time 
from control_interface.settings import CHARTREUSE, AQUAMARINE, NEON_ORANGE, COOL_GRAY

class Server:
    def __init__(self, app, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.client_socket = None
        self.server_socket = None
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.command = None 
        self.app = app
        
    # Se define el socket del server por los que se va a mandar los mensjaes 
    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor escuchando en el puerto {self.port}")

        while True:
            self.client_socket, addr = self.server_socket.accept()
            if addr:
                self.app.label_state.config(text='CONECTADO', bg=AQUAMARINE)
            print(f"Conexión aceptada de {addr}")
            threading.Thread(target=self.handle_client, args=(self.client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    if message == 'True B':
                        self.app.change_color(self.app.button_advertising, COOL_GRAY, CHARTREUSE)
                        self.app.enable_button(self.app.button_state_slot)
                        self.app.enable_button(self.app.button_advertising)
                        self.app.disable_button(self.app.button_slot)
                        self.app.change_color(self.app.button_slot, NEON_ORANGE, NEON_ORANGE)
                        self.app.change_color(self.app.button_state_slot, NEON_ORANGE, COOL_GRAY)
                    if message == 'True A':
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
                        self.app.label.config(bg=AQUAMARINE)
                        time.sleep(4)
                        self.app.enable_button(self.app.button_state_slot)
                    if message == 'PERDEDOR':
                        self.app.update_label(self.app.label, message)
                        time.sleep(4)
                        self.app.enable_button(self.app.button_state_slot)
                    if message == 'PROCESANDO...':
                        self.app.update_label(self.app.label, message)
                        self.app.disable_button(self.app.button_state_slot)
                        
                    client_socket.send(f"Comando {message} recibido en el PC".encode())

            except Exception as e:
                self.app.label_state.config(text='DESCONECTADO', bg=NEON_ORANGE)
                print(f"Error en la conexión: {e}")
                client_socket.close()
                break

    def send_command(self, command):
        if self.client_socket:
            try:
                self.client_socket.send(command.encode())
            except Exception as e:
                print(f"Error enviando comando: {e}")

