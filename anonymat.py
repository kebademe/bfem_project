import random
import sqlite3

from database import Database

class Anonymat:
    """ Modèle représentant le numéro d'anonymat d'un candidat """

    def __init__(self, candidat_id, anonymat_principal=None):
        self.candidat_id = candidat_id
        self.anonymat_principal = anonymat_principal or self.generate_anonymat()

    def generate_anonymat(self):
        """ Génère un numéro d'anonymat unique """
        return f"A-{random.randint(1000, 9999)}"

    def save(self):
        """ Enregistre le numéro d'anonymat dans la base """
        db = Database()
        try:
            db.cursor.execute("""
                INSERT INTO Anonymat (candidat_id, anonymat_principal)
                VALUES (?, ?)
            """, (self.candidat_id, self.anonymat_principal))
            db.conn.commit()
            print(f"Anonymat {self.anonymat_principal} généré pour le candidat {self.candidat_id} !")
        except sqlite3.IntegrityError:
            print("Erreur : L'anonymat existe déjà pour ce candidat.")
        finally:
            db.close()

    def update(self, id):
        """ Met à jour les informations d'un anonymat basé sur l'ID """
        db = Database()
        try:
            db.cursor.execute("""
                UPDATE Anonymat
                SET candidat_id = ?, 
                    anonymat_principal = ?
                WHERE id = ?
            """, (
                self.candidat_id, self.anonymat_principal, id
            ))

            if db.cursor.rowcount == 0:  # Vérifier si aucune ligne n'a été mise à jour
                print("Erreur : Aucun anonymat trouvé avec cet ID.")
            else:
                db.conn.commit()
                print("Anonymat mis à jour avec succès !")
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour : {e}")
        finally:
            db.close()

    @staticmethod
    def get_all():
        """ Récupère tous les anonymats avec le numéro de table des candidats """
        db = Database()
        try:
            # Jointure entre les tables Anonymat et Candidat pour récupérer le numero_table
            db.cursor.execute("""
                SELECT Anonymat.id, Anonymat.candidat_id, Candidat.numero_table,  Candidat.prenom, Candidat.nom, Anonymat.anonymat_principal
                FROM Anonymat
                JOIN Candidat ON Anonymat.candidat_id = Candidat.id
            """)
            anonymats = db.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des anonymats : {e}")
            anonymats = []
        finally:
            db.close()

        return anonymats

    @staticmethod
    def delete(id_anonymat):
        """ Supprime un anonymat """
        db = Database()
        try:
            db.cursor.execute("DELETE FROM Anonymat WHERE id = ?", (id_anonymat,))
            if db.cursor.rowcount == 0:  # Vérifie si un enregistrement a été supprimé
                print("Erreur : Aucun anonymat trouvé avec cet ID.")
            else:
                db.conn.commit()
                print("Anonymat supprimé avec succès !")
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression : {e}")
        finally:
            db.close()

    @staticmethod
    def generate_and_save_for_all():
        """ Génère et enregistre un anonymat pour tous les candidats sans numéro anonyme """
        db = Database()
        try:
            # Identifie les candidats qui n'ont pas encore d'anonymat
            db.cursor.execute("""
                SELECT id FROM Candidat
                WHERE id NOT IN (SELECT candidat_id FROM Anonymat)
            """)
            candidats_sans_anonymat = db.cursor.fetchall()

            # Générer et enregistrer un anonymat pour chaque candidat
            for candidate in candidats_sans_anonymat:
                candidat_id = candidate[0]
                anonymat_principal = f"A-{random.randint(1000, 9999)}"

                db.cursor.execute("""
                    INSERT INTO Anonymat (candidat_id, anonymat_principal)
                    VALUES (?, ?)
                """, (candidat_id, anonymat_principal))

            db.conn.commit()
            print(f"Anonymat généré et enregistré pour {len(candidats_sans_anonymat)} candidats.")
        except sqlite3.Error as e:
            print(f"Erreur lors de la génération des anonymats : {e}")
        finally:
            db.close()

    @staticmethod
    def get_anonymat_by_candidat_id(candidat_id):
        """ Récupère le numéro anonyme d'un candidat spécifique via candidat_id """
        db = Database()
        try:
            # Requête pour récupérer le numéro anonyme basé sur candidat_id
            db.cursor.execute("""
                SELECT anonymat_principal
                FROM Anonymat
                WHERE candidat_id = ?
            """, (candidat_id,))
            result = db.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération de l'anonymat : {e}")
            result = None
        finally:
            db.close()

        # Retourner le numéro anonyme s'il existe, sinon None
        if result:
            return result[0]
        else:
            print(f"Aucun numéro anonyme trouvé pour le candidat avec l'ID {candidat_id}")
            return None

    @staticmethod
    def get_candidat_by_anonymat_id(anonymat_id):
        """ Récupère le numéro anonyme d'un candidat spécifique via candidat_id """
        db = Database()
        try:
            # Requête pour récupérer le numéro candidat basé sur anonyme_id
            db.cursor.execute("""
                SELECT candidat_id 
                FROM Anonymat
                WHERE anonymat_principal = ?
            """, (anonymat_id,))
            result = db.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération de l'id candidat : {e}")
            result = None
        finally:
            db.close()

        # Retourner le numéro du candidat s'il existe, sinon None
        if result:
            return result[0]
        else:
            print(f"Aucun  candidat id trouvé pour l' anonymat {anonymat_id}")
            return None
