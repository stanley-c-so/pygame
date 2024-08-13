import pygame as pg

# ========== LABELS ========== #

MOUSE = 'MOUSE'
KEYBOARD = 'KEYBOARD'
CLOCK = 'CLOCK'
TILE = 'TILE'
MAP = 'MAP'
PLAYER = 'PLAYER'
CAMERA = 'CAMERA'

U = 'U'
L = 'L'
D = 'D'
R = 'R'

dir = 'dir'
impassable = 'impassable'

INPUT_QUIT = 'INPUT_QUIT'
INPUT_RESTART = 'INPUT_RESTART'
INPUT_PAUSE = 'INPUT_PAUSE'

INPUT_UP = 'INPUT_UP'
INPUT_LEFT = 'INPUT_LEFT'
INPUT_DOWN = 'INPUT_DOWN'
INPUT_RIGHT = 'INPUT_RIGHT'

ENTITY_CHIP = 'ENTITY_CHIP'
ENTITY_BUG = 'ENTITY_BUG'
ENTITY_PARAMECIUM = 'ENTITY_PARAMECIUM'
ENTITY_TANK = 'ENTITY_TANK'
ENTITY_BALL_PINK = 'ENTITY_BALL_PINK'
ENTITY_BALL_BLUE = 'ENTITY_BALL_BLUE'
ENTITY_GLIDER = 'ENTITY_GLIDER'
ENTITY_FIREBALL = 'ENTITY_FIREBALL'
ENTITY_TEETH = 'ENTITY_TEETH'
ENTITY_BLOB = 'ENTITY_BLOB'


# ========== CONSTANTS ========== #

DEBUG = False
DEBUG = True

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1260, 900
SCREEN_WINDOW_TITLE = 'Chips'
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# FPS
TIME_FACTOR = 1
# TIME_FACTOR = 0.5
# TIME_FACTOR = 0.25
FPS = 60

# Colors
COLOR_BACKGROUND = 'black'

# Inputs


# Fonts
pg.font.init()
FONT_SIZE = 100
FONT_NAME = 'Comic Sans MS'
FONT = pg.font.SysFont(FONT_NAME, FONT_SIZE)

# Filesystem
# FS_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# Assets
# some_img = pg.image.load(FS_CURRENT_DIR + '\\' + 'img.png')
# img_scale = 1
# ASSETS_IMG_SURF = pg.transform.rotozoom(some_img, 0, img_scale)


# ========== GLOBAL DATA STRUCTURES ========== #

ALL_EVENT_TYPES_DICT = {}

SINGLETONS = {}

INPUTS = set()


# ========== GLOBAL VARIABLES ========== #

dt = 0
def get_dt():
  return dt
def set_dt(t):
  global dt
  dt = t

GAME_TICKS = 0
def get_global_GAME_TICKS():
  return GAME_TICKS
def set_global_GAME_TICKS(ticks):
  global GAME_TICKS
  GAME_TICKS = ticks

GAME_PAUSED = False
def get_global_GAME_PAUSED():
  return GAME_PAUSED
def set_global_GAME_PAUSED(bool):
  global GAME_PAUSED
  GAME_PAUSED = bool

KILLING_ENTITY = None
def get_global_KILLING_ENTITY():
  return KILLING_ENTITY
def set_global_KILLING_ENTITY(entity):
  global KILLING_ENTITY
  KILLING_ENTITY = entity