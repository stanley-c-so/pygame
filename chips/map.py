import os
from collections import deque

from globals import *
from utils import *

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
      entity.set_dir(SINGLETONS[TILE].ids[id][dir])

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
    entity = request_payload[0]
    original_dir = request_payload[1]
    transform_idx = request_payload[2] if len(request_payload) >= 3 else -1

    row = entity.row
    col = entity.col
    name = entity.name
    
    transform = 0 if name == ENTITY_CHIP or transform_idx == -1 else entity.redirection_transforms[transform_idx]
    dir = dir_with_applied_transformation(original_dir, transform)

    layer_idx = LAYER_IDX_PLAYER if name == ENTITY_CHIP else LAYER_IDX_CREATURES

    # Dead
    if SINGLETONS[PLAYER].dead: return

    # Prevent movement spam
    if entity.move_time != None and transform_idx == -1:
      return
    entity.set_move_time(get_global_GAME_TICKS())

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
    entity.turn(dir, name)

    # Player-specific logic
    if name == ENTITY_CHIP:

      # OOB or hit wall
      if new_row < 0 or new_row == self.HEIGHT_IN_TILES \
        or new_col < 0 or new_col == self.WIDTH_IN_TILES \
        or SINGLETONS[TILE].ids[self.MAP[new_row][new_col][LAYER_IDX_WALLS]].get(impassable):
        debug_print('hitting a wall')
        entity.set_hit_wall(True)
        return

      # Move
      else:
        entity.set_coords(new_row, new_col)
        self.MAP[row][col][layer_idx] = None
        self.MAP[new_row][new_col][layer_idx] = entity

    # Creature-specific logic
    else:
      
      # OOB or hit wall or creature
      if new_row < 0 or new_row == self.HEIGHT_IN_TILES \
        or new_col < 0 or new_col == self.WIDTH_IN_TILES \
        or SINGLETONS[TILE].ids[self.MAP[new_row][new_col][LAYER_IDX_WALLS]].get(impassable) \
        or self.MAP[new_row][new_col][LAYER_IDX_CREATURES] != None:
        
        # entity.set_hit_wall_or_creature(True)

        if transform_idx + 1 < len(entity.redirection_transforms):
          # recurse
          self.process_movement_request(( entity, original_dir, transform_idx + 1 ))
          return

        else:
          debug_print('STUCK!')
          return

      # Move
      else:
        entity.set_coords(new_row, new_col)
        self.MAP[row][col][layer_idx] = None
        self.MAP[new_row][new_col][layer_idx] = entity

  def update_all_creatures(self):
    for creature in self.all_creatures:
      creature.update()

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
      killing_entity = self.MAP[player_row][player_col][LAYER_IDX_CREATURES]
      set_global_KILLING_ENTITY(killing_entity)
      SINGLETONS[PLAYER].set_dead(True)

  def handle_all_collisions(self):
    self.handle_player_creature_collision()

  def update(self):
    # self.update_all_creatures()
    self.handle_all_movement_requests()
    self.update_all_creatures()
    self.handle_all_collisions()