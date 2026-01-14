"""
THOUV'RUN - Serveur Central Multi-Joueur avec Stockage Persistant
Synchronise les scores de tous les joueurs en ligne

Architecture:
- Base de données SQLite (scores.db)
- Fichier JSON de sauvegarde (data/server_scores.json) - sauvegarde persistante
- Chaque joueur envoie son score au serveur
- Leaderboard web global à https://votre-domaine.com
- Téléchargement des scores pour tous les joueurs
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import json
from datetime import datetime
import threading

app = Flask(__name__, static_folder='../assets', static_url_path='/assets')
CORS(app)

# Configuration
DATABASE = os.environ.get('DATABASE_PATH', os.path.join(os.path.dirname(__file__), '..', 'data', 'scores.db'))
SCORES_BACKUP = os.environ.get('BACKUP_PATH', os.path.join(os.path.dirname(__file__), '..', 'data', 'server_scores.json'))
API_PORT = int(os.environ.get('PORT', 5000))

# Debug: afficher les chemins
print(f"[Config] DATABASE: {DATABASE}")
print(f"[Config] BACKUP: {SCORES_BACKUP}")
print(f"[Config] BACKUP EXISTS: {os.path.exists(SCORES_BACKUP)}")

# Créer le dossier data s'il n'existe pas
os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

def init_db():
    """Initialiser la base de données"""
    db_exists = os.path.exists(DATABASE)
    
    if not db_exists:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                score_total INTEGER NOT NULL,
                distance INTEGER NOT NULL,
                bedos INTEGER NOT NULL,
                version TEXT NOT NULL,
                difficulte TEXT DEFAULT 'NORMALE',
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    # Charger la sauvegarde si elle existe (toujours, même si DB existe)
    load_from_backup()
    
    # Nettoyer les doublons qui pourraient rester
    remove_duplicates()

def load_from_backup():
    """Charger les scores depuis la sauvegarde JSON - force reload on startup"""
    if os.path.exists(SCORES_BACKUP):
        try:
            with open(SCORES_BACKUP, 'r', encoding='utf-8') as f:
                backup_scores = json.load(f)
            
            if backup_scores:
                conn = sqlite3.connect(DATABASE)
                c = conn.cursor()
                
                # TOUJOURS vider et recharger le backup au démarrage
                # Cela garantit que Railway a toujours les scores corrects
                c.execute('DELETE FROM scores')
                
                for score in backup_scores:
                    c.execute('''
                        INSERT INTO scores (nom, score_total, distance, bedos, version, difficulte, date)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        score.get('nom'),
                        int(score.get('score_total', 0)),
                        int(score.get('distance', 0)),
                        int(score.get('bedos', 0)),
                        score.get('version', ''),
                        score.get('difficulte', 'NORMALE'),
                        score.get('date', datetime.now().strftime("%d/%m/%Y %H:%M"))
                    ))
                
                conn.commit()
                print(f"[Init] {len(backup_scores)} scores reloadés depuis le backup (all previous deleted)")
                conn.close()
        except Exception as e:
            print(f"[Init] Erreur lors du chargement de la sauvegarde: {e}")

def remove_duplicates():
    """Nettoie les doublons exacts de la BD"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        # Trouver et supprimer les doublons
        c.execute('''
            DELETE FROM scores WHERE rowid NOT IN (
                SELECT MIN(rowid) FROM scores
                GROUP BY nom, score_total, distance, bedos, version, difficulte, date
            )
        ''')
        
        deleted = c.rowcount
        if deleted > 0:
            print(f"[Init] {deleted} doublons supprimés")
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Init] Erreur lors du nettoyage des doublons: {e}")

def save_to_backup():
    """Sauvegarder les scores dans un fichier JSON pour persistance"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT nom, score_total, distance, bedos, version, difficulte, date FROM scores')
        rows = c.fetchall()
        conn.close()
        
        # Convertir en dictionnaire
        scores = []
        for row in rows:
            scores.append({
                'nom': row[0],
                'score_total': row[1],
                'distance': row[2],
                'bedos': row[3],
                'version': row[4],
                'difficulte': row[5],
                'date': row[6]
            })
        
        with open(SCORES_BACKUP, 'w', encoding='utf-8') as f:
            json.dump(scores, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Backup] Erreur: {e}")

def get_db():
    """Retourner une connexion à la base de données"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Servir les fichiers statiques (images, etc)"""
    return send_from_directory('../assets', filename)

@app.route('/api/scores', methods=['GET'])
def get_scores():
    """Récupère tous les scores (pour le leaderboard web)"""
    try:
        limit = request.args.get('limit', 500, type=int)  # Augmenté à 500 (pour supporter 500+ scores)
        offset = request.args.get('offset', 0, type=int)
        
        conn = get_db()
        c = conn.cursor()
        
        # Récupérer les scores triés par score_total descending
        c.execute('''
            SELECT nom, score_total, distance, bedos, version, difficulte, date 
            FROM scores 
            ORDER BY score_total DESC 
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        scores = [dict(row) for row in c.fetchall()]
        conn.close()
        
        return jsonify(scores), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scores', methods=['POST'])
def add_score():
    """Ajoute un nouveau score"""
    try:
        data = request.json
        
        # Validation
        required = ['nom', 'score_total', 'distance', 'bedos', 'version']
        if not all(k in data for k in required):
            return jsonify({'error': 'Données manquantes'}), 400
        
        if len(data['nom']) < 2 or len(data['nom']) > 50:
            return jsonify({'error': 'Nom invalide (2-50 caractères)'}), 400
        
        conn = get_db()
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO scores (nom, score_total, distance, bedos, version, difficulte, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['nom'],
            int(data['score_total']),
            int(data['distance']),
            int(data['bedos']),
            data['version'],
            data.get('difficulte', 'NORMALE'),
            data.get('date', datetime.now().strftime("%d/%m/%Y %H:%M"))
        ))
        
        conn.commit()
        conn.close()
        
        # Sauvegarder le backup après chaque nouveau score
        save_to_backup()
        
        return jsonify({'message': 'Score enregistré'}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Récupère les statistiques globales"""
    try:
        conn = get_db()
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*) as total FROM scores')
        total_games = c.fetchone()['total']
        
        c.execute('SELECT MAX(score_total) as best FROM scores')
        best_score = c.fetchone()['best'] or 0
        
        c.execute('SELECT COUNT(DISTINCT nom) as count FROM scores')
        player_count = c.fetchone()['count']
        
        c.execute('SELECT AVG(score_total) as avg FROM scores')
        average_score = c.fetchone()['avg'] or 0
        
        conn.close()
        
        return jsonify({
            'total_games': total_games,
            'best_score': int(best_score),
            'player_count': player_count,
            'average_score': int(average_score)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/player/<nom>', methods=['GET'])
def get_player_stats(nom):
    """Récupère les statistiques d'un joueur"""
    try:
        conn = get_db()
        c = conn.cursor()
        
        c.execute('''
            SELECT nom, score_total, distance, bedos, version, difficulte, date
            FROM scores
            WHERE nom = ?
            ORDER BY score_total DESC
        ''', (nom,))
        
        scores = [dict(row) for row in c.fetchall()]
        
        if not scores:
            return jsonify({'error': 'Joueur non trouvé'}), 404
        
        c.execute('''
            SELECT 
                COUNT(*) as total_games,
                MAX(score_total) as best_score,
                AVG(score_total) as average_score
            FROM scores
            WHERE nom = ?
        ''', (nom,))
        
        stats = dict(c.fetchone())
        conn.close()
        
        return jsonify({
            'nom': nom,
            'total_games': stats['total_games'],
            'best_score': int(stats['best_score']),
            'average_score': int(stats['average_score']),
            'scores': scores
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
@app.route('/scores.html', methods=['GET'])
def serve_leaderboard():
    """Sert la page HTML du leaderboard"""
    try:
        leaderboard_path = os.path.join(os.path.dirname(__file__), '..', 'web', 'scores.html')
        if os.path.exists(leaderboard_path):
            with open(leaderboard_path, 'r', encoding='utf-8') as f:
                return f.read(), 200, {'Content-Type': 'text/html; charset=utf-8'}
        else:
            return "scores.html non trouvé", 404
    except Exception as e:
        return f"Erreur: {str(e)}", 500

@app.route('/health', methods=['GET'])
def health():
    """Vérifier que le serveur est actif"""
    return jsonify({'status': 'online', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/admin/clean', methods=['POST'])
def admin_clean():
    """Endpoint d'admin pour nettoyer les doublons (non documenté)"""
    try:
        removed = 0
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        # Supprimer les doublons
        c.execute('''
            DELETE FROM scores WHERE rowid NOT IN (
                SELECT MIN(rowid) FROM scores
                GROUP BY nom, score_total, distance, bedos, version, difficulte, date
            )
        ''')
        
        removed = c.rowcount
        conn.commit()
        conn.close()
        
        return jsonify({'message': f'{removed} doublons supprimés'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialiser la base de données au démarrage
    init_db()
    
    print("=" * 60)
    print("🎮 Serveur Multi-Joueur Thouv'Run")
    print("=" * 60)
    print(f"📊 Leaderboard: http://localhost:5000/scores.html")
    print(f"🔧 API Health: http://localhost:5000/health")
    print(f"📈 Stats Globales: http://localhost:5000/api/stats")
    print("=" * 60)
    print("Note: Sur Render, le serveur écoute sur 0.0.0.0:PORT")
    print("=" * 60)
    
    # Pour développement local
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=False  # À mettre à True pour développement
    )
