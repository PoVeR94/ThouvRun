# 🎮 Thouv'Run - Le Jeu de Plateforme Multijoueur

> **Un jeu rapide, fun et compétitif!** Gravissez les obstacles, défiez vos amis, et rejoignez le leaderboard mondial! 🏆

![Badge Joueurs](https://img.shields.io/badge/Joueurs-Actifs-brightgreen?style=flat-square)
![Badge Plateforme](https://img.shields.io/badge/Plateforme-Windows-0078D4?style=flat-square)
![Badge Version](https://img.shields.io/badge/Version-1.0-blue?style=flat-square)

---

## 🎯 C'est Quoi?

**Thouv'Run** c'est un **petit jeu de plateforme fun et addictif** où tu dois:
- 💨 **Esquiver** des obstacles
- 🏃 **Courir** le plus loin possible
- 📊 **Comparer** tes scores avec les autres joueurs

Le meilleur? **Tes scores se synchronisent automatiquement en ligne** - pas besoin de configuration!

---

## ⚡ Lancement Rapide

### 1️⃣ **Installation (en deux fois)**

#### 🪟 Windows
Double-clic sur: **`SETUP.bat`**, une fois pour Python, une deuxieme pour les dépendances.

#### 🍎 Mac / 🐧 Linux
```bash
chmod +x setup.sh
./setup.sh
```

Ça installe automatiquement tout ce qu'il faut (Python, dépendances, etc.)

### 2️⃣ **Jouer au Jeu**

Choisis la version que tu préfères:

#### 🎨 **Version Graphique (Pygame)** - Recommandée!
Double-clic sur: **`Thouv-Run-Graphique.bat`**

#### 🖥️ **Version Terminal (Retro)**
Double-clic sur: **`Thouv-Run-Terminal.bat`**

---

## 🏆 Leaderboard en Ligne

**Accessible 24/7:** https://www.thouvrun.com

Vois tes scores, ceux de tes amis, et sois numéro 1! 🥇

**Fonctionnalités:**
- 🔍 Recherche par joueur
- 📊 Tri par points, distance, date et bedos
- 📈 Statistiques globales
- 🔄 Mise à jour automatique

---

## � Synchronisation des Scores (Développeurs)

### ✅ AUTOMATIQUE (Recommandé!)

Les scores se synchronisent **automatiquement** avant chaque `git push` grâce à un git hook.

```bash
git push  # C'est tout! Les scores se synchro automatiquement
```

### 🔧 MANUEL (Si le hook ne fonctionne pas)

```bash
python scripts/sync_scores_before_push.py
git add data/thouv_scores.json
git commit -m "Update scores"
git push
```

---

## �💡 Astuces pour Scorer Haut

1. **Maîtrise le timing** - Les sauts doivent être précis!
2. **Anticipe les obstacles** - Commence à sauter avant!
3. **Reste concentré** - C'est vite difficile, reste zen!
4. **Entraîne-toi** - Plus tu joues, mieux tu deviens!

---

## 🛠️ Configuration Système

**Requirements minimum:**
- Windows 7+ / macOS 10.14+ / Linux (Ubuntu 18.04+)
- Python 3.8+ (installé automatiquement)
- ~100 MB d'espace disque
- Connexion internet (pour sync scores)

---

## ❓ FAQ

### "Mes scores se sauvegardent?"
✅ Oui! Automatiquement en ligne et en local. Aucun problème de connexion? Les scores se synchro quand tu reviendras en ligne!

### "Je peux jouer hors ligne?"
✅ Oui! Le jeu marche 100% hors ligne. Tes scores se synchro dès que tu as internet.

### "Pourquoi installer Python?"
C'est le langage du jeu. L'installation est automatique - tu appuies juste sur SETUP.bat!

### "Je peux modifier mes scores?"
❌ Non, c'est protégé! Le serveur valide tous les scores. Joue juste, play fair! ⚽

### "Y a un budget?"
💰 Complètement gratuit! Pas de pub, pas de microtransactions, rien. Juste du fun pur!

---

## 📞 Support

Des problèmes? Des suggestions?
- 🐛 Signale un bug
- 💬 Propose une amélioration
- 🎮 Partage tes high-scores!

---

## 📜 License

MIT License - Tu peux faire ce que tu veux avec le code! 

---

**Bon jeu! 🚀 Et que le meilleur gagne!** 🏆
