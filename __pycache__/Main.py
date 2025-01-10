import cv2
import numpy as np
from Vaisseau import vaisseau
from Ennemis import ennemi
from Projectile import projectile
import random


def dessiner_barre_point_de_vie(fenetre, position, largeur, hauteur, point_de_vie, point_de_vie_max, couleur_fond=(50, 50, 50), couleur_point_de_vie=(0, 255, 0)):
    if point_de_vie > point_de_vie_max:  # Assurez-vous que les valeurs sont correctes
        point_de_vie = point_de_vie_max
    if point_de_vie < 0:
        point_de_vie = 0

    largeur_point_de_vie = int((point_de_vie / point_de_vie_max) * largeur)
    cv2.rectangle(fenetre, position, (position[0] + largeur, position[1] + hauteur), couleur_fond, -1)
    if point_de_vie > 0:
        cv2.rectangle(fenetre, position, (position[0] + largeur_point_de_vie, position[1] + hauteur), couleur_point_de_vie, -1)

def main():
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    VAISSEAU_WIDTH, VAISSEAU_HEIGHT = 60, 20
    PROJECTILE_RADIUS = 2
    ENNEMI_WIDTH, ENNEMI_HEIGHT = 40, 20
    # Vitesse
    vitesse_vaisseau = 10
    vitesse_projectils = 5
    vitesse_ennemi = 2

    cv2.namedWindow("Space Invader")

    # Création des sprites
    projectile_sprite = np.zeros((PROJECTILE_RADIUS * 2, PROJECTILE_RADIUS * 2, 3), dtype=np.uint8)
    cv2.circle(projectile_sprite, (PROJECTILE_RADIUS, PROJECTILE_RADIUS), PROJECTILE_RADIUS, (255, 0, 0), -1)

    vaisseau_sprite = np.ones((VAISSEAU_HEIGHT, VAISSEAU_WIDTH, 3), dtype=np.uint8) * 255
    ennemi_sprite = np.ones((ENNEMI_HEIGHT, ENNEMI_WIDTH, 3), dtype=np.uint8) * 255

    
    # Initialisation des objets
    Vaisseau = vaisseau(
        position=[270, 500],
        graphic=vaisseau_sprite,
        vitesse_vaisseau=vitesse_vaisseau,
        largeur=VAISSEAU_WIDTH,
        hauteur=VAISSEAU_HEIGHT,
        point_de_vie=10  # Ajout des points de point_de_vie du vaisseau
    )
    
    ennemis = [
        ennemi(
            position=[100 + i * 100, 100],
            graphic=ennemi_sprite,
            vitesse_ennemi=vitesse_ennemi,
            largeur=ENNEMI_WIDTH,
            hauteur=ENNEMI_HEIGHT,
            point_de_vie=1  # Ajout des points de point_de_vie pour chaque ennemi
        )
        for i in range(5)
    ]

    ennemis_direction = [vitesse_ennemi, 0]

    vaisseau_proj = []
    ennemi_proj = []

    # Fenêtre de jeu
    game_window = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

    # Gestion des touches
    keys = {'left': False, 'right': False, 'shoot': False}

    while True:
        game_window.fill(0)

        # Détecter les touches pressées
        key = cv2.waitKey(1) & 0xFF
        if key == 81:  # Flèche gauche
            keys['left'] = True
        elif key == 83:  # Flèche droite
            keys['right'] = True
        elif key == 32:  # Barre d'espace
            keys['shoot'] = True
        elif key == 255:  # Pas de touche pressée
            keys = {'left': False, 'right': False, 'shoot': False}
        elif key == 27:  # ESC pour quitter
            break

        # Déplacement gauche/droite du vaisseau
        if keys['left']:
            Vaisseau.position[0] = max(0, Vaisseau.position[0] - vitesse_vaisseau)
        if keys['right']:
            Vaisseau.position[0] = min(WINDOW_WIDTH - VAISSEAU_WIDTH, Vaisseau.position[0] + vitesse_vaisseau)

        # Tir avec la barre d'espace
        if keys['shoot']:
            if not any(proj.position[1] >= Vaisseau.position[1] for proj in vaisseau_proj):
                nouveau_projectile = Vaisseau.vaisseau_projectile([0, -10], PROJECTILE_RADIUS, projectile_sprite)
                vaisseau_proj.append(nouveau_projectile)

        # Déplacement des ennemis comme un bloc
        ennemis_bounds = [min(e.position[0] for e in ennemis), max(e.position[0] + ENNEMI_WIDTH for e in ennemis)]
        if ennemis_bounds[0] <= 0 or ennemis_bounds[1] >= WINDOW_WIDTH:
            ennemis_direction[0] = -ennemis_direction[0]

        for Ennemi in ennemis:
            Ennemi.position[0] += ennemis_direction[0]

            # Les ennemis tirent de manière aléatoire
            if random.random() < 0.02:
                ennemi_proj.append(projectile(
                    graphic=projectile_sprite,
                    vitesse_ennemi=[0, 5],
                    degat=1,
                    rayon=PROJECTILE_RADIUS,
                    position=[Ennemi.position[0] + ENNEMI_WIDTH // 2, Ennemi.position[1] + ENNEMI_HEIGHT]
                ))

        # Afficher le vaisseau
        game_window[Vaisseau.position[1]:Vaisseau.position[1] + VAISSEAU_HEIGHT,
                    Vaisseau.position[0]:Vaisseau.position[0] + VAISSEAU_WIDTH] = Vaisseau.graphic

        # Dessiner la barre de point_de_vie du vaisseau
        dessiner_barre_point_de_vie(
            game_window,
            position=(Vaisseau.position[0], Vaisseau.position[1] - 10),
            largeur=VAISSEAU_WIDTH,
            hauteur=5,
            point_de_vie=Vaisseau.point_de_vie,
            point_de_vie_max=100
        )

        # Afficher les ennemis et leurs barres de point_de_vie
        for Ennemi in ennemis:
            game_window[Ennemi.position[1]:Ennemi.position[1] + ENNEMI_HEIGHT,
                        Ennemi.position[0]:Ennemi.position[0] + ENNEMI_WIDTH] = Ennemi.graphic
            dessiner_barre_point_de_vie(
                game_window,
                position=(Ennemi.position[0], Ennemi.position[1] - 10),
                largeur=ENNEMI_WIDTH,
                hauteur=5,
                point_de_vie=Ennemi.point_de_vie,
                point_de_vie_max=50
            )

        # Déplacement et affichage des projectiles du vaisseau
        for proj in vaisseau_proj[:]:
            proj.move_projectile(1)
            if proj.position[1] < 0:
                vaisseau_proj.remove(proj)
            else:
                game_window[proj.position[1]:proj.position[1] + PROJECTILE_RADIUS * 2,
                            proj.position[0]:proj.position[0] + PROJECTILE_RADIUS * 2] = proj.graphic

        # Déplacement et affichage des projectiles ennemis
        for proj in ennemi_proj[:]:
            proj.move_projectile(1)
            if proj.position[1] >= WINDOW_HEIGHT:
                ennemi_proj.remove(proj)
            else:
                game_window[proj.position[1]:proj.position[1] + PROJECTILE_RADIUS * 2,
                            proj.position[0]:proj.position[0] + PROJECTILE_RADIUS * 2] = proj.graphic

        # Afficher la fenêtre de jeu
        cv2.imshow("Space Invader", game_window)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
