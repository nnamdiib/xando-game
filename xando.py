# X and O game, (Naughts and Crosses clone)
# By Uxbal, davidia@outlook.com
###### Truth is singular; Its versions are mistruths ######
# try initializing board with 'False' instead of 0
import pygame, sys, random, os
from pygame.locals import *

WINDOWWIDTH = 500
WINDOWHEIGHT = 500
XMARGIN = 28
YMARGIN = 28
GAP = 5
BOARDWIDTH = WINDOWWIDTH - (XMARGIN * 2)
BOARDHEIGHT = BOARDWIDTH
BOXSIZE = BOARDWIDTH / 3
assert (BOARDWIDTH / BOXSIZE == 3), "Box size should go 3 places into boardwidth and height"

#            R    G    B  
WHITE =    (255, 255, 255)
DARKBLUE = ( 33,  47,  61)
RED =      (241,  62,  65)
GREEN =    ( 46, 204, 113)

BGCOLOUR = DARKBLUE
X = 'X'
O = 'O'

RESOURCES_PATH = os.path.join(os.path.dirname(__file__), "assets")
FONT_PATH = os.path.join(RESOURCES_PATH, "Exo-Light.otf")

def main():
    global BASICFONT, DISPLAYSURF, last_move, board

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('XandO')
    BASICFONT = pygame.font.Font(FONT_PATH, 80)
    SCOREFONT = pygame.font.Font(FONT_PATH, 17)

    # Setting up game variables.
    board = get_blank_board()
    first_move = X # player that goes first
    last_move = None
    X_score = 0
    O_score = 0
    DISPLAYSURF.fill(BGCOLOUR)

    while True:
        check_quit()
        draw_board(board)

        # check if the game is a draw
        if check_for_draw(board):
            # reset game if its a draw
            pygame.time.wait(2000)
            reset()
        else:
            # check if someone won the game.
            result = check_for_win(board)
            if False not in result:
                # Someone won the game. Increment score of winner and reset.
                # result[0] holds the name of the wonner (X or O)
                # result[1] is a flag. 'True' if a winner was found. 'False' otherwise.
                if result[0] == X:
                    X_score += 1
                elif result[0] == O:
                    O_score += 1
                pygame.time.wait(2000)
                reset()

        # setting up the text the show X scores.
        x_score_surf = SCOREFONT.render("X: %s" %(X_score), True, GREEN)
        x_score_surf_rect = x_score_surf.get_rect()
        x_score_surf_rect.topleft = (YMARGIN, XMARGIN)

        # setting up the text to show the O scores.
        o_score_surf = SCOREFONT.render("O: %s"%(O_score), True, WHITE)
        o_score_surf_rect = o_score_surf.get_rect()
        o_score_surf_rect.topleft = (XMARGIN + x_score_surf_rect.width + (BOXSIZE * 2.5), YMARGIN)
        
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(board, event.pos[0], event.pos[1])
                if spotx != None and spoty != None:
                    if last_move == X:
                        # if last move was X, it is O's turn.
                        make_move(board, spotx, spoty, O)                    
                    elif last_move == O:
                        # if last move was O, it is X's turn.
                        make_move(board, spotx, spoty, X)                    
                    elif not last_move: 
                        # it is the first move in the game.
                        make_move(board, spotx, spoty, first_move)
                    
        DISPLAYSURF.blit(x_score_surf, x_score_surf_rect)
        DISPLAYSURF.blit(o_score_surf, o_score_surf_rect)
        pygame.display.update()

def terminate():
    pygame.quit()
    sys.exit()

def check_quit():
    for event in pygame.event.get(QUIT): # get all QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):
        # all KEYUP events.
        if event.key == K_ESCAPE:
            terminate() # terminate if KEYUP was Esc
        pygame.event.post(event) # Put the other KEYUP event objects back

def get_left_top(tilex, tiley):
    # converts board coords to pixel coordinates
    left = XMARGIN + (tilex * BOXSIZE) + (tilex - 1)
    top = YMARGIN + (tiley * BOXSIZE) + (tiley - 1)
    return (left, top)

def getSpotClicked(board, x, y):
    # converts pixel coordinates to board coords
    boardx, boardy = None, None

    for boxy in range(len(board)):
        for boxx in range(len(board[0])):
            left, top = get_left_top(boxx, boxy)
            box_rect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if box_rect.collidepoint(x, y):
                boardx, boardy = boxx, boxy
    
    return (boardx, boardy)

def make_move(board, x, y, player):
    global last_move
    # this switch is neccessary so (x,y) matches the on-screen cell coords.
    x, y = y, x  
    if player == X:
        if board[x][y] == 0:
            board[x][y] = X
            last_move = X
    elif player == O:
        if board[x][y] == 0:
            board[x][y] = O
            last_move = O
    else:
        # first move of game 
        board[x][y] = X 
        last_move = first_move

def get_blank_board():
    # creating the board structure: a list that contains three lists. 
    # [ [1] , [2], [3] ]
    board = []
    for y in range(0, BOARDHEIGHT, BOXSIZE):
        row = []
        for x in range(0, BOARDWIDTH, BOXSIZE):
            row.append(0)
        board.append(row)
    return board

def reset():
    global board
    DISPLAYSURF.fill(BGCOLOUR)
    new_board = get_blank_board()
    board = new_board
    last_move = None


def draw_moves(tilex, tiley, text=''):
    # draws the X and O's, or empty cell
    left, top = get_left_top(tilex, tiley)
    box = pygame.Rect(top, left, BOXSIZE, BOXSIZE)
    if text == X:
        text_surf = BASICFONT.render(text, True, GREEN)
    elif text == O:
        text_surf = BASICFONT.render(text, True, WHITE)
    else:
        text_surf = BASICFONT.render(text, True, BGCOLOUR)
    text_rect = text_surf.get_rect()
    text_rect.center = (box.centerx, box.centery)
    DISPLAYSURF.blit(text_surf, text_rect)

def draw_board(board):
    # draw vertical lines
    for x in range(XMARGIN + BOXSIZE, BOARDWIDTH, BOXSIZE):
        pygame.draw.line(DISPLAYSURF, RED, (x, YMARGIN), (x, BOARDHEIGHT), 5)
    # draw horizontal lines
    for y in range(YMARGIN + BOXSIZE, BOARDHEIGHT, BOXSIZE):
        pygame.draw.line(DISPLAYSURF, RED, (YMARGIN, y), (BOARDWIDTH, y), 5)
    # loop through each item in board and draw what it contains
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == X:
                draw_moves(x, y, X)
            elif board[x][y] == O:
                draw_moves(x, y, O)
            else: # its an empty cell
                draw_moves(x, y)
    pygame.display.update()

def check_for_win(board):
    # check if consecutive cells match, and if theres a winner
    # This part seems grossly inefficient. I broke the DRY rule repeatedly.

    if board[0][0] == board[1][1] == board[2][2] != 0: # Diagonal win -ve slope
        winner = board[0][0]
        win = True
    elif board[2][0] == board[1][1] == board[0][2] != 0: # diagonal win +ve slope
        winner = board[2][0]
        win = True
    elif board[0][0] == board[1][0] == board[2][0] != 0: # horizontal up win
        winner = board[0][0]
        win = True
    elif board[0][1] == board[1][1] == board[2][1] != 0: # horizontal middle win
        winner =  board[0][1]
        win = True
    elif board[0][2] == board[1][2] == board[2][2] != 0: # horizontal down win
        winner = board[0][2]
        win = True
    elif board[0][0] == board[0][1] == board[0][2] != 0: # vertical left win
        winner = board[0][0]
        win = True
    elif board[1][0] == board[1][1] == board[1][2] != 0: # vertical middle win
        winner = board[1][0]
        win = True
    elif board[2][0] == board[2][1] == board[2][2] != 0: # vertical right win
        winner = board[2][0]
        win = True
    else:
        winner = False
        win = False
    return (winner, win)

def check_for_draw(board):
    # loop throigh board data structure and add each cell
    # if there is TypeError in adding, not all cells have been filled.
    # else, if the length of all added cells == (row length * column length) then
    # all moves have been played. its a draw.
    total = ''
    for x in range(len(board)):
        for y in range(len(board[0])):
            try:
                total += board[x][y]
            except TypeError:
                draw = False
                break
    if len(total) == (len(board) * len(board[0])):
        draw = True
    return draw

if __name__ == '__main__':
    main()