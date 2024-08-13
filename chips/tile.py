import pygame as pg
import os

from globals import *
from utils import *

FS_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class Tile():

  def __init__(self):

    self.ids = {
      None: {},
      '000': { 'filename': 'floor' },
      '018': { 'filename': 'water' },
      '201': { 'filename': 'wall', impassable: True },
      '312': { 'filename': 'ball_pink', dir: D },
      '313': { 'filename': 'ball_pink', dir: L },
      '314': { 'filename': 'ball_pink', dir: U },
      '315': { 'filename': 'ball_pink', dir: R },
      '400': { 'filename': 'chip_D', dir: D },
      '401': { 'filename': 'chip_L', dir: L },
      '402': { 'filename': 'chip_U', dir: U },
      '403': { 'filename': 'chip_R', dir: R },
    }

    IMAGE_SIDE_LENGTH_IN_PX = 32
    IMAGE_SCALE = 2

    self.surfaces = {
      id: pg.transform.scale(
        pg.image.load(FS_CURRENT_DIR + '\\' + f'{self.ids[id]["filename"]}.png').convert_alpha(),
        (IMAGE_SIDE_LENGTH_IN_PX * IMAGE_SCALE, IMAGE_SIDE_LENGTH_IN_PX * IMAGE_SCALE)
      ) for id in self.ids \
        if id != None
    }
    for surface in self.surfaces.values(): surface.set_colorkey((255, 192, 255))

    self.entities = {
      ENTITY_CHIP: { D: '400', L: '401', U: '402', R: '403' },
      ENTITY_BUG: { D: '300', L: '301', U: '302', R: '303' },
      ENTITY_PARAMECIUM: { D: '304', L: '305', U: '306', R: '307' },
      ENTITY_TANK: { D: '308', L: '309', U: '310', R: '311' },
      ENTITY_BALL_PINK: { D: '312', L: '313', U: '314', R: '315' },
      ENTITY_BALL_BLUE: { D: '316', L: '317', U: '318', R: '319' },
      ENTITY_GLIDER: { D: '320', L: '321', U: '322', R: '323' },
      ENTITY_FIREBALL: { D: '324', L: '325', U: '326', R: '327' },
      ENTITY_TEETH: { D: '328', L: '329', U: '330', R: '331' },
      ENTITY_BLOB: { D: '332', L: '333', U: '334', R: '335' },
    }

  def is_player(self, id):
    return id in ('400', '401', '402', '403')
  
  def is_pinkball(self, id):
    return id in ('312', '313', '314', '315')