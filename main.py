import tkinter as tk 
from server.connection import Server
from control_interface.server_app import ServerApp

if __name__ == "__main__":
    server = Server()
    root = tk.Tk()
    app = ServerApp(root, server)
    root.mainloop()