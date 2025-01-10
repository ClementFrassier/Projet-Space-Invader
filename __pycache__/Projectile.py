class projectile:
    def __init__(self,graphic,vitesse_projectile,degat,rayon,position):
        self.position=position or [0,0]
        self.degat=degat
        self.graphic=graphic
        self.vitesse_projectile=vitesse_projectile
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
    def get_vitesse_projectile(self):
        return self.vitesse_projectile

    # Setter pour vitesse
    def set_vitesse_projectile(self, vitesse_projectile):
        self.vitesse_projectile = vitesse_projectile

    """
    Déplace le projectile selon dt et la vitesse_projectile
    Paramètre :
        dt : valeur du déplacement
    """
    def move_projectile(self, dt):
        self.position[1] += dt * self.vitesse_projectile  # Déplacement vertical  

