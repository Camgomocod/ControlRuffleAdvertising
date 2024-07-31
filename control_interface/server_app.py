import tkinter as tk
from server.connection import Server

class ServerApp:
    def __init__(self, master, server):
        self.master = master
        self.master.title("Control de Interfaz")
        self.master.geometry("300x200")

        self.server = server

        tk.Button(self.master, text="Mostrar Suma", command=self.send_add_command).pack(pady=10)
        tk.Button(self.master, text="Mostrar División", command=self.send_divide_command).pack(pady=10)

    def send_add_command(self):
        self.server.send_command("add")

    def send_divide_command(self):
        self.server.send_command("divide")
