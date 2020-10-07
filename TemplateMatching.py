# GUI Imports
import tkinter as tk
import threading
import sys


# Script Imports
import time
import cv2
import pyautogui as pgui
import numpy as np
import imutils

# Variables in global scope
sizeX, sizeY = pgui.size()  # Size of screen, used in screenshot function
method = cv2.TM_SQDIFF_NORMED  # Method to use when comparing captures
pgui.PAUSE = 0.05  # PyAutoGUI low delay

dictJailItems = {0:'img/normiefish.png', 1:'img/goldenfish.png', 2:'img/epicfish.png', 3:'img/epiccoin.png',
                 4:'img/lifepotion.png', 5:'img/ruby.png', 6:'img/coin.png', 7:'img/zombieeye.png',
                 8:'img/unicornhorn.png', 9:'img/mermaidhair.png', 10:'img/chip.png', 11:'img/dragonscale.png',
                 12:'img/apple.png', 13:'img/banana.png', 14:'img/wolfskin.png'}

dictJailItemsNames = {0:'Normie Fish', 1:'Golden Fish', 2:'Epic Fish', 3:'Epic Coin', 4:'Life Potion',
                      5:'Ruby', 6:'Coin', 7:'Zombie Eye', 8:'Unicorn Horn',
                      9:'Mermaid Hair', 10:'Chip', 11:'Dragon Scale', 12:'Apple', 13:'Banana', 14:'Wolf Skin'}

temp = cv2.imread("currentss/temp.png")

def jailTest():
    for x in dictJailItems:
        find = cv2.imread(dictJailItems.get(x))
        result = cv2.matchTemplate(find, currentCapture, method)
        itemConfidence = round((1 - np.amin(result)) * 100, 4)

        if itemConfidence >= 95:
            print('>' + dictJailItemsNames.get(x) + ' found!. \nConf: ' + str(itemConfidence) + '%.')
            #time.sleep(0.5)
            #pgui.write(str(dictJailItemsNames.get(x)), interval=0.11)
            #time.sleep(0.2)
            #pgui.press('enter')
            #time.sleep(1)
        else:
            print('>' + dictJailItemsNames.get(x) + ' NOT found!. \nConf: ' + str(itemConfidence) + '%.')

#jailTest()

def newJailTest():
    for scale in np.linspace(0.5, 2, 20)[::-1]:
        print(scale)
        find = cv2.imread('img/lifepotion.png')
        resized = imutils.resize(find, width=int(find.shape[1] * scale))
        result = cv2.matchTemplate(resized, temp, method)

        itemConfidence = round((1 - np.amin(result)) * 100, 4)

        if itemConfidence >= 90:
            print('>Banana found!. \nConf: ' + str(itemConfidence) + '%.')
            # time.sleep(0.5)
            # pgui.write(str(dictJailItemsNames.get(x)), interval=0.11)
            # time.sleep(0.2)
            # pgui.press('enter')
            # time.sleep(1)
        else:
            print('>Banana NOT found!. \nConf: ' + str(itemConfidence) + '%.')

newJailTest()