from tkinter import ttk, messagebox
from jury import Jury


class ParametragePage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Stockage des champs (Entrées pour dynamiquement récupérer les valeurs saisies)
        self.entries = {}

        # Frame pour le titre
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=5, pady=20)

        # Titre
        title = ttk.Label(
            header_frame,
            text="Paramétrage",
            font=("Helvetica", 20, "bold")
        )
        title.pack(side="left")

        # Frame pour le contenu
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Générer dynamiquement les champs à partir des données existantes dans la base Jury
        self.create_fields(content_frame)

        # Bouton de sauvegarde
        ttk.Button(
            content_frame,
            text="Enregistrer les paramètres",
            style=".TButton",
            command=self.save_data
        ).pack(pady=20)

    def create_fields(self, parent):
        """ Crée dynamiquement les champs d'entrée à partir des données retournées par Jury.get_all """
        jurys = Jury.get_all()
        if jurys:
            for setting, default in jurys[0]:  # La méthode get_all() retourne les tuples descriptifs
                # Frame pour chaque champ
                setting_frame = ttk.Frame(parent)
                setting_frame.pack(fill="x", pady=5)

                # Label pour le nom du champ
                ttk.Label(
                    setting_frame,
                    text=setting,
                    font=("Helvetica", 12)
                ).pack(side="left", padx=5)

                # Champ d'entrée
                entry = ttk.Entry(setting_frame, font=("Helvetica", 12))
                entry.insert(0, default)  # Valeur par défaut venant de la base
                entry.pack(side="right", padx=5)

                # Stocker l'entrée pour récupération ultérieure
                self.entries[setting] = entry
        else:
            messagebox.showinfo("Information", "Aucune donnée trouvée dans la base de données.")

    def save_data(self):
        """ Récupère les données des champs et les enregistre via la méthode save() de Jury """
        try:
            # Récupérer les valeurs saisies pour chaque champ
            region = self.entries["Région"].get()
            ief = self.entries["IEF"].get()
            localite = self.entries["Localité"].get()
            centre_examen = self.entries["Centre d'examen"].get()
            president_jury = self.entries["Président du jury"].get()
            telephone = self.entries["Téléphone"].get()

            # Créer une instance de Jury avec les données
            jury = Jury(region, ief, localite, centre_examen, president_jury, telephone)

            # Sauvegarder dans la base de données
            Jury.delete_all()  # Supprimer toutes les données existantes dans la table avant d'enregistrer les nouvelles
            jury.save()

            # Confirmation de sauvegarde
            messagebox.showinfo("Succès", "Paramètres enregistrés avec succès !")
        except KeyError as e:
            # Si une clé est introuvable, cela indique un problème dans le mapping des champs
            messagebox.showerror("Erreur", f"Clé manquante dans les entrées : {e}")
        except Exception as e:
            # Gérer toute autre exception
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'enregistrement : {e}")
