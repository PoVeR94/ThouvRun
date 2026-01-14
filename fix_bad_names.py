import json

# Charger les scores
with open('data/thouv_scores.json', encoding='utf-8') as f:
    scores = json.load(f)

# Corriger les noms invalides
fixed = 0
for i, score in enumerate(scores):
    nom = score.get('nom', '')
    if len(nom) < 2:
        new_nom = nom + ' ' * (2 - len(nom))  # Ajouter des espaces
        print(f"Score {i}: '{nom}' -> '{new_nom}'")
        score['nom'] = new_nom
        fixed += 1

print(f"\nTotal corrigés: {fixed}")

# Sauvegarder
with open('data/thouv_scores.json', 'w', encoding='utf-8') as f:
    json.dump(scores, f, indent=4, ensure_ascii=False)

print("Sauvegardé!")
