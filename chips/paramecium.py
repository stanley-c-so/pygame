from globals import *
from constants import *
from utils import *

from creature import Creature

class Paramecium(Creature):

  def __init__(self):

    # super() is the parent class; here we call the parent's init
    super().__init__()

    # CONSTANTS
    self.name = ENTITY_PARAMECIUM
    self.cooldown = 200
    self.redirection_transforms = [ 90, 0, 270, 180 ]
    self.invincible_to = set(())

    # VARIABLES

  def update(self):
    super().update()