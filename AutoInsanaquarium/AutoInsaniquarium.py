#project step 1: program will click on any pixels which are the color of a hungry fish

import pyautogui
import threading
import time
import win32api, win32con
from pynput.keyboard import Listener, KeyCode
from pynput.mouse import Controller, Button
import sys

#monitor dimensions are different because it's emulating a different monitor: 960 x 700
#note: not precise numbers but they get the job done
X_MAX = 960
Y_MAX = 700

Y_MIN = 200

clickCount = 0

#monitor dimensions of actual laptop
#X_MAX = 1080
#Y_MAX = 1920

#color of hungry fish: 
FISH_R = 209
FISH_G = 199
FISH_B = 0

#color of silver coin:
SILVER_COIN_R = 181
SILVER_COIN_G = 181
SILVER_COIN_B = 181

#color of gold coin:
GOLD_COIN_R = 247
GOLD_COIN_G = 181
GOLD_COIN_B = 49

#higher values make the color choices less picky
COLOR_PRECISION = 80

#toggles the program
TOGGLE_KEY = KeyCode(char = "t")

#press u to upgrade gun, food count, food quality, and buy a guppy, in that order
UPGRADE_KEY= KeyCode(char = "u")

#press 1 to buy the first type of fish (either guppy or breeder) 10 times
FISH_1_KEY = KeyCode(char = "1")

#press 2 to buy the second type of fish (usually carnivore) 30 times
FISH_2_KEY = KeyCode(char = "2")

#press 3 to buy the third type of fish (usually ultravore) 10 times
FISH_3_KEY = KeyCode(char = "3")

#press f to spam the center of the screen with food
FEED_KEY = KeyCode(char = "f")

#press c to focus on coin collecting (click on one row near the bottom of the screen)
COIN_COLLECT_KEY = KeyCode(char = "c")

#press p to print the number of times the program has clicked
PRINT_KEY = KeyCode(char = "p")

#press f to select the pets Meryl, Amp, and Presto
SELECT_PETS_KEY = KeyCode(char = "s")

#SPEED = 1 #number of seconds program waits before clicking again (not used at the moment)

clicking = True
feeding = False
collecting = False
mouse = Controller()

#wait 5 seconds to open insaniquarium

time.sleep(5)

def clicker():
    while True:
        if clicking:
            if not feeding and not collecting:
                #pic = pyautogui.screenshot(region = (0, Y_MIN, X_MAX, Y_MAX))
                #just click on a bunch of pixels which ends up both feeding fish and collecting coins
                for x in range (0, X_MAX, 100):
                    #if settings change in the middle of a sweep, program does not waste time continuing a sweep
                    if not clicking or feeding or collecting:
                        break
                    for y in range(Y_MIN, Y_MAX, 50):
                        mouseSetAndClick(x,y)

                        #r, g, b = pic.getpixel((x, y))    relic from when the program tried to read color 
                        #                                   values from the screen and click accordingly
                            
            elif feeding:
                feed()

            elif collecting:
                collect()

#program keys: 
#t toggles the clicking on and off
#u upgrades various ameneties and buys a guppy (if the player has enough coins)
#f places the cursor in one spot in the middle of the screen and clicks to feed the fish
#c makes the cursor follow a horizontal line along the bottom of the screen and click to collect as many coins as possible
#p prints the number of times the program has clicked
#2 buys fish 2 (usually carnivore) 30 times
#3 buys fish 3 (usually ultravore) 10 times

def toggleEvent(key):
    global feeding
    global collecting

    if key == TOGGLE_KEY:
        global clicking
        clicking = not clicking
    if key == UPGRADE_KEY:
        upgradeGun()#attmept to upgrade ameneties with the most expensive items first, then continue in descending order
        upgradeFood()
    if key == FEED_KEY:
        feeding = not feeding
        collecting = False
    if key == COIN_COLLECT_KEY:
        collecting = not collecting
        feeding = False
    if key == PRINT_KEY:
        print(clickCount)
    if key == SELECT_PETS_KEY:
        selectPets()

    if key == FISH_1_KEY or key == FISH_2_KEY or key == FISH_3_KEY:
        buyFish(key)



def mouseSetAndClick(x, y):
    win32api.SetCursorPos((x, y))

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0 ,0)
    time.sleep(0.001)#in case the click is too fast
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0 ,0)

    global clickCount
    clickCount+= 1


def buyGuppy():
    mouseSetAndClick(70, 50)

def upgradeFood():
    #upgrade food count, then quality
    mouseSetAndClick(240, 50)
    mouseSetAndClick(140, 50)

def upgradeGun():
    mouseSetAndClick(600, 50)

def feed():
    mouseSetAndClick(300, 200)

def buyFish(fish):
    if fish == FISH_1_KEY: #buy 10 guppys/breeders
        for i in range(10):
            mouseSetAndClick(70, 50)
    elif fish == FISH_2_KEY:#buy 30 carnivores/guppysnatchers
        for i in range(30):
            mouseSetAndClick(360, 50)
    elif fish == FISH_3_KEY:#buy 10 ultravores/beetlesnatchers
        for i in range(10):
            mouseSetAndClick(450, 50)


def collect():
    for x in range(0, X_MAX, 60):
        mouseSetAndClick(x, Y_MAX - 200)
    for x in range(30, X_MAX - 30, 60):
        mouseSetAndClick(x, Y_MAX - 150)

def selectPets():
    #click Meryl
    mouseSetAndClick(230, 450)

    #click Amp
    mouseSetAndClick(850, 200)

    #click Presto
    mouseSetAndClick(850, 600)


            

click_thread = threading.Thread(target = clicker)
click_thread.start()

with Listener(on_press = toggleEvent) as listener:
    listener.join()

#color searching function junkyard vvvvvvv

#def checkOneColor(colorToCheck, COLOR, PRECISION):
#    return colorToCheck in range(COLOR - PRECISION, COLOR + PRECISION)

#def checkRGB(rCheck, gCheck, bCheck, R, G, B, PRECISION):
#    return checkOneColor(rCheck, R, PRECISION) and checkOneColor(gCheck, G, PRECISION) and checkOneColor(bCheck, B, PRECISION)