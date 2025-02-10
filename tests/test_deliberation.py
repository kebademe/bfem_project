from deliberation import Deliberation


# Test sur un candidat existant
candidat_id = 1  # Remplace par un ID existant dans la BD
deliberation = Deliberation(candidat_id)

print(f"Total des points : {deliberation.calculer_total()}")
print(f"Résultat final : {deliberation.determiner_resultat()}")

deliberation.save_resultat()
