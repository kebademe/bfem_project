import tkinter as tk
from tkinter import ttk, messagebox

from candidat import Candidat


class CandidatePage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Frame pour le titre et les boutons
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=20, pady=20)

        # Titre
        title = ttk.Label(
            header_frame,
            text="Gestion des Candidats",
            font=("Helvetica", 20, "bold")
        )
        title.pack(side="left")

        # Frame pour les boutons
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.pack(side="right")

        # Boutons d'action avec style e
        ttk.Button(
            buttons_frame,
            text="➕ Ajouter",
            style=".TButton",
            command=self.add_candidat
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons_frame,
            text="✏️ Modifier",
            style=".TButton",
            command=self.modify_candidate
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons_frame,
            text="🗑️ Supprimer",
            style=".TButton",
            command=self.delete_candidate
        ).pack(side="left", padx=5)

        # Table des candidats avec style e
        self.tree = ttk.Treeview(
            self,
            columns=("ID","N° Table", "Prénom", "Nom", "Date Naissance", "Lieu Naissance",
                     "Sexe", "Nationalité",  "Choix Ép Facultative", "Épreuve Facultative", "Aptitude Sportive"),
            show="headings",
            style=".Treeview"
        )

        # Configuration des colonnes
        columns = {
            "ID": 50,
            "N° Table": 70,
            "Nom": 90,
            "Prénom": 150,
            "Date Naissance": 150,
            "Lieu Naissance": 150,
            "Sexe": 50,
            "Nationalité": 150,
            "Choix Ép Facultative": 150,
            "Épreuve Facultative": 150,
            "Aptitude Sportive": 150
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

        for candidat in Candidat.get_all():
            self.tree.insert("", "end", values=(
                candidat[0],
                candidat[1],
                candidat[2],
                candidat[3],
                candidat[4],
                candidat[5],
                candidat[6],
                candidat[7],
                candidat[8],
                candidat[9],
               candidat[10]

            ))

    def create_combo_box(self, window, label_text, values):
        frame = ttk.Frame(window)
        frame.pack(fill="x", padx=20, pady=5)

        ttk.Label(
            frame,
            text=label_text,
            font=("Helvetica", 10)
        ).pack(anchor="w")

        combo_box = ttk.Combobox(frame, values=values, font=("Helvetica", 10), state="readonly")
        combo_box.pack(fill="x", pady=2)

        return combo_box

    def create__entry(self, window, label_text):
        frame = ttk.Frame(window)
        frame.pack(fill="x", padx=20, pady=5)

        ttk.Label(
            frame,
            text=label_text,
            font=("Helvetica", 10)
        ).pack(anchor="w")

        entry = ttk.Entry(frame, font=("Helvetica", 10))
        entry.pack(fill="x", pady=2)

        return entry

    # Fonction pour ajouter un candidat
    def add_candidat(self):
        """ Ajoute un nouveau candidat """
        add_window = tk.Toplevel(self)
        add_window.title("Ajouter un candidat")
        add_window.geometry("400x700")

        # Titre
        ttk.Label(
            add_window,
            text="Nouveau Candidat",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        numero_table_entry = self.create__entry(add_window, "Numero Table")
        prenom_entry = self.create__entry(add_window, "Prénom")
        nom_entry = self.create__entry(add_window, "Nom")
        nationalite_entry = self.create__entry(add_window, "Nationalité")
        date_naissance_entry = self.create__entry(add_window, "Date de naissance (YYYY-MM-DD)")
        lieu_naissance_entry = self.create__entry(add_window, "Lieu de naissance")
        sexe_combobox = self.create_combo_box(add_window, "Sexe", ["M", "F"])
        choix_epreuve_facultative_combobox = self.create_combo_box(add_window, "Choix épreuve facultative",["OUI","NON"])
        epreuve_facultative_combobox =self.create_combo_box(add_window, " Epreuve facultative",["Couture","Dessin","Musique"])
        aptitude_sportive_combobox = self.create_combo_box(add_window, "Aptitude sportive",["OUI","NON"])

        def save_candidat():
            # Récupérer les données du formulaire
            numero_table = int(numero_table_entry.get())
            prenom = prenom_entry.get()
            nom = nom_entry.get()
            date_naissance = date_naissance_entry.get()
            lieu_naissance = lieu_naissance_entry.get()
            sexe = sexe_combobox.get()  # "M" ou "F"
            nationalite = nationalite_entry.get()
            choix_epreuve_facultative = choix_epreuve_facultative_combobox.get()  # "OUI" ou "NON"
            epreuve_facultative = epreuve_facultative_combobox.get()  # "Couture", "Dessin", ou "Musique"
            aptitude_sportive = aptitude_sportive_combobox.get()  # "OUI" ou "NON"

            # Créer une instance de Candidat
            candidat = Candidat(
                numero_table, prenom, nom, date_naissance, lieu_naissance, sexe,
                nationalite, choix_epreuve_facultative, epreuve_facultative, aptitude_sportive
            )

            # Sauvegarder le candidat dans la base de données
            candidat.save()

            self.refresh_table()
            add_window.destroy()
            messagebox.showinfo("Succès", "Candidat ajouté avec succès!")

        ttk.Button(
            add_window,
            text="Enregistrer",
            style="Modern.TButton",
            command=save_candidat
        ).pack(pady=20)

    def modify_candidate(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un candidat à modifier")
            return

        values = self.tree.item(selected_item)['values']
        id = values[0]

        modify_window = tk.Toplevel(self)
        modify_window.title("Modifier un candidat")
        modify_window.geometry("400x700")

        # Titre
        ttk.Label(
            modify_window,
            text="Modifier Candidat",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        # Champs de saisie
        numero_table_entry = self.create__entry(modify_window, "Numero Table")
        numero_table_entry.insert(0,values[1])

        prenom_entry = self.create__entry(modify_window, "Prénom")
        prenom_entry.insert(0,values[2])

        nom_entry = self.create__entry(modify_window, "Nom")
        nom_entry.insert(0,values[3])

        date_naissance_entry = self.create__entry(modify_window, "Date de naissance (YYYY-MM-DD)")
        date_naissance_entry.insert(0,values[4])

        lieu_naissance_entry = self.create__entry(modify_window, "Lieu de naissance")
        lieu_naissance_entry.insert(0,values[5])

        sexe_combobox = self.create_combo_box(modify_window, "Sexe", ["M", "F"])
        sexe_combobox.set(values[6])

        nationalite_entry = self.create__entry(modify_window, "Nationalité")
        nationalite_entry.insert(0, values[7])

        choix_epreuve_facultative_combobox = self.create_combo_box(modify_window, "Choix épreuve facultative",["OUI", "NON"])
        choix_epreuve_facultative_combobox.set(values[8])

        epreuve_facultative_combobox = self.create_combo_box(modify_window, " Epreuve facultative",["Couture", "Dessin", "Musique"])
        epreuve_facultative_combobox.set(values[9])

        aptitude_sportive_combobox = self.create_combo_box(modify_window, "Aptitude sportive", ["OUI", "NON"])
        aptitude_sportive_combobox.set(values[10])



        def save_modifications():
            # Récupérer les données du formulaire
            numero_table = int(numero_table_entry.get())
            prenom = prenom_entry.get()
            nom = nom_entry.get()
            date_naissance = date_naissance_entry.get()
            lieu_naissance = lieu_naissance_entry.get()
            sexe = sexe_combobox.get()  # "M" ou "F"
            nationalite = nationalite_entry.get()
            choix_epreuve_facultative = choix_epreuve_facultative_combobox.get()  # "OUI" ou "NON"
            epreuve_facultative = epreuve_facultative_combobox.get()  # "Couture", "Dessin", ou "Musique"
            aptitude_sportive = aptitude_sportive_combobox.get()  # "OUI" ou "NON"

            # Créer une instance de Candidat
            candidat = Candidat(
                numero_table, prenom, nom, date_naissance, lieu_naissance, sexe,
                nationalite, choix_epreuve_facultative, epreuve_facultative, aptitude_sportive
            )

            # Sauvegarder les modificatins du candidat dans la base de données
            candidat.update(id)

            self.refresh_table()
            modify_window.destroy()
            messagebox.showinfo("Succès", "Candidat modifié avec succès!")

        ttk.Button(
            modify_window,
            text="Enregistrer les modifications",
            style=".TButton",
            command=save_modifications
        ).pack(pady=10)


    def delete_candidate(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un candidat à supprimer")
            return

        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce candidat?"):
            values = self.tree.item(selected_item)['values']
            Candidat.delete(values[0])
            self.refresh_table()
            messagebox.showinfo("Succès", "Candidat supprimé avec succès!")
