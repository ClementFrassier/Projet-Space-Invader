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



    def dessiner_ennemi(self,fenetre, ennemi_objet):
        """
        Dessine un ennemi sur la fenêtre de jeu.

        :param fenetre: Fenêtre de jeu.
        :param ennemi_objet: Objet ennemi avec des attributs position, graphic, largeur, hauteur, point_de_vie, point_de_vie_max.
        """
        if ennemi_objet.point_de_vie > 0:
            # Dessiner l'ennemi
            fenetre[
                ennemi_objet.position[1]:ennemi_objet.position[1] + ENNEMI_HEIGHT,
                ennemi_objet.position[0]:ennemi_objet.position[0] + ENNEMI_WIDTH
            ] = ennemi_objet.graphic

        # Dessiner la barre de vie de l'ennemi
        self.dessiner_barre_point_de_vie(
            fenetre,
            position=(ennemi_objet.position[0], ennemi_objet.position[1] - 10),
            largeur=ENNEMI_WIDTH,
            hauteur=5,
            point_de_vie=ennemi_objet.point_de_vie,
            point_de_vie_max=ennemi_objet.point_de_vie_max
        )


    def dessiner_vaisseau(self,fenetre, vaisseau_objet):
        """
        Dessine le vaisseau sur la fenêtre de jeu.

        :param fenetre: Fenêtre de jeu.
        :param vaisseau_objet: Objet vaisseau avec des attributs position, graphic, largeur, hauteur, point_de_vie, point_de_vie_max.
        """
        if vaisseau_objet.point_de_vie > 0:
            # Dessiner le vaisseau
            fenetre[
                vaisseau_objet.position[1]:vaisseau_objet.position[1] + VAISSEAU_HEIGHT,
                vaisseau_objet.position[0]:vaisseau_objet.position[0] + VAISSEAU_WIDTH
            ] = vaisseau_objet.graphic

            # Dessiner la barre de vie du vaisseau
            
            self.dessiner_barre_point_de_vie(
                fenetre,
                position=(vaisseau_objet.position[0], vaisseau_objet.position[1] - 10),
                largeur=VAISSEAU_WIDTH,
                hauteur=5,
                point_de_vie=vaisseau_objet.point_de_vie,
                point_de_vie_max=vaisseau_objet.point_de_vie_max
            )
    

        
