# ✅ Projet Thouv'Run - Multi-Joueur Configuré

## Résumé de ce qui a été fait

### 1. ✅ Nettoyage du Projet
- Supprimé tous les fichiers de documentation inutiles
- Gardé uniquement les fichiers essentiels pour le multi-joueur

### 2. ✅ Serveur Multi-Joueur Complètement Refondu
- **Nouveau**: `api_server.py` avec SQLite au lieu de JSON
- **Endpoints**: GET/POST scores, stats, player stats, health check
- **Base de données**: Persistent SQLite database
- **Leaderboard**: Page web intégrée (scores.html servie automatiquement)

### 3. ✅ Client Mis à Jour
- **`src/gestion_scores.py`**: Nouvelle fonction `synchroniser_scores_depuis_serveur()`
- **Configuration**: `API_SERVER_URL` prêt pour domaine personnalisé
- **Sync**: Fusion des scores locaux et distants

### 4. ✅ Documentation Complète
- **README.md**: Guide complet du projet
- **DEPLOYMENT_QUICK_START.md**: Déploiement en 5 minutes
- **MULTIPLAYER_SETUP.md**: Configuration détaillée
- **ARCHITECTURE_MULTIPLAYER.md**: Explication complète du système

---

## 🎯 Structure Finale du Projet

```
📁 Projet Thouv/
├── 📄 README.md                           ← Lire d'abord!
├── 📄 DEPLOYMENT_QUICK_START.md           ← Guide rapide (5 min)
├── 📄 MULTIPLAYER_SETUP.md                ← Configuration détaillée
├── 📄 ARCHITECTURE_MULTIPLAYER.md         ← Comprendre le système
│
├── 🐍 api_server.py                       ← Serveur Flask (NEW)
├── 📊 scores.html                         ← Leaderboard web
├── 📦 requirements.txt                    ← Dépendances
│
├── 📁 src/
│   ├── main_graphique.py                  ← Jeu (Pygame)
│   ├── main_terminal.py                   ← Jeu (Terminal)
│   ├── gestion_scores.py                  ← Sync scores (MODIFIÉ)
│   ├── moteur_jeu.py
│   └── tache_fond.py
│
├── 📁 assets/                             ← Images, sons
│
├── 📁 data/
│   ├── thouv_scores.json                  ← Stockage local
│   └── last_player.txt
│
├── 🖼️ Thouv-Run-Graphique.bat
├── 🖼️ Thouv-Run-Terminal.bat
├── 🖼️ Thouv-Leaderboard.bat
├── 🔧 SETUP.bat
└── 📋 project.json
```

---

## 🚀 Comment ça Marche Maintenant

### Schéma Simple:

```
Vous jouez sur votre PC
        ↓
    Score sauvegardé localement ✓
        ↓
    Score envoyé au serveur (background) ✓
        ↓
    Serveur reçoit et stocke dans SQLite ✓
        ↓
    Votre site web affiche le leaderboard ✓
        ↓
    Tous les joueurs voient le classement en temps réel ✓
```

### Étapes de Déploiement:

1. **IONOS** (~1€/an)
   - Acheter domaine: `thouv-run.com`

2. **Render.com** (Gratuit)
   - Créer Web Service
   - Uploader `api_server.py`
   - Obtenir URL: `thouv-run.onrender.com`

3. **Configuration DNS**
   - Pointer domaine IONOS vers Render
   - Accéder via: `https://thouv-run.yourdomain.com`

4. **Mise à jour du jeu**
   - Éditer `src/gestion_scores.py` ligne ~11:
     ```python
     API_SERVER_URL = "https://thouv-run.yourdomain.com/api/scores"
     ```

5. **Tester!**
   - Lancer le jeu → scores s'envoient
   - Visiter le site → leaderboard en temps réel

---

## 📊 Endpoints API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/scores` | GET | Tous les scores |
| `/api/scores` | POST | Soumettre un score |
| `/api/stats` | GET | Stats globales |
| `/api/player/{nom}` | GET | Stats joueur |
| `/health` | GET | Vérifier serveur |
| `/` ou `/scores.html` | GET | Leaderboard web |

---

## 💾 Stockage des Données

### Local (Chaque PC)
- `data/thouv_scores.json` - Sauvegarde de secours
- Permet de jouer hors ligne
- Mise à jour par le jeu

### Central (Serveur Render)
- SQLite database
- Contient tous les scores de tous les joueurs
- Accessible via API REST
- Source de vérité unique

---

## 🔄 Sync Multi-Joueur

### Flux Automatique:
1. Joueur 1 termine partie → Score envoyé au serveur
2. Joueur 2 visite leaderboard → Voit score de Joueur 1
3. Joueur 3 lance le jeu → Peut appeler `synchroniser_scores_depuis_serveur()`
4. Tous les joueurs voient tous les scores

### Code pour Sync (Optionnel):

```python
# Dans main_graphique.py ou main_terminal.py, au démarrage:
from gestion_scores import synchroniser_scores_depuis_serveur

print("Synchronisation des scores...")
synchroniser_scores_depuis_serveur()
```

---

## 📋 Fichiers de Configuration

### `requirements.txt`
```
Flask==3.0.0
Flask-CORS==4.0.0
requests==2.31.0
pygame==2.6.1
windows-curses==2.3.0 (Windows seulement)
```

### `src/gestion_scores.py`
Ligne ~11:
```python
# À personnaliser avant déploiement:
API_SERVER_URL = "https://thouv-run.yourdomain.com/api/scores"
```

### `api_server.py`
- Commence automatiquement avec `if __name__ == '__main__'`
- Écoute sur `0.0.0.0:PORT` (configurable)
- Crée `data/scores.db` automatiquement

---

## ⚠️ Points Importants

### Render Gratuit
- S'arrête après 15 minutes sans activité
- Redémarrage automatique à la prochaine requête
- Les données (SQLite) sont toujours sauvegardées

### Sécurité
- Actuellement: pas d'authentification
- Possible amélioration: ajouter tokens/login
- Validation des scores: peut être améliorée

### Performance
- SQLite: Ok pour 1-100 joueurs
- Au-delà: migrer vers PostgreSQL

---

## 🔗 Ressources

- [README.md](README.md) - Vue d'ensemble
- [DEPLOYMENT_QUICK_START.md](DEPLOYMENT_QUICK_START.md) - Déploiement rapide
- [MULTIPLAYER_SETUP.md](MULTIPLAYER_SETUP.md) - Configuration détaillée
- [ARCHITECTURE_MULTIPLAYER.md](ARCHITECTURE_MULTIPLAYER.md) - Architecture complète

---

## ✨ Prochaines Étapes

### Immédiat:
1. ✅ Lire [README.md](README.md)
2. ✅ Tester le jeu localement: `python src/main_graphique.py`
3. ✅ Vérifier que scores sont sauvegardés dans `data/thouv_scores.json`

### Court terme:
1. ⏳ Acheter domaine IONOS
2. ⏳ Créer compte Render.com
3. ⏳ Déployer en suivant [DEPLOYMENT_QUICK_START.md](DEPLOYMENT_QUICK_START.md)
4. ⏳ Mettre à jour `API_SERVER_URL` dans le code
5. ⏳ Tester le leaderboard web

### Futur:
- Ajouter authentification
- Valider les scores (anti-triche)
- Rate limiting
- Upgrader vers PostgreSQL si plus de joueurs

---

## 🎮 Lancement du Jeu

### Local (Développement)
```bash
# Terminal 1:
python api_server.py

# Terminal 2:
python src/main_graphique.py
```

### Via les Raccourcis (Windows)
- `Thouv-Run-Graphique.bat` - Jeu Pygame
- `Thouv-Run-Terminal.bat` - Jeu Terminal
- `Thouv-Leaderboard.bat` - Ouverture du leaderboard

---

## 📞 Support

**Question sur le déploiement?**
→ Voir [DEPLOYMENT_QUICK_START.md](DEPLOYMENT_QUICK_START.md)

**Question sur l'architecture?**
→ Voir [ARCHITECTURE_MULTIPLAYER.md](ARCHITECTURE_MULTIPLAYER.md)

**Question sur la configuration?**
→ Voir [MULTIPLAYER_SETUP.md](MULTIPLAYER_SETUP.md)

---

**Votre système multi-joueur est prêt!** 🎉

Prochaine étape: Lire README.md puis DEPLOYMENT_QUICK_START.md pour mettre en ligne! 🚀
