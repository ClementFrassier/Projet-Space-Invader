import cv2
import numpy as np
from Vaisseau import vaisseau
from Ennemis import ennemi
from Projectile import projectile

def main():

    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

    VAISSEAU_WIDTH, VAISSEAU_HEIGHT = 60, 20
    PROJECTILE_RADIUS = 2
    ENNEMI_WIDTH, ENNEMI_HEIGHT = 40, 20

    VITESSE = 10
    
    cv2.namedWindow("Space Invader")

    projectile_sprite = np.zeros((PROJECTILE_RADIUS * 2, PROJECTILE_RADIUS * 2, 3), dtype=np.uint8)
    cv2.circle(projectile_sprite, (PROJECTILE_RADIUS, PROJECTILE_RADIUS), PROJECTILE_RADIUS, (255, 0, 0), -1)

    vaisseau_sprite = np.ones((VAISSEAU_HEIGHT, VAISSEAU_WIDTH, 3), dtype=np.uint8) * 255
    ennemi_sprite = np.ones((ENNEMI_HEIGHT, ENNEMI_WIDTH, 3), dtype=np.uint8) * 255

    Vaisseau = vaisseau(
        position = [270,500],
        graphic = vaisseau_sprite,
        vitesse = [VITESSE,0],
        largeur=VAISSEAU_WIDTH,
        hauteur=VAISSEAU_HEIGHT,
    )

    Ennemi = ennemi(
        position = [270,100],
        graphic = ennemi_sprite,
        vitesse = [VITESSE,0],
        largeur=ENNEMI_WIDTH,
        hauteur=ENNEMI_HEIGHT,
    )

    Projectile = projectile(
        position=None,
        degat=1,
        graphic=projectile_sprite,
        vitesse=[0,-10],
        rayon=PROJECTILE_RADIUS
    )

    game_window = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

    vaisseau_proj=[]

    while True : 
        game_window.fill(0)

        key = cv2.waitKey(30)  
        
        if key == 27:  # Si la touche échappée (ESC) est pressée, quitter
            break
        if key == 81:  # Flèche gauche
            Vaisseau.position[0] = max(0, Vaisseau.position[0] - VITESSE)
        elif key == 83:  # Flèche droite
            Vaisseau.position[0] = min(WINDOW_WIDTH - VAISSEAU_WIDTH, Vaisseau.position[0] + VITESSE)
        elif key == 32:  # Barre d'espace
            nouveau_projectile = Vaisseau.vaisseau_projectile([0, -1], PROJECTILE_RADIUS, projectile_sprite)
            vaisseau_proj.append(nouveau_projectile)




        # Déplacer l'ennemi
        Ennemi.position[0] += Ennemi.vitesse[0]

        # Vérifier si l'ennemi atteint le bord de l'écran, il rebondit
        if Ennemi.position[0] <= 0 or Ennemi.position[0] + ENNEMI_WIDTH >= WINDOW_WIDTH:
            Ennemi.vitesse[0] = -Ennemi.vitesse[0]

        # Afficher les éléments à leurs positions
        game_window[Vaisseau.position[1]:Vaisseau.position[1] + VAISSEAU_HEIGHT, Vaisseau.position[0]:Vaisseau.position[0] + VAISSEAU_WIDTH] = Vaisseau.graphic
        game_window[Ennemi.position[1]:Ennemi.position[1] + ENNEMI_HEIGHT, Ennemi.position[0]:Ennemi.position[0] + ENNEMI_WIDTH] = Ennemi.graphic

        for proj in vaisseau_proj:
            proj.move_projectile(2 * VITESSE)
            if proj.position[1] < 0:  
                vaisseau_proj.remove(proj)
            else:
                game_window[proj.position[1]:proj.position[1] + PROJECTILE_RADIUS * 2,
                    proj.position[0]:proj.position[0] + PROJECTILE_RADIUS * 2] = proj.graphic


        # Afficher la fenêtre de jeu avec tous les éléments
        cv2.imshow("Space Invader", game_window)

    # Fermer la fenêtre
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
