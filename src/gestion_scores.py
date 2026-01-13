import json
import os
from datetime import datetime
import threading
import requests

# --- CHEMINS DES DONNÉES ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

FICHIER_SCORES = os.path.join(DATA_DIR, "thouv_scores.json")
FICHIER_DERNIER_JOUEUR = os.path.join(DATA_DIR, "last_player.txt")

# --- CONFIGURATION API ---
# Pour développement local
# API_SERVER_URL = "http://localhost:5000/api/scores"

# Pour production sur domaine personnalisé (configurer avant déploiement)
API_SERVER_URL = "https://thouvrun.com/api/scores"  # Domaine IONOS

API_ENABLED = True  # Set to False to disable API sync

def _envoyer_score_api(donnees_score):
    """
    Envoie le score à l'API REST en arrière-plan (thread)
    Cette fonction ne bloque jamais le jeu
    """
    if not API_ENABLED:
        return
    
    try:
        response = requests.post(
            API_SERVER_URL,
            json=donnees_score,
            timeout=5
        )
        # On log silencieusement - pas de blocage du jeu
        if response.status_code != 201 and response.status_code != 200:
            print(f"[API] Erreur lors de l'envoi du score: {response.status_code}")
    except requests.exceptions.ConnectionError:
        # API non disponible (serveur pas lancé) - c'est OK, on continue
        print("[API] Serveur API non disponible - scores sauvegardés localement")
    except Exception as e:
        # Erreur quelconque - on ignore silencieusement
        print(f"[API] Erreur: {e}")

def _telecharger_scores_api():
    """
    Télécharge tous les scores depuis le serveur API
    Retourne une liste de scores ou [] si erreur
    """
    if not API_ENABLED:
        return []
    
    try:
        # Utiliser l'URL GET /api/scores
        api_get_url = API_SERVER_URL.rsplit('/', 1)[0] + "/scores"
        response = requests.get(api_get_url, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[API] Erreur lors du téléchargement: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        print("[API] Serveur API non disponible - utilisation des scores locaux")
        return []
    except Exception as e:
        print(f"[API] Erreur lors du téléchargement: {e}")
        return []

def synchroniser_scores_depuis_serveur():
    """
    Synchronise les scores depuis le serveur distant
    Fusionne les scores locaux et distants (pas de doublons)
    """
    # Charger les scores locaux
    scores_locaux = charger_scores()
    
    # Télécharger les scores distants
    scores_distants = _telecharger_scores_api()
    
    if not scores_distants:
        return scores_locaux
    
    # Fusionner: ajouter les scores distants qui ne sont pas déjà locaux
    # (basé sur: même joueur, score, date)
    scores_fusionnes = scores_locaux.copy()
    
    for score_distant in scores_distants:
        # Vérifier si ce score existe déjà localement
        existe = False
        for score_local in scores_locaux:
            if (score_local.get('nom') == score_distant.get('nom') and
                score_local.get('score_total') == score_distant.get('score_total') and
                score_local.get('date') == score_distant.get('date')):
                existe = True
                break
        
        if not existe:
            scores_fusionnes.append(score_distant)
    
    # Sauvegarder les scores fusionnés localement
    if scores_distants:  # Seulement si on a reçu des données
        try:
            with open(FICHIER_SCORES, 'w', encoding='utf-8') as f:
                json.dump(scores_fusionnes, f, indent=4, ensure_ascii=False)
            print(f"[Sync] {len(scores_distants)} scores synchronisés")
        except Exception as e:
            print(f"[Sync] Erreur lors de la sauvegarde fusionnée: {e}")
    
    return scores_fusionnes

def charger_scores():
    if not os.path.exists(FICHIER_SCORES):
        return []
    try:
        with open(FICHIER_SCORES, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # On nettoie les données à la volée pour l'affichage
            return [_nettoyer_entree(s) for s in data]
    except:
        return []

def _nettoyer_entree(score_dict):
    """
    Sépare la difficulté de la version si elle est incluse dedans.
    Ex: "Console (DIFFICILE)" -> Version: "Console", Difficulte: "DIFFICILE"
    """
    s = score_dict.copy()
    raw_version = s.get('version', 'Inconnue')
    
    # Si la difficulté n'est pas déjà un champ à part entière
    if 'difficulte' not in s:
        if "(DIFFICILE)" in raw_version:
            s['difficulte'] = "DIFFICILE"
            s['version'] = raw_version.replace("(DIFFICILE)", "").strip()
        elif "(NORMALE)" in raw_version:
            s['difficulte'] = "NORMALE"
            s['version'] = raw_version.replace("(NORMALE)", "").strip()
        else:
            s['difficulte'] = "NORMALE" # Par défaut
            s['version'] = raw_version
            
    # Nettoyage cosmétique
    s['version'] = s['version'].replace("Version ", "").strip()
    
    return s

# --- FONCTIONS DE LECTURE ---

def recuperer_records(nom_joueur):
    """Renvoie (Record Global, Record Perso) pour le HUD."""
    scores = charger_scores()
    record_global = 0
    if scores:
        record_global = max(s.get('score_total', 0) for s in scores)
        
    record_perso = 0
    scores_joueur = [s.get('score_total', 0) for s in scores if s['nom'] == nom_joueur]
    if scores_joueur:
        record_perso = max(scores_joueur)
            
    return int(record_global), int(record_perso)

def recuperer_top3_global():
    """Renvoie les 3 meilleures parties."""
    scores = charger_scores()
    scores_tries = sorted(scores, key=lambda k: k.get('score_total', 0), reverse=True)
    return scores_tries[:3]

def recuperer_meilleurs_scores(limit=10):
    """Renvoie les N meilleures parties pour le tableau des scores."""
    scores = charger_scores()
    scores_tries = sorted(scores, key=lambda k: k.get('score_total', 0), reverse=True)
    return scores_tries[:limit]

def recuperer_historique_joueur(nom_joueur):
    """Renvoie tout l'historique trié par score."""
    scores = charger_scores()
    scores_perso = [s for s in scores if s['nom'] == nom_joueur]
    return sorted(scores_perso, key=lambda k: k.get('score_total', 0), reverse=True)

def recuperer_dernieres_parties(nom_joueur, limit=10):
    """Renvoie les N dernières parties jouées (Chronologique inverse)."""
    # On charge le fichier brut pour avoir l'ordre chronologique (si append)
    scores = charger_scores()
    scores_perso = [s for s in scores if s['nom'] == nom_joueur]
    # On inverse pour avoir les plus récents en premier
    return scores_perso[::-1][:limit]

# --- SAUVEGARDE ---

def sauvegarder_nouveau_score(nom_joueur, score_total, distance, bedos, version, difficulte=None):
    # On charge le fichier brut sans nettoyage pour la sauvegarde
    if os.path.exists(FICHIER_SCORES):
        try:
            with open(FICHIER_SCORES, 'r', encoding='utf-8') as f:
                scores = json.load(f)
        except: scores = []
    else:
        scores = []

    date_actuelle = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Si difficulte est fournie, on la sauvegarde à part, sinon on garde le comportement par défaut
    nouvelle_entree = {
        "nom": nom_joueur,
        "score_total": int(score_total),
        "distance": int(distance),
        "bedos": int(bedos),
        "version": version,
        "date": date_actuelle
    }
    
    if difficulte:
        nouvelle_entree["difficulte"] = difficulte

    scores.append(nouvelle_entree)

    # Sauvegarde locale (toujours)
    with open(FICHIER_SCORES, 'w', encoding='utf-8') as f:
        json.dump(scores, f, indent=4, ensure_ascii=False)
    
    # Envoi à l'API en arrière-plan (ne bloque pas le jeu)
    thread_api = threading.Thread(target=_envoyer_score_api, args=(nouvelle_entree,), daemon=True)
    thread_api.start()

# --- GESTION NOM ---
def sauvegarder_dernier_joueur(nom):
    try:
        with open(FICHIER_DERNIER_JOUEUR, 'w', encoding='utf-8') as f:
            f.write(nom)
    except: pass

def recuperer_dernier_joueur():
    if not os.path.exists(FICHIER_DERNIER_JOUEUR): return ""
    try:
        with open(FICHIER_DERNIER_JOUEUR, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except: return ""