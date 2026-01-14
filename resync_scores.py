#!/usr/bin/env python3
"""
Script de re-synchronisation: Envoie tous les scores locaux vers le serveur Railway.
À exécuter une seule fois après la refonte de l'architecture.
"""

import json
import requests
import sys
import time
from pathlib import Path

# Configuration
API_URL = "https://thouvrun-production.up.railway.app/api/scores"
FICHIER_SCORES = Path(__file__).parent / "data" / "thouv_scores.json"

def resync_all_scores():
    """Charge tous les scores locaux et les envoie vers le serveur."""
    
    # Charger les scores locaux
    if not FICHIER_SCORES.exists():
        print(f"❌ Fichier de scores non trouvé: {FICHIER_SCORES}")
        return False
    
    try:
        with open(FICHIER_SCORES, 'r', encoding='utf-8') as f:
            scores = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lecture scores: {e}")
        return False
    
    if not scores:
        print("❌ Aucun score à synchroniser")
        return False
    
    print(f"📊 {len(scores)} scores trouvés localement")
    print(f"🚀 Envoi vers {API_URL}...")
    print("-" * 60)
    
    sent = 0
    errors = 0
    
    for i, score in enumerate(scores, 1):
        try:
            # Chaque requête a son propre try/except et timeout court
            response = requests.post(
                API_URL,
                json=score,
                timeout=0.3
            )
            
            if response.status_code in [200, 201]:
                sent += 1
            else:
                errors += 1
        
        except requests.exceptions.Timeout:
            errors += 1
        except requests.exceptions.ConnectionError:
            errors += 1
        except Exception:
            errors += 1
        
        # Progress et délai petit pour laisser l'API respirer
        if i % 25 == 0:
            print(f"✓ {i}/{len(scores)} ({sent} OK, {errors} KO)")
            time.sleep(0.05)  # 50ms délai entre batches
    
    print("-" * 60)
    print(f"✅ Synchronisation terminée!")
    print(f"   Envoyés: {sent}/{len(scores)}")
    print(f"   Erreurs: {errors}")
    if len(scores) > 0:
        print(f"   Taux réussite: {sent*100//len(scores)}%")
    
    return sent > 0

if __name__ == "__main__":
    success = resync_all_scores()
    sys.exit(0 if success else 1)
