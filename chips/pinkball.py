from globals import *

from creature import Creature

class Pinkball(Creature):

  def __init__(self):

    # super() is the parent class; here we call the parent's init
    super().__init__()

    self.entity_name = ENTITY_BALL_PINK

    self.cooldown = 200