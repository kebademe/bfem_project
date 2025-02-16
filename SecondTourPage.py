from tkinter import ttk, messagebox


class SecondTourPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Frame pour le titre
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=20, pady=20)

        # Titre
        title = ttk.Label(
            header_frame,
            text="Second Tour",
            font=("Helvetica", 20, "bold")
        )
        title.pack(side="left")

        # Contenu
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=20)

        # Liste des candidats du second tour
        self.tree = ttk.Treeview(
            content_frame,
            columns=("ID", "Candidat", "Moyenne", "Matières à repasser"),
            show="headings",
            style=".Treeview"
        )

        # Configuration des colonnes
        columns = {
            "ID": 50,
            "Candidat": 200,
            "Moyenne": 100,
            "Matières à repasser": 300
        }

        for col, width in columns.items():
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=width, anchor="w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(pady=10, fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Données exemple
        second_tour = [
            (1, "Dupont Jean", "9.5", "Mathématiques, Physique"),
            (2, "Martin Marie", "9.8", "Français"),
            (3, "Bernard Pierre", "9.2", "Mathématiques")
        ]

        for item in second_tour:
            self.tree.insert("", "end", values=item)

        # Boutons d'action
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(pady=20)

        ttk.Button(
            buttons_frame,
            text="Programmer Épreuves",
            style=".TButton",
            command=lambda: messagebox.showinfo("Info", "Programmation des épreuves")
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons_frame,
            text="Imprimer Convocations",
            style=".TButton",
            command=lambda: messagebox.showinfo("Info", "Impression des convocations")
        ).pack(side="left", padx=5)
