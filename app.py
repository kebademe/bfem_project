import tkinter as tk
from tkinter import ttk

from AnonymatPage import AnonymatPage
from CandidatePage import CandidatePage
from DeliberationPage import DeliberationPage
from HomePage import HomePage
from NotesPage import NotesPage
from ParametragePage import ParametragePage
from SecondTourPage import SecondTourPage


class ExamApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestion des Examens BFEM")
        self.state('zoomed')

        # Configuration des styles
        self.configure_styles()


        self.setup_ui()

    def configure_styles(self):
        # Configuration du thème
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Couleurs
        self.primary_color = "#2962ff"  # Bleu
        self.secondary_color = "#f5f5f5"  # Gris clair
        self.accent_color = "#ff3d00"  # Orange
        self.text_color = "#212121"  # Noir

        # Style pour les boutons
        self.style.configure(
            ".TButton",
            padding=10,
            relief="flat",
            background=self.primary_color,
            foreground="white",
            font=("Helvetica", 10)
        )

        # Style pour le Treeview
        self.style.configure(
            ".Treeview",
            background="white",
            fieldbackground="white",
            foreground=self.text_color,
            rowheight=30,
            font=("Helvetica", 10)
        )

        self.style.configure(
            ".Treeview.Heading",
            background=self.secondary_color,
            foreground=self.text_color,
            relief="flat",
            font=("Helvetica", 10, "bold")
        )

        # Style pour les labels
        self.style.configure(
            ".TLabel",
            background=self.secondary_color,
            foreground=self.text_color,
            font=("Helvetica", 12)
        )

    def setup_ui(self):
        # Frame principal
        self.main_frame = ttk.Frame(self, style=".TFrame")
        self.main_frame.pack(fill="both", expand=True)

        # Frame pour le menu latéral
        self.sidebar = ttk.Frame(self.main_frame, style="Sidebar.TFrame")
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)

        # Frame pour le contenu
        self.content_frame = ttk.Frame(self.main_frame, style="Content.TFrame")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Création du menu latéral
        self.create_sidebar()

        # Container pour les différentes pages
        self.container = ttk.Frame(self.content_frame)
        self.container.pack(side="top", fill="both", expand=True)

        # Dictionnaire pour stocker les différentes pages
        self.frames = {}

        # Création des pages
        for F in (HomePage, CandidatePage,AnonymatPage, ParametragePage,
                  NotesPage, DeliberationPage, SecondTourPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Afficher la page d'accueil
        self.show_frame(HomePage)

    def create_sidebar(self):
        # Style du menu latéral
        sidebar_style = {
            "background": self.secondary_color,
            "foreground": self.text_color,
            "activebackground": self.primary_color,
            "activeforeground": "white",
            "relief": "flat",
            "font": ("Helvetica", 11),
            "width": 20,
            "anchor": "w",
            "pady": 5
        }

        # Logo ou titre
        logo_label = tk.Label(
            self.sidebar,
            text="BFEM EXAM",
            font=("Helvetica", 16, "bold"),
            background=self.secondary_color,
            foreground=self.primary_color,
            pady=20
        )
        logo_label.pack(fill="x")

        # Boutons du menu
        menus = [
            ("Accueil", HomePage),
            ("Gestion Candidats", CandidatePage),
            ("Gestion Anonymat", AnonymatPage),
            ("Gestion Notes", NotesPage),
            ("Délibération", DeliberationPage),
            ("Second Tour", SecondTourPage),
            ("Paramétrage", ParametragePage)
        ]

        for text, page in menus:
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=lambda p=page: self.show_frame(p),
                **sidebar_style
            )
            btn.pack(fill="x", padx=5, pady=2)

            # Binding pour l'effet hover
            btn.bind("<Enter>", lambda e, b=btn: b.configure(
                background=self.primary_color,
                foreground="white"
            ))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(
                background=self.secondary_color,
                foreground=self.text_color
            ))

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app = ExamApp()
    app.mainloop()