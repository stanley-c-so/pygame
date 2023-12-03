import pygame as pg
import os

FS_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class Tile():
  
  def __init__(self):

    self.ids = {
      None: {},
      '000': { 'filename': 'floor' },
      '201': { 'filename': 'wall', 'impassable': True },
      '400': { 'filename': 'chip_standing_D' },
      '401': { 'filename': 'chip_standing_L' },
      '402': { 'filename': 'chip_standing_U' },
      '403': { 'filename': 'chip_standing_R' },
    }

    IMAGE_SIDE_LENGTH_IN_PX = 32
    IMAGE_SCALE = 2

    self.surfaces = { id: pg.transform.scale(pg.image.load(FS_CURRENT_DIR + '\\' + f'{self.ids[id]["filename"]}.png').convert_alpha(), (IMAGE_SIDE_LENGTH_IN_PX * IMAGE_SCALE, IMAGE_SIDE_LENGTH_IN_PX * IMAGE_SCALE)) for id in self.ids if id != None }
    for surface in self.surfaces.values(): surface.set_colorkey((255, 192, 255))