#!/usr/bin/env python3
"""
Synchronise les scores avec le serveur AVANT de faire git push
Cela garantit que les scores perdus lors du déploiement sont récupérés
"""

import sys
sys.path.insert(0, 'src')

from gestion_scores import _synchroniser_backup_depuis_serveur, charger_scores
import time

print("=" * 60)
print("SYNCHRONISATION PRE-PUSH")
print("=" * 60)
print()

print("[*] Synchronisation des scores avec le serveur...")
print("    (Cela va telecharger les derniers scores depuis Railway)")
print()

# Attendre un peu pour que le serveur réponde
time.sleep(1)

# Synchroniser
_synchroniser_backup_depuis_serveur()

# Afficher le nombre de scores
scores = charger_scores()
print()
print(f"[OK] {len(scores)} scores dans thouv_scores.json")
print()
print("Maintenant tu peux faire:")
print("  git add data/thouv_scores.json")
print("  git commit -m 'Update scores from server'")
print("  git push")
print()
