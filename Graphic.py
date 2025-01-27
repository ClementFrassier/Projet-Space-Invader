from Constant import *
import cv2

class graphic:
    def __init__(self):
        pass
    
    def dessiner_barre_point_de_vie(self,fenetre, position, largeur, hauteur, point_de_vie, point_de_vie_max, couleur_fond=(50, 50, 50), couleur_point_de_vie=(0, 255, 0)):
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



    def dessiner_ennemi(self,fenetre, ennemi):
        """
        Dessine un ennemi sur la fenêtre de jeu.

        :param fenetre: Fenêtre de jeu.
        :param ennemi: Objet ennemi avec des attributs position, graphic, largeur, hauteur, point_de_vie, point_de_vie_max.
        """
        if ennemi.point_de_vie > 0:
            # Dessiner l'ennemi
            fenetre[
                ennemi.position[1]:ennemi.position[1] + ENNEMI_HEIGHT,
                ennemi.position[0]:ennemi.position[0] + ENNEMI_WIDTH
            ] = ennemi.graphic

        # Dessiner la barre de vie de l'ennemi
        self.dessiner_barre_point_de_vie(
            fenetre,
            position=(ennemi.position[0], ennemi.position[1] - 10),
            largeur=ENNEMI_WIDTH,
            hauteur=5,
            point_de_vie=ennemi.point_de_vie,
            point_de_vie_max=ennemi.point_de_vie_max
        )


    def dessiner_vaisseau(self,fenetre, vaisseau):
        """
        Dessine le vaisseau sur la fenêtre de jeu.

        :param fenetre: Fenêtre de jeu.
        :param objet: Objet vaisseau avec des attributs position, graphic, largeur, hauteur, point_de_vie, point_de_vie_max.
        """
        if vaisseau.point_de_vie > 0:
            # Dessiner le vaisseau
            fenetre[
                vaisseau.position[1]:vaisseau.position[1] + VAISSEAU_HEIGHT,
                vaisseau.position[0]:vaisseau.position[0] + VAISSEAU_WIDTH
            ] = vaisseau.graphic

            # Dessiner la barre de vie du vaisseau
            
            self.dessiner_barre_point_de_vie(
                fenetre,
                position=(vaisseau.position[0], vaisseau.position[1] - 10),
                largeur=VAISSEAU_WIDTH,
                hauteur=5,
                point_de_vie=vaisseau.point_de_vie,
                point_de_vie_max=vaisseau.point_de_vie_max
            )
    

        
        # Fonction pour dessiner les projectiles du vaisseau
    def dessiner_projectile_vaisseau(self, fenetre, projectile):
        """
        Dessine un projectile du vaisseau sur la fenêtre de jeu.
        
        :param fenetre: Fenêtre de jeu.
        :param projectile: Objet projectile du vaisseau avec des attributs position et graphic.
        """
        if projectile is not None:
            y_start = max(0, projectile.position[1])
            y_end = min(WINDOW_HEIGHT, projectile.position[1] + PROJECTILE_RADIUS * 2)
            x_start = max(0, projectile.position[0])
            x_end = min(WINDOW_WIDTH, projectile.position[0] + PROJECTILE_RADIUS * 2)
            
            if y_end > y_start and x_end > x_start:
                graphic_part = projectile.graphic[:y_end - y_start, :x_end - x_start]
                fenetre[y_start:y_end, x_start:x_end] = graphic_part

    # Fonction pour dessiner les projectiles ennemis
    def dessiner_projectile_ennemi(self, fenetre, projectile):
        """
        Dessine un projectile des ennemis sur la fenêtre de jeu.
        
        :param fenetre: Fenêtre de jeu.
        :param projectile: Objet projectile de l'ennemi avec des attributs position et graphic.
        """
        if projectile is not None:
            y_start = max(0, projectile.position[1])
            y_end = min(WINDOW_HEIGHT, projectile.position[1] + PROJECTILE_RADIUS * 2)
            x_start = max(0, projectile.position[0])
            x_end = min(WINDOW_WIDTH, projectile.position[0] + PROJECTILE_RADIUS * 2)
            
            if y_end > y_start and x_end > x_start:
                graphic_part = projectile.graphic[:y_end - y_start, :x_end - x_start]
                fenetre[y_start:y_end, x_start:x_end] = graphic_part
