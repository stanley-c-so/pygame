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

def INIT():
  debug_print('INITING')

  pg.init()
  pg.display.set_caption(SCREEN_WINDOW_TITLE)
  # FONT = pg.font.Font(None, FONT_SIZE)

  SINGLETONS[MOUSE] = Mouse()
  SINGLETONS[KEYBOARD] = Keyboard()

  SINGLETONS[CLOCK] = pg.time.Clock()

  SINGLETONS[TILE] = Tile()

  # must init before map
  SINGLETONS[PLAYER] = Player()

  SINGLETONS[MAP_DATA] = MapData()
  SINGLETONS[MAP] = Map()

  SINGLETONS[CAMERA] = Camera()

  # SINGLETONS[CAMERA].init()
  # SINGLETONS[MAP].init()
  # SINGLETONS[PLAYER].init()

  SCREEN.fill(COLOR_BACKGROUND)


def RESTART():
  debug_print('RESTARTING')
  INIT()

def QUIT():
  debug_print('QUITTING')
  pg.quit()
  exit()

def GET_INPUTS():

  # Get inputs
  SINGLETONS[MOUSE].update()
  SINGLETONS[KEYBOARD].update()

def HANDLE_EVENTS():

  # Update events
  ALL_EVENT_TYPES_DICT.clear()
  for event in pg.event.get():
    ALL_EVENT_TYPES_DICT[event.type] = []
    ALL_EVENT_TYPES_DICT[event.type].append(event)

  # Handle global events
  if pg.QUIT in ALL_EVENT_TYPES_DICT:
    QUIT()

def UPDATE_SINGLETONS():

  # Update state
  SINGLETONS[MAP].update()
  SINGLETONS[PLAYER].update()

  # Draw
  SINGLETONS[CAMERA].update()
  SINGLETONS[CAMERA].draw(SCREEN)

def handle_inputs():

  if INPUT_QUIT in INPUTS:
    debug_print('QUIT')
    QUIT()

  if INPUT_RESTART in INPUTS:
    debug_print('RESTART')
    RESTART()


# ========== GAME LOOP ========== #

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
INIT()
while True:
  GET_INPUTS()
  HANDLE_EVENTS()
  UPDATE_SINGLETONS()
  handle_inputs()
  INPUTS.clear()
  pg.display.update()
  dt = SINGLETONS[CLOCK].tick(FPS)