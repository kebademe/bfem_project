from tkinter import ttk, messagebox

from anonymat import Anonymat


class AnonymatPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Frame pour le titre et les boutons
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=20, pady=20)

        # Titre
        title = ttk.Label(
            header_frame,
            text="Gestion des anonymes",
            font=("Helvetica", 20, "bold")
        )
        title.pack(side="left")

        # Frame pour les boutons
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.pack(side="right")

        # Boutons d'action avec style e
        ttk.Button(
            buttons_frame,
            text="➕ Générer",
            style=".TButton",
            command=self.generer_anonymat
        ).pack(side="left", padx=5)


        # Table des candidats avec style e
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Candidat", "Numéro Table","Numéro Anonyme"),
            show="headings",
            style=".Treeview"
        )

        # Configuration des colonnes
        columns = {
            "ID": 10,
            "Candidat": 100,
            "Numéro Table": 70,
            "Numéro Anonyme": 70
        }

        for col, width in columns.items():
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=width, anchor="w")

        # Ajout de la barre de défilement
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Placement de la table et de la barre de défilement
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Remplir la table
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for anonymat in Anonymat.get_all():
            self.tree.insert("", "end", values=(
                anonymat[0],
                anonymat[3]+" "+anonymat[4],
                anonymat[2],
                anonymat[5]

            ))

    def generer_anonymat(self):
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir générer des numéros anonymes"):
           Anonymat.generate_and_save_for_all()
           self.refresh_table()
           messagebox.showinfo("Succès", "Numéro anonyme généré")
