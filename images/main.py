from stockfish import Stockfish
from time import sleep
import pygame



screen = pygame.display.set_mode((600, 600))
stockfish = Stockfish(path="stockfish/stockfish-ubuntu-x86-64-avx2")
running = True
customelo = False # set this to True if you want to customize the bots elo (not recommended as it makes the bot slower)
eloinput = None

white = (255, 255, 255)
black = (0, 0, 0)
selectedmove = "--"
moving = False


square_size = 600//8
bb,bk,bn,bp,bq,br,wb,wk,wn,wp,wq,wr = [pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (square_size, square_size)) for piece in ["bb","bk","bn","bp","bq","br","wb","wk","wn","wp","wq","wr"]]

board = [
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"]
]

def draw_board():
    for row in range(8):
        for col in range(8):
            x = col * square_size
            y = row * square_size
            if (row + col) % 2 == 0:
                color = white
            else:
                color = black
            pygame.draw.rect(screen, color, (x, y, square_size, square_size))

def draw_pieces():
    for row in range(8):
        for col in range(8):
            if board[row][col] != "--":
                piece = globals()[board[row][col]]
                x = col * square_size
                y = row * square_size
                screen.blit(piece, (x, y))

if customelo:
    eloinput = input("Please enter the ELO you want stockfish to play at:")
    eloinput = eloinput.strip()
    if eloinput.isnumeric():
        print("set stockfish ELO to ", eloinput)
        stockfish.set_elo_rating(int(eloinput))
    else:
        print("Please enter a number!")
        
pygame.init()
pygame.display.set_caption("Chess | Elo: " + str(eloinput))

def PlayFirstMove():
    bestmove = stockfish.get_best_move()
    stockfish.make_moves_from_current_position([bestmove])
    #print(stockfish.get_board_visual())
    bestmove = list(bestmove)
    #print("best move", bestmove)

    bestmove[0] = ord(bestmove[0]) - 97
    bestmove[1] = int(bestmove[1]) - 1
    bestmove[2] = ord(bestmove[2]) - 97
    bestmove[3] = int(bestmove[3]) - 1
    #print("in numbers:", bestmove)
    board[bestmove[3]][bestmove[2]] = board[bestmove[1]][bestmove[0]]
    board[bestmove[1]][bestmove[0]] = "--"

PlayFirstMove()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            col = mouse_x // square_size
            row = mouse_y // square_size
            
            #print(chr(col + 97) + str(row + 1))
            selectedmove = str(col) + str(row)
            #print(moving)
            if moving:
                if board[start_row][start_col] != "--" and (row,col) != (start_row,start_col):
                    move = chr(start_col + 97) + str(start_row + 1) + chr(col + 97) + str(row + 1)
                    #print("moving", start_row, start_col, ":", row, col)
                    if stockfish.is_move_correct(move):
                        board[row][col] = board[start_row][start_col]
                        board[start_row][start_col] = "--"
                        
                        #print(move)
                        #print(start_row,start_col,row,col)
                    
                        #print("correct move, best move:", stockfish.get_best_move())

                        stockfish.make_moves_from_current_position([move])
                        
                        bestmove = stockfish.get_best_move()
                        if bestmove == None:
                            print("You Won! FEN:", stockfish.get_fen_position())
                            running = False
                        stockfish.make_moves_from_current_position([bestmove])
                        #print(stockfish.get_board_visual())
                        bestmove = list(bestmove)
                        #print("best move", bestmove)
                        
                        bestmove[0] = ord(bestmove[0]) - 97
                        bestmove[1] = int(bestmove[1]) - 1
                        bestmove[2] = ord(bestmove[2]) - 97
                        bestmove[3] = int(bestmove[3]) - 1
                        #print("in numbers:", bestmove)
                        board[bestmove[3]][bestmove[2]] = board[bestmove[1]][bestmove[0]]
                        board[bestmove[1]][bestmove[0]] = "--"
                        
                        if stockfish.get_best_move() == None:
                            print("You lost! FEN:", stockfish.get_fen_position())
                            running = False

                    moving = False
                else:
                    #print("beep", start_row, start_col, ":", row, col)
                    moving = False
            elif not moving:
                
                start_row = row
                start_col = col
                #print("not moving", start_row, start_col)
                moving = True

    screen.fill(white)




    draw_board()

    if len(selectedmove) <= 2 and selectedmove != "--":
        var = list(selectedmove)
        column, roww = int(var[0]), int(var[1])
        if moving:
            pygame.draw.rect(screen, (255,0,0), (column*square_size, roww*square_size, square_size,square_size))



    draw_pieces()

    pygame.display.update()


pygame.quit()
