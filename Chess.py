"""
2 player chess game
"""
import sys
from setup import *  # import everything from setup.py


# draw main game board (32 squares, because the rest is the default color)
def draw_board():
    for i in range(32):
        column = i % 4
        # first 4 squares are going to be 0, then row number 1 starts
        row = i // 4
        if row % 2 == 0:  # if row is even; go down 100 per each row
            pygame.draw.rect(screen, (0, 170, 255), [
                600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, (0, 170, 255), [
                700 - (column * 200), row * 100, 100, 100])
        # horizontal block
        pygame.draw.rect(screen, (252, 251, 230), [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'black', [0, 800, WIDTH, 100], 5)
        # vertical block
        pygame.draw.rect(screen, (252, 251, 230), [800, 0, 200, HEIGHT])
        pygame.draw.rect(screen, 'black', [800, 0, 200, HEIGHT], 5)

        status_text1 = ['White: Select a piece!', 'White: Select destination!',
                        'Black: Select a piece!', 'Black: Select destination!']

        status_text2 = ['Black: Select a piece!', 'Black: Select destination!',
                        'White: Select a piece!', 'White: Select destination!']
        if Is_changed == 0:
            screen.blit(big_font.render(
                status_text1[turn_step], True, 'black'), (20, 825))
        else:
            screen.blit(big_font.render(
                status_text2[turn_step], True, 'black'), (20, 825))

        # Forfeit button                      # anti alias
        pygame.draw.rect(screen, 'black', [805, 800, 190, 95])
        pygame.draw.rect(screen, (244, 243, 239), [805, 805, 95, 90])
        pygame.draw.rect(screen, (0, 170, 255), [905, 805, 95, 90])
        screen.blit(flag_black, [808, 820])
        screen.blit(flag_white, [910, 820])
        # black and white promotion
        if white_promote or black_promote:
            pygame.draw.rect(screen, (252, 251, 230), [
                0, 800, WIDTH - 200, 100])
            pygame.draw.rect(screen, 'black', [0, 800, WIDTH - 200, 100], 5)
            screen.blit(big_font.render(
                'Select piece to promote pawn!', True, 'black'), (20, 825))


# draw pieces on the board
def draw_pieces():
    if Is_changed == 0:
        for i in range(len(white_pieces)):
            # index will choose the correct piece image
            index = piece_list.index(white_pieces[i])
            screen.blit(white_images[index], (white_locations[i]
                                              [0] * 100 + 8,
                                              white_locations[i][1] * 100 + 8))
            if turn_step < 2:  # whites turn
                if selection == i:
                    pygame.draw.rect(screen, 'gold',
                                     [white_locations[i][0] * 100,
                                      white_locations[i][1] * 100,
                                      100, 100], 3)
        for i in range(len(black_pieces)):
            # index will choose the correct piece image
            index = piece_list.index(black_pieces[i])
            screen.blit(black_images[index], (black_locations[i]
                                              [0] * 100 + 8,
                                              black_locations[i][1] * 100 + 8))
            if turn_step >= 2:  # blacks turn
                if selection == i:
                    pygame.draw.rect(screen, 'gold',
                                     [black_locations[i][0] * 100,
                                      black_locations[i][1] * 100,
                                      100, 100], 3)
    elif Is_changed == 1:
        for i in range(len(black_pieces)):
            # index will choose the correct piece image
            index = piece_list.index(black_pieces[i])
            screen.blit(white_images[index], (black_locations[i]
                                              [0] * 100 + 8,
                                              black_locations[i][1] * 100 + 8))
            if turn_step >= 2:  # blacks turn
                if selection == i:
                    pygame.draw.rect(screen, 'gold',
                                     [black_locations[i][0] * 100,
                                      black_locations[i][1] * 100,
                                      100, 100], 3)

        for i in range(len(white_pieces)):
            # index will choose the correct piece image
            index = piece_list.index(white_pieces[i])
            screen.blit(black_images[index], (white_locations[i]
                                              [0] * 100 + 8,
                                              white_locations[i][1] * 100 + 8))
            if turn_step <= 1:  # whites turn
                if selection == i:
                    pygame.draw.rect(screen, 'gold',
                                     [white_locations[i][0] * 100,
                                      white_locations[i][1] * 100,
                                      100, 100], 3)


def change_sides():
    global white_locations, black_locations, Is_changed, turn_step
    new_white_locations = []
    new_black_locations = []

    # Is_changed variable change
    if Is_changed == 0:
        Is_changed = 1
        turn_step = 2
    elif Is_changed == 1:
        Is_changed = 0
        turn_step = 0

    for loc in white_locations:
        new_white_locations.append((7 - loc[0], 7 - loc[1]))

    for loc in black_locations:
        new_black_locations.append((7 - loc[0], 7 - loc[1]))

    white_locations = new_black_locations
    black_locations = new_white_locations
    draw_pieces()


# ---------------------------MOVE CHECKING---------------------------------

# function checking all valid moves for pieces
def check_moves(pieces, locations, turn):
    global castling_moves
    moves_list = []
    all_moves_list = []
    castling_moves = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':  # checking valid moves for every piece
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        if piece == 'knight':  # checking valid moves for every piece
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        if piece == 'queen':  # checking valid moves for every piece
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list, castling_moves = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list  # all available moves of a piece in one turn


# valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':  # white pawn conditions for moving forward
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and \
                position[1] < 7:  # board edge
            moves_list.append((position[0], position[1] + 1))
            # pawn can go 2 squares forward on its first move
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and \
                    position[1] == 1:  # 1 - starting position
                moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1,
                position[1] + 1) in black_locations:  # diagonal attack right
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1,
                position[1] + 1) in black_locations:  # diagonal attack left
            moves_list.append((position[0] - 1, position[1] + 1))
    elif color == 'black':
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and \
                position[1] > 0:  # board edge
            moves_list.append((position[0], position[1] - 1))
            # pawn can go 2 squares forward on its first move
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and \
                    position[1] == 6:  # 6 - starting position
                moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1,
                position[1] - 1) in white_locations:  # diagonal attack right
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1,
                position[1] - 1) in white_locations:  # diagonal attack left
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


# valid rook moves
def check_rook(position, color):
    moves_list = []
    x = 999
    y = 999
    friends_list = []
    enemies_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    elif color == 'black':
        enemies_list = white_locations
        friends_list = black_locations

    for i in range(4):  # up, down, right, left
        path = True
        chain = 1
        if i == 0:  # up
            x = 0
            y = -1
        elif i == 1:  # down
            x = 0
            y = 1
        elif i == 2:  # right
            x = 1
            y = 0
        elif i == 3:  # left
            x = -1
            y = 0
        while path:
            # check how many moves are available for rook in evey direction
            #  moves range (don't append positions with friendly pieces)
            if (position[0] + (chain * x),
                    position[1] + (chain * y)) not in friends_list and \
                0 <= position[0] + (chain * x) <= 7 and 0 <= position[
                    1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                # option of capturing opposite color pieces
                if (position[0] + (chain * x),
                        position[1] + (chain * y)) in enemies_list:
                    # rook can capture enemy piece, but can't go further
                    path = False
                chain += 1
            else:
                # rook can't move if friendly piece od board edge is in the way
                path = False

    return moves_list


# valid knight moves
def check_knight(position, color):
    moves_list = []
    friends_list = []
    if color == 'white':
        friends_list = white_locations
    elif color == 'black':
        friends_list = black_locations
    # 8 squares to check for knights; two squares in one dir, one to the other
    targets = [(1, 2), (1, -2), (2, 1), (2, -1),
               (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):  # checking moves for knight in position[0], position[1]
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[
                1] <= 7:
            moves_list.append(target)
    return moves_list


# valid bishop moves (same method as rook, just different x and y modifiers)
def check_bishop(position, color):
    moves_list = []
    x = 999
    y = 999
    friends_list = []
    enemies_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    elif color == 'black':
        enemies_list = white_locations
        friends_list = black_locations
    for i in range(4):
        path = True
        chain = 1
        if i == 0:  # right up
            x = 1
            y = -1
        elif i == 1:  # left up
            x = -1
            y = -1
        elif i == 2:  # right down
            x = 1
            y = 1
        elif i == 3:  # left down
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x),
                    position[1] + (chain * y)) not in friends_list and \
                0 <= position[0] + (chain * x) <= 7 and 0 <= position[
                    1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                # option of capturing opposite color pieces
                if (position[0] + (chain * x),
                        position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# valid queen moves (rook and bishop moves combination)
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# valid king moves (similar to knight moves function)
def check_king(position, color):
    moves_list = []
    castle_moves = check_castling()
    friends_list = []

    if color == 'white':
        friends_list = white_locations
    elif color == 'black':
        friends_list = black_locations
    # 8 squares to check for king; one square any direction
    targets = [(1, 1), (1, 0), (1, -1), (-1, 1),
               (-1, 0), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):  # checking moves for knight in position[0], position[1]
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[
                1] <= 7:
            moves_list.append(target)

    return moves_list, castle_moves


# ----------------------------Drawing---------------------------------------
# draw valid moves
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# draw valid moves
def draw_valid(moves):
    for i in range(
            len(moves)):  # centering dots showing the moves on the screen
        pygame.draw.circle(
            screen, 'gold', (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50),
            5)


# draw captured pieces on the right side
def draw_captured():
    # white captures black piece
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        if Is_changed == 0:
            screen.blit(small_black_images[index], (825, 5 + 50 * i))
        else:
            screen.blit(small_white_images[index], (925, 5 + 50 * i))
    # black captures white piece
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        if Is_changed == 0:
            screen.blit(small_white_images[index], (925, 5 + 50 * i))
        else:
            screen.blit(small_black_images[index], (825, 5 + 50 * i))


# draw red rectangle indicating that king is in check
def draw_check():
    global check
    check = False
    if 'king' in white_pieces:  # if statement in order not to get error
        king_index = white_pieces.index('king')
        king_location = white_locations[king_index]
        for i in range(len(black_options)):
            if king_location in black_options[i]:
                check = True
                pygame.draw.rect(screen, 'dark red',
                                 [white_locations[king_index][0] * 100,
                                  white_locations[king_index][1] * 100, 100,
                                  100], 6)
    if 'king' in black_pieces:
        king_index = black_pieces.index('king')
        king_location = black_locations[king_index]
        for i in range(len(white_options)):
            if king_location in white_options[i]:
                check = True
                pygame.draw.rect(screen, 'dark red',
                                 [black_locations[king_index][0] * 100,
                                  black_locations[king_index][1] * 100, 100,
                                  100], 6)


def draw_game_over():
    if (winner == 'black' and Is_changed == 0) or (
            winner == 'white' and Is_changed == 1) or winner == 'whiteff':
        pygame.draw.rect(screen, 'white', [
            160, 200, 550, 400], border_radius=20)
        screen.blit(big_font.render('Black won the game!',
                                    True, 'black'), (170, 210))  # destination
        screen.blit(font.render(
            'Press ENTER key to close the game', True, 'black'), (260, 550))
        black_victory = pygame.image.load('images/black-king.png')
        black_victory = pygame.transform.scale(black_victory, (260, 260))
        screen.blit(black_victory, (300, 270))
    elif winner == 'draw':
        pygame.draw.rect(screen, 'black', [
            160, 200, 550, 400], border_radius=20)
        screen.blit(big_font.render('Draw!', True, 'white'),
                    (360, 230))  # destination
        screen.blit(font.render(
            'Press ENTER key to close the game', True, 'white'), (260, 550))
        white_victory = pygame.image.load('images/white-king.png')
        white_victory = pygame.transform.scale(
            white_victory, (200, 200))  # white king
        black_victory = pygame.image.load('images/black-king.png')
        black_victory = pygame.transform.scale(
            black_victory, (200, 200))  # black king
        screen.blit(white_victory, (250, 300))
        screen.blit(black_victory, (460, 300))
    else:
        pygame.draw.rect(screen, 'black', [
            160, 200, 550, 400], border_radius=20)
        screen.blit(big_font.render('White won the game!',
                                    True, 'white'), (170, 210))  # destination
        screen.blit(font.render(
            'Press ENTER key to close the game', True, 'white'), (260, 550))
        white_victory = pygame.image.load('images/white-king.png')
        white_victory = pygame.transform.scale(white_victory, (260, 260))
        screen.blit(white_victory, (300, 270))


def introduce():
    screen.blit(backgroundPNG, (0, 0))
    intro = True
    blink_timer = 0
    blink_speed = 30  # Adjust blinking speed (lower value blinks faster)

    # Display introduction text
    screen.blit(PiecesPNG, (0, 100))  # font color
    screen.blit(bigger_font.render('Welcome to the chess game!',
                                   True, (244, 243, 219)), (80, 60))
    screen.blit(medium_font.render(
        'Controls:', True, (184, 243, 219)), (370, 170))
    screen.blit(font.render('RMB  ->  moving the pieces, forfeiting',
                            True, (244, 223, 219)), (290, 230))
    screen.blit(font.render('ENTER  ->  closing the window after the game',
                            True, (244, 223, 219)), (290, 265))
    screen.blit(font.render('1  ->  choose white',
                            True, (244, 223, 219)), (290, 300))
    screen.blit(font.render('2  ->  choose black',
                            True, (244, 223, 219)), (290, 335))

    screen.blit(medium_font.render('Press SPACE to continue...',
                                   True, (190, 225, 222)), (230, 450))

    while intro:
        # if player closes the screen during intro screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        pygame.display.flip()
        timer.tick(fps)


def pick_side():
    global turn_step

    screen.fill('black')
    pygame.draw.rect(screen, 'black', [0, 0, 1000, 300])  # rect
    pygame.draw.rect(screen, 'black', [0, 400, 1000, 500])  # rect
    pygame.draw.rect(screen, 'gold', [0, 400, 1000, 500], 5)  # border
    pygame.draw.rect(screen, 'gold', [500, 400, 5, 500], 5)  # middle line
    screen.blit(gigantic_font.render(
        'Pick the side for', True, 'white'), (170, 70))
    screen.blit(gigantic_font.render('Player 1!', True, 'white'), (320, 170))
    screen.blit(font.render('Press 1 for white!', True, 'white'), (160, 345))
    screen.blit(font.render('Press 2 for black!', True, 'white'), (660, 345))
    # displaying gigantic kings
    black_king_gigant = pygame.image.load('images/black-king.png')
    black_king_gigant = pygame.transform.scale(black_king, (400, 400))
    screen.blit(black_king_gigant, (550, 450))
    choice = True

    white_king_gigant = pygame.image.load('images/black-king.png')
    white_king_gigant = pygame.transform.scale(white_king, (400, 400))
    screen.blit(white_king_gigant, (50, 450))
    choice = True

    while choice:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # white
                    if Is_changed == 0:
                        change_sides()  # change sides
                    else:
                        turn_step = 2
                    choice = False

                if event.key == pygame.K_2:  # black
                    if Is_changed == 1:
                        change_sides()  # change sides
                    else:
                        turn_step = 0
                    choice = False
        pygame.display.flip()
        timer.tick(fps)


# are castling moves valid
def check_castling():
    # king can't be in check after and before,
    # king and rook has not moved previously, nothing between king and rook
    # valid castle moves as [((king_coords), (castle_coords))]
    castle_moves = []
    rook_indexes = []
    rook_locations = []
    king_index = 0
    king_pos = (0, 0)
    if turn_step >= 2:  # blacks turn
        for i in range(len(white_pieces)):
            if white_pieces[i] == 'rook':
                # checking whether rook has moved
                rook_indexes.append(white_moved[i])
                rook_locations.append(white_locations[i])
            if white_pieces[i] == 'king':
                king_index = i
                king_pos = white_locations[i]
        # if white king didn't move and at least one false in rook indexes
        # and king not in check
        if not white_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if Is_changed == 0:
                    # rook to the right of the king
                    if rook_locations[i][0] > king_pos[0]:
                        empty_squares = [(king_pos[0] + 1, king_pos[1]),
                                         (king_pos[0] + 2, king_pos[1]),
                                         (king_pos[0] + 3, king_pos[1])]
                    else:
                        # rook to the left of the king
                        empty_squares = [
                            (king_pos[0] - 1, king_pos[1]),
                            (king_pos[0] - 2, king_pos[1])]
                    for j in range(len(empty_squares)):
                        # if something is in the way of castling
                        # or attacking king/rook
                        if empty_squares[j] in white_locations or \
                                empty_squares[j] in black_locations or \
                                empty_squares[j] in black_options or \
                                rook_indexes[i] is True:
                            castle = False

                elif Is_changed == 1:
                    # rook to the right of the king
                    if rook_locations[i][0] < king_pos[0]:
                        empty_squares = [(king_pos[0] - 1, king_pos[1]),
                                         (king_pos[0] - 2, king_pos[1]),
                                         (king_pos[0] - 3, king_pos[1])]
                    else:
                        # rook to the left of the king
                        empty_squares = [
                            (king_pos[0] + 1, king_pos[1]),
                            (king_pos[0] + 2, king_pos[1])]
                    for j in range(len(empty_squares)):
                        # if something is in the way of castling
                        # or attacking king/rook
                        if empty_squares[j] in white_locations or \
                                empty_squares[j] in black_locations or \
                                empty_squares[j] in black_options or \
                                rook_indexes[i] is True:
                            castle = False
                if castle:
                    # if castling is possible, king is moving to [1]
                    # and rook to [0] index of the list
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    elif turn_step <= 1:  # whites turn
        for i in range(len(black_pieces)):
            if black_pieces[i] == 'rook':
                # checking whether rook has moved
                rook_indexes.append(black_moved[i])
                rook_locations.append(black_locations[i])
            if black_pieces[i] == 'king':
                king_index = i
                king_pos = black_locations[i]
        # if white king didn't move and at least one false in rook indexes
        # and king not in check
        if not black_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if Is_changed == 0:
                    # rook to the right of the king
                    if rook_locations[i][0] > king_pos[0]:
                        empty_squares = [(king_pos[0] + 1, king_pos[1]),
                                         (king_pos[0] + 2, king_pos[1]),
                                         (king_pos[0] + 3, king_pos[1])]
                    else:
                        # rook to the left of the king
                        empty_squares = [
                            (king_pos[0] - 1, king_pos[1]),
                            (king_pos[0] - 2, king_pos[1])]
                elif Is_changed == 1:
                    if rook_locations[i][0] > king_pos[0]:
                        empty_squares = [
                            (king_pos[0] + 1, king_pos[1]),
                            (king_pos[0] + 2, king_pos[1])]
                    else:
                        empty_squares = [(king_pos[0] - 1, king_pos[1]),
                                         (king_pos[0] - 2, king_pos[1]),
                                         (king_pos[0] - 3, king_pos[1])]

                for j in range(len(empty_squares)):
                    # if something is in the way of castling
                    # or attacking king/rook
                    if empty_squares[j] in white_locations or empty_squares[
                            j] in black_locations or \
                        empty_squares[j] in white_options or rook_indexes[
                            i] == True:
                        castle = False
                if castle:
                    # if castling is possible, king is moving to [1]
                    # and rook to [0] index of the list
                    castle_moves.append((empty_squares[1], empty_squares[0]))

    return castle_moves


def draw_castling(moves):
    for i in range(
            len(moves)):  # set of coordinates; kings moves; x coordinate
        pygame.draw.circle(
            screen, 'red',
            (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 50), 8)


# pawn promotion
def check_promotion():
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index = 999  # index of the pawn that is getting promoted
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)  # appending the pawn index value
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 7:
            white_promotion = True
            promote_index = pawn_indexes[i]

    pawn_indexes = []  # resetting pawn indexes

    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)  # appending the pawn index value
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 0:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index


def draw_promotion():
    pygame.draw.rect(screen, (0, 170, 255), [800, 0, 200, 420])
    if (white_promote and Is_changed == 0) or (
            black_promote and Is_changed == 1):
        color = 'white'
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            index = piece_list.index(piece)
            screen.blit(white_images[index], (860, 5 + 100 * i))
    elif (black_promote and Is_changed == 0) or (
            white_promote and Is_changed == 1):
        color = 'black'
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            index = piece_list.index(piece)
            screen.blit(black_images[index], (860, 5 + 100 * i))
    pygame.draw.rect(screen, color, [800, 0, 200, 420], 8)  # border


def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 100
    y_pos = mouse_pos[1] // 100
    if white_promote and left_click and x_pos > 7 and y_pos < 4:
        white_pieces[promo_index] = white_promotions[y_pos]
    elif black_promote and left_click and x_pos > 7 and y_pos < 4:
        black_pieces[promo_index] = black_promotions[y_pos]


# ___________________________ MAIN GAME LOOP ______________________________
introduce()
pick_side()
# checking moves at the start of the game
black_options = check_moves(black_pieces, black_locations, 'black')
white_options = check_moves(white_pieces, white_locations, 'white')
print(black_options)
run = True
while run:
    timer.tick(fps)
    screen.fill((244, 243, 239))
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()

    if not game_over:
        # assigning values returned by the function
        white_promote, black_promote, promo_index = check_promotion()
        if white_promote or black_promote:
            draw_promotion()
            check_promo_select()
            black_options = check_moves(black_pieces, black_locations,
                                        'black')
            white_options = check_moves(white_pieces, white_locations, 'white')
            draw_check()
    # drawing valid moves
    if selection != 999:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
        if selected_piece == 'king':
            draw_castling(castling_moves)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if len(white_pieces) == 1 and len(black_pieces) == 1:
            winner = 'draw'
        elif event.type == pygame.MOUSEBUTTONDOWN \
                and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            ClickPos = (x_coord, y_coord)  # tuple with mouse position
            # forfeit button for black
            if ClickPos == (8, 8):
                winner = 'blackff'
            # forfeit button for white
            if ClickPos == (9, 8):
                winner = 'whiteff'
            if turn_step < 2:  # blacks turn
                if ClickPos in white_locations:
                    selection = white_locations.index(ClickPos)
                    # check what piece is selected
                    # (for drawing castling moves when king is selected)
                    selected_piece = white_pieces[selection]
                    if turn_step == 0:
                        turn_step = 1  # change of the t_s when piece is chosen
                # if move is valid and piece is selected (!= 999)
                if ClickPos in valid_moves and selection != 999:
                    # white piece position change
                    white_locations[selection] = ClickPos
                    white_moved[selection] = True  # important for castling
                    if ClickPos in black_locations:  # capturing the b piece
                        black_piece = black_locations.index(ClickPos)
                        # adding piece to the captured list
                        captured_pieces_white.append(black_pieces[black_piece])
                        # winner before popping black king from the list
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        # remove a piece from the active players list
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)
                    # black options after move
                    black_options = check_moves(
                        black_pieces, black_locations, 'black')
                    # white ...
                    white_options = check_moves(
                        white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 999
                    valid_moves = []  # clearing valid moves to find new ones

                # add option to castle
                elif selection != 999 and selected_piece == 'king':
                    for q in range(len(castling_moves)):
                        if ClickPos == castling_moves[q][0]:
                            # king moves to clicked position
                            white_locations[selection] = ClickPos
                            white_moved[selection] = True
                            if (ClickPos == (1, 0) and Is_changed == 0) or (
                                    ClickPos == (2, 0) and Is_changed == 1):
                                rook_coords = (0, 0)  # left rook
                            else:
                                rook_coords = (7, 0)  # right rook
                            rook_index = white_locations.index(rook_coords)
                            white_locations[rook_index] = castling_moves[q][1]
                            # black options after move
                            black_options = check_moves(black_pieces,
                                                        black_locations,
                                                        'black')
                            # white ...
                            white_options = check_moves(
                                white_pieces, white_locations, 'white')
                            turn_step = 2
                            selection = 999
                            # clearing valid moves to find new ones
                            valid_moves = []

            elif turn_step >= 2:  # whites turn
                if ClickPos in black_locations:
                    selection = black_locations.index(ClickPos)
                    # check what piece is selected
                    # (for drawing castling moves when king is selected)
                    selected_piece = black_pieces[selection]
                    if turn_step == 2:
                        turn_step = 3  # white has selected a piece
                # if move is valid and piece is selected (!= 999)
                if ClickPos in valid_moves and selection != 999:
                    # black piece position change
                    black_locations[selection] = ClickPos
                    black_moved[selection] = True  # important for castling
                    if ClickPos in white_locations:  # capturing the wh piece
                        white_piece = white_locations.index(ClickPos)
                        # adding to the captured list
                        captured_pieces_black.append(white_pieces[white_piece])
                        # winner before popping white king from the list
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        # remove white piece from the active players list
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)
                    # black options after move
                    black_options = check_moves(
                        black_pieces, black_locations, 'black')
                    # white ...
                    white_options = check_moves(
                        white_pieces, white_locations, 'white')
                    turn_step = 0  # black chooses the piece
                    selection = 999
                    valid_moves = []  # clearing valid moves to find new ones
                # add option to castle
                elif selection != 999 and selected_piece == 'king':
                    for q in range(len(castling_moves)):
                        if ClickPos == castling_moves[q][0]:
                            # king moves to clicked position
                            black_locations[selection] = ClickPos
                            black_moved[selection] = True
                            if (ClickPos == (1, 7) and Is_changed == 0) or (
                                    ClickPos == (2, 7) and Is_changed == 1):
                                rook_coords = (0, 7)  # left rook
                            else:
                                rook_coords = (7, 7)  # right rook

                            rook_index = black_locations.index(rook_coords)
                            black_locations[rook_index] = castling_moves[q][1]
                            # black options after move
                            black_options = check_moves(black_pieces,
                                                        black_locations,
                                                        'black')
                            # white ...
                            white_options = check_moves(
                                white_pieces, white_locations, 'white')
                            turn_step = 0
                            selection = 999
                            valid_moves = []

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:  # return is enter in pygame
                pygame.quit()
                sys.exit()

    # If one of the players won
    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame.quit()
sys.exit()  # to make sure I close everything
