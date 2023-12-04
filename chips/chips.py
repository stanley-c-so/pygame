# ========== LIBRARIES ========== #

import pygame as pg
from sys import exit

import math
# import os
import collections

from tile import Tile

# ========== CLASSES ========== #

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
    if self.pressed:
      return
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

class Camera(pg.sprite.Sprite):

  def __init__(self):
    self.init()

  # def __init__(self):
  def init(self):

    super().__init__()

    # Constants
    self.TILE_SIZE_IN_PX = 64
    self.VIEWPORT_WIDTH_IN_TILES = 9
    self.VIEWPORT_HEIGHT_IN_TILES = 9

    # Computed
    self.VIEWPORT_WIDTH_IN_PX = self.TILE_SIZE_IN_PX * self.VIEWPORT_WIDTH_IN_TILES
    self.VIEWPORT_HEIGHT_IN_PX = self.TILE_SIZE_IN_PX * self.VIEWPORT_HEIGHT_IN_TILES
    self.MIN_ROW = math.floor(self.VIEWPORT_HEIGHT_IN_TILES / 2)
    self.MAX_ROW = MAP.HEIGHT_IN_TILES - 1 - math.floor(self.VIEWPORT_HEIGHT_IN_TILES / 2)
    self.MIN_COL = math.floor(self.VIEWPORT_WIDTH_IN_TILES / 2)
    self.MAX_COL = MAP.WIDTH_IN_TILES - 1 - math.floor(self.VIEWPORT_WIDTH_IN_TILES / 2)

    self.zoom_scale = 1.0

    # Set image, rect
    self.image = pg.Surface((self.VIEWPORT_WIDTH_IN_PX, self.VIEWPORT_HEIGHT_IN_PX), pg.SRCALPHA)
    self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    # Test surfaces
    self.test_colors = [
      'lightgray',
      'darkgray',
      'red',
    ]
    self.test_sprites = [ pg.Surface((self.TILE_SIZE_IN_PX, self.TILE_SIZE_IN_PX), pg.SRCALPHA) for _ in range(len(self.test_colors)) ]
    for i in range(len(self.test_colors)): self.test_sprites[i].fill(self.test_colors[i])

    # Init
    self.camera_row = None
    self.camera_col = None


  def update_camera_world_pos(self):

    old_row, old_col = self.camera_row, self.camera_col

    self.camera_row = self.MIN_ROW if PLAYER.row < self.MIN_ROW \
                        else self.MAX_ROW if PLAYER.row > self.MAX_ROW \
                        else PLAYER.row
    self.camera_col = self.MIN_COL if PLAYER.col < self.MIN_COL \
                        else self.MAX_COL if PLAYER.col > self.MAX_COL \
                        else PLAYER.col

  def draw_all(self):
    
    # Clear surface
    self.image.fill('black')

    # Draw tiles
    for row in range(self.VIEWPORT_HEIGHT_IN_TILES):
      map_row = self.camera_row - math.floor(self.VIEWPORT_HEIGHT_IN_TILES / 2) + row
      for col in range(self.VIEWPORT_WIDTH_IN_TILES):
        map_col = self.camera_col - math.floor(self.VIEWPORT_WIDTH_IN_TILES / 2) + col
        for id in MAP.MAP[map_row][map_col]:
          if id == None: continue
          self.image.blit(TILE.surfaces[id], (col * self.TILE_SIZE_IN_PX, row * self.TILE_SIZE_IN_PX))

  def update(self):
    self.update_camera_world_pos()
    self.draw_all()

class Map():

  def __init__(self):
    self.init()

  # def __init__(self):
  def init(self):
    self.MAP = [
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, '201', None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, '400'], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
    ]
    self.movement_request_queue = collections.deque()

    # Computed
    self.HEIGHT_IN_TILES = len(self.MAP)
    self.WIDTH_IN_TILES = len(self.MAP[0])
    # debug_print(f"HEIGHT_IN_TILES: {self.HEIGHT_IN_TILES} | WIDTH_IN_TILES: {self.WIDTH_IN_TILES}")

    # Init


  def send_movement_request(self, request_payload):
    self.movement_request_queue.append(request_payload)
    # debug_print(f'SENDING MOVEMENT REQUEST')

  def process_movement_request(self, request_payload):
    [ instance, dir ] = request_payload

    row = instance.row
    col = instance.col
    entity = TILE.ids[instance.id]['entity']
    layer_idx = 4 if entity == TILE.ENTITY_CHIP else 3

    # Prevent player spam
    if entity == TILE.ENTITY_CHIP:
      if instance.move_time != None:
        debug_print('CANNOT MOVE YET')
        return
      instance.move_time = pg.time.get_ticks()

    # Calculate destination
    DELTAS = {
      'U': (-1, 0),
      'D': (+1, 0),
      'L': (0, -1),
      'R': (0, +1),
    }
    dy, dx = DELTAS[dir]
    new_row, new_col = row + dy, col + dx

    # Turn sprite
    instance.id = TILE.entities[entity][dir]
    self.MAP[row][col][layer_idx] = instance.id

    # Out of bounds
    if new_row < 0 or new_row == self.HEIGHT_IN_TILES or \
      new_col < 0 or new_col == self.WIDTH_IN_TILES:
      debug_print('OUT OF BOUNDS')
      return

    # Player
    if entity == TILE.ENTITY_CHIP:
      if not TILE.ids[self.MAP[new_row][new_col][2]].get('impassable'):
        self.MAP[row][col][layer_idx] = None
        self.MAP[new_row][new_col][layer_idx] = instance.id
      else:
        debug_print('hitting a wall')

  def handle_all_movement_requests(self):
    while len(self.movement_request_queue):
      request_payload = self.movement_request_queue.popleft()
      # debug_print(f'PROCESSING MOVEMENT REQUEST WITH PAYLOAD: {request_payload}')
      self.process_movement_request(request_payload)
      
  def update(self):
    self.handle_all_movement_requests()

class Player():

  def __init__(self):
    self.init()

  # def __init__(self):
  def init(self):
    self.MOVE_SPEED = 0.006

    self.row, self.col = self.update_world_pos()
    self.move_time = None
    self.id = '400'

  def handle_reset_movement_timers(self):
    if self.move_time != None and pg.time.get_ticks() - self.move_time >= (1 / self.MOVE_SPEED):
      self.move_time = None

  def handle_keydown(self):
    if pg.KEYDOWN in ALL_EVENT_TYPES_DICT:
      for event in ALL_EVENT_TYPES_DICT[pg.KEYDOWN]:
        match event.key:
          case pg.K_w:
            MAP.send_movement_request([ self, 'U' ])
          case pg.K_a:
            MAP.send_movement_request([ self, 'L' ])
          case pg.K_s:
            MAP.send_movement_request([ self, 'D' ])
          case pg.K_d:
            MAP.send_movement_request([ self, 'R' ])

  # def handle_keypress(self):
  #   keys = pg.key.get_pressed()

  def update_world_pos(self):
    found_player = False
    for row in range(MAP.HEIGHT_IN_TILES):
      for col in range(MAP.WIDTH_IN_TILES):
        if TILE.ids.get(MAP.MAP[row][col][4]).get('entity') == TILE.ENTITY_CHIP:
          self.row, self.col = row, col
          found_player = True
          break
      if found_player: break
    return self.row, self.col

  def get_inputs(self):
    self.handle_keydown()
    # self.handle_keypress()

  def update(self):
    self.update_world_pos()
    self.handle_reset_movement_timers()


# ========== CONSTANTS ========== #d

DEBUG = False
DEBUG = True

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1260, 900
SCREEN_WINDOW_TITLE = 'Chips'

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

  CAMERA.sprite.init()
  MAP.init()
  PLAYER.init()

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
  global ALL_EVENT_TYPES_DICT
  ALL_EVENT_TYPES_DICT.clear()
  for event in pg.event.get():
    ALL_EVENT_TYPES_DICT[event.type] = []
    ALL_EVENT_TYPES_DICT[event.type].append(event)

  # Handle global events
  if pg.QUIT in ALL_EVENT_TYPES_DICT:
    QUIT()


def UPDATE():

  # Get inputs
  MOUSE.update()
  KEYBOARD.update()
  PLAYER.get_inputs()

  # Update state
  MAP.update()
  PLAYER.update()

  # Draw
  CAMERA.update()
  CAMERA.draw(SCREEN)


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

TILE = Tile()

MAP = Map()

PLAYER = Player()

CAMERA = pg.sprite.GroupSingle()
CAMERA.add(Camera())


# ========== GAME LOOP ========== #

INIT()
while True:
  HANDLE_EVENTS()
  UPDATE()
  pg.display.update()
  dt = CLOCK.tick(FPS) / 1000