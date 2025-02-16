import tkinter as tk
from tkinter import ttk, messagebox

from anonymat import Anonymat
from notes import Notes


class NotesPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Frame pour le titre
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=20, pady=20)

        # Titre
        title = ttk.Label(
            header_frame,
            text="Gestion des Notes",
            font=("Helvetica", 20, "bold")
        )
        title.pack(side="left")

        # Boutons d'action
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.pack(side="right")

        ttk.Button(
            buttons_frame,
            text="➕ Ajout",
            style=".TButton",
            command= self.add_notes
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons_frame,
            text="✏️ Modifier",
            style=".TButton",
            command=self.modify_notes
        ).pack(side="left", padx=5)

        # ttk.Button(
        #     buttons_frame,
        #     text="🗑️ Supprimer",
        #     style=".TButton",
        #     command=self.delete_candidate
        # ).pack(side="left", padx=5)
        # Table des notes
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Candidat", "Compo Franc", "Dictée","Etude de texte","Inst Civique","HG","Maths","PC","SVT","Ang ecrit","Ang oral","EPS","Ep Facultative"),
            show="headings",
            style=".Treeview"
        )

        # Configuration des colonnes
        columns = {
            "ID":10,
            "Candidat":70,
            "Compo Franc":70,
            "Dictée":50,
            "Etude de texte":70,
            "Inst Civique":70,
            "HG":30,
            "Maths":30,
            "PC":25,
            "SVT":25,
            "Ang ecrit":70,
            "Ang oral":70,
            "EPS":30,
            "Ep Facultative":70
        }

        for col, width in columns.items():
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=width, anchor="w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Remplir la table
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for note in Notes.get_all():
            self.tree.insert("", "end", values=(
                note[0],
                Anonymat.get_anonymat_by_candidat_id(note[1]),
                note[2],
                note[3],
                note[4],
                note[5],
                note[6],
                note[7],
                note[8],
                note[9],
                note[10],
                note[11],
                note[12],
                note[13]

            ))

    def create__entry(self, window, label_text):
        frame = ttk.Frame(window)
        frame.pack(fill="x", padx=20, pady=2)

        ttk.Label(
            frame,
            text=label_text,
            font=("Helvetica", 10)
        ).pack(anchor="w")

        entry = ttk.Entry(frame, font=("Helvetica", 10))
        entry.pack(fill="x", pady=2)

        return entry

 # Fonction pour ajouter les notes d'un candidat
    def add_notes(self):
        """ Ajoute note"""
        add_window = tk.Toplevel(self)
        add_window.title("Noter un candidat")
        add_window.geometry("400x750")

        # Titre
        ttk.Label(
            add_window,
            text="Noter Le Candidat",
            font=("Helvetica", 16, "bold")
        ).pack(pady=2)

        anonymat_entry = self.create__entry(add_window, "Numéro Anonyme")
        compo_franc_entry = self.create__entry(add_window, "Compo franc")
        dictee_entry = self.create__entry(add_window, "Dictee")
        etude_de_texte_entry = self.create__entry(add_window, "Etude de texte")
        instruction_civique_entry = self.create__entry(add_window, "Instruction civique")
        histoire_geographie_entry = self.create__entry(add_window, "Histoire Geographie")
        mathematiques_entry = self.create__entry(add_window, "Mathematiques")
        pc_lv2_entry = self.create__entry(add_window, "PC lv2")
        svt_entry = self.create__entry(add_window, "SVT")
        anglais_ecrit_entry = self.create__entry(add_window, "Anglais écrit")
        anglais_oral_entry = self.create__entry(add_window, "Anglais oral")
        eps_entry = self.create__entry(add_window, "EPS")
        epreuve_facultative_entry = self.create__entry(add_window, "Epreuve Facultative")


        def save_notes():
            # Récupérer les données du formulaire
            candidat_id = Anonymat.get_candidat_by_anonymat_id(anonymat_entry.get())
            compo_franc = float(compo_franc_entry.get())
            dictee = float(dictee_entry.get())
            etude_de_texte = float(etude_de_texte_entry.get())
            instruction_civique = float(instruction_civique_entry.get())
            histoire_geographie = float(histoire_geographie_entry.get())
            mathematiques = float(mathematiques_entry.get())
            pc_lv2 = float(pc_lv2_entry.get())
            svt = float(svt_entry.get())
            anglais_ecrit = float(anglais_ecrit_entry.get())
            anglais_oral = float(anglais_oral_entry.get())
            eps = float(eps_entry.get())
            epreuve_facultative = float(epreuve_facultative_entry.get())

            # Créer une instance de Candidat
            note = Notes(
                candidat_id, compo_franc, dictee, etude_de_texte, instruction_civique, histoire_geographie,
                mathematiques, pc_lv2, svt, anglais_ecrit,anglais_oral,eps,epreuve_facultative
            )

            # Sauvegarder les notes du candidat dans la base de données
            note.save()

            self.refresh_table()
            add_window.destroy()
            messagebox.showinfo("Succès", "Notes ajoutés avec succès!")

        ttk.Button(
            add_window,
            text="Enregistrer",
            style="Modern.TButton",
            command=save_notes
        ).pack(pady=1)

    def modify_notes(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un candidat pour modifier ses notes")
            return

        values = self.tree.item(selected_item)['values']

        modify_window = tk.Toplevel(self)
        modify_window.title("Modifier Notes")
        modify_window.geometry("400x750")

        # Titre
        ttk.Label(
            modify_window,
            text="Modifier Notes",
            font=("Helvetica", 16, "bold")
        ).pack(pady=5)

        # Champs de saisie
        anonymat_entry = self.create__entry(modify_window, "Numéro Anonyme")
        anonymat_entry.insert(0,values[1])

        compo_franc_entry = self.create__entry(modify_window, "Compo franc")
        compo_franc_entry.insert(0,values[2])

        dictee_entry = self.create__entry(modify_window, "Dictee")
        dictee_entry.insert(0,values[3])

        etude_de_texte_entry = self.create__entry(modify_window, "Etude de texte")
        etude_de_texte_entry.insert(0,values[4])

        instruction_civique_entry = self.create__entry(modify_window, "Instruction civique")
        instruction_civique_entry.insert(0,values[5])

        histoire_geographie_entry = self.create__entry(modify_window, "Histoire Geographie")
        histoire_geographie_entry.insert(0,values[6])

        mathematiques_entry = self.create__entry(modify_window, "Mathematiques")
        mathematiques_entry.insert(0,values[7])

        pc_lv2_entry = self.create__entry(modify_window, "PC lv2")
        pc_lv2_entry.insert(0,values[8])

        svt_entry = self.create__entry(modify_window, "SVT")
        svt_entry.insert(0,values[9])

        anglais_ecrit_entry = self.create__entry(modify_window, "Anglais écrit")
        anglais_ecrit_entry.insert(0,values[10])

        anglais_oral_entry = self.create__entry(modify_window, "Anglais oral")
        anglais_oral_entry.insert(0,values[11])

        eps_entry = self.create__entry(modify_window, "EPS")
        eps_entry.insert(0,values[12])

        epreuve_facultative_entry = self.create__entry(modify_window, "Epreuve Facultative")
        epreuve_facultative_entry.insert(0,values[13])


        def save_modifications():
            # Récupérer les données du formulaire
            id = Anonymat.get_candidat_by_anonymat_id(values[1])
            candidat_id = id
            compo_franc = float(compo_franc_entry.get())
            dictee = float(dictee_entry.get())
            etude_de_texte = float(etude_de_texte_entry.get())
            instruction_civique = float(instruction_civique_entry.get())
            histoire_geographie = float(histoire_geographie_entry.get())
            mathematiques = float(mathematiques_entry.get())
            pc_lv2 = float(pc_lv2_entry.get())
            svt = float(svt_entry.get())
            anglais_ecrit = float(anglais_ecrit_entry.get())
            anglais_oral = float(anglais_oral_entry.get())
            eps = float(eps_entry.get())
            epreuve_facultative = float(epreuve_facultative_entry.get())

            # Créer une instance de Candidat
            note = Notes(
                candidat_id, compo_franc, dictee, etude_de_texte, instruction_civique, histoire_geographie,
                mathematiques, pc_lv2, svt, anglais_ecrit, anglais_oral, eps, epreuve_facultative
            )

            # Sauvegarder les modificatins du candidat dans la base de données
            note.update(id)

            self.refresh_table()
            modify_window.destroy()
            messagebox.showinfo("Succès", "Candidat modifié avec succès!")

        ttk.Button(
            modify_window,
            text="Enregistrer les modifications",
            style=".TButton",
            command=save_modifications
        ).pack(pady=5)
