from SkeletonTracker import *

class handTracker:
    def __init__(self):
        self.previous_position = None
        self.variation = 0.01  

    def detect_movement(self, current_position):
        """
        Détecte le mouvement de la main basé sur la position actuelle.

        Args:
            current_position (list or np.ndarray): Coordonnées [x, y] actuelles de la main.

        Returns:
            str: Direction du mouvement ('left', 'right', ou 'stationary').
        """
        # Si aucune position précédente n'existe, initialise-la
        if self.previous_position is None:
            self.previous_position = current_position
            return "stationary"

        # Calcul du déplacement horizontal (x)
        delta_x = current_position[0] - self.previous_position[0]

        # Détection de la direction
        if abs(delta_x) > self.movement_threshold:
            direction = "right" if delta_x > 0 else "left"
        else:
            direction = "stationary"

        # Mise à jour de la position précédente
        self.previous_position = current_position

        return direction

