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
b,k,n,p,q,r,B,K,N,P,Q,R = [pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (square_size, square_size)) for piece in ["b","k","n","p","q","r","B","K","N","P","Q","R"]]


board = [
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"]
]

emptyboard = [
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"]
]

def fromFEN(FEN):
    print(FEN)
    FEN = list(FEN)
    currentpos = 0
    currentrow = 0
    for i in range(8):
        for b in range(8):
            board[i][b] = "--"
    for i in FEN:
        if i.isnumeric():
            currentpos += int(i)
            continue
        elif i != "/" and i != " ":
            board[currentrow][currentpos] = i
        currentpos += 1
        if i == "/":
            currentrow += 1
            currentpos = 0
        if i == " ":
            break
    print(stockfish.get_board_visual())

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
    fromFEN(stockfish.get_fen_position())

for i in range(10):
    PlayFirstMove()

print(stockfish.get_board_visual())
print(str(board).replace("],", "]\n"))

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            col = mouse_x // square_size
            row = mouse_y // square_size
            
            nums = [0,8,7,6,5,4,3,2,1]

            selectedmove = str(col) + str(row)
            print(stockfish.get_board_visual())
            print(str(board).replace("],", "]\n"))
            
            if moving:
                print(start_row,start_col, ":", row,col)
                if board[start_row][start_col] != "--" and (row,col) != (start_row,start_col):
                    move = chr(start_col + 97) + str(nums[start_row]-1) + chr(col + 97) + str(nums[row] -1)
                    print(move)
                    if stockfish.is_move_correct(move):
                        print("a")
                        
                    
                        stockfish.make_moves_from_current_position([move])
                        fromFEN(stockfish.get_fen_position())

                        bestmove = stockfish.get_best_move()
                        if bestmove == None:
                            print("You Won! FEN:", stockfish.get_fen_position())
                            running = False
                        stockfish.make_moves_from_current_position([bestmove])
                        
                        
                        fromFEN(stockfish.get_fen_position())
                        
                        

                        if stockfish.get_best_move() == None:
                            print("You lost! FEN:", stockfish.get_fen_position())
                            running = False

                    moving = False
                else:
                    moving = False
            elif not moving:
                
                start_row = row
                start_col = col
                moving = True

    screen.fill(white)


    
    fromFEN(stockfish.get_fen_position())
    draw_board()

    if len(selectedmove) <= 2 and selectedmove != "--":
        
        var = list(selectedmove)
        column, roww = int(var[0]), int(var[1])
        if moving:
            pygame.draw.rect(screen, (255,0,0), (column*square_size, roww*square_size, square_size,square_size))



    draw_pieces()

    pygame.display.update()


pygame.quit()
