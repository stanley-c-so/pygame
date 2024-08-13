import os
from collections import deque

from globals import *

from pinkball import Pinkball

FILENAME = 'map1'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
INPUT_PATH = CURRENT_DIR + '\\' + FILENAME + '.txt'
data = open(INPUT_PATH, 'r').read()

TILE_DELIMITER = '|'
LAYER_DELIMITER = ','
NONE = '___'

LAYER_IDX_FLOORS = 0
LAYER_IDX_PICKUPS = 1
LAYER_IDX_WALLS = 2
LAYER_IDX_CREATURES = 3
LAYER_IDX_PLAYER = 4

class Map():

  def parse(self, data):
    chunks_dict = {}
    chunks = data.split('\n\n')
    for chunk in chunks:
      lines = chunk.split('\n')
      chunks_dict[lines[0]] = lines[1:]

    res = {
      MAP: []
    }

    # PROCESS MAP
    def init_entity(entity, map_col, row, col, id, is_player = False):

      # Add entity to map
      map_col.append(entity)

      # Add non-player entity to entities list
      if not is_player:
        self.all_creatures.append(entity)
      
      # Set entity info within class
      entity.set_coords(row, col)
      entity.set_id(id)
      entity.set_dir(SINGLETONS[TILE].ids[id]['dir'])

    for row in range(len(chunks_dict[MAP])):
      row_data = chunks_dict[MAP][row]
      row_data_split = row_data.split(TILE_DELIMITER)
      map_row = []
      for col in range(len(row_data_split)):
        map_col = []
        col_data_split = row_data_split[col].split(LAYER_DELIMITER)
        for layer_idx in range(len(col_data_split)):
          id = col_data_split[layer_idx]
          if SINGLETONS[TILE].is_player(id):
            if layer_idx != LAYER_IDX_PLAYER: assert False
            init_entity(SINGLETONS[PLAYER], map_col, row, col, id, True)
          elif SINGLETONS[TILE].is_pinkball(id):
            if layer_idx != LAYER_IDX_CREATURES: assert False
            init_entity(Pinkball(), map_col, row, col, id)
          elif id == NONE:
            map_col.append(None)
          else:
            map_col.append(id)
        map_row.append(map_col)
      res[MAP].append(map_row)

    # PROCESS BUTTON CONNECTIONS

    return res

  def __init__(self):

    # Init
    self.movement_request_queue = deque()
    self.all_creatures = []

    # Parse map data
    parse = self.parse(data)
    self.MAP = parse[MAP]

    # Computed
    self.HEIGHT_IN_TILES = len(self.MAP)
    self.WIDTH_IN_TILES = len(self.MAP[0])
    # debug_print(f"HEIGHT_IN_TILES: {self.HEIGHT_IN_TILES} | WIDTH_IN_TILES: {self.WIDTH_IN_TILES}")

  def send_movement_request(self, request_payload):
    self.movement_request_queue.append(request_payload)
    # debug_print(f'SENDING MOVEMENT REQUEST')

  def process_movement_request(self, request_payload):
    ( instance, dir ) = request_payload

    row = instance.row
    col = instance.col
    entity_name = instance.entity_name
    layer_idx = LAYER_IDX_PLAYER if entity_name == ENTITY_CHIP else LAYER_IDX_CREATURES

    # Prevent movement spam
    if instance.move_time != None:
      # debug_print('CANNOT MOVE YET')
      return
    # instance.set_move_time(pg.time.get_ticks())
    instance.set_move_time(get_GAME_TICKS())
    # debug_print('STARTING MOVEMENT')

    # Calculate destination
    DELTAS = {
      U: (-1, 0),
      D: (+1, 0),
      L: (0, -1),
      R: (0, +1),
    }
    dy, dx = DELTAS[dir]
    new_row, new_col = row + dy, col + dx

    # Turn entity in intended direction (even if move will fail)
    instance.turn(dir, entity_name)

    # Common fail condition: Out of bounds
    if new_row < 0 or new_row == self.HEIGHT_IN_TILES or \
      new_col < 0 or new_col == self.WIDTH_IN_TILES:
      debug_print('OUT OF BOUNDS')
      instance.set_hit_wall(True)
      return

    # Player-specific logic
    if entity_name == ENTITY_CHIP:

      # Move
      # NOTE: for monsters, also check that they're not bumping into a monster
      if not SINGLETONS[TILE].ids[self.MAP[new_row][new_col][2]].get('impassable'):
        instance.set_coords(new_row, new_col)
        self.MAP[row][col][layer_idx] = None
        self.MAP[new_row][new_col][layer_idx] = instance

      # Hit wall
      else:
        debug_print('hitting a wall')
        instance.set_hit_wall(True)

  def handle_all_movement_requests(self):
    while len(self.movement_request_queue):
      request_payload = self.movement_request_queue.popleft()
      # debug_print(f'PROCESSING MOVEMENT REQUEST WITH PAYLOAD: {request_payload}')
      self.process_movement_request(request_payload)

  def handle_player_creature_collision(self):
    player_row = SINGLETONS[PLAYER].row
    player_col = SINGLETONS[PLAYER].col

    if self.MAP[player_row][player_col][LAYER_IDX_CREATURES] != None:
      debug_print('CREATURE COLLISION')
      SINGLETONS[PLAYER].set_dead(True)

  def handle_all_collisions(self):
    self.handle_player_creature_collision()

  def update(self):
    self.handle_all_movement_requests()
    self.handle_all_collisions()