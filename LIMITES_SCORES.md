# 🎮 Augmenter la Limite de Scores

## 📊 Limite Actuelle

- **Limite API**: 500 scores par défaut (configurable)
- **Base de données**: **ILLIMITÉE** (pas de limite SQLite)
- **Leaderboard web**: Demande 500 scores max

## ⚙️ Comment Augmenter la Limite?

### Option 1: Augmenter via la Page Web

**Fichier**: `scores.html` (ligne ~376)

```javascript
// Actuellement:
const response = await fetch('/api/scores?limit=500');

// Pour augmenter à 1000:
const response = await fetch('/api/scores?limit=1000');
```

### Option 2: Augmenter la Limite API

**Fichier**: `api_server.py` (ligne ~54)

```python
# Actuellement:
limit = request.args.get('limit', 500, type=int)

# Pour augmenter le défaut à 1000:
limit = request.args.get('limit', 1000, type=int)
```

### Option 3: URL Dynamique (Avancé)

Vous pouvez aussi ajouter un sélecteur sur la page web:

```html
<select id="limitSelector" onchange="changeLimit()">
    <option value="50">Top 50</option>
    <option value="100">Top 100</option>
    <option value="500" selected>Top 500</option>
    <option value="1000">Tous (1000+)</option>
</select>

<script>
function changeLimit() {
    const limit = document.getElementById('limitSelector').value;
    fetch(`/api/scores?limit=${limit}`)
        .then(r => r.json())
        .then(data => displayScores(data));
}
</script>
```

## 🗄️ Base de Données SQLite

SQLite **n'a pas de limite théorique** pour le nombre de lignes:
- Une base SQLite peut stocker des **milliards de lignes**
- Limite pratique: espace disque disponible
- Performance: reste bon jusqu'à plusieurs millions

## 💾 Espace Disque

Chaque score enregistré occupe environ **~150 bytes**:

| Nombre de scores | Taille approx |
|---|---|
| 100 | 15 KB |
| 1,000 | 150 KB |
| 10,000 | 1.5 MB |
| 100,000 | 15 MB |
| 1,000,000 | 150 MB |

## ⚡ Performance

### Query Times (sur 500 scores)
```
SELECT * FROM scores ORDER BY score_total DESC LIMIT 500
→ ~5-10ms ⚡
```

### Avec 100,000 scores
```
→ ~20-50ms (acceptable)
```

### Avec 1,000,000 scores
```
→ ~100-200ms (peut nécessiter une optimisation)
```

## 🔧 Optimisation pour Grand Volume

Si vous avez **100,000+ scores**, ajoutez un **index**:

**SQL**:
```sql
CREATE INDEX idx_score_total ON scores(score_total DESC);
```

**Via API** (ajoutez dans `api_server.py`):
```python
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        # ... table creation ...
        c.execute('CREATE INDEX idx_score_total ON scores(score_total DESC)')
        conn.commit()
        conn.close()
```

## 📈 Recommandations

### Pour 1-500 joueurs
✅ Limite actuelle (500) est **parfaite**

### Pour 500-5000 joueurs
⚠️ Augmentez à **1000-2000**

### Pour 5000+ joueurs
⚠️ Considérez:
- Pagination (50 par page)
- Cache des données
- Index sur la base de données
- Réplication de la BD

## 🌐 Cas d'Usage

### Petit Jeu (Amis/LAN)
```
100-500 scores → Limite 500 ✅
```

### Jeu Indie
```
500-5000 scores → Limite 1000 ✅
```

### Jeu Populaire
```
5000+ scores → Limite ILLIMITÉE + Pagination ✅
```

## 📝 Résumé

- **Actuellement**: Affiche jusqu'à **500 scores**
- **Maximum**: **Illimité** (base de données)
- **Recommandation**: Gardez la limite à 500 pour les perfs
- **Alternative**: Ajouter pagination si vous avez beaucoup de scores

---

*Dernière mise à jour: 14 Janvier 2026*
