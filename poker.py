import re
import cv2 
import pytesseract 
import numpy as np

import Card

from subprocess import call, check_output, Popen, PIPE,  STDOUT
from pyautogui import position, locateOnScreen, screenshot

CARD_OFFSETS_RATIOS = [0.44,0.59]
CARD_SIZE_RATIOS = [0.12,0.07]
CARD_COLOR_RATIOS = [0.25,0.75]

def getWindowSize():
    pokerWindows = check_output(["GetWindowID", "PokerStarsEU", "--list"]).decode('UTF-8').splitlines()
    pokerWindows = [window for window in pokerWindows if "Logged In as" in window]

    pattern = r'size=([0-9]+)x([0-9]+)'
    sizes = [[re.search(pattern, pokerWindow).group(1),re.search(pattern, pokerWindow).group(2)] for pokerWindow in pokerWindows]
    size = [int(sizes[0][0])*2, int(sizes[0][1])*2] # Scale for pyautogui, doubles for some reason
    return size # for simplictity assume all the poker windows are around the same size

def getWindowLocation():
    instance = locateOnScreen('/Users/lukehackett/Documents/Poker/star.png', grayscale=True, confidence=.5)
    if instance != None:
        return [int(instance.left), int(instance.top)]
    return None

def calcCardScreenInfo(gameWindowSize, windowLocation):
    cardScreenInfo = {}

    #Card position
    cardXPos = windowLocation[0] + (gameWindowSize[0] * CARD_OFFSETS_RATIOS[0])
    cardYPos = windowLocation[1] + (gameWindowSize[1] * CARD_OFFSETS_RATIOS[1])
    cardScreenInfo['position'] = [cardXPos, cardYPos]

    #Card Size
    cardXSize = gameWindowSize[0] * CARD_SIZE_RATIOS[0]
    cardYSize = gameWindowSize[1] * CARD_SIZE_RATIOS[1]
    cardScreenInfo['size'] = [cardXSize, cardYSize]

    return cardScreenInfo

def readCardData(cardImg):
    # Get Card Ranks
    cardGray = cv2.cvtColor(cardImg, cv2.COLOR_BGR2GRAY)
    cardGray = ~cardGray
    cardGray = cv2.threshold(cardGray, 100, 255, cv2.THRESH_BINARY)[1]
    text = pytesseract.image_to_string(cardGray, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

    # Get Card Suits
    cardRgb = cv2.cvtColor(cardImg, cv2.COLOR_BGR2RGB)
    
    h, w, _ = cardRgb.shape
    colors = [cardRgb[int(h/2), int(w * CARD_COLOR_RATIOS[0])],cardRgb[int(h/2), int(w * CARD_COLOR_RATIOS[1])]]

    cardSuits = []
    # This is stupid below, need to change
    for color in colors:
        if color[0] > 150:
            cardSuits.append('heart')
            break
        if color[1] > 150:
            cardSuits.append('club')
            break
        if color[2] > 150:
            cardSuits.append('diamond')
            break
        else:
            cardSuits.append('spade')

    cards = []
    i=0
    for rank in text:
        cards.append(Card())
        cards[i].rank = rank
        cards[i].suit = cardSuits[i]
        i = i+1

    return cards

def gameLoop(size, windowLocation):
    while True:
        print(size)
        print(windowLocation)

#gameWindowSize = getWindowSize()
#windowLocation = getWindowLocation()
#cardScreenInfo = calcCardScreenInfo(gameWindowSize, windowLocation)

#gameLoop(gameWindowSize, windowLocation)
cardImg = cv2.imread('/Users/lukehackett/Documents/Poker/my_screenshot.png')
readCardData(cardImg)

'''
screenshot('my_screenshot.png', region=(cardScreenInfo['position'][0],
                                        cardScreenInfo['position'][1],
                                        cardScreenInfo['size'][0],
                                        cardScreenInfo['size'][1]))
'''