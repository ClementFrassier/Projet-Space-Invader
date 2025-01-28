# Space Invaders - Python Project

## Introduction

**Space Invaders** is an academic project designed to recreate the iconic 2D shooting game. Developed in Python, this game combines the classic gameplay with a modern twist: gesture recognition using a camera to control player movements. This project explores interactive gameplay and advanced programming concepts.

---

## Project Objectives

- Recreate the classic **Space Invaders** gameplay.
- Introduce innovative interaction with gesture recognition via a camera.
- Implement advanced features (levels, sound effects, animations, etc.) depending on the time available.

---

## Features

### Core Features
1. **Ship Control**:  
   - Move the ship using hand movements captured by a camera.
   - Real-time and smooth movements.

2. **Shooting System**:  
   - Gesture detection (e.g., clenching the fist) to shoot projectiles.
   - Projectiles destroy enemies upon collision.

3. **Enemies**:  
   - Horizontal zigzag movement with progressive descent.
   - Increasing difficulty over time (faster movement, more enemies).

4. **Collision Management**:  
   - Destroy enemies with projectiles.
   - Lose lives if hit by enemy fire or upon direct collision with an enemy.

5. **Score System**:  
   - Points are awarded for each destroyed enemy.
   - Real-time score display during the game.

### Advanced Features (ongoing or planned)
- Multiple levels with increasing difficulty.
- Special enemies (faster, tougher, or more destructive).
- Destructible barriers to protect the player.
- Immersive sound effects and visual animations.
- Bonus system (extra lives, ship upgrades).

---

## Project Architecture

The project is modular and designed for easy scalability. Below are the key files and directories:

### Main Files
- **`main.py`**: The game entry point. Initializes components and runs the main loop.

### Directories and Modules
- **`classes/`**: Contains the main gameplay classes:
  - `Vaisseau`: Manages the player's ship.
  - `Ennemi`: Handles enemy behavior and movement.
  - `Projectile`: Manages projectiles for both the player and enemies.
  - `Jeu`: Oversees global game logic (state updates, collisions, scoring, etc.).
  - `BDD`: Handles the database for saving scores, names, and dates.
  - `Camera`: Captures and processes hand movements for gesture recognition.
  - `Constants`: Defines global constants (e.g., sizes, enemy speed).
  - `FPSCounter`: Displays frames per second.
  - `Graphics`: Manages visual elements (enemies, ships, projectiles, animations).
  - `Parsers`: Detects skeletal joints and draws connections between them.
  - `Setup`: Prepares the Python project as a package.
  - `SkeletonTracker`: Detects the human skeleton for gesture-based interaction.
  - `Son`: Manages sound effects and music.
  - `SpaceInvader`: Manages the overall game structure.

- **`image/`**: Contains graphical assets (sprites for enemies, the ship, etc.).
- **`son/`**: Contains audio files for sound effects and background music.
- **`models/`**: Includes models for gesture detection using the SkeletonTracker.

---

## Technologies and Tools

- **Language**: Python (≥ 3.8)
- **Graphics Library**: Pygame
- **Gesture Recognition**: OpenCV
- **Recommended IDE**: Visual Studio Code
- **Version Control**: Git (GitLab)

---

## Installation

To run this project on your local machine, follow these steps:

1. **Clone the Git Repository**:  
   ```bash
   git clone git@gitlab.polytech.umontpellier.fr:julien.fabre05/projet-space-invader.git
   cd projet-space-invader

2. **Recreate the Conda Environment**:
   Ensure Anaconda or Miniconda is installed, then run:
   conda env create -f environment.yml

3. **Activate the Environment**:
   conda activate space_invader

4. **Run the game**:
   python main.py

## Authors and Contributions

This project was developed as part of an academic course by **Fabre Julien** and **Clément Frassier**. Special thanks to **Hartley Marc** for his assistance and the development of the **SkeletonTracker** functionality.



