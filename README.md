# 🎮 Thouv'Run - Multi-Joueur Leaderboard

Jeu de plateforme (Pygame) avec **leaderboard multi-joueur en temps réel**.

## Qu'est-ce que c'est?

Un jeu classique de plateforme où:
- **Jouez** sur votre PC (graphique ou terminal)
- **Vos scores** sont envoyés automatiquement à un serveur central
- **Tous les joueurs** voient le leaderboard en temps réel via un site web
- **Pas besoin d'internet** pour jouer (les scores se synchronisent quand possible)

## Lancement Rapide

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Lancer le jeu

- **Version Graphique** (Pygame): Double-clic sur `Thouv-Run-Graphique.bat`
- **Version Terminal** (Curses): Double-clic sur `Thouv-Run-Terminal.bat`
- **Leaderboard Web**: Double-clic sur `Thouv-Leaderboard.bat`

### 3. (Optionnel) Déployer en ligne

Voir [DEPLOYMENT_QUICK_START.md](DEPLOYMENT_QUICK_START.md) pour:
- Acheter un domaine IONOS (1€/an)
- Déployer sur Render.com (gratuit)
- Configurer le leaderboard public

## Architecture

```
Votre Domaine (IONOS)
├── https://thouv-run.yourdomain.com
│   ├── /           → Leaderboard web
│   └── /api/*      → API REST
│
Serveur (Render.com - Gratuit)
├── api_server.py   → Reçoit/sert les scores
├── scores.db       → Base de données SQLite
└── scores.html     → Page leaderboard

Vos PCs
├── main_graphique.py
├── main_terminal.py
└── gestion_scores.py → Envoie les scores au serveur
```

## Structure des Fichiers

```
📁 Projet Thouv/
├── 📄 README.md (ce fichier)
├── 📄 DEPLOYMENT_QUICK_START.md (guide déploiement)
├── 📄 MULTIPLAYER_SETUP.md (configuration multi-joueur)
├── 📄 ARCHITECTURE_MULTIPLAYER.md (architecture détaillée)
│
├── 🐍 api_server.py (serveur Flask)
├── 📊 scores.html (leaderboard web)
├── 📦 requirements.txt
├── 🔧 SETUP.bat
│
├── 📁 src/
│   ├── main_graphique.py
│   ├── main_terminal.py
│   ├── gestion_scores.py ← Envoie scores au serveur
│   ├── moteur_jeu.py
│   └── tache_fond.py
│
├── 📁 assets/ (images, sons)
│
├── 📁 data/
│   ├── thouv_scores.json (stockage local)
│   └── last_player.txt
│
└── 🖼️ Thouv-Run-*.bat (raccourcis)
```

## Configuration Multi-Joueur

### Local (Développement)

Le jeu et le serveur tournent sur `localhost:5000`:

```bash
# Terminal 1: Lancer le serveur
python api_server.py

# Terminal 2: Lancer le jeu
python src/main_graphique.py
```

### En Ligne (Production)

Voir [DEPLOYMENT_QUICK_START.md](DEPLOYMENT_QUICK_START.md) pour:
1. Acheter domaine IONOS
2. Déployer sur Render
3. Configurer DNS
4. Mettre à jour `src/gestion_scores.py`

## Fonctionnalités

### Jeu
- ✅ Plateforme classique (monter, sauter, éviter obstacles)
- ✅ Deux versions: Graphique (Pygame) et Terminal (Curses)
- ✅ Scores automatiquement sauvegardés
- ✅ Fonctionne hors ligne

### Leaderboard Web
- ✅ Affiche tous les scores en temps réel
- ✅ Recherche par joueur
- ✅ Tri par colonne
- ✅ Stats globales
- ✅ Auto-refresh (5 sec)
- ✅ Responsive design

### Multi-Joueur
- ✅ Scores centralisés sur serveur
- ✅ Synchronisation automatique
- ✅ Accessible via domaine personnalisé
- ✅ Gratuit (Render + IONOS 1€)

## Endpoints API

```
GET  /api/scores          → Tous les scores
POST /api/scores          → Soumettre un score
GET  /api/stats           → Stats globales
GET  /api/player/{nom}    → Stats joueur
GET  /health              → Vérifier que serveur est actif
GET  /                    → Leaderboard web
```

## Questions Fréquentes

**Q: Comment jouer hors ligne?**
- Les scores sont sauvegardés localement, jouez normalement
- Ils se synchronisent au serveur dès que vous avez internet

**Q: Quel est le coût?**
- IONOS: ~1€/an
- Render: Gratuit (avec pause après 15 min inactivité)
- **Total: ~1€/an**

**Q: Puis-je partager le leaderboard?**
- Oui! Donnez l'URL: `https://thouv-run.yourdomain.com`

**Q: Comment changer `API_SERVER_URL`?**
- Fichier: `src/gestion_scores.py` ligne ~11
- Mettez votre domaine

**Q: Les scores sont sécurisés?**
- Les données sont sur serveur central
- Actuellement pas d'authentification (improvement future)

## Dépannage

### Le serveur n'écoute pas?
```bash
python api_server.py
```
Ou vérifier que port 5000 est libre

### Les scores ne s'envoient pas?
1. Vérifier `API_SERVER_URL` est correct
2. Vérifier que `API_ENABLED = True`
3. Vérifier que serveur est actif

### Problème DNS après déploiement?
- Vérifier à https://mxtoolbox.com
- Attendre propagation DNS (5-30 min)

### Render redémarrage lent?
- Render gratuit s'arrête après 15 min
- Visiter le site pour redémarrer
- Données toujours sauvegardées en base

## Documentation Complète

- [ARCHITECTURE_MULTIPLAYER.md](ARCHITECTURE_MULTIPLAYER.md) - Explication complète du système
- [MULTIPLAYER_SETUP.md](MULTIPLAYER_SETUP.md) - Configuration détaillée
- [DEPLOYMENT_QUICK_START.md](DEPLOYMENT_QUICK_START.md) - Guide déploiement

## Stack Technique

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Flask 3.0.0, SQLite
- **Jeu**: Pygame 2.6.1, windows-curses
- **Hébergement**: Render.com
- **Domaine**: IONOS
- **Communication**: REST API, JSON

## Versions

- **v1.0**: Jeu local avec leaderboard sur machine unique
- **v2.0**: Multi-joueur en ligne avec Render + IONOS

## Licence

Projet personnel

---

**Prêt à joueur?** Lancez `Thouv-Run-Graphique.bat` ou lisez [DEPLOYMENT_QUICK_START.md](DEPLOYMENT_QUICK_START.md) pour le déploiement! 🚀
