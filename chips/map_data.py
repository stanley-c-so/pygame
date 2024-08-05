# import pygame as pg
# import os

# FS_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class MapData():
  
  def __init__(self):

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
      [['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['018', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, '400'], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, '201', None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None], ['000', None, None, None, None]],
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