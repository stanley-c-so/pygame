from globals import *
from utils import *

from creature import Creature

class Fireball(Creature):

  def __init__(self):

    # super() is the parent class; here we call the parent's init
    super().__init__()

    self.name = ENTITY_FIREBALL

    self.cooldown = 200

    self.redirection_transforms = [ 90, 270, 180 ]

  def update(self):
    super().update()