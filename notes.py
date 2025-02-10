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
