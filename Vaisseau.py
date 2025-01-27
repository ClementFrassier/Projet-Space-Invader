from Projectile import projectile
from Son import *

class vaisseau:
    def __init__(self, position, graphic, vitesse_vaisseau, hauteur, largeur, point_de_vie):
        # Position est maintenant un tableau (liste) avec [x, y]
        self.position = position
        self.graphic = graphic
        self.vitesse_vaisseau = vitesse_vaisseau
        self.largeur = largeur
        self.hauteur = hauteur
        self.point_de_vie = point_de_vie
        self.point_de_vie_max=point_de_vie

    # Getter pour position (renvoie la liste entière)
    def get_position(self):
        return self.position

    # Setter pour position
    def set_position(self, x, y):
        self.position[0] = x
        self.position[1] = y

    # Getter pour X (accède à la première valeur du tableau)
    def get_X(self):
        return self.position[0]

    # Setter pour X (modifie la première valeur du tableau)
    def set_X(self, x):
        self.position[0] = x

    # Getter pour y (accède à la deuxième valeur du tableau)
    def get_y(self):
        return self.position[1]

    # Setter pour y (modifie la deuxième valeur du tableau)
    def set_y(self, y):
        self.position[1] = y

    # Getter pour point_de_vie
    def get_point_de_vie(self):
        return self.point_de_vie

    # Setter pour point_de_vie
    def set_point_de_vie(self, point_de_vie):
        self.point_de_vie = point_de_vie

    # Getter pour graphic
    def get_graphic(self):
        return self.graphic

    # Getter pour vitesse
    def get_vitesse(self):
        return self.vitesse_vaisseau

    # Setter pour vitesse
    def set_vitesse(self, vitesse_vaisseau):
        self.vitesse = vitesse_vaisseau

    # Getter pour largeur
    def get_largeur(self):
        return self.largeur


    # Getter pour hauteur
    def get_hauteur(self):
        return self.hauteur

    """
    Déplace le vaisseau selon dt et la vitesse
    Paramètre :
        dt : valeur du déplacement
    """
    def move_vaisseau(self, dt):
        self.position += dt * self.vitesse_vaisseau  


    def vaisseau_projectile(self, vitesse_projectile,rayon,graphic):
        nouveau_projectile = projectile(
        position=[
            self.position[0] + self.largeur // 2 - 5,  # Centré horizontalement sur le vaisseau
            self.position[1] - 10  # Positionné juste au-dessus du vaisseau
            ],
            degat=1,
            graphic=graphic,
            vitesse_projectile=vitesse_projectile,
            rayon=rayon
        )
        return nouveau_projectile

    """
    Determine si le vaisseau a ete touchee par un projectile true, sinon false
    entree : le projectile
    sortie : un booleen
    """
    def vaisseau_projectile_interaction(self, projectile, explosion_sound=None):
        if (projectile.getPosition()[0] > self.position[0] and
                projectile.getPosition()[0] < self.position[0] + self.largeur and
                projectile.getPosition()[1]>self.position[1] and
                projectile.getPosition()[1]<self.position[1] + self.hauteur):
            self.point_de_vie -= projectile.getDegat()
            
            # Jouer le son d'explosion si disponible
            if explosion_sound:
                explosion_sound.play()
            
            return True
        return False








