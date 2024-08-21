import tkinter as tk 
from server.connection import Server
from control_interface.server_app import ServerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root, None)
    server = Server(app)
    app.server = server
    root.mainloop()