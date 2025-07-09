import numpy as np
import pygame
import sys
import math
import random

from constants import *

# ----- Game Logic Functions -----
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT-1, -1, -1):
        if board[r][col] == 0:
            return r

def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

def print_board(board):
    print(np.flip(board, 0))

winning_positions = []

def winning_move(board, piece):
    global winning_positions
    winning_positions = []

    # Horizontal, vertical, positive and negative diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                winning_positions = [(r, c+i) for i in range(4)]
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                winning_positions = [(r+i, c) for i in range(4)]
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                winning_positions = [(r+i, c+i) for i in range(4)]
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)):
                winning_positions = [(r-i, c+i) for i in range(4)]
                return True

    return False

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    # Center column preference
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    score += center_array.count(piece) * 3

    # Horizontal, vertical, diagonals
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            score += evaluate_window([board[r+i][c+i] for i in range(WINDOW_LENGTH)], piece)
            score += evaluate_window([board[r+3-i][c+i] for i in range(WINDOW_LENGTH)], piece)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or not get_valid_locations(board)

def minimax(board, depth, alpha, beta, maximizing):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE): return (None, 1e14)
            elif winning_move(board, PLAYER_PIECE): return (None, -1e13)
            else: return (None, 0)
        return (None, score_position(board, AI_PIECE))

    best_col = random.choice(valid_locations)

    if maximizing:
        value = -math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            _, new_score = minimax(temp_board, depth-1, alpha, beta, False)
            if new_score > value:
                value, best_col = new_score, col
            alpha = max(alpha, value)
            if alpha >= beta: break
        return best_col, value

    else:
        value = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            _, new_score = minimax(temp_board, depth-1, alpha, beta, True)
            if new_score < value:
                value, best_col = new_score, col
            beta = min(beta, value)
            if alpha >= beta: break
        return best_col, value

# ----- Drawing -----
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, GRID_COLOR, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            color = EMPTY_COLOR
            if board[r][c] == PLAYER_PIECE:
                color = PLAYER_COLOR
            elif board[r][c] == AI_PIECE:
                color = AI_COLOR
            pygame.draw.circle(screen, color, (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for r, c in winning_positions:
        pygame.draw.circle(screen, (0,255,0), (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS, 5)

    pygame.display.update()

# ----- Game Setup -----
pygame.init()

SQUARESIZE = 100
width, height = COLUMN_COUNT * SQUARESIZE, (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = SQUARESIZE//2 - 5

screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 75) or pygame.font.Font(None, 75)
screen.fill(BACKGROUND_COLOR)

board = create_board()
draw_board(board)
pygame.display.update()

game_over = False
turn = random.randint(PLAYER, AI)

# ----- Main Game Loop -----
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARESIZE))
            pygame.draw.circle(screen, PLAYER_COLOR, (event.pos[0], SQUARESIZE//2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER:
            pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARESIZE))
            col = event.pos[0] // SQUARESIZE

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)

                if winning_move(board, PLAYER_PIECE):
                    label = myfont.render("Player wins!", 1, PLAYER_COLOR)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn = AI
                draw_board(board)

    if turn == AI and not game_over:
        col, _ = minimax(board, 5, -math.inf, math.inf, True)
        if col is not None and is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("AI wins!", 1, AI_COLOR)
                screen.blit(label, (40, 10))
                game_over = True

            draw_board(board)
            turn = PLAYER

    if game_over:
        pygame.time.wait(5000)