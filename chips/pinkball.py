from globals import *
from constants import *
from utils import *

from creature import Creature

class Pinkball(Creature):

  def __init__(self):

    # super() is the parent class; here we call the parent's init
    super().__init__()

    # CONSTANTS
    self.name = ENTITY_BALL_PINK
    self.cooldown = 200
    self.redirection_transforms = [ 0, 180 ]
    self.invincible_to = set(())

    # VARIABLES

  def update(self):
    super().update()