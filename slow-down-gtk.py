#!/usr/bin/env python3

import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GObject
import time
from threading import Thread

def color(pct, onPct):
	if pct >= onPct:
		return "🖤"
	elif pct >= .75:
		return "❤️"
	elif pct >= .5:
		return "💛"
	else:
		return "💚"

def progressBar(size, frac):
	frac = min(max(frac,0),1)
	onPixels = int(size * frac)
	offPixels = size - onPixels
	return ''.join(color(p/size, frac) for p in range(size))
	#return ("\u2588"*onPixels) + ("\u2591"*offPixels) + "🔴"

#https://askubuntu.com/questions/751608/how-can-i-write-a-dynamically-updated-panel-app-indicator
class Indicator():
	def __init__(self):
		self.app = 'slow-down'
		iconpath = '/snap/gnome-3-34-1804/77/usr/share/icons/hicolor/16x16/apps/preferences-color.pngg'
		iconpath = '/home/tommy/Downloads/keyboard.png'
		self.indicator = AppIndicator3.Indicator.new(self.app, iconpath, AppIndicator3.IndicatorCategory.OTHER)
		self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		self.indicator.set_menu(self.create_menu())

		self.size = 20
		self.indicator.set_label(progressBar(self.size,0), self.app)

		self.update = Thread(target=self.update_thread)
		self.update.setDaemon(True)
		self.update.start()

	def create_menu(self):
		menu = Gtk.Menu()
		# menu item 1
		item_1 = Gtk.MenuItem('Menu item')
		# item_about.connect('activate', self.about)
		menu.append(item_1)
		# separator
		menu_sep = Gtk.SeparatorMenuItem()
		menu.append(menu_sep)
		# quit
		item_quit = Gtk.MenuItem('Quit')
		item_quit.connect('activate', self.stop)
		menu.append(item_quit)

		menu.show_all()
		return menu

	def stop(self, source):
		Gtk.main_quit()

	def updatee(self, frac):
		GObject.idle_add(
			self.indicator.set_label,
			" " + progressBar(self.size, frac),
			self.app, priority=GObject.PRIORITY_DEFAULT
			)

	def update_thread(self):
		global indicator
		thresh = 0
		while(True):
			time.sleep(.1)
			thresh = calcThresh()
			indicator.updatee(thresh)


#######################
import argparse
import pynput
import time

DEFAULT_WPM = 40
BUFFER_S = 2 # seconds

####### PARSE
parser = argparse.ArgumentParser(description='Yell at you when you type too fast.')
parser.add_argument('--wpm', action='store', type=int, default=DEFAULT_WPM,
                    help='Maximum typing speed in wpm')
args = parser.parse_args()

MAX_STROKES_PER_SECOND = args.wpm * 5 / 60
MAX_TYPING_SLICE = 1. / MAX_STROKES_PER_SECOND

####### RATE LIMITER
nextAllowedKeyStroke = time.time()
thresh = 0
def calcThresh():
	global nextAllowedKeyStroke
	t = time.time()
	return (nextAllowedKeyStroke - t) / BUFFER_S;

indicator = Indicator()

def rateLimit(k):
	global nextAllowedKeyStroke
	thresh = calcThresh()

	indicator.updatee(thresh)

	t = time.time()
	if thresh > 1:
		nextAllowedKeyStroke = t + BUFFER_S
		print("\a")
	else:
		#print(nextAllowedKeyStroke, MAX_TYPING_SLICE)
		nextAllowedKeyStroke = max(nextAllowedKeyStroke, time.time()) + MAX_TYPING_SLICE

def startListener():
	keyStateListener = pynput.keyboard.Listener(
	    on_press=rateLimit
	    #on_release=rateLimit
	)
	keyStateListener.start()

startListener()


signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()


