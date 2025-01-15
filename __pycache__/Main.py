import cv2
import numpy as np
from Vaisseau import vaisseau
from Ennemis import ennemi
from Projectile import projectile
import random


def dessiner_barre_point_de_vie(fenetre, position, largeur, hauteur, point_de_vie, point_de_vie_max, couleur_fond=(50, 50, 50), couleur_point_de_vie=(0, 255, 0)):
    """
    Dessine une barre de point de vie.

    :param fenetre: Fenêtre de jeu.
    :param position: Position (x, y) de la barre.
    :param largeur: Largeur de la barre.
    :param hauteur: Hauteur de la barre.
    :param point_de_vie: Points de vie actuels.
    :param point_de_vie_max: Points de vie maximum.
    :param couleur_fond: Couleur du fond de la barre.
    :param couleur_point_de_vie: Couleur des points de vie restants.
    """
    point_de_vie = max(0, min(point_de_vie, point_de_vie_max))
    largeur_point_de_vie = int((point_de_vie / point_de_vie_max) * largeur)
    cv2.rectangle(fenetre, position, (position[0] + largeur, position[1] + hauteur), couleur_fond, -1)
    if point_de_vie > 0:
        cv2.rectangle(fenetre, position, (position[0] + largeur_point_de_vie, position[1] + hauteur), couleur_point_de_vie, -1)


def main():
    # Dimensions de la fenêtre
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    VAISSEAU_WIDTH, VAISSEAU_HEIGHT = 60, 20
    PROJECTILE_RADIUS = 2
    ENNEMI_WIDTH, ENNEMI_HEIGHT = 40, 20

    # Vitesse
    vitesse_vaisseau = 10
    vitesse_projectils = 5  # Vitesse des projectiles du vaisseau
    vitesse_ennemi = 1  # Vitesse des ennemis
    vitesse_projectils_ennemi = 3  # Vitesse des projectiles ennemis


    # Créer la fenêtre
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
        point_de_vie=10
    )

    ennemis = [
        ennemi(
            position=[100 + i * 100, 100],
            graphic=ennemi_sprite,
            vitesse_ennemi=vitesse_ennemi,
            largeur=ENNEMI_WIDTH,
            hauteur=ENNEMI_HEIGHT,
            point_de_vie=3
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

        # Gestion des événements clavier
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
            if not any(proj.position[1] < Vaisseau.position[1] for proj in vaisseau_proj):
                nouveau_projectile = projectile(
                    graphic=projectile_sprite,
                    vitesse_projectile=vitesse_projectils,
                    direction=-1,  # Monte
                    degat=1,
                    rayon=PROJECTILE_RADIUS,
                    position=[Vaisseau.position[0] + VAISSEAU_WIDTH // 2, Vaisseau.position[1]]
                )
                vaisseau_proj.append(nouveau_projectile)

        # Déplacement des ennemis comme un bloc
        ennemis_bounds = [min(e.position[0] for e in ennemis), max(e.position[0] + ENNEMI_WIDTH for e in ennemis)]
        if ennemis_bounds[0] <= 0 or ennemis_bounds[1] >= WINDOW_WIDTH:
            ennemis_direction[0] = -ennemis_direction[0]

        for Ennemi in ennemis[:]:
            Ennemi.position[0] += ennemis_direction[0]

            # Les ennemis tirent de manière aléatoire
            if random.random() < 0.01:
                ennemi_proj.append(projectile(
                    graphic=projectile_sprite,
                    vitesse_projectile=vitesse_projectils_ennemi,
                    direction=1,  # Descend
                    degat=1,
                    rayon=PROJECTILE_RADIUS,
                    position=[Ennemi.position[0] + ENNEMI_WIDTH // 2, Ennemi.position[1] + ENNEMI_HEIGHT]
                ))

            # Affichage des ennemis
            if Ennemi.point_de_vie > 0:
                game_window[Ennemi.position[1]:Ennemi.position[1] + ENNEMI_HEIGHT,
                            Ennemi.position[0]:Ennemi.position[0] + ENNEMI_WIDTH] = Ennemi.graphic

                # Barre de point de vie de l'ennemi
                dessiner_barre_point_de_vie(
                    game_window,
                    position=(Ennemi.position[0], Ennemi.position[1] - 10),
                    largeur=ENNEMI_WIDTH,
                    hauteur=5,
                    point_de_vie=Ennemi.point_de_vie,
                    point_de_vie_max=3
                )

        # Déplacement et affichage des projectiles du vaisseau
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
                    game_window[y_start:y_end, x_start:x_end] = graphic_part

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

        # Affichage du vaisseau
        y_start = max(0, Vaisseau.position[1])
        y_end = min(WINDOW_HEIGHT, Vaisseau.position[1] + VAISSEAU_HEIGHT)
        x_start = max(0, Vaisseau.position[0])
        x_end = min(WINDOW_WIDTH, Vaisseau.position[0] + VAISSEAU_WIDTH)

        if y_end > y_start and x_end > x_start:
            game_window[y_start:y_end, x_start:x_end] = Vaisseau.graphic[:y_end - y_start, :x_end - x_start]

        # Barre de point de vie du vaisseau
        dessiner_barre_point_de_vie(
            game_window,
            position=(Vaisseau.position[0], Vaisseau.position[1] - 10),
            largeur=VAISSEAU_WIDTH,
            hauteur=5,
            point_de_vie=Vaisseau.point_de_vie,
            point_de_vie_max=10
        )

        # Affichage de la fenêtre
        cv2.imshow("Space Invader", game_window)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
