import asyncio
import platform
import pygame
import chess
import os

from constants import *


# Initialize Pygame
pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Chess: Human vs AI")

# Load sound effects
MOVE_SOUND = pygame.mixer.Sound("move.wav")
CAPTURE_SOUND = pygame.mixer.Sound("capture.wav")


# Load chess piece images
PIECE_IMAGES = {}
for piece in ['K', 'Q', 'R', 'B', 'N', 'P']:
    for color in ['w', 'b']:
        filename = f"pieces/{color}{piece}.png"
        image = pygame.image.load(filename)
        PIECE_IMAGES[color + piece] = pygame.transform.scale(image, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))

# Piece values for AI evaluation
PIECE_VALUES = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0}

# Central squares for evaluation
CENTER_SQUARES = {chess.D4, chess.D5, chess.E4, chess.E5}

# Initialize chess board
board = chess.Board()
selected_square = None
valid_moves = []

# Draw the chessboard
def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces
def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row, col = 7 - chess.square_rank(square), chess.square_file(square)
            piece_key = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()
            screen.blit(PIECE_IMAGES[piece_key], (col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5))

# Highlight selected square and valid moves
def draw_highlights():
    if selected_square is not None:
        row, col = 7 - chess.square_rank(selected_square), chess.square_file(selected_square)
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(HIGHLIGHT)
        screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        for move in valid_moves:
            row, col = 7 - chess.square_rank(move.to_square), chess.square_file(move.to_square)
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Enhanced evaluation function (simplified for speed)
def evaluate_board():
    if board.is_checkmate():
        return float('-inf') if board.turn == chess.WHITE else float('inf')
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    total = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = PIECE_VALUES[piece.symbol().lower()]
            total += value if piece.color == chess.BLACK else -value

    for square in CENTER_SQUARES:
        piece = board.piece_at(square)
        if piece:
            bonus = 0.5 if piece.piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP] else 0.3
            total += bonus if piece.color == chess.BLACK else -bonus

    for color in [chess.WHITE, chess.BLACK]:
        king_square = board.king(color)
        if king_square in CENTER_SQUARES:
            penalty = 0.5
            total += penalty if color == chess.WHITE else -penalty

    return total

# Minimax with alpha-beta pruning and move ordering
def minimax(depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board()

    legal_moves = list(board.legal_moves)
    legal_moves.sort(key=lambda move: (
        -1 if board.is_capture(move) else 0,
        -1 if board.gives_check(move) else 0
    ))

    if maximizing:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# AI move selection
def make_ai_move():
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None

    best_move = None
    best_value = float('-inf')
    best_capture = False

    for move in legal_moves:
        is_capture = board.is_capture(move)
        board.push(move)
        value = minimax(3, float('-inf'), float('inf'), False)
        board.pop()
        if value > best_value:
            best_value = value
            best_move = move
            best_capture = is_capture

    if best_move:
        board.push(best_move)
        if best_capture:
            CAPTURE_SOUND.play()
        else:
            MOVE_SOUND.play()

# Main game loop
async def main():
    global selected_square, valid_moves
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE:
                pos = pygame.mouse.get_pos()
                col, row = pos[0] // SQUARE_SIZE, 7 - (pos[1] // SQUARE_SIZE)
                square = chess.square(col, row)

                if selected_square is None:
                    piece = board.piece_at(square)
                    if piece and piece.color == chess.WHITE:
                        selected_square = square
                        valid_moves = [move for move in board.legal_moves if move.from_square == square]
                else:
                    for move in valid_moves:
                        if move.to_square == square:
                            is_capture = board.is_capture(move)
                            board.push(move)
                            if is_capture:
                                CAPTURE_SOUND.play()
                            else:
                                MOVE_SOUND.play()
                            selected_square = None
                            valid_moves = []
                            make_ai_move()
                            break
                    else:
                        selected_square = None
                        valid_moves = []

        draw_board()
        draw_highlights()
        draw_pieces()
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

    pygame.quit()

# Run the game
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
