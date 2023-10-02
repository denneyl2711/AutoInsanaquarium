#This program is an autoclicker which helps the user play PopCap's Insaniquarium.
#In the game, the user manages an aquarium. 
#They must feed their fish, collect coins which drop from their fish, and defend the tank from hungry aliens.

#This program was originally designed to scan for specific pixel values (color of coins, hungry fish, etc.) and click them, but now it clicks blindly.
#This results in a great increase in speed with minimal loss of efficiency/effectiveness.

#There are multiple clicking settings.
#1. Clicking
    #General purpose type of click. 
    #Clicks pixels throughout the entire tank, so it clicks coins and feeds hungry fish
#2. Feeding
    #Puts the cursor in one spot and only clicks there.
    #Does not collect many coins, but allows the fish to group together in one spot to feed.
    #Without this clicking type, fish would run around the tank chasing food, often dying before they reached it.
#3. Collecting
    #Scrapes the bottom of the screen, clicking only pixels in the lowest clickable part of the tank.
    #Usually the best way to collect a massive amount of coins.
    #May also be used to kill some aliens which only reside in the bottom of the tank

#This program also includes hotkeys to select pets, buy fish, and buy/upgrade food and weapons
    



import threading
import time
import win32api, win32con
from pynput.keyboard import Listener, KeyCode
from pynput.mouse import Controller, Button
import sys
import random

#monitor dimensions are different because it's emulating a different monitor: 960 x 700
#note: not precise numbers but they get the job done
X_MAX = 960
Y_MAX = 700

X_MIN = 0
Y_MIN = 200

PURCHASE_X = 40 #height of every purchase button (buy fish, upgrade gun, etc.)

#toggles the clicking on and off
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

#press s to select the pets Meryl, Amp, and Presto
SELECT_PETS_KEY = KeyCode(char = "s")

#press e to purchase an egg
EGG_KEY = KeyCode(char = "e")

clicking = True
feeding = False
collecting = False
mouse = Controller()
clickCount = 0

def clicker():
    while True:
        if clicking:
            if not feeding and not collecting:
                #just click on a bunch of pixels which ends up both feeding fish and collecting coins

                #offset the start by a small amount so it doesn't click in exactly the same spot every time (would miss some coins)
                offset = createOffset(20)
                for x in range (X_MIN - offset, X_MAX, 100):
                    #if settings change in the middle of a sweep, program does not waste time continuing a sweep
                    if not clicking or feeding or collecting:
                        break
                    for y in range(Y_MIN, Y_MAX, 50):
                        mouseSetAndClick(x,y)
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
#e buys an egg
#2 buys fish 2 (usually carnivore) 30 times
#3 buys fish 3 (usually ultravore) 10 times

def toggleEvent(key):
    global feeding
    global collecting
    global clicking

    if key == TOGGLE_KEY:
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
   
    if key == EGG_KEY:
        buyEgg()

def mouseSetAndClick(x, y):
    win32api.SetCursorPos((x, y))

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0 ,0)
    time.sleep(0.001)#in case the click is too fast
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0 ,0)

    global clickCount
    clickCount+= 1

def buyGuppy():
    mouseSetAndClick(70, PURCHASE_X)

def upgradeFood():
    #upgrade food count, then quality
    mouseSetAndClick(180, PURCHASE_X)
    mouseSetAndClick(100, PURCHASE_X)

def upgradeGun():
    mouseSetAndClick(380, PURCHASE_X)

def feed():
    mouseSetAndClick(300, 200)

def buyFish(fish):
    if fish == FISH_1_KEY: #buy 10 guppys/breeders
        for i in range(10):
            mouseSetAndClick(70, PURCHASE_X)
    elif fish == FISH_2_KEY:#buy 30 carnivores/guppysnatchers
        for i in range(30):
            mouseSetAndClick(230, PURCHASE_X)
    elif fish == FISH_3_KEY:#buy 10 ultravores/beetlesnatchers
        for i in range(10):
            mouseSetAndClick(320, PURCHASE_X)
            
def buyEgg():
    mouseSetAndClick(460, PURCHASE_X)


def collect():
    offset = createOffset(20)

    for x in range(X_MIN - offset, X_MAX, 60):
        mouseSetAndClick(x, Y_MAX - 350 - offset)

#user can select three pets before the start of the game. My personal favorite three pets are hard-coded here
def selectPets():
    #click Meryl
    mouseSetAndClick(230, 450)

    #click Amp
    mouseSetAndClick(850, 200)

    #click Presto
    mouseSetAndClick(850, 600)

def createOffset(range):
    return random.randint(0, range)
    
def main():
    time.sleep(5) #give user time to navigate to the game- before clicking starts
    click_thread = threading.Thread(target = clicker)
    click_thread.start()

    with Listener(on_press = toggleEvent) as listener:
        listener.join()
        
if __name__ == '__main__':
    main()