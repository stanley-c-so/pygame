from globals import *

import collections

class Map():

  # def __init__(self):
  #   self.init()

  def __init__(self):
  # def init(self):
    # self.MAP = [ [ data.copy() for data in row ] for row in SINGLETONS[MAP_DATA].MAP ]
    self.MAP = []
    for row in SINGLETONS[MAP_DATA].MAP:
      map_row = []
      for col in row:
        map_col = []
        for entity in col:
          # to-do: make this generate an entity class instance where applicable
          map_col.append(entity)
        map_row.append(map_col)
      self.MAP.append(map_row)

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
    entity = SINGLETONS[TILE].ids[instance.id]['entity']
    layer_idx = 4 if entity == SINGLETONS[TILE].ENTITY_CHIP else 3

    # Prevent player spam
    if entity == SINGLETONS[TILE].ENTITY_CHIP:
      if instance.move_time != None:
        debug_print('CANNOT MOVE YET')
        return
      instance.move_time = pg.time.get_ticks()
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
    instance.dir = dir
    instance.id = SINGLETONS[TILE].entities[entity][dir]
    self.MAP[row][col][layer_idx] = instance.id

    # Out of bounds
    if new_row < 0 or new_row == self.HEIGHT_IN_TILES or \
      new_col < 0 or new_col == self.WIDTH_IN_TILES:
      debug_print('OUT OF BOUNDS')
      instance.move_time = None
      return

    # Player
    if entity == SINGLETONS[TILE].ENTITY_CHIP:

      # Move
      if not SINGLETONS[TILE].ids[self.MAP[new_row][new_col][2]].get('impassable'):
        self.MAP[row][col][layer_idx] = None
        self.MAP[new_row][new_col][layer_idx] = instance.id

      # Hit wall
      else:
        debug_print('hitting a wall')
        instance.move_time = None

  def handle_all_movement_requests(self):
    while len(self.movement_request_queue):
      request_payload = self.movement_request_queue.popleft()
      # debug_print(f'PROCESSING MOVEMENT REQUEST WITH PAYLOAD: {request_payload}')
      self.process_movement_request(request_payload)
      
  def update(self):
    self.handle_all_movement_requests()