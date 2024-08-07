from globals import *

class Player():

  # def __init__(self):
  #   self.init()

  def __init__(self):
  # def init(self):
    self.COOLDOWN = 200
    # self.COOLDOWN = 500
    # self.COOLDOWN = 1000

    self.row, self.col, self.id, self.dir = self.update_world_pos()
    self.moving_sprite_offset_x = 0
    self.moving_sprite_offset_y = 0
    self.move_time = None
    self.dead = False

  def handle_reset_movement_timers(self):
    if self.move_time != None and pg.time.get_ticks() - self.move_time >= self.COOLDOWN:
      debug_print('STOPPING MOVEMENT')
      self.move_time = None

  def update_world_pos(self):
    found_player = False
    for row in range(SINGLETONS[MAP].HEIGHT_IN_TILES):
      for col in range(SINGLETONS[MAP].WIDTH_IN_TILES):
        if SINGLETONS[TILE].ids.get(SINGLETONS[MAP].MAP[row][col][4]).get('entity') == SINGLETONS[TILE].ENTITY_CHIP:
          self.row, self.col = row, col
          self.id = SINGLETONS[MAP].MAP[row][col][4]
          self.dir = SINGLETONS[TILE].ids[self.id]['dir']
          found_player = True
          break
      if found_player: break
    return self.row, self.col, self.id, self.dir

  def handle_moving_sprite_offset(self):

    # reset offset
    self.moving_sprite_offset_x = 0
    self.moving_sprite_offset_y = 0

    if self.move_time != None:

      abs_movement_across_tile_ratio = (pg.time.get_ticks() - self.move_time) / self.COOLDOWN
      abs_movement_across_tile_ratio_in_px = abs_movement_across_tile_ratio * SINGLETONS[CAMERA].TILE_SIZE_IN_PX
      # to-do: RECONSIDER THE MATH?
      match self.dir:
        case 'D':
          self.moving_sprite_offset_y = (SINGLETONS[CAMERA].TILE_SIZE_IN_PX - abs_movement_across_tile_ratio_in_px) / SINGLETONS[CAMERA].TILE_SIZE_IN_PX
        case 'L':
          self.moving_sprite_offset_x = (abs_movement_across_tile_ratio_in_px - SINGLETONS[CAMERA].TILE_SIZE_IN_PX) / SINGLETONS[CAMERA].TILE_SIZE_IN_PX
        case 'U':
          self.moving_sprite_offset_y = (abs_movement_across_tile_ratio_in_px - SINGLETONS[CAMERA].TILE_SIZE_IN_PX) / SINGLETONS[CAMERA].TILE_SIZE_IN_PX
        case 'R':
          self.moving_sprite_offset_x = (SINGLETONS[CAMERA].TILE_SIZE_IN_PX - abs_movement_across_tile_ratio_in_px) / SINGLETONS[CAMERA].TILE_SIZE_IN_PX

  def handle_inputs(self):
    if INPUT_UP in INPUTS:
      SINGLETONS[MAP].send_movement_request([ self, U ])
    if INPUT_LEFT in INPUTS:
      SINGLETONS[MAP].send_movement_request([ self, L ])
    if INPUT_DOWN in INPUTS:
      SINGLETONS[MAP].send_movement_request([ self, D ])
    if INPUT_RIGHT in INPUTS:
      SINGLETONS[MAP].send_movement_request([ self, R ])

  def update(self):
    self.update_world_pos()
    self.handle_reset_movement_timers()
    self.handle_moving_sprite_offset()
    self.handle_inputs()