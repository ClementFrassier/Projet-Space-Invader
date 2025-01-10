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

    # Création des sprites
    projectile_sprite = np.zeros((PROJECTILE_RADIUS * 2, PROJECTILE_RADIUS * 2, 3), dtype=np.uint8)
    cv2.circle(projectile_sprite, (PROJECTILE_RADIUS, PROJECTILE_RADIUS), PROJECTILE_RADIUS, (255, 0, 0), -1)

    vaisseau_sprite = np.ones((VAISSEAU_HEIGHT, VAISSEAU_WIDTH, 3), dtype=np.uint8) * 255
    ennemi_sprite = np.ones((ENNEMI_HEIGHT, ENNEMI_WIDTH, 3), dtype=np.uint8) * 255

    # Initialisation des objets
    Vaisseau = vaisseau(
        position=[270, 500],
        graphic=vaisseau_sprite,
        vitesse=[VITESSE, 0],
        largeur=VAISSEAU_WIDTH,
        hauteur=VAISSEAU_HEIGHT,
    )

    ennemis = [
        ennemi(
            position=[100 + i * 100, 100],
            graphic=ennemi_sprite,
            vitesse=[VITESSE, 0],
            largeur=ENNEMI_WIDTH,
            hauteur=ENNEMI_HEIGHT,
        )
        for i in range(5)
    ]

    ennemis_direction = [VITESSE, 0]

    vaisseau_proj = []

    # Fenêtre de jeu
    game_window = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

    # Gestion des touches
    pressed_keys = set()

    def handle_key_down(key_code):
        pressed_keys.add(key_code)

    def handle_key_up(key_code):
        if key_code in pressed_keys:
            pressed_keys.remove(key_code)

    while True:
        game_window.fill(0)

        key = cv2.waitKey(30) & 0xFF  # Détection des touches pressées
        if key != 255:  # Ajouter la touche détectée
            handle_key_down(key)
        else:
            pressed_keys.clear()

        # Si ESC est pressé, quitter le jeu
        if 27 in pressed_keys:
            break

        # Déplacement gauche/droite du vaisseau
        if 81 in pressed_keys:  # Flèche gauche
            Vaisseau.position[0] = max(0, Vaisseau.position[0] - VITESSE)
        if 83 in pressed_keys:  # Flèche droite
            Vaisseau.position[0] = min(WINDOW_WIDTH - VAISSEAU_WIDTH, Vaisseau.position[0] + VITESSE)

        # Tir avec la barre d'espace
        if 32 in pressed_keys:  # Barre d'espace
            if not any(proj.position[1] >= Vaisseau.position[1] for proj in vaisseau_proj):
                nouveau_projectile = Vaisseau.vaisseau_projectile([0, -1], PROJECTILE_RADIUS, projectile_sprite)
                vaisseau_proj.append(nouveau_projectile)

        # Déplacer les ennemis comme un bloc
        ennemis_bounds = [min(e.position[0] for e in ennemis), max(e.position[0] + ENNEMI_WIDTH for e in ennemis)]
        if ennemis_bounds[0] <= 0 or ennemis_bounds[1] >= WINDOW_WIDTH:
            ennemis_direction[0] = -ennemis_direction[0]  # Inverser la direction

        for Ennemi in ennemis:
            Ennemi.position[0] += ennemis_direction[0]

        # Afficher le vaisseau
        game_window[Vaisseau.position[1]:Vaisseau.position[1] + VAISSEAU_HEIGHT,
                    Vaisseau.position[0]:Vaisseau.position[0] + VAISSEAU_WIDTH] = Vaisseau.graphic

        # Afficher les ennemis
        for Ennemi in ennemis:
            game_window[Ennemi.position[1]:Ennemi.position[1] + ENNEMI_HEIGHT,
                        Ennemi.position[0]:Ennemi.position[0] + ENNEMI_WIDTH] = Ennemi.graphic

        # Déplacement et affichage des projectiles
        for proj in vaisseau_proj[:]:
            proj.move_projectile(2 * VITESSE)
            if proj.position[1] < 0:
                vaisseau_proj.remove(proj)
            else:
                game_window[proj.position[1]:proj.position[1] + PROJECTILE_RADIUS * 2,
                            proj.position[0]:proj.position[0] + PROJECTILE_RADIUS * 2] = proj.graphic

        # Afficher la fenêtre de jeu
        cv2.imshow("Space Invader", game_window)

    # Fermer la fenêtre
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
