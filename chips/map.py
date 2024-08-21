import os
from collections import deque

from globals import *
from constants import *
from utils import *

FILENAME = 'map1'
# FILENAME = 'map2'
# FILENAME = 'map3'
FILENAME = 'level1'
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
      CHIPS_REQUIRED: 0,
      MAP: []
    }

    # CHIPS REQUIRED
    if chunks_dict.get(CHIPS_REQUIRED):
      res[CHIPS_REQUIRED] = int(chunks_dict[CHIPS_REQUIRED][0])
    # debug_print(f'CHIPS REQUIRED: {res[CHIPS_REQUIRED]}')

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
      entity.set_dir(SINGLETONS[TILE].data_by_id[id][dir])

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
          elif SINGLETONS[TILE].is_creature(id):
            if layer_idx != LAYER_IDX_CREATURES: assert False
            entity = SINGLETONS[TILE].data_by_id[id][entity_class]()
            init_entity(entity, map_col, row, col, id)
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

    # Data structures
    self.creatures_to_delete_by_idx = set()
    self.walls_to_delete_by_coords = {}
    self.pickups_to_delete_by_coords = {}

    # Map variables
    self.chips_required = parse[CHIPS_REQUIRED]


  # ========== MOVEMENT REQUESTS ========== #

  def send_movement_request(self, request_payload):
    self.movement_request_queue.append(request_payload)
    # debug_print(f'SENDING MOVEMENT REQUEST')

  def process_movement_request(self, request_payload):
    entity = request_payload[0]
    original_dir = request_payload[1]
    transform_idx = request_payload[2] if len(request_payload) >= 3 else 0

    # Dead
    if entity.dead: return

    row = entity.row
    col = entity.col
    name = entity.name
    
    transform = 0 if name == ENTITY_CHIP else entity.redirection_transforms[transform_idx]
    dir = dir_with_applied_transformation(original_dir, transform)

    layer_idx = LAYER_IDX_PLAYER if name == ENTITY_CHIP else LAYER_IDX_CREATURES

    # Prevent movement spamW
    if entity.move_time != None and transform_idx == 0: return
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
    entity.turn(dir)

    # Player-specific logic
    if name == ENTITY_CHIP:

      # OOB or hit wall
      if new_row < 0 or new_row == self.HEIGHT_IN_TILES \
        or new_col < 0 or new_col == self.WIDTH_IN_TILES \
        or SINGLETONS[TILE].data_by_id[self.MAP[new_row][new_col][LAYER_IDX_WALLS]].get(impassable) \
        or self.MAP[new_row][new_col][LAYER_IDX_WALLS] == SINGLETONS[TILE].walls[WALL_SOCKET] and self.chips_required > 0 \
        or self.MAP[new_row][new_col][LAYER_IDX_WALLS] == SINGLETONS[TILE].walls[LOCK_BLUE] and entity.keys_blue == 0 \
        or self.MAP[new_row][new_col][LAYER_IDX_WALLS] == SINGLETONS[TILE].walls[LOCK_RED] and entity.keys_red == 0 \
        or self.MAP[new_row][new_col][LAYER_IDX_WALLS] == SINGLETONS[TILE].walls[LOCK_GREEN] and entity.keys_green == 0 \
        or self.MAP[new_row][new_col][LAYER_IDX_WALLS] == SINGLETONS[TILE].walls[LOCK_YELLOW] and entity.keys_yellow == 0 \
        :
        # debug_print('HITTING A WALL')
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
        or SINGLETONS[TILE].data_by_id[self.MAP[new_row][new_col][LAYER_IDX_WALLS]].get(impassable) \
        or SINGLETONS[TILE].data_by_id[self.MAP[new_row][new_col][LAYER_IDX_WALLS]].get(impassable_for_creatures) \
        or (SINGLETONS[TILE].data_by_id[self.MAP[new_row][new_col][LAYER_IDX_PICKUPS]].get(pickup) and (new_row, new_col) not in self.pickups_to_delete_by_coords) \
        or self.MAP[new_row][new_col][LAYER_IDX_CREATURES] != None \
        :

        if transform_idx + 1 < len(entity.redirection_transforms):
          # recurse
          self.process_movement_request(( entity, original_dir, transform_idx + 1 ))
          return

        else:
          entity.set_hit_wall_or_creature(True)
          entity.turn(original_dir)
          return

      # Move
      else:
        entity.set_coords(new_row, new_col)
        self.MAP[row][col][layer_idx] = None
        self.MAP[new_row][new_col][layer_idx] = entity

  def handle_all_movement_requests(self):
    while len(self.movement_request_queue):
      request_payload = self.movement_request_queue.popleft()
      # debug_print(f'PROCESSING MOVEMENT REQUEST WITH PAYLOAD: {request_payload}')
      self.process_movement_request(request_payload)


  # ========== COLLISIONS ========== #

  def handle_collision_with_creature(self, entity):
    if entity != SINGLETONS[PLAYER]: return
    if entity.dead: return
    entity_row = entity.row
    entity_col = entity.col

    if self.MAP[entity_row][entity_col][LAYER_IDX_CREATURES] != None:
      killing_entity = self.MAP[entity_row][entity_col][LAYER_IDX_CREATURES]
      set_global_KILLING_ENTITY(killing_entity)
      entity.set_dead(True)
      debug_print(f'PLAYER-CREATURE COLLISION - killed by {killing_entity}')

  def handle_collision_with_interactive_floor(self, entity):
    entity_is_player = entity == SINGLETONS[PLAYER]
    entity_row = entity.row
    entity_col = entity.col

    id = self.MAP[entity_row][entity_col][LAYER_IDX_FLOORS]
    if id == None or not SINGLETONS[TILE].data_by_id[id].get(interactive): return

    if SINGLETONS[TILE].interactive_floors[INTERACTIVE_FLOOR_WATER] == id:
      if entity.dead: return
      if INTERACTIVE_FLOOR_WATER in entity.invincible_to: return
      if entity_is_player and entity.boots_water: return
      entity.set_dead(True)
      if entity_is_player:
        set_global_KILLING_HAZARD(INTERACTIVE_FLOOR_WATER)
        debug_print(f'PLAYER-HAZARD COLLISION - killed by WATER')
      else:
        debug_print(f'CREATURE-HAZARD COLLISION - killed by WATER')
    if SINGLETONS[TILE].interactive_floors[INTERACTIVE_FLOOR_FIRE] == id:
      if entity.dead: return
      if INTERACTIVE_FLOOR_FIRE in entity.invincible_to: return
      if entity_is_player and entity.boots_fire: return
      entity.set_dead(True)
      if entity_is_player:
        set_global_KILLING_HAZARD(INTERACTIVE_FLOOR_FIRE)
        debug_print(f'PLAYER-HAZARD COLLISION - killed by FIRE')
      else:
        debug_print(f'CREATURE-HAZARD COLLISION - killed by FIRE')

  def handle_collision_with_wall(self, entity):
    if entity != SINGLETONS[PLAYER]: return
    entity_row = entity.row
    entity_col = entity.col

    if self.MAP[entity_row][entity_col][LAYER_IDX_WALLS] != None and (entity_row, entity_col) not in self.walls_to_delete_by_coords:
      self.walls_to_delete_by_coords[(entity_row, entity_col)] = get_global_GAME_TICKS()
      debug_print(f'PLAYER-WALL COLLISION')


  def handle_collision_with_pickup(self, entity):
    if entity != SINGLETONS[PLAYER]: return
    entity_row = entity.row
    entity_col = entity.col

    if self.MAP[entity_row][entity_col][LAYER_IDX_PICKUPS] != None and (entity_row, entity_col) not in self.pickups_to_delete_by_coords:
      self.pickups_to_delete_by_coords[(entity_row, entity_col)] = get_global_GAME_TICKS()
      debug_print(f'PLAYER-PICKUP COLLISION')

      if self.MAP[entity_row][entity_col][LAYER_IDX_PICKUPS] == SINGLETONS[TILE].pickups[PICKUP_CHIP]:
        self.chips_required -= 1
        debug_print(f'chips required: - {self.chips_required}')
      if self.MAP[entity_row][entity_col][LAYER_IDX_PICKUPS] == SINGLETONS[TILE].pickups[PICKUP_KEY_BLUE]:
        entity.keys_blue += 1
        debug_print(f'blue keys: - {entity.keys_blue}')
      if self.MAP[entity_row][entity_col][LAYER_IDX_PICKUPS] == SINGLETONS[TILE].pickups[PICKUP_KEY_RED]:
        entity.keys_red += 1
        debug_print(f'red keys: - {entity.keys_red}')
      if self.MAP[entity_row][entity_col][LAYER_IDX_PICKUPS] == SINGLETONS[TILE].pickups[PICKUP_KEY_GREEN]:
        entity.keys_green += 1
        debug_print(f'green keys: - {entity.keys_green}')
      if self.MAP[entity_row][entity_col][LAYER_IDX_PICKUPS] == SINGLETONS[TILE].pickups[PICKUP_KEY_YELLOW]:
        entity.keys_yellow += 1
        debug_print(f'yellow keys: - {entity.keys_yellow}')


  def handle_all_collisions(self):
    for entity in [ SINGLETONS[PLAYER], *self.all_creatures ]:
      self.handle_collision_with_creature(entity)
      self.handle_collision_with_interactive_floor(entity)
      self.handle_collision_with_wall(entity)
      self.handle_collision_with_pickup(entity)


  # ========== UPDATES ========== #

  def update_all_creatures(self):
    for i in range(len(self.all_creatures)):
      creature = self.all_creatures[i]
      creature.update()
      # to-do creature is not moving, AND the thing that killed it (if moving entity) is also not moving
      if creature.dead and creature.move_time == None:
        # debug_print(f'DELETING {creature}')
        self.MAP[creature.row][creature.col][LAYER_IDX_CREATURES] = None
        self.creatures_to_delete_by_idx.add(i)

    if len(self.creatures_to_delete_by_idx):
      self.all_creatures = [ self.all_creatures[i] for i in range(len(self.all_creatures)) if i not in self.creatures_to_delete_by_idx ]
      self.creatures_to_delete_by_idx.clear()
      debug_print(f'Number of creatures remaining: {len(self.all_creatures)}')

  def update_all_walls(self):
    coords_to_delete = []
    for (row, col) in self.walls_to_delete_by_coords:
      t = self.walls_to_delete_by_coords[(row, col)]
      if get_global_GAME_TICKS() - t >= SINGLETONS[PLAYER].cooldown:
        coords_to_delete.append((row, col))

    for (row, col) in coords_to_delete:
      del self.walls_to_delete_by_coords[(row, col)]
      self.MAP[row][col][LAYER_IDX_WALLS] = None
      # Or, other logic depending on the wall type

  def update_all_pickups(self):
    coords_to_delete = []
    for (row, col) in self.pickups_to_delete_by_coords:
      t = self.pickups_to_delete_by_coords[(row, col)]
      if get_global_GAME_TICKS() - t >= SINGLETONS[PLAYER].cooldown:
        coords_to_delete.append((row, col))

    for (row, col) in coords_to_delete:
      del self.pickups_to_delete_by_coords[(row, col)]
      self.MAP[row][col][LAYER_IDX_PICKUPS] = None


  def update(self):
    self.handle_all_movement_requests()
    self.update_all_creatures()
    self.update_all_walls()
    self.update_all_pickups()
    self.handle_all_collisions()