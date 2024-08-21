import pygame as pg

from globals import *
from constants import *

DIRS = [ U, R, D, L ]

def dir_with_applied_transformation(dir, transform):
  idx_delta = 0 if transform == 0 \
                else 1 if transform == 90 \
                else 2 if transform == 180 \
                else 3 if transform == 270 \
                else -1
  
  if idx_delta == -1: assert False
  return DIRS[ (DIRS.index(dir) + idx_delta) % 4 ]

def flatten(list_of_lists):
  output = []
  for l in list_of_lists:
    for x in l:
      output.append(x)
  return output

# ========== TESTING ========== #

def debug_print(*args):
  if DEBUG: print(f"TRUE TICKS {pg.time.get_ticks()} | GAME TICKS {get_global_GAME_TICKS()} |", *args)