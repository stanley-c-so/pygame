import pygame as pg

# ========== LABELS ========== #

MOUSE = 'MOUSE'
KEYBOARD = 'KEYBOARD'
CLOCK = 'CLOCK'
TILE = 'TILE'
MAP_DATA = 'MAP_DATA'
MAP = 'MAP'
PLAYER = 'PLAYER'
CAMERA = 'CAMERA'

U = 'U'
L = 'L'
D = 'D'
R = 'R'

INPUT_QUIT = 'INPUT_QUIT'
INPUT_RESTART = 'INPUT_RESTART'
INPUT_UP = 'INPUT_UP'
INPUT_LEFT = 'INPUT_LEFT'
INPUT_DOWN = 'INPUT_DOWN'
INPUT_RIGHT = 'INPUT_RIGHT'


# ========== CONSTANTS ========== #

DEBUG = False
DEBUG = True

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1260, 900
SCREEN_WINDOW_TITLE = 'Chips'

# FPS
# FPS = 64
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


# ========== GLOBAL VARIABLES ========== #

dt = 0

ALL_EVENT_TYPES_DICT = {}

SINGLETONS = {}

INPUTS = set()


# ========== TESTING ========== #

def debug_print(*args):
  if DEBUG: print(f"{pg.time.get_ticks()} |", *args)