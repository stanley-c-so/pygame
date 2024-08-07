from globals import *

import math

class Camera():

  # def __init__(self):
  #   self.init()

  def __init__(self):
  # def init(self):

    super().__init__()

    # Constants
    self.TILE_SIZE_IN_PX = 64
    self.VIEWPORT_WIDTH_IN_TILES = 9
    self.VIEWPORT_HEIGHT_IN_TILES = 9

    # Computed
    self.VIEWPORT_WIDTH_IN_PX = self.TILE_SIZE_IN_PX * self.VIEWPORT_WIDTH_IN_TILES
    self.VIEWPORT_HEIGHT_IN_PX = self.TILE_SIZE_IN_PX * self.VIEWPORT_HEIGHT_IN_TILES
    self.MIN_ROW = math.floor(self.VIEWPORT_HEIGHT_IN_TILES / 2)
    self.MAX_ROW = SINGLETONS[MAP].HEIGHT_IN_TILES - 1 - math.floor(self.VIEWPORT_HEIGHT_IN_TILES / 2)
    self.MIN_COL = math.floor(self.VIEWPORT_WIDTH_IN_TILES / 2)
    self.MAX_COL = SINGLETONS[MAP].WIDTH_IN_TILES - 1 - math.floor(self.VIEWPORT_WIDTH_IN_TILES / 2)

    self.zoom_scale = 1.0

    # Set image, rect
    self.image = pg.Surface((self.VIEWPORT_WIDTH_IN_PX, self.VIEWPORT_HEIGHT_IN_PX), pg.SRCALPHA)
    self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    # Test surfaces
    self.test_colors = [
      'lightgray',
      'darkgray',
      'red',
    ]
    self.test_sprites = [ pg.Surface((self.TILE_SIZE_IN_PX, self.TILE_SIZE_IN_PX), pg.SRCALPHA) for _ in range(len(self.test_colors)) ]
    for i in range(len(self.test_colors)): self.test_sprites[i].fill(self.test_colors[i])

    # Init
    self.camera_destination_row = None
    self.camera_destination_col = None

  def draw(self, SCREEN):
    SCREEN.blit(self.image, self.rect)

  def update_camera_world_pos(self):

    # NOTE: values are integers
    self.camera_destination_row = self.MIN_ROW if SINGLETONS[PLAYER].row < self.MIN_ROW \
                                    else self.MAX_ROW if SINGLETONS[PLAYER].row > self.MAX_ROW \
                                    else SINGLETONS[PLAYER].row
    self.camera_destination_col = self.MIN_COL if SINGLETONS[PLAYER].col < self.MIN_COL \
                                    else self.MAX_COL if SINGLETONS[PLAYER].col > self.MAX_COL \
                                    else SINGLETONS[PLAYER].col

    # NOTE: camera does not move when you are close to the edge of the map, hence 0. else, values may be floats
    self.moving_camera_offset_x = 0 if (SINGLETONS[PLAYER].moving_sprite_offset_x < 0 and SINGLETONS[PLAYER].col < self.MIN_COL \
                                      or SINGLETONS[PLAYER].moving_sprite_offset_x > 0 and SINGLETONS[PLAYER].col > self.MAX_COL) \
                                    else SINGLETONS[PLAYER].moving_sprite_offset_x
    self.moving_camera_offset_y = 0 if (SINGLETONS[PLAYER].moving_sprite_offset_y < 0 and SINGLETONS[PLAYER].row < self.MIN_ROW \
                                      or SINGLETONS[PLAYER].moving_sprite_offset_y > 0 and SINGLETONS[PLAYER].row > self.MAX_ROW) \
                                    else SINGLETONS[PLAYER].moving_sprite_offset_y

    # NOTE: values are floats, and must be bounded by MIN_ROW and MAX_ROW to avoid bug when moving in the direction away from the nearby edge
    self.camera_actual_row = self.camera_destination_row - self.moving_camera_offset_y
    self.camera_actual_row = max(self.camera_actual_row, self.MIN_ROW)
    self.camera_actual_row = min(self.camera_actual_row, self.MAX_ROW)

    self.camera_actual_col = self.camera_destination_col - self.moving_camera_offset_x
    self.camera_actual_col = max(self.camera_actual_col, self.MIN_COL)
    self.camera_actual_col = min(self.camera_actual_col, self.MAX_COL)


  def draw_all(self):
    
    # Clear surface
    self.image.fill('black')

    # Draw tiles (need extra buffer for scrolling camera during movement)
    for row in range(-1, self.VIEWPORT_HEIGHT_IN_TILES + 1):
      map_row = self.camera_destination_row - math.floor(self.VIEWPORT_HEIGHT_IN_TILES / 2) + row
      for col in range(-1, self.VIEWPORT_WIDTH_IN_TILES + 1):
        map_col = self.camera_destination_col - math.floor(self.VIEWPORT_WIDTH_IN_TILES / 2) + col
        if not (0 <= map_row < SINGLETONS[MAP].HEIGHT_IN_TILES and 0 <= map_col < SINGLETONS[MAP].WIDTH_IN_TILES): continue
        for id in SINGLETONS[MAP].MAP[map_row][map_col]:
          if id == None: continue

          # ORIGINAL CODE WITHOUT SCROLLING CAMERA
          # self.image.blit(SINGLETONS[TILE].surfaces[id], (col * self.TILE_SIZE_IN_PX, row * self.TILE_SIZE_IN_PX))

          # don't draw the player here when moving
          # to-do: in fact, don't draw any moving entity
          # to-do: in fact, don't draw any entities at all that can potentially move
          # to-do: what if we refactor the map to hold a UUID of some entity instance?
          if SINGLETONS[PLAYER].move_time != None and id[0] == '4': continue

          self.image.blit(
            SINGLETONS[TILE].surfaces[id],
            (
              (col + (self.camera_destination_col - self.camera_actual_col)) * self.TILE_SIZE_IN_PX,
              (row + (self.camera_destination_row - self.camera_actual_row)) * self.TILE_SIZE_IN_PX,
            )
          )

    # draw all moving entities' sprites

    screen_center_col = math.floor(self.VIEWPORT_WIDTH_IN_TILES / 2)
    screen_center_row = math.floor(self.VIEWPORT_HEIGHT_IN_TILES / 2)
    if SINGLETONS[PLAYER].move_time != None:

      player_true_col = SINGLETONS[PLAYER].col - SINGLETONS[PLAYER].moving_sprite_offset_x
      player_camera_offset_x = self.camera_actual_col - player_true_col
      player_camera_screen_offset_x = screen_center_col - player_camera_offset_x

      player_true_row = SINGLETONS[PLAYER].row - SINGLETONS[PLAYER].moving_sprite_offset_y
      player_camera_offset_y = self.camera_actual_row - player_true_row
      player_camera_screen_offset_y = screen_center_row - player_camera_offset_y

      self.image.blit(
        SINGLETONS[TILE].surfaces['400'] if SINGLETONS[PLAYER].dir == D \
          else SINGLETONS[TILE].surfaces['401'] if SINGLETONS[PLAYER].dir == L \
          else SINGLETONS[TILE].surfaces['402'] if SINGLETONS[PLAYER].dir == U \
          else SINGLETONS[TILE].surfaces['403'],
        (

          # to-do - make this general to the entity, not just the player
          player_camera_screen_offset_x * self.TILE_SIZE_IN_PX,
          player_camera_screen_offset_y * self.TILE_SIZE_IN_PX
        )
      )

  def update(self):
    self.update_camera_world_pos()
    self.draw_all()