import socket
import threading

class Server:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.client_socket = None
        self.server_socket = None
        # Está sección del código es para que para que los comand se envien en el mismo puerto 
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor escuchando en el puerto {self.port}")

        while True:
            self.client_socket, addr = self.server_socket.accept()
            print(f"Conexión aceptada de {addr}")

    def send_command(self, command):
        if self.client_socket:
            try:
                self.client_socket.send(command.encode())
            except Exception as e:
                print(f"Error enviando comando: {e}")

