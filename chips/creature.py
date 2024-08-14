from globals import *
from utils import *

class Creature():

  def __init__(self):
    self.row = None
    self.col = None
    self.id = None
    self.dir = None
    self.moving_sprite_offset_x = 0
    self.moving_sprite_offset_y = 0
    self.move_time = None
    self.hit_wall_or_creature = False
    self.dead = False

  # def __del__(self):
  #   debug_print("__del__")

  def handle_reset_movement_timers(self):
    if self.move_time != None and get_global_GAME_TICKS() - self.move_time >= self.cooldown:
      self.move_time = None
      self.hit_wall_or_creature = False

  def handle_moving_sprite_offset(self):

    # reset offset
    self.moving_sprite_offset_x = 0
    self.moving_sprite_offset_y = 0

    if self.move_time != None and not self.hit_wall_or_creature:
    # if self.move_time != None:

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

  def update_movement_request(self):
    if self.move_time == None:
      SINGLETONS[MAP].send_movement_request(( self, self.dir ))

  def update(self):
    self.handle_reset_movement_timers()
    self.handle_moving_sprite_offset()
    self.update_movement_request()

  def set_move_time(self, t):
    self.move_time = t

  def set_hit_wall_or_creature(self, bool):
    self.hit_wall_or_creature = bool

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