import tkinter as tk
from tkinter import PhotoImage
from interface.assets.settings import AQUAMARINE, COOL_GRAY, NEON_ORANGE, CHARTREUSE

class ServerApp:
    def __init__(self, master, server):
        self.master = master
        self.master.title("BAYSI")
        self.master.geometry("350x250")
        self.master.configure(bg=CHARTREUSE)
        self.master.resizable(False, False)

        # Cambiar el icono de la pestaña
        self.icon_image = PhotoImage(file="control_interface/assets/icon_plant.png")
        self.master.iconphoto(False, self.icon_image)

        self.server = server

        # Crear un contenedor frame
        self.container = tk.Frame(
            self.master,
            padx=10,
            pady=10,
            bg=AQUAMARINE,
            highlightbackground=CHARTREUSE,
            highlightthickness=10,
        )
        self.container.grid(row=0, column=0, sticky="nsew")

        self.button_state_slot = tk.Button(
            self.container,
            text="Botón",
            command=self.send_button_command,
            bg=COOL_GRAY,
            bd=4,
            relief="raised",
            state=tk.DISABLED,
        )

        self.button_slot = tk.Button(
            self.container,
            text="Sorteo",
            command=self.send_add_command,
            bg=COOL_GRAY,
            bd=4,
            relief="raised",
            state=tk.NORMAL,
        )
        self.button_advertising = tk.Button(
            self.container,
            text="Publicidad",
            command=self.send_divide_command,
            bg=CHARTREUSE,
            bd=4,
            relief="raised",
        )
        self.button_exit = tk.Button(
            self.master,
            text="SALIR",
            command=self.send_exit_command,
            bg=NEON_ORANGE,
            bd=4,
            relief="raised",
        )
        self.label = tk.Label(
            self.container, text="ESTADO", bd=2, relief="solid", bg=COOL_GRAY
        )
        self.label_state = tk.Label(
            self.master, text="ESPERANDO", bd=2, relief="solid", bg=COOL_GRAY
        )

        # Configurar los botonesL:
        self.button_slot.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.button_advertising.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.button_state_slot.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.button_exit.grid(row=2, columnspan=2, padx=40, pady=10, sticky="nsew")

        self.label_state.grid(row=1, padx=10)
        self.label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Configurar las filas y las columnas
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        # Configrar la fila y columna del contenedor
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # efecto hover sobre los botone
        self.configure_hover(self.button_slot, NEON_ORANGE, COOL_GRAY)
        self.configure_hover(self.button_exit, COOL_GRAY, NEON_ORANGE)
        self.configure_hover(self.button_advertising, COOL_GRAY, CHARTREUSE)

        # Cambiar de estado
        self.state = False

    def configure_hover(self, button, color1, color2):
        button.bind("<Enter>", lambda e: button.config(bg=color1))
        button.bind("<Leave>", lambda e: button.config(bg=color2))

    def disable_hover(self, button):
        button.unbind("<Enter>")
        button.unbind("<Leave>")

    def close_window(self):
        pass

    def send_button_command(self):
        self.server.send_command("button")
        self.update_label(self.label, "ESTADO")
        self.label.config(bg=COOL_GRAY)

    def send_add_command(self):
        self.server.send_command("sorteo")

    def send_divide_command(self):
        self.server.send_command("publicidad")

    def send_exit_command(self):
        self.server.send_command("salir")
        self.label_state.config(text="ESPERANDO", bg=COOL_GRAY)
        self.enable_button(self.button_advertising)
        self.enable_button(self.button_slot)
        self.change_color(self.button_advertising, COOL_GRAY, CHARTREUSE)
        self.change_color(self.button_slot, NEON_ORANGE, COOL_GRAY)

    def enable_button(self, button):
        button.config(state=tk.NORMAL)

    def disable_button(self, button):
        button.config(state=tk.DISABLED)

    def change_color(self, button, hover_color, normal_color):
        button.config(bg=normal_color)  # Cambiar el color del botón inmediatamente
        self.configure_hover(button, hover_color, normal_color)

    def update_label(self, label, text):
        label.config(text=text)
