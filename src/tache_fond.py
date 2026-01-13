import threading
import time
import os
import random

# On vérifie juste si le module existe
try:
    import pygame
    MODULE_PYGAME_PRESENT = True
except ImportError:
    MODULE_PYGAME_PRESENT = False

# --- CHEMINS DES ASSETS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")

def asset_path(asset_type, filename):
    """Construit le chemin complet vers un asset."""
    if asset_type == "sound":
        return os.path.join(SOUNDS_DIR, filename)
    elif asset_type == "music":
        return os.path.join(MUSIC_DIR, filename)
    return filename

class GestionnaireMusique(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True
        self.daemon = True 
        self.etat_musique = "Silence"
        self.titre_actuel = ""
        self.fichier_actuel = ""
        self.mode_actuel = "MENU"
        
        # --- VOLUME (0.0 à 1.0) ---
        self.volume_global = 0.5 
        
        self.audio_actif = MODULE_PYGAME_PRESENT
        
        self.playlist_menu = ["musique_menu.mp3"] 
        self.playlist_jeu = ["track1.mp3", "track2.mp3", "track3.mp3", "track4.mp3", "track5.mp3"]
        
        self.infos_pistes = {
            "musique_menu.mp3": "Fyahbwoy - Forget & Forgive",
            "track1.mp3": "Faya Ganjah - Citoyen du monde",
            "track2.mp3": "Kabuto - Ganyita Radioaktiva",
            "track3.mp3": "Fyahbwoy - Tanto por ti",
            "track4.mp3": "Bob Marley & The Wailers - Three Little Birds",
            "track5.mp3": "Skrillex & Damian Marley - Make It Bun Dem",
        }

        self.sfx_saut = None
        self.sfx_crash = None
        self.sfx_police = None
        self.sfx_bedo = None
        self.sfx_gameover = None 
        
        self.canal_sfx_en_cours = None
        
        if self.audio_actif:
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                
                if os.path.exists(asset_path("sound", "saut.wav")): self.sfx_saut = pygame.mixer.Sound(asset_path("sound", "saut.wav"))
                if os.path.exists(asset_path("sound", "crash.wav")): self.sfx_crash = pygame.mixer.Sound(asset_path("sound", "crash.wav"))
                if os.path.exists(asset_path("sound", "police.wav")): self.sfx_police = pygame.mixer.Sound(asset_path("sound", "police.wav"))
                if os.path.exists(asset_path("sound", "cigarette.wav")): self.sfx_bedo = pygame.mixer.Sound(asset_path("sound", "cigarette.wav"))
                if os.path.exists(asset_path("sound", "gameover.wav")): self.sfx_gameover = pygame.mixer.Sound(asset_path("sound", "gameover.wav"))
                
                self._appliquer_volume()
                self.etat_musique = "Audio OK"
            except Exception as e:
                self.etat_musique = f"Erreur Audio: {e}"
                self.audio_actif = False

    def run(self):
        while self.running:
            if self.audio_actif:
                if self.mode_actuel == "GAMEOVER_WAIT":
                    if self.canal_sfx_en_cours and not self.canal_sfx_en_cours.get_busy():
                        self.jouer_son_final_gameover()
                        self.mode_actuel = "GAMEOVER_FIN"
                elif self.mode_actuel in ["MENU", "JEU"]:
                    try:
                        if not pygame.mixer.music.get_busy():
                            self._enchainer_suivante()
                    except: pass
            time.sleep(0.1)

    def _enchainer_suivante(self):
        if not self.audio_actif: return
        if "GAMEOVER" in self.mode_actuel: return

        if self.mode_actuel == "MENU":
            if self.playlist_menu:
                piste = random.choice(self.playlist_menu)
                self._charger_et_jouer(piste)
                
        elif self.mode_actuel == "JEU":
            if self.playlist_jeu:
                piste = random.choice(self.playlist_jeu)
                self._charger_et_jouer(piste)

    def _charger_et_jouer(self, fichier):
        if not self.audio_actif: return
        path = asset_path("music", fichier)
        if not os.path.exists(path):
            self.etat_musique = f"Introuvable: {fichier}"
            return
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self._appliquer_volume()
            
            self.fichier_actuel = fichier
            joli_nom = self.infos_pistes.get(fichier, fichier)
            self.titre_actuel = f"{joli_nom}"
            self.etat_musique = "Lecture en cours"
            
        except Exception as e:
            self.etat_musique = f"Err Lecture: {e}"

    def _appliquer_volume(self):
        if not self.audio_actif: return
        try:
            pygame.mixer.music.set_volume(self.volume_global)
            if self.sfx_saut: self.sfx_saut.set_volume(self.volume_global)
            if self.sfx_crash: self.sfx_crash.set_volume(self.volume_global)
            if self.sfx_police: self.sfx_police.set_volume(self.volume_global)
            if self.sfx_bedo: self.sfx_bedo.set_volume(self.volume_global)
            if self.sfx_gameover: self.sfx_gameover.set_volume(self.volume_global)
        except: pass

    # --- COMMANDES PUBLIQUES ---

    def changer_volume(self, delta):
        self.volume_global += delta
        if self.volume_global > 1.0: self.volume_global = 1.0
        if self.volume_global < 0.0: self.volume_global = 0.0
        self._appliquer_volume()

    # NOUVELLE FONCTION POUR LA SOURIS
    def definir_volume(self, valeur):
        self.volume_global = valeur
        if self.volume_global > 1.0: self.volume_global = 1.0
        if self.volume_global < 0.0: self.volume_global = 0.0
        self._appliquer_volume()

    def demarrer_ambiance_menu(self):
        self.mode_actuel = "MENU"
        if self.audio_actif:
            try:
                pygame.mixer.music.stop()
                self._enchainer_suivante()
            except: pass

    def demarrer_ambiance_jeu(self):
        self.mode_actuel = "JEU"
        if self.audio_actif:
            try:
                pygame.mixer.stop()
                pygame.mixer.music.stop()
                self._enchainer_suivante()
            except: pass

    def jouer_saut(self):
        if self.audio_actif and self.sfx_saut:
            try: self.sfx_saut.play()
            except: pass

    def jouer_bedo(self):
        if self.audio_actif and self.sfx_bedo:
            try: self.sfx_bedo.play()
            except: pass

    def jouer_crash(self):
        if self.audio_actif:
            self.mode_actuel = "GAMEOVER_WAIT"
            self.titre_actuel = "ACCIDENT !"
            try:
                pygame.mixer.music.stop()
                if self.sfx_crash: 
                    self.canal_sfx_en_cours = self.sfx_crash.play()
            except: pass

    def jouer_police(self):
        if self.audio_actif:
            self.mode_actuel = "GAMEOVER_WAIT"
            self.titre_actuel = "ARRESTATION !" 
            try:
                pygame.mixer.music.stop()
                if self.sfx_police: 
                    self.canal_sfx_en_cours = self.sfx_police.play()
            except: pass
            
    def jouer_son_final_gameover(self):
        if self.audio_actif and self.sfx_gameover:
            try: 
                self.sfx_gameover.play()
                self.titre_actuel = "GAME OVER"
            except: pass

    def stop(self):
        self.running = False
        if self.audio_actif:
            try: pygame.mixer.quit()
            except: pass