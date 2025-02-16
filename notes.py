import sqlite3

from database import Database

class Notes:
    """ Modèle représentant les notes d'un candidat """

    def __init__(self, candidat_id, compo_franc, dictee, etude_de_texte, instruction_civique, histoire_geographie,
                 mathematiques, pc_lv2, svt, anglais_ecrit, anglais_oral, eps, epreuve_facultative):
        self.candidat_id = candidat_id
        self.compo_franc = compo_franc
        self.dictee = dictee
        self.etude_de_texte = etude_de_texte
        self.instruction_civique = instruction_civique
        self.histoire_geographie = histoire_geographie
        self.mathematiques = mathematiques
        self.pc_lv2 = pc_lv2
        self.svt = svt
        self.anglais_ecrit = anglais_ecrit
        self.anglais_oral = anglais_oral
        self.eps = eps
        self.epreuve_facultative = epreuve_facultative

    def save(self):
        """ Enregistre les notes d'un candidat """
        db = Database()
        db.cursor.execute("""
            INSERT INTO Notes (candidat_id, compo_franc, dictee, etude_de_texte, instruction_civique, histoire_geographie, 
                               mathematiques, pc_lv2, svt, anglais_ecrit, anglais_oral, eps, epreuve_facultative)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.candidat_id, self.compo_franc, self.dictee, self.etude_de_texte, self.instruction_civique,
              self.histoire_geographie, self.mathematiques, self.pc_lv2, self.svt, self.anglais_ecrit,
              self.anglais_oral, self.eps, self.epreuve_facultative))
        db.conn.commit()
        db.close()
        print("Notes ajoutées avec succès !")


    def get_notes_by_candidat_id(candidat_id):
        """  Récupère les notes d'un candidat spécifique. """
        db = Database()
        db.cursor.execute("""
            SELECT compo_franc, dictee, etude_de_texte, instruction_civique, histoire_geographie, 
                   mathematiques, pc_lv2, svt, anglais_ecrit, anglais_oral, eps, epreuve_facultative
            FROM Notes
            WHERE candidat_id = ?
        """, (candidat_id,))

        result = db.cursor.fetchone()  # Récupère une seule ligne (car l'ID est unique)
        db.close()

        if result:
            # Retourner les notes sous forme de dictionnaire avec des clés descriptives
            return {
                "compo_franc": result[0],
                "dictee": result[1],
                "etude_de_texte": result[2],
                "instruction_civique": result[3],
                "histoire_geographie": result[4],
                "mathematiques": result[5],
                "pc_lv2": result[6],
                "svt": result[7],
                "anglais_ecrit": result[8],
                "anglais_oral": result[9],
                "eps": result[10],
                "epreuve_facultative": result[11]
            }
        else:
            # Aucun enregistrement trouvé pour cet ID candidat
            print(f"Aucune note trouvée pour le candidat avec l'ID {candidat_id}")
            return None

    def update(self, candidat_id):
        """ Met à jour les notes d'un candidat existant """
        db = Database()
        try:
            db.cursor.execute("""
                    UPDATE Notes
                    SET compo_franc = ?, dictee = ?, etude_de_texte = ?, instruction_civique = ?, 
                        histoire_geographie = ?, mathematiques = ?, pc_lv2 = ?, svt = ?, 
                        anglais_ecrit = ?, anglais_oral = ?, eps = ?, epreuve_facultative = ?
                    WHERE candidat_id = ?
                """, (self.compo_franc, self.dictee, self.etude_de_texte, self.instruction_civique,
                      self.histoire_geographie, self.mathematiques, self.pc_lv2, self.svt,
                      self.anglais_ecrit, self.anglais_oral, self.eps, self.epreuve_facultative,
                      candidat_id))
            db.conn.commit()
            print("Notes mises à jour avec succès !")
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour des notes : {e}")
        finally:
            db.close()

    @staticmethod
    def get_all():
        """ Récupère toutes les notes pour tous les candidats """
        db = Database()
        try:
            db.cursor.execute("""
                SELECT id, candidat_id, compo_franc, dictee, etude_de_texte, instruction_civique, 
                       histoire_geographie, mathematiques, pc_lv2, svt, anglais_ecrit, 
                       anglais_oral, eps, epreuve_facultative
                FROM Notes
            """)
            notes = db.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des notes : {e}")
            notes = []
        finally:
            db.close()

        return notes
