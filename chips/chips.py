# ========== LIBRARIES ========== #

import pygame as pg
from sys import exit


# ========== IMPORTS ========== #

from globals import *
from utils import *

from mouse import Mouse
from kb import Keyboard

from tile import Tile

from map import Map
from player import Player
from camera import Camera


# ========== GLOBAL METHODS ========== #

def INIT():
  debug_print('INITING')

  pg.init()
  pg.display.set_caption(SCREEN_WINDOW_TITLE)

  reset_global_data_structures()
  reset_global_vars()

  SINGLETONS[MOUSE] = Mouse()
  SINGLETONS[KEYBOARD] = Keyboard()

  SINGLETONS[CLOCK] = pg.time.Clock()

  SINGLETONS[TILE] = Tile()

  # must init before map
  SINGLETONS[PLAYER] = Player()

  SINGLETONS[MAP] = Map()

  SINGLETONS[CAMERA] = Camera()


  SCREEN.fill(COLOR_BACKGROUND)


def TOGGLE_PAUSE():
  game_paused = get_global_GAME_PAUSED()
  if game_paused:
    # debug_print('UNPAUSING')
    set_global_GAME_PAUSED(False)
  else:
    # debug_print('PAUSING')
    set_global_GAME_PAUSED(True)

def RESTART():
  debug_print('RESTARTING')
  INIT()

def QUIT():
  debug_print('QUITTING')
  pg.quit()
  exit()

def UPDATE_GAME_OVER():
  killing_entity = get_global_KILLING_ENTITY()
  game_over = SINGLETONS[PLAYER].dead \
                and SINGLETONS[PLAYER].move_time == None \
                and (killing_entity == None or killing_entity.move_time == None)
  if game_over: set_global_GAME_OVER(True)

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

def UPDATE_SINGLETONS(game_running):

  # Update state
  if (game_running):
    SINGLETONS[MAP].update()
    SINGLETONS[PLAYER].update()

  # Draw
  SINGLETONS[CAMERA].update()
  SINGLETONS[CAMERA].draw(SCREEN)

def handle_local_inputs():

  if INPUT_QUIT in INPUTS:
    debug_print('QUIT')
    QUIT()

  if INPUT_RESTART in INPUTS:
    debug_print('RESTART')
    RESTART()

  if INPUT_PAUSE in INPUTS:
    # debug_print('TOGGLE PAUSE')
    TOGGLE_PAUSE()
  

# ========== GAME LOOP ========== #

INIT()

while True:

  UPDATE_GAME_OVER()
  game_running = not get_global_GAME_PAUSED() and not get_global_GAME_OVER()

  GET_INPUTS()
  HANDLE_EVENTS()

  UPDATE_SINGLETONS(game_running)

  handle_local_inputs()

  INPUTS.clear()
  pg.display.update()
  set_dt(SINGLETONS[CLOCK].tick(FPS) * TIME_FACTOR)

  if game_running:
    dt = get_dt()
    GAME_TICKS = get_global_GAME_TICKS()
    set_global_GAME_TICKS(GAME_TICKS + dt)