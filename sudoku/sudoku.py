import pygame as pg
import math
import threading
import time
from sys import exit

# ========== CLASSES ========== #

class Mouse():
  
  def __init__(self):
    self.mouse_pos = None
    self.mouse_row = None
    self.mouse_col = None
    self.pressed = False

  def update_mouse_pos(self):
    self.mouse_pos = pg.math.Vector2(pg.mouse.get_pos()) - BOARD.sprite.rect.topleft

  def handle_click(self):
    if not pg.mouse.get_pressed()[0]:
      self.pressed = False
      return
    if self.pressed:
      return
    self.pressed = True
    BOARD.sprite.handle_click()
          
  def mouse_in_bounds(self):
    return self.mouse_pos.x >= 0 and self.mouse_pos.x < BOARD_SQUARE_SIZE * 9 and self.mouse_pos.y >= 0 and self.mouse_pos.y < BOARD_SQUARE_SIZE * 9

  def update_mouse_coords(self):
    if self.mouse_in_bounds():
      self.mouse_row = math.floor(self.mouse_pos.y / BOARD_SQUARE_SIZE)
      self.mouse_col = math.floor(self.mouse_pos.x / BOARD_SQUARE_SIZE)
    else:
      self.mouse_row = None
      self.mouse_col = None

  def update(self):
    self.update_mouse_pos()
    self.update_mouse_coords()
    self.handle_click()

class Keyboard():

  def handle_keydown(self, event):

    if event.key in KEYCODES_NUMBER:
      BOARD.sprite.handle_number_input(event.key)

    elif event.key in KEYCODES_REMOVE:
      BOARD.sprite.handle_remove_input(event.key)

    else:
      match event.key:
        case pg.K_ESCAPE:
          QUIT()
        case pg.K_r:
          RESTART()
        case pg.K_s:
          debug_print('CALLED SOLVE')
          BOARD.sprite.solve()

class Board(pg.sprite.Sprite):

  def __init__(self, PUZZLE):
    super().__init__()

    # Create a surface containing the board lines
    self.surface_lines = pg.Surface((BOARD_SQUARE_SIZE * 9, BOARD_SQUARE_SIZE * 9), pg.SRCALPHA)
    for i in range(1, 9):
      if i % 3 != 0:
        pg.draw.line(self.surface_lines, BOARD_LINE_THIN_COLOR, (BOARD_SQUARE_SIZE * i, 0), (BOARD_SQUARE_SIZE * i, BOARD_SQUARE_SIZE * 9), BOARD_LINE_MINOR_THICKNESS)
        pg.draw.line(self.surface_lines, BOARD_LINE_THIN_COLOR, (0, BOARD_SQUARE_SIZE * i), (BOARD_SQUARE_SIZE * 9, BOARD_SQUARE_SIZE * i), BOARD_LINE_MINOR_THICKNESS)
    for i in range(1, 9):
      if i % 3 == 0:
        pg.draw.line(self.surface_lines, BOARD_LINE_THICK_COLOR, (BOARD_SQUARE_SIZE * i, 0), (BOARD_SQUARE_SIZE * i, BOARD_SQUARE_SIZE * 9), BOARD_LINE_MAJOR_THICKNESS)
        pg.draw.line(self.surface_lines, BOARD_LINE_THICK_COLOR, (0, BOARD_SQUARE_SIZE * i), (BOARD_SQUARE_SIZE * 9, BOARD_SQUARE_SIZE * i), BOARD_LINE_MAJOR_THICKNESS)

    # Create a background surface
    self.surface_background_dark = pg.Surface((BOARD_SQUARE_SIZE * 3, BOARD_SQUARE_SIZE * 3), pg.SRCALPHA)
    self.surface_background_dark.fill(BOARD_DARK_COLOR)

    # Set image, rect
    self.image = pg.Surface((BOARD_SQUARE_SIZE * 9, BOARD_SQUARE_SIZE * 9), pg.SRCALPHA)
    self.rect = self.image.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    # Game state
    self.reset()

  def reset(self):
    self.board = [ [ {'num': 0, 'fixed': False} for _ in range(9) ] for _ in range(9) ]
    self.filled = 0
    for fixed_num in PUZZLE:
      row, col, num = fixed_num['row'], fixed_num['col'], fixed_num['num']
      self.board[row][col]['fixed'] = True
      self.add_number(row, col, num)
    self.active = None
    self.solving = None
    self.solver_highlight_add = None
    self.solver_highlight_remove = None

  def draw_background(self):
    self.image.fill(BOARD_LIGHT_COLOR)
    for row in range(0, 9, 3):
      for col in range(0, 9, 3):
        if row % 2 != col % 2:
          self.image.blit(self.surface_background_dark, (col * BOARD_SQUARE_SIZE, row * BOARD_SQUARE_SIZE))
          # self.image.blit(self.surface_background_dark, (col * 1, row * 1))
    
  def highlight(self):

    # Mouseover
    if MOUSE.mouse_in_bounds():
      mouseover_highlight_surf = pg.Surface((BOARD_SQUARE_SIZE, BOARD_SQUARE_SIZE), pg.SRCALPHA)
      mouseover_highlight_surf.fill(BOARD_HIGHLIGHT_COLOR)
      self.image.blit(mouseover_highlight_surf, mouseover_highlight_surf.get_rect(topleft=(MOUSE.mouse_col * BOARD_SQUARE_SIZE, MOUSE.mouse_row * BOARD_SQUARE_SIZE)))

    # Active
    if self.active:
      active_highlight_surf = pg.Surface((BOARD_SQUARE_SIZE, BOARD_SQUARE_SIZE), pg.SRCALPHA)
      active_highlight_surf.fill(BOARD_ACTIVE_COLOR)
      self.image.blit(active_highlight_surf, active_highlight_surf.get_rect(topleft=(self.active[1] * BOARD_SQUARE_SIZE, self.active[0] * BOARD_SQUARE_SIZE)))
    
    # Solver
    if self.solver_highlight_add:
      solver_highlight_add_surf = pg.Surface((BOARD_SQUARE_SIZE, BOARD_SQUARE_SIZE), pg.SRCALPHA)
      solver_highlight_add_surf.fill(BOARD_SOLVER_HIGHLIGHT_ADD_COLOR)
      self.image.blit(solver_highlight_add_surf, solver_highlight_add_surf.get_rect(topleft=(self.solver_highlight_add[1] * BOARD_SQUARE_SIZE, self.solver_highlight_add[0] * BOARD_SQUARE_SIZE)))

    if self.solver_highlight_remove:
      solver_highlight_remove = pg.Surface((BOARD_SQUARE_SIZE, BOARD_SQUARE_SIZE), pg.SRCALPHA)
      solver_highlight_remove.fill(BOARD_SOLVER_HIGHLIGHT_REMOVE_COLOR)
      self.image.blit(solver_highlight_remove, solver_highlight_remove.get_rect(topleft=(self.solver_highlight_remove[1] * BOARD_SQUARE_SIZE, self.solver_highlight_remove[0] * BOARD_SQUARE_SIZE)))

    # Fixed
    for fixed_num in PUZZLE:
      row, col = fixed_num['row'], fixed_num['col']
      fixed_highlight_surf = pg.Surface((BOARD_SQUARE_SIZE, BOARD_SQUARE_SIZE), pg.SRCALPHA)
      fixed_highlight_surf.fill(BOARD_FIXED_COLOR)
      self.image.blit(fixed_highlight_surf, fixed_highlight_surf.get_rect(topleft=(col * BOARD_SQUARE_SIZE, row * BOARD_SQUARE_SIZE)))
    
  def draw_lines(self):
    self.image.blit(self.surface_lines, (0, 0))

  def draw_numbers(self):
    for row in range(9):
      for col in range(9):
        if self.board[row][col]['num']:
          # debug_print(f"Should draw {self.board[row][col]['num']} at row {row}, col {col}")
          num_surf = FONT.render(f"{self.board[row][col]['num']}", False, FONT_FIXED_COLOR if self.board[row][col]['fixed'] else FONT_INPUT_COLOR)
          num_rect = num_surf.get_rect(center=((col + 0.5) * BOARD_SQUARE_SIZE, (row + 0.5) * BOARD_SQUARE_SIZE))
          self.image.blit(num_surf, num_rect)

  def is_complete(self):
    
    if self.filled < 81: return False

    # Verify rows 1-9
    for row in range(9):
      nums = map(lambda data: data['num'], self.board[row])
      if len(set(nums)) != 9:
        return False
    
    # Verify cols 1-9
    for col in range(9):
      nums = [self.board[row][col]['num'] for row in range(9)]
      if len(set(nums)) != 9:
        return False

    # Verify regions 1-9
    for row in range(0, 9, 3):
      for col in range(0, 9, 3):
        nums = []
        for r in range(3):
          for c in range(3):
            nums.append(self.board[row + r][col + c]['num'])
        if len(set(nums)) != 9:
          return False

    return True

  def handle_click(self):
    if self.solving: return
    in_bounds = MOUSE.mouse_in_bounds()
    debug_print(f"BOARD handle_click | in bounds? {in_bounds}")
    row, col = MOUSE.mouse_row, MOUSE.mouse_col
    if in_bounds and self.active != (row, col):
      if self.board[row][col]['fixed']: return
      debug_print(f"{row}, {col}")
      self.active = (row, col)
    else:
      self.active = None

  def add_number(self, row, col, num):
    if num and not self.board[row][col]['num']: self.filled += 1
    self.board[row][col]['num'] = num

  def remove_number(self, row, col):
    if self.board[row][col]['num']: self.filled -= 1
    self.board[row][col]['num'] = 0

  def change_number(self, row, col, num):
    self.remove_number(row, col)
    self.add_number(row, col, num)

  def handle_number_input(self, key):
    debug_print('PRESSED A NUMBER')
    if self.solving: return
    if self.active:
      debug_print(f"{KEYCODES_NUMBER[key]}")
      row, col = self.active
      self.change_number(row, col, KEYCODES_NUMBER[key])
      self.active = None
      self.solver_highlight_add = None
      self.solver_highlight_remove = None
      if self.filled == 81:
        debug_print('FULL')
        if self.is_complete():
          win()
        else:
          debug_print('PUZZLE IS INCORRECT')
    # debug_print(self.board)
    debug_print(f"FILLED: {self.filled}")

  def handle_remove_input(self, key):
    debug_print('PRESSED A REMOVE KEY')
    if self.active:
      row, col = self.active
      self.remove_number(row, col)
      self.active = None
      self.solver_highlight_add = None
      self.solver_highlight_remove = None
    # debug_print(self.board)
    debug_print(f"FILLED: {self.filled}")

  def update(self):
    self.draw_background()
    self.highlight()
    self.draw_lines()
    self.draw_numbers()
    if self.solving and (pg.time.get_ticks() - self.solving >= SOLVER_DELAY_MS): self.handle_solve()

  def get_eligible_nums(self, row, col):

    if self.board[row][col]['num']: return { self.board[row][col]['num'] }

    eligible = { n + 1 for n in range(9) }
    
    # Check column
    for r in range(9):
      if r != row:
        eligible.discard(self.board[r][col]['num'])
    
    # Check row
    for c in range(9):
      if c != col:
        eligible.discard(self.board[row][c]['num'])

    # Check region
    R, C = row // 3, col // 3
    for r in range(3):
      for c in range(3):
        if not (R*3 + r == row and C*3 + c == col):
          eligible.discard(self.board[R*3 + r][C*3 + c]['num'])

    return eligible

  def get_next_node_eligible_nums(self):
    min_count = 10
    next_node_eligible_nums = []
    for row in range(9):
      for col in range(9):
        if not self.board[row][col]['num']:
          eligible_nums = self.get_eligible_nums(row, col)
          if len(eligible_nums) == 0:
            return []
          if len(eligible_nums) < min_count:
            min_count = len(eligible_nums)
            next_node_eligible_nums = []
            for n in eligible_nums:
              next_node_eligible_nums.append({
                'row': row,
                'col': col,
                'value': n,
                'visited': False
              })
    return next_node_eligible_nums


  def solve(self):
    if not self.solving:
      if self.is_complete():
        win()
        return
      self.solving = pg.time.get_ticks()
      self.active = None
      self.solver_stack = self.get_next_node_eligible_nums()
      # debug_print('START:', self.solver_stack)
      # self.memo = set()

  def handle_solve(self):
    self.solving = pg.time.get_ticks()
    iterations = 0
    while self.solver_stack:
      if iterations == FPS: return
      iterations += 1

      node = self.solver_stack[-1]
      # debug_print(f"CURRENT NODE: {node}")
      row, col, value, visited = node['row'], node['col'], node['value'], node['visited']
      if visited:
        self.remove_number(row, col)
        self.solver_stack.pop()
        self.solver_highlight_add = None
        self.solver_highlight_remove = (row, col)
        if not SOLVER_ALLOW_MULTIPLE_ITERATIONS: return
        continue
      node['visited'] = True
      self.add_number(row, col, value)
      self.solver_highlight_add = (row, col)
      self.solver_highlight_remove = None

      # serial = self.serialize()
      # if serial in self.memo:
      #   debug_print('REPEATED SERIAL')
      #   debug_print(f"CURRENT NODE: {node}")
      #   for i in range(0, 81, 9):
      #     debug_print(list(serial[i:i+9]))
      #   QUIT()
      # self.memo.add(serial)

      if self.filled == 81:
        if self.is_complete():
          self.solving = None
          win()
          return
      else:
        for node in self.get_next_node_eligible_nums():
          self.solver_stack.append(node)
      if not SOLVER_ALLOW_MULTIPLE_ITERATIONS: return      
    self.solving = None
    debug_print('CURRENT BOARD STATE NOT SOLVABLE')

  # def serialize(self):
  #   serial = ''
  #   for row in range(9):
  #     for col in range(9):
  #       serial += str(self.board[row][col]['num'])
  #   return serial


# ========== CONSTANTS ========== #

DEBUG = False
# DEBUG = True

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 900

# FPS
FPS = 1
FPS = 10
FPS = 60
FPS = 1000
FPS = 2000
# FPS = 5000
# FPS = 10000
# FPS = 20000

# Solver
SOLVER_ALLOW_MULTIPLE_ITERATIONS = True
# SOLVER_ALLOW_MULTIPLE_ITERATIONS = False
SOLVER_DELAY_MS = 0
# SOLVER_DELAY_MS = 1
# SOLVER_DELAY_MS = 2
# SOLVER_DELAY_MS = 10
# SOLVER_DELAY_MS = 20
# SOLVER_DELAY_MS = 50
# SOLVER_DELAY_MS = 100

# Colors
BACKGROUND_COLOR = "Black"
BOARD_LIGHT_COLOR = "White"
BOARD_DARK_COLOR = (191, 191, 191)
BOARD_LINE_THIN_COLOR = (63, 63, 63)
BOARD_LINE_THICK_COLOR = (31, 31, 31)
BOARD_HIGHLIGHT_COLOR = (255, 255, 0, 255)
BOARD_ACTIVE_COLOR = (223, 15, 63, 255)
BOARD_FIXED_COLOR = (95, 95, 95)
BOARD_SOLVER_HIGHLIGHT_ADD_COLOR = (0, 255, 0, 255)
BOARD_SOLVER_HIGHLIGHT_REMOVE_COLOR = (255, 0, 0, 255)
FONT_FIXED_COLOR = 'Black'
FONT_INPUT_COLOR = (31, 31, 31)

# Board size
BOARD_SQUARE_SIZE = 80
BOARD_LINE_MINOR_THICKNESS = 4
BOARD_LINE_MAJOR_THICKNESS = 6

# Inputs
KEYCODES_NUMBER = {
  pg.K_1: 1,
  pg.K_2: 2,
  pg.K_3: 3,
  pg.K_4: 4,
  pg.K_5: 5,
  pg.K_6: 6,
  pg.K_7: 7,
  pg.K_8: 8,
  pg.K_9: 9,
  pg.K_KP1: 1,
  pg.K_KP2: 2,
  pg.K_KP3: 3,
  pg.K_KP4: 4,
  pg.K_KP5: 5,
  pg.K_KP6: 6,
  pg.K_KP7: 7,
  pg.K_KP8: 8,
  pg.K_KP9: 9,
}

KEYCODES_REMOVE = {
  pg.K_BACKSPACE,
  pg.K_DELETE,
}

# Fonts
FONT_SIZE = 80


# ========== TESTING ========== #

def debug_print(*args):
  if DEBUG: print(f"{pg.time.get_ticks()} |", *args)


# ========== GLOBAL METHODS ========== #

def draw_background():
  SCREEN.fill(BACKGROUND_COLOR)

def INIT():
  debug_print('INITING')
  draw_background()
  BOARD.sprite.reset()

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
  BOARD.draw(SCREEN)
  BOARD.update()

def win():
  debug_print('CONGRATS YOU WIN!')


# ========== PUZZLE ========== #

# BLANK
PUZZLE_0 = []

# GENERIC
PUZZLE_1 = [
  {'row': 0, 'col': 1, 'num': 1},
  {'row': 0, 'col': 2, 'num': 8},
  {'row': 0, 'col': 5, 'num': 2},
  {'row': 0, 'col': 6, 'num': 3},
  {'row': 0, 'col': 8, 'num': 4},
  {'row': 1, 'col': 2, 'num': 3},
  {'row': 1, 'col': 3, 'num': 5},
  {'row': 2, 'col': 0, 'num': 5},
  {'row': 2, 'col': 1, 'num': 2},
  {'row': 2, 'col': 2, 'num': 4},
  {'row': 2, 'col': 3, 'num': 8},
  {'row': 2, 'col': 4, 'num': 9},
  {'row': 3, 'col': 0, 'num': 1},
  {'row': 3, 'col': 2, 'num': 5},
  {'row': 3, 'col': 4, 'num': 7},
  {'row': 3, 'col': 6, 'num': 4},
  {'row': 3, 'col': 8, 'num': 6},
  {'row': 4, 'col': 2, 'num': 7},
  {'row': 4, 'col': 6, 'num': 9},
  {'row': 5, 'col': 0, 'num': 2},
  {'row': 5, 'col': 2, 'num': 9},
  {'row': 5, 'col': 4, 'num': 4},
  {'row': 5, 'col': 6, 'num': 5},
  {'row': 5, 'col': 8, 'num': 8},
  {'row': 6, 'col': 4, 'num': 8},
  {'row': 6, 'col': 5, 'num': 9},
  {'row': 6, 'col': 6, 'num': 6},
  {'row': 6, 'col': 7, 'num': 4},
  {'row': 6, 'col': 8, 'num': 3},
  {'row': 7, 'col': 5, 'num': 7},
  {'row': 7, 'col': 6, 'num': 2},
  {'row': 8, 'col': 2, 'num': 1},
  {'row': 8, 'col': 3, 'num': 6},
  {'row': 8, 'col': 6, 'num': 7},
  {'row': 8, 'col': 7, 'num': 8},
]

# HARD; BRUTE FORCE REQUIRED
PUZZLE_2 = [
  {'row': 1, 'col': 5, 'num': 3},
  {'row': 1, 'col': 7, 'num': 8},
  {'row': 1, 'col': 8, 'num': 5},
  {'row': 2, 'col': 2, 'num': 1},
  {'row': 2, 'col': 4, 'num': 2},
  {'row': 3, 'col': 3, 'num': 5},
  {'row': 3, 'col': 5, 'num': 7},
  {'row': 4, 'col': 2, 'num': 4},
  {'row': 4, 'col': 6, 'num': 1},
  {'row': 5, 'col': 1, 'num': 9},
  {'row': 6, 'col': 0, 'num': 5},
  {'row': 6, 'col': 7, 'num': 7},
  {'row': 6, 'col': 8, 'num': 3},
  {'row': 7, 'col': 2, 'num': 2},
  {'row': 7, 'col': 4, 'num': 1},
  {'row': 8, 'col': 4, 'num': 4},
  {'row': 8, 'col': 8, 'num': 9},
]

# HARD?
PUZZLE_3 = [
  {'row': 0, 'col': 3, 'num': 8},
  {'row': 0, 'col': 5, 'num': 1},
  {'row': 1, 'col': 6, 'num': 4},
  {'row': 1, 'col': 7, 'num': 3},
  {'row': 2, 'col': 0, 'num': 5},
  {'row': 3, 'col': 4, 'num': 7},
  {'row': 3, 'col': 6, 'num': 8},
  {'row': 4, 'col': 6, 'num': 1},
  {'row': 5, 'col': 1, 'num': 2},
  {'row': 5, 'col': 4, 'num': 3},
  {'row': 6, 'col': 0, 'num': 6},
  {'row': 6, 'col': 7, 'num': 7},
  {'row': 6, 'col': 8, 'num': 5},
  {'row': 7, 'col': 2, 'num': 3},
  {'row': 7, 'col': 3, 'num': 4},
  {'row': 8, 'col': 3, 'num': 2},
  {'row': 8, 'col': 6, 'num': 6},
]

# INTERESTING SHAPE
PUZZLE_4 = [
  {'row': 1, 'col': 2, 'num': 1},
  {'row': 1, 'col': 3, 'num': 2},
  {'row': 1, 'col': 5, 'num': 3},
  {'row': 1, 'col': 6, 'num': 6},
  {'row': 2, 'col': 1, 'num': 5},
  {'row': 2, 'col': 2, 'num': 9},
  {'row': 2, 'col': 3, 'num': 8},
  {'row': 2, 'col': 5, 'num': 1},
  {'row': 2, 'col': 6, 'num': 4},
  {'row': 2, 'col': 7, 'num': 2},
  {'row': 3, 'col': 1, 'num': 3},
  {'row': 3, 'col': 2, 'num': 7},
  {'row': 3, 'col': 6, 'num': 8},
  {'row': 3, 'col': 7, 'num': 6},
  {'row': 5, 'col': 1, 'num': 9},
  {'row': 5, 'col': 2, 'num': 6},
  {'row': 5, 'col': 6, 'num': 1},
  {'row': 5, 'col': 7, 'num': 3},
  {'row': 6, 'col': 1, 'num': 4},
  {'row': 6, 'col': 2, 'num': 2},
  {'row': 6, 'col': 3, 'num': 7},
  {'row': 6, 'col': 5, 'num': 6},
  {'row': 6, 'col': 6, 'num': 5},
  {'row': 6, 'col': 7, 'num': 8},
  {'row': 7, 'col': 2, 'num': 8},
  {'row': 7, 'col': 3, 'num': 9},
  {'row': 7, 'col': 5, 'num': 2},
  {'row': 7, 'col': 6, 'num': 7},
]

PUZZLE = PUZZLE_0
PUZZLE = PUZZLE_1
PUZZLE = PUZZLE_2
# PUZZLE = PUZZLE_3
# PUZZLE = PUZZLE_4

# ========== GAME STATE VARIABLES ========== #

pg.init()

MOUSE = Mouse()

KEYBOARD = Keyboard()

BOARD = pg.sprite.GroupSingle()
BOARD.add(Board(PUZZLE))

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