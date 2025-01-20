# Space Invaders - Projet Python

## Introduction

**Space Invaders** est un projet académique visant à recréer le jeu classique de tir en 2D. Développé en Python, le jeu repose sur des fonctionnalités de base et utilise une caméra pour capturer les mouvements du joueur, ce qui ajoute une dimension interactive et innovante.

---

## Objectifs du Projet

- Reproduire le gameplay classique de Space Invaders.
- Introduire une nouvelle interaction basée sur la reconnaissance gestuelle à l’aide de la caméra.
- Ajouter des améliorations selon le temps disponible (niveaux, sons, effets visuels, etc.).

---

## Fonctionnalités

### Fonctionnalités de base
1. **Déplacement du vaisseau** : 
   - Contrôlé par les mouvements capturés par une caméra.
   - Mouvement fluide et en temps réel.

2. **Système de tir** :
   - Détection de gestes (ex. fermer le poing) pour lancer un projectile.
   - Les projectiles détruisent les ennemis en cas de collision.

3. **Ennemis** :
   - Déplacement horizontal en zigzag et descente progressive.
   - Augmentation de la difficulté au fil du temps.

4. **Gestion des collisions** :
   - Les projectiles détruisent les ennemis.
   - Les tirs ennemis ou collisions directes font perdre des vies au joueur.

5. **Score** :
   - Un compteur s’incrémente à chaque ennemi détruit.
   - Affichage en temps réel.

### Fonctionnalités avancées (en cours ou planifiées)
- Niveaux avec difficulté croissante.
- Ennemis spéciaux (plus rapides, résistants, ou destructeurs).
- Barrières destructibles pour protéger le joueur.
- Effets visuels et sonores immersifs.
- Système de vie supplémentaire et bonus.

---

## Architecture du Projet

- **`main.py`** : Point d’entrée du jeu.
- **`classes/`** : Contient les classes principales :
  - `Vaisseau` : Gestion du vaisseau du joueur.
  - `Ennemi` : Comportement des ennemis.
  - `Projectile` : Gestion des tirs.
  - `Jeu` : Logique globale (mise à jour, collisions, score).
- **`assets/`** : Images, sons et autres ressources.
- **`utils/`** : Fonctions utilitaires (détection de collisions, gestion des mouvements, etc.).

---

## Technologies et outils

- **Langage** : Python (≥ 3.8)
- **Bibliothèque graphique** : Pygame
- **Détection gestuelle** : OpenCV
- **IDE recommandé** : Visual Studio Code
- **Gestionnaire de versions** : Git (GitLab)

---

## Installation

1. **Cloner le dépôt Git** :
   ```bash
   git clone git@gitlab.polytech.umontpellier.fr:julien.fabre05/projet-space-invader.git
   cd projet-space-invader
