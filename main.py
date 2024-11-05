import tkinter as tk  
from server.connection import Server  
from control_interface.server_app import ServerApp  

if __name__ == "__main__":
    root = tk.Tk()  
    app = ServerApp(root, None)  # Instantiate the ServerApp with the main window and no specific parameter
    server = Server(app)  # Create an instance of the Server, passing the app instance
    app.server = server  # Assign the server instance to the app for later use
    root.mainloop()  # Start the Tkinter event loop, displaying the GUI
