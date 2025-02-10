from database import Database

class Deliberation:
    """ Classe pour calculer le total des points et gérer la délibération """

    def __init__(self, candidat_id):
        self.candidat_id = candidat_id
        self.db = Database()
        self.notes = self.get_notes()
        self.livret = self.get_livret()

    def get_notes(self):
        """ Récupère les notes du candidat """
        self.db.cursor.execute("SELECT * FROM Notes WHERE candidat_id = ?", (self.candidat_id,))
        return self.db.cursor.fetchone()

    def get_livret(self):
        """ Récupère le livret scolaire du candidat """
        self.db.cursor.execute("SELECT * FROM LivretScolaire WHERE candidat_id = ?", (self.candidat_id,))
        return self.db.cursor.fetchone()

    def calculer_total(self):
        """ Applique les coefficients et retourne le total des points """
        if not self.notes:
            print("Aucune note trouvée pour ce candidat !")
            return 0

        # Extraction des notes et coefficients
        coef_dict = {
            "compo_franc": 2, "dictee": 1, "etude_de_texte": 1, "instruction_civique": 1,
            "histoire_geographie": 2, "mathematiques": 4, "pc_lv2": 2, "svt": 2,
            "anglais_ecrit": 2, "anglais_oral": 1, "eps": 1, "epreuve_facultative": 1
        }

        total = 0
        for i, (matiere, coef) in enumerate(coef_dict.items()):
            note = self.notes[i + 2]  # Décalage à cause de l'ID candidat
            if note is not None:
                total += note * coef

        # Gestion du bonus/malus EPS
        if self.notes[11] > 10:
            total += self.notes[11] - 10  # Bonus EPS
        else:
            total -= (10 - self.notes[11])  # Malus EPS

        # Gestion du bonus épreuve facultative
        if self.notes[12] > 10:
            total += self.notes[12] - 10  # Bonus épreuve facultative

        return total

    def determiner_resultat(self):
        """ Détermine si le candidat est admis, repêchable ou recalé """
        total = self.calculer_total()

        if total >= 180:
            return "ADMIS"
        elif total >= 171:
            return "REPÊCHABLE (1er Tour)"
        elif total >= 153:
            return "2ND TOUR"
        elif total >= 144:
            return "REPÊCHABLE (2nd Tour)"
        elif self.livret and self.livret[6] >= 12:  # Moyenne cycle >= 12
            return "REPÊCHABLE"
        else:
            return "ÉCHEC"

    def save_resultat(self):
        """ Sauvegarde le résultat du candidat """
        resultat = self.determiner_resultat()
        print(f"Résultat du candidat {self.candidat_id} : {resultat}")
