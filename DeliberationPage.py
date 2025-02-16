from tkinter import ttk, messagebox
from deliberation import Deliberation
from database import Database


class DeliberationPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Frame pour le titre
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=20, pady=20)

        # Titre
        title = ttk.Label(
            header_frame,
            text="Délibération",
            font=("Helvetica", 20, "bold")
        )
        title.pack(side="left")

        # Contenu
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=20)

        # Tableau des candidats
        self.create_candidates_table(content_frame)

        # Bouton pour délibérer
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.pack(pady=20)

        ttk.Button(
            buttons_frame,
            text="Délibérer",
            style=".TButton",
            command=self.deliberer
        ).pack(side="left", padx=5)

        # Charger les candidats au démarrage
        self.load_candidates()

    def create_candidates_table(self, parent):
        """Créer l'interface pour afficher les candidats et leurs résultats."""
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True, pady=10)

        # Définir les styles de couleurs pour les résultats
        style = ttk.Style()
        style.map("Treeview", foreground=fixed_map("foreground"), background=fixed_map("background"))

        # Tableau des candidats
        self.candidate_table = ttk.Treeview(
            table_frame,
            columns=("numero_table", "nom", "prenom", "resultat"),
            show="headings",
            height=15
        )
        self.candidate_table.pack(fill="both", expand=True, padx=5, pady=5)

        # Définir les colonnes
        self.candidate_table.heading("numero_table", text="Numéro Table")
        self.candidate_table.heading("nom", text="Nom")
        self.candidate_table.heading("prenom", text="Prénom")
        self.candidate_table.heading("resultat", text="Résultat Délibération")

        self.candidate_table.column("numero_table", width=100, anchor="center")
        self.candidate_table.column("nom", width=150, anchor="center")
        self.candidate_table.column("prenom", width=150, anchor="center")
        self.candidate_table.column("resultat", width=200, anchor="center")

        # Ajouter les tags pour les couleurs
        self.candidate_table.tag_configure("admis", foreground="green")
        self.candidate_table.tag_configure("repechable", foreground="blue")
        self.candidate_table.tag_configure("echec", foreground="red")
        self.candidate_table.tag_configure("attente", foreground="orange")

    def load_candidates(self):
        """Charger les candidats dans le tableau."""
        # Réinitialiser le tableau
        for row in self.candidate_table.get_children():
            self.candidate_table.delete(row)

        # Connexion à la base et récupération des candidats
        db = Database()
        try:
            db.cursor.execute("""
                SELECT c.id, c.numero_table, c.nom, c.prenom, r.resultat
                FROM Candidat c
                LEFT JOIN Resultat r ON c.id = r.candidat_id
            """)
            candidats = db.cursor.fetchall()

            # Ajouter les données dans le tableau avec les tags pour les couleurs
            for candidat in candidats:
                resultat = candidat[4] if candidat[4] else "En attente de délibération"

                # Définir le tag en fonction du résultat
                if resultat == "ADMIS":
                    tag = "admis"
                elif resultat.startswith("REPÊCHABLE"):
                    tag = "repechable"
                elif resultat == "ÉCHEC":
                    tag = "echec"
                else:
                    tag = "attente"

                self.candidate_table.insert(
                    "", "end",
                    values=(
                        candidat[1],  # numéro table
                        candidat[2],  # nom
                        candidat[3],  # prénom
                        resultat  # résultat
                    ),
                    tags=(tag,)
                )
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des candidats : {e}")
        finally:
            db.close()

    def deliberer(self):
        """Effectuer la délibération pour chaque candidat."""
        db = Database()
        try:
            # Récupérer tous les candidats
            db.cursor.execute("SELECT id FROM Candidat")
            candidats = db.cursor.fetchall()

            if not candidats:
                messagebox.showinfo("Info", "Aucun candidat trouvé dans la base de données.")
                return

            # Effectuer la délibération pour chaque candidat
            for candidat in candidats:
                delib = Deliberation(candidat_id=candidat[0])  # Délibération pour un candidat
                resultat = delib.determiner_resultat()

                # Sauvegarder le résultat dans la base
                db.cursor.execute("""
                    INSERT INTO Resultat (candidat_id, resultat)
                    VALUES (?, ?)
                    ON CONFLICT(candidat_id) DO UPDATE SET resultat = excluded.resultat
                """, (candidat[0], resultat))
                db.conn.commit()

            messagebox.showinfo("Succès", "Délibération effectuée avec succès !")
            self.load_candidates()  # Recharger le tableau avec les nouveaux résultats

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la délibération : {e}")
        finally:
            db.close()


def fixed_map(option):
    """ Correction pour éviter que les paramètres ne soient ignorés dans le style Treeview. """
    return [elm for elm in ttk.Style().map("Treeview", query_opt=option) if elm[:2] != ("!disabled", "!selected")]
