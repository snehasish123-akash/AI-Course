# প্রোগ্রামে প্রয়োজনীয় লাইব্রেরি আমদানি করা হচ্ছে
import numpy as np  # নিউমেরিক গণনা এবং অ্যারে পরিচালনার জন্য
import pygame  # গ্রাফিকাল ইউজার ইন্টারফেস এবং গেম ডেভেলপমেন্টের জন্য
import sys  # সিস্টেম ফাংশন যেমন প্রোগ্রাম বন্ধ করার জন্য
import math  # গাণিতিক ফাংশন যেমন ইনফিনিটি ব্যবহারের জন্য
import random  # এলোমেলো সংখ্যা বা পছন্দ তৈরির জন্য

# ধ্রুবক মান সংজ্ঞায়িত ফাইল থেকে আমদানি করা হচ্ছে
from constants import *  # গেমের ধ্রুবক মান যেমন ROW_COUNT, COLUMN_COUNT ইত্যাদি

# ----- গেম লজিক ফাংশন -----
# গেম বোর্ড তৈরির ফাংশন
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))  # ROW_COUNT x COLUMN_COUNT সাইজের শূন্য ম্যাট্রিক্স তৈরি করে বোর্ড হিসেবে

# বোর্ডে প্লেয়ার বা AI-এর পিস রাখার ফাংশন
def drop_piece(board, row, col, piece):
    board[row][col] = piece  # নির্দিষ্ট সারি এবং কলামে পিস (1 বা 2) রাখে

# কলামে পিস রাখা যায় কিনা তা পরীক্ষা করার ফাংশন
def is_valid_location(board, col):
    return board[0][col] == 0  # কলামের উপরের সারি খালি থাকলে True ফেরায়

# কলামে পরবর্তী খালি সারি খুঁজে বের করার ফাংশন
def get_next_open_row(board, col):
    for r in range(ROW_COUNT-1, -1, -1):  # নিচ থেকে উপরের দিকে সারি চেক করে
        if board[r][col] == 0:  # খালি সারি পেলে তার ইনডেক্স ফেরায়
            return r

# বোর্ডে বৈধ কলামগুলোর তালিকা ফেরানোর ফাংশন
def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]  # বৈধ কলামগুলোর তালিকা তৈরি করে

# বোর্ড কনসোলে প্রিন্ট করার ফাংশন
def print_board(board):
    print(np.flip(board, 0))  # বোর্ড উল্টিয়ে প্রিন্ট করে (নিচ থেকে উপরে)

# জয়ের অবস্থান সংরক্ষণের জন্য গ্লোবাল ভেরিয়েবল
winning_positions = []  # জয়ী পিসগুলোর অবস্থান সংরক্ষণ করতে

# জয়ের শর্ত পরীক্ষা করার ফাংশন
def winning_move(board, piece):
    global winning_positions  # গ্লোবাল ভেরিয়েবল ব্যবহারের জন্য
    winning_positions = []  # প্রতিবার নতুন করে জয়ী অবস্থান শূন্য করে

    # অনুভূমিকভাবে ৪টি পিস পরীক্ষা
    for c in range(COLUMN_COUNT - 3):  # ৪টি পিস ধরার জন্য কলাম সীমিত
        for r in range(ROW_COUNT):  # প্রতিটি সারি চেক
            if all(board[r][c+i] == piece for i in range(4)):  # ৪টি পিস একই হলে
                winning_positions = [(r, c+i) for i in range(4)]  # জয়ী অবস্থান সংরক্ষণ
                return True  # জয় হয়েছে

    # উল্লম্বভাবে ৪টি পিস পরীক্ষা
    for c in range(COLUMN_COUNT):  # প্রতিটি কলাম চেক
        for r in range(ROW_COUNT - 3):  # ৪টি পিস ধরার জন্য সারি সীমিত
            if all(board[r+i][c] == piece for i in range(4)):  # ৪টি পিস একই হলে
                winning_positions = [(r+i, c) for i in range(4)]  # জয়ী অবস্থান সংরক্ষণ
                return True  # জয় হয়েছে

    # ডানদিকে তির্যকভাবে ৪টি পিস পরীক্ষা
    for c in range(COLUMN_COUNT - 3):  # তির্যক জয়ের জন্য কলাম সীমিত
        for r in range(ROW_COUNT - 3):  # তির্যক জয়ের জন্য সারি সীমিত
            if all(board[r+i][c+i] == piece for i in range(4)):  # ৪টি পিস একই হলে
                winning_positions = [(r+i, c+i) for i in range(4)]  # জয়ী অবস্থান সংরক্ষণ
                return True  # জয় হয়েছে

    # বামদিকে তির্যকভাবে ৪টি পিস পরীক্ষা
    for c in range(COLUMN_COUNT - 3):  # তির্যক জয়ের জন্য কলাম সীমিত
        for r in range(3, ROW_COUNT):  # তির্যক জয়ের জন্য সারি সীমিত
            if all(board[r-i][c+i] == piece for i in range(4)):  # ৪টি পিস একই হলে
                winning_positions = [(r-i, c+i) for i in range(4)]  # জয়ী অবস্থান সংরক্ষণ
                return True  # জয় হয়েছে

    return False  # কোনো জয় না হলে False ফেরায়

# উইন্ডোর স্কোর নির্ধারণের ফাংশন
def evaluate_window(window, piece):
    score = 0  # স্কোর শুরুতে শূন্য
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE  # বিপক্ষ প্লেয়ার নির্ধারণ

    if window.count(piece) == 4:  # ৪টি পিস নিজের হলে উচ্চ স্কোর
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:  # ৩টি পিস নিজের এবং ১টি খালি
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:  # ২টি পিস নিজের এবং ২টি খালি
        score += 2
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:  # বিপক্ষের ৩টি পিস এবং ১টি খালি
        score -= 4

    return score  # স্কোর ফেরায়

# বোর্ডের অবস্থার স্কোর নির্ধারণের ফাংশন
def score_position(board, piece):
    score = 0  # স্কোর শুরুতে শূন্য

    # কেন্দ্রীয় কলামে পিস থাকলে অতিরিক্ত স্কোর
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]  # কেন্দ্রীয় কলামের ডেটা
    score += center_array.count(piece) * 3  # প্রতিটি পিসের জন্য ৩ স্কোর

    # অনুভূমিকভাবে উইন্ডো স্কোর
    for r in range(ROW_COUNT):  # প্রতিটি সারি চেক
        row_array = [int(i) for i in list(board[r,:])]  # সারির ডেটা
        for c in range(COLUMN_COUNT-3):  # ৪টি পিসের উইন্ডো
            window = row_array[c:c+WINDOW_LENGTH]  # উইন্ডো তৈরি
            score += evaluate_window(window, piece)  # উইন্ডোর স্কোর যোগ

    # উল্লম্বভাবে উইন্ডো স্কোর
    for c in range(COLUMN_COUNT):  # প্রতিটি কলাম চেক
        col_array = [int(i) for i in list(board[:,c])]  # কলামের ডেটা
        for r in range(ROW_COUNT-3):  # ৪টি পিসের উইন্ডো
            window = col_array[r:r+WINDOW_LENGTH]  # উইন্ডো তৈরি
            score += evaluate_window(window, piece)  # উইন্ডোর স্কোর যোগ

    # তির্যকভাবে উইন্ডো স্কোর
    for r in range(ROW_COUNT-3):  # তির্যক উইন্ডোর জন্য সারি সীমিত
        for c in range(COLUMN_COUNT-3):  # তির্যক উইন্ডোর জন্য কলাম সীমিত
            score += evaluate_window([board[r+i][c+i] for i in range(WINDOW_LENGTH)], piece)  # ডান তির্যক
            score += evaluate_window([board[r+3-i][c+i] for i in range(WINDOW_LENGTH)], piece)  # বাম তির্যক

    return score  # মোট স্কোর ফেরায়

# বোর্ডের অবস্থা শেষ হয়েছে কিনা তা পরীক্ষা
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or not get_valid_locations(board)  # জয় বা ড্র হলে True

# মিনিম্যাক্স অ্যালগরিদম ফাংশন
def minimax(board, depth, alpha, beta, maximizing):
    valid_locations = get_valid_locations(board)  # বৈধ কলামগুলো নির্ধারণ
    is_terminal = is_terminal_node(board)  # শেষ অবস্থা কিনা চেক

    if depth == 0 or is_terminal:  # গভীরতা শূন্য বা শেষ হলে
        if is_terminal:  # শেষ অবস্থা হলে
            if winning_move(board, AI_PIECE): return (None, 1e14)  # AI জিতলে উচ্চ স্কোর
            elif winning_move(board, PLAYER_PIECE): return (None, -1e13)  # প্লেয়ার জিতলে নিম্ন স্কোর
            else: return (None, 0)  # ড্র হলে শূন্য স্কোর
        return (None, score_position(board, AI_PIECE))  # বোর্ডের স্কোর ফেরায়

    best_col = random.choice(valid_locations)  # ডিফল্ট হিসেবে এলোমেলো কলাম

    if maximizing:  # AI-এর পালা (সর্বোচ্চ স্কোর চায়)
        value = -math.inf  # সর্বনিম্ন মান দিয়ে শুরু
        for col in valid_locations:  # প্রতিটি বৈধ কলাম চেক
            row = get_next_open_row(board, col)  # পরবর্তী খালি সারি
            temp_board = board.copy()  # বোর্ডের কপি
            drop_piece(temp_board, row, col, AI_PIECE)  # AI-এর পিস রাখা
            _, new_score = minimax(temp_board, depth-1, alpha, beta, False)  # রিকার্সিভ কল
            if new_score > value:  # ভালো স্কোর পেলে আপডেট
                value, best_col = new_score, col
            alpha = max(alpha, value)  # আলফা আপডেট
            if alpha >= beta: break  # আলফা-বিটা প্রুনিং
        return best_col, value  # সেরা কলাম এবং স্কোর ফেরায়

    else:  # প্লেয়ারের পালা (সর্বনিম্ন স্কোর চায়)
        value = math.inf  # সর্বোচ্চ মান দিয়ে শুরু
        for col in valid_locations:  # প্রতিটি বৈধ কলাম চেক
            row = get_next_open_row(board, col)  # পরবর্তী খালি সারি
            temp_board = board.copy()  # বোর্ডের কপি
            drop_piece(temp_board, row, col, PLAYER_PIECE)  # প্লেয়ারের পিস রাখা
            _, new_score = minimax(temp_board, depth-1, alpha, beta, True)  # রিকার্সিভ কল
            if new_score < value:  # কম স্কোর পেলে আপডেট
                value, best_col = new_score, col
            beta = min(beta, value)  # বিটা আপডেট
            if alpha >= beta: break  # আলফা-বিটা প্রুনিং
        return best_col, value  # সেরা কলাম এবং স্কোর ফেরায়

# ----- গ্রাফিক্স অঙ্কন -----
# বোর্ড গ্রাফিকালি আঁকার ফাংশন
def draw_board(board):
    for c in range(COLUMN_COUNT):  # প্রতিটি কলাম চেক
        for r in range(ROW_COUNT):  # প্রতিটি সারি চেক
            pygame.draw.rect(screen, GRID_COLOR, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))  # গ্রিডের বর্গ আঁকে
            color = EMPTY_COLOR  # ডিফল্ট রং খালি
            if board[r][c] == PLAYER_PIECE:  # প্লেয়ারের পিস হলে
                color = PLAYER_COLOR  # প্লেয়ারের রং
            elif board[r][c] == AI_PIECE:  # AI-এর পিস হলে
                color = AI_COLOR  # AI-এর রং
            pygame.draw.circle(screen, color, (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)  # বৃত্ত আঁকে

    for r, c in winning_positions:  # জয়ী পিসগুলোর জন্য
        pygame.draw.circle(screen, (0,255,0), (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS, 5)  # সবুজ বর্ডার আঁকে

    pygame.display.update()  # স্ক্রিন আপডেট করে

# ----- গেম সেটআপ -----
# Pygame ইনিশিয়ালাইজ করা
pygame.init()  # Pygame শুরু করে

# গেম বোর্ডের মাত্রা নির্ধারণ
SQUARESIZE = 100  # প্রতিটি বর্গের সাইজ
width, height = COLUMN_COUNT * SQUARESIZE, (ROW_COUNT+1) * SQUARESIZE  # স্ক্রিনের প্রস্থ এবং উচ্চতা
size = (width, height)  # স্ক্রিনের সাইজ টাপল
RADIUS = SQUARESIZE//2 - 5  # বৃত্তের রেডিয়াস

# Pygame স্ক্রিন তৈরি
screen = pygame.display.set_mode(size)  # নির্দিষ্ট সাইজের স্ক্রিন তৈরি
myfont = pygame.font.SysFont("monospace", 75) or pygame.font.Font(None, 75)  # টেক্সট রেন্ডারিংয়ের জন্য ফন্ট
screen.fill(BACKGROUND_COLOR)  # স্ক্রিন ব্যাকগ্রাউন্ড রং দিয়ে ভরাট

# গেম বোর্ড তৈরি এবং অঙ্কন
board = create_board()  # নতুন বোর্ড তৈরি
draw_board(board)  # বোর্ড গ্রাফিকালি আঁকে
pygame.display.update()  # স্ক্রিন আপডেট করে

# গেমের অবস্থা এবং পালা নির্ধারণ
game_over = False  # গেম শেষ হয়নি
turn = random.randint(PLAYER, AI)  # এলোমেলোভাবে প্লেয়ার বা AI-এর পালা নির্ধারণ

# ----- প্রধান গেম লুপ -----
while not game_over:  # গেম শেষ না হওয়া পর্যন্ত চলবে
    for event in pygame.event.get():  # Pygame-এর ইভেন্টগুলো চেক
        if event.type == pygame.QUIT:  # বন্ধ বোতাম ক্লিক হলে
            sys.exit()  # প্রোগ্রাম বন্ধ

        # মাউসের গতিবিধি চেক
        if event.type == pygame.MOUSEMOTION:  # মাউস সরানো হলে
            pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARESIZE))  # উপরের এলাকা পরিষ্কার
            pygame.draw.circle(screen, PLAYER_COLOR, (event.pos[0], SQUARESIZE//2), RADIUS)  # প্লেয়ারের পিস দেখায়
            pygame.display.update()  # স্ক্রিন আপডেট

        # প্লেয়ারের পালায় মাউস ক্লিক
        if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER:  # প্লেয়ার ক্লিক করলে
            pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARESIZE))  # উপরের এলাকা পরিষ্কার
            col = event.pos[0] // SQUARESIZE  # ক্লিক করা কলাম নির্ধারণ

            if is_valid_location(board, col):  # কলাম বৈধ হলে
                row = get_next_open_row(board, col)  # পরবর্তী খালি সারি
                drop_piece(board, row, col, PLAYER_PIECE)  # প্লেয়ারের পিস রাখা

                if winning_move(board, PLAYER_PIECE):  # প্লেয়ার জিতলে
                    label = myfont.render("Player wins!", 1, PLAYER_COLOR)  # জয়ের বার্তা
                    screen.blit(label, (40, 10))  # বার্তা স্ক্রিনে দেখানো
                    game_over = True  # গেম শেষ

                turn = AI  # AI-এর পালা
                draw_board(board)  # বোর্ড আপডেট

    # AI-এর পালা
    if turn == AI and not game_over:  # AI-এর পালা এবং গেম শেষ না হলে
        col, _ = minimax(board, 5, -math.inf, math.inf, True)  # মিনিম্যাক্স দিয়ে সেরা কলাম নির্বাচন
        if col is not None and is_valid_location(board, col):  # বৈধ কলাম হলে
            pygame.time.wait(500)  # ০.৫ সেকেন্ড অপেক্ষা
            row = get_next_open_row(board, col)  # পরবর্তী খালি সারি
            drop_piece(board, row, col, AI_PIECE)  # AI-এর পিস রাখা

            if winning_move(board, AI_PIECE):  # AI জিতলে
                label = myfont.render("AI wins!", 1, AI_COLOR)  # জয়ের বার্তা
                screen.blit(label, (40, 10))  # বার্তা স্ক্রিনে দেখানো
                game_over = True  # গেম শেষ

            draw_board(board)  # বোর্ড আপডেট
            turn = PLAYER  # প্লেয়ারের পালা

    if game_over:  # গেম শেষ হলে
        pygame.time.wait(5000)  # ৫ সেকেন্ড অপেক্ষা করে প্রোগ্রাম বন্ধ