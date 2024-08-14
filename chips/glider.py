from globals import *
from utils import *

from creature import Creature

class Glider(Creature):

  def __init__(self):

    # super() is the parent class; here we call the parent's init
    super().__init__()

    self.name = ENTITY_GLIDER

    self.cooldown = 200

    self.redirection_transforms = [ 270, 90, 180 ]

  def update(self):
    super().update()