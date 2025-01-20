class jeu:

    def __init__(self, joueur, score):
        self.joueur = joueur
        self.score=score

    # Getter pour joueur
    def get_joueur(self):
        return self.joueur

    # Setter pour joueur
    def set_joueur(self, joueur):
        self.joueur = joueur

    # Getter pour score
    def get_score(self):
        return self.score

    # Setter pour score
    def set_score(self, score):
        self.score = score

    