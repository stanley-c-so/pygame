import pygame as pg
from sys import exit

# ========== CLASSES ========== #

class Mouse():
  
  def __init__(self):
    self.mouse_pos = None
    self.pressed = False

  def update_mouse_pos(self):
    self.mouse_pos = pg.math.Vector2(pg.mouse.get_pos())

  def handle_click(self):
    if not pg.mouse.get_pressed()[0]:
      self.pressed = False
      return
    if self.pressed:
      return
    self.pressed = True

  def update(self):
    self.update_mouse_pos()
    self.handle_click()

class Keyboard():

  def handle_keydown(self, event):
    match event.key:
      case pg.K_ESCAPE:
        QUIT()
      case pg.K_r:
        RESTART()


# ========== CONSTANTS ========== #

DEBUG = False
DEBUG = True

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 900

# FPS
FPS = 60

# Colors
BACKGROUND_COLOR = "Black"

# Inputs


# Fonts
FONT_SIZE = 100


# ========== TESTING ========== #

def debug_print(*args):
  if DEBUG: print(f"{pg.time.get_ticks()} |", *args)


# ========== GLOBAL METHODS ========== #

def draw_background():
  SCREEN.fill(BACKGROUND_COLOR)

def INIT():
  debug_print('INITING')
  draw_background()

def RESTART():
  debug_print('RESTARTING')
  INIT()

def QUIT():
  debug_print('QUITTING')
  pg.quit()
  exit()

def handle_events():
  for event in pg.event.get():
    match event.type:
      case pg.QUIT:
        QUIT()
      case pg.KEYDOWN:
        KEYBOARD.handle_keydown(event)

def update_objects():
  MOUSE.update()


# ========== GAME STATE VARIABLES ========== #

pg.init()

MOUSE = Mouse()

KEYBOARD = Keyboard()

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FONT = pg.font.Font(None, FONT_SIZE)

CLOCK = pg.time.Clock()
dt = 0


# ========== GAME LOOP ========== #

INIT()
while True:
  handle_events()
  update_objects()
  pg.display.update()
  dt = CLOCK.tick(FPS) / 1000