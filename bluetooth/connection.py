import socket

def send_message_to_server():
    server_port = 9999
    server_ip = "192.168.128.13"
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    
    # Envía un mensaje al servidor
    message = "Hola desde la PC"
    client.send(message.encode())
    
    # Recibe la respuesta del servidor
    response = client.recv(1024).decode()
    client.close()
    
    print(f"Respuesta del servidor: {response}")

if __name__ == "__main__":
    send_message_to_server()

