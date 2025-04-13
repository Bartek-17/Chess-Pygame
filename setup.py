"""
File containing initialization of all variables in the game
"""
import pygame

pygame.init()

# set up constants and images

WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Chess')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
bigger_font = pygame.font.Font('freesansbold.ttf', 60)
gigantic_font = pygame.font.Font('freesansbold.ttf', 80)
timer = pygame.time.Clock()
fps = 60
# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop',
                'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
                   (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
                   (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop',
                'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
                   (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6),
                   (7, 6)]
captured_pieces_white = []
captured_pieces_black = []

# 0-whites turn no selection, 1-whites turn piece selected,
# 2-black turn no selection, 3-black turn piece selected
turn_step = 0
selection = 999  # no piece is selected at the start
valid_moves = []

# other images
flag = pygame.image.load('images/A_Forfeit.png')
flag_white = pygame.transform.scale(flag, (75, 75))
flag2 = pygame.image.load('images/B_Forfeit.png')
flag_black = pygame.transform.scale(flag2, (70, 70))

chess_pieces = pygame.image.load('images/Intro.png')
PiecesPNG = pygame.transform.scale(chess_pieces, (1000, 900))

background = pygame.image.load('images/Intro2.png')
backgroundPNG = pygame.transform.scale(background, (1000, 900))

# loading piece images for black and white:
# original image is 150x150 pixels, so I keep the proportions
black_queen = pygame.image.load('images/black-queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))

black_king = pygame.image.load('images/black-king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))

black_rook = pygame.image.load('images/black-rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))

black_bishop = pygame.image.load('images/black-bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))

black_knight = pygame.image.load('images/black-knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))

black_pawn = pygame.image.load('images/black-pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (80, 80))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))

white_queen = pygame.image.load('images/white-queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))

white_king = pygame.image.load('images/white-king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))

white_rook = pygame.image.load('images/white-rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))

white_bishop = pygame.image.load('images/white-bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))

white_knight = pygame.image.load('images/white-knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))

white_pawn = pygame.image.load('images/white-pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (80, 80))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

white_images = [white_pawn, white_queen, white_king,
                white_knight, white_rook, white_bishop]
white_promotions = ['bishop', 'knight', 'rook', 'queen']
small_white_images = [white_pawn_small, white_queen_small, white_king_small,
                      white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king,
                black_knight, black_rook, black_bishop]
black_promotions = ['bishop', 'knight', 'rook', 'queen']
small_black_images = [black_pawn_small, black_queen_small, black_king_small,
                      black_knight_small,
                      black_rook_small, black_bishop_small]

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

Is_changed = 0  # variable indicating if board is flipped

# ending the game variables initialization
winner = ''
game_over = False

white_promote = False
black_promote = False
promo_index = 999

# checking if moved (checking if castling is possible)
white_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
black_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]

check = False
castling_moves = []
