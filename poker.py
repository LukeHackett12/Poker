import re
import cv2 
import pytesseract 
import numpy as np

from Card import Card
from subprocess import check_output
from pyautogui import locateOnScreen, screenshot

#These were on 3440 1440 monitor
OWN_CARD_OFFSETS_RATIOS = [0.22,0.26]
OWN_CARD_SIZE_RATIOS = [0.06,0.035]
FLOP_OFFSETS_RATIOS = [0.17,0.12]
FLOP_SIZE_RATIOS = [0.16,0.065]
CARD_COLOR_RATIOS = [0.25,0.75]
FLOP_COLOR_RATIOS = [0.16,0.32,0.5,0.66,0.84]

def getWindowSize():
    pokerWindows = check_output(["GetWindowID", "PokerStarsEU", "--list"]).decode('UTF-8').splitlines()
    pokerWindows = [window for window in pokerWindows if "Logged In as" in window]

    pattern = r'size=([0-9]+)x([0-9]+)'
    sizes = [[re.search(pattern, pokerWindow).group(1),re.search(pattern, pokerWindow).group(2)] for pokerWindow in pokerWindows]
    size = [int(sizes[0][0])*2, int(sizes[0][1])*2] # Scale for pyautogui, doubles for some reason
    return size # for simplictity assume all the poker windows are around the same size

def getWindowLocation():
    instance = locateOnScreen('/Users/lukehackett/Documents/Poker/target.png', grayscale=True, confidence=.5)
    if instance != None:
        return [int(instance.left), int(instance.top)]
    return None

def calcCardScreenInfo(gameWindowSize, windowLocation, offsetRatio, sizeRatio):
    cardScreenInfo = {}

    #Card position
    cardXPos = windowLocation[0] + (gameWindowSize[0] * offsetRatio[0])
    cardYPos = windowLocation[1] + (gameWindowSize[1] * offsetRatio[1])
    cardScreenInfo['position'] = [cardXPos, cardYPos]

    #Card Size
    cardXSize = gameWindowSize[0] * sizeRatio[0]
    cardYSize = gameWindowSize[1] * sizeRatio[1]
    cardScreenInfo['size'] = [cardXSize, cardYSize]

    return cardScreenInfo

def getCards(cardImg, colorRatio):
    h, w, _ = cardImg.shape

    cardGray = cv2.cvtColor(cardImg, cv2.COLOR_BGR2GRAY)
    cardGray = ~cardGray
    cardGray = cv2.threshold(cardGray, 80, 255, cv2.THRESH_BINARY)[1]
    cardGray = cv2.resize(cardGray, (w*3,h*3), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite('test.png', cardGray)
    text = pytesseract.image_to_string(cardGray, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=AJQK023456789').rstrip()

    # Get Card Suits
    cardRgb = cv2.cvtColor(cardImg, cv2.COLOR_BGR2RGB)
    colors = []
    for i in range(0,len(colorRatio)):
        colors.append(cardRgb[int((h/4) * 3), int(w * colorRatio[i])])

    cardSuits = []
    # This is stupid below, need to change
    for color in colors:
        if color[0] > 200 and color[1] < 200 and color[2] < 200:
            cardSuits.append('heart')
        else:
            if color[0] < 200 and color[1] < 200 and color[2] > 200:
                cardSuits.append('diamond')
            else:
                if color[0] < 50 and color[1] > 150 and color[2] < 200:
                    cardSuits.append('club')
                else:
                    cardSuits.append('spade')

    cards = []
    i=0
    for rank in text:
        cards.append(Card())
        if rank == '0':
            cards[i].rank = 'T'
        else:
            cards[i].rank = rank
        cards[i].suit = cardSuits[i]
        i = i+1

    return cards

def readCardData(ownCardScreenInfo, flopScreenInfo):
    # Get Card Ranks
    screenshot('my_screenshot.png', region=(ownCardScreenInfo['position'][0],
                                ownCardScreenInfo['position'][1],
                                ownCardScreenInfo['size'][0],
                                ownCardScreenInfo['size'][1]))

    cardImg = cv2.imread('/Users/lukehackett/Documents/Poker/my_screenshot.png')
    ownCards = getCards(cardImg, CARD_COLOR_RATIOS)

    screenshot('my_screenshot.png', region=(flopScreenInfo['position'][0],
                                flopScreenInfo['position'][1],
                                flopScreenInfo['size'][0],
                                flopScreenInfo['size'][1]))

    cardImg = cv2.imread('/Users/lukehackett/Documents/Poker/my_screenshot.png')
    flop = getCards(cardImg, FLOP_COLOR_RATIOS)

    return {'ownCards': ownCards, 'flop': flop}

def gameLoop(size, windowLocation):
    cardScreenInfo = calcCardScreenInfo(size, windowLocation, OWN_CARD_OFFSETS_RATIOS, OWN_CARD_SIZE_RATIOS)
    flopScreenInfo = calcCardScreenInfo(size, windowLocation, FLOP_OFFSETS_RATIOS, FLOP_SIZE_RATIOS)

    while True:
        cardImg = cv2.imread('/Users/lukehackett/Documents/Poker/my_screenshot.png')
        data = readCardData(cardScreenInfo, flopScreenInfo)
        cards = data['ownCards']
        for card in cards:
            print("card has rank {} with suit {}".format(card.rank, card.suit))
        print("_________________")

gameWindowSize = getWindowSize()
windowLocation = getWindowLocation()

gameLoop(gameWindowSize, windowLocation)


'''

'''
