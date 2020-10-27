import numpy as np
import cv2
import time

class Card:
    def __init__(self):
        self.rank = "Placeholder" # Thresholded, sized rank image loaded from hard drive
        self.suit = "Placeholder"
