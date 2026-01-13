# 🚀 Guide Déploiement Render + IONOS

## Déploiement en 5 Minutes

### 1. Domaine IONOS (1€/an)

**Aller sur**: https://www.ionos.fr

1. Chercher un domaine (ex: `thouv-run.com`)
2. Ajouter au panier → payer
3. Aller à **Manage Domains** (gestion des domaines)
4. Sélectionner votre domaine
5. Aller à **DNS Settings** (Paramètres DNS)

On viendra modifier ici après Render.

### 2. Render.com (Gratuit)

**Aller sur**: https://render.com

#### 2.1 Créer un compte

- Sign up avec GitHub ou email
- Email de confirmation

#### 2.2 Déployer le serveur

1. **New +** → **Web Service**

2. Remplir les champs:
   - **Name**: `thouv-run` (ou votre choix)
   - **Region**: `Frankfurt (EU)` (ou proche de vous)
   - **Runtime**: `Python 3`
   - **Build command**: 
     ```
     pip install -r requirements.txt
     ```
   - **Start command**: 
     ```
     python api_server.py
     ```

3. Cliquer **Deploy Web Service**

4. Attendre ~2-3 minutes (il télécharge Python, pip install, lance le serveur)

5. ✅ Vous avez une URL: `https://thouv-run.onrender.com`

#### 2.3 Configurer le domaine personnalisé

1. Aller à **Settings** de votre service
2. Scroll jusqu'à **Custom Domain**
3. Ajouter votre domaine: `thouv-run.yourdomain.com` (ou juste `yourdomain.com`)
4. Cliquer **Add Custom Domain**
5. Render donne un message avec les enregistrements DNS à créer

### 3. Configuration DNS (IONOS)

Retour au **Manage Domains** IONOS:

1. Sélectionner votre domaine
2. **DNS Settings** → **DNS Records**
3. Créer un nouvel enregistrement `CNAME`:
   - **Name/Subdomain**: `thouv-run` (ou vide pour la racine)
   - **Type**: `CNAME`
   - **Value/Target**: `votre-app.onrender.com` (URL fournie par Render)
   - **TTL**: `3600` (défaut)
4. Cliquer **Save**

⏳ Attendre 5-30 minutes (propagation DNS)

### 4. Tester

Visitez: `https://thouv-run.yourdomain.com`

Vous devriez voir le leaderboard avec les scores! 🎉

### 5. Mettre à jour votre jeu

**Dans `src/gestion_scores.py`**:

```python
# Ligne ~11, changer:
API_SERVER_URL = "https://thouv-run.yourdomain.com/api/scores"
```

Relancer le jeu → les scores s'envoient au serveur central!

---

## Notes Importantes

⚠️ **Render gratuit s'arrête après 15 min d'inactivité**
- Solution: Visiter le site chaque jour ou peu avant de jouer
- Les scores sont sauvegardés en base de données, jamais perdu

⚠️ **Assurez-vous que `scores.html` existe** dans le dossier racine

⚠️ **Fichier `requirements.txt` doit contenir**:
```
Flask==3.0.0
Flask-CORS==4.0.0
requests==2.31.0
```

---

## Problèmes Courants

**DNS ne fonctionne pas?**
- Vérifier sur: https://mxtoolbox.com/ que le CNAME est propagé
- Attendre un peu plus longtemps

**Render dit "Build failed"?**
- Cliquer **Manual Deploy** dans les settings
- Vérifier que `requirements.txt` existe

**Scores ne s'envoient pas?**
- Vérifier que `API_SERVER_URL` est correct dans `gestion_scores.py`
- Vérifier que le serveur Render est en ligne (visit le site)

---

**C'est tout!** Votre leaderboard multi-joueur est live! 🚀
