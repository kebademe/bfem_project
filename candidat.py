
import sqlite3
from database import Database

class Candidat:
    """ Modèle représentant un candidat """

    def __init__(self, numero_table, prenom, nom, date_naissance, lieu_naissance, sexe, nationalite, choix_epreuve_facultative, epreuve_facultative, aptitude_sportive):
        self.numero_table = numero_table
        self.prenom = prenom
        self.nom = nom
        self.date_naissance = date_naissance
        self.lieu_naissance = lieu_naissance
        self.sexe = sexe
        self.nationalite = nationalite
        self.choix_epreuve_facultative = choix_epreuve_facultative
        self.epreuve_facultative = epreuve_facultative
        self.aptitude_sportive = aptitude_sportive

    def save(self):
        """ Enregistre un candidat dans la base """
        db = Database()
        try:
            db.cursor.execute("""
                INSERT INTO Candidat (numero_table, prenom, nom, date_naissance, lieu_naissance, sexe, nationalite, choix_epreuve_facultative, epreuve_facultative, aptitude_sportive)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.numero_table, self.prenom, self.nom, self.date_naissance, self.lieu_naissance, self.sexe, self.nationalite, self.choix_epreuve_facultative, self.epreuve_facultative, self.aptitude_sportive))
            db.conn.commit()
            print("Candidat ajouté avec succès !")
        except sqlite3.IntegrityError:
            print("Erreur : Le numéro de table existe déjà.")
        finally:
            db.close()

    def update(self,id):
        """ Met à jour les informations d'un candidat existant dans la base basé sur l'ID """
        db = Database()
        try:
            # Mise à jour des informations du candidat dans la table `Candidat`
            db.cursor.execute("""
                UPDATE Candidat
                SET numero_table = ?, 
                    prenom = ?, 
                    nom = ?, 
                    date_naissance = ?, 
                    lieu_naissance = ?, 
                    sexe = ?, 
                    nationalite = ?, 
                    choix_epreuve_facultative = ?, 
                    epreuve_facultative = ?, 
                    aptitude_sportive = ?
                WHERE id = ?
            """, (
                self.numero_table, self.prenom, self.nom, self.date_naissance,
                self.lieu_naissance, self.sexe, self.nationalite, self.choix_epreuve_facultative,
                self.epreuve_facultative, self.aptitude_sportive, id
                # L'ID est utilisé ici pour identifier le candidat
            ))

            if db.cursor.rowcount == 0:  # Vérifier si aucune ligne n'a été mise à jour
                print("Erreur : Aucun candidat trouvé avec cet ID.")
            else:
                db.conn.commit()
                print("Candidat mis à jour avec succès !")
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour : {e}")
        finally:
            db.close()


    @staticmethod
    def get_all():
        """ Récupère tous les candidats """
        db = Database()
        db.cursor.execute("SELECT * FROM Candidat")
        candidats = db.cursor.fetchall()
        db.close()
        return candidats

    @staticmethod
    def delete(id_candidat):
        """ Supprime un candidat """
        db = Database()
        db.cursor.execute("DELETE FROM Candidat WHERE id = ?", (id_candidat,))
        db.conn.commit()
        db.close()
        print("Candidat supprimé avec succès !")


