import pygame as pg
from packageChess import boardChess123 as boardChess
from packageChess import menu as cntxMenu
import datetime as dt


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


mode = cntxMenu.startMenu()

screen = pg.display.set_mode((640, 640))

screen.fill("white")
pg.display.set_caption("Chess")
boardIMG = pg.image.load(r"packageChess/sprites/chessBoard.jpg")
boardRect = boardIMG.get_rect(bottomright=(640, 640))
screen.blit(boardIMG, boardRect)

pg.init()
pg.mixer.music.load(r"packageChess/sprites/move-self.mp3")

gameBoard = boardChess.Board()

if mode == "random" or mode == "randomTimed":
    gameBoard.setRandomBoard()
else:
    gameBoard.setStandardBoard()

if mode == "secret" or mode == "secretTimed":
    secretWhite = None
    secretBlack = None
    updateStandartDesk()

    while secretWhite is None:
        pg.display.flip()
        for event in pg.event.get():
            ID_event = event.type
            if ID_event == pg.QUIT:
                exit()
            if ID_event == 1025:
                x, y = event.pos
                x = x // 80
                y = y // 80
                piece = gameBoard.board[y][x]
                if piece.color == 1:
                    secretWhite = piece
                    pg.mixer.music.load(r"packageChess/sprites/steam-message.mp3")
                    pg.mixer.music.play()
    while secretBlack is None:
        pg.display.flip()
        for event in pg.event.get():
            ID_event = event.type
            if ID_event == pg.QUIT:
                exit()
            if ID_event == 1025:
                x, y = event.pos
                x = x // 80
                y = y // 80
                piece = gameBoard.board[y][x]
                if piece.color == -1:
                    secretBlack = piece
                    pg.mixer.music.load(r"packageChess/sprites/steam-message.mp3")
                    pg.mixer.music.play()

timeOfLastTurn = dt.datetime.now()
while True:

    #  Трансформация пешек
    if len(gameBoard.checkPawn()):
        p = gameBoard.checkPawn()
        if p[1] == 0:
            gameBoard.transformPawn(cntxMenu.pawnTransformationWhite())
        else:
            gameBoard.transformPawn(cntxMenu.pawnTransformationBlack())
        screen = pg.display.set_mode((640, 640))
        screen.fill("white")
        pg.display.set_caption("Chess")

    updateStandartDesk()

    if mode == "standard" or mode == "random":
        if gameBoard.checkForMate() or gameBoard.checkForStalemate():
            break
        for event in pg.event.get():
            ID_event = event.type

            if ID_event == pg.QUIT:
                exit()

            if ID_event == 1025:
                if gameBoard.notSelected:
                    x, y = event.pos
                    x = x // 80
                    y = y // 80
                    print(x + 1, 8 - y)
                    gameBoard.turns = gameBoard.selectPiece(x, y)
                    gameBoard.notSelected = not (len(gameBoard.turns[0]) or len(gameBoard.turns[1]))
                    if not gameBoard.notSelected:
                        selectedPiece = (x, y)
                        print(selectedPiece)
                else:
                    x, y = event.pos
                    click = (x // 80, y // 80)
                    if click in gameBoard.turns[0] or click in gameBoard.turns[1]:
                        if click in gameBoard.turns[0]:
                            pg.mixer.music.load(r"packageChess/sprites/move-self.mp3")
                        else:
                            pg.mixer.music.load(r"packageChess/sprites/move-check.mp3")
                        gameBoard.movePiece(selectedPiece[0], selectedPiece[1], click[0], click[1])
                        pg.mixer.music.play()
                        if gameBoard.checkCheck():
                            pg.mixer.music.load(r"packageChess/sprites/steam-message.mp3")
                            pg.mixer.music.play()
                        gameBoard.turn *= -1

                    gameBoard.turns = []
                    gameBoard.notSelected = True
    elif mode == "standardTimed" or mode == "randomTimed":
        if gameBoard.checkForMate() or gameBoard.checkForStalemate():
            break

        curTime = dt.datetime.now()

        if (curTime - timeOfLastTurn).total_seconds() > 20:
            pg.mixer.music.load(r"packageChess/sprites/clock.mp3")
            pg.mixer.music.play()
            if gameBoard.turn == 1 and gameBoard.whiteChecked:
                gameBoard.boardState = 1
                break
            elif gameBoard.turn == -1 and gameBoard.blackChecked:
                gameBoard.boardState = -1
                break
            gameBoard.turn *= -1
            gameBoard.turns = []
            gameBoard.notSelected = True
            timeOfLastTurn = dt.datetime.now()
            continue

        for event in pg.event.get():
            ID_event = event.type

            if ID_event == pg.QUIT:
                exit()

            if ID_event == 1025:
                if gameBoard.notSelected:
                    x, y = event.pos
                    x = x // 80
                    y = y // 80
                    print(x + 1, 8 - y)
                    gameBoard.turns = gameBoard.selectPiece(x, y)
                    gameBoard.notSelected = not (len(gameBoard.turns[0]) or len(gameBoard.turns[1]))
                    if not gameBoard.notSelected:
                        selectedPiece = (x, y)
                else:
                    x, y = event.pos
                    click = (x // 80, y // 80)
                    if click in gameBoard.turns[0] or click in gameBoard.turns[1]:
                        if click in gameBoard.turns[0]:
                            pg.mixer.music.load(r"packageChess/sprites/move-self.mp3")
                        else:
                            pg.mixer.music.load(r"packageChess/sprites/move-check.mp3")
                        gameBoard.movePiece(selectedPiece[0], selectedPiece[1], click[0], click[1])
                        pg.mixer.music.play()
                        if gameBoard.checkCheck():
                            pg.mixer.music.load(r"packageChess/sprites/steam-message.mp3")
                            pg.mixer.music.play()
                        timeOfLastTurn = dt.datetime.now()
                        gameBoard.turn *= -1

                    gameBoard.turns = []
                    gameBoard.notSelected = True
    elif mode == "secret" or mode == "secretTimed":
        curTime = dt.datetime.now()

        if gameBoard.checkForStalemateSecret():
            break
        if gameBoard.board[secretWhite.y][secretWhite.x] != secretWhite:
            gameBoard.boardState = 1
            break
        if gameBoard.board[secretBlack.y][secretBlack.x] != secretBlack:
            gameBoard.boardState = -1
            break

        if mode == "secretTimed" and (curTime - timeOfLastTurn).total_seconds() > 20:
            pg.mixer.music.load(r"packageChess/sprites/clock.mp3")
            pg.mixer.music.play()
            gameBoard.turn *= -1
            gameBoard.turns = []
            gameBoard.notSelected = True
            timeOfLastTurn = dt.datetime.now()
            continue

        for event in pg.event.get():
            ID_event = event.type
            if ID_event == pg.QUIT:
                exit()

            if ID_event == 1025:
                if gameBoard.notSelected:
                    x, y = event.pos
                    x = x // 80
                    y = y // 80
                    print(x + 1, 8 - y)
                    gameBoard.turns = gameBoard.selectPieceSecret(x, y)
                    gameBoard.notSelected = not (len(gameBoard.turns[0]) or len(gameBoard.turns[1]))
                    if not gameBoard.notSelected:
                        selectedPiece = (x, y)
                else:
                    x, y = event.pos
                    click = (x // 80, y // 80)
                    if click in gameBoard.turns[0] or click in gameBoard.turns[1]:
                        if click in gameBoard.turns[0]:
                            pg.mixer.music.load(r"packageChess/sprites/move-self.mp3")
                        else:
                            pg.mixer.music.load(r"packageChess/sprites/move-check.mp3")
                        timeOfLastTurn = dt.datetime.now()
                        gameBoard.movePiece(selectedPiece[0], selectedPiece[1], click[0], click[1])
                        pg.mixer.music.play()
                        gameBoard.turn *= -1

                    gameBoard.turns = []
                    gameBoard.notSelected = True
    pg.display.flip()

pg.font.init()
font = pg.font.Font(None, 36)
text = font.render("Hello Wold", True, (0, 0, 0))

if gameBoard.boardState == -1:
    text = font.render("Победа Белых", True, (255, 0, 0))
elif gameBoard.boardState == 1:
    text = font.render("Победа Чёрных", True, (255, 0, 0))
else:
    text = font.render("Пат", True, (255, 255, 255))

place = text.get_rect(center=(320, 320))
screen.blit(text, place)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

    pg.display.flip()