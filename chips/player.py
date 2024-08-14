from globals import *
from utils import *

class Player():

  def __init__(self):
    self.cooldown = 200

    self.name = ENTITY_CHIP

    self.row = None
    self.col = None
    self.id = None
    self.dir = None
    self.moving_sprite_offset_x = 0
    self.moving_sprite_offset_y = 0
    self.move_time = None
    self.hit_wall = False
    self.dead = False

    self.boots_water = False
    self.boots_fire = False
    self.boots_forcefield = False
    self.boots_ice = False
    self.keys_blue = 0
    self.keys_red = 0
    self.keys_green = 0
    self.keys_yellow = 0

  def handle_reset_movement_timers(self):
    if self.move_time != None and get_global_GAME_TICKS() - self.move_time >= self.cooldown:
      # debug_print('STOPPING MOVEMENT')
      self.move_time = None
      self.hit_wall = False

  def handle_moving_sprite_offset(self):

    # reset offset
    self.moving_sprite_offset_x = 0
    self.moving_sprite_offset_y = 0

    if self.move_time != None and not self.hit_wall:

      abs_movement_across_tile_ratio = (get_global_GAME_TICKS() - self.move_time) / self.cooldown
      abs_movement_across_tile_ratio_in_px = abs_movement_across_tile_ratio * SINGLETONS[CAMERA].TILE_SIZE_IN_PX
      match self.dir:
        case 'D':
          self.moving_sprite_offset_y = (SINGLETONS[CAMERA].TILE_SIZE_IN_PX - abs_movement_across_tile_ratio_in_px) / SINGLETONS[CAMERA].TILE_SIZE_IN_PX
        case 'L':
          self.moving_sprite_offset_x = (abs_movement_across_tile_ratio_in_px - SINGLETONS[CAMERA].TILE_SIZE_IN_PX) / SINGLETONS[CAMERA].TILE_SIZE_IN_PX
        case 'U':
          self.moving_sprite_offset_y = (abs_movement_across_tile_ratio_in_px - SINGLETONS[CAMERA].TILE_SIZE_IN_PX) / SINGLETONS[CAMERA].TILE_SIZE_IN_PX
        case 'R':
          self.moving_sprite_offset_x = (SINGLETONS[CAMERA].TILE_SIZE_IN_PX - abs_movement_across_tile_ratio_in_px) / SINGLETONS[CAMERA].TILE_SIZE_IN_PX

  def handle_local_inputs(self):
    if INPUT_UP in INPUTS:
      SINGLETONS[MAP].send_movement_request(( self, U ))
    if INPUT_LEFT in INPUTS:
      SINGLETONS[MAP].send_movement_request(( self, L ))
    if INPUT_DOWN in INPUTS:
      SINGLETONS[MAP].send_movement_request(( self, D ))
    if INPUT_RIGHT in INPUTS:
      SINGLETONS[MAP].send_movement_request(( self, R ))

  def update(self):
    self.handle_reset_movement_timers()
    self.handle_moving_sprite_offset()
    self.handle_local_inputs()

  def set_move_time(self, t):
    self.move_time = t

  def set_hit_wall(self, bool):
    self.hit_wall = bool

  def set_coords(self, row, col):
    self.row = row
    self.col = col

  def set_dir(self, dir):
    self.dir = dir

  def set_id(self, id):
    self.id = id

  def turn(self, dir):
    self.set_dir(dir)
    self.set_id(SINGLETONS[TILE].entities[self.name][dir])

  def set_dead(self, bool):
    self.dead = bool