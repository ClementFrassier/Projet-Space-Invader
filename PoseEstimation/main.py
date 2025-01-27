import os

import cv2
import numpy as np

from SkeletonTracker import *
from FPSCounter import *
from Parsers import *
from GestionMain import handTracker

def main():
    EPSILON = 1
    video_path = 0 # "../ImageProcessing/BodyVideos/body9.mp4"
    cap = cv2.VideoCapture(video_path)
    fps = FPSCounter()

    params = SkeletonTrackerParameters()
    params.use_yolo = False
    params.use_body = False
    params.max_bodies = 1
    params.use_hands = True
    params.use_face = False
    params.hand_skip_frames = 0
    params.models_paths = "PoseEstimation/models"
    tracking = SkeletonTracker(params)

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        img = cv2.resize(img, (800, 600))
        img = cv2.flip(img, 1)

        tracking.update(img)

        tracker = handTracker()

        for hand in tracking.hands:
            img = hand.displaySkeleton(img)
            # Détection des mains
            coords = hand.skeleton()[0]
            current_position = coords[0]

            if current_position is not None:
                direction = tracker.detect_movement(current_position)
                # Affichage de la direction
                print(f"Direction du mouvement : {direction}")

            # Affichage des coordonnées
            print("Coordonnées des mains détectées :", coords)

        fps.update()
        img = fps.display(img)
        cv2.imshow("Resultat", img)
        key = cv2.waitKey(EPSILON) & 0xFF
        if key == ord("q") or key == 27:
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()