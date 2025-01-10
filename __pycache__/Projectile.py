class projectile:
    def __init__(self,graphic,vitesse,degat,rayon,position):
        self.position=position or [0,0]
        self.degat=degat
        self.graphic=graphic
        self.vitesse=vitesse
        self.rayon=rayon
        
    
    # Setter pour position
    def set_position(self, position):
        self.position = position


    # Getter pour degat
    def get_degat(self):
        return self.degat

    # Setter pour degat
    def set_degat(self, degat):
        self.degat = degat

    # Getter pour rayon
    def get_rayon(self):
        return self.rayon

    # Getter pour vitesse
    def get_vitesse(self):
        return self.vitesse

    # Setter pour vitesse
    def set_vitesse(self, vitesse):
        self.vitesse = vitesse

    """
    Déplace le projectile selon dt et la vitesse
    Paramètre :
        dt : valeur du déplacement
    """
    def move_projectile(self, dt):
        self.position[0] += dt * self.vitesse[0]  # Déplacement horizontal
        self.position[1] += dt * self.vitesse[1]  # Déplacement vertical  

