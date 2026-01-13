# 🚀 Setup GitHub Repo - ThouvRun

Votre repo Git est prêt localement! Maintenant, créez-le sur GitHub et poussez le code.

## Étape 1: Créer le Repo sur GitHub

1. Aller à https://github.com/new
2. **Repository name**: `ThouvRun`
3. **Description**: `Multi-player platformer game with online leaderboard (Pygame, Render, IONOS)`
4. **Visibility**: `Public` (pour que les autres puissent le cloner)
5. **Initialize this repository with**: ❌ Décocher (le repo existe déjà localement)
6. Cliquer **Create repository**

→ GitHub vous montre les commandes à exécuter

## Étape 2: Ajouter l'URL Distante et Pusher

Copier-coller ces commandes dans PowerShell:

```powershell
cd "c:\Users\bobes\Desktop\Projet Thouv"

# Ajouter le repo GitHub (remplacer USERNAME par votre username GitHub)
git remote add origin https://github.com/USERNAME/ThouvRun.git

# Renommer la branche en main (GitHub standard)
git branch -M main

# Pousser le code
git push -u origin main
```

### Détails:
- `USERNAME` = Votre username GitHub (ex: `bobes-dev`)
- Si authentification demandée:
  - **Option 1**: SSH keys (recommandé)
  - **Option 2**: Personal Access Token (plus simple pour commencer)

## Personal Access Token (Si Authentification Échoue)

Si `git push` échoue avec authentification:

1. Aller à https://github.com/settings/tokens/new
2. **Token name**: `ThouvRun-Push`
3. **Expiration**: `No expiration` (ou 90 jours)
4. **Scopes**: ✅ `repo` (Full control of private repositories)
5. Cliquer **Generate token**
6. **Copier le token** (vous ne pouvez le voir qu'une fois)

Puis modifier la commande:

```powershell
git remote set-url origin https://USERNAME:TOKEN@github.com/USERNAME/ThouvRun.git
git push -u origin main
```

Remplacer:
- `USERNAME` = Votre username GitHub
- `TOKEN` = Le token copié

## Étape 3: Vérifier sur GitHub

Aller à `https://github.com/USERNAME/ThouvRun`

Vous devriez voir:
- ✅ Tous les fichiers (api_server.py, src/, assets/, etc.)
- ✅ 81 files, X commits
- ✅ README.md affiché

## Étape 4: Configuration Domaine IONOS

Retour à IONOS pour pointer vers Render:

1. **Domaine**: `thouvrun.com` (déjà acheté)
2. **Manage Domains** → **DNS Settings**
3. Créer enregistrement **CNAME**:
   ```
   Name/Subdomain: (vide pour racine)
   Type: CNAME
   Value: thouvrun.onrender.com (URL Render)
   TTL: 3600
   ```
4. **Save**

⏳ Attendre 5-30 minutes (propagation DNS)

## Étape 5: Déployer sur Render

1. Aller à https://render.com
2. Sign up ou Login
3. **New** → **Web Service**
4. **Connect Repository**: Clonez de GitHub
   - Ou: Uploadez le code manuellement
5. Configuration:
   ```
   Name: thouvrun
   Runtime: Python 3
   Build command: pip install -r requirements.txt
   Start command: python api_server.py
   Region: Frankfurt (EU)
   ```
6. **Deploy**

⏳ Attendre 2-3 minutes

Render donne: `https://thouvrun.onrender.com` (URL provisoire)

## Étape 6: Connecter le Domaine IONOS à Render

1. Dans Render, allez à **Settings** de votre service
2. **Custom Domains**
3. Ajouter: `thouvrun.com`
4. Render donne instructions DNS
5. Configurer dans IONOS (étape 4)

## Étape 7: Tester!

```powershell
# Tester l'API:
curl https://thouvrun.com/health

# Voir le leaderboard:
# Ouvrir https://thouvrun.com dans le navigateur
```

✅ Tout fonctionne!

## Futurs Pushes (Après Modifications)

Quand vous modifiez le code localement:

```powershell
cd "c:\Users\bobes\Desktop\Projet Thouv"

git add .
git commit -m "Description de vos changements"
git push
```

Si vous avez déployé via GitHub (connecté à Render):
- Render redéploie **automatiquement** quand vous poussez!

---

## Résumé des URLs

| Service | URL |
|---------|-----|
| **Code Source** | `https://github.com/USERNAME/ThouvRun` |
| **Leaderboard Web** | `https://thouvrun.com` |
| **API Serveur** | `https://thouvrun.com/api/scores` |
| **Render Dashboard** | `https://dashboard.render.com` |

---

**C'est tout!** Votre repo est configuré et prêt! 🎉
