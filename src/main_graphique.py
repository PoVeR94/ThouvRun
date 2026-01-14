import pygame
import time
import os
import math
import webbrowser
import moteur_jeu
import tache_fond
from gestion_scores import (
    sauvegarder_dernier_joueur, 
    recuperer_dernier_joueur,
    recuperer_top3_global, 
    recuperer_meilleurs_scores,
    recuperer_dernieres_parties,
    synchroniser_scores_au_demarrage
)

# --- CHEMINS DES ASSETS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

def asset_path(asset_type, filename):
    """Construit le chemin complet vers un asset."""
    if asset_type == "image":
        return os.path.join(IMAGES_DIR, filename)
    elif asset_type == "sound":
        return os.path.join(SOUNDS_DIR, filename)
    elif asset_type == "music":
        return os.path.join(MUSIC_DIR, filename)
    elif asset_type == "font":
        return os.path.join(FONTS_DIR, filename)
    return filename

# --- CONFIGURATION INTERNE (RESOLUTION FULL HD 1080p) ---
VIRTUAL_W = 1920
VIRTUAL_H = 1080
FPS = 60

# --- CONFIGURATION FENETRE DE DEPART ---
WINDOW_W = 1280 
WINDOW_H = 720

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_FONCE = (30, 30, 30)
GRIS_CLAIR = (200, 200, 200)
ROUGE = (200, 50, 50)
VERT = (50, 200, 50)
BLEU = (50, 50, 200)
JAUNE = (255, 215, 0)
ORANGE = (255, 165, 0)
JAUNE_PASTEL = (255, 253, 208)

# --- CALIBRAGE PHYSIQUE HD ---
SOL_HAUTEUR = 120 
HAUTEUR_CIBLE_PERSO = 220 
POS_SCALE_X = 22 
POS_SCALE_Y = 40 

FONT_FILE = asset_path("font", "Jersey10-Regular.ttf")

# --- GESTION ÉCHELLE & PLEIN ECRAN ---
global_scale = 1.0
offset_x = 0
offset_y = 0

def calculer_echelle(window_w, window_h):
    global global_scale, offset_x, offset_y
    scale_w = window_w / VIRTUAL_W
    scale_h = window_h / VIRTUAL_H
    global_scale = min(scale_w, scale_h)
    
    if global_scale <= 0: global_scale = 0.1
        
    new_w = int(VIRTUAL_W * global_scale)
    new_h = int(VIRTUAL_H * global_scale)
    offset_x = (window_w - new_w) // 2
    offset_y = (window_h - new_h) // 2

def convertir_souris(mouse_pos):
    mx, my = mouse_pos
    mx -= offset_x
    my -= offset_y
    if global_scale > 0:
        mx /= global_scale
        my /= global_scale
    return int(mx), int(my)

# --- FONCTIONS UTILITAIRES ---
def charger_image_redimensionnee(nom, hauteur_cible):
    path = asset_path("image", nom)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            if h == 0: return img
            ratio = hauteur_cible / h
            nouvelle_w = int(w * ratio)
            nouvelle_h = int(h * ratio)
            img = pygame.transform.scale(img, (nouvelle_w, nouvelle_h))
            return img
        except: return None
    return None

def charger_bouton(nom, hauteur_cible=100): 
    path = asset_path("image", nom)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            if h == 0: return img
            ratio = hauteur_cible / h
            nouvelle_w = int(w * ratio)
            nouvelle_h = int(h * ratio)
            img = pygame.transform.scale(img, (nouvelle_w, nouvelle_h))
            return img
        except: return None
    return None

def charger_icone_touche(nom, hauteur_cible=64):
    path = asset_path("image", nom)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            w, h = img.get_size()
            if h == 0: return img
            ratio = hauteur_cible / h
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            img = pygame.transform.smoothscale(img, (new_w, new_h))
            return img
        except: return None
    return None

def charger_disque(nom):
    path = asset_path("image", nom)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(img, (100, 100))
        except: return None
    return None

def get_font(size):
    if os.path.exists(FONT_FILE):
        return pygame.font.Font(FONT_FILE, size)
    else:
        return pygame.font.SysFont("Arial", size, bold=True)

def dessiner_texte_centre(surface, font, text, color, y_pos):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(VIRTUAL_W // 2, y_pos))
    surface.blit(text_surface, rect)

# --- FOND DYNAMIQUE ---
def dessiner_fond_menu_dynamique(surface, img_pattern, scroll_x, scroll_y):
    surface.fill(JAUNE_PASTEL)

    if img_pattern:
        w_pat = img_pattern.get_width()
        h_pat = img_pattern.get_height()
        cols = (VIRTUAL_W // w_pat) + 3
        rows = (VIRTUAL_H // h_pat) + 3
        
        start_x = (scroll_x % w_pat) - w_pat
        start_y = (scroll_y % h_pat) - h_pat

        for r in range(rows):
            for c in range(cols):
                draw_x = start_x + c * w_pat
                draw_y = start_y + r * h_pat
                surface.blit(img_pattern, (draw_x, draw_y))

    overlay = pygame.Surface((VIRTUAL_W, VIRTUAL_H))
    overlay.fill(JAUNE_PASTEL)
    overlay.set_alpha(100) 
    surface.blit(overlay, (0, 0))


# --- HEADER MODIFIÉ ---
# Paramètres optionnels (peuvent être None)
def dessiner_infos_musique(surface, font, musique_thread, images_cd, assets_keys, float_offset, difficulte=None, img_normale=None, img_difficile=None):
    bandeau_h = 120
    bandeau = pygame.Surface((VIRTUAL_W, bandeau_h))
    bandeau.set_alpha(200)
    bandeau.fill(GRIS_FONCE)
    surface.blit(bandeau, (0, 0))

    y_center = bandeau_h // 2

    # --- PARTIE GAUCHE : MUSIQUE ---
    titre_zik = getattr(musique_thread, "titre_actuel", "")
    fichier_zik = getattr(musique_thread, "fichier_actuel", "")
    
    cd_center_x = 80
    if titre_zik:
        img_cd = images_cd.get(fichier_zik)
        if img_cd:
            angle = -(time.time() * 90) % 360 
            img_rotated = pygame.transform.rotate(img_cd, angle)
            rect_rotated = img_rotated.get_rect(center=(cd_center_x, y_center))
            surface.blit(img_rotated, rect_rotated)
        else:
            pygame.draw.circle(surface, GRIS_CLAIR, (cd_center_x, y_center), 50)

        text_surf = font.render(titre_zik, True, JAUNE)
        rect_txt = text_surf.get_rect(midleft=(cd_center_x + 70, y_center))
        surface.blit(text_surf, rect_txt)

    # --- PARTIE CENTRALE : DIFFICULTÉ (UNIQUEMENT SI DÉFINIE) ---
    if difficulte:
        if difficulte == "NORMALE":
            head_img = img_normale
            diff_text = "NORMALE"
            diff_color = VERT
        else:
            head_img = img_difficile
            diff_text = "DIFFICILE"
            diff_color = ROUGE
            
        gap_head_txt = 15 
        
        txt_surf_diff = font.render(diff_text, True, diff_color)
        
        total_w_diff = txt_surf_diff.get_width()
        if head_img:
            total_w_diff += head_img.get_width() + gap_head_txt
            
        start_x_diff = (VIRTUAL_W - total_w_diff) // 2
        
        current_x_center = start_x_diff
        
        if head_img:
            rect_head = head_img.get_rect(midleft=(current_x_center, y_center))
            surface.blit(head_img, rect_head)
            current_x_center += head_img.get_width() + gap_head_txt
            
        rect_txt_diff = txt_surf_diff.get_rect(midleft=(current_x_center, y_center))
        surface.blit(txt_surf_diff, rect_txt_diff)
    # -----------------------------------------------

    # --- PARTIE DROITE : VOLUME ---
    vol = musique_thread.volume_global
    vol_pct = int(vol * 100)
    
    x_end = VIRTUAL_W - 100 
    
    bar_width = 200
    bar_height = 15
    x_bar = x_end - bar_width
    y_bar = y_center + 10 

    if assets_keys['minus']:
        surface.blit(assets_keys['minus'], (x_bar - 50, y_bar - 15 + float_offset))
    
    if assets_keys['plus']:
        surface.blit(assets_keys['plus'], (x_bar + bar_width + 10, y_bar - 15 + float_offset))

    font_emoji = pygame.font.SysFont("segoe ui emoji", 40)
    if vol_pct == 0: icon_vol = "🔇"
    elif vol_pct < 35: icon_vol = "🔈"
    elif vol_pct < 70: icon_vol = "🔉"
    else: icon_vol = "🔊"
    surf_icon = font_emoji.render(icon_vol, True, BLANC)
    txt_vol = f"{vol_pct}%"
    surf_text = font.render(txt_vol, True, BLANC)

    rect_icon = surf_icon.get_rect(bottomright=(x_end, y_bar - 10))
    surface.blit(surf_icon, rect_icon)
    rect_txt = surf_text.get_rect(bottomright=(rect_icon.left - 20, y_bar - 10))
    surface.blit(surf_text, rect_txt)

    pygame.draw.rect(surface, GRIS_FONCE, (x_bar, y_bar, bar_width, bar_height))
    fill_width = int(bar_width * vol)
    
    if vol_pct > 0:
        pygame.draw.rect(surface, BLANC, (x_bar, y_bar, fill_width, bar_height))
        knob_x = x_bar + fill_width
        knob_y = y_bar + bar_height // 2
        pygame.draw.circle(surface, BLANC, (knob_x, knob_y), 12) 
    else:
        pygame.draw.rect(surface, ROUGE, (x_bar, y_bar, 4, bar_height))
        pygame.draw.circle(surface, ROUGE, (x_bar, y_bar + bar_height // 2), 12)
        
    return pygame.Rect(x_bar - 20, y_bar - 20, bar_width + 40, bar_height + 40)


# --- MENUS ---
def dessiner_menu_principal(surface, fonts, musique_thread, images_cd, assets_menu, assets_keys, float_offset):
    if assets_menu['logo']:
        logo_rect = assets_menu['logo'].get_rect(center=(VIRTUAL_W // 2, 260))
        surface.blit(assets_menu['logo'], logo_rect)
    else:
        dessiner_texte_centre(surface, fonts['titre'], "THOUV'RUN", BLANC, 200)

    y_start = 500 
    gap = 130 
    rects_boutons = {} 
    liste_btns = [
        ('jouer', assets_menu['btn_jouer']),
        ('tuto', assets_menu['btn_tuto']),
        ('scores', assets_menu['btn_scores']),
        ('quitter', assets_menu['btn_quitter'])
    ]
    
    for i, (cle, img) in enumerate(liste_btns):
        if img:
            rect = img.get_rect(center=(VIRTUAL_W // 2, y_start + i * gap))
            surface.blit(img, rect)
            rects_boutons[cle] = rect
        else:
            dessiner_texte_centre(surface, fonts['menu'], cle.upper(), BLANC, y_start + i * gap)

    dessiner_texte_centre(surface, fonts['ui_small'], "Projet Thouv'Run - © King Vernus 2026", GRIS_FONCE, VIRTUAL_H - 40)
    
    if assets_keys['f11']:
        txt_f11 = fonts['ui_small'].render(" Plein Ecran", True, GRIS_FONCE)
        rect_txt_f11 = txt_f11.get_rect(bottomright=(VIRTUAL_W - 20, VIRTUAL_H - 20))
        surface.blit(txt_f11, rect_txt_f11)
        y_key = rect_txt_f11.centery - assets_keys['f11'].get_height() // 2
        x_key = rect_txt_f11.left - assets_keys['f11'].get_width()
        surface.blit(assets_keys['f11'], (x_key, y_key + float_offset)) 
    else:
        txt_f11 = fonts['ui_small'].render("[F11] Plein Ecran", True, GRIS_FONCE)
        rect_f11 = txt_f11.get_rect(bottomright=(VIRTUAL_W - 20, VIRTUAL_H - 20))
        surface.blit(txt_f11, rect_f11)

    # Ici, on ne passe PAS de difficulté pour le Menu
    rect_vol = dessiner_infos_musique(surface, fonts['ui'], musique_thread, images_cd, assets_keys, float_offset, difficulte=None)
    return rects_boutons, rect_vol

# --- ECRAN SETUP ---
def dessiner_ecran_setup(surface, fonts, nom_actuel, difficulte_actuelle, assets_keys, float_offset, img_titre_setup):
    width_bg = 1000
    height_bg = 600
    bg_setup = pygame.Surface((width_bg, height_bg), pygame.SRCALPHA)
    pygame.draw.rect(bg_setup, (0, 0, 0, 180), bg_setup.get_rect(), border_radius=30)
    rect_bg = bg_setup.get_rect(center=(VIRTUAL_W // 2, VIRTUAL_H // 2 + 50))
    surface.blit(bg_setup, rect_bg)

    if img_titre_setup:
        rect_titre = img_titre_setup.get_rect(midbottom=(VIRTUAL_W // 2, rect_bg.top - 20))
        surface.blit(img_titre_setup, rect_titre)
    else:
        dessiner_texte_centre(surface, fonts['titre'], "NOUVELLE PARTIE", JAUNE, 180)

    y_start_content = rect_bg.top + 80
    dessiner_texte_centre(surface, fonts['menu'], "VOTRE BLASE :", BLANC, y_start_content)
    
    input_w, input_h = 500, 80
    rect_input = pygame.Rect((VIRTUAL_W - input_w)//2, y_start_content + 50, input_w, input_h)
    
    pygame.draw.rect(surface, BLANC, rect_input, border_radius=10)
    pygame.draw.rect(surface, GRIS_FONCE, rect_input, 4, border_radius=10)
    
    txt_nom = fonts['go'].render(nom_actuel, True, NOIR)
    rect_txt = txt_nom.get_rect(center=rect_input.center)
    surface.blit(txt_nom, rect_txt)
    
    if (time.time() * 2) % 2 > 1:
        cursor_x = rect_txt.right + 5
        pygame.draw.line(surface, NOIR, (cursor_x, rect_input.top + 15), (cursor_x, rect_input.bottom - 15), 3)

    y_diff = y_start_content + 200
    dessiner_texte_centre(surface, fonts['menu'], "DIFFICULTE :", BLANC, y_diff)
    
    rect_diff = pygame.Rect((VIRTUAL_W - input_w)//2, y_diff + 50, input_w, input_h)
    
    if difficulte_actuelle == "NORMALE":
        color_diff = VERT
        text_desc = "Classique"
    else:
        color_diff = ROUGE
        text_desc = "Chaos Total (Score x1.5)"
    
    pygame.draw.rect(surface, color_diff, rect_diff, border_radius=10)
    
    txt_diff = fonts['go'].render(difficulte_actuelle, True, BLANC)
    rect_txt_diff = txt_diff.get_rect(center=rect_diff.center)
    surface.blit(txt_diff, rect_txt_diff)
    
    txt_info = fonts['ui_small'].render(f"{text_desc} - (Cliquez pour changer)", True, GRIS_CLAIR)
    surface.blit(txt_info, (rect_diff.centerx - txt_info.get_width()//2, rect_diff.bottom + 15))

    margin_x = 40
    margin_y = 40
    y_btns = rect_bg.bottom - margin_y

    if assets_keys['esc']:
        icon_esc = assets_keys['esc']
        pos_esc = (rect_bg.left + margin_x, y_btns - icon_esc.get_height()//2 + float_offset)
        surface.blit(icon_esc, pos_esc)
        txt_back = fonts['ui'].render(" Retour", True, BLANC)
        pos_txt_back = (rect_bg.left + margin_x + icon_esc.get_width() + 10, y_btns - txt_back.get_height()//2)
        surface.blit(txt_back, pos_txt_back)

    if assets_keys['enter']:
        txt_play = fonts['ui'].render(" JOUER !", True, JAUNE)
        icon_enter = assets_keys['enter']
        total_w_play = icon_enter.get_width() + 10 + txt_play.get_width()
        pos_enter = (rect_bg.right - margin_x - total_w_play, y_btns - icon_enter.get_height()//2 + float_offset)
        surface.blit(icon_enter, pos_enter)
        pos_txt_play = (rect_bg.right - margin_x - txt_play.get_width(), y_btns - txt_play.get_height()//2)
        surface.blit(txt_play, pos_txt_play)
    else:
        txt_play = fonts['ui'].render("[ENTRÉE] JOUER !", True, JAUNE)
        pos_txt_play = (rect_bg.right - margin_x - txt_play.get_width(), y_btns - txt_play.get_height()//2)
        surface.blit(txt_play, pos_txt_play)

    return rect_diff

# --- TUTO ---
def dessiner_tuto(surface, fonts, img_titre, assets_keys, float_offset):
    width_bg = 1400
    height_bg = 650
    bg_tuto = pygame.Surface((width_bg, height_bg), pygame.SRCALPHA)
    pygame.draw.rect(bg_tuto, (0, 0, 0, 180), bg_tuto.get_rect(), border_radius=30)
    
    x_bg = (VIRTUAL_W - width_bg) // 2
    vertical_shift = 80 
    y_bg = (VIRTUAL_H - height_bg) // 2 + vertical_shift
    
    surface.blit(bg_tuto, (x_bg, y_bg))

    if img_titre:
        rect_titre = img_titre.get_rect(center=(VIRTUAL_W // 2, 180))
        surface.blit(img_titre, rect_titre)
    else:
        dessiner_texte_centre(surface, fonts['titre'], "COMMENT JOUER ?", JAUNE, 150)

    texte_histoire = "C'est le premier jour des cours et tu es en retard ! Bastien va au CSND avec ses rollers et pendant sa route il doit esquiver voitures, camions et policiers, sans oublier de prendre quelques bedos sur la route !"
    
    def rendre_texte_wrap(txt, font, color, max_width):
        mots = txt.split(' ')
        lignes = []
        ligne_courante = []
        for mot in mots:
            ligne_courante.append(mot)
            fw, fh = font.size(' '.join(ligne_courante))
            if fw > max_width:
                ligne_courante.pop()
                lignes.append(' '.join(ligne_courante))
                ligne_courante = [mot]
        lignes.append(' '.join(ligne_courante))
        return lignes

    lignes_histoire = rendre_texte_wrap(texte_histoire, fonts['menu'], BLANC, width_bg - 100)
    
    current_y = y_bg + 40
    for lig in lignes_histoire:
        dessiner_texte_centre(surface, fonts['menu'], lig, BLANC, current_y)
        current_y += 50

    y_controles = current_y + 50
    gap_lines = 85
    
    def dessiner_ligne_controles(elements_list, description, y_pos):
        total_width = 0
        for item in elements_list:
            if isinstance(item, pygame.Surface):
                total_width += item.get_width() + 10
            elif isinstance(item, str):
                s = fonts['menu'].render(item, True, BLANC)
                total_width += s.get_width() + 10
        
        txt_surf = fonts['menu'].render(" : " + description, True, JAUNE)
        total_width += txt_surf.get_width()
        
        current_x = (VIRTUAL_W - total_width) // 2
        
        for item in elements_list:
            if isinstance(item, pygame.Surface):
                surface.blit(item, (current_x, y_pos - item.get_height()//2 + float_offset))
                current_x += item.get_width() + 10
            elif isinstance(item, str):
                s = fonts['menu'].render(item, True, BLANC)
                r = s.get_rect(midleft=(current_x, y_pos))
                surface.blit(s, r)
                current_x += s.get_width() + 10
        
        rect_txt = txt_surf.get_rect(midleft=(current_x, y_pos))
        surface.blit(txt_surf, rect_txt)

    line1_elements = [assets_keys['space'], " / ", assets_keys['up']]
    dessiner_ligne_controles(line1_elements, "Saut Court (Voiture, Police)", y_controles)
    
    line2_elements = [assets_keys['z'], " / ", assets_keys['w']]
    dessiner_ligne_controles(line2_elements, "Saut Long (Camion)", y_controles + gap_lines)
    
    y_systeme = y_controles + gap_lines * 2 + 30 
    
    if assets_keys['r']:
        dessiner_ligne_controles([assets_keys['r']], "Restart apres le game over", y_systeme)
        
    if assets_keys['esc']:
        dessiner_ligne_controles([assets_keys['esc']], "Retour au menu", y_systeme + gap_lines)


# --- NOUVEAUX ECRANS DE SCORES ---

def dessiner_scores_accueil(surface, fonts, assets_scores, assets_keys, float_offset):
    # Titre "SCORES" (Texte)
    if assets_scores['title_scores']:
        rect_titre = assets_scores['title_scores'].get_rect(center=(VIRTUAL_W // 2, 150))
        surface.blit(assets_scores['title_scores'], rect_titre)
    else:
        dessiner_texte_centre(surface, fonts['titre'], "SCORES", BLANC, 150)

    y_cards = 350
    gap_cards = 150
    
    rect_best = pygame.Rect(0,0,0,0)
    rect_hist = pygame.Rect(0,0,0,0)
    rect_all = pygame.Rect(0,0,0,0)

    if assets_scores['btn_best'] and assets_scores['btn_hist']:
        w_card = assets_scores['btn_best'].get_width()
        total_w = w_card * 2 + gap_cards
        start_x = (VIRTUAL_W - total_w) // 2
        
        rect_best = assets_scores['btn_best'].get_rect(topleft=(start_x, y_cards))
        surface.blit(assets_scores['btn_best'], rect_best)
        
        rect_hist = assets_scores['btn_hist'].get_rect(topleft=(start_x + w_card + gap_cards, y_cards))
        surface.blit(assets_scores['btn_hist'], rect_hist)

        # Calculer la largeur cible pour le bouton du bas = largeur totale des 2 cartes + gap
        target_w_all = total_w 
        
        # Redimensionnement du bouton "Tous les scores"
        if assets_scores['btn_all']:
            img_all_scaled = pygame.transform.scale(assets_scores['btn_all'], (target_w_all, 120))
            rect_all = img_all_scaled.get_rect(center=(VIRTUAL_W // 2, 850))
            surface.blit(img_all_scaled, rect_all)

    # Retour
    if assets_keys['esc']:
        icon_esc = assets_keys['esc']
        txt_ret = fonts['ui'].render(" Pour sortir au menu", True, NOIR)
        
        total_w_ret = icon_esc.get_width() + 10 + txt_ret.get_width()
        x_ret = (VIRTUAL_W - total_w_ret) // 2
        y_ret = VIRTUAL_H - 80
        
        surface.blit(icon_esc, (x_ret, y_ret - icon_esc.get_height()//2 + float_offset))
        surface.blit(txt_ret, (x_ret + icon_esc.get_width() + 10, y_ret - txt_ret.get_height()//2))
    
    return rect_best, rect_hist, rect_all

def dessiner_scores_top(surface, fonts, assets_scores, assets_keys, float_offset):
    # 1. Fond (Ordre Z: 1er)
    width_bg = 1400
    height_bg = 700 
    bg_list = pygame.Surface((width_bg, height_bg), pygame.SRCALPHA)
    pygame.draw.rect(bg_list, (0, 0, 0, 180), bg_list.get_rect(), border_radius=30) 
    rect_bg_list = bg_list.get_rect(center=(VIRTUAL_W // 2, VIRTUAL_H // 2 + 50))
    surface.blit(bg_list, rect_bg_list)

    # 2. Titre (Ordre Z: 2nd)
    if assets_scores['title_best']:
        rect_titre = assets_scores['title_best'].get_rect(center=(VIRTUAL_W // 2, 100))
        surface.blit(assets_scores['title_best'], rect_titre)
    else:
        dessiner_texte_centre(surface, fonts['titre'], "MEILLEURS SCORES", JAUNE, 100)

    top_scores = recuperer_meilleurs_scores(10)
    if not top_scores: top_scores = recuperer_top3_global()

    # --- PODIUMS ---
    y_base_podium = rect_bg_list.top + 250
    x_1 = VIRTUAL_W // 2
    x_2 = x_1 - 300
    x_3 = x_1 + 300

    def draw_podium_entry(idx, x_center, asset_podium):
        if idx < len(top_scores):
            s = top_scores[idx]
            if asset_podium:
                rect_pod = asset_podium.get_rect(midbottom=(x_center, y_base_podium))
                surface.blit(asset_podium, rect_pod)
                
                txt_nom = fonts['ui'].render(s['nom'], True, BLANC)
                rect_nom = txt_nom.get_rect(midbottom=(x_center, rect_pod.top - 10))
                surface.blit(txt_nom, rect_nom)
                
                txt_score = fonts['ui'].render(f"{s['score_total']} pts", True, BLANC)
                rect_score = txt_score.get_rect(midtop=(x_center, rect_pod.bottom + 10))
                surface.blit(txt_score, rect_score)

    draw_podium_entry(0, x_1, assets_scores['podium_1'])
    draw_podium_entry(1, x_2, assets_scores['podium_2'])
    draw_podium_entry(2, x_3, assets_scores['podium_3'])

    # --- LISTE (4-10) ---
    y_list = y_base_podium + 120
    
    # En-tête tableau pour les scores 4-10
    font_head = fonts['ui_small']
    
    # Définition des colonnes pour le top scores
    center_x = VIRTUAL_W // 2
    col_x_top = {
        'rank': center_x - 500,
        'joueur': center_x - 300,
        'points': center_x - 50,
        'vers': center_x + 200,
        'diff': center_x + 450
    }

    # Dessin des titres de colonnes
    def draw_col_top(text, x_pos, y, color=BLANC):
        surf = font_head.render(text, True, color)
        rect = surf.get_rect(center=(x_pos, y))
        surface.blit(surf, rect)

    draw_col_top("RANG", col_x_top['rank'], y_list - 40, ORANGE)
    draw_col_top("JOUEUR", col_x_top['joueur'], y_list - 40, ORANGE)
    draw_col_top("POINTS", col_x_top['points'], y_list - 40, ORANGE)
    draw_col_top("VERSION", col_x_top['vers'], y_list - 40, ORANGE)
    draw_col_top("DIFFICULTE", col_x_top['diff'], y_list - 40, ORANGE)

    if len(top_scores) > 3:
        for i in range(3, min(len(top_scores), 10)):
            s = top_scores[i]
            diff = s.get('difficulte', 'Normale')
            ver = s.get('version', 'Graphique')
            
            draw_col_top(f"{i+1}.", col_x_top['rank'], y_list)
            draw_col_top(f"{s['nom']}", col_x_top['joueur'], y_list)
            draw_col_top(f"{s['score_total']}", col_x_top['points'], y_list)
            draw_col_top(f"{ver}", col_x_top['vers'], y_list)
            draw_col_top(f"{diff}", col_x_top['diff'], y_list)
            
            y_list += 50

    # Retour (Centré globalement + NOIR)
    if assets_keys['esc']:
        icon_esc = assets_keys['esc']
        txt_back = fonts['ui'].render(" Pour sortir au menu", True, NOIR)
        
        total_w = icon_esc.get_width() + 10 + txt_back.get_width()
        x_start = (VIRTUAL_W - total_w) // 2
        y_pos = VIRTUAL_H - 80
        
        surface.blit(icon_esc, (x_start, y_pos - icon_esc.get_height()//2 + float_offset))
        surface.blit(txt_back, (x_start + icon_esc.get_width() + 10, y_pos - txt_back.get_height()//2))

def dessiner_scores_perso(surface, fonts, assets_scores, assets_keys, float_offset, nom_joueur):
    if assets_scores['title_hist']:
        rect_titre = assets_scores['title_hist'].get_rect(center=(VIRTUAL_W // 2, 100))
        surface.blit(assets_scores['title_hist'], rect_titre)
    else:
        dessiner_texte_centre(surface, fonts['titre'], "MON HISTORIQUE", JAUNE, 100)

    bg_list = pygame.Surface((1600, 700), pygame.SRCALPHA)
    pygame.draw.rect(bg_list, (0, 0, 0, 180), bg_list.get_rect(), border_radius=30)
    rect_bg_list = bg_list.get_rect(center=(VIRTUAL_W // 2, VIRTUAL_H // 2 + 50))
    surface.blit(bg_list, rect_bg_list)

    y_content = rect_bg_list.top + 40
    dessiner_texte_centre(surface, fonts['menu'], f"10 DERNIERES PARTIES DE {nom_joueur.upper()}", JAUNE, y_content)
    y_content += 60
    
    # SYSTEME DE COLONNES
    center_x = VIRTUAL_W // 2
    col_x = {
        'score': center_x - 500,
        'dist': center_x - 300,
        'bedos': center_x - 100,
        'ver': center_x + 100,
        'diff': center_x + 300,
        'date': center_x + 550
    }

    # En-tête du tableau
    font_head = fonts['ui_small']
    
    def draw_col(text, x_pos, color=BLANC):
        surf = font_head.render(text, True, color)
        rect = surf.get_rect(center=(x_pos, y_content))
        surface.blit(surf, rect)

    draw_col("SCORE", col_x['score'], ORANGE)
    draw_col("DIST", col_x['dist'], ORANGE)
    draw_col("BEDOS", col_x['bedos'], ORANGE)
    draw_col("VERSION", col_x['ver'], ORANGE)
    draw_col("DIFFICULTE", col_x['diff'], ORANGE)
    draw_col("DATE", col_x['date'], ORANGE)
    
    y_content += 50
    
    historique = recuperer_dernieres_parties(nom_joueur, 10)
    
    if not historique:
        dessiner_texte_centre(surface, fonts['ui'], "Aucune partie enregistrée pour ce joueur.", GRIS_CLAIR, y_content + 100)
    else:
        for i, s in enumerate(historique):
            ver = s.get('version', 'Graphique')
            date_str = s.get('date', '')
            
            draw_col(f"{s['score_total']} pts", col_x['score'])
            draw_col(f"{s['distance']} m", col_x['dist'])
            draw_col(f"{s['bedos']}", col_x['bedos'])
            draw_col(f"{ver}", col_x['ver'])
            draw_col(f"{s.get('difficulte','?')}", col_x['diff'])
            draw_col(f"{date_str}", col_x['date'])
            
            y_content += 50

    # --- AJOUT : Bouton retour en bas de l'historique ---
    if assets_keys['esc']:
        icon_esc = assets_keys['esc']
        txt_back = fonts['ui'].render(" Pour sortir au menu", True, NOIR)
        
        total_w = icon_esc.get_width() + 10 + txt_back.get_width()
        x_start = (VIRTUAL_W - total_w) // 2
        y_pos = VIRTUAL_H - 80
        
        surface.blit(icon_esc, (x_start, y_pos - icon_esc.get_height()//2 + float_offset))
        surface.blit(txt_back, (x_start + icon_esc.get_width() + 10, y_pos - txt_back.get_height()//2))

# --- FONCTION DESSIN HUD DANS UNE PASTILLE (CENTRAGE PARFAIT) ---
def dessiner_hud_element(surface, img, font, valeur, x, y, suffixe=""):
    if not img: return
    surface.blit(img, (x, y))
    
    w_img = img.get_width()
    h_img = img.get_height()
    
    empty_zone_x = x + (w_img * 0.25)
    empty_zone_y = y + (h_img * 0.05)
    empty_zone_w = (w_img * 0.97) - (w_img * 0.25)
    empty_zone_h = h_img * 0.90
    
    empty_zone_rect = pygame.Rect(empty_zone_x, empty_zone_y, empty_zone_w, empty_zone_h)
    
    text_str = f"{valeur}{suffixe}"
    txt_surf = font.render(text_str, True, BLANC)
    
    rect_txt = txt_surf.get_rect(center=empty_zone_rect.center)
    
    surface.blit(txt_surf, rect_txt)


# --- MAIN LOOP ---
def main():
    pygame.init()
    
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.RESIZABLE)
    canvas = pygame.Surface((VIRTUAL_W, VIRTUAL_H))
    
    if os.path.exists(asset_path("image", "minilogo.png")):
        try:
            icon = pygame.image.load(asset_path("image", "minilogo.png"))
            pygame.display.set_icon(icon)
        except: pass
        
    pygame.display.set_caption("Projet Thouv'Run - Graphical Edition")
    clock = pygame.time.Clock()
    
    calculer_echelle(WINDOW_W, WINDOW_H)
    
    fonts = {
        'titre': get_font(100),
        'menu': get_font(55),
        'ui': get_font(40),
        'ui_small': get_font(30),
        'go': get_font(80),
        'hud': get_font(45)
    }

    # ASSETS JEU
    img_ville = charger_image_redimensionnee("ville.png", VIRTUAL_H)
    bg_width = img_ville.get_width() if img_ville else 100 
    
    img_run1 = charger_image_redimensionnee("thouverez-run-1.png", HAUTEUR_CIBLE_PERSO)
    img_run2 = charger_image_redimensionnee("thouverez-run-2.png", HAUTEUR_CIBLE_PERSO)
    img_jump_up = charger_image_redimensionnee("thouverez-jump-1.png", HAUTEUR_CIBLE_PERSO)
    img_jump_fall = charger_image_redimensionnee("thouverez-jump-2.png", HAUTEUR_CIBLE_PERSO)
    img_dead = charger_image_redimensionnee("thouverez-dead.png", 160) 
    
    img_police = charger_image_redimensionnee("policier.png", 220)     
    img_voiture = charger_image_redimensionnee("voiture.png", 150)     
    img_camion = charger_image_redimensionnee("camion.png", 280)      
    img_bedo = charger_image_redimensionnee("bedo.png", 90)           
    img_gameover = charger_image_redimensionnee("game_over.png", 250)

    images_cd = {
        "musique_menu.mp3": charger_disque("musique_menu.png"),
        "track1.mp3": charger_disque("track1.png"),
        "track2.mp3": charger_disque("track2.png"),
        "track3.mp3": charger_disque("track3.png"),
        "track4.mp3": charger_disque("track4.png"),
        "track5.mp3": charger_disque("track5.png"),
    }

    # ASSETS HUD
    assets_hud = {
        'score': charger_image_redimensionnee("score_counter.png", 90),
        'bedo': charger_image_redimensionnee("bedo_counter.png", 90),
        'best': charger_image_redimensionnee("best_score.png", 90),
        'p_best': charger_image_redimensionnee("personal_best.png", 90)
    }
    
    # ASSETS DIFFICULTE (HEADER)
    img_tete_normale = charger_image_redimensionnee("tete_normale.png", 70)
    img_tete_difficile = charger_image_redimensionnee("tete_difficile.png", 70)


    # ASSETS MENU & TOUCHES
    img_weed_pattern = charger_image_redimensionnee("weed.png", 80)
    if img_weed_pattern:
        img_weed_pattern = pygame.transform.rotate(img_weed_pattern, -45)
    
    img_titre_setup = charger_image_redimensionnee("nouvelle_partie.png", 130)

    assets_menu = {
        'logo': charger_image_redimensionnee("logo.png", 250),
        'btn_jouer': charger_bouton("jouer.png", hauteur_cible=100), 
        'btn_tuto': charger_bouton("comment_jouer.png", hauteur_cible=100),
        'btn_scores': charger_bouton("scores.png", hauteur_cible=100),
        'btn_quitter': charger_bouton("quitter.png", hauteur_cible=100)
    }

    assets_scores = {
        'title_scores': charger_image_redimensionnee("scores.png", 130),
        'title_best': charger_image_redimensionnee("meilleurs_scores.png", 120),
        'title_hist': charger_image_redimensionnee("mon_historique.png", 120),
        
        'btn_best': charger_image_redimensionnee("top_scores.png", 400),
        'btn_hist': charger_image_redimensionnee("historique.png", 400), 
        'btn_all': pygame.image.load("all_scores.png").convert_alpha() if os.path.exists("all_scores.png") else None,
        
        'podium_1': charger_image_redimensionnee("Podium_1.png", 180),
        'podium_2': charger_image_redimensionnee("Podium_2.png", 140),
        'podium_3': charger_image_redimensionnee("Podium_3.png", 120),
    }

    assets_keys = {
        'esc': charger_icone_touche("key_esc.png"),
        'enter': charger_icone_touche("key_enter.png"), 
        'space': charger_icone_touche("key_space.png", hauteur_cible=64), 
        'up': charger_icone_touche("key_up.png"),
        'w': charger_icone_touche("key_w.png"),
        'z': charger_icone_touche("key_z.png"),
        'plus': charger_icone_touche("key_plus.png", hauteur_cible=40),
        'minus': charger_icone_touche("key_minus.png", hauteur_cible=40),
        'r': charger_icone_touche("key_r.png"), 
        'f11': charger_icone_touche("key_f11.png", hauteur_cible=40)
    }

    musique_thread = tache_fond.GestionnaireMusique()
    musique_thread.start()
    musique_thread.demarrer_ambiance_menu() 

    nom_joueur = recuperer_dernier_joueur()
    if not nom_joueur: nom_joueur = "Player1"
    
    difficulte_actuelle = "NORMALE" 
    liste_difficultes = ["NORMALE", "DIFFICILE"]
    
    jeu = None 
    game_state = "MENU" 
    running = True
    frame_count = 0
    bg_scroll_float = 0.0
    
    menu_scroll_x = 0.0
    menu_scroll_y = 0.0
    
    is_dragging_volume = False
    menu_buttons_rects = {}
    volume_bar_rect = pygame.Rect(0,0,0,0)
    rect_diff_setup = pygame.Rect(0,0,0,0)
    
    rect_score_best = pygame.Rect(0,0,0,0)
    rect_score_hist = pygame.Rect(0,0,0,0)
    rect_score_all = pygame.Rect(0,0,0,0)
    
    is_fullscreen = False

    hud_best_score_val = 0
    hud_perso_best_val = 0
    
    # Synchroniser les scores au démarrage (envoyer locaux vers serveur + récupérer distants)
    print("[Init] Synchronisation des scores au démarrage...")
    synchroniser_scores_au_demarrage()

    while running:
        dt = clock.tick(FPS)
        frame_count += 1
        temps_actuel = time.time()
        key_float_offset = math.sin(temps_actuel * 4) * 5
        menu_scroll_x += 2.0 
        menu_scroll_y -= 2.0 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                if not is_fullscreen: calculer_echelle(event.w, event.h)

            # --- INPUT SETUP ---
            if event.type == pygame.KEYDOWN and game_state == "SETUP":
                if event.key == pygame.K_BACKSPACE:
                    nom_joueur = nom_joueur[:-1]
                elif event.key == pygame.K_RETURN: 
                    # Sauvegarder le nom du joueur choisi
                    sauvegarder_dernier_joueur(nom_joueur)
                    jeu = moteur_jeu.Jeu(nom_joueur, version_jeu="Graphique", difficulte=difficulte_actuelle)
                    musique_thread.demarrer_ambiance_jeu()
                    bg_scroll_float = 0.0
                    
                    top_list = recuperer_meilleurs_scores(1)
                    if top_list: hud_best_score_val = top_list[0]['score_total']
                    else: hud_best_score_val = 0
                    
                    hist_joueur = recuperer_dernieres_parties(nom_joueur, 100)
                    if hist_joueur:
                        hud_perso_best_val = max(p['score_total'] for p in hist_joueur)
                    else:
                        hud_perso_best_val = 0
                    
                    game_state = "JEU"

                elif event.key == pygame.K_ESCAPE:
                    game_state = "MENU"
                    continue
                else:
                    if event.key != pygame.K_SPACE and len(nom_joueur) < 15 and event.unicode.isprintable():
                        nom_joueur += event.unicode

            # --- CLICS ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = convertir_souris(event.pos)
                    
                    if volume_bar_rect.collidepoint(mx, my):
                        is_dragging_volume = True
                        pct = (mx - volume_bar_rect.x) / (volume_bar_rect.width - 40)
                        pct = max(0.0, min(1.0, pct))
                        musique_thread.definir_volume(pct)

                    if game_state == "MENU":
                        if menu_buttons_rects.get('jouer') and menu_buttons_rects['jouer'].collidepoint(mx, my):
                            game_state = "SETUP" 
                        elif menu_buttons_rects.get('tuto') and menu_buttons_rects['tuto'].collidepoint(mx, my):
                            game_state = "TUTO"
                        elif menu_buttons_rects.get('scores') and menu_buttons_rects['scores'].collidepoint(mx, my):
                            game_state = "SCORES_MAIN" 
                        elif menu_buttons_rects.get('quitter') and menu_buttons_rects['quitter'].collidepoint(mx, my):
                            running = False
                    
                    elif game_state == "SETUP":
                        if rect_diff_setup.collidepoint(mx, my):
                            idx = liste_difficultes.index(difficulte_actuelle)
                            difficulte_actuelle = liste_difficultes[(idx + 1) % len(liste_difficultes)]
                            
                    elif game_state == "SCORES_MAIN":
                        if rect_score_best.collidepoint(mx, my):
                            game_state = "SCORES_TOP"
                        elif rect_score_hist.collidepoint(mx, my):
                            game_state = "SCORES_HIST"
                        elif rect_score_all.collidepoint(mx, my):
                            webbrowser.open("https://thouvrun.com/scores") 

                    elif game_state in ["TUTO", "SCORES_TOP", "SCORES_HIST"]:
                        if not is_dragging_volume: pass

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: is_dragging_volume = False
            
            elif event.type == pygame.MOUSEMOTION:
                if is_dragging_volume:
                    mx, my = convertir_souris(event.pos)
                    pct = (mx - volume_bar_rect.x) / (volume_bar_rect.width - 40)
                    pct = max(0.0, min(1.0, pct))
                    musique_thread.definir_volume(pct)

            # --- CLAVIER ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen: window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else: window = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.RESIZABLE)
                    w, h = window.get_size()
                    calculer_echelle(w, h)

                if event.key == pygame.K_KP_PLUS or event.key == pygame.K_PLUS:
                    musique_thread.changer_volume(0.1)
                elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS:
                    musique_thread.changer_volume(-0.1)

                if game_state == "MENU":
                    if event.key == pygame.K_ESCAPE: running = False
                
                elif game_state == "SCORES_MAIN":
                    if event.key == pygame.K_ESCAPE: game_state = "MENU"
                
                elif game_state in ["SCORES_TOP", "SCORES_HIST"]:
                    if event.key == pygame.K_ESCAPE: game_state = "SCORES_MAIN"

                elif game_state == "TUTO":
                    if event.key == pygame.K_ESCAPE: game_state = "MENU"

                elif game_state == "JEU":
                    if jeu and jeu.running:
                        if event.key == pygame.K_ESCAPE:
                            musique_thread.demarrer_ambiance_menu()
                            game_state = "MENU"
                        if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not jeu.joueur.is_jumping:
                            jeu.joueur.sauter_court(); musique_thread.jouer_saut()
                        elif (event.key in [pygame.K_w, pygame.K_z]) and not jeu.joueur.is_jumping:
                            jeu.joueur.sauter_long(); musique_thread.jouer_saut()
                    else:
                        son_gameover_en_cours = False
                        if musique_thread.sfx_gameover and musique_thread.sfx_gameover.get_num_channels() > 0:
                            son_gameover_en_cours = True
                        if musique_thread.mode_actuel == "GAMEOVER_FIN" and not son_gameover_en_cours:
                            if event.key == pygame.K_r:
                                jeu = moteur_jeu.Jeu(nom_joueur, version_jeu="Graphique", difficulte=difficulte_actuelle)
                                musique_thread.demarrer_ambiance_jeu()
                                bg_scroll_float = 0.0
                                
                                top_list = recuperer_meilleurs_scores(1)
                                if top_list: hud_best_score_val = top_list[0]['score_total']
                                else: hud_best_score_val = 0
                                hist_joueur = recuperer_dernieres_parties(nom_joueur, 100)
                                if hist_joueur: hud_perso_best_val = max(p['score_total'] for p in hist_joueur)
                                else: hud_perso_best_val = 0
                                
                            elif event.key == pygame.K_ESCAPE:
                                musique_thread.demarrer_ambiance_menu()
                                game_state = "MENU"

        # --- DRAW ---
        canvas.fill(NOIR) 

        if game_state == "MENU":
            dessiner_fond_menu_dynamique(canvas, img_weed_pattern, menu_scroll_x, menu_scroll_y)
            # ICI : Appel modifié pour ne PAS passer de difficulté (masque le centre du header)
            menu_buttons_rects, volume_bar_rect = dessiner_menu_principal(canvas, fonts, musique_thread, images_cd, assets_menu, assets_keys, key_float_offset)
        
        elif game_state == "SETUP":
            dessiner_fond_menu_dynamique(canvas, img_weed_pattern, menu_scroll_x, menu_scroll_y)
            rect_diff_setup = dessiner_ecran_setup(canvas, fonts, nom_joueur, difficulte_actuelle, assets_keys, key_float_offset, img_titre_setup)

        elif game_state == "TUTO":
            dessiner_fond_menu_dynamique(canvas, img_weed_pattern, menu_scroll_x, menu_scroll_y)
            dessiner_tuto(canvas, fonts, assets_menu['btn_tuto'], assets_keys, key_float_offset)
        
        elif game_state == "SCORES_MAIN":
            dessiner_fond_menu_dynamique(canvas, img_weed_pattern, menu_scroll_x, menu_scroll_y)
            rect_score_best, rect_score_hist, rect_score_all = dessiner_scores_accueil(canvas, fonts, assets_scores, assets_keys, key_float_offset)
            
        elif game_state == "SCORES_TOP":
            dessiner_fond_menu_dynamique(canvas, img_weed_pattern, menu_scroll_x, menu_scroll_y)
            dessiner_scores_top(canvas, fonts, assets_scores, assets_keys, key_float_offset)
            
        elif game_state == "SCORES_HIST":
            dessiner_fond_menu_dynamique(canvas, img_weed_pattern, menu_scroll_x, menu_scroll_y)
            dessiner_scores_perso(canvas, fonts, assets_scores, assets_keys, key_float_offset, nom_joueur)
        
        elif game_state == "JEU":
            if jeu.running:
                jeu.update()
                bg_scroll_float -= 5 * jeu.vitesse
                if bg_scroll_float <= -bg_width: bg_scroll_float += bg_width
                if jeu.bedo_collecte: musique_thread.jouer_bedo()
                
                current_score = int(jeu.score)
                if current_score > hud_perso_best_val: hud_perso_best_val = current_score
                if current_score > hud_best_score_val: hud_best_score_val = current_score
                
            else:
                if not getattr(jeu, "son_joue", False):
                    if "arrete" in jeu.message_fin or "ACAB" in jeu.message_fin: musique_thread.jouer_police()
                    else: musique_thread.jouer_crash()
                    jeu.son_joue = True

            x_pos = int(bg_scroll_float)
            if img_ville:
                canvas.blit(img_ville, (x_pos, 0))
                canvas.blit(img_ville, (x_pos + bg_width, 0))
            else:
                canvas.fill(BLEU) 
            
            def get_pixel_pos(entite_x, entite_y, sprite_h):
                px = entite_x * POS_SCALE_X
                py = VIRTUAL_H - SOL_HAUTEUR - (entite_y * POS_SCALE_Y) - sprite_h
                return px, py

            player_img = img_run1
            if not jeu.running: player_img = img_dead
            elif jeu.joueur.is_jumping:
                if jeu.joueur.dy > 0: player_img = img_jump_up
                else: player_img = img_jump_fall
            else:
                if (frame_count // 10) % 2 == 0: player_img = img_run1
                else: player_img = img_run2
            
            if player_img:
                px, py = get_pixel_pos(jeu.joueur.x, jeu.joueur.y, player_img.get_height())
                if not jeu.running: py += 15 
                canvas.blit(player_img, (px, py))
            else:
                pygame.draw.rect(canvas, ORANGE, (jeu.joueur.x*POS_SCALE_X, 300, 40, 80))

            vibration_y = int(math.sin(temps_actuel * 30) * 2)
            for obs in jeu.obstacles:
                img_obs = None
                if obs.type == "policier": img_obs = img_police
                elif obs.type == "voiture": img_obs = img_voiture
                elif obs.type == "camion": img_obs = img_camion
                
                if img_obs:
                    ox, oy = get_pixel_pos(obs.x, obs.y, img_obs.get_height())
                    canvas.blit(img_obs, (ox, oy + vibration_y))
                else:
                    ox, oy = get_pixel_pos(obs.x, obs.y, 50)
                    color = BLEU if obs.type == "camion" else ROUGE
                    pygame.draw.rect(canvas, color, (ox, oy, 100, 50))

            float_y = int(math.sin(temps_actuel * 5) * 5)
            for bon in jeu.bonus:
                if img_bedo:
                    ox, oy = get_pixel_pos(bon.x, bon.y, img_bedo.get_height())
                    canvas.blit(img_bedo, (ox, oy - 10 + float_y))
                else:
                    ox, oy = get_pixel_pos(bon.x, bon.y, 20)
                    pygame.draw.ellipse(canvas, JAUNE, (ox, oy, 20, 20))

            # ICI : On passe la difficulté uniquement en JEU
            volume_bar_rect = dessiner_infos_musique(canvas, fonts['ui'], musique_thread, images_cd, assets_keys, key_float_offset, difficulte_actuelle, img_tete_normale, img_tete_difficile)
            
            hud_y_start = 140
            hud_gap = 10
            hud_margin_x = 20
            
            # GAUCHE
            if assets_hud['score']:
                h_img = assets_hud['score'].get_height()
                dessiner_hud_element(canvas, assets_hud['score'], fonts['hud'], int(jeu.score), hud_margin_x, hud_y_start, " pts")
                dessiner_hud_element(canvas, assets_hud['bedo'], fonts['hud'], jeu.bedos, hud_margin_x, hud_y_start + h_img + hud_gap, "")

            # DROITE
            if assets_hud['best']:
                w_img = assets_hud['best'].get_width()
                h_img = assets_hud['best'].get_height()
                x_right = VIRTUAL_W - hud_margin_x - w_img
                dessiner_hud_element(canvas, assets_hud['best'], fonts['hud'], hud_best_score_val, x_right, hud_y_start, " pts")
                dessiner_hud_element(canvas, assets_hud['p_best'], fonts['hud'], hud_perso_best_val, x_right, hud_y_start + h_img + hud_gap, " pts")

            if not jeu.running:
                s = pygame.Surface((VIRTUAL_W, VIRTUAL_H))
                s.set_alpha(200); s.fill(NOIR); canvas.blit(s, (0,0))
                
                if img_gameover:
                    rect_go = img_gameover.get_rect(center=(VIRTUAL_W//2, VIRTUAL_H//2 - 150))
                    canvas.blit(img_gameover, rect_go)
                    y_text_start = rect_go.bottom + 50
                else:
                    txt_go = fonts['go'].render("GAME OVER", True, BLANC)
                    rect_go = txt_go.get_rect(center=(VIRTUAL_W//2, VIRTUAL_H//2 - 150))
                    canvas.blit(txt_go, rect_go)
                    y_text_start = rect_go.bottom + 50

                lignes_fin = jeu.message_fin.split('\n')
                for i, lig in enumerate(lignes_fin):
                    txt_fin = fonts['go'].render(lig, True, ROUGE)
                    rect_fin = txt_fin.get_rect(center=(VIRTUAL_W // 2, y_text_start + i * 80))
                    canvas.blit(txt_fin, rect_fin)
                
                y_stats = y_text_start + len(lignes_fin) * 80 + 20
                stats_txt = f"Distance: {int(jeu.distance)}m | Score Final: {int(jeu.score)}"
                dessiner_texte_centre(canvas, fonts['ui'], stats_txt, GRIS_CLAIR, y_stats)
                
                son_gameover_en_cours = False
                if musique_thread.sfx_gameover and musique_thread.sfx_gameover.get_num_channels() > 0: son_gameover_en_cours = True
                
                if musique_thread.mode_actuel == "GAMEOVER_FIN" and not son_gameover_en_cours:
                    base_y = VIRTUAL_H - 150
                    gap_go = 100 
                    
                    if assets_keys['r'] and assets_keys['esc']:
                        txt_r = fonts['ui'].render(" Rejouer", True, BLANC)
                        txt_esc = fonts['ui'].render(" Menu Principal", True, BLANC)
                        
                        w_line1 = assets_keys['r'].get_width() + 10 + txt_r.get_width()
                        w_line2 = assets_keys['esc'].get_width() + 10 + txt_esc.get_width()
                        max_w = max(w_line1, w_line2)
                        
                        total_width_buttons = w_line1 + 100 + w_line2
                        start_x = (VIRTUAL_W - total_width_buttons) // 2
                        
                        canvas.blit(assets_keys['r'], (start_x, base_y - assets_keys['r'].get_height()//2 + key_float_offset))
                        canvas.blit(txt_r, (start_x + assets_keys['r'].get_width() + 10, base_y - txt_r.get_height()//2))
                        
                        start_x_esc = start_x + w_line1 + 100
                        canvas.blit(assets_keys['esc'], (start_x_esc, base_y - assets_keys['esc'].get_height()//2 + key_float_offset))
                        canvas.blit(txt_esc, (start_x_esc + assets_keys['esc'].get_width() + 10, base_y - txt_esc.get_height()//2))

                    else:
                        txt_restart = fonts['ui'].render("[R] Rejouer   ---   [ECHAP] Menu Principal", True, BLANC)
                        rect = txt_restart.get_rect(center=(VIRTUAL_W//2, base_y))
                        canvas.blit(txt_restart, rect)

        # --- RENDER FINAL ---
        window.fill(NOIR)
        scaled_w = int(VIRTUAL_W * global_scale)
        scaled_h = int(VIRTUAL_H * global_scale)
        if scaled_w > 0 and scaled_h > 0:
            scaled_canvas = pygame.transform.scale(canvas, (scaled_w, scaled_h))
            window.blit(scaled_canvas, (offset_x, offset_y))
        
        pygame.display.flip()

    musique_thread.stop()
    pygame.quit()

if __name__ == "__main__":
    main()