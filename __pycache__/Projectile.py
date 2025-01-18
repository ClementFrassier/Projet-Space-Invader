class projectile:
    def __init__(self, graphic, vitesse_projectile, direction, degat, rayon, position):
        # Validation de la position
        if not isinstance(position, (list, tuple)) or len(position) != 2:
            raise ValueError("La position doit être une liste ou un tuple contenant [x, y].")

        # Validation de la direction
        if not isinstance(direction, int) or direction not in [-1, 1]:
            raise ValueError("La direction doit être un entier valant -1 (monte) ou 1 (descend).")

        # Validation de la vitesse
        if not isinstance(vitesse_projectile, int):
            raise ValueError("vitesse_projectile doit être un entier positif.")

        # Assignation des attributs
        self.graphic = graphic
        self.vitesse_projectile = vitesse_projectile  # Vitesse positive
        self.direction = direction  # -1 pour monter, 1 pour descendre
        self.degat = degat
        self.rayon = rayon
        self.position = list(position)  # Copie pour éviter les références externes

    def move_projectile(self, dt):
        # Le mouvement est influencé par la direction (-1 ou 1)
        self.position[1] += dt * self.vitesse_projectile * self.direction

    def is_out_of_bounds(self, screen_height):
        return self.position[1] < 0 or self.position[1] >= screen_height

    def getPosition(self):
        return self.position
    
    def getDegat(self):
        return self.degat