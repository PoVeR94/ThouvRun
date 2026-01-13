# 🎮 Configuration Multi-Joueur Thouv'Run

## Vue d'Ensemble de l'Architecture

Votre système multi-joueur fonctionne avec une **architecture client-serveur centralisée**:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Votre Domaine Personnalisé (thouv-run.yourdomain.com) │
│  ┌──────────────────────────────────────────────────┐  │
│  │         RENDER.COM (Hébergement Gratuit)         │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │  api_server.py (Serveur Flask)             │  │  │
│  │  │  - Base de données SQLite                  │  │  │
│  │  │  - API REST pour recevoir les scores       │  │  │
│  │  │  - Page leaderboard scores.html            │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│                         ▲                              │
│                    Internet (HTTPS)                    │
│                         │                              │
└─────────────────────────┼──────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
    │ Maison 1│      │ Maison 2│      │ Maison 3│
    │ PC Joueur       │ PC Joueur       │ PC Joueur
    │ (Jeu lancé)     │ (Jeu lancé)     │ (Jeu lancé)
    └────┬────┘      └────┬────┘      └────┬────┘
         │                │                │
         └────────────────┼────────────────┘
              Envoie les scores au serveur
              + Récupère tous les autres scores
```

## Comment Ça Marche

### 1️⃣ Quand un joueur joue et finit une partie:

- Le jeu sauve le score **localement** dans `data/thouv_scores.json`
- En arrière-plan, `gestion_scores.py` envoie le score au serveur (thread non-bloquant)
- Le serveur stocke le score dans SQLite

### 2️⃣ Le leaderboard se met à jour:

- Visitez votre site: `https://thouv-run.yourdomain.com`
- La page télécharge tous les scores depuis le serveur
- Les scores se mettent à jour toutes les 5 secondes (auto-refresh)

### 3️⃣ Synchronisation entre joueurs:

- **À partir du jeu**: Avant de jouer, il est possible d'appeler `synchroniser_scores_depuis_serveur()` pour récupérer les scores des autres joueurs
- **Localement**: Chaque PC garde aussi une copie des scores pour jouer hors ligne

## Configuration (Avant Déploiement)

### Étape 1: Configurer votre domaine (IONOS)

1. Achetez un domaine chez [IONOS](https://www.ionos.fr) (~1€/an)
   - Exemple: `thouv-run.com`

2. Accédez aux **Paramètres DNS** de votre domaine

3. Pointez le domaine vers Render:
   - Créez un enregistrement `CNAME`:
     - **Domaine**: `thouv-run.yourdomain.com`
     - **Cible**: `votre-app.onrender.com` (fourni par Render)

### Étape 2: Déployer sur Render.com

1. Créez un compte gratuit sur [Render.com](https://render.com)

2. **Connectez votre dépôt GitHub** ou uploadez le code

3. Créez un **Web Service**:
   - **Name**: `thouv-run` (ou votre choix)
   - **Runtime**: `Python 3`
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `python api_server.py`
   - **Port**: `5000`

4. Render crée une URL provisoire: `thouv-run.onrender.com`

5. Configurez le **domaine personnalisé**:
   - Allez dans **Settings** → **Custom Domains**
   - Ajoutez votre domaine IONOS
   - Render donne les instructions DNS

### Étape 3: Configurer le jeu pour votre serveur

**Dans `src/gestion_scores.py`**, changez:

```python
# ❌ Ancien (développement local):
# API_SERVER_URL = "http://localhost:5000/api/scores"

# ✅ Nouveau (production):
API_SERVER_URL = "https://thouv-run.yourdomain.com/api/scores"
```

Remplacez `yourdomain.com` par votre vrai domaine IONOS.

### Étape 4: Ajouter la synchronisation au jeu

Optionnel: Pour que les joueurs récupèrent automatiquement les scores des autres:

Dans `main_graphique.py` ou `main_terminal.py`, au **démarrage du jeu**:

```python
from gestion_scores import synchroniser_scores_depuis_serveur

# Lors du démarrage
print("Synchronisation des scores...")
synchroniser_scores_depuis_serveur()
```

## Endpoints API Disponibles

### Scores

- **GET** `/api/scores` - Récupère tous les scores
- **POST** `/api/scores` - Soumet un nouveau score

```json
POST body:
{
  "nom": "Bastien",
  "score_total": 1500,
  "distance": 500,
  "bedos": 10,
  "version": "Graphique",
  "difficulte": "NORMALE",
  "date": "12/01/2024 15:30"
}
```

### Statistiques

- **GET** `/api/stats` - Stats globales (nombre de parties, meilleur score, etc.)
- **GET** `/api/player/{nom}` - Stats d'un joueur spécifique

### Santé

- **GET** `/health` - Vérifie que le serveur est en ligne

## Fichiers Modifiés pour Multi-Joueur

### `api_server.py`
- Serveur central Flask avec SQLite
- Base de données persistante au lieu de JSON en mémoire
- Endpoints pour recevoir/servir les scores

### `src/gestion_scores.py`
- Nouvelle fonction `synchroniser_scores_depuis_serveur()` pour récupérer les scores du serveur
- Configuration `API_SERVER_URL` pour pointer vers votre domaine

### `scores.html`
- Page web du leaderboard
- À héberger sur Render (servie automatiquement par `api_server.py`)

## Stockage des Données

### Local (sur chaque PC)
- `data/thouv_scores.json` - Copie locale des scores (sauvegarde de secours)
- `data/last_player.txt` - Dernier joueur utilisé

### Central (sur Render)
- Base de données SQLite dans le conteneur Render
- Stocke **tous** les scores de **tous** les joueurs
- Accessible via API

> ⚠️ **Note**: À la première synchronisation après déploiement, les anciens scores locaux seront fusionnés avec le serveur.

## Dépannage

### Le jeu ne peut pas envoyer les scores
- Vérifiez que `API_ENABLED = True` dans `gestion_scores.py`
- Vérifiez que `API_SERVER_URL` est correct
- Vérifiez que votre domaine pointe vers Render

### Render dit "Free tier limit reached"
- Render met en pause les services gratuits après 15 min d'inactivité
- Visitez le site: il redémarre automatiquement
- Alternative: utiliser Railway.app (plus généreux) ou payer pour Render

### SQLite "database is locked"
- Cela ne devrait pas arriver avec Render
- Si problème en développement local: relancer `api_server.py`

## Coûts

- **Domaine IONOS**: ~1€/an
- **Hébergement Render**: Gratuit (pour les premiers essais)
- **SQLite**: Gratuit (base de données embarquée)

**Total**: ~1€/an + votre électricité pour lancer le jeu

## Questions Fréquentes

**Q: Pourquoi SQLite au lieu de PostgreSQL?**
- SQLite est embarqué dans Python, zéro configuration
- Parfait pour petit nombre d'utilisateurs
- Migration vers PostgreSQL possible plus tard

**Q: Qu'arrive-t-il si Render s'arrête?**
- Votre PC continue à jouer (stockage local)
- Les scores se synchronisent quand le serveur revient

**Q: Puis-je partager le leaderboard sur les réseaux sociaux?**
- Oui! Donnez l'URL: `https://thouv-run.yourdomain.com`

---

**Configuration complète et jeu!** 🚀
