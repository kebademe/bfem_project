from tkinter import ttk


class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Frame central
        center_frame = ttk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Titre de bienvenue
        welcome_label = ttk.Label(
            center_frame,
            text="Bienvenue dans l'application\nde gestion des examens du BFEM",
            font=("Helvetica", 24),
            justify="center"
        )
        welcome_label.pack(pady=20)

        # Sous-titre
        subtitle_label = ttk.Label(
            center_frame,
            text="Sélectionnez une option dans le menu latéral pour commencer",
            font=("Helvetica", 12),
            foreground="gray"
        )
        subtitle_label.pack(pady=10)
