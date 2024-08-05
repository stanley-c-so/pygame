from globals import *

class Keyboard():

  def __init__(self, funcs):
    self.QUIT = funcs["QUIT"]
    self.RESTART = funcs["RESTART"]

  def handle_keydown(self):
    if pg.KEYDOWN in ALL_EVENT_TYPES_DICT:
      for event in ALL_EVENT_TYPES_DICT[pg.KEYDOWN]:
        match event.key:
          case pg.K_ESCAPE:
            debug_print("QUIT")
            self.QUIT()
          case pg.K_r:
            debug_print("RESTART")
            self.RESTART()

  # def handle_keypress(self):
  #   keys = pg.key.get_pressed()

  def update(self):
    self.handle_keydown()
    # self.handle_keypress()