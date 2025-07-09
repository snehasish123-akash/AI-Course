# লাইব্রেরি ইমপোর্ট করা হচ্ছে যা গভীর কপি তৈরির জন্য ব্যবহৃত হয়, মিনিম্যাক্স অ্যালগরিদমে বোর্ডের অবস্থা কপি করতে।
import copy

# সিস্টেম ফাংশন ইমপোর্ট করা হচ্ছে, যেমন প্রোগ্রাম বন্ধ করার জন্য sys.exit() ব্যবহার করা হবে।
import sys

# পাইগেম লাইব্রেরি ইমপোর্ট করা হচ্ছে, যা গ্রাফিকাল ইন্টারফেস এবং ইভেন্ট হ্যান্ডলিংয়ের জন্য ব্যবহৃত হয়।
import pygame

# র‍্যান্ডম মডিউল ইমপোর্ট করা হচ্ছে, যদিও এই কোডে এটি ব্যবহৃত হয়নি, সম্ভবত ভবিষ্যতের জন্য রাখা হয়েছে।
import random

# নামপাই লাইব্রেরি ইমপোর্ট করা হচ্ছে, বোর্ডের অ্যারে পরিচালনার জন্য ব্যবহৃত হয়।
import numpy as np

# কনস্ট্যান্ট ফাইল থেকে সংজ্ঞায়িত ধ্রুবক মান (যেমন WIDTH, HEIGHT, SQSIZE) ইমপোর্ট করা হচ্ছে।
from constants import *

# পাইগেম ইনিশিয়ালাইজ করা হচ্ছে, যা পাইগেমের সমস্ত মডিউল সক্রিয় করে।
pygame.init()

# গেমের উইন্ডো তৈরি করা হচ্ছে, WIDTH এবং HEIGHT দ্বারা নির্ধারিত আকারে।
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# গেম উইন্ডোর শিরোনাম সেট করা হচ্ছে 'TIC TAC TOE AI'।
pygame.display.set_caption('TIC TAC TOE AI')

# পুরো স্ক্রিনটি পটভূমির রঙ (BG_COLOR) দিয়ে পূর্ণ করা হচ্ছে।
screen.fill(BG_COLOR)

# বোর্ড ক্লাস সংজ্ঞায়িত করা হচ্ছে, যা গেম বোর্ডের অবস্থা এবং লজিক পরিচালনা করে।
class Board:
    # বোর্ড ক্লাসের ইনিশিয়ালাইজার ফাংশন, বোর্ড তৈরি এবং শুরু করার জন্য।
    def __init__(self):
        # 3x3 নামপাই অ্যারে তৈরি করা হচ্ছে, যেখানে সব স্কোয়ার শূন্য দিয়ে শুরু হয় (কোনো চিহ্ন নেই)।
        self.squares = np.zeros((ROWS, COLS))
        # চিহ্নিত স্কোয়ারের সংখ্যা ট্র্যাক করার জন্য ভেরিয়েবল, শুরুতে 0।
        self.marked_sqrs = 0

    # গেমের চূড়ান্ত অবস্থা পরীক্ষা করার জন্য ফাংশন, বিজয়ী কে বা ড্র কিনা তা নির্ধারণ করে।
    def final_state(self, show=False):
        # প্রতিটি কলাম চেক করা হচ্ছে যদি তিনটি একই চিহ্ন থাকে এবং শূন্য না হয়।
        for col in range(COLS):
            # যদি একই কলামের তিনটি স্কোয়ার একই চিহ্ন (1 বা 2) থাকে এবং 0 না হয়।
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                # যদি show=True হয়, তবে বিজয়ী লাইন আঁকা হবে।
                if show:
                    # চিহ্ন অনুযায়ী রঙ নির্বাচন করা হচ্ছে (2 হলে CIRC_COLOR, অন্যথায় CROSS_COLOR)।
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    # কলামে উল্লম্ব লাইন আঁকা হচ্ছে বিজয়ী চিহ্ন দেখানোর জন্য।
                    pygame.draw.line(screen, color, (col * SQSIZE + SQSIZE // 2, 20),
                                     (col * SQSIZE + SQSIZE // 2, HEIGHT - 20), LINE_WIDTH)
                # বিজয়ী প্লেয়ারের চিহ্ন (1 বা 2) রিটার্ন করা হচ্ছে।
                return self.squares[0][col]

        # প্রতিটি সারি চেক করা হচ্ছে যদি তিনটি একই চিহ্ন থাকে এবং শূন্য না হয়।
        for row in range(ROWS):
            # যদি একই সারির তিনটি স্কোয়ার একই চিহ্ন (1 বা 2) থাকে এবং 0 না হয়।
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                # যদি show=True হয়, তবে বিজয়ী লাইন আঁকা হবে।
                if show:
                    # চিহ্ন অনুযায়ী রঙ নির্বাচন করা হচ্ছে (2 হলে CIRC_COLOR, অন্যথায় CROSS_COLOR)।
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    # সারিতে অনুভূমিক লাইন আঁকা হচ্ছে বিজয়ী চিহ্ন দেখানোর জন্য।
                    pygame.draw.line(screen, color, (20, row * SQSIZE + SQSIZE // 2),
                                     (WIDTH - 20, row * SQSIZE + SQSIZE // 2), LINE_WIDTH)
                # বিজয়ী প্লেয়ারের চিহ্ন (1 বা 2) রিটার্ন করা হচ্ছে।
                return self.squares[row][0]

        # প্রধান ডায়াগোনাল (উপরের বাম থেকে নিচের ডান) চেক করা হচ্ছে।
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            # যদি show=True হয়, তবে বিজয়ী লাইন আঁকা হবে।
            if show:
                # চিহ্ন অনুযায়ী রঙ নির্বাচন করা হচ্ছে (2 হলে CIRC_COLOR, অন্যথায় CROSS_COLOR)।
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                # ডায়াগোনাল লাইন আঁকা হচ্ছে বিজয়ী চিহ্ন দেখানোর জন্য।
                pygame.draw.line(screen, color, (20, 20), (WIDTH - 20, HEIGHT - 20), CROSS_WIDTH)
            # বিজয়ী প্লেয়ারের চিহ্ন (1 বা 2) রিটার্ন করা হচ্ছে।
            return self.squares[1][1]

        # বিপরীত ডায়াগোনাল (নিচের বাম থেকে উপরের ডান) চেক করা হচ্ছে।
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            # যদি show=True হয়, তবে বিজয়ী লাইন আঁকা হবে।
            if show:
                # চিহ্ন অনুযায়ী রঙ নির্বাচন করা হচ্ছে (2 হলে CIRC_COLOR, অন্যথায় CROSS_COLOR)।
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                # ডায়াগোনাল লাইন আঁকা হচ্ছে বিজয়ী চিহ্ন দেখানোর জন্য।
                pygame.draw.line(screen, color, (20, HEIGHT - 20), (WIDTH - 20, 20), CROSS_WIDTH)
            # বিজয়ী প্লেয়ারের চিহ্ন (1 বা 2) রিটার্ন করা হচ্ছে।
            return self.squares[1][1]

        # যদি কোনো বিজয়ী না থাকে, তবে 0 রিটার্ন করা হচ্ছে (গেম চলমান বা ড্র)।
        return 0

    # বোর্ডে নির্দিষ্ট স্কোয়ারে প্লেয়ারের চিহ্ন স্থাপন করার জন্য ফাংশন।
    def mark_sqr(self, row, col, player):
        # নির্দিষ্ট সারি এবং কলামে প্লেয়ারের চিহ্ন (1 বা 2) সেট করা হচ্ছে।
        self.squares[row][col] = player
        # চিহ্নিত স্কোয়ারের সংখ্যা এক বাড়ানো হচ্ছে।
        self.marked_sqrs += 1

    # নির্দিষ্ট স্কোয়ার খালি কিনা তা চেক করার জন্য ফাংশন।
    def empty_sqr(self, row, col):
        # স্কোয়ারের মান 0 হলে True রিটার্ন করা হচ্ছে (খালি), অন্যথায় False।
        return self.squares[row][col] == 0

    # বোর্ডে খালি স্কোয়ারগুলোর তালিকা পাওয়ার জন্য ফাংশন।
    def get_empty_sqrs(self):
        # সব খালি স্কোয়ারের সারি এবং কলামের তালিকা তৈরি করা হচ্ছে।
        return [(r, c) for r in range(ROWS) for c in range(COLS) if self.empty_sqr(r, c)]

    # বোর্ড পূর্ণ কিনা তা চেক করার জন্য ফাংশন।
    def isfull(self):
        # যদি 9টি স্কোয়ার চিহ্নিত হয়ে থাকে, তবে True রিটার্ন করা হচ্ছে।
        return self.marked_sqrs == 9

    # বোর্ড খালি কিনা তা চেক করার জন্য ফাংশন।
    def isempty(self):
        # যদি কোনো স্কোয়ার চিহ্নিত না হয়, তবে True রিটার্ন করা হচ্ছে।
        return self.marked_sqrs == 0

# AI ক্লাস সংজ্ঞায়িত করা হচ্ছে, যা AI প্লেয়ারের আচরণ এবং মিনিম্যাক্স অ্যালগরিদম পরিচালনা করে।
class AI:
    # AI ক্লাসের ইনিশিয়ালাইজার ফাংশন, AI প্লেয়ার সেট করার জন্য।
    def __init__(self, player=2):
        # AI এর প্লেয়ার চিহ্ন সেট করা হচ্ছে (ডিফল্ট হল 2, অর্থাৎ O)।
        self.player = player

    # মিনিম্যাক্স অ্যালগরিদম বাস্তবায়নের জন্য ফাংশন, যা AI এর সেরা পদক্ষেপ নির্ধারণ করে।
    def minimax(self, board, maximizing):
        # বোর্ডের চূড়ান্ত অবস্থা চেক করা হচ্ছে।
        case = board.final_state()
        # যদি প্লেয়ার 1 জিতে, তবে 1 রিটার্ন করা হচ্ছে (AI এর জন্য খারাপ)।
        if case == 1: return 1, None
        # যদি AI (প্লেয়ার 2) জিতে, তবে -1 রিটার্ন করা হচ্ছে (AI এর জন্য ভালো)।
        if case == 2: return -1, None
        # যদি বোর্ড পূর্ণ হয় (ড্র), তবে 0 রিটার্ন করা হচ্ছে।
        if board.isfull(): return 0, None

        # সেরা পদক্ষেপ ট্র্যাক করার জন্য ভেরিয়েবল।
        best_move = None
        # যদি ম্যাক্সিমাইজিং হয় (প্লেয়ার 1 এর পালা), তবে সর্বোচ্চ স্কোর খুঁজতে হবে।
        if maximizing:
            # সর্বনিম্ন সম্ভাব্য স্কোর দিয়ে শুরু করা হচ্ছে।
            max_eval = -100
            # প্রতিটি খালি স্কোয়ারের জন্য লুপ চালানো হচ্ছে।
            for (r, c) in board.get_empty_sqrs():
                # বোর্ডের একটি গভীর কপি তৈরি করা হচ্ছে পরীক্ষার জন্য।
                temp = copy.deepcopy(board)
                # অস্থায়ী বোর্ডে প্লেয়ার 1 এর চিহ্ন স্থাপন করা হচ্ছে।
                temp.mark_sqr(r, c, 1)
                # মিনিম্যাক্স ফাংশন পুনরাবৃত্তি করে মূল্যায়ন করা হচ্ছে।
                eval = self.minimax(temp, False)[0]
                # যদি এই মূল্যায়ন সর্বোচ্চ হয়, তবে এটি সংরক্ষণ করা হচ্ছে।
                if eval > max_eval:
                    # সর্বোচ্চ মূল্যায়ন এবং সংশ্লিষ্ট পদক্ষেপ আপডেট করা হচ্ছে।
                    max_eval, best_move = eval, (r, c)
            # সর্বোচ্চ মূল্যায়ন এবং সেরা পদক্ষেপ রিটার্ন করা হচ্ছে।
            return max_eval, best_move
        # যদি মিনিমাইজিং হয় (AI এর পালা), তবে সর্বনিম্ন স্কোর খুঁজতে হবে।
        else:
            # সর্বোচ্চ সম্ভাব্য স্কোর দিয়ে শুরু করা হচ্ছে।
            min_eval = 100
            # প্রতিটি খালি স্কোয়ারের জন্য লুপ চালানো হচ্ছে।
            for (r, c) in board.get_empty_sqrs():
                # বোর্ডের একটি গভীর কপি তৈরি করা হচ্ছে পরীক্ষার জন্য।
                temp = copy.deepcopy(board)
                # অস্থায়ী বোর্ডে AI এর চিহ্ন (প্লেয়ার 2) স্থাপন করা হচ্ছে।
                temp.mark_sqr(r, c, self.player)
                # মিনিম্যাক্স ফাংশন পুনরাবৃত্তি করে মূল্যায়ন করা হচ্ছে।
                eval = self.minimax(temp, True)[0]
                # যদি এই মূল্যায়ন সর্বনিম্ন হয়, তবে এটি সংরক্ষণ করা হচ্ছে।
                if eval < min_eval:
                    # সর্বনিম্ন মূল্যায়ন এবং সংশ্লিষ্ট পদক্ষেপ আপডেট করা হচ্ছে।
                    min_eval, best_move = eval, (r, c)
            # সর্বনিম্ন মূল্যায়ন এবং সেরা পদক্ষেপ রিটার্ন করা হচ্ছে।
            return min_eval, best_move

    # AI এর পদক্ষেপ মূল্যায়ন করার জন্য ফাংশন।
    def eval(self, main_board):
        # মিনিম্যাক্স অ্যালগরিদম ব্যবহার করে সেরা পদক্ষেপ এবং এর মূল্যায়ন পাওয়া হচ্ছে।
        eval, move = self.minimax(main_board, False)
        # AI এর নির্বাচিত পদক্ষেপ এবং এর মূল্যায়ন প্রিন্ট করা হচ্ছে।
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        # সেরা পদক্ষেপ রিটার্ন করা হচ্ছে।
        return move

# গেম ক্লাস সংজ্ঞায়িত করা হচ্ছে, যা গেমের সামগ্রিক লজিক এবং ইন্টারফেস পরিচালনা করে।
class Game:
    # গেম ক্লাসের ইনিশিয়ালাইজার ফাংশন, গেমের প্রাথমিক অবস্থা সেট করার জন্য।
    def __init__(self):
        # নতুন বোর্ড অবজেক্ট তৈরি করা হচ্ছে।
        self.board = Board()
        # নতুন AI অবজেক্ট তৈরি করা হচ্ছে (ডিফল্ট প্লেয়ার 2)।
        self.ai = AI()
        # বর্তমান প্লেয়ার সেট করা হচ্ছে (1 দিয়ে শুরু, অর্থাৎ X)।
        self.player = 1
        # গেম চলমান কিনা তা ট্র্যাক করার জন্য ভেরিয়েবল, শুরুতে True।
        self.running = True
        # গেম বোর্ডের গ্রিড লাইন আঁকার জন্য ফাংশন কল করা হচ্ছে।
        self.show_lines()

    # গেম বোর্ডের গ্রিড লাইন আঁকার জন্য ফাংশন।
    def show_lines(self):
        # স্ক্রিনটি পটভূমির রঙ দিয়ে পূর্ণ করা হচ্ছে।
        screen.fill(BG_COLOR)
        # প্রথম উল্লম্ব লাইন আঁকা হচ্ছে বোর্ডের গ্রিড তৈরির জন্য।
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        # দ্বিতীয় উল্লম্ব লাইন আঁকা হচ্ছে বোর্ডের গ্রিড তৈরির জন্য।
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        # প্রথম অনুভূমিক লাইন আঁকা হচ্ছে বোর্ডের গ্রিড তৈরির জন্য।
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        # দ্বিতীয় অনুভূমিক লাইন আঁকা হচ্ছে বোর্ডের গ্রিড তৈরির জন্য।
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    # নির্দিষ্ট স্কোয়ারে প্লেয়ারের চিহ্ন (X বা O) আঁকার জন্য ফাংশন।
    def draw_fig(self, row, col):
        # যদি বর্তমান প্লেয়ার 1 হয় (X), তবে X আঁকা হবে।
        if self.player == 1:
            # X এর প্রথম তির্যক লাইন আঁকা হচ্ছে।
            pygame.draw.line(screen, CROSS_COLOR,
                             (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET),
                             (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET), CROSS_WIDTH)
            # X এর দ্বিতীয় তির্যক লাইন আঁকা হচ্ছে।
            pygame.draw.line(screen, CROSS_COLOR,
                             (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET),
                             (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET), CROSS_WIDTH)
        # যদি বর্তমান প্লেয়ার 2 হয় (O), তবে O আঁকা হবে।
        else:
            # O আঁকার জন্য বৃত্ত আঁকা হচ্ছে নির্দিষ্ট স্কোয়ারের কেন্দ্রে।
            pygame.draw.circle(screen, CIRC_COLOR,
                               (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2), RADIUS, CIRC_WIDTH)

    # প্লেয়ারের পদক্ষেপ বাস্তবায়ন করার জন্য ফাংশন।
    def make_move(self, row, col):
        # বোর্ডে নির্দিষ্ট স্কোয়ারে প্লেয়ারের চিহ্ন স্থাপন করা হচ্ছে।
        self.board.mark_sqr(row, col, self.player)
        # স্ক্রিনে চিহ্ন (X বা O) আঁকা হচ্ছে।
        self.draw_fig(row, col)
        # প্লেয়ার পরিবর্তন করা হচ্ছে (1 থেকে 2 বা 2 থেকে 1)।
        self.player = self.player % 2 + 1

    # গেম শেষ হয়েছে কিনা তা চেক করার জন্য ফাংশন।
    def isover(self):
        # যদি বিজয়ী থাকে (final_state != 0) বা বোর্ড পূর্ণ হয়, তবে True রিটার্ন করা হচ্ছে।
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    # গেম রিসেট করার জন্য ফাংশন।
    def reset(self):
        # গেম ক্লাসের ইনিশিয়ালাইজার পুনরায় কল করে নতুন গেম শুরু করা হচ্ছে।
        self.__init__()

# প্রধান ফাংশন সংজ্ঞায়িত করা হচ্ছে, যা গেম লুপ চালায়।
def main():
    # নতুন গেম অবজেক্ট তৈরি করা হচ্ছে।
    game = Game()
    # বোর্ড এবং AI অবজেক্ট স্থানীয় ভেরিয়েবলে সংরক্ষণ করা হচ্ছে।
    board, ai = game.board, game.ai

    # গেমের মূল লুপ, যা গেম চলতে থাকে।
    while True:
        # পাইগেমের ইভেন্টগুলো প্রক্রিয়া করার জন্য লুপ।
        for event in pygame.event.get():
            # যদি ব্যবহারকারী উইন্ডো বন্ধ করে, তবে প্রোগ্রাম বন্ধ হবে।
            if event.type == pygame.QUIT:
                # পাইগেম বন্ধ করা হচ্ছে।
                pygame.quit()
                # প্রোগ্রাম থেকে প্রস্থান করা হচ্ছে।
                sys.exit()

            # যদি কীবোর্ড কী চাপা হয়, তবে তা প্রক্রিয়া করা হবে।
            if event.type == pygame.KEYDOWN:
                # যদি 'r' কী চাপা হয়, তবে গেম রিসেট করা হবে।
                if event.key == pygame.K_r:
                    # গেম রিসেট করা হচ্ছে।
                    game.reset()
                    # নতুন বোর্ড এবং AI অবজেক্ট সংরক্ষণ করা হচ্ছে।
                    board, ai = game.board, game.ai

            # যদি মাউস বাটন ক্লিক করা হয় এবং গেম চলমান থাকে।
            if event.type == pygame.MOUSEBUTTONDOWN and game.running:
                # মাউস ক্লিকের অবস্থান থেকে সারি এবং কলাম গণনা করা হচ্ছে।
                row, col = event.pos[1] // SQSIZE, event.pos[0] // SQSIZE
                # যদি নির্বাচিত স্কোয়ার খালি থাকে, তবে পদক্ষেপ করা হবে।
                if board.empty_sqr(row, col):
                    # প্লেয়ারের পদক্ষেপ বাস্তবায়ন করা হচ্ছে।
                    game.make_move(row, col)
                    # গেম শেষ হয়েছে কিনা তা চেক করা হচ্ছে।
                    if game.isover(): game.running = False

        # যদি AI এর পালা হয় এবং গেম চলমান থাকে।
        if game.player == ai.player and game.running:
            # স্ক্রিন আপডেট করা হচ্ছে।
            pygame.display.update()
            # AI এর সেরা পদক্ষেপ গণনা করা হচ্ছে।
            row, col = ai.eval(board)
            # AI এর পদক্ষেপ বাস্তবায়ন করা হচ্ছে।
            game.make_move(row, col)
            # গেম শেষ হয়েছে কিনা তা চেক করা হচ্ছে।
            if game.isover(): game.running = False

        # স্ক্রিন আপডেট করা হচ্ছে যাতে সব পরিবর্তন দৃশ্যমান হয়।
        pygame.display.update()

# প্রধান ফাংশন কল করা হচ্ছে গেম শুরু করার জন্য।
main()