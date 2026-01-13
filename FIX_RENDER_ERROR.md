# 🔧 Fix Render Deploy - windows-curses Error

## ❌ Problème

Render (serveur Linux) ne peut pas installer `windows-curses` car c'est une dépendance **Windows only**.

```
ERROR: Could not find a version that satisfies the requirement windows-curses==2.4.1
ERROR: No matching distribution found for windows-curses==2.4.1
```

---

## ✅ Solution Appliquée

### Fichiers Créés:

1. **requirements.txt** (pour Render - Production)
   ```
   flask==3.0.0
   flask-cors==4.0.0
   requests==2.31.0
   ```
   ✅ Sans pygame ni windows-curses (pas nécessaires pour l'API)

2. **requirements-dev.txt** (pour votre PC - Développement)
   ```
   pygame==2.6.1
   windows-curses==2.4.1
   flask==3.0.0
   flask-cors==4.0.0
   requests==2.31.0
   ```
   ✅ Avec toutes les dépendances pour jouer localement

---

## 🚀 Prochaine Étape

### Pour Render:
1. Aller à votre service Render: https://dashboard.render.com
2. Cliquer **Manual Deploy** pour redéployer
3. Attendre 2-3 minutes
4. Vérifier les logs → Aucune erreur cette fois! ✅

### Pour Développement Local:
```powershell
# Installer les dépendances de développement
pip install -r requirements-dev.txt

# Jouer localement
python src/main_graphique.py
```

---

## 📊 Résumé

| Fichier | Usage | Contenu |
|---------|-------|---------|
| `requirements.txt` | Render (serveur) | Flask, CORS, Requests |
| `requirements-dev.txt` | Votre PC | + Pygame + windows-curses |

---

**Status**: ✅ Code poussé sur GitHub → Render va redéployer automatiquement! 🎉
