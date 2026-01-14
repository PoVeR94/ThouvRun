# 🚀 TEST RAPIDE - 5 MINUTES

Tout ce qu'il faut faire pour tester que le jeu envoie les scores au serveur en ligne!

---

## ✅ **Checklist Rapide**

```powershell
# 1. Installer les dépendances
pip install -r requirements-dev.txt

# 2. Vérifier que Render répond
curl -UseBasicParsing https://thouvrun.onrender.com/health

# 3. Lancer le jeu
python src/main_graphique.py

# 4. Jouer une partie jusqu'au game over

# 5. Vérifier que le score s'est envoyé
curl -UseBasicParsing https://thouvrun.onrender.com/api/scores

# 6. Voir le leaderboard web
# Ouvrir: https://thouvrun.onrender.com
```

---

## 🎯 **Résultats Attendus**

### ✅ Étape 2: Health Check
```
StatusCode: 200
{"status":"online","timestamp":"..."}
```

### ✅ Étape 5: Vos Scores sur le Serveur
```json
[
  {
    "nom": "YourName",
    "score_total": 1500,
    "distance": 500,
    "bedos": 10,
    ...
  }
]
```

### ✅ Étape 6: Leaderboard Web
Votre score apparaît dans le tableau! ✅

---

## 📝 **Logs à Vérifier**

Lors du jeu, vous verrez dans la console:

```
[API] Score envoyé avec succès
[Sync] Scores synchronisés
```

---

**Si tout ça fonctionne → C'est bon! 🎉**

Voir [TEST_GAMEPLAY.md](TEST_GAMEPLAY.md) pour plus de détails.
