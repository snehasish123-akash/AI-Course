# !প্রোগ্রাম শুরু করার জন্য asyncio মডিউল আমদানি করা হয়েছে। এটি অ্যাসিঙ্ক্রোনাস প্রোগ্রামিংয়ের জন্য ব্যবহৃত হয়।
import asyncio
# !platform মডিউল আমদানি করা হয়েছে। এটি সিস্টেমের প্ল্যাটফর্ম (যেমন Emscripten) চেক করতে ব্যবহৃত হয়।
import platform
# !pygame লাইব্রেরি আমদানি করা হয়েছে। এটি গেম ডেভেলপমেন্টের জন্য গ্রাফিক্স, সাউন্ড এবং ইনপুট পরিচালনা করে।
import pygame
# !chess মডিউল আমদানি করা হয়েছে। এটি দাবা গেমের লজিক, বোর্ড এবং মুভ পরিচালনার জন্য ব্যবহৃত হয়।
import chess
# !os মডিউল আমদানি করা হয়েছে। এটি ফাইল এবং ডিরেক্টরি পরিচালনার জন্য ব্যবহৃত হয়, যদিও এই কোডে সরাসরি ব্যবহৃত হয়নি।
import os

# !constants ফাইল থেকে স্থির মান (যেমন বোর্ডের আকার, রঙ ইত্যাদি) আমদানি করা হয়েছে।
from constants import *

# !pygame ইনিশিয়ালাইজ করা হয়েছে। এটি pygame লাইব্রেরির সমস্ত মডিউল সক্রিয় করে।
pygame.init()
# !pygame-এর মিক্সার মডিউল ইনিশিয়ালাইজ করা হয়েছে। এটি সাউন্ড ইফেক্ট এবং মিউজিক পরিচালনার জন্য ব্যবহৃত হয়।
pygame.mixer.init()

# !গেম উইন্ডো তৈরি করা হয়েছে। BOARD_SIZE দ্বারা নির্ধারিত আকারে একটি স্ক্রিন তৈরি করা হয়।
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
# !উইন্ডোর শিরোনাম সেট করা হয়েছে। এটি গেম উইন্ডোর উপরে "Chess: Human vs AI" দেখাবে।
pygame.display.set_caption("Chess: Human vs AI")

# !দাবার চাল এবং ক্যাপচারের জন্য সাউন্ড ইফেক্ট লোড করা হয়েছে।
MOVE_SOUND = pygame.mixer.Sound("move.wav")  # !চাল দেওয়ার সময় বাজানো সাউন্ড।
CAPTURE_SOUND = pygame.mixer.Sound("capture.wav")  # !পিস ক্যাপচার করার সময় বাজানো সাউন্ড।

# !দাবার পিসের ছবি লোড করার জন্য একটি খালি ডিকশনারি তৈরি করা হয়েছে।
PIECE_IMAGES = {}
# !দাবার প্রতিটি পিস (কিং, কুইন ইত্যাদি) এবং রঙের জন্য লুপ চালানো হয়েছে।
for piece in ['K', 'Q', 'R', 'B', 'N', 'P']:  # !দাবার পিসের ধরন (K=King, Q=Queen ইত্যাদি)।
    for color in ['w', 'b']:  # !রঙ: 'w' হলো সাদা, 'b' হলো কালো।
        filename = f"pieces/{color}{piece}.png"  # !পিসের ছবির ফাইল পাথ তৈরি করা হয়েছে।
        image = pygame.image.load(filename)  # !ছবি লোড করা হয়েছে।
        PIECE_IMAGES[color + piece] = pygame.transform.scale(image, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))  # !ছবির আকার স্কেল করা হয়েছে যাতে বোর্ডে ফিট হয়।

# !AI-এর বোর্ড মূল্যায়নের জন্য পিসের মান নির্ধারণ করা হয়েছে।
PIECE_VALUES = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0}  # !প্রতিটি পিসের মান (পন=1, নাইট=3 ইত্যাদি)।

# !বোর্ডের কেন্দ্রীয় স্কোয়ারগুলোর সেট তৈরি করা হয়েছে। এগুলো মূল্যায়নে বোনাস দেওয়ার জন্য ব্যবহৃত হয়।
CENTER_SQUARES = {chess.D4, chess.D5, chess.E4, chess.E5}  # !কেন্দ্রীয় স্কোয়ার (D4, D5, E4, E5)।

# !দাবার বোর্ড ইনিশিয়ালাইজ করা হয়েছে। এটি দাবা গেমের প্রাথমিক অবস্থা তৈরি করে।
board = chess.Board()
# !কোনো স্কোয়ার নির্বাচিত না থাকলে None সেট করা হয়েছে।
selected_square = None
# !বৈধ চালের খালি লিস্ট তৈরি করা হয়েছে।
valid_moves = []

# !দাবার বোর্ড আঁকার ফাংশন সংজ্ঞায়িত করা হয়েছে।
def draw_board():
    # !প্রতিটি সারি এবং কলামের জন্য লুপ চালানো হয়েছে।
    for row in range(8):
        for col in range(8):
            # !স্কোয়ারের রঙ নির্ধারণ: সাদা বা ধূসর, চেকারবোর্ড প্যাটার্নের জন্য।
            color = WHITE if (row + col) % 2 == 0 else GRAY
            # !প্রতিটি স্কোয়ার আঁকা হয়েছে রঙ এবং অবস্থান ব্যবহার করে।
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# !দাবার পিস আঁকার ফাংশন সংজ্ঞায়িত করা হয়েছে।
def draw_pieces():
    # !বোর্ডের প্রতিটি স্কোয়ারের জন্য লুপ চালানো হয়েছে।
    for square in chess.SQUARES:
        # !স্কোয়ারে পিস আছে কিনা চেক করা হয়েছে।
        piece = board.piece_at(square)
        if piece:
            # !স্কোয়ারের সারি এবং কলাম গণনা করা হয়েছে (বোর্ডের উল্টো দিক থেকে)।
            row, col = 7 - chess.square_rank(square), chess.square_file(square)
            # !পিসের কী তৈরি করা হয়েছে (যেমন 'wK' বা 'bQ')।
            piece_key = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()
            # !পিসের ছবি স্ক্রিনে আঁকা হয়েছে।
            screen.blit(PIECE_IMAGES[piece_key], (col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5))

# !নির্বাচিত স্কোয়ার এবং বৈধ চাল হাইলাইট করার ফাংশন সংজ্ঞায়িত করা হয়েছে।
def draw_highlights():
    # !কোনো স্কোয়ার নির্বাচিত থাকলে এটি হাইলাইট করা হবে।
    if selected_square is not None:
        # !নির্বাচিত স্কোয়ারের সারি এবং কলাম গণনা করা হয়েছে।
        row, col = 7 - chess.square_rank(selected_square), chess.square_file(selected_square)
        # !একটি স্বচ্ছ সারফেস তৈরি করা হয়েছে হাইলাইটের জন্য।
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        # !সারফেসে হাইলাইট রঙ পূর্ণ করা হয়েছে।
        s.fill(HIGHLIGHT)
        # !নির্বাচিত স্কোয়ারে হাইলাইট আঁকা হয়েছে।
        screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        # !বৈধ চালগুলোর জন্য লুপ চালানো হয়েছে।
        for move in valid_moves:
            # !প্রতিটি বৈধ চালের গন্তব্য স্কোয়ারের সারি এবং কলাম গণনা করা হয়েছে।
            row, col = 7 - chess.square_rank(move.to_square), chess.square_file(move.to_square)
            # !গন্তব্য স্কোয়ারে হাইলাইট আঁকা হয়েছে।
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# !বোর্ডের মূল্যায়ন ফাংশন সংজ্ঞায়িত করা হয়েছে। এটি AI-এর জন্য বোর্ডের অবস্থা মূল্যায়ন করে।
def evaluate_board():
    # !যদি চেকমেট হয়, তবে প্লেয়ারের পক্ষে স্কোর নির্ধারণ করা হয়।
    if board.is_checkmate():
        return float('-inf') if board.turn == chess.WHITE else float('inf')
    # !স্টেলমেট বা অপর্যাপ্ত উপাদান হলে স্কোর ০ রিটার্ন করা হয়।
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # !মোট স্কোরের জন্য ভেরিয়েবল ইনিশিয়ালাইজ করা হয়েছে।
    total = 0
    # !প্রতিটি স্কোয়ারের জন্য লুপ চালানো হয়েছে।
    for square in chess.SQUARES:
        # !স্কোয়ারে পিস আছে কিনা চেক করা হয়েছে।
        piece = board.piece_at(square)
        if piece:
            # !পিসের মান নির্ধারণ করা হয়েছে।
            value = PIECE_VALUES[piece.symbol().lower()]
            # !কালো পিস হলে মান যোগ, সাদা হলে বিয়োগ করা হয়েছে।
            total += value if piece.color == chess.BLACK else -value

    # !কেন্দ্রীয় স্কোয়ারে পিস থাকলে বোনাস দেওয়া হয়েছে।
    for square in CENTER_SQUARES:
        piece = board.piece_at(square)
        if piece:
            # !পিসের ধরনের উপর ভিত্তি করে বোনাস নির্ধারণ করা হয়েছে।
            bonus = 0.5 if piece.piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP] else 0.3
            # !কালো পিস হলে বোনাস যোগ, সাদা হলে বিয়োগ।
            total += bonus if piece.color == chess.BLACK else -bonus

    # !কিং এর অবস্থানের জন্য পেনাল্টি দেওয়া হয়েছে।
    for color in [chess.WHITE, chess.BLACK]:
        king_square = board.king(color)
        if king_square in CENTER_SQUARES:
            penalty = 0.5
            total += penalty if color == chess.WHITE else -penalty

    # !মোট স্কোর রিটার্ন করা হয়েছে।
    return total

# !মিনিম্যাক্স অ্যালগরিদম ফাংশন সংজ্ঞায়িত করা হয়েছে। এটি AI-এর চাল নির্বাচনের জন্য ব্যবহৃত হয়।
def minimax(depth, alpha, beta, maximizing):
    # !গভীরতা ০ বা গেম শেষ হলে বোর্ড মূল্যায়ন করা হয়।
    if depth == 0 or board.is_game_over():
        return evaluate_board()

    # !বৈধ চালের লিস্ট তৈরি করা হয়েছে।
    legal_moves = list(board.legal_moves)
    # !চালগুলো সাজানো হয়েছে, ক্যাপচার এবং চেক দেওয়া চালকে প্রাধান্য দেওয়া হয়েছে।
    legal_moves.sort(key=lambda move: (
        -1 if board.is_capture(move) else 0,
        -1 if board.gives_check(move) else 0
    ))

    # !ম্যাক্সিমাইজিং প্লেয়ারের (কালো) জন্য।
    if maximizing:
        max_eval = float('-inf')  # !সর্বোচ্চ মূল্য ইনিশিয়ালাইজ করা হয়েছে।
        for move in legal_moves:
            board.push(move)  # !চাল প্রয়োগ করা হয়েছে।
            eval = minimax(depth - 1, alpha, beta, False)  # !পরবর্তী স্তরে মিনিম্যাক্স কল করা হয়েছে।
            board.pop()  # !চাল পূর্বাবস্থায় ফিরিয়ে আনা হয়েছে।
            max_eval = max(max_eval, eval)  # !সর্বোচ্চ মূল্য আপডেট করা হয়েছে।
            alpha = max(alpha, eval)  # !আলফা আপডেট করা হয়েছে।
            if beta <= alpha:  # !আলফা-বিটা প্রুনিং।
                break
        return max_eval
    else:
        min_eval = float('inf')  # !সর্বনিম্ন মূল্য ইনিশিয়ালাইজ করা হয়েছে।
        for move in legal_moves:
            board.push(move)  # !চাল প্রয়োগ করা হয়েছে।
            eval = minimax(depth - 1, alpha, beta, True)  # !পরবর্তী স্তরে মিনিম্যাক্স কল করা হয়েছে।
            board.pop()  # !চাল পূর্বাবস্থায় ফিরিয়ে আনা হয়েছে।
            min_eval = min(min_eval, eval)  # !সর্বনিম্ন মূল্য আপডেট করা হয়েছে।
            beta = min(beta, eval)  # !বিটা আপডেট করা হয়েছে।
            if beta <= alpha:  # !আলফা-বিটা প্রুনিং।
                break
        return min_eval

# !AI-এর চাল নির্বাচনের ফাংশন সংজ্ঞায়িত করা হয়েছে।
def make_ai_move():
    # !বৈধ চালের লিস্ট তৈরি করা হয়েছে।
    legal_moves = list(board.legal_moves)
    if not legal_moves:  # !কোনো বৈধ চাল না থাকলে None রিটার্ন করা হয়েছে।
        return None

    best_move = None  # !সেরা চালের জন্য ভেরিয়েবল ইনিশিয়ালাইজ করা হয়েছে।
    best_value = float('-inf')  # !সেরা মূল্য ইনিশিয়ালাইজ করা হয়েছে।
    best_capture = False  # !ক্যাপচার চাল কিনা তা ট্র্যাক করা হয়েছে।

    # !প্রতিটি বৈধ চালের জন্য লুপ চালানো হয়েছে।
    for move in legal_moves:
        is_capture = board.is_capture(move)  # !চালটি ক্যাপচার কিনা চেক করা হয়েছে।
        board.push(move)  # !চাল প্রয়োগ করা হয়েছে।
        value = minimax(3, float('-inf'), float('inf'), False)  # !মিনিম্যাক্স দিয়ে মূল্যায়ন করা হয়েছে।
        board.pop()  # !চাল পূর্বাবস্থায় ফিরিয়ে আনা হয়েছে।
        if value > best_value:  # !যদি নতুন মূল্য সেরা মূল্যের চেয়ে বেশি হয়।
            best_value = value  # !সেরা মূল্য আপডেট করা হয়েছে।
            best_move = move  # !সেরা চাল আপডেট করা হয়েছে।
            best_capture = is_capture  # !ক্যাপচার স্ট্যাটাস আপডেট করা হয়েছে।

    # !যদি সেরা চাল পাওয়া যায়।
    if best_move:
        board.push(best_move)  # !সেরা চাল প্রয়োগ করা হয়েছে।
        if best_capture:  # !যদি চালটি ক্যাপচার হয়।
            CAPTURE_SOUND.play()  # !ক্যাপচার সাউন্ড বাজানো হয়েছে।
        else:
            MOVE_SOUND.play()  # !সাধারণ চালের সাউন্ড বাজানো হয়েছে।

# !প্রধান গেম লুপ ফাংশন সংজ্ঞায়িত করা হয়েছে।
async def main():
    global selected_square, valid_moves  # !গ্লোবাল ভেরিয়েবল ঘোষণা করা হয়েছে।
    clock = pygame.time.Clock()  # !গেমের ফ্রেম রেট নিয়ন্ত্রণের জন্য ক্লক তৈরি করা হয়েছে।
    running = True  # !গেম চলমান কিনা তা ট্র্যাক করার জন্য।

    while running:
        # !প্রতিটি ইভেন্টের জন্য লুপ চালানো হয়েছে।
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # !যদি উইন্ডো বন্ধ করা হয়।
                running = False  # !গেম বন্ধ করা হয়েছে।
            # !যদি মাউস ক্লিক করা হয় এবং সাদা প্লেয়ারের পালা হয়।
            elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE:
                pos = pygame.mouse.get_pos()  # !মাউসের অবস্থান পাওয়া হয়েছে।
                col, row = pos[0] // SQUARE_SIZE, 7 - (pos[1] // SQUARE_SIZE)  # !ক্লিক করা স্কোয়ার গণনা করা হয়েছে।
                square = chess.square(col, row)  # !স্কোয়ারের ইনডেক্স পাওয়া হয়েছে।

                # !যদি কোনো স্কোয়ার নির্বাচিত না থাকে।
                if selected_square is None:
                    piece = board.piece_at(square)  # !স্কোয়ারে পিস আছে কিনা চেক করা হয়েছে।
                    if piece and piece.color == chess.WHITE:  # !যদি পিস সাদা হয়।
                        selected_square = square  # !স্কোয়ার নির্বাচিত হয়েছে।
                        valid_moves = [move for move in board.legal_moves if move.from_square == square]  # !বৈধ চালের লিস্ট তৈরি করা হয়েছে।
                else:
                    # !বৈধ চালের মধ্যে ক্লিক করা স্কোয়ার আছে কিনা চেক করা হয়েছে।
                    for move in valid_moves:
                        if move.to_square == square:
                            is_capture = board.is_capture(move)  # !চালটি ক্যাপচার কিনা চেক করা হয়েছে।
                            board.push(move)  # !চাল প্রয়োগ করা হয়েছে।
                            if is_capture:  # !যদি ক্যাপচার হয়।
                                CAPTURE_SOUND.play()  # !ক্যাপচার সাউন্ড বাজানো হয়েছে।
                            else:
                                MOVE_SOUND.play()  # !সাধারণ চালের সাউন্ড বাজানো হয়েছে।
                            selected_square = None  # !নির্বাচিত স্কোয়ার রিসেট করা হয়েছে।
                            valid_moves = []  # !বৈধ চালের লিস্ট রিসেট করা হয়েছে।
                            make_ai_move()  # !AI-এর চাল প্রয়োগ করা হয়েছে।
                            break
                    else:
                        selected_square = None  # !কোনো বৈধ চাল না হলে নির্বাচন রিসেট।
                        valid_moves = []  # !বৈধ চালের লিস্ট রিসেট।

        draw_board()  # !দাবার বোর্ড আঁকা হয়েছে।
        draw_highlights()  # !নির্বাচিত স্কোয়ার এবং বৈধ চাল হাইলাইট করা হয়েছে।
        draw_pieces()  # !দাবার পিস আঁকা হয়েছে।
        pygame.display.flip()  # !স্ক্রিন আপডেট করা হয়েছে।
        clock.tick(FPS)  # !ফ্রেম রেট নিয়ন্ত্রণ করা হয়েছে।
        await asyncio.sleep(1.0 / FPS)  # !অ্যাসিঙ্ক্রোনাস বিলম্ব যোগ করা হয়েছে।

    pygame.quit()  # !গেম বন্ধ করার সময় pygame বন্ধ করা হয়েছে।

# !গেম চালানোর জন্য শর্ত চেক করা হয়েছে।
if platform.system() == "Emscripten":  # !যদি প্ল্যাটফর্ম Emscripten হয় (ব্রাউজারে চলার জন্য)।
    asyncio.ensure_future(main())  # !অ্যাসিঙ্ক্রোনাসভাবে মেইন ফাংশন চালানো হয়েছে।
else:
    if __name__ == "__main__":  # !যদি স্ক্রিপ্ট সরাসরি চালানো হয়।
        asyncio.run(main())  # !মেইন ফাংশন অ্যাসিঙ্ক্রোনাসভাবে চালানো হয়েছে।