from globals import *

class Creature():

  def __init__(self):
    self.row = None
    self.col = None
    self.id = None
    self.dir = None
    self.moving_sprite_offset_x = 0
    self.moving_sprite_offset_y = 0
    self.move_time = None
    self.hit_wall = False

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

  def turn(self, dir, entity_name):
    self.set_dir(dir)
    self.set_id(SINGLETONS[TILE].entities[entity_name][dir])