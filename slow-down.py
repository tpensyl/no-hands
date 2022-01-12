#!/usr/bin/env python3

import argparse
import pynput
import time

DEFAULT_WPM = 40
BUFFER_S = 1 # seconds

####### PARSE
parser = argparse.ArgumentParser(description='Yell at you when you type too fast.')
parser.add_argument('--wpm', action='store', type=int, default=DEFAULT_WPM,
                    help='Maximum typing speed in wpm')
args = parser.parse_args()

MAX_STROKES_PER_SECOND = args.wpm * 5 / 60
MAX_TYPING_SLICE = 1. / MAX_STROKES_PER_SECOND

####### RATE LIMITER
global nextAllowedKeyStroke
nextAllowedKeyStroke = time.time()
def rateLimit(k):
	global nextAllowedKeyStroke
	t = time.time()
	#print(t, nextAllowedKeyStroke)
	if nextAllowedKeyStroke > t + BUFFER_S:
		nextAllowedKeyStroke = t + BUFFER_S
		print("\a")
	else:
		nextAllowedKeyStroke = max(nextAllowedKeyStroke, time.time()) + MAX_TYPING_SLICE

def start():
	keyStateListener = pynput.keyboard.Listener(
	    on_press=rateLimit
	    #on_release=rateLimit
	)
	keyStateListener.start()

	while(True):
		time.sleep(5) # long-living process

start()

