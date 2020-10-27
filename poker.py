import re
import Cards
from subprocess import call, check_output, Popen, PIPE,  STDOUT
import numpy as np
from pyautogui import position, locateOnScreen, screenshot
import cv2 


CARD_OFFSETS_RATIOS = [0.44,0.59]
CARD_SIZE_RATIOS = [0.12,0.07]

RANK_TEMPLATES = Cards.load_ranks("/Users/lukehackett/Documents/Poker/cards/")
SUIT_TEMPLATES = Cards.load_suits("/Users/lukehackett/Documents/Poker/cards/")

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
    return 0

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