import copy
import sys
import pygame
import numpy as np
from constants import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.marked_sqrs = 0

    def final_state(self, show=False):
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    pygame.draw.line(screen, color, (col * SQSIZE + SQSIZE // 2, 20),
                                     (col * SQSIZE + SQSIZE // 2, HEIGHT - 20), LINE_WIDTH)
                return self.squares[0][col]

        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    pygame.draw.line(screen, color, (20, row * SQSIZE + SQSIZE // 2),
                                     (WIDTH - 20, row * SQSIZE + SQSIZE // 2), LINE_WIDTH)
                return self.squares[row][0]

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                pygame.draw.line(screen, color, (20, 20), (WIDTH - 20, HEIGHT - 20), CROSS_WIDTH)
            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                pygame.draw.line(screen, color, (20, HEIGHT - 20), (WIDTH - 20, 20), CROSS_WIDTH)
            return self.squares[1][1]

        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        return [(r, c) for r in range(ROWS) for c in range(COLS) if self.empty_sqr(r, c)]

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self, player=2):
        self.player = player

    def minimax(self, board, maximizing):
        case = board.final_state()
        if case == 1: return 1, None
        if case == 2: return -1, None
        if board.isfull(): return 0, None

        best_move = None
        if maximizing:
            max_eval = -100
            for (r, c) in board.get_empty_sqrs():
                temp = copy.deepcopy(board)
                temp.mark_sqr(r, c, 1)
                eval = self.minimax(temp, False)[0]
                if eval > max_eval:
                    max_eval, best_move = eval, (r, c)
            return max_eval, best_move
        else:
            min_eval = 100
            for (r, c) in board.get_empty_sqrs():
                temp = copy.deepcopy(board)
                temp.mark_sqr(r, c, self.player)
                eval = self.minimax(temp, True)[0]
                if eval < min_eval:
                    min_eval, best_move = eval, (r, c)
            return min_eval, best_move

    def eval(self, main_board):
        eval, move = self.minimax(main_board, False)
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.running = True
        self.show_lines()

    def show_lines(self):
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            pygame.draw.line(screen, CROSS_COLOR,
                             (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET),
                             (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET), CROSS_WIDTH)
            pygame.draw.line(screen, CROSS_COLOR,
                             (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET),
                             (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET), CROSS_WIDTH)
        else:
            pygame.draw.circle(screen, CIRC_COLOR,
                               (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2), RADIUS, CIRC_WIDTH)

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.player = self.player % 2 + 1

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():
    game = Game()
    board, ai = game.board, game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    board, ai = game.board, game.ai

            if event.type == pygame.MOUSEBUTTONDOWN and game.running:
                row, col = event.pos[1] // SQSIZE, event.pos[0] // SQSIZE
                if board.empty_sqr(row, col):
                    game.make_move(row, col)
                    if game.isover(): game.running = False

        if game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.eval(board)
            game.make_move(row, col)
            if game.isover(): game.running = False

        pygame.display.update()

main()