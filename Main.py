import cv2
import numpy as np
from Vaisseau import vaisseau
from Ennemis import ennemi
from Projectile import projectile
from Jeu import jeu
from SpaceInvader import spaceInvader
from Graphic import *
from Camera import *
import time
from FPSCounter import *
from SkeletonTracker import *
from Parsers import *
from models import *

from Constant import *

game = spaceInvader()
game_graphic = graphic()

def main():
    nombre_ennemi=1
    name=game.menu_princiapl()
    
    while True:
        # Initialisation de la fenêtre de jeu
        cv2.namedWindow("Space Invader")
        game_window = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
        
        # Initialisation des sprites et objets
        projectile_vaisseau_sprite, projectile_ennemi_sprite, vaisseau_sprite, ennemi_sprite = game.initialiser_sprites()
        Vaisseau, ennemis, Jeu = game.initialiser_objets(vaisseau_sprite, ennemi_sprite,nombre_ennemi,name)

        # Variables de jeu
        ennemis_direction = [VITESSE_ENNEMI, 0]
        vaisseau_proj = []
        ennemi_proj = []
        last_shoot_time = time.time()

        # Paramètres de la caméra
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
        game_camera = camera(cap)

        # Boucle principale
        game_over = False
        while not game_over and cap.isOpened():
            print(f"Player Name: {name}")

            game_window.fill(0)

            # Gestion de la caméra
            previous_x, last_shoot_time, vaisseau_proj = game_camera.gerer_camera(previous_x, last_shoot_time, Vaisseau, game, tracking, projectile_vaisseau_sprite, vaisseau_proj)

            # Gestion des événements clavier pour quitter
            key = cv2.waitKey(EPSILON) & 0xFF
            if key == 27:  # ESC pour quitter
                cv2.destroyAllWindows()
                return

            # Déplacement des ennemis
            ennemis = game.gerer_deplacement_ennemis(ennemis, ennemis_direction, Jeu, game_graphic, game_window)

            #Si tous les ennemis detruits :
            if not ennemis:
                if nombre_ennemi <= 3:
                    nombre_ennemi+=1
                _ , ennemis, _ = game.initialiser_objets(vaisseau_sprite, ennemi_sprite,nombre_ennemi,name)

            # Déplacement et affichage des projectiles
            vaisseau_proj = game.gerer_projectiles_vaisseau(vaisseau_proj, ennemis, game_graphic, game_window)

            # Déplacement et affichage des projectiles ennemis
            ennemi_proj = game.gerer_projectiles_ennemi(ennemi_proj, Vaisseau, ennemis, projectile_ennemi_sprite, game_graphic, game_window)

            # Affichage du vaisseau
            game_graphic.dessiner_vaisseau(game_window, Vaisseau)

            cv2.putText(game_window, f"Score: {Jeu.score}", (WINDOW_WIDTH - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Si perdu
            if Vaisseau.point_de_vie <= 0:
                game_over = True
                break

            # Affichage de la fenêtre
            cv2.imshow("Space Invader", game_window)

        #  gestion si perdi
        while game_over:
            nombre_ennemi=1
            game_window.fill(0)
            cv2.putText(game_window, "Perdu", (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(game_window, f"Score: {Jeu.score}", (WINDOW_WIDTH - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow("Space Invader", game_window)
            key = cv2.waitKey(1) & 0xFF

            if key == 27:  # ESC pour quitter
                cv2.destroyAllWindows()
                return
            elif key == 32:  # Barre d'espace pour relancer
                game_over = False  

        cv2.destroyWindow("Space Invader")  

if __name__ == "__main__":
    main()
