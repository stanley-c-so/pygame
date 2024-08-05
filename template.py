# ========== LIBRARIES ========== #

import pygame as pg
from sys import exit

# import math
# import os


# ========== IMPORTS ========== #



# ========== SINGLETON CLASSES ========== #

class Mouse():
  
  def __init__(self):
    self.mouse_pos = None
    self.pressed = False

  def update_mouse_pos(self):
    self.mouse_pos = pg.math.Vector2(pg.mouse.get_pos())

  def handle_left_click(self):
    if not pg.mouse.get_pressed()[0]:
      self.pressed = False
      return
    # if self.pressed:
    #   return
    self.pressed = True

  def update(self):
    self.update_mouse_pos()
    self.handle_left_click()

class Keyboard():

  def handle_keydown(self):
    if pg.KEYDOWN in ALL_EVENT_TYPES_DICT:
      for event in ALL_EVENT_TYPES_DICT[pg.KEYDOWN]:
        match event.key:
          case pg.K_ESCAPE:
            QUIT()
          case pg.K_r:
            RESTART()

  def handle_keypress(self):
    keys = pg.key.get_pressed()

  def update(self):
    self.handle_keydown()
    self.handle_keypress()


# ========== CONSTANTS ========== #

DEBUG = False
DEBUG = True

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 900
SCREEN_WINDOW_TITLE = 'Template'

# FPS
FPS = 60

# Colors
COLOR_BACKGROUND = 'black'

# Inputs


# Fonts
FONT_SIZE = 100

# Filesystem
# FS_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# Assets
# some_img = pg.image.load(FS_CURRENT_DIR + '\\' + 'img.png')
# img_scale = 1
# ASSETS_IMG_SURF = pg.transform.rotozoom(some_img, 0, img_scale)


# ========== TESTING ========== #

def debug_print(*args):
  if DEBUG: print(f"{pg.time.get_ticks()} |", *args)


# ========== GLOBAL METHODS ========== #

def DRAW_BACKGROUND():
  SCREEN.fill(COLOR_BACKGROUND)

def INIT():
  debug_print('INITING')
  DRAW_BACKGROUND()

def RESTART():
  debug_print('RESTARTING')
  INIT()

def QUIT():
  debug_print('QUITTING')
  pg.quit()
  exit()

def HANDLE_EVENTS():

  # Update events
  global ALL_EVENT_TYPES_DICT
  ALL_EVENT_TYPES_DICT.clear()
  for event in pg.event.get():
    ALL_EVENT_TYPES_DICT[event.type] = []
    ALL_EVENT_TYPES_DICT[event.type].append(event)

  # Handle global events
  if pg.QUIT in ALL_EVENT_TYPES_DICT:
    QUIT()


def UPDATE():

  # Mouse
  MOUSE.update()

  # Keyboard
  KEYBOARD.update()


# ========== GAME STATE VARIABLES ========== #

pg.init()
pg.display.set_caption(SCREEN_WINDOW_TITLE)

ALL_EVENT_TYPES_DICT = {}

MOUSE = Mouse()

KEYBOARD = Keyboard()

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FONT = pg.font.Font(None, FONT_SIZE)

CLOCK = pg.time.Clock()
dt = 0


# ========== GAME LOOP ========== #

INIT()
while True:
  HANDLE_EVENTS()
  UPDATE()
  pg.display.update()
  dt = CLOCK.tick(FPS) / 1000