import pygame, sys 
import numpy as np

pygame.init()

WIDTH = 600
HEIGHT = 600
SQUARE_SIZE = 200
LINEA_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 65
CIRCLE_WIDTH = 15
X_WIDTH = 30
SPACE = 45

#Colores 
BG_COLOR = (47, 72, 88)
LINEA_COLOR = (51, 101, 138)
MARK_COLOR = (134, 187, 216)
CIRCLE_COLOR = (246, 174, 45)
CROSS_COLOR = (242, 100, 25)

pantalla = pygame.display.set_mode(( WIDTH, HEIGHT))
pygame.display.set_caption( 'Ta Te Ti')
Icon = pygame.image.load('src/Alien.png')
pygame.display.set_icon(Icon)
pantalla.fill( BG_COLOR )

#Tablero 
board = np.zeros( (BOARD_ROWS, BOARD_COLS) )

#Funciones 

def draw_lines():
    # Línea horizontal 1
    pygame.draw.line( pantalla, LINEA_COLOR, (0, 200), (600, 200), LINEA_WIDTH )
    # Línea horizontal 2
    pygame.draw.line( pantalla, LINEA_COLOR, (0, 400), (600, 400), LINEA_WIDTH )
    # línea vertical 1
    pygame.draw.line( pantalla, LINEA_COLOR, (200, 0), (200, 600), LINEA_WIDTH )
    # línea vertical 2
    pygame.draw.line( pantalla, LINEA_COLOR, (400, 0), (400, 600), LINEA_WIDTH )

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle( pantalla, MARK_COLOR, (int( col * 200 + 100), int( row * 200 + 100)), CIRCLE_RADIUS, CIRCLE_WIDTH )
            elif board[row][col] == 2:
                pygame.draw.line(pantalla, MARK_COLOR, (col * 200 + SPACE, row * 200 + 200 - SPACE), (col * 200 + 200 - SPACE, row * 200 + SPACE), X_WIDTH)
                pygame.draw.line(pantalla, MARK_COLOR, (col * 200 + SPACE, row * 200 + SPACE), (col * 200 + 200 - SPACE, row * 200 + 200 - SPACE), X_WIDTH)
            
                        
def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0

# if board is full or empty
def is_board_full():
    # firt loop -> throw all the rows
    for row in range(BOARD_ROWS):
        # second loop -> throw all the columns
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    # if we loop through all the board and don't have any empty square left
    return True


def check_win(player):
    # Verificar victorias verticales
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            vertical_win(col, player)
            return True

    # Verificar victorias horizontales
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            horizontal_win(row, player)
            return True

    # Verificar victorias diagonales
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        diagonal_asc_win(player)
        return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        diagonal_desc_win(player)
        return True

    return False


def vertical_win(col, player):
	posX = col * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( pantalla, color, (posX, 15), (posX, HEIGHT - 15), LINEA_WIDTH )


def horizontal_win(row, player):
	posY = row * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( pantalla, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH )


def diagonal_asc_win(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( pantalla, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

def diagonal_desc_win(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( pantalla, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )


def reset_board():
    pantalla.fill(BG_COLOR)
    draw_lines()
    player = 1
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0
  

draw_lines()

game_over = False
player = 1

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = int(mouseY // 200)
            clicked_col = int(mouseX // 200)

            if available_square(clicked_row, clicked_col):
                if player == 1:
                    mark_square(clicked_row, clicked_col, 1)
                    if check_win(player):
                        game_over = True
                    player = 2

                elif player == 2:
                    mark_square(clicked_row, clicked_col, 2)
                    if check_win(player):
                        game_over = True
                    player = 1

                draw_figures()

                # print(board)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        game_over = False
        reset_board()

    pygame.display.update()
