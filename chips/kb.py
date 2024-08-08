from globals import *

class Keyboard():

  def handle_keydown(self, key):
    match key:
      case pg.K_ESCAPE:
        INPUTS.add(INPUT_QUIT)
      case pg.K_r:
        INPUTS.add(INPUT_RESTART)

  def handle_keypress(self):
    keys = pg.key.get_pressed()

    if keys[pg.K_w]:
      INPUTS.add(INPUT_UP)
    if keys[pg.K_a]:
      INPUTS.add(INPUT_LEFT)
    if keys[pg.K_s]:
      INPUTS.add(INPUT_DOWN)
    if keys[pg.K_d]:
      INPUTS.add(INPUT_RIGHT)

  def update(self):
    self.handle_keypress()