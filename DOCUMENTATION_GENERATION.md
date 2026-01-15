# Thouv'Run - Documentation Technique

## 📄 Fichiers Inclus

### 1. **Thouv-Run_Report.tex** (LaTeX)
Document complet présentant le projet Thouv'Run :
- **Présentation** : Concept, objectifs, caractéristiques
- **Gameplay** : Contrôles, mécanique, système de score
- **Architecture** : Structure du projet, stack technologique, classes
- **Choix de Conception** : Justifications techniques
- **Processus de Développement** : Phases, itérations, bug fixes
- **Résultats** : Métriques, performances, uptime
- **Avenir** : Améliorations futures

### 2. **Thouv-Run_ClassDiagram.puml** (PlantUML)
Diagramme de classes montrant :
- Hiérarchie des entités (Entite → Thouverez)
- Classe moteur Jeu (logique pure)
- Système de gestion des scores
- Gestionnaire musique (threading)
- Interfaces UI (Pygame + Terminal)
- API serveur et Leaderboard
- Relations et responsabilités

### 3. **Thouv-Run_SequenceDiagram.puml** (PlantUML)
Diagramme de séquence illustrant :
- Flux complet de sauvegarde d'un score
- Asynchrone (threads) vs synchrone
- Synchronisation backup local + serveur
- Actualisation leaderboard web
- Garanties zéro perte données

---

## 🛠️ Comment Générer les Fichiers

### A) Générer le PDF à partir de LaTeX

#### Méthode 1 : Avec MiKTeX (Windows)
```bash
# Installer MiKTeX : https://miktex.org/download
# Puis dans le dossier du projet :
pdflatex -interaction=nonstopmode Thouv-Run_Report.tex
```

#### Méthode 2 : Avec Overleaf (En ligne)
1. Aller sur https://www.overleaf.com/
2. Créer un nouveau projet
3. Copier le contenu de `Thouv-Run_Report.tex`
4. Compiler en PDF directement

#### Méthode 3 : Avec Docker (Linux/Mac)
```bash
docker run --rm -v $(pwd):/data docker.io/blang/latex latexmk -pdf Thouv-Run_Report.tex
```

**Résultat** : `Thouv-Run_Report.pdf` (8-10 pages)

---

### B) Générer les Diagrammes PlantUML

#### Méthode 1 : PlantUML Online
1. Aller sur https://www.plantuml.com/plantuml/uml/
2. Copier le contenu de `Thouv-Run_ClassDiagram.puml`
3. Générer PNG/SVG directement dans le navigateur

#### Méthode 2 : Avec PlantUML CLI (Windows/Mac/Linux)
```bash
# Installer PlantUML :
# https://plantuml.com/download

# Générer images :
java -jar plantuml.jar Thouv-Run_ClassDiagram.puml
java -jar plantuml.jar Thouv-Run_SequenceDiagram.puml
```

**Résultats** :
- `Thouv-Run_ClassDiagram.png` (1 image)
- `Thouv-Run_SequenceDiagram.png` (1 image)

#### Méthode 3 : Avec VS Code Extension
1. Installer l'extension **PlantUML** de jgraph
2. Ouvrir les fichiers `.puml`
3. Preview avec `Alt + D`
4. Exporter en PNG via interface

---

## 📊 Contenu des Diagrammes

### Diagramme de Classes
```
Entite (classe parent)
├── Thouverez (joueur)
├── Entité (obstacles/bonus)

Jeu (moteur)
├── uses Entite (joueur + obstacles + bonus)
├── uses GestionScores
└── uses GestionnaireMusique

UIGraphique / UITerminal
├── uses Jeu
└── uses GestionnaireMusique

APIServeur
├── POST /api/scores
├── GET /api/scores
└── syncs with GestionScores

Leaderboard (Web)
└── fetches from APIServeur
```

### Diagramme de Séquence
1. **Fin de partie** → Sauvegarde locale (JSON)
2. **Thread API** → POST le score au serveur (asynchrone)
3. **Thread Backup** → GET tous les scores du serveur
4. **Fusion** → Local + Serveur sans doublons
5. **Leaderboard Web** → Actualisation toutes les 10s

---

## 🎯 Points Clés du Rapport

### Architecture
- **Modularité** : Logique de jeu ≠ Présentation
- **Testabilité** : Classes indépendantes, faciles à mocker
- **Évolutivité** : Ajouter nouvelles interfaces sans modifier moteur

### Synchronisation
- **Triple couche** : Local (JSON) → Serveur (API) → Web (HTML)
- **Résilience** : Perte serveur ≠ perte données (backup Git)
- **Non-bloquant** : Tout en threads → UI fluide

### Choix Techniques
- **Python** : Rapidité dev + écosystème riche
- **JSON** : Zéro dépendance, versionnage naturel
- **Flask** : Léger, suffisant pour leaderboard
- **Railway** : Déploiement simple, HTTPS auto

### Processus Itératif
- **8 itérations** animation weeds → apprentissage CSS
- **5 responsives** breakpoints → accessibilité maximale
- **Zéro perte données** → 3 synchronisations parallèles

---

## 📝 Licence

MIT License - Tu peux utiliser ce rapport comme base pour :
- Mémoires d'école
- Portfolios de développement
- Documentations de projets perso
- Présentations académiques

---

## 🔗 Ressources Utiles

- **LaTeX Documentation** : https://www.overleaf.com/learn
- **PlantUML Guide** : https://plantuml.com/guide
- **MiKTeX** : https://miktex.org/
- **Overleaf** : https://www.overleaf.com/
- **PlantUML Online** : https://www.plantuml.com/plantuml/uml/

---

**Généré pour Thouv'Run le 15 Janvier 2026**
