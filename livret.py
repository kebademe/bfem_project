from database import Database

class LivretScolaire:
    """ Modèle représentant le livret scolaire d'un candidat """

    def __init__(self, candidat_id, nombre_de_fois, moyenne_6e, moyenne_5e, moyenne_4e, moyenne_3e, moyenne_cycle):
        self.candidat_id = candidat_id
        self.nombre_de_fois = nombre_de_fois
        self.moyenne_6e = moyenne_6e
        self.moyenne_5e = moyenne_5e
        self.moyenne_4e = moyenne_4e
        self.moyenne_3e = moyenne_3e
        self.moyenne_cycle = moyenne_cycle

    def save(self):
        """ Enregistre un livret scolaire """
        db = Database()
        db.cursor.execute("""
            INSERT INTO LivretScolaire (candidat_id, nombre_de_fois, moyenne_6e, moyenne_5e, moyenne_4e, moyenne_3e, moyenne_cycle)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.candidat_id, self.nombre_de_fois, self.moyenne_6e, self.moyenne_5e, self.moyenne_4e, self.moyenne_3e,
              self.moyenne_cycle))
        db.conn.commit()
        db.close()
        print("Livret scolaire ajouté avec succès !")
