from globals import *
from constants import *
from utils import *

import math

class Camera():

  def __init__(self):

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

    # # Test surfaces
    # self.test_colors = [
    #   'lightgray',
    #   'darkgray',
    #   'red',
    # ]
    # self.test_sprites = [ pg.Surface((self.TILE_SIZE_IN_PX, self.TILE_SIZE_IN_PX), pg.SRCALPHA) for _ in range(len(self.test_colors)) ]
    # for i in range(len(self.test_colors)): self.test_sprites[i].fill(self.test_colors[i])

    # Init
    self.camera_destination_row = None
    self.camera_destination_col = None

  def draw(self, SCREEN):
    SCREEN.blit(self.image, self.rect)
    self.draw_messages()

  def update_camera_world_pos(self):

    player_row = SINGLETONS[PLAYER].row
    player_col = SINGLETONS[PLAYER].col

    # NOTE: values are integers
    self.camera_destination_row = self.MIN_ROW if player_row < self.MIN_ROW \
                                    else self.MAX_ROW if player_row > self.MAX_ROW \
                                    else player_row
    self.camera_destination_col = self.MIN_COL if player_col < self.MIN_COL \
                                    else self.MAX_COL if player_col > self.MAX_COL \
                                    else player_col

    # NOTE: camera does not move when you are close to the edge of the map, hence 0. else, values may be floats
    self.moving_camera_offset_x = 0 if (SINGLETONS[PLAYER].moving_sprite_offset_x < 0 and player_col < self.MIN_COL \
                                      or SINGLETONS[PLAYER].moving_sprite_offset_x > 0 and player_col > self.MAX_COL) \
                                    else SINGLETONS[PLAYER].moving_sprite_offset_x
    self.moving_camera_offset_y = 0 if (SINGLETONS[PLAYER].moving_sprite_offset_y < 0 and player_row < self.MIN_ROW \
                                      or SINGLETONS[PLAYER].moving_sprite_offset_y > 0 and player_row > self.MAX_ROW) \
                                    else SINGLETONS[PLAYER].moving_sprite_offset_y

    # NOTE: values are floats, and must be bounded by MIN_ROW and MAX_ROW to avoid bug when moving in the direction away from the nearby edge
    self.camera_actual_row = self.camera_destination_row - self.moving_camera_offset_y
    self.camera_actual_row = max(self.camera_actual_row, self.MIN_ROW)
    self.camera_actual_row = min(self.camera_actual_row, self.MAX_ROW)

    self.camera_actual_col = self.camera_destination_col - self.moving_camera_offset_x
    self.camera_actual_col = max(self.camera_actual_col, self.MIN_COL)
    self.camera_actual_col = min(self.camera_actual_col, self.MAX_COL)


  def draw_all_to_self_image(self):
    
    # Clear surface
    self.image.fill('black')

    screen_center_col = math.floor(self.VIEWPORT_WIDTH_IN_TILES / 2)
    screen_center_row = math.floor(self.VIEWPORT_HEIGHT_IN_TILES / 2)

    # Draw static tiles (need extra buffer for scrolling camera during movement)

    for row in range(-1, self.VIEWPORT_HEIGHT_IN_TILES + 1):
      map_row = self.camera_destination_row - math.floor(self.VIEWPORT_HEIGHT_IN_TILES / 2) + row
      for col in range(-1, self.VIEWPORT_WIDTH_IN_TILES + 1):
        map_col = self.camera_destination_col - math.floor(self.VIEWPORT_WIDTH_IN_TILES / 2) + col
        if not (0 <= map_row < SINGLETONS[MAP].HEIGHT_IN_TILES and 0 <= map_col < SINGLETONS[MAP].WIDTH_IN_TILES): continue
        for x in SINGLETONS[MAP].MAP[map_row][map_col]:
          if x == None: continue

          is_instance = type(x) != str
          if is_instance: continue

          id = x

          self.image.blit(
            SINGLETONS[TILE].surfaces[id],
            (
              (col + (self.camera_destination_col - self.camera_actual_col)) * self.TILE_SIZE_IN_PX,
              (row + (self.camera_destination_row - self.camera_actual_row)) * self.TILE_SIZE_IN_PX,
            )
          )

    # Draw entities (draw player last)

    for entity in [ *SINGLETONS[MAP].all_creatures, SINGLETONS[PLAYER] ]:

      entity_true_col = entity.col - entity.moving_sprite_offset_x
      entity_camera_offset_x = self.camera_actual_col - entity_true_col
      entity_camera_screen_offset_x = screen_center_col - entity_camera_offset_x

      entity_true_row = entity.row - entity.moving_sprite_offset_y
      entity_camera_offset_y = self.camera_actual_row - entity_true_row
      entity_camera_screen_offset_y = screen_center_row - entity_camera_offset_y

      id_by_dir = SINGLETONS[TILE].entities[entity.name][entity.dir]
      player_special_id = None
      killing_hazard = get_global_KILLING_HAZARD()
      death_tile_id = SINGLETONS[TILE].death_tiles[killing_hazard] if killing_hazard and entity == SINGLETONS[PLAYER] and get_global_GAME_OVER() else None
      surface_to_draw = SINGLETONS[TILE].surfaces[ player_special_id or death_tile_id or id_by_dir ]

      self.image.blit(
        surface_to_draw,
        (
          entity_camera_screen_offset_x * self.TILE_SIZE_IN_PX,
          entity_camera_screen_offset_y * self.TILE_SIZE_IN_PX
        )
      )

  def draw_messages(self):
    # player_dead_and_entities_stopped = SINGLETONS[PLAYER].dead and SINGLETONS[PLAYER].move_time == None and (KILLING_ENTITY == None or KILLING_ENTITY.move_time == None)
    if get_global_GAME_OVER():
      text_surface = FONT.render('YOU DIED', False, 'yellow')
      SCREEN.blit(text_surface, (0, 0))

  def update(self):
    self.update_camera_world_pos()
    self.draw_all_to_self_image()