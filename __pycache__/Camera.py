from Constant import *
import cv2
from FPSCounter import *
from SkeletonTracker import *
from Parsers import *
from models import *
import time
class camera :
    def __init__(self, cap):
        self.cap = cap
        self.previous_x = None
        self.last_shoot_time = time.time()


    def savoir_main_ferme(self,y1, y2, x1, x2):
        """
        Vérifie si les coordonnées du point 2 (x2, y2) sont à ±0.1 
        des coordonnées du point 1 (x1, y1).
        """
        if y1 is not None and y2 is not None and x1 is not None and x2 is not None:
            if abs(y2 - y1) <= 0.1 and abs(x2 - x1) <= 0.1:
                return True
        return False


    def detection_deplacement_main(self,current_x, previous_x):
        #0.01 = correction d'erreur
        if current_x > previous_x + 0.01:
            return True                #Droite
                            
        elif current_x < previous_x - 0.01:
            return False              #Gauche
        

    def gerer_camera(self, previous_x, last_shoot_time, vaisseau, game, tracking, projectile_sprite,vaisseau_proj):
        ret, img = self.cap.read()
        if not ret:
            return previous_x, last_shoot_time, []

        img = cv2.resize(img, (300, 240))
        img = cv2.flip(img, 1)

        tracking.update(img)

        
        for hand in tracking.hands:
            img = hand.displaySkeleton(img)
            articulation_paume = hand.skeleton()[0]
            articulation_Middle = hand.skeleton()[12]

            paume_x = articulation_paume[1]
            paume_y = articulation_paume[0]
            middle_x = articulation_Middle[1]
            middle_y = articulation_Middle[0]

            if not np.isnan(articulation_paume).any():
                current_x = articulation_paume[1]
                if previous_x is not None:
                    if self.detection_deplacement_main(current_x, previous_x):
                        # Droite
                        vaisseau.position[0] = min(WINDOW_WIDTH - VAISSEAU_WIDTH, vaisseau.position[0] + VITESSE_VAISSEAU * 3)
                    elif self.detection_deplacement_main(current_x, previous_x) == False:
                        # Gauche
                        vaisseau.position[0] = max(0, vaisseau.position[0] - VITESSE_VAISSEAU * 3)

                if self.savoir_main_ferme(paume_y, middle_y, paume_x, middle_x):
                    current_time = time.time()
                    if current_time - last_shoot_time >= 0.25:  # 4 tirs par seconde
                        dernier_projectile = game.create_vaisseau_proj(projectile_sprite, vaisseau)
                        vaisseau_proj.append(dernier_projectile)
                        last_shoot_time = current_time

                previous_x = current_x

        cv2.imshow("Camera Feed", img)  # Affiche la caméra dans une fenêtre distincte
        return previous_x, last_shoot_time, vaisseau_proj
