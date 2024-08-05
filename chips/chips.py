# ========== LIBRARIES ========== #

import pygame as pg
from sys import exit


# ========== IMPORTS ========== #

from globals import *

from mouse import Mouse
from kb import Keyboard

from map_data import MapData
from tile import Tile

from map import Map
from player import Player
from camera import Camera


# ========== GLOBAL METHODS ========== #

def DRAW_BACKGROUND():
  SCREEN.fill(COLOR_BACKGROUND)

def INIT():
  debug_print('INITING')
  DRAW_BACKGROUND()

  # CAMERA.sprite.init()
  # MAP.init()
  # PLAYER.init()

  # debug_print(TILE)
  # debug_print(TILE.surfaces)

def RESTART():
  debug_print('RESTARTING')
  INIT()

def QUIT():
  debug_print('QUITTING')
  pg.quit()
  exit()

def HANDLE_EVENTS():

  # Update events
  # global ALL_EVENT_TYPES_DICT
  ALL_EVENT_TYPES_DICT.clear()
  for event in pg.event.get():
    ALL_EVENT_TYPES_DICT[event.type] = []
    ALL_EVENT_TYPES_DICT[event.type].append(event)
    # print(ALL_EVENT_TYPES_DICT)
  # print(pg.QUIT)

  # Handle global events
  if pg.QUIT in ALL_EVENT_TYPES_DICT:
    QUIT()


def UPDATE():

  # Get inputs
  SINGLETONS[MOUSE].update()
  SINGLETONS[KEYBOARD].update()
  SINGLETONS[PLAYER].get_inputs()

  # Update state
  SINGLETONS[MAP].update()
  SINGLETONS[PLAYER].update()

  # # Draw
  SINGLETONS[CAMERA].update()
  SINGLETONS[CAMERA].draw(SCREEN)


# ========== START UP ROUTINES ========== #

pg.init()
pg.display.set_caption(SCREEN_WINDOW_TITLE)
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# FONT = pg.font.Font(None, FONT_SIZE)

SINGLETONS[MOUSE] = Mouse()

SINGLETONS[KEYBOARD] = Keyboard({
  "QUIT": QUIT,
  "RESTART": RESTART,
})

SINGLETONS[CLOCK] = pg.time.Clock()

SINGLETONS[TILE] = Tile()

SINGLETONS[MAP_DATA] = MapData()
SINGLETONS[MAP] = Map()

SINGLETONS[PLAYER] = Player()

SINGLETONS[CAMERA] = pg.sprite.GroupSingle()
SINGLETONS[CAMERA].add(Camera())


# ========== GAME LOOP ========== #

INIT()
while True:
  HANDLE_EVENTS()
  UPDATE()
  pg.display.update()
  dt = SINGLETONS[CLOCK].tick(FPS)