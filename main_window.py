
import tkinter as tk
from tkinter import messagebox

from candidat import Candidat
from deliberation import Deliberation


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Candidats - BFEM")
        self.root.geometry("600x400")

        # Label principal
        tk.Label(root, text="Gestion des Candidats", font=("Arial", 16, "bold")).pack(pady=10)

        # Boutons
        tk.Button(root, text="Ajouter un Candidat", command=self.ajouter_candidat, width=30).pack(pady=5)
        tk.Button(root, text="Voir les Candidats", command=self.afficher_candidats, width=30).pack(pady=5)
        tk.Button(root, text="Délibérer", command=self.deliberer, width=30).pack(pady=5)
        tk.Button(root, text="Quitter", command=root.quit, width=30, bg="red", fg="white").pack(pady=10)

    def ajouter_candidat(self):
        """ Fenêtre pour ajouter un candidat """
        new_window = tk.Toplevel(self.root)
        new_window.title("Ajouter un Candidat")
        new_window.geometry("400x400")

        tk.Label(new_window, text="Numéro Table:").pack()
        entry_numero = tk.Entry(new_window)
        entry_numero.pack()

        tk.Label(new_window, text="Prénom:").pack()
        entry_prenom = tk.Entry(new_window)
        entry_prenom.pack()

        tk.Label(new_window, text="Nom:").pack()
        entry_nom = tk.Entry(new_window)
        entry_nom.pack()

        tk.Label(new_window, text="Date Naissance (YYYY-MM-DD):").pack()
        entry_date = tk.Entry(new_window)
        entry_date.pack()

        tk.Label(new_window, text="Lieu Naissance:").pack()
        entry_lieu = tk.Entry(new_window)
        entry_lieu.pack()

        tk.Label(new_window, text="Sexe (M/F):").pack()
        entry_sexe = tk.Entry(new_window)
        entry_sexe.pack()

        tk.Label(new_window, text="Nationalité:").pack()
        entry_nationalite = tk.Entry(new_window)
        entry_nationalite.pack()

        def save_candidat():
            try:
                candidat = Candidat(
                    int(entry_numero.get()), entry_prenom.get(), entry_nom.get(),
                    entry_date.get(), entry_lieu.get(), entry_sexe.get(),
                    entry_nationalite.get(), "NON", None, "OUI"
                )
                candidat.save()
                messagebox.showinfo("Succès", "Candidat ajouté avec succès !")
                new_window.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        tk.Button(new_window, text="Enregistrer", command=save_candidat).pack(pady=10)

    def afficher_candidats(self):
        """ Affiche la liste des candidats """
        new_window = tk.Toplevel(self.root)
        new_window.title("Liste des Candidats")
        new_window.geometry("500x300")

        candidats = Candidat.get_all()
        for candidat in candidats:
            tk.Label(new_window, text=f"{candidat[1]} - {candidat[2]} {candidat[3]}").pack()

    def deliberer(self):
        """ Lance la délibération et affiche les résultats """
        new_window = tk.Toplevel(self.root)
        new_window.title("Résultats de la Délibération")
        new_window.geometry("500x300")

        candidats = Candidat.get_all()
        for candidat in candidats:
            delib = Deliberation(candidat[0])
            resultat = delib.determiner_resultat()
            tk.Label(new_window, text=f"{candidat[1]} - {candidat[2]} {candidat[3]} : {resultat}").pack()

# Exécution de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
