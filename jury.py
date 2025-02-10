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

