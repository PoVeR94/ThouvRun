"""
THOUV'RUN - Serveur Central Multi-Joueur
Synchronise les scores de tous les joueurs en ligne

Architecture:
- Base de données SQLite (scores.db)
- Chaque joueur envoie son score au serveur
- Leaderboard web global à https://votre-domaine.com
- Téléchargement des scores pour tous les joueurs
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
DATABASE = os.environ.get('DATABASE_PATH', 'data/scores.db')
API_PORT = int(os.environ.get('PORT', 5000))

# Créer le dossier data s'il n'existe pas
os.makedirs('data', exist_ok=True)

def init_db():
    """Initialiser la base de données"""
    if not os.path.exists(DATABASE):
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

def get_db():
    """Retourner une connexion à la base de données"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

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
        if os.path.exists('scores.html'):
            with open('scores.html', 'r', encoding='utf-8') as f:
                return f.read(), 200, {'Content-Type': 'text/html; charset=utf-8'}
        else:
            return "scores.html non trouvé", 404
    except Exception as e:
        return f"Erreur: {str(e)}", 500

@app.route('/health', methods=['GET'])
def health():
    """Vérifier que le serveur est actif"""
    return jsonify({'status': 'online', 'timestamp': datetime.now().isoformat()}), 200

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
