# 📊 Architecture Multi-Joueur Thouv'Run - Explication Complète

## Vue Globale

Votre système Thouv'Run v2.0 est une **plateforme multi-joueur en ligne décentralisée** où:

- 🎮 **Chaque joueur** lance le jeu sur son PC
- 📤 **Les scores** sont envoyés automatiquement au serveur central
- 🌐 **Un leaderboard public** montre tous les scores en temps réel
- 🔄 **La synchronisation** se fait automatiquement entre serveur et clients

---

## Architecture Détaillée

### Couche 1: Clients (Vos PCs avec le Jeu)

```
Maison 1 - PC du Joueur 1
├── Thouv-Run-Graphique.bat ou Terminal.bat
├── src/main_graphique.py (ou main_terminal.py)
├── src/gestion_scores.py ← MODIFIÉ pour API distante
└── data/thouv_scores.json (sauvegarde locale)

Maison 2 - PC du Joueur 2
└── ... idem ...

Maison 3 - PC du Joueur 3
└── ... idem ...
```

**Rôle des clients**:
1. Lancer le jeu (pygame ou terminal)
2. Terminer une partie → score enregistré localement
3. `gestion_scores.py` envoie le score au serveur (thread non-bloquant)
4. Optionnel: Récupérer les scores des autres joueurs via `synchroniser_scores_depuis_serveur()`

### Couche 2: Serveur Central (Render.com)

```
Render.com (Hébergement Gratuit)
├── api_server.py ← Serveur Flask
│   ├── Reçoit les scores via POST
│   ├── Stocke dans SQLite
│   └── Sert les scores via GET
├── scores.html ← Page web du leaderboard
├── thouv_scores.db ← Base de données SQLite
└── run sur: https://thouv-run.yourdomain.com
```

**Rôle du serveur**:
1. Écouter sur port 5000 (ou PORT env var)
2. Recevoir les scores POST depuis tous les clients
3. Servir les scores GET à tous
4. Servir la page HTML du leaderboard

### Couche 3: Domaine Personnalisé (IONOS)

```
IONOS (1€/an)
├── Domaine: thouv-run.com
└── DNS CNAME pointant vers:
    └── thouv-run.onrender.com (URL Render)
```

**Rôle du domaine**:
- Transformer `https://thouv-run.onrender.com` en `https://thouv-run.yourdomain.com`
- Plus professionnel et mémorisable
- Facilite la configuration des clients

---

## Flux de Données - Étape par Étape

### Scénario: Joueur 1 finit une partie

```
┌──────────────────────────────────┐
│ Joueur 1 termine sa partie       │
│ Score: 1500 pts                  │
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│ Jeu sauvegarde localement:       │
│ data/thouv_scores.json           │
│ ✅ Joueur peut jouer hors ligne  │
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│ Thread daemon envoie POST à:     │
│ https://thouv-run.yourdomain.com │
│           /api/scores            │
│ Données: nom, score, distance... │
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│ Serveur Render reçoit            │
│ Vérifie les données              │
│ Enregistre dans SQLite           │
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│ Leaderboard se met à jour:       │
│ https://thouv-run.yourdomain.com │
│                                  │
│ Joueur 1: 1500 ✅ (nouveau)      │
│ Joueur 2: 1200                   │
│ Joueur 3: 950                    │
└──────────────────────────────────┘
```

### Scénario: Joueur 2 veut voir le classement

```
┌──────────────────────────────────┐
│ Joueur 2 visite:                 │
│ https://thouv-run.yourdomain.com │
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│ Navigateur reçoit scores.html    │
│ + JavaScript qui fetch:          │
│ /api/scores                      │
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│ Serveur retourne JSON:           │
│ [{nom: "Joueur1", score: 1500}...│
└─────────────┬────────────────────┘
              │
              ▼
┌──────────────────────────────────┐
│ Page affiche leaderboard         │
│ Auto-refresh chaque 5 secondes   │
└──────────────────────────────────┘
```

---

## Composants Clés

### 1. API Server (`api_server.py`)

**Endpoints**:
- `GET /api/scores` → Liste tous les scores
- `POST /api/scores` → Ajoute un nouveau score
- `GET /api/stats` → Stats globales (total, best, avg)
- `GET /api/player/{nom}` → Stats d'un joueur
- `GET /` et `/scores.html` → Page du leaderboard
- `GET /health` → Vérifie que le serveur est actif

**Base de données**:
```sql
CREATE TABLE scores (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    score_total INTEGER,
    distance INTEGER,
    bedos INTEGER,
    version TEXT,
    difficulte TEXT,
    date TEXT,
    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### 2. Client Modifications (`gestion_scores.py`)

**Nouvelles fonctions**:
- `synchroniser_scores_depuis_serveur()` → Télécharge et fusionne les scores
- `_telecharger_scores_api()` → Récupère les scores du serveur
- Existantes: `sauvegarder_nouveau_score()` maintenant envoie au serveur aussi

**Configuration**:
```python
API_SERVER_URL = "https://thouv-run.yourdomain.com/api/scores"
API_ENABLED = True  # Pour activer/désactiver facilement
```

### 3. Interface Web (`scores.html`)

**Fonctionnalités**:
- Tableau des 100 meilleurs scores
- Recherche par joueur
- Tri par colonne (score, date, distance, etc.)
- Stats globales (nb joueurs, meilleur score, etc.)
- Auto-refresh toutes les 5 secondes
- Responsive design (fonctionne sur mobile)

---

## Stockage des Données

### Local (Chaque PC)

```
data/
├── thouv_scores.json ← Sauvegarde locale
│   Exemple:
│   [
│       {
│           "nom": "Joueur 1",
│           "score_total": 1500,
│           "distance": 500,
│           "bedos": 10,
│           "version": "Graphique",
│           "difficulte": "NORMALE",
│           "date": "12/01/2024 15:30"
│       },
│       ...
│   ]
└── last_player.txt ← Dernier joueur utilisé
```

**Avantages**:
- ✅ Jouer hors ligne (sans internet)
- ✅ Pas dépendant du serveur
- ✅ Récupération rapide

### Centralisé (Serveur Render)

```
Render Container
└── thouv_scores.db ← Base de données SQLite
    Contient tous les scores de tous les joueurs
    Accessible via API REST
```

**Avantages**:
- ✅ Source de vérité unique
- ✅ Accessible de partout
- ✅ Leaderboard en temps réel
- ✅ Statistiques globales

---

## Flux de Synchronisation

```
PC 1                    Serveur                 PC 2
└─ Termine partie       │                      │
   └─ Envoie score ────→ │                      │
   │  stocke local       │ (SQLite)             │
   │                     │                      │
   │                     ← (sync auto)          │
   │                     │ télécharge           │
   │                     │ (fond)               │
   │                     │────→ Joue            │
   │                     │      récupère        │
   │                     │      les 100 meilleurs
   └─ Affiche ranking    │      du serveur
      mises à jour       │
```

---

## Sécurité & Limitations

### Limitations Render Gratuit

| Aspect | Limite |
|--------|--------|
| Inactivité | Pause après 15 min sans requête |
| Redémarrage | Automatique à la première requête |
| Stockage | ~1 GB (sufficient pour 100k scores) |
| Bandwidth | ~100 GB/mois (sufficient) |
| Requests | Illimitées |

### Sécurité

**Actuellement**:
- Pas d'authentification (anyone peut soumettre des scores)
- API accessible publiquement

**Améliorations possibles**:
- Ajouter authentification (token, login)
- Valider les scores côté serveur (ex: pas de 999999999 pts)
- Rate limiting (limiter le nombre de requests par IP)

---

## Performance & Scaling

### Cas actuel (petit nombre de joueurs)

```
1-5 joueurs  → SQLite suffit
              → Render gratuit suffit
              → Réponse <100ms
```

### Cas futur (plus de joueurs)

```
5-100 joueurs    → SQLite ralentit
                 → Upgrade vers PostgreSQL
                 → Render payant (~$7/mois)

100+ joueurs     → PostgreSQL nécessaire
                 → Caching Redis
                 → CDN pour scores.html
```

---

## Exemples de Code

### 1. Envoyer un score depuis le jeu

```python
from gestion_scores import sauvegarder_nouveau_score

# Après terminer une partie:
sauvegarder_nouveau_score(
    nom_joueur="Alice",
    score_total=1500,
    distance=500,
    bedos=10,
    version="Graphique",
    difficulte="DIFFICILE"
)
# ✅ Sauvegardé localement + envoyé au serveur
```

### 2. Récupérer les scores des autres

```python
from gestion_scores import synchroniser_scores_depuis_serveur

# Au démarrage du jeu:
tous_les_scores = synchroniser_scores_depuis_serveur()

# Afficher le top 3:
for i, score in enumerate(tous_les_scores[:3], 1):
    print(f"{i}. {score['nom']}: {score['score_total']} pts")
```

### 3. Afficher le leaderboard

```python
# Simplement visiter:
# https://thouv-run.yourdomain.com
#
# Ou utiliser l'API directement:
import requests
response = requests.get("https://thouv-run.yourdomain.com/api/scores")
scores = response.json()
```

---

## Déploiement Récapitulatif

| Étape | Durée | Coût |
|-------|-------|------|
| 1. IONOS Domaine | 5 min | ~1€/an |
| 2. Render Setup | 10 min | Gratuit |
| 3. DNS Configuration | 5 min | Gratuit |
| 4. Code Update | 5 min | Gratuit |
| **Total** | **25 min** | **~1€/an** |

---

## Prochaines Étapes

1. ✅ Lire ce document
2. ⏳ Acheter domaine IONOS
3. ⏳ Créer compte Render.com
4. ⏳ Déployer api_server.py
5. ⏳ Configurer DNS
6. ⏳ Mettre à jour `API_SERVER_URL` dans le jeu
7. ⏳ Tester!

---

## Support & Questions

**Le serveur est down?**
- Visiter le site pour le redémarrer (Render gratuit)

**Comment voir les logs du serveur?**
- Render Dashboard → Logs

**Comment changer le code du serveur?**
- Modifie `api_server.py` → Git push → Render redéploie automatiquement

**Comment exporter les scores?**
- Récupérer `data/thouv_scores.json` sur chaque PC
- Ou faire GET /api/scores et télécharger le JSON

---

**Bienvenue dans le multi-joueur!** 🎮🌐
