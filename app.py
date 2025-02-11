import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from candidat import Candidat
from notes import Notes


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Candidats - BFEM")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2d8688")

        # Police personnalisée pour titres
        title_font = Font(family="Arial", size=20, weight="bold")

        # Titre de l'application
        tk.Label(
            root,
            text="Gestion des Candidats - BFEM",
            font=title_font,
            bg="#ffffff",
            fg="#000000"
        ).pack(pady=20)

        # Cadre pour les boutons principaux
        button_frame = tk.Frame(root, bg="#ffffff")
        button_frame.pack(pady=30, fill="x")

        # Style  pour les boutons
        style = ttk.Style()
        style.configure(
            "Menu.TButton",
            font=("Arial", 12, "bold"),
            padding=10,
            background="#e1f5fe",
            foreground="#2c3e50",
            relief="flat",
            borderwidth=1
        )
        style.map(
            "Menu.TButton",
            background=[("active", "#b3e5fc")],
            foreground=[("active", "#1b4f72")],
            relief=[("active", "raised")]
        )

        # Boutons
        ttk.Button(button_frame, text="Ajouter un Candidat", command=self.ajouter_candidat, width=30,
                   style="Menu.TButton").pack(pady=15)
        ttk.Button(button_frame, text="Voir les Candidats", command=self.afficher_candidats, width=30,
                   style="Menu.TButton").pack(pady=15)
        ttk.Button(button_frame, text="Quitter", command=self.root.quit, width=30,
                   style="Menu.TButton").pack(pady=15)

    def ajouter_candidat(self):
        """ Logique pour ajouter un candidat """
        add_window = tk.Toplevel(self.root)
        add_window.title("Ajouter un candidat")
        add_window.geometry("700x300")

        fields = [
            'Numéro de table', 'Prénom', 'Nom', 'Date de naissance', 'Lieu de naissance',
            'Sexe', 'Nationalité', 'Choix épreuve facultative', 'Epreuve facultative', 'Aptitude sportive'
        ]
        entries = {}

        # Conteneur principal (pour padding et centrage)
        form_frame = tk.Frame(add_window, padx=20, pady=20)
        form_frame.pack(expand=True, fill="both")

        # Ajout des labels et entrées alignés deux par deux
        for i, field in enumerate(fields):
            row, col = divmod(i, 2)
            label = tk.Label(form_frame, text=field, anchor="w", font=("Arial", 10))
            label.grid(row=row, column=col * 2, padx=10, pady=5, sticky="w")

            # Si le champ est "Sexe", utiliser une combobox
            if field == "Sexe":
                entry = ttk.Combobox(form_frame, values=["M", "F"], state="readonly", font=("Arial", 10))
                entry.grid(row=row, column=col * 2 + 1, padx=10, pady=5, sticky="ew")

            elif field == "Epreuve facultative":
                entry = ttk.Combobox(form_frame, values=["Couture", "Dessin","Musique"], state="readonly", font=("Arial", 10))
                entry.grid(row=row, column=col * 2 + 1, padx=10, pady=5, sticky="ew")

            elif field in ['Choix épreuve facultative', 'Aptitude sportive']:
                entry = ttk.Combobox(form_frame, values=["OUI", "NON"], state="readonly", font=("Arial", 10))
                entry.grid(row=row, column=col * 2 + 1, padx=10, pady=5, sticky="ew")


            else:
                entry = tk.Entry(form_frame, font=("Arial", 10))
                entry.grid(row=row, column=col * 2 + 1, padx=10, pady=5, sticky="ew")

            entries[field] = entry

        # Ajustement des colonnes pour un redimensionnement équilibré
        for col in range(4):
            form_frame.grid_columnconfigure(col, weight=1)

        def save_new_candidate():
                try:
                    candidat = Candidat(
                        numero_table=entries['Numéro de table'].get(),
                        prenom=entries['Prénom'].get(),
                        nom=entries['Nom'].get(),
                        date_naissance=entries['Date de naissance'].get(),
                        lieu_naissance=entries['Lieu de naissance'].get(),
                        sexe=entries['Sexe'].get(),
                        nationalite=entries['Nationalité'].get(),
                        choix_epreuve_facultative=entries['Choix épreuve facultative'].get(),
                        epreuve_facultative=entries['Epreuve facultative'].get(),
                        aptitude_sportive=entries['Aptitude sportive'].get()
                    )
                    candidat.save()
                    messagebox.showinfo("Succès", "Candidat ajouté avec succès !")
                    add_window.destroy()
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible d'ajouter le candidat : {e}")

        # Bouton de validation
        tk.Button(
            add_window,
            text="Enregistrer",
            command=save_new_candidate,
            bg="#3498db",
            fg="white",
            font=("Arial", 12),
            padx=10,
            pady=5
        ).pack(pady=10)

    def afficher_candidats(self):
        """ Affiche tous les candidats """
        candidats = Candidat.get_all()
        view_window = tk.Toplevel(self.root)
        view_window.title("Liste des Candidats")
        view_window.geometry("800x500")

        tree = ttk.Treeview(view_window, columns=('ID', 'Prénom', 'Nom', 'Numéro Table'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Prénom', text='Prénom')
        tree.heading('Nom', text='Nom')
        tree.heading('Numéro Table', text='Numéro de Table')

        for candidat in candidats:
            tree.insert('', tk.END, values=(candidat[0], candidat[2], candidat[3], candidat[1]))

        tree.pack(fill="both", expand=True)

        def voir_notes():
            """ Afficher les notes d'un candidat sélectionné """
            selected_item = tree.selection()
            if selected_item:
                candidat_id = tree.item(selected_item)['values'][0]
                self.afficher_notes(candidat_id)

        def delete_selected():
            selected_item = tree.selection()
            if selected_item:
                candidat_id = tree.item(selected_item)['values'][0]
                confirm = messagebox.askyesno("Confirmation", "Confirmez-vous la suppression ?")
                if confirm:
                    Candidat.delete(candidat_id)
                    tree.delete(selected_item)
                    messagebox.showinfo("Succès", "Candidat supprimé avec succès !")

        def add_notes():
            selected_item = tree.selection()
            if selected_item:
                candidat_id = tree.item(selected_item)['values'][0]
                self.ajouter_notes(candidat_id)

        ttk.Button(view_window, text="Voir Notes", command=voir_notes, style="Menu.TButton").pack(side="left", padx=20, pady=10)
        ttk.Button(view_window, text="Ajouter Notes", command=add_notes, style="Menu.TButton").pack(side="left",padx=20, pady=10)
        ttk.Button(view_window, text="Supprimer", command=delete_selected, style="Menu.TButton").pack(side="left", padx=20, pady=10)

    def afficher_notes(self, candidat_id):
        """ Affiche les notes d'un candidat spécifique """
        notes_window = tk.Toplevel(self.root)
        notes_window.title("Notes du Candidat")
        notes_window.geometry("700x400")

        notes = Notes.get_notes_by_candidat_id(candidat_id)
        if not notes:
            messagebox.showinfo("Info", "Aucune note trouvée pour ce candidat.")
            return

        # Tableau des notes
        # Création d'un style pour Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), anchor="center")  # Style des en-têtes
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25)  # Font des cellules

        # Ajout d'une barre de défilement
        scrollbar = ttk.Scrollbar(notes_window, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Tableau des notes
        tree = ttk.Treeview(
            notes_window,
            columns=("Matière", "Note"),
            show="headings",
            yscrollcommand=scrollbar.set,  # Liaison avec la scrollbar
            height=15  # Nombre de lignes visibles
        )
        tree.heading("Matière", text="Matière", anchor="center")
        tree.heading("Note", text="Note", anchor="center")

        # Définir les tailles et alignements des colonnes
        tree.column("Matière", anchor="w", width=400)
        tree.column("Note", anchor="center", width=100)
        tree.pack(fill="both", expand=True)

        # Associer la scrollbar au tableau
        scrollbar.config(command=tree.yview)

        # Liste des matières correspondant aux clés du dictionnaire
        fields = [
            ("Compo. Française", "compo_franc"),
            ("Dictée", "dictee"),
            ("Étude de Texte", "etude_de_texte"),
            ("Instruction Civique", "instruction_civique"),
            ("Histoire-Géo", "histoire_geographie"),
            ("Mathématiques", "mathematiques"),
            ("PC/LV2", "pc_lv2"),
            ("SVT", "svt"),
            ("Anglais Écrit", "anglais_ecrit"),
            ("Anglais Oral", "anglais_oral"),
            ("EPS", "eps"),
            ("Epreuve Facultative", "epreuve_facultative")
        ]

        # Ajouter les données dans le tableau
        for field_label, field_key in fields:
            tree.insert('', tk.END, values=(field_label, notes[field_key]))


        def delete_notes():
            confirm = messagebox.askyesno("Confirmation", "Voulez-vous supprimer toutes les notes de ce candidat ?")
            if confirm:
                Notes.delete_by_candidat_id(candidat_id)
                notes_window.destroy()
                messagebox.showinfo("Succès", "Toutes les notes ont été supprimées avec succès !")

        ttk.Button(notes_window, text="Supprimer Notes", command=delete_notes, style="Menu.TButton").pack(pady=10)

    def ajouter_notes(self, candidat_id):
        """ Ajouter ou modifier des notes pour un candidat """
        notes_window = tk.Toplevel(self.root)
        notes_window.title("Ajouter des Notes")
        notes_window.geometry("500x700")

        fields = [
            'Compo. Française', 'Dictée', 'Étude de Texte', 'Instruction Civique',
            'Histoire-Géo', 'Mathématiques', 'PC/LV2', 'SVT', 'Anglais écrit',
            'Anglais oral', 'EPS', 'Épreuve Facultative'
        ]
        entries = {}

        for field in fields:
            tk.Label(notes_window, text=field).pack()
            entry = tk.Entry(notes_window)
            entry.pack(pady=5)
            entries[field] = entry

        def save_notes():
            try:
                data =  [entries[field].get() for field in fields]
                # Extraction des valeurs
                (
                    compo_franc, dictee, etude_de_texte, instruction_civique,
                    histoire_geographie, mathematiques, pc_lv2, svt, anglais_ecrit,
                    anglais_oral, eps, epreuve_facultative
                ) = data

                # Création et enregistrement des notes du candidat
                notes = Notes(
                    candidat_id= candidat_id,  # Assurez-vous que l'ID est un entier
                    compo_franc=float(compo_franc),
                    dictee=float(dictee),
                    etude_de_texte=float(etude_de_texte),
                    instruction_civique=float(instruction_civique),
                    histoire_geographie=float(histoire_geographie),
                    mathematiques=float(mathematiques),
                    pc_lv2=float(pc_lv2),
                    svt=float(svt),
                    anglais_ecrit=float(anglais_ecrit),
                    anglais_oral=float(anglais_oral),
                    eps=float(eps),
                    epreuve_facultative=float(epreuve_facultative)
                )

                notes.save()
                messagebox.showinfo("Succès", "Notes enregistrées avec succès !")
                notes_window.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'enregistrer les notes : {e}")

        tk.Button(
            notes_window,
            text="Enregistrer",
            command=save_notes,
            bg="#2c3e50",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=10)

    def deliberer(self):
        """ Fonction non implémentée """
        messagebox.showinfo("Info", "La fonctionnalité de délibération n'est pas encore disponible.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
