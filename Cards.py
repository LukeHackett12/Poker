import numpy as np
import cv2
import time

class TrainRank:
    def __init__(self):
        self.img = [] # Thresholded, sized rank image loaded from hard drive
        self.name = "Placeholder"

class TrainSuit:
    def __init__(self):
        self.img = [] # Thresholded, sized rank image loaded from hard drive
        self.name = "Placeholder"

def load_ranks(filepath):
    ranks = []
    i = 0
    
    for Rank in ['rank_2','rank_3','rank_4','rank_5','rank_6','rank_7','rank_8',
                 'rank_9','rank_10','rank_a','rank_j','rank_q','rank_k']:
        ranks.append(TrainRank())
        ranks[i].name = Rank
        filename = Rank + '.png'
        ranks[i].img = cv2.imread(filepath+filename, cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return ranks

def load_suits(filepath):
    """Loads suit images from directory specified by filepath. Stores
    them in a list of Train_suits objects."""

    suits = []
    i = 0
    
    for Suit in ['suit_club','suit_diamond','suit_heart','suit_spade']:
        suits.append(TrainSuit())
        suits[i].name = Suit
        filename = Suit + '.png'
        suits[i].img = cv2.imread(filepath+filename, cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return suits
