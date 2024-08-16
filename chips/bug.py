from globals import *
from utils import *

from creature import Creature

class Bug(Creature):

  def __init__(self):

    # super() is the parent class; here we call the parent's init
    super().__init__()

    # CONSTANTS
    self.name = ENTITY_BUG
    self.cooldown = 200
    self.redirection_transforms = [ 270, 0, 90, 180 ]
    self.invincible_to = set(())

    # VARIABLES

  def update(self):
    super().update()