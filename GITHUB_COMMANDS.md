# 📋 Commandes GitHub - Copier-Coller

## 1️⃣ Créer le Repo sur GitHub

Allez à: https://github.com/new

```
Repository name: ThouvRun
Description: Multi-player platformer game with online leaderboard
Visibility: Public
Initialize: ❌ (décocher)
```

Cliquer **Create repository**

---

## 2️⃣ Pousser le Code (Copy-Paste Complet)

```powershell
cd "c:\Users\bobes\Desktop\Projet Thouv"

# Remplacer USERNAME par votre username GitHub (ex: bobes-dev)
git remote add origin https://github.com/USERNAME/ThouvRun.git

git branch -M main

git push -u origin main
```

**Vous serez demandé vos identifiants GitHub:**
- Si SSH: configuré automatiquement
- Si HTTPS: username + token personnel (voir GITHUB_SETUP.md)

---

## 3️⃣ Après Modifications (Push Futur)

```powershell
cd "c:\Users\bobes\Desktop\Projet Thouv"

git add .

git commit -m "Description de vos changements"

git push
```

---

## 📊 État Actuel

```
📁 ThouvRun (repo local)
├── ✅ Git initialisé
├── ✅ Initial commit (81 files)
├── ✅ Prêt à pusher sur GitHub
└── ✅ Domaine: thouvrun.com configuré
```

---

## 🔗 Liens Importants

- GitHub: https://github.com (créer repo)
- Render: https://render.com (déploiement)
- IONOS: https://www.ionos.fr (domaine déjà acheté)
- Guide complet: [GITHUB_SETUP.md](GITHUB_SETUP.md)

---

**Prêt!** Créez le repo GitHub et lancez `git push`! 🚀
