import curses
import time
import os
import moteur_jeu
import tache_fond
from gestion_scores import (
    sauvegarder_dernier_joueur, 
    recuperer_dernier_joueur, 
    recuperer_top3_global, 
    recuperer_meilleurs_scores, # AJOUTÉ
    recuperer_dernieres_parties
)

# --- CONFIGURATION ---
TITRE_ASCII = [
    r" _______ _   _  ___   _   _ __      __   _____  _   _ _   _ ",
    r"|__   __| | | |/ _ \ | | | |\ \    / /  |  __ \| | | | \ | |",
    r"   | |  | |_| | | | || | | | \ \  / /   | |__) | | | |  \| |",
    r"   | |  |  _  | | | || | | |  \ \/ /    |  _  /| | | | . ` |",
    r"   | |  | | | | |_| || |_| |   \  /     | | \ \| |_| | |\  |",
    r"   |_|  |_| |_|\___/  \___/     \/      |_|  \_\\___/|_| \_|",
]

# --- FONCTIONS SYSTÈME ---
def silence(): pass
curses.beep = silence
curses.flash = silence

def safe_addstr(stdscr, y, x, text, max_y, max_x, attr=curses.A_NORMAL):
    try:
        if y < 0 or y >= max_y: return
        if x < 0:
            if -x >= len(text): return
            text = text[-x:]
            x = 0
        if x + len(text) > max_x:
            text = text[:max_x - x]
        if text:
            if y == max_y - 1 and x + len(text) >= max_x:
                text = text[:-1]
            stdscr.addstr(int(y), int(x), str(text), attr)
    except: pass

def centrer_texte(stdscr, y, texte, max_x, attr=curses.A_NORMAL):
    x = (max_x - len(texte)) // 2
    safe_addstr(stdscr, y, x, texte, 1000, max_x, attr)

def centrer_texte_multiligne(stdscr, y_depart, texte, max_y, max_x, attribut=curses.A_NORMAL):
    lignes = texte.split('\n')
    for i, ligne in enumerate(lignes):
        centrer_texte(stdscr, y_depart + i, ligne, max_x, attribut)
    return len(lignes)

def saisir_nom_manuel(stdscr, y, x, nom_defaut=""):
    curses.noecho()
    stdscr.nodelay(False)
    nom = nom_defaut
    LIMIT_CHAR = 15 
    run_saisie = True
    while run_saisie:
        stdscr.addstr(y - 2, x, "VOTRE BLASE :", curses.A_BOLD)
        
        stdscr.addstr(y, x, "_" * LIMIT_CHAR)
        stdscr.addstr(y, x, nom)
        if len(nom) < LIMIT_CHAR: stdscr.addstr(y, x + len(nom), "█")
        stdscr.refresh()
        ch = stdscr.getch()
        
        if ch == 27: # ECHAP
            stdscr.nodelay(True)
            return None

        if ch == 10 or ch == 13: 
            if len(nom) > 0: run_saisie = False
        elif ch == 8 or ch == 127 or ch == curses.KEY_BACKSPACE: nom = nom[:-1]
        elif 32 <= ch <= 126: 
            if len(nom) < LIMIT_CHAR: nom += chr(ch)
    stdscr.nodelay(True)
    return nom

def dessiner_entite(stdscr, entite, offset_y_sol, max_y, max_x):
    screen_y = offset_y_sol - int(entite.y) - entite.height
    screen_x = int(entite.x)
    char_art = entite.art
    if isinstance(char_art, list):
        for i, ligne in enumerate(char_art):
            safe_addstr(stdscr, screen_y + i, screen_x, ligne, max_y, max_x)
    else:
        safe_addstr(stdscr, screen_y, screen_x, str(char_art), max_y, max_x)

# --- SOUS-MENUS ---
def afficher_tuto(stdscr, h, w):
    stdscr.clear()
    stdscr.nodelay(False)
    centrer_texte(stdscr, 4, "COMMENT JOUER ?", w, curses.A_BOLD | curses.A_UNDERLINE)
    lignes = [
        "", "C'est le premier jour des cours et tu es en retard !",
        "Bastien va au CSND avec ses rollers et pendant sa route il doit esquiver voitures, camions et policiers",
        "sans oublier de prendre quelques bedos sur la route !", "",
        "--- COMMANDES ---", "",
        "SAUT COURT : [ESPACE] ou [FLECHE HAUT]",
        "> Ideal pour esquiver les VOITURES et les POLICIERS.",
        "CONSEIL : L'utiliser juste avant de toucher la voiture",
        "pour ne pas toucher le coffre !", "",
        "SAUT LONG  : [W] ou [Z]",
        "> Indispensable pour passer par dessus les CAMIONS.",
        "CONSEIL : Ce saut est tres long, l'utiliser bien avant",
        "de toucher le camion pour avoir le temps d'esquiver la suite !", "",
        "VOLUME : [+] et [-] (Clavier ou Pave Num)",
        "RESTART : [R] (quand Game Over)", "QUITTER : [ESC]", "",
        "Appuyez sur une touche pour revenir au menu..."
    ]
    y = 6
    for ligne in lignes:
        if y < h - 1:
            centrer_texte(stdscr, y, ligne, w)
            y += 1
    stdscr.getch()

def afficher_ecran_scores(stdscr, h, w):
    while True:
        stdscr.clear()
        stdscr.nodelay(False)
        centrer_texte(stdscr, 4, "TABLEAU DES SCORES", w, curses.A_BOLD)
        centrer_texte(stdscr, 7, "1. Meilleurs Scores", w) # MODIFIÉ
        centrer_texte(stdscr, 8, "2. Mon Historique", w)
        centrer_texte(stdscr, 10, "[ESC] Retour au menu", w)
        key = stdscr.getch()
        
        if key == 27: 
            break
            
        elif key == ord('1'):
            stdscr.clear()
            centrer_texte(stdscr, 2, "MEILLEURS SCORES", w, curses.A_BOLD)
            
            # En-têtes pour le Top 10
            header = "RANG | JOUEUR         | SCORE  | VERSION | DIFFICULTE"
            centrer_texte(stdscr, 5, header, w, curses.A_UNDERLINE)
            
            # Récupération du Top 10
            top10 = recuperer_meilleurs_scores(10)
            if not top10: top10 = recuperer_top3_global() # Fallback au cas où
            
            y = 7
            if not top10: 
                centrer_texte(stdscr, y, "Aucun score.", w)
            else:
                for i, s in enumerate(top10):
                    # Formatage des données
                    rg = f"{i+1}."
                    nm = s['nom'][:14] # Tronque le nom si trop long
                    sc = f"{s['score_total']} pts"
                    
                    vr = s.get('version', 'Console').replace("Version ", "")
                    if vr == "Graphique": vr = "Graph" 
                    if vr == "Console": vr = "Cons"
                    
                    df = s.get('difficulte', 'NORMALE')
                    
                    # Création de la ligne alignée
                    line = f"{rg:<5}| {nm:<15}| {sc:<7}| {vr:<8}| {df}"
                    centrer_texte(stdscr, y, line, w)
                    y += 1
                    
            centrer_texte(stdscr, h-3, "Touche pour retour...", w)
            stdscr.getch()
            
        elif key == ord('2'):
            nom = recuperer_dernier_joueur()
            stdscr.clear()
            if not nom: centrer_texte(stdscr, h//2, "Aucun joueur identifie.", w)
            else:
                centrer_texte(stdscr, 2, f"HISTORIQUE DE : {nom}", w, curses.A_BOLD)
                centrer_texte(stdscr, 4, "10 DERNIERES PARTIES :", w, curses.A_UNDERLINE)
                
                header = "SCORE  | DIST | BEDOS | VERSION |   DIFF   |    DATE"
                centrer_texte(stdscr, 6, header, w, curses.A_DIM)
                
                historique = recuperer_dernieres_parties(nom, 10)
                y = 8
                
                if not historique: 
                    centrer_texte(stdscr, y, "Aucune partie enregistrée.", w)
                else:
                    for s in historique:
                        sc = f"{s['score_total']} pts"
                        ds = f"{s['distance']}m"
                        bd = f"{s['bedos']}"
                        vr = s.get('version', 'Console').replace("Version ", "")
                        if vr == "Graphique": vr = "Graph" 
                        if vr == "Console": vr = "Cons"
                        
                        df = s.get('difficulte', 'NORMALE')
                        dt = s.get('date', '').split(' ')[0]
                        
                        line = f"{sc:<7}| {ds:<5}| {bd:<5} | {vr:<7} | {df:<8} | {dt}"
                        centrer_texte(stdscr, y, line, w)
                        y += 1
                        
            centrer_texte(stdscr, h-3, "Touche pour retour...", w)
            stdscr.getch()

def choisir_difficulte(stdscr, h, w):
    stdscr.nodelay(False)
    while True:
        stdscr.clear()
        centrer_texte(stdscr, h//2 - 3, "CHOISISSEZ LA DIFFICULTE", w, curses.A_BOLD)
        centrer_texte(stdscr, h//2 - 1, "1. NORMALE (Classique)", w)
        centrer_texte(stdscr, h//2, "2. DIFFICILE (Chaos total x1.5 points)", w)
        key = stdscr.getch()
        if key == ord('1'): return "NORMALE"
        elif key == ord('2'): return "DIFFICILE"
        elif key == 27: return None

# --- JEU PRINCIPAL ---
def lancer_le_jeu(stdscr, h, w, musique_thread):
    # 1. SETUP
    stdscr.clear()
    nom = saisir_nom_manuel(stdscr, h // 2, (w - 20) // 2, recuperer_dernier_joueur())
    
    if nom is None:
        return

    sauvegarder_dernier_joueur(nom)
    difficulte = choisir_difficulte(stdscr, h, w)
    if not difficulte: return
    
    stdscr.clear()
    SOL_ECRAN = h - 6
    jeu = moteur_jeu.Jeu(nom, version_jeu="Console", difficulte=difficulte)
    
    # --- MUSIQUE JEU ---
    musique_thread.demarrer_ambiance_jeu()

    stdscr.nodelay(True)
    running = True
    
    # LISTES CODES TOUCHES
    KEYS_PLUS = [ord('+'), 43, 339, 464, 520]
    KEYS_MINUS = [ord('-'), 45, 338, 465, 510]
    
    while running:
        # INPUT
        key = -1
        try:
            event = stdscr.getch()
            if event != curses.ERR:
                key = event
                curses.flushinp()
        except: pass

        # --- GESTION VOLUME ---
        if key in KEYS_PLUS: 
            musique_thread.changer_volume(0.1)
        elif key in KEYS_MINUS:
            musique_thread.changer_volume(-0.1)

        if jeu.running:
            if key == 27: running = False

            # Commandes de jeu
            if (key == ord(' ') or key == curses.KEY_UP) and not jeu.joueur.is_jumping:
                jeu.joueur.sauter_court()
                musique_thread.jouer_saut()
            elif (key in [ord('w'), ord('W'), ord('z'), ord('Z')]) and not jeu.joueur.is_jumping:
                jeu.joueur.sauter_long()
                musique_thread.jouer_saut()

            jeu.update()
            
            if jeu.bedo_collecte:
                musique_thread.jouer_bedo()
        
        # DESSIN
        stdscr.erase()
        
        hud_records = f"Global: {jeu.record_global} | Perso: {jeu.record_perso}"
        safe_addstr(stdscr, 0, w - len(hud_records) - 2, hud_records, h, w)
        
        # --- AFFICHE LE TITRE AVEC SCROLLING ---
        titre_zik = getattr(musique_thread, "titre_actuel", "")
        LARGEUR_MAX = 40
        if len(titre_zik) > LARGEUR_MAX:
            titre_complet = f"{titre_zik}     *** "
            offset = int(time.time() * 3) % len(titre_complet)
            texte_a_afficher = (titre_complet + titre_complet)[offset : offset + LARGEUR_MAX]
            safe_addstr(stdscr, 1, w - LARGEUR_MAX - 2, texte_a_afficher, h, w, curses.A_BOLD)
        else:
            safe_addstr(stdscr, 1, w - len(titre_zik) - 2, titre_zik, h, w, curses.A_BOLD)
        
        vol_pct = int(musique_thread.volume_global * 100)
        info_vol = f"Vol: {vol_pct}%"
        safe_addstr(stdscr, 2, w - len(info_vol) - 2, info_vol, h, w)

        safe_addstr(stdscr, SOL_ECRAN, 0, "_" * (w - 1), h, w)
        dessiner_entite(stdscr, jeu.joueur, SOL_ECRAN, h, w)
        for obs in jeu.obstacles: dessiner_entite(stdscr, obs, SOL_ECRAN, h, w)
        for bon in jeu.bonus: dessiner_entite(stdscr, bon, SOL_ECRAN, h, w)

        hud_score = f"Score: {int(jeu.score)} | Bedos: {jeu.bedos} | {jeu.nom_joueur}"
        safe_addstr(stdscr, 1, 2, hud_score, h, w)
        safe_addstr(stdscr, 2, 2, f"Mode: {difficulte}", h, w)

        if not jeu.running:
            if not getattr(jeu, "son_joue", False):
                if "arrete" in jeu.message_fin or "ACAB" in jeu.message_fin: 
                    musique_thread.jouer_police()
                else: 
                    musique_thread.jouer_crash()
                jeu.son_joue = True 
            
            y_c = h // 2 - 2
            nb_l = centrer_texte_multiligne(stdscr, y_c, f"GAME OVER: {jeu.message_fin}", h, w, curses.A_BOLD)
            y_nxt = y_c + nb_l + 1
            stats = f"Distance: {int(jeu.distance)}m | Bedos: {jeu.bedos}"
            centrer_texte(stdscr, y_nxt, stats, w)

            son_gameover_en_cours = False
            if musique_thread.sfx_gameover and musique_thread.sfx_gameover.get_num_channels() > 0:
                son_gameover_en_cours = True

            if musique_thread.mode_actuel == "GAMEOVER_FIN" and not son_gameover_en_cours:
                centrer_texte(stdscr, y_nxt + 2, "[R] Rejouer  ---  [ESC] Menu Principal", w, curses.A_BLINK)
                
                if key == ord('r') or key == ord('R'):
                    jeu = moteur_jeu.Jeu(nom, version_jeu="Console", difficulte=difficulte)
                    musique_thread.demarrer_ambiance_jeu()
                elif key == 27: # ESC
                    running = False
            
        stdscr.refresh()
        time.sleep(0.04)

# --- MENU PRINCIPAL ---
def menu_principal(stdscr):
    try: curses.curs_set(0)
    except: pass
    stdscr.keypad(True)
    
    musique_thread = tache_fond.GestionnaireMusique()
    musique_thread.start()
    musique_thread.demarrer_ambiance_menu()
    
    KEYS_PLUS = [ord('+'), 43, 339, 464, 520]
    KEYS_MINUS = [ord('-'), 45, 338, 465, 510]

    while True:
        stdscr.nodelay(False)
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        start_y_titre = 2
        for i, ligne in enumerate(TITRE_ASCII):
            centrer_texte(stdscr, start_y_titre + i, ligne, w, curses.A_BOLD)
            
        y_menu = start_y_titre + len(TITRE_ASCII) + 4
        centrer_texte(stdscr, y_menu,     "1. JOUER", w)
        centrer_texte(stdscr, y_menu + 2, "2. COMMENT JOUER ?", w)
        centrer_texte(stdscr, y_menu + 4, "3. SCORES", w)
        centrer_texte(stdscr, y_menu + 6, "4. QUITTER", w)
        
        vol_pct = int(musique_thread.volume_global * 100)
        centrer_texte(stdscr, h - 4, f"Volume: {vol_pct}% (+/-)", w)

        titre_menu = getattr(musique_thread, "titre_actuel", "")
        centrer_texte(stdscr, h - 5, titre_menu, w, curses.A_DIM)

        centrer_texte(stdscr, h - 2, "Projet Thouv'Run - © King Vernus 2026", w)
        
        key = stdscr.getch()
        
        if key in KEYS_PLUS: 
            musique_thread.changer_volume(0.1)
        elif key in KEYS_MINUS:
            musique_thread.changer_volume(-0.1)
        
        if key == ord('1'):
            lancer_le_jeu(stdscr, h, w, musique_thread)
            musique_thread.demarrer_ambiance_menu()
        elif key == ord('2'):
            afficher_tuto(stdscr, h, w)
        elif key == ord('3'):
            afficher_ecran_scores(stdscr, h, w)
        elif key == ord('4') or key == 27:
            break
            
    musique_thread.stop()

def main():
    """Point d'entrée principal pour la version terminal"""
    os.environ.setdefault('ESCDELAY', '25')
    try:
        curses.wrapper(menu_principal)
    except Exception as e:
        print("Erreur:", e)

if __name__ == "__main__":
    main()