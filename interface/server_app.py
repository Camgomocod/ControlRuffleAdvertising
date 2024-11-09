import tkinter as tk
from tkinter import PhotoImage
from interface.settings import AQUAMARINE, COOL_GRAY, NEON_ORANGE, CHARTREUSE, BLACK

class ServerApp:
    """
    ServerApp is the main interface for controlling server commands. It includes
    buttons to send specific commands to the server, change application states, 
    and provides feedback on the current server state.
    """

    def __init__(self, master, server):
        """
        Initializes the ServerApp with main window settings, server instance, and UI components.

        Args:
            master (tk.Tk): The main tkinter window instance.
            server: An instance representing the server connection.
        """
        # Initialize the main application window and settings
        self.master = master
        self.master.title("BAYSI")
        self.master.geometry("350x250")
        self.master.configure(bg=CHARTREUSE)
        self.master.resizable(False, False)

        # Set the window icon
        self.icon_image = PhotoImage(file="interface/assets/icon_plant.png")
        self.master.iconphoto(False, self.icon_image)

        self.server = server

        # Create a frame container with custom padding and background color
        self.container = tk.Frame(
            self.master,
            padx=10,
            pady=10,
            bg=AQUAMARINE,
            highlightbackground=CHARTREUSE,
            highlightthickness=10,
        )
        self.container.grid(row=0, column=0, sticky="nsew")

        # Define buttons for controlling different server commands
        self.button_state_slot = tk.Button(
            self.container,
            text="Botón",
            command=self.send_button_command,
            bg=COOL_GRAY,
            bd=4,
            relief="raised",
            state=tk.DISABLED,  # Disabled by default
        )
        self.button_slot = tk.Button(
            self.container,
            text="Sorteo",
            command=self.send_add_command,
            bg=COOL_GRAY,
            bd=4,
            relief="raised",
            state=tk.DISABLED,
        )
        self.button_advertising = tk.Button(
            self.container,
            text="Publicidad",
            command=self.send_divide_command,
            bg=CHARTREUSE,
            bd=4,
            relief="raised",
            state=tk.DISABLED
        )
        self.button_exit = tk.Button(
            self.master,
            text="SALIR",
            command=self.send_exit_command,
            bg=NEON_ORANGE,
            bd=4,
            relief="raised",
        )

        # Label to display current state of the server commands
        self.label = tk.Label(
            self.container, text="ESTADO", bd=2, relief="solid", bg=COOL_GRAY
        )
        self.label_state = tk.Label(
            self.master, text="  ESPERANDO  ", bd=2, relief="solid", bg=COOL_GRAY
        )

        # Arrange buttons and labels within the frame
        self.button_slot.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.button_advertising.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.button_state_slot.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.button_exit.grid(row=2, columnspan=2, padx=40, pady=10, sticky="nsew")
        self.label_state.grid(row=1, padx=10)
        self.label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Configure grid rows and columns within the frame for resizing
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        # Configure main window grid for layout management
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Add hover effects to buttons
        self.configure_hover(self.button_slot, NEON_ORANGE, COOL_GRAY)
        self.configure_hover(self.button_exit, COOL_GRAY, NEON_ORANGE)
        self.configure_hover(self.button_advertising, COOL_GRAY, CHARTREUSE)

        # Initialize a state variable for toggling
        self.state = False

    def configure_hover(self, button, color1, color2):
        """
        Configure hover effect on a button to change its background color.

        Args:
            button (tk.Button): Button to which the hover effect is applied.
            color1 (str): Background color when hovered.
            color2 (str): Default background color.
        """
        button.bind("<Enter>", lambda e: button.config(bg=color1))
        button.bind("<Leave>", lambda e: button.config(bg=color2))

    def disable_hover(self, button):
        """
        Disable hover effect for a button.

        Args:
            button (tk.Button): Button on which to disable the hover effect.
        """
        button.unbind("<Enter>")
        button.unbind("<Leave>")

    def close_window(self):
        """
        Placeholder function to handle window closing, if needed.
        """
        pass

    def send_button_command(self):
        """
        Send "button" command to the server and update the label's state.
        """
        self.server.send_command("button")
        self.update_label(self.label, "ESTADO")
        self.label.config(bg=COOL_GRAY)

    def send_add_command(self):
        """
        Send "sorteo" command to the server.
        """
        self.server.send_command("sorteo")

    def send_divide_command(self):
        """
        Send "publicidad" command to the server.
        """
        self.server.send_command("publicidad")

    def send_exit_command(self):
        """
        Send "salir" command to the server and reset UI elements.
        """
        self.server.send_command("salir")
        self.label_state.config(text="  ESPERANDO  ", bg=COOL_GRAY, fg=BLACK)
        self.label.config(text=" ESTADO  ", bg=COOL_GRAY)
        self.disable_button(self.button_advertising)
        self.disable_button(self.button_slot)
        self.disable_button(self.button_state_slot)
        self.change_color(self.button_advertising, COOL_GRAY, CHARTREUSE)
        self.change_color(self.button_slot, NEON_ORANGE, COOL_GRAY)

    def enable_button(self, button):
        """
        Enable a button to allow interaction.

        Args:
            button (tk.Button): Button to enable.
        """
        button.config(state=tk.NORMAL)

    def disable_button(self, button):
        """
        Disable a button to prevent interaction.

        Args:
            button (tk.Button): Button to disable.
        """
        button.config(state=tk.DISABLED)

    def change_color(self, button, hover_color, normal_color):
        """
        Set the button color and reconfigure the hover effect.

        Args:
            button (tk.Button): Button to apply color changes.
            hover_color (str): Color when hovered.
            normal_color (str): Default color.
        """
        button.config(bg=normal_color)
        self.configure_hover(button, hover_color, normal_color)

    def update_label(self, label, text):
        """
        Update the text content of a label.

        Args:
            label (tk.Label): Label to update.
            text (str): New text content.
        """
        label.config(text=text)
