from anonymat import Anonymat
from candidat import Candidat
from jury import Jury
from livret import LivretScolaire
from notes import Notes
from deliberation import Deliberation



# Ajouter un candidat
candidat = Candidat(103, "Moussa", "Sarr", "2007-02-14", "Dakar", "M", "Sénégalais", "OUI", "Dessin", "OUI")
candidat.save()

# Récupérer l'ID du candidat
candidats = Candidat.get_all()
candidat_id = candidats[-1][0]  # Prend le dernier candidat inséré

# Ajouter un livret scolaire
livret = LivretScolaire(candidat_id, 1, 12.5, 13.0, 11.8, 14.0, 12.8)
livret.save()

# Ajouter des notes
notes = Notes(candidat_id, 15, 14, 13, 12, 10, 16, 14, 13, 12, 15, 10, 0)
notes.save()

# Ajouter un jury
jury = Jury("Dakar", "IEF Dakar", "Centre A", "Lycée Blaise Diagne", "Mr. Ndiaye", "771234567")
jury.save()

# Générer un anonymat pour le candidat
anonymat = Anonymat(candidat_id)
anonymat.save()

# Vérification
print(Candidat.get_all())

# Test sur un candidat existant
candidat_id = 1  # Remplace par un ID existant dans la BD
deliberation = Deliberation(candidat_id)

print(f"Total des points : {deliberation.calculer_total()}")
print(f"Résultat final : {deliberation.determiner_resultat()}")

deliberation.save_resultat()
