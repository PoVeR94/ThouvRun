# 🎯 ThouvRun GitHub - Guide Étape par Étape

## ✅ État Actuel

```
✅ Repo Git initialisé localement
✅ 4 commits créés
✅ Domaine: thouvrun.com acheté
✅ Code configuré pour thouvrun.com
✅ Prêt à pusher!
```

---

## 📋 ÉTAPE 1: Créer le Repo sur GitHub

### Ouvrir GitHub
Allez à: **https://github.com/new**

### Remplir le Formulaire
```
Repository name:        ThouvRun
Description:            Multi-player platformer game with Render + IONOS
Public/Private:         Public
Add .gitignore:         No (déjà fait)
Add License:            No (optionnel)
Initialize README:      No (déjà fait)
```

### Cliquer
Cliquer le bouton bleu: **"Create repository"**

### Résultat
GitHub vous montre un écran avec des instructions. Gardez cette page ouverte.

---

## 🚀 ÉTAPE 2: Pousser le Code sur GitHub

### Ouvrir PowerShell

```powershell
# Naviguer au projet
cd "c:\Users\bobes\Desktop\Projet Thouv"
```

### Remplacer USERNAME

Dans les commandes ci-dessous, remplacez `USERNAME` par votre username GitHub.

**Exemple**: Si votre profil est `https://github.com/bobes-dev`, alors `USERNAME = bobes-dev`

### Commandes à Copier-Coller

```powershell
# 1. Ajouter l'adresse distante (remplacer USERNAME)
git remote add origin https://github.com/USERNAME/ThouvRun.git

# 2. Renommer master en main
git branch -M main

# 3. Pousser le code
git push -u origin main
```

### Authentification

- Si pop-up: **Autoriser** l'accès à GitHub
- Si erreur d'authentification: 
  - Voir section **Personal Access Token** ci-dessous
  - Ou utiliser SSH keys (recommandé pour longue durée)

### Vérification

Après `git push`, vous devriez voir:
```
Branch 'main' set up to track 'origin/main'.
```

✅ Code pushé!

---

## 🔑 Alternative: Personal Access Token

Si authentification HTTPS échoue:

### 1. Créer un Token

Allez à: **https://github.com/settings/tokens/new**

```
Token name:             ThouvRun-Deploy
Expiration:             No expiration (ou 90 jours)
Scopes:                 ✅ repo (Full control)
```

Cliquer: **Generate token**

### 2. Copier le Token

⚠️ **Important**: Vous ne verrez le token qu'une fois!

Copier-coller dans un endroit sûr (temporairement).

### 3. Utiliser dans Git

```powershell
# Remplacer:
# USERNAME = votre username GitHub
# TOKEN = le token copié
git remote set-url origin https://USERNAME:TOKEN@github.com/USERNAME/ThouvRun.git

git push -u origin main
```

### 4. Vérifier sur GitHub

Allez à: **https://github.com/USERNAME/ThouvRun**

Vous devriez voir tous les fichiers! ✅

---

## 🔄 ÉTAPE 3: Futurs Pushes (Après Modifications)

Quand vous modifiez le code:

```powershell
cd "c:\Users\bobes\Desktop\Projet Thouv"

# 1. Ajouter les changements
git add .

# 2. Créer un commit
git commit -m "Description des changements"

# 3. Pousser
git push
```

**Exemples de messages**:
```
git commit -m "Fix leaderboard refresh issue"
git commit -m "Add new game level"
git commit -m "Update API documentation"
```

---

## 📊 ÉTAPE 4: Render - Déploiement

Une fois sur GitHub, Render peut se connecter et redéployer automatiquement!

### 1. Aller sur Render

https://render.com

### 2. Créer Web Service

**New** → **Web Service**

### 3. Connecter GitHub

- Cliquer: **Connect Repository**
- Autoriser Render à accéder GitHub
- Chercher et sélectionner: **ThouvRun**

### 4. Configuration

```
Name:               thouvrun
Environment:        Python 3
Build Command:      pip install -r requirements.txt
Start Command:      python api_server.py
Region:             Frankfurt (EU)
Plan:               Free
```

### 5. Deploy

Cliquer: **Create Web Service**

⏳ Attendre 2-3 minutes

### 6. Résultat

Render vous donne une URL: `https://thouvrun.onrender.com`

---

## 🌐 ÉTAPE 5: Domaine IONOS

Vous avez déjà acheté `thouvrun.com`!

### 1. Aller sur IONOS

**Manage Domains** → **thouvrun.com**

### 2. DNS Settings

Aller à: **DNS Settings** ou **Paramètres DNS**

### 3. Créer CNAME

**Add Record** ou **Ajouter enregistrement**:

```
Name/Subdomain:     (vide pour la racine)
Type:               CNAME
Value/Cible:        thouvrun.onrender.com
TTL:                3600 (défaut)
```

Cliquer: **Save** ou **Enregistrer**

### 4. Propagation DNS

⏳ Attendre 5-30 minutes

Vérifier propagation:
```powershell
nslookup thouvrun.com
```

Vous devriez voir: `thouvrun.onrender.com`

---

## ✅ ÉTAPE 6: Vérifier tout Fonctionne

### 1. Test DNS

```powershell
# Vérifier que le domaine pointe vers Render
nslookup thouvrun.com
```

### 2. Tester l'API

```powershell
# Vérifier que le serveur répond
curl https://thouvrun.com/health

# Devrait retourner: {"status":"online",...}
```

### 3. Voir le Leaderboard

Ouvrir dans le navigateur:
```
https://thouvrun.com
```

Vous devriez voir la page leaderboard! ✅

---

## 🎮 ÉTAPE 7: Mettre à Jour le Jeu

Votre jeu est déjà configuré:

```python
# src/gestion_scores.py
API_SERVER_URL = "https://thouvrun.com/api/scores"
```

✅ Prêt!

Quand vous jouez, les scores s'envoient à `thouvrun.com`!

---

## 📋 Checklist Finale

```
☐ 1. Créé repo sur GitHub
☐ 2. Pushé le code: git push -u origin main
☐ 3. Vérifié sur https://github.com/USERNAME/ThouvRun
☐ 4. Créé Web Service sur Render
☐ 5. Configuré DNS IONOS
☐ 6. Attendu propagation DNS (5-30 min)
☐ 7. Testé https://thouvrun.com
☐ 8. Joué et vérifié que scores s'envoient
☐ 9. Vu les scores sur le leaderboard
```

---

## 🚀 Résumé Commandes (Copy-Paste)

```powershell
# Configuration initiale
cd "c:\Users\bobes\Desktop\Projet Thouv"
git remote add origin https://github.com/USERNAME/ThouvRun.git
git branch -M main
git push -u origin main

# Futurs pushes
git add .
git commit -m "Your message"
git push
```

---

## 💾 En Cas de Problème

**"fatal: remote origin already exists"**
```powershell
git remote remove origin
git remote add origin https://github.com/USERNAME/ThouvRun.git
```

**"Please make sure you have the correct access rights"**
- Utiliser Personal Access Token (voir section ci-dessus)
- Ou configurer SSH keys

**DNS ne fonctionne pas?**
- Attendre plus longtemps (30 min)
- Vérifier avec: `nslookup thouvrun.com`
- Vérifier IONOS DNS Settings

**Render deploy échoue?**
- Vérifier que `requirements.txt` existe
- Vérifier que `api_server.py` existe
- Voir les logs dans Render Dashboard

---

## 📞 Ressources

- GitHub Help: https://docs.github.com
- Render Docs: https://render.com/docs
- IONOS Help: https://www.ionos.fr/help

---

**Vous êtes prêt!** 🎉

Commencez par créer le repo GitHub et pousser le code!
