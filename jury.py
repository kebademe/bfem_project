import sqlite3

from database import Database

class Jury:
    """ Modèle représentant un jury d'examen """

    def __init__(self, region, ief, localite, centre_examen, president_jury, telephone):
        self.region = region
        self.ief = ief
        self.localite = localite
        self.centre_examen = centre_examen
        self.president_jury = president_jury
        self.telephone = telephone

    def save(self):
        """ Enregistre un jury """
        db = Database()
        db.cursor.execute("""
            INSERT INTO Jury (region, ief, localite, centre_examen, president_jury, telephone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.region, self.ief, self.localite, self.centre_examen, self.president_jury, self.telephone))
        db.conn.commit()
        db.close()
        print("Jury ajouté avec succès !")

    @staticmethod
    def get_all():
        """ Récupère tous les jurys enregistrés sous forme de tuples descriptifs ou des champs vides si aucune donnée """
        db = Database()
        try:
            db.cursor.execute("""
                    SELECT id, region, ief, localite, centre_examen, president_jury, telephone
                    FROM Jury
                """)
            jurys = db.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des jurys : {e}")
            jurys = []
        finally:
            db.close()

        # Si la base est vide, retourner une structure vide
        if not jurys:
            return [
                [
                    ("Région", ""),
                    ("IEF", ""),
                    ("Localité", ""),
                    ("Centre d'examen", ""),
                    ("Président du jury", ""),
                    ("Téléphone", "")
                ]
            ]

        # Structurer le retour sous forme de liste de tuples descriptifs
        result = []
        for jury in jurys:
            result.append([
                ("Région", jury[1]),
                ("IEF", jury[2]),
                ("Localité", jury[3]),
                ("Centre d'examen", jury[4]),
                ("Président du jury", jury[5]),
                ("Téléphone", jury[6])
            ])
        return result

    def update(self, jury_id):
        """ Met à jour les informations d'un jury existant """
        db = Database()
        try:
            db.cursor.execute("""
                    UPDATE Jury
                    SET region = ?, ief = ?, localite = ?, centre_examen = ?, 
                        president_jury = ?, telephone = ?
                    WHERE id = ?
                """, (self.region, self.ief, self.localite, self.centre_examen,
                      self.president_jury, self.telephone, jury_id))
            db.conn.commit()
            print("Jury mis à jour avec succès !")
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour du jury : {e}")
        finally:
            db.close()


    @staticmethod
    def delete_all():
        """ Supprime tous les jurys enregistrés dans la table """
        db = Database()
        try:
            db.cursor.execute("DELETE FROM Jury")
            db.conn.commit()
            print("Tous les jurys ont été supprimés avec succès.")
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression des jurys : {e}")
        finally:
            db.close()
