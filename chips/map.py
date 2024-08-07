import os
import collections

from globals import *

FILENAME = 'map1'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
INPUT_PATH = CURRENT_DIR + '\\' + FILENAME + '.txt'
data = open(INPUT_PATH, 'r').read()

TILE_DELIMITER = '|'
LAYER_DELIMITER = ','
NONE = '___'

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
    for row in range(len(chunks_dict[MAP])):
      row_data = chunks_dict[MAP][row]
      split = row_data.split(TILE_DELIMITER)
      map_row = []
      for col in range(len(split)):
        col_data = split[col]
        map_col = []
        for id in col_data.split(LAYER_DELIMITER):
          if id[0] == '4':
            map_col.append(SINGLETONS[PLAYER])
            SINGLETONS[PLAYER].set_coords(row, col)
            SINGLETONS[PLAYER].set_id(id)
            SINGLETONS[PLAYER].set_dir(SINGLETONS[TILE].ids[id]['dir'])
          # to-do: make this generate an entity class instance for monsters
          elif id == NONE:
            map_col.append(None)
          else:
            map_col.append(id)
        map_row.append(map_col)
      res[MAP].append(map_row)

    # PROCESS BUTTON CONNECTIONS

    return res

  # def __init__(self):
  #   self.init()

  def __init__(self):
  # def init(self):

    parse = self.parse(data)
    self.MAP = parse[MAP]

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
    ( instance, dir ) = request_payload

    row = instance.row
    col = instance.col
    entity = instance.entity
    layer_idx = 4 if entity == SINGLETONS[TILE].ENTITY_CHIP else 3

    # Prevent player spam
    if entity == SINGLETONS[TILE].ENTITY_CHIP:
      if instance.move_time != None:
        # debug_print('CANNOT MOVE YET')
        return
      instance.set_move_time(pg.time.get_ticks())
      debug_print('STARTING MOVEMENT')

    # Calculate destination
    DELTAS = {
      U: (-1, 0),
      D: (+1, 0),
      L: (0, -1),
      R: (0, +1),
    }
    dy, dx = DELTAS[dir]
    new_row, new_col = row + dy, col + dx

    # Turn sprite
    instance.set_dir(dir)
    instance.set_id(SINGLETONS[TILE].entities[entity][dir])

    # Out of bounds
    if new_row < 0 or new_row == self.HEIGHT_IN_TILES or \
      new_col < 0 or new_col == self.WIDTH_IN_TILES:
      debug_print('OUT OF BOUNDS')
      instance.set_move_time(None)
      return

    # Player
    if entity == SINGLETONS[TILE].ENTITY_CHIP:

      # Move
      # NOTE: for monsters, also check that they're not bumping into a monster
      if not SINGLETONS[TILE].ids[self.MAP[new_row][new_col][2]].get('impassable'):
        instance.set_coords(new_row, new_col)
        self.MAP[row][col][layer_idx] = None
        self.MAP[new_row][new_col][layer_idx] = instance

      # Hit wall
      else:
        debug_print('hitting a wall')
        instance.set_move_time(None)

  def handle_all_movement_requests(self):
    while len(self.movement_request_queue):
      request_payload = self.movement_request_queue.popleft()
      # debug_print(f'PROCESSING MOVEMENT REQUEST WITH PAYLOAD: {request_payload}')
      self.process_movement_request(request_payload)
      
  def update(self):
    self.handle_all_movement_requests()