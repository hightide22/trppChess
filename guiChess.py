import pygame as pg
import os
from packageChess import boardChess123 as boardChess
from packageChess import consoleChess as console
from packageChess import menu


def updateStandartDesk():
    screen.blit(boardIMG, boardRect)
    for i in range(8):
        for j in range(8):
            pieceIMG = pg.image.load(r"packageChess/sprites/" + str(gameBoard.board[i][j]) + ".png")
            pieceRect = pieceIMG.get_rect(center=(40 + 80 * j, 40 + 80 * i))
            screen.blit(pieceIMG, pieceRect)
    if len(gameBoard.turns):
        for i in gameBoard.turns[0]:
            webImg = pg.image.load(r"packageChess/sprites/pos.png")
            webRec = webImg.get_rect(center=(40 + 80 * i[0], 40 + 80 * i[1]))
            screen.blit(webImg, webRec)
        for i in gameBoard.turns[1]:
            webImg = pg.image.load(r"packageChess/sprites/kill.png")
            webRec = webImg.get_rect(center=(40 + 80 * i[0], 40 + 80 * i[1]))
            screen.blit(webImg, webRec)


cntxMenu = menu.Menu()

mode = cntxMenu.startMenu()

#mode = "standard"


screen = pg.display.set_mode((640, 640))
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (640,640)

screen.fill("white")
pg.display.set_caption("Chess")
boardIMG = pg.image.load(r"packageChess/sprites/chessBoard.jpg")
boardRect = boardIMG.get_rect(bottomright=(640, 640))
screen.blit(boardIMG, boardRect)

gameBoard = boardChess.Board()

if mode == "standard":
    gameBoard.setStandardBoard()
elif mode == "random":
    gameBoard.setRandomBoard()


print(gameBoard.board)
while True:

    #  Трансформация пешек
    if len(gameBoard.checkPawn()):
        p = gameBoard.checkPawn()
        if p[1] == 0:
            gameBoard.transformPawn(p, cntxMenu.pawnTransormationWhite())
        else:
            gameBoard.transformPawn(p, cntxMenu.pawnTransormationBlack())
        screen = pg.display.set_mode((840, 640))
        screen.fill("white")
        pg.display.set_caption("Chess")

    gameBoard.checkForKings()
    if gameBoard.checkForMate() or gameBoard.checkForStalemate():
        exit(1)
    updateStandartDesk()

    for event in pg.event.get():
        ID_event = event.type

        if ID_event == pg.QUIT:
            exit()

        if ID_event == 1025:
            if gameBoard.notSelected:
                x, y = event.pos
                x = x // 80
                y = y // 80
                print(x + 1, 8 - y )
                gameBoard.turns = gameBoard.selectPiece(x, y)
                gameBoard.notSelected = not (len(gameBoard.turns[0]) or len(gameBoard.turns[1]))
                if not gameBoard.notSelected:
                    selectedPiece = (x, y)
            else:
                x, y = event.pos
                click = (x//80, y//80)
                if click in gameBoard.turns[0] or click in gameBoard.turns[1]:
                    gameBoard.movePiece(selectedPiece[0], selectedPiece[1], click[0], click[1])
                    ch = gameBoard.checkCheck()
                    gameBoard.turn *= -1

                gameBoard.turns = []
                gameBoard.notSelected = True

    pg.display.flip()

# pg.font.init()
# font = pg.font.Font(None, 36)
# text = font.render("Hello Wold", True, (0, 0, 0) )
# place = text.get_rect(topleft=(660, 0), height=200, width = 100)
# screen.blit(text, place)
# log = console.console()

