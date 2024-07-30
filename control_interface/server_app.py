import tkinter as tk 

class ServerApp:
    def __init__(self, master, server):
        self.master = master 
        self.master.title("Control de interfaz")
        self.master.geometry("300x200")

        self.server = server 

        tk.Button(self.master, text="Suma", command=self.send_add_command).pack(pady=10)
        tk.Button(self.master, text="Division", command=self.send_div_command).pack(pady=10)

    def send_add_command(self):
        self.server.send_command("add")
    
    def send_div_command(self):
        self.server.send_command("divide")
    
