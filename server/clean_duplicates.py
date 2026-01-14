"""
Script de nettoyage: Supprime les doublons exacts de la BD
Doit être exécuté sur Railway avec SSH ou localement
"""

import sqlite3
import os

DATABASE = '../data/scores.db'

def clean_duplicates():
    """Supprime les doublons exacts (même nom + score + date)"""
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Trouver les doublons
    c.execute('''
        SELECT nom, score_total, distance, bedos, version, difficulte, date, COUNT(*) as count
        FROM scores
        GROUP BY nom, score_total, distance, bedos, version, difficulte, date
        HAVING count > 1
    ''')
    
    doublons = c.fetchall()
    
    if not doublons:
        print("✓ Pas de doublons trouvés!")
        conn.close()
        return
    
    print(f"❌ {len(doublons)} groupes de doublons détectés!\n")
    
    total_deleted = 0
    
    for nom, score, distance, bedos, version, diff, date, count in doublons:
        print(f"  {count}x: {nom} | {score} pts | {date}")
        
        # Garder 1, supprimer les autres
        c.execute('''
            DELETE FROM scores WHERE rowid NOT IN (
                SELECT MIN(rowid) FROM scores 
                WHERE nom=? AND score_total=? AND distance=? AND bedos=? AND version=? AND difficulte=? AND date=?
            )
            AND nom=? AND score_total=? AND distance=? AND bedos=? AND version=? AND difficulte=? AND date=?
        ''', (nom, score, distance, bedos, version, diff, date, 
              nom, score, distance, bedos, version, diff, date))
        
        deleted = c.rowcount
        total_deleted += deleted
        print(f"    → {deleted} supprimé(s)")
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Nettoyage terminé: {total_deleted} scores supprimés!")

if __name__ == '__main__':
    clean_duplicates()
