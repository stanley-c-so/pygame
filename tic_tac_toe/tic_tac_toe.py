import pygame as pg
from sys import exit

# ========== METHODS ========== #

def draw_board():
  screen.blit(H_LINE, H_LINE_RECT_TOP)
  screen.blit(H_LINE, H_LINE_RECT_BOTTOM)
  screen.blit(V_LINE, V_LINE_RECT_LEFT)
  screen.blit(V_LINE, V_LINE_RECT_RIGHT)

def redraw():
  screen.fill(BACKGROUND_COLOR)
  draw_board()

def restart():
  global board
  global turn
  board = [ [0] * 3 for _ in range(3) ]
  turn = 1
  redraw()

def check_win(r, c):
  return all(board[i][c] == board[r][c] for i in range(3))    \
    or all(board[r][i] == board[r][c] for i in range(3))      \
    or all(board[i][i] == board[r][c] for i in range(3))      \
    or all(board[i][2 - i] == board[r][c] for i in range(3))

def draw_shape(turn, clickable_square):
  surf = pg.Surface((CLICKABLE_SQUARE_SIZE, CLICKABLE_SQUARE_SIZE), pg.SRCALPHA)
  if turn == 1:
    pg.draw.circle(surf, O_COLOR, (CLICKABLE_SQUARE_SIZE/2, CLICKABLE_SQUARE_SIZE/2), SHAPE_SIZE/2, SHAPE_THICKNESS)
  elif turn == -1:
    PADDING = (CLICKABLE_SQUARE_SIZE - SHAPE_SIZE) / 2
    pg.draw.line(surf, X_COLOR, (PADDING, PADDING), (PADDING + SHAPE_SIZE, PADDING + SHAPE_SIZE), SHAPE_THICKNESS)
    pg.draw.line(surf, X_COLOR, (PADDING, PADDING + SHAPE_SIZE), (PADDING + SHAPE_SIZE, PADDING), SHAPE_THICKNESS)
  screen.blit(surf, clickable_square)

def print_game_state():
  # global board
  print('BOARD:')
  for row in board:
    print(row)
  print('TURN:', turn)


# ========== CONSTANTS ========== #

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

SQUARE_SIZE = 150
LINE_THICKNESS = 10
BACKGROUND_COLOR = "Black"
BOARD_COLOR = "Blue"
CLICKABLE_SQUARE_SIZE = SQUARE_SIZE + LINE_THICKNESS

SHAPE_SIZE = SQUARE_SIZE * 0.8

SHAPE_THICKNESS = 2
O_COLOR = "Green"
X_COLOR = "Red"


# ========== SURFACES AND RECTS ========== #

H_LINE = pg.Surface((3 * SQUARE_SIZE + 2 * LINE_THICKNESS, LINE_THICKNESS))
H_LINE.fill(BOARD_COLOR)
H_LINE_RECT_TOP = H_LINE.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - SQUARE_SIZE/2 - LINE_THICKNESS/2))
H_LINE_RECT_BOTTOM = H_LINE.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + SQUARE_SIZE/2 + LINE_THICKNESS/2))

V_LINE = pg.Surface((LINE_THICKNESS, 3 * SQUARE_SIZE + 2 * LINE_THICKNESS))
V_LINE.fill(BOARD_COLOR)
V_LINE_RECT_LEFT = V_LINE.get_rect(center = (SCREEN_WIDTH/2 - SQUARE_SIZE/2 - LINE_THICKNESS/2, SCREEN_HEIGHT/2))
V_LINE_RECT_RIGHT = V_LINE.get_rect(center = (SCREEN_WIDTH/2 + SQUARE_SIZE/2 + LINE_THICKNESS/2, SCREEN_HEIGHT/2))

CLICKABLE_SQUARE = pg.Surface((CLICKABLE_SQUARE_SIZE, CLICKABLE_SQUARE_SIZE))
CLICKABLE_SQUARE_RECTS = [ [ CLICKABLE_SQUARE.get_rect(center = (SCREEN_WIDTH/2 + CLICKABLE_SQUARE_SIZE * c, SCREEN_HEIGHT/2 + CLICKABLE_SQUARE_SIZE * r)) for c in range(-1, 2) ] for r in range(-1, 2) ]


# ========== GAME STATE VARIABLES ========== #

# board = [ [0] * 3 for _ in range(3) ]
# turn = 1
board = None
turn = None


# ========== TESTING ========== #

# test_surf = pg.Surface((100, 100))
# test_surf.fill("Yellow")
# test_surf_rect = test_surf.get_rect(topleft = (0, 0))


# ========== GAME LOOP ========== #

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pg.font.Font(None, 30)

restart()

print('BOARD AT START', board)

while True:
  for event in pg.event.get():
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      pg.quit()
      exit()

    if event.type == pg.KEYDOWN and event.key == pg.K_r:
      restart()

    if event.type == pg.MOUSEBUTTONDOWN:

      click_x, click_y = event.pos
      for r, row in enumerate(CLICKABLE_SQUARE_RECTS):
        for c, clickable_square in enumerate(row):
          if board[r][c] == 0 and clickable_square.collidepoint(event.pos):

            board[r][c] = turn
            draw_shape(turn, clickable_square)

            if check_win(r, c):
              print("SOMEONE WON")
              screen.fill("Pink")
            else:
              turn *= -1

            print_game_state()
            break

  pg.display.update()

  # draw()