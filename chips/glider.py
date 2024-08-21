from globals import *
from constants import *
from utils import *

from creature import Creature

class Glider(Creature):

  def __init__(self):

    # super() is the parent class; here we call the parent's init
    super().__init__()

    # CONSTANTS
    self.name = ENTITY_GLIDER
    self.cooldown = 200
    self.redirection_transforms = [ 0, 270, 90, 180 ]
    self.invincible_to = set((
      INTERACTIVE_FLOOR_WATER,
    ))

    # VARIABLES

  def update(self):
    super().update()