import random
from database import Database

class Anonymat:
    """ Modèle représentant le numéro d'anonymat d'un candidat """

    def __init__(self, candidat_id):
        self.candidat_id = candidat_id
        self.anonymat_principal = self.generate_anonymat()

    def generate_anonymat(self):
        """ Génère un numéro d'anonymat unique """
        return f"A-{random.randint(1000, 9999)}"

    def save(self):
        """ Enregistre le numéro d'anonymat """
        db = Database()
        db.cursor.execute("""
            INSERT INTO Anonymat (candidat_id, anonymat_principal)
            VALUES (?, ?)
        """, (self.candidat_id, self.anonymat_principal))
        db.conn.commit()
        db.close()
        print(f"Anonymat {self.anonymat_principal} généré pour le candidat {self.candidat_id} !")
