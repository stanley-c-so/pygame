# from constants import *

# ========== GLOBAL DATA STRUCTURES ========== #

ALL_EVENT_TYPES_DICT = {}

SINGLETONS = {}

INPUTS = set()

def reset_global_data_structures():
  ALL_EVENT_TYPES_DICT.clear()
  SINGLETONS.clear()
  INPUTS.clear()

# ========== GLOBAL VARIABLES ========== #

dt = 0
def get_dt(): return dt
def set_dt(t):
  global dt
  dt = t

GAME_TICKS = 0
def get_global_GAME_TICKS(): return GAME_TICKS
def set_global_GAME_TICKS(ticks):
  global GAME_TICKS
  GAME_TICKS = ticks

GAME_PAUSED = False
def get_global_GAME_PAUSED(): return GAME_PAUSED
def set_global_GAME_PAUSED(bool):
  global GAME_PAUSED
  GAME_PAUSED = bool

GAME_OVER = False
def get_global_GAME_OVER(): return GAME_OVER
def set_global_GAME_OVER(bool):
  global GAME_OVER
  GAME_OVER = bool

KILLING_ENTITY = None
def get_global_KILLING_ENTITY(): return KILLING_ENTITY
def set_global_KILLING_ENTITY(entity):
  global KILLING_ENTITY
  KILLING_ENTITY = entity

KILLING_HAZARD = None
def get_global_KILLING_HAZARD(): return KILLING_HAZARD
def set_global_KILLING_HAZARD(hazard):
  global KILLING_HAZARD
  KILLING_HAZARD = hazard

def reset_global_vars():
  set_global_GAME_TICKS(0)
  set_global_GAME_PAUSED(False)
  set_global_GAME_OVER(False)
  set_global_KILLING_ENTITY(None)
  set_global_KILLING_HAZARD(None)