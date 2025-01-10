class ennemi:
    def __init__(self, position, hauteur, largeur,graphic,vitesse):
        self.position = position
        self.hauteur=hauteur
        self.largeur=largeur
        self.graphic=graphic
        self.vitesse=vitesse

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
    def get_vitesse(self):
        return self.vitesse

    # Setter pour vitesse
    def set_vitesse(self, vitesse):
        self.vitesse = vitesse

    """
    Déplace l'ennemi selon dt et la vitesse
    Paramètre :
        dt : valeur du déplacement
    """
    def move_ennemi(self, dt):
        self.position += dt * self.vitesse  

