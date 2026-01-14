import json

with open('data/thouv_scores.json', encoding='utf-8') as f:
    scores = json.load(f)

print(f"Total scores: {len(scores)}\n")
bad_scores = []

for i, s in enumerate(scores):
    nom = s.get('nom', '')
    if len(nom) < 2 or len(nom) > 50:
        bad_scores.append(i)
        print(f"Score {i}: nom='{nom}' ({len(nom)} char) - INVALIDE")

print(f"\nTotal problemes: {len(bad_scores)}")
print(f"Indices: {bad_scores}")
