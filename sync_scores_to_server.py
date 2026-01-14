#!/usr/bin/env python3
"""
Script pour synchroniser TOUS les scores locaux vers le serveur
Utilisation: python sync_scores_to_server.py
"""

import json
import os
import sys
import requests
import time

# Chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FICHIER_SCORES = os.path.join(DATA_DIR, "thouv_scores.json")

# Configuration
API_SERVER_URL = "https://thouvrun.onrender.com/api/scores"

def charger_scores_locaux():
    """Charge tous les scores du fichier JSON local"""
    if not os.path.exists(FICHIER_SCORES):
        print(f"❌ Fichier non trouvé: {FICHIER_SCORES}")
        return []
    
    try:
        with open(FICHIER_SCORES, 'r', encoding='utf-8') as f:
            scores = json.load(f)
            print(f"✅ {len(scores)} scores chargés localement")
            return scores
    except Exception as e:
        print(f"❌ Erreur lors de la lecture: {e}")
        return []

def envoyer_tous_les_scores(scores):
    """Envoie TOUS les scores au serveur (synchrone, pas de thread)"""
    if not scores:
        print("❌ Aucun score à envoyer")
        return 0
    
    reussis = 0
    echoues = 0
    
    print(f"\n🚀 Envoi de {len(scores)} scores au serveur...")
    print(f"API: {API_SERVER_URL}\n")
    
    for i, score in enumerate(scores, 1):
        try:
            response = requests.post(
                API_SERVER_URL,
                json=score,
                timeout=5
            )
            
            if response.status_code in [200, 201]:
                reussis += 1
                print(f"  [{i}/{len(scores)}] ✅ {score['nom']:<15} - {score['score_total']:>3} pts")
            else:
                echoues += 1
                print(f"  [{i}/{len(scores)}] ❌ {score['nom']:<15} - Code {response.status_code}")
        
        except requests.exceptions.Timeout:
            echoues += 1
            print(f"  [{i}/{len(scores)}] ❌ {score['nom']:<15} - Timeout")
        
        except Exception as e:
            echoues += 1
            print(f"  [{i}/{len(scores)}] ❌ {score['nom']:<15} - {str(e)[:40]}")
        
        # Petit délai pour ne pas surcharger l'API
        if i % 10 == 0:
            time.sleep(0.1)
    
    print(f"\n📊 Résultat:")
    print(f"   ✅ Réussis: {reussis}")
    print(f"   ❌ Échoués: {echoues}")
    print(f"   📈 Total: {reussis + echoues}")
    
    return reussis

def main():
    print("=" * 60)
    print(" SYNCHRONISATION DES SCORES VERS LE SERVEUR")
    print("=" * 60)
    
    # Charger les scores locaux
    scores = charger_scores_locaux()
    
    if not scores:
        print("Aucun score à envoyer.")
        return
    
    # Envoyer vers le serveur
    reussis = envoyer_tous_les_scores(scores)
    
    # Vérifier le résultat
    print("\n🔍 Vérification du serveur...")
    try:
        r = requests.get('https://thouvrun.onrender.com/api/scores', timeout=10)
        scores_serveur = r.json()
        print(f"✅ Scores sur le serveur: {len(scores_serveur)} entrées")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    main()
