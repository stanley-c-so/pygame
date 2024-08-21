import pygame as pg
import os

from globals import *
from constants import *
from utils import *

from bug import Bug
from paramecium import Paramecium
from pinkball import Pinkball
from glider import Glider
from fireball import Fireball

FS_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

IMAGE_SIDE_LENGTH_IN_PX = 32
IMAGE_SCALE = 2
TRANSPARENT_COLORKEY = (255, 192, 255)

class Tile():

  def __init__(self):

    self.data_by_id = {
      None: {},

      '000': { filename: 'floor' },
      '013': { filename: 'clue' },
      '018': { filename: 'water', interactive: True },
      '019': { filename: 'water_dead' },
      '032': { filename: 'fire', interactive: True },
      '033': { filename: 'fire_dead' },
      '036': { filename: 'exit_1' },

      '100': { filename: 'key_blue', impassable_for_creatures: True },
      '101': { filename: 'key_red', impassable_for_creatures: True },
      '102': { filename: 'key_green', impassable_for_creatures: True },
      '103': { filename: 'key_yellow', impassable_for_creatures: True },
      '108': { filename: 'computer_chip', impassable_for_creatures: True },

      '200': { filename: 'socket', impassable_for_creatures: True },
      '201': { filename: 'wall', impassable: True },
      '207': { filename: 'lock_blue', impassable_for_creatures: True },
      '208': { filename: 'lock_red', impassable_for_creatures: True },
      '209': { filename: 'lock_green', impassable_for_creatures: True },
      '210': { filename: 'lock_yellow', impassable_for_creatures: True },
      
      '300': { filename: 'bug_D', dir: D, entity_class: Bug },
      '301': { filename: 'bug_L', dir: L, entity_class: Bug },
      '302': { filename: 'bug_U', dir: U, entity_class: Bug },
      '303': { filename: 'bug_R', dir: R, entity_class: Bug },
      '304': { filename: 'paramecium_UD', dir: D, entity_class: Paramecium },
      '305': { filename: 'paramecium_LR', dir: L, entity_class: Paramecium },
      '306': { filename: 'paramecium_UD', dir: U, entity_class: Paramecium },
      '307': { filename: 'paramecium_LR', dir: R, entity_class: Paramecium },
      '312': { filename: 'ball_pink', dir: D, entity_class: Pinkball },
      '313': { filename: 'ball_pink', dir: L, entity_class: Pinkball },
      '314': { filename: 'ball_pink', dir: U, entity_class: Pinkball },
      '315': { filename: 'ball_pink', dir: R, entity_class: Pinkball },
      '320': { filename: 'glider_D', dir: D, entity_class: Glider },
      '321': { filename: 'glider_L', dir: L, entity_class: Glider },
      '322': { filename: 'glider_U', dir: U, entity_class: Glider },
      '323': { filename: 'glider_R', dir: R, entity_class: Glider },
      '324': { filename: 'fireball', dir: D, entity_class: Fireball },
      '325': { filename: 'fireball', dir: L, entity_class: Fireball },
      '326': { filename: 'fireball', dir: U, entity_class: Fireball },
      '327': { filename: 'fireball', dir: R, entity_class: Fireball },

      '400': { filename: 'chip_D', dir: D },
      '401': { filename: 'chip_L', dir: L },
      '402': { filename: 'chip_U', dir: U },
      '403': { filename: 'chip_R', dir: R },
    }

    self.creatures = {
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

    self.creature_ids = flatten([ list(dd.values()) for dd in [ d for d in self.creatures.values() ] ])

    self.entities = {
      ENTITY_CHIP: { D: '400', L: '401', U: '402', R: '403' },
      **self.creatures
    }

    self.interactive_floors = {
      INTERACTIVE_FLOOR_WATER: '018',
      INTERACTIVE_FLOOR_FIRE: '032',
    }

    self.death_tiles = {
      INTERACTIVE_FLOOR_WATER: '019',
      INTERACTIVE_FLOOR_FIRE: '033',
    }

    self.surfaces = {
      id: pg.transform.scale(
        pg.image.load(FS_CURRENT_DIR + '\\' + f'{self.data_by_id[id]["filename"]}.png').convert_alpha(),
        (IMAGE_SIDE_LENGTH_IN_PX * IMAGE_SCALE, IMAGE_SIDE_LENGTH_IN_PX * IMAGE_SCALE)
      ) for id in self.data_by_id \
        if id != None
    }
    for surface in self.surfaces.values(): surface.set_colorkey(TRANSPARENT_COLORKEY)

  def is_player(self, id):
    return id in self.entities[ENTITY_CHIP].values()
  
  def is_creature(self, id):
    return id in self.creature_ids