import cv2
import numpy as np
from Vaisseau import vaisseau
from Ennemis import ennemi
from Projectile import projectile
from Jeu import jeu
from SpaceInvader import spaceInvader
from Graphic import *
import random
import time
import os

import cv2

from FPSCounter import *
from SkeletonTracker import *
from Parsers import *
from models import *

from Constant import *

game = spaceInvader()
game_graphic = graphic()



"""CAMERA////////////////////////////////////////////////////"""

def savoir_main_ferme(y1, y2, x1, x2):
    """
    Vérifie si les coordonnées du point 2 (x2, y2) sont à ±0.1 
    des coordonnées du point 1 (x1, y1).
    """
    if y1 is not None and y2 is not None and x1 is not None and x2 is not None:
        if abs(y2 - y1) <= 0.2 and abs(x2 - x1) <= 0.2:
            return True
    return False


def detection_deplacement_main(current_x, previous_x):
    #0.01 = correction d'erreur
    if current_x > previous_x + 0.01:
        return True                #Droite
                        
    elif current_x < previous_x - 0.01:
        return False              #Gauche 
                        

def main():
    # Initialisation de la fenêtre de jeu
    cv2.namedWindow("Space Invader")
    game_window = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

    # Initialisation des sprites et objets
    projectile_sprite, vaisseau_sprite, ennemi_sprite = game.initialiser_sprites()
    Vaisseau, ennemis, Jeu = game.initialiser_objets(vaisseau_sprite, ennemi_sprite)

    # Variables de jeu
    ennemis_direction = [VITESSE_ENNEMI, 0]
    vaisseau_proj = []
    ennemi_proj = []
    keys = {'left': False, 'right': False, 'shoot': False}
    last_shoot_time = time.time()

    pv_vaisseau_max=Vaisseau.point_de_vie
    #CAMERAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    EPSILON = 1
    video_path = 0 
    cap = cv2.VideoCapture(video_path)
    fps = FPSCounter()

    params = SkeletonTrackerParameters()
    params.use_yolo = False
    params.use_body = False
    params.max_bodies = 1
    params.use_hands = True
    params.use_face = False
    params.hand_skip_frames = 1
    params.models_paths = "PoseEstimation/models"
    tracking = SkeletonTracker(params)

    previous_x = None
    

    # Boucle principale
    while True and cap.isOpened():

        game_window.fill(0)
        #CAMERA
        ret, img = cap.read()
        if not ret:
            break
        img = cv2.resize(img, (300, 240))
        img = cv2.flip(img, 1)
        tracking.update(img)

        for hand in tracking.hands:
            img = hand.displaySkeleton(img)
            articulation_paume = hand.skeleton()[0]
            articulation_Middle = hand.skeleton()[12]

            paume_x=articulation_paume[1]
            paume_y=articulation_paume[0]

            middle_x=articulation_Middle[1]
            middle_y=articulation_Middle[0]

            
            if not np.isnan(articulation_paume).any():
                current_x = articulation_paume[1]
                if previous_x is not None:
                  
                    if detection_deplacement_main(current_x,previous_x):
                        #Droite
                        Vaisseau.position[0] = min(WINDOW_WIDTH - VAISSEAU_WIDTH, Vaisseau.position[0] + VITESSE_VAISSEAU*3)
                    elif detection_deplacement_main(current_x,previous_x)==False:
                        #Gauche 
                        Vaisseau.position[0] = max(0, Vaisseau.position[0] - VITESSE_VAISSEAU*3)

                if savoir_main_ferme(paume_y, middle_y, paume_x, middle_x):
                    current_time = time.time()
                    if current_time - last_shoot_time >= 0.25: #4 tires par secondes 
                        dernier_projectile = game.create_vaisseau_proj(projectile_sprite,Vaisseau)
                        vaisseau_proj.append(dernier_projectile)
                        last_shoot_time = current_time

                previous_x = current_x
                
        fps.update()
        img = fps.display(img)
        cv2.imshow("Resultat", img)
        key = cv2.waitKey(EPSILON) & 0xFF
        #FIN CAMERA

        # Gestion des événements clavier
        key = cv2.waitKey(8) & 0xFF
        if key == 81 or key == ord("q"):  # Flèche gauche
            keys['left'] = True
        elif key == 83 or key == ord("d"):  # Flèche droite
            keys['right'] = True
        elif key == 32:  # Barre d'espace
            keys['shoot'] = True
        elif key == 255:  # Pas de touche pressée
            keys = {'left': False, 'right': False, 'shoot': False}
        elif key == 27:  # ESC pour quitter
            break
            

        # Déplacement du vaisseau
        if keys['left']:
            Vaisseau.position[0] = max(0, Vaisseau.position[0] - VITESSE_VAISSEAU)
        if keys['right']:
            Vaisseau.position[0] = min(WINDOW_WIDTH - VAISSEAU_WIDTH, Vaisseau.position[0] + VITESSE_VAISSEAU)

        # Tir du vaisseau
        if keys['shoot']:
            current_time = time.time()
            if current_time - last_shoot_time >= 0.25: #4 tires par secondes 
                dernier_projectile = game.create_vaisseau_proj(projectile_sprite,Vaisseau)
                vaisseau_proj.append(dernier_projectile)
                last_shoot_time = current_time

        # Déplacement des ennemis
        if ennemis:
            ennemis_bounds = [min(e.position[0] for e in ennemis), max(e.position[0] + ENNEMI_WIDTH for e in ennemis)]
            if ennemis_bounds[0] <= 0 or ennemis_bounds[1] >= WINDOW_WIDTH:
                ennemis_direction[0] = -ennemis_direction[0]

        if not ennemis:  # Si aucun ennemi n'est présent
            ennemis = game.initialiser_objets(vaisseau_sprite, ennemi_sprite)[1]

        for Ennemi in ennemis[:]:
            Ennemi.position[0] += ennemis_direction[0]
            # Tir aléatoire des ennemis
            if random.random() < PROBA_TIR_ENNEMI:
                ennemi_proj.append(game.create_ennemi_proj(projectile_sprite,Ennemi))

            # Affichage des ennemis
            game_graphic.dessiner_ennemi(game_window, Ennemi)
            
            if Ennemi.point_de_vie <= 0:
                ennemis.remove(Ennemi)
                Jeu.score+=1

        
        # Déplacement et affichage des projectiles
        for proj in vaisseau_proj[:]:
            proj.move_projectile(1)
            if proj.is_out_of_bounds(WINDOW_HEIGHT):
                vaisseau_proj.remove(proj)
            else:
                y_start = max(0, proj.position[1])
                y_end = min(WINDOW_HEIGHT, proj.position[1] + PROJECTILE_RADIUS * 2)
                x_start = max(0, proj.position[0])
                x_end = min(WINDOW_WIDTH, proj.position[0] + PROJECTILE_RADIUS * 2)
                if y_end > y_start and x_end > x_start:
                    graphic_part = proj.graphic[:y_end - y_start, :x_end - x_start]
                    game_window[y_start:y_end, x_start :x_end] = graphic_part
                    for Ennemi in ennemis[:]:
                        if Ennemi.ennemi_projectile_interaction(proj):
                            vaisseau_proj.remove(proj)

 
        # Déplacement et affichage des projectiles ennemis
        for proj in ennemi_proj[:]:
            proj.move_projectile(1)
            if proj.is_out_of_bounds(WINDOW_HEIGHT):
                ennemi_proj.remove(proj)
            else:
                y_start = max(0, proj.position[1])
                y_end = min(WINDOW_HEIGHT, proj.position[1] + PROJECTILE_RADIUS * 2)
                x_start = max(0, proj.position[0])
                x_end = min(WINDOW_WIDTH, proj.position[0] + PROJECTILE_RADIUS * 2)
                if y_end > y_start and x_end > x_start:
                    graphic_part = proj.graphic[:y_end - y_start, :x_end - x_start]
                    game_window[y_start:y_end, x_start:x_end] = graphic_part
                if Vaisseau.vaisseau_projectile_interaction(proj):
                    ennemi_proj.remove(proj)
                    

        # Affichage du vaisseau
        game_graphic.dessiner_vaisseau(game_window, Vaisseau)
        
        cv2.putText(game_window, f"Score: {Jeu.score}", (WINDOW_WIDTH - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        
        #Si perdu
        if Vaisseau.point_de_vie <= 0:
            cv2.namedWindow("Perdu")
            while True:
                game_window.fill(0)
                cv2.putText(game_window, "Perdu", (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(game_window, f"Score: {Jeu.score}", (WINDOW_WIDTH - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                cv2.imshow("Perdu", game_window)
                key = cv2.waitKey(1) & 0xFF

                if key == 27:  # ESC pour quitter
                    break
                elif key == 32:  # Barre d'espace pour relancer
                    cv2.destroyAllWindows()
                    main()

            break


        # Affichage de la fenêtre
        cv2.imshow("Space Invader", game_window)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
