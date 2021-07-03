#!/usr/bin/env python3

# Herein are bits of code for manipulating or measuring
# keyboard and mouse input/output

# https://pypi.org/project/pynput/

import pynput
import math
import time

#####################################
####     Produce Mouse Events    ####
#####################################
from pynput.mouse import Button

mouse = pynput.mouse.Controller()

def moveMouseTo(x,y):
    allowBreak()
    mouse.position = (x,y)

def clickLeftMouse():
    allowBreak()
    mouse.press(Button.left)
    mouse.release(Button.left)

def clickAt(x,y, delayMs=10, debug=False):
    if debug:
        for i in range(int(delayMs/10)):
            time.sleep(.01)
            moveMouseTo(int(x+3*math.sin(i)),
                        int(y+3*math.cos(i)))
    moveMouseTo(x,y)
    clickLeftMouse()
    #time.sleep(0.05)

def dragMouse(xy1, xy2, speed=100):
    allowBreak()
    mouse.position=xy1
    mouse.press(Button.left)
    xtrack = range(xy1[0],xy2[0],speed)
    for i in range(0,101,speed):
        print(i)
        mouse.position = (
            int((xy1[0]*(100-i)+i*xy2[0])/100),
            int((xy1[1]*(100-i)+i*xy2[1])/100)
        )
        time.sleep(.1)
    mouse.position = xy2
    mouse.release(Button.left)

######### Tools ##############

mouse_position_last = mouse.position
is_mouse_moving = False
def clickOnStop(interval_sec, cooldown_sec=1):
    global mouse_position_last, is_mouse_moving
    while(not breakKeyPressed()):
        if is_mouse_moving:
            if mouse.position == mouse_position_last:
                clickLeftMouse()
                is_mouse_moving = False
                time.sleep(cooldown_sec)
        else:
            if mouse.position != mouse_position_last:
                is_mouse_moving = True
                time.sleep(cooldown_sec)

        mouse_position_last = mouse.position
        time.sleep(interval_sec)


def clickLoop(interval_sec):
    while True:
        time.sleep(interval_sec)
        pynputIO.clickLeftMouse()

##################################
####     Read Mouse Events    ####
##################################

def getCursorPosition():
    return mouse.position[0], mouse.position[1]

def printCursorPositionForever():
    while True:
        print(getCursorPosition())
        time.sleep(1)


def printCursorPositionOnClick():
    listener = pynput.mouse.Listener(on_click=print)
    listener.start()


#####################################
####   Produce Keyboard Events   ####
#####################################
from pynput.keyboard import Key

# Keycode reference: http://www.flint.jp/misc/?q=dik&lang=en

keyboard = pynput.keyboard.Controller()

def pressKey(key):
    allowBreak()
    keyboard.press(key)
    keyboard.release(key)

def typeStr(string):
    allowBreak()
    keyboard.type(string)
    
keyCodes = {}

####################################
####   Detect Keyboard Events   ####
####################################
from collections import defaultdict

### Allow events/loops to break out on escape
breakKey = Key.esc
continueKey = Key.tab

global keyState
keyState = defaultdict(bool)

def breakKeyPressed():
    return keyState[breakKey]

def allowBreak():
    global keyState
    if keyState[breakKey]:
        while(keyState[breakKey]):
            x=3
        raise KeyboardInterrupt("Escape key detected")

def waitForContinue():
    global keyState
    while(not keyState[continueKey]):
        time.sleep(.01)
    while(keyState[continueKey]):
        time.sleep(.01)
            

keyStateListener = pynput.keyboard.Listener(
    on_press=  (lambda k: keyState.__setitem__(k,True)),
    on_release=(lambda k: keyState.__setitem__(k,False))
)
keyStateListener.start()

global customKeyMap
customMap = {}
def triggerCustomKeyMap(key):
    global customMap
    customMap.get(key,lambda k:k)(key)
def attachFunctionToKey(function, key):
    global customMap
    customMap[key]=function

customKeyListener = pynput.keyboard.Listener(
    on_release=triggerCustomKeyMap
)
customKeyListener.start()

### Debug output
if __name__ == "__main__":
    debugListener = pynput.keyboard.Listener(on_press=print)
    #debugListener.start()

if __name__ == "__main__":
    #printCursorPositionOnClick()
    #printCursorPositionForever()
    x = 3
