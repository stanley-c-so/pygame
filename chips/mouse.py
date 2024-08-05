from globals import *

class Mouse():
  
  def __init__(self):
    self.mouse_pos = None
    self.pressed = False

  def update_mouse_pos(self):
    self.mouse_pos = pg.math.Vector2(pg.mouse.get_pos())

  def handle_left_click(self):
    if not pg.mouse.get_pressed()[0]:
      self.pressed = False
      return
    # if self.pressed:
    #   return
    self.pressed = True

  def update(self):
    self.update_mouse_pos()
    self.handle_left_click()