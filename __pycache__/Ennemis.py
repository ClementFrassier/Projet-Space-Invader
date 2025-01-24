class ennemi:
    def __init__(self, position, hauteur, largeur,graphic,vitesse_ennemi, point_de_vie):
        self.position = position
        self.hauteur=hauteur
        self.largeur=largeur
        self.graphic=graphic
        self.vitesse_ennemi=vitesse_ennemi
        self.point_de_vie=point_de_vie
        self.point_de_vie_max=point_de_vie

    # Getter pour position
    def get_position(self):
        return self.position

    # Setter pour position
    def set_position(self, position):
        self.position = position

    # Getter pour graphic
    def get_graphic(self):
        return self.graphic

    # Setter pour graphic
    def set_graphic(self, graphic):
        self.graphic = graphic

    # Getter pour vitesse
    def get_vitesse_ennemi(self):
        return self.vitesse_ennemi

    # Setter pour vitesse
    def set_vitesse_ennemi(self, vitesse_ennemi):
        self.vitesse_ennemi = vitesse_ennemi

    """
    Déplace l'ennemi selon dt et la vitesse_ennemi
    Paramètre :
        dt : valeur du déplacement
    """
    def move_ennemi(self, dt):
        self.position += dt * self.vitesse_ennemi  

    def ennemi_projectile_interaction(self, projectile):
        if (projectile.getPosition()[0] > self.position[0] and
                projectile.getPosition()[0] < self.position[0] + self.largeur and
                projectile.getPosition()[1]>self.position[1] and
                projectile.getPosition()[1]<self.position[1] + self.hauteur):
            self.point_de_vie -= projectile.getDegat()
            return True
        return False

        