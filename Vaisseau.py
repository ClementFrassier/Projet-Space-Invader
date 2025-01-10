from Projectile import projectile

class vaisseau:
    def __init__(self, position, graphic, vitesse, hauteur, largeur):
        # Position est maintenant un tableau (liste) avec [x, y]
        self.position = position
        self.pv = 3
        self.graphic = graphic
        self.vitesse = vitesse
        self.largeur = largeur
        self.hauteur = hauteur

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

    # Getter pour pv
    def get_pv(self):
        return self.pv

    # Setter pour pv
    def set_pv(self, pv):
        self.pv = pv

    # Getter pour graphic
    def get_graphic(self):
        return self.graphic

    # Getter pour vitesse
    def get_vitesse(self):
        return self.vitesse

    # Setter pour vitesse
    def set_vitesse(self, vitesse):
        self.vitesse = vitesse

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
        self.position += dt * self.vitesse  


    def vaisseau_projectile(self, vitesse,rayon,graphic):
        nouveau_projectile = projectile(
        position=[
            self.position[0] + self.largeur // 2 - 5,  # Centré horizontalement sur le vaisseau
            self.position[1] - 10  # Positionné juste au-dessus du vaisseau
            ],
            degat=1,
            graphic=graphic,
            vitesse=vitesse,
            rayon=rayon
        )
        return nouveau_projectile

    









