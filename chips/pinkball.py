from globals import *
from utils import *

from creature import Creature

class Pinkball(Creature):

  def __init__(self):

    # super() is the parent class; here we call the parent's init
    super().__init__()

    self.name = ENTITY_BALL_PINK

    self.cooldown = 200

    self.redirection_transforms = [180]

  def update(self):
    super().update()