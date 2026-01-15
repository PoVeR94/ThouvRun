import random
from gestion_scores import sauvegarder_nouveau_score, recuperer_records

# --- ART ASCII ---
ART_THOUVEREZ = [r" \\\\ ", r" [o_o]", r"/) B )\ ", r" |_ |_"]
ART_POLICIER = [r"  ___", r" [o_o]", r"-( P (>", r" _| |_"]
ART_VOITURE = [r"      _______", r"     //  ||\ \ ", r" ___//___||_\ \__", r")  _         _   \ ", r"|_/ \_______/ \___|", r"  \_/       \_/    "]
ART_CAMION = [r"        _________________________", r"       //  ||                    \ ", r" _____//___||                     \ ", r")  _       ||  _               _   \ ", r"|_/ \______||_/ \_____________/ \___|", r"  \_/         \_/             \_/"]
ART_BEDO = [r"(=_=_=_=_(_)~"] 

class Entite:
    def __init__(self, x, y, width, height, type_entite, art):
        self.x = x; self.y = y; self.width = width; self.height = height; self.type = type_entite; self.art = art 
    def rect_collision(self, autre):
        col_x = (self.x < autre.x + autre.width - 2) and (self.x + self.width > autre.x + 2)
        col_y = (self.y < autre.y + autre.height) and (self.y + self.height > autre.y)
        return col_x and col_y

class Thouverez(Entite):
    def __init__(self):
        super().__init__(x=10, y=0, width=8, height=4, type_entite="joueur", art=ART_THOUVEREZ)
        self.dy = 0; self.is_jumping = False; self.terre = 0; self.gravite = 0.12; self.force_saut = 1.6   
    def sauter_court(self):
        if not self.is_jumping:
            self.is_jumping = True; self.gravite = 0.13; self.force_saut = 2.0; self.dy = self.force_saut
    def sauter_long(self):
        if not self.is_jumping:
            self.is_jumping = True; self.gravite = 0.05; self.force_saut = 1.5; self.dy = self.force_saut
    def update(self):
        if self.is_jumping:
            self.y += self.dy; self.dy -= self.gravite
            if self.y <= self.terre: self.y = self.terre; self.is_jumping = False; self.dy = 0

class Jeu:
    def __init__(self, nom_joueur="Anonyme", version_jeu="Inconnue", difficulte="NORMALE"):
        self.joueur = Thouverez()
        self.obstacles = []
        self.bonus = []
        self.score = 0; self.distance = 0; self.bedos = 0
        
        self.bedo_collecte = False # <--- NOUVEAU : Indicateur de collecte
        
        self.version = f"{version_jeu} ({difficulte})"; self.difficulte = difficulte
        self.vitesse = 1.0; self.running = True; self.nom_joueur = nom_joueur
        self.message_fin = ""; self.timer_spawn = 0
        self.record_global, self.record_perso = recuperer_records(nom_joueur)

    def update(self):
        if not self.running: return
        
        self.bedo_collecte = False # <--- On reset l'indicateur à chaque image
        
        self.joueur.update()
        vitesse_reelle = 1.2 * self.vitesse
        for obs in self.obstacles: obs.x -= vitesse_reelle
        for bon in self.bonus: bon.x -= vitesse_reelle
        self.obstacles = [o for o in self.obstacles if o.x > -50]
        self.bonus = [b for b in self.bonus if b.x > -50]
        self.timer_spawn += 1
        
        if self.difficulte == "DIFFICILE":
            cond = (self.timer_spawn > (45 / self.vitesse) + random.randint(0, 30))
        else:
            safe = True
            if self.obstacles: 
                if self.obstacles[-1].x > 40: safe = False
            cond = (self.timer_spawn > (90 / self.vitesse) + random.randint(0, 40)) and safe
        
        if cond:
            self.timer_spawn = 0
            chance = 15 if self.difficulte == "DIFFICILE" else 10
            if random.randint(0, 100) < chance: 
                art = ART_BEDO; w = max(len(l) for l in art) 
                self.bonus.append(Entite(100, 6, w-5, 1, "bedo", art))
            else:
                choix = random.randint(0, 2)
                if choix == 0: self.obstacles.append(Entite(100, 0, max(len(l) for l in ART_VOITURE), len(ART_VOITURE), "voiture", ART_VOITURE))
                elif choix == 1: self.obstacles.append(Entite(100, 0, max(len(l) for l in ART_CAMION), len(ART_CAMION), "camion", ART_CAMION))
                else: self.obstacles.append(Entite(100, 0, max(len(l) for l in ART_POLICIER), len(ART_POLICIER), "policier", ART_POLICIER))

        for obs in self.obstacles:
            if self.joueur.rect_collision(obs): self.fin_partie(obs.type)
        for bon in self.bonus:
            if self.joueur.rect_collision(bon):
                self.score += 50; self.bedos += 1; self.bonus.remove(bon)
                self.bedo_collecte = True # <--- NOUVEAU : On signale la collecte
                
        gain = 0.1 * self.vitesse
        self.distance += gain
        self.score += (gain * 1.5) if self.difficulte == "DIFFICILE" else gain
        self.vitesse += 0.0002

    def fin_partie(self, cause):
        self.running = False
        sauvegarder_nouveau_score(self.nom_joueur, self.score, self.distance, self.bedos, self.version, self.difficulte)
        if cause in ["camion", "voiture"]: self.message_fin = "Tu as été percuté !\nArrêt maladie pendant 6 mois pour se récupérer !"
        elif cause == "policier": self.message_fin = "ACAB\nTu as été arrêté ! 1 an d'emprisonnement et 3 750€ d'amende !"
        else: self.message_fin = "G A M E   O V E R"