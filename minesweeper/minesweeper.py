# ========== LIBRARIES ========== #

import pygame as pg
from sys import exit
import math
import random
import os


# ========== CLASSES ========== #

class Mouse():
  
  def __init__(self):
    self.mouse_pos = None
    self.mouse_row = None
    self.mouse_col = None
    self.left_pressed = False
    self.middle_pressed = False
    self.right_pressed = False

  def update(self):
    self.update_mouse_pos()
    self.update_mouse_coords()
    self.handle_left_click()
    self.handle_middle_click()
    self.handle_right_click()

  def update_mouse_pos(self):
    self.mouse_pos = pg.math.Vector2(pg.mouse.get_pos()) - GRID.sprite.rect.topleft

  def handle_left_click(self):
    if not pg.mouse.get_pressed()[0]:
      self.left_pressed = False
      return
    if self.left_pressed:
      return
    self.left_pressed = True
    GRID.sprite.handle_left_click()

  def handle_middle_click(self):
    if not pg.mouse.get_pressed()[1]:
      self.middle_pressed = False
      return
    if self.middle_pressed:
      return
    self.middle_pressed = True
    GRID.sprite.handle_middle_click()

  def handle_right_click(self):
    if not pg.mouse.get_pressed()[2]:
      self.right_pressed = False
      return
    if self.right_pressed:
      return
    self.right_pressed = True
    GRID.sprite.handle_right_click()

  def mouse_in_bounds(self):
    return self.mouse_pos.x >= 0 and self.mouse_pos.x < GRID_SQUARE_SIZE * WIDTH and self.mouse_pos.y >= 0 and self.mouse_pos.y < GRID_SQUARE_SIZE * HEIGHT

  def update_mouse_coords(self):
    if self.mouse_in_bounds():
      self.mouse_row = math.floor(self.mouse_pos.y / GRID_SQUARE_SIZE)
      self.mouse_col = math.floor(self.mouse_pos.x / GRID_SQUARE_SIZE)
    else:
      self.mouse_row = None
      self.mouse_col = None


class Keyboard():

  def handle_keydown(self, event):
    match event.key:
      case pg.K_ESCAPE:
        QUIT()
      case pg.K_r:
        RESTART()

class Grid(pg.sprite.Sprite):

  def __init__(self):
    super().__init__()

    # Set image, rect
    self.image = pg.Surface((GRID_SQUARE_SIZE * WIDTH, GRID_SQUARE_SIZE * HEIGHT), pg.SRCALPHA)
    self.rect = self.image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    # Create lines surface
    self.surface_lines = pg.Surface((GRID_SQUARE_SIZE * WIDTH, GRID_SQUARE_SIZE * HEIGHT), pg.SRCALPHA)
    for i in range(1, WIDTH):
      pg.draw.line(self.surface_lines, COLOR_GRID_LINE, (GRID_SQUARE_SIZE * i, 0), (GRID_SQUARE_SIZE * i, GRID_SQUARE_SIZE * HEIGHT), GRID_LINE_THICKNESS)
    for i in range(1, HEIGHT):
      pg.draw.line(self.surface_lines, COLOR_GRID_LINE, (0, GRID_SQUARE_SIZE * i), (GRID_SQUARE_SIZE * WIDTH, GRID_SQUARE_SIZE * i), GRID_LINE_THICKNESS)

    self.reset()

  def update(self):
    self.draw_background()
    self.draw_cell_background()
    self.draw_numbers()
    self.draw_lines()

  def draw_background(self):
    self.image.fill(COLOR_GRID)

  def draw_cell_background(self):
    for row in range(HEIGHT):
      for col in range(WIDTH):
        color = None
        if not self.grid[row][col]['explored']:
          color = COLOR_CELL_UNEXPLORED
        elif self.grid[row][col]['mine']:
          color = COLOR_CELL_MINE
        else:
          color = COLOR_CELL_EXPLORED
        cell_background_surf = pg.Surface((GRID_SQUARE_SIZE, GRID_SQUARE_SIZE), pg.SRCALPHA)
        cell_background_surf.fill(color)
        self.image.blit(cell_background_surf, (GRID_SQUARE_SIZE * col, GRID_SQUARE_SIZE * row))

  def draw_numbers(self):
    for row in range(HEIGHT):
      for col in range(WIDTH):
        if self.playing and not self.grid[row][col]['explored'] and not self.grid[row][col]['flagged']: continue
        if not self.grid[row][col]['mine'] and not self.grid[row][col]['explored'] and not self.grid[row][col]['flagged']: continue

        if self.grid[row][col]['flagged']:
          self.image.blit(FLAG_SURF, FLAG_SURF.get_rect(center=((col + 0.5) * GRID_SQUARE_SIZE, (row + 0.5) * GRID_SQUARE_SIZE)))
        elif self.grid[row][col]['mine']:
          self.image.blit(MINE_SURF, MINE_SURF.get_rect(center=((col + 0.5) * GRID_SQUARE_SIZE, (row + 0.5) * GRID_SQUARE_SIZE)))
        else:
          text = f"{self.grid[row][col]['num']}" if self.grid[row][col]['num'] else ''
          color = COLOR_TEXT_NUMBERS[self.grid[row][col]['num']]
          num_surf = FONT.render(text, False, color)
          num_rect = num_surf.get_rect(center=((col + 0.5) * GRID_SQUARE_SIZE, (row + 0.5) * GRID_SQUARE_SIZE))
          self.image.blit(num_surf, num_rect)

  def draw_lines(self):
    self.image.blit(self.surface_lines, (0, 0))

  def reset(self):
    self.grid = [ [{ 'explored': False, 'mine': False, 'num': 0, 'flagged': False } for _ in range(WIDTH) ] for _ in range(HEIGHT) ]
    self.first_click = None
    self.playing = True
    self.explored_count = 0
    self.flagged_count = 0
  
  def spawn_mines(self):
    for _ in range(MINE_COUNT):
      row, col = self.first_click
      while ((row, col) == self.first_click or self.grid[row][col]['mine']):
        row = random.randint(0, HEIGHT - 1)
        col = random.randint(0, WIDTH - 1)
      self.grid[row][col]['mine'] = True

  def generate_puzzle(self):
    self.spawn_mines()
    for row in range(HEIGHT):
      for col in range(WIDTH):
        num = 0
        for dy in range(-1, 2):
          for dx in range(-1, 2):
            if (dy, dx) != (0, 0) and \
              row + dy >= 0 and row + dy < HEIGHT and \
              col + dx >= 0 and col + dx < WIDTH and \
              self.grid[row + dy][col + dx]['mine']:
              num += 1
        self.grid[row][col]['num'] = num
    debug_print(f"NUMBER OF MINES: {MINE_COUNT}")

  def explore(self, row, col):
    stack = [(row, col)]
    while stack:
      r, c = stack.pop()
      if self.grid[r][c]['explored']: continue
      self.grid[r][c]['explored'] = True
      self.explored_count += 1
      self.grid[r][c]['flagged'] = False
      if self.grid[row][col]['mine']:
        self.lose()
        return
      if self.explored_count == HEIGHT * WIDTH - MINE_COUNT:
        self.win()
        return
      if self.grid[r][c]['num'] == 0:
        for dy in range(-1, 2):
          for dx in range(-1, 2):
            if (dy, dx) != (0, 0) and \
              r + dy >= 0 and r + dy < HEIGHT and \
              c + dx >= 0 and c + dx < WIDTH:
              stack.append((r + dy, c + dx))
    debug_print(f"EXPLORED COUNT: {self.explored_count}")
    debug_print(f"REMAINING SQUARES TO EXPLORE: {HEIGHT * WIDTH - MINE_COUNT - self.explored_count}")
    debug_print(f"UNFLAGGED MINES: {MINE_COUNT - self.flagged_count}")

  def toggle_flagged(self, row, col):
    # Guard when square is already explored
    if self.grid[row][col]['explored']:
      debug_print("can't toggle flagged: square already explored")
      return

    self.grid[row][col]['flagged'] = not self.grid[row][col]['flagged']
    if self.grid[row][col]['flagged']: self.flagged_count += 1
    else: self.flagged_count -= 1
    debug_print(f"UNFLAGGED MINES: {MINE_COUNT - self.flagged_count}")

  def explore_neighbors(self, row, col):
    # Guard when square is not yet explored
    if not self.grid[row][col]['explored']:
      debug_print(f"can't explore neighbors: square not yet explored")
      return
    # Guard when square is empty
    if self.grid[row][col]['num'] == 0:
      debug_print(f"can't explore neighbors: square is empty")
      return
    # Guard when neighboring flag count does not match number itself
    neighboring_flags = 0
    for dy in range(-1, 2):
      for dx in range(-1, 2):
        if (dy, dx) != (0, 0) and \
          row + dy >= 0 and row + dy < HEIGHT and \
          col + dx >= 0 and col + dx < WIDTH and \
          self.grid[row + dy][col + dx]['flagged']:
          neighboring_flags += 1
    if neighboring_flags != self.grid[row][col]['num']:
      debug_print(f"can't explore neighbors: invalid neighboring flag count")
      return

    for dy in range(-1, 2):
      for dx in range(-1, 2):
        if (dy, dx) != (0, 0) and \
          row + dy >= 0 and row + dy < HEIGHT and \
          col + dx >= 0 and col + dx < WIDTH and \
          not self.grid[row + dy][col + dx]['flagged']:
          self.explore(row + dy, col + dx)

  def lose(self):
    debug_print('YOU LOSE, SUCKER')
    self.playing = False

  def win(self):
    debug_print('YOU WIN, CONGRATS!')
    self.playing = False

  def handle_left_click(self):
    # debug_print(f"GRID handle_left_click")
    # debug_print(f"MOUSE COORDS: row {MOUSE.mouse_row} col {MOUSE.mouse_col}")
    # debug_print(f"MOUSE IN BOUNDS?: {MOUSE.mouse_in_bounds()}")

    row, col = MOUSE.mouse_row, MOUSE.mouse_col
    
    # Guard when not playing
    if not self.playing: return
    # Guard when out of bounds
    if not MOUSE.mouse_in_bounds(): return
    # Guard when square is already explored
    if self.grid[row][col]['explored']: return
    # Guard when square is flagged
    if self.grid[row][col]['flagged']: return

    # First click
    if self.first_click == None:
      self.first_click = (row, col)
      self.generate_puzzle()

    self.explore(row, col)

  def handle_middle_click(self):
    # debug_print(f"GRID handle_middle_click")
    # debug_print(f"MOUSE COORDS: row {MOUSE.mouse_row} col {MOUSE.mouse_col}")
    # debug_print(f"MOUSE IN BOUNDS?: {MOUSE.mouse_in_bounds()}")

    row, col = MOUSE.mouse_row, MOUSE.mouse_col

    # Guard when not playing
    if not self.playing: return
    # Guard when out of bounds
    if not MOUSE.mouse_in_bounds(): return

    self.explore_neighbors(row, col)

  def handle_right_click(self):
    # debug_print(f"GRID handle_right_click")
    # debug_print(f"MOUSE COORDS: row {MOUSE.mouse_row} col {MOUSE.mouse_col}")
    # debug_print(f"MOUSE IN BOUNDS?: {MOUSE.mouse_in_bounds()}")

    row, col = MOUSE.mouse_row, MOUSE.mouse_col

    # Guard when not playing
    if not self.playing: return
    # Guard when out of bounds
    if not MOUSE.mouse_in_bounds(): return
    # Guard when square is already explored
    if self.grid[row][col]['explored']: return
    
    self.toggle_flagged(row, col)


# ========== CONSTANTS ========== #

DEBUG = False
DEBUG = True

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 900
# SCREEN_WIDTH, SCREEN_HEIGHT = 675, 900
WINDOW_TITLE = 'Minesweeper'

# FPS
FPS = 60

# Colors
COLOR_BACKGROUND = 'black'
COLOR_GRID = 'white'
COLOR_GRID_LINE = (127, 127, 127, 255)
COLOR_CELL_UNEXPLORED = (207, 207, 207)
COLOR_CELL_EXPLORED = (223, 223, 223)
COLOR_CELL_MINE = (255, 0, 0)
COLOR_TEXT_FLAGGED = 'hotpink'
COLOR_TEXT_MINE = 'black'
COLOR_TEXT_NUMBERS = {
  0: 'black',
  1: 'blue',
  2: 'green',
  3: 'red',
  4: 'navy',
  5: 'maroon',
  6: 'teal',
  7: 'black',
  8: 'dimgray',
}

# Grid
HEIGHT, WIDTH = 20, 20
# HEIGHT, WIDTH = 5, 5
# HEIGHT, WIDTH = 40, 40
RATIO_OF_GRID_SIZE_TO_SCREEN = 0.9
GRID_SQUARE_SIZE = math.floor(min(SCREEN_HEIGHT * RATIO_OF_GRID_SIZE_TO_SCREEN / HEIGHT, SCREEN_WIDTH * RATIO_OF_GRID_SIZE_TO_SCREEN / WIDTH))
GRID_LINE_THICKNESS = 1
IMAGE_SCALE = 0.8

MINE_RATIO = 0.15
MINE_RATIO = 0.20
MINE_COUNT = math.floor(HEIGHT * WIDTH * MINE_RATIO)

# Fonts
FONT_SIZE = GRID_SQUARE_SIZE

# Filesystem
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# Assets
flag_img = pg.image.load(CURRENT_DIR + '\\' + 'flag.png')
flag_scale = FONT_SIZE / max(flag_img.get_width(), flag_img.get_height()) * IMAGE_SCALE
FLAG_SURF = pg.transform.rotozoom(flag_img, 0, flag_scale)
mine_img = pg.image.load(CURRENT_DIR + '\\' + 'mine.png')
mine_scale = FONT_SIZE / max(mine_img.get_width(), mine_img.get_height()) * IMAGE_SCALE
MINE_SURF = pg.transform.rotozoom(mine_img, 0, mine_scale)


# ========== TESTING ========== #

def debug_print(*args):
  if DEBUG: print(f"{pg.time.get_ticks()} |", *args)


# ========== GLOBAL METHODS ========== #

def DRAW_BACKGROUND():
  SCREEN.fill(COLOR_BACKGROUND)

def INIT():
  debug_print('INITING')
  DRAW_BACKGROUND()
  GRID.sprite.reset()

def RESTART():
  debug_print('RESTARTING')
  INIT()

def QUIT():
  debug_print('QUITTING')
  pg.quit()
  exit()

def HANDLE_EVENTS():
  for event in pg.event.get():
    match event.type:
      case pg.QUIT:
        QUIT()
      case pg.KEYDOWN:
        KEYBOARD.handle_keydown(event)

def UPDATE():

  # Mouse
  MOUSE.update()

  # Grid
  GRID.draw(SCREEN)
  GRID.update()


# ========== GAME STATE VARIABLES ========== #

pg.init()
pg.display.set_caption(WINDOW_TITLE)

MOUSE = Mouse()

KEYBOARD = Keyboard()

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FONT = pg.font.Font(None, FONT_SIZE)

CLOCK = pg.time.Clock()
dt = 0

GRID = pg.sprite.GroupSingle()
GRID.add(Grid())


# ========== GAME LOOP ========== #

INIT()
while True:
  HANDLE_EVENTS()
  UPDATE()
  pg.display.update()
  dt = CLOCK.tick(FPS) / 1000