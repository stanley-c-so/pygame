from globals import *

import math

class Camera(pg.sprite.Sprite):

  def __init__(self):
    self.init()

  # def __init__(self):
  def init(self):

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


  def update_camera_world_pos(self):

    self.camera_destination_row = self.MIN_ROW if SINGLETONS[PLAYER].row < self.MIN_ROW \
                        else self.MAX_ROW if SINGLETONS[PLAYER].row > self.MAX_ROW \
                        else SINGLETONS[PLAYER].row
    self.camera_destination_col = self.MIN_COL if SINGLETONS[PLAYER].col < self.MIN_COL \
                        else self.MAX_COL if SINGLETONS[PLAYER].col > self.MAX_COL \
                        else SINGLETONS[PLAYER].col

  def draw_all(self):
    
    # Clear surface
    self.image.fill('black')

    offset_sprite_camera_x = (SINGLETONS[PLAYER].moving_sprite_offset_x_in_px / self.TILE_SIZE_IN_PX) + SINGLETONS[PLAYER].col - self.camera_destination_col
    offset_sprite_camera_y = (SINGLETONS[PLAYER].moving_sprite_offset_y_in_px / self.TILE_SIZE_IN_PX) + SINGLETONS[PLAYER].row - self.camera_destination_row

    self.MIN_COL < SINGLETONS[PLAYER].col < self.MAX_COL

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
          # to-do: what if we refactor the map to hold a UUID of some entity instance?
          if SINGLETONS[PLAYER].move_time != None and id[0] == '4': continue

          # to-do: in fact, don't draw any moving entity

          # ORIGINAL CODE FOR SCROLLING CAMERA
          # self.image.blit(
          #   SINGLETONS[TILE].surfaces[id],
          #   (
          #     (col - offset_sprite_camera_x) * self.TILE_SIZE_IN_PX,
          #     (row - offset_sprite_camera_y) * self.TILE_SIZE_IN_PX
          #   )
          # )

          self.image.blit(
            SINGLETONS[TILE].surfaces[id],
            (
              (col - (offset_sprite_camera_x if self.MIN_COL < SINGLETONS[PLAYER].col < self.MAX_COL else 0)) * self.TILE_SIZE_IN_PX,
              (row - (offset_sprite_camera_y if self.MIN_ROW < SINGLETONS[PLAYER].row < self.MAX_ROW else 0)) * self.TILE_SIZE_IN_PX
            )
          )

    # draw all moving entities' sprites

    if SINGLETONS[PLAYER].move_time != None:
      self.image.blit(
        SINGLETONS[TILE].surfaces['400'] if SINGLETONS[PLAYER].dir == D \
          else SINGLETONS[TILE].surfaces['401'] if SINGLETONS[PLAYER].dir == L \
          else SINGLETONS[TILE].surfaces['402'] if SINGLETONS[PLAYER].dir == U \
          else SINGLETONS[TILE].surfaces['403'],
        (
          # math.floor(self.VIEWPORT_WIDTH_IN_TILES / 2) * self.TILE_SIZE_IN_PX,
          # math.floor(self.VIEWPORT_HEIGHT_IN_TILES / 2) * self.TILE_SIZE_IN_PX
          (math.floor(self.VIEWPORT_WIDTH_IN_TILES / 2) + (0 if self.MIN_COL <= SINGLETONS[PLAYER].col <= self.MAX_COL else offset_sprite_camera_x)) * self.TILE_SIZE_IN_PX,
          (math.floor(self.VIEWPORT_HEIGHT_IN_TILES / 2) + (0 if self.MIN_ROW <= SINGLETONS[PLAYER].row <= self.MAX_ROW else offset_sprite_camera_y)) * self.TILE_SIZE_IN_PX
        )
      )
    
    # # TEST FOR ANIMATION:
    # # to-do - remove
    # if SINGLETONS[PLAYER].move_time != None:
    #   self.image.blit(
    #     SINGLETONS[TILE].surfaces['400'] if SINGLETONS[PLAYER].dir == D \
    #       else SINGLETONS[TILE].surfaces['401'] if SINGLETONS[PLAYER].dir == L \
    #       else SINGLETONS[TILE].surfaces['402'] if SINGLETONS[PLAYER].dir == U \
    #       else SINGLETONS[TILE].surfaces['403'],
    #     (
    #       (math.floor(self.VIEWPORT_WIDTH_IN_TILES / 2) + offset_sprite_camera_x) * self.TILE_SIZE_IN_PX,
    #       (math.floor(self.VIEWPORT_HEIGHT_IN_TILES / 2) + offset_sprite_camera_y) * self.TILE_SIZE_IN_PX
    #     )
    #   )

  def update(self):
    self.update_camera_world_pos()
    self.draw_all()