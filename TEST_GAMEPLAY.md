# 🧪 Guide de Test - ThouvRun

Testons que tout fonctionne: le jeu envoie les scores au serveur en ligne! 🚀

---

## 📋 **Étapes de Test**

### Étape 1: Installer les Dépendances

```powershell
cd "c:\Users\bobes\Desktop\Projet Thouv"
pip install -r requirements-dev.txt
```

### Étape 2: Vérifier que Render Répond

```powershell
curl -UseBasicParsing https://thouvrun.onrender.com/health

# Devrait répondre:
# StatusCode: 200
# Content: {"status":"online",...}
```

### Étape 3: Lancer le Jeu

**Option A - Graphique (Pygame):**
```powershell
python src/main_graphique.py
```

**Option B - Terminal (Curses):**
```powershell
python src/main_terminal.py
```

### Étape 4: Jouer une Partie

1. **Entrer votre nom** (ex: "TestPlayer")
2. **Jouer jusqu'à game over** (avancer, sauter, éviter obstacles)
3. **Score enregistré automatiquement** ✅

### Étape 5: Vérifier Localement

Vérifier que le score est sauvegardé localement:

```powershell
cat data/thouv_scores.json

# Vous devriez voir votre score dans le JSON
```

### Étape 6: Vérifier sur le Serveur

Récupérer les scores du serveur:

```powershell
curl -UseBasicParsing https://thouvrun.onrender.com/api/scores

# Devrait contenir votre score! ✅
```

### Étape 7: Voir le Leaderboard Web

Ouvrir dans le navigateur:
```
https://thouvrun.onrender.com
```

Vous devriez voir:
- ✅ Votre nom dans le classement
- ✅ Votre score
- ✅ Autres statistiques

---

## 🔄 **Cycle Complet de Test**

```
1. Lancer le jeu
   ↓
2. Jouer une partie
   ↓
3. Terminer → Score envoyé au serveur (dans les logs du jeu)
   ↓
4. Vérifier data/thouv_scores.json (sauvegarde locale)
   ↓
5. curl /api/scores (vérifier serveur)
   ↓
6. Navigateur → leaderboard (voir le score en direct)
```

---

## ✅ **Checklist de Vérification**

```
☐ Game lance sans erreur
☐ Score enregistré localement
☐ Score visible dans /api/scores
☐ Leaderboard affiche le score
☐ Leaderboard se met à jour (refresh)
☐ Pas d'erreur SSL/TLS
```

---

## 🐛 **Dépannage**

### "Import Error: pygame"
```powershell
pip install pygame==2.6.1
```

### "SSL Error"
```powershell
# Attendre ou tester sans HTTPS en attendant
curl -UseBasicParsing http://thouvrun.onrender.com/api/scores
```

### "Le score ne s'envoie pas"
Vérifier que dans `src/gestion_scores.py`:
```python
API_ENABLED = True
API_SERVER_URL = "https://thouvrun.onrender.com/api/scores"
```

### "Connection timeout"
Render peut être en pause (gratuit = inactif 15 min). Visitez:
```
https://thouvrun.onrender.com
```
pour le réveiller.

---

## 📊 **Résultats Attendus**

### Après une partie:

**Console du jeu:**
```
[Sync] 1 scores synchronisés
[API] Score envoyé avec succès
```

**Leaderboard:**
```
Rang | Joueur | Points | Distance | Date
1    | TestPlayer | 1500 | 500 | 14/01/2026
```

---

## 🎯 **Test Multi-Joueur**

Pour tester le vrai multi-joueur:

1. **Joueur 1:** Lance le jeu, joue, envoie un score
2. **Joueur 2:** Ouvre le leaderboard → voit le score de Joueur 1
3. **Joueur 2:** Lance le jeu, joue, envoie un score  
4. **Joueur 1:** Voit le score de Joueur 2 en temps réel

---

## 🚀 **Après le Test**

Si tout fonctionne:

1. ✅ **GitHub:** Code est à jour (c066fd5)
2. ✅ **Render:** Serveur en ligne
3. ✅ **Domaine:** Attendre propagation DNS
4. ✅ **Test réussi!**

---

**Happy testing! 🎮**
