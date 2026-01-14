# 🔄 Synchronisation des Scores - Thouv'Run

## Vue d'ensemble

Le jeu Thouv'Run synchronise les scores avec un serveur central sur **Render.com** pour permettre à plusieurs joueurs de partager leurs records et de consulter un classement global.

## Comment ça marche?

### 1️⃣ **Au démarrage du jeu**
- Le jeu charge les scores **locaux** (fichier `data/thouv_scores.json`)
- Lance une synchronisation en arrière-plan (thread) qui:
  - ✅ Envoie TOUS les scores locaux vers le serveur
  - ✅ Récupère les scores des autres joueurs depuis le serveur
  - ✅ Fusionne les scores (évite les doublons)

### 2️⃣ **À chaque fin de partie**
- Le nouveau score est **sauvegardé localement** immédiatement (fichier JSON)
- Envoyé au serveur en arrière-plan (thread non-bloquant)
- Les autres joueurs verront votre score dans le leaderboard en ligne

### 3️⃣ **Consultation du leaderboard**
- Accédez à: **https://thouvrun.onrender.com/scores.html**
- La page affiche les meilleurs scores de TOUS les joueurs
- Se rafraîchit automatiquement chaque 5 secondes

## Fichiers impliqués

### Client (Ton PC)
- **`data/thouv_scores.json`** - Base de données locale (197 scores)
- **`data/last_player.txt`** - Dernier joueur utilisé
- **`src/gestion_scores.py`** - Module de gestion des scores
  - `charger_scores()` - Charge depuis le JSON local
  - `sauvegarder_nouveau_score()` - Sauvegarde et envoie au serveur
  - `synchroniser_scores_au_demarrage()` - Sync au démarrage

### Serveur (Render.com)
- **`api_server.py`** - Serveur Flask
  - `GET /api/scores` - Récupère tous les scores
  - `POST /api/scores` - Ajoute un nouveau score
  - `GET /health` - Vérification de disponibilité
- **`scores.html`** - Interface web du leaderboard
- **`data/thouv_scores.db`** - Base de données SQLite

## Synchronisation manuelle

Si tu veux synchroniser TOUS tes scores locaux immédiatement:

### Option 1: Fichier batch (Windows)
```bash
Double-clique sur: Sync-Scores.bat
```

### Option 2: Ligne de commande
```bash
python sync_scores_to_server.py
```

Cela va:
1. Charger les 197 scores locaux
2. Les envoyer TOUS au serveur
3. Afficher un rapport détaillé
4. Vérifier que tout est bien passé

## État actuel

```
✅ 194 scores synchronisés (3 ont eu erreur de validation)
📊 100 scores disponibles sur le leaderboard
🌐 https://thouvrun.onrender.com/scores.html
```

## Dépannage

### Le leaderboard est vide?
- ❌ Lance `Sync-Scores.bat` pour forcer la synchronisation
- ❌ Attends quelques secondes (la synchronisation en thread est asynchrone)
- ❌ Rafraîchis la page web (F5)

### Un score n'apparaît pas?
- Le serveur limite à 100 scores pour les performances
- Seuls les meilleurs scores sont affichés
- Les scores bas peuvent être "en file d'attente"

### Erreur de connexion au serveur?
- ✅ C'est normal! Le serveur peut être en redémarrage
- ✅ Tes scores sont TOUJOURS sauvegardés localement
- ✅ Ils seront resynchronisés à ta prochaine partie

## Configurations avancées

### Désactiver la synchronisation
Dans `src/gestion_scores.py`:
```python
API_ENABLED = False  # Change à False pour désactiver
```

### Serveur local (développement)
```python
API_SERVER_URL = "http://localhost:5000/api/scores"
```
Puis lance: `python api_server.py`

## Flux détaillé

```
┌─────────────────────────┐
│  Démarrage du jeu       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ Thread 1: Envoyer tous les scores locaux    │
│ (non-bloquant)                              │
└────────────┬────────────────────────────────┘
             │
             ▼ (simultanément)
┌──────────────────────────────────────────┐
│ Thread 2: Récupérer scores du serveur    │
│ et fusionner avec les locaux              │
└──────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────┐
│  Le jeu peut commencer!  │
│  (scores sont chargés)   │
└──────────────────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│  Fin de partie                       │
│  → Nouveau score sauvegardé LOCAL   │
│  → Envoyé au SERVEUR en arrière-plan │
└──────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────┐
│  Page web se rafraîchit (5 sec)          │
│  → Récupère les meilleurs scores         │
│  → Les affiche au leaderboard            │
└──────────────────────────────────────────┘
```

## Points clés

✅ **Sauvegarde locale = Priorité #1**
- Tous tes scores sont TOUJOURS sauvegardés localement en JSON
- Aucune perte même si le serveur est down

✅ **Synchronisation asynchrone = Performance**
- Le jeu ne ralentit jamais pour envoyer les scores
- Les envois se font en background (threads)

✅ **Fusion intelligente = Pas de doublons**
- Les scores identiques ne sont pas dupliqués
- Chaque joueur voit tous les scores (locaux + distants)

✅ **Leaderboard centralisé = Compétition**
- Tous les joueurs voient le MÊME classement global
- Accès web 24/7

## Améliorations futures

- [ ] Authentification (comptes joueurs)
- [ ] Statistiques par joueur
- [ ] Classements hebdomadaires/mensuels
- [ ] Anti-triche (validation côté serveur)
- [ ] Badges et achievements

---

*Dernière mise à jour: 14 Janvier 2026*
