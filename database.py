import sqlite3

DB_NAME = "bfem.db"

class Database:
    """ Classe de gestion de la connexion à la base de données """
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """ Création des tables si elles n'existent pas """
        # Table Candidat
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Candidat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_table INTEGER UNIQUE NOT NULL,
                prenom TEXT NOT NULL,
                nom TEXT NOT NULL,
                date_naissance TEXT NOT NULL,
                lieu_naissance TEXT NOT NULL,
                sexe TEXT CHECK(sexe IN ('M', 'F')) NOT NULL,
                nationalite TEXT NOT NULL,
                choix_epreuve_facultative TEXT CHECK(choix_epreuve_facultative IN ('OUI', 'NON')),
                epreuve_facultative TEXT CHECK(epreuve_facultative IN ('Couture', 'Dessin', 'Musique')),
                aptitude_sportive TEXT CHECK(aptitude_sportive IN ('OUI', 'NON'))
            )
        """)

        # Table Livret Scolaire
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS LivretScolaire (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidat_id INTEGER UNIQUE NOT NULL,
                nombre_de_fois INTEGER NOT NULL,
                moyenne_6e REAL,
                moyenne_5e REAL,
                moyenne_4e REAL,
                moyenne_3e REAL,
                moyenne_cycle REAL,
                FOREIGN KEY (candidat_id) REFERENCES Candidat(id) ON DELETE CASCADE
            )
        """)

        # Table Notes
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        candidat_id INTEGER UNIQUE NOT NULL,
                        compo_franc REAL,
                        dictee REAL,
                        etude_de_texte REAL,
                        instruction_civique REAL,
                        histoire_geographie REAL,
                        mathematiques REAL,
                        pc_lv2 REAL,
                        svt REAL,
                        anglais_ecrit REAL,
                        anglais_oral REAL,
                        eps REAL,
                        epreuve_facultative REAL,
                        FOREIGN KEY (candidat_id) REFERENCES Candidat(id) ON DELETE CASCADE
                    )
                """)

        # Table Jury
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Jury (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region TEXT NOT NULL,
                ief TEXT NOT NULL,
                localite TEXT NOT NULL,
                centre_examen TEXT NOT NULL,
                president_jury TEXT NOT NULL,
                telephone TEXT NOT NULL
            )
        """)

        # Table Anonymat
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Anonymat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidat_id INTEGER UNIQUE NOT NULL,
                anonymat_principal TEXT UNIQUE NOT NULL,
                FOREIGN KEY (candidat_id) REFERENCES Candidat(id) ON DELETE CASCADE
            )
        """)

        # Table Resultat
        self.cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Resultat (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       candidat_id INTEGER UNIQUE NOT NULL,
                       resultat TEXT NOT NULL,
                       FOREIGN KEY (candidat_id) REFERENCES Candidat(id) ON DELETE CASCADE
                   )
               """)

        self.conn.commit()

    def close(self):
        """ Fermeture de la connexion """
        self.conn.close()
