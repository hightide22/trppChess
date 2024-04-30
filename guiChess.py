import pygame as pg
from packageChess import boardChess123 as boardChess
from packageChess import menu as cntxMenu
import datetime as dt


class Gui:
    screen = None

    loop = True

    mode = "standart"

    gameBoard = None

    secretWhite = None
    secretBlack = None

    timeOfLastTurn = None

    boardIMG = pg.image.load(r"packageChess/sprites/chessBoard.jpg")
    boardRect = boardIMG.get_rect(bottomright=(640, 640))

    selectedPiece = None

    def __init__(self):
        self.screen = pg.display.set_mode((640, 640))

    def selectSecretPieces(self):
        while self.secretWhite is None:
            pg.display.flip()
            for event in pg.event.get():
                ID_event = event.type
                if ID_event == pg.QUIT:
                    exit()
                if ID_event == 1025:
                    x, y = event.pos
                    x = x // 80
                    y = y // 80
                    piece = self.gameBoard.board[y][x]
                    if piece.color == 1:
                        self.secretWhite = piece
                        pg.mixer.music.load(r"packageChess/sprites/steam-message.mp3")
                        pg.mixer.music.play()
        while self.secretBlack is None:
            pg.display.flip()
            for event in pg.event.get():
                ID_event = event.type
                if ID_event == pg.QUIT:
                    exit()
                if ID_event == 1025:
                    x, y = event.pos
                    x = x // 80
                    y = y // 80
                    piece = self.gameBoard.board[y][x]
                    if piece.color == -1:
                        self.secretBlack = piece
                        pg.mixer.music.load(r"packageChess/sprites/steam-message.mp3")
                        pg.mixer.music.play()

    def setStart(self):
        self.mode = cntxMenu.startMenu()

        self.screen.fill("white")
        pg.display.set_caption("Chess")
        self.screen.blit(self.boardIMG, self.boardRect)

        pg.init()
        pg.mixer.music.load(r"packageChess/sprites/move-self.mp3")

        self.gameBoard = boardChess.Board()
        self.screen = pg.display.set_mode((640, 640))

        if self.mode == "random" or self.mode == "randomTimed":
            self.gameBoard.setRandomBoard()
        else:
            self.gameBoard.setStandardBoard()

        if self.mode == "secret" or self.mode == "secretTimed":
            self.updateStandartDesk()
            self.selectSecretPieces()

        self.timeOfLastTurn = dt.datetime.now()

    def pawnTransformation(self):
        if self.gameBoard.checkPawn():
            p = self.gameBoard.checkPawn()
            if p[1] == 0:
                self.gameBoard.transformPawn(cntxMenu.pawnTransormationWhite())
            else:
                self.gameBoard.transformPawn(cntxMenu.pawnTransormationBlack())
            self.screen = pg.display.set_mode((640, 640))
            self.screen.fill("white")
            pg.display.set_caption("Chess")

    def mainLoop(self):
        self.setStart()
        while self.loop:
            self.pawnTransformation()
            self.updateStandartDesk()
            if self.mode == "secretTimed" or self.mode == "secret":

                if self.gameBoard.checkForStalemateSecret():
                    self.loop = False
                    continue
                if self.gameBoard.board[self.secretWhite.y][self.secretWhite.x] != self.secretWhite:
                    self.gameBoard.boardState = 1
                    self.loop = False
                    continue
                if self.gameBoard.board[self.secretBlack.y][self.secretBlack.x] != self.secretBlack:
                    self.gameBoard.boardState = -1
                    self.loop = False
                    continue

                if self.mode[-5:] == "Timed" and self.runOutOfTime():
                    continue

                for event in pg.event.get():
                    ID_event = event.type
                    if ID_event == pg.QUIT:
                        exit()

                    if ID_event == 1025:
                        if self.gameBoard.notSelected:
                            x, y = event.pos
                            x = x // 80
                            y = y // 80
                            print(x + 1, 8 - y)
                            self.gameBoard.turns = self.gameBoard.selectPieceSecret(x, y)
                            self.gameBoard.notSelected = not (self.gameBoard.turns[0] or self.gameBoard.turns[1])
                            if not self.gameBoard.notSelected:
                                self.selectedPiece = (x, y)
                        else:
                            x, y = event.pos
                            click = (x // 80, y // 80)
                            if click in self.gameBoard.turns[0] or click in self.gameBoard.turns[1]:
                                if click in self.gameBoard.turns[0]:
                                    pg.mixer.music.load(r"packageChess/sprites/move-self.mp3")
                                else:
                                    pg.mixer.music.load(r"packageChess/sprites/move-check.mp3")
                                self.timeOfLastTurn = dt.datetime.now()
                                self.gameBoard.movePiece(self.selectedPiece[0], self.selectedPiece[1], click[0],
                                                         click[1])
                                pg.mixer.music.play()
                                self.gameBoard.turn *= -1

                            self.gameBoard.turns = []
                            self.gameBoard.notSelected = True
            else:
                if self.gameBoard.checkForMate() or self.gameBoard.checkForStalemate():
                    self.loop = False


                if self.mode[-5:] == "Timed" and self.runOutOfTime(): continue

                for event in pg.event.get():
                    ID_event = event.type

                    if ID_event == pg.QUIT:
                        exit()

                    if ID_event == 1025:
                        if self.gameBoard.notSelected:
                            x, y = event.pos
                            x = x // 80
                            y = y // 80
                            print(x + 1, 8 - y)
                            self.gameBoard.turns = self.gameBoard.selectPiece(x, y)
                            self.gameBoard.notSelected = not (
                                        len(self.gameBoard.turns[0]) or len(self.gameBoard.turns[1]))
                            if not self.gameBoard.notSelected:
                                self.selectedPiece = (x, y)
                        else:
                            x, y = event.pos
                            click = (x // 80, y // 80)
                            if click in self.gameBoard.turns[0] or click in self.gameBoard.turns[1]:
                                if click in self.gameBoard.turns[0]:
                                    pg.mixer.music.load(r"packageChess/sprites/move-self.mp3")
                                else:
                                    pg.mixer.music.load(r"packageChess/sprites/move-check.mp3")
                                self.gameBoard.movePiece(self.selectedPiece[0], self.selectedPiece[1], click[0],
                                                         click[1])
                                pg.mixer.music.play()
                                if self.gameBoard.checkCheck():
                                    pg.mixer.music.load(r"packageChess/sprites/steam-message.mp3")
                                    pg.mixer.music.play()
                                self.timeOfLastTurn = dt.datetime.now()
                                self.gameBoard.turn *= -1

                            self.gameBoard.turns = []
                            self.gameBoard.notSelected = True

            pg.display.flip()
        self.endOfGame()

    def updateStandartDesk(self):
        self.screen.blit(self.boardIMG, self.boardRect)
        for i in range(8):
            for j in range(8):
                pieceIMG = pg.image.load(r"packageChess/sprites/" + str(self.gameBoard.board[i][j]) + ".png")
                pieceRect = pieceIMG.get_rect(center=(40 + 80 * j, 40 + 80 * i))
                self.screen.blit(pieceIMG, pieceRect)
        if len(self.gameBoard.turns):
            for i in self.gameBoard.turns[0]:
                webImg = pg.image.load(r"packageChess/sprites/pos.png")
                webRec = webImg.get_rect(center=(40 + 80 * i[0], 40 + 80 * i[1]))
                self.screen.blit(webImg, webRec)
            for i in self.gameBoard.turns[1]:
                webImg = pg.image.load(r"packageChess/sprites/kill.png")
                webRec = webImg.get_rect(center=(40 + 80 * i[0], 40 + 80 * i[1]))
                self.screen.blit(webImg, webRec)

    def runOutOfTime(self):
        curTime = dt.datetime.now()
        if (curTime - self.timeOfLastTurn).total_seconds() > 15:
            pg.mixer.music.load(r"packageChess/sprites/clock.mp3")
            pg.mixer.music.play()
            if self.gameBoard.turn == 1 and self.gameBoard.whiteChecked:
                self.gameBoard.boardState = 1
                self.loop = False
            elif self.gameBoard.turn == -1 and self.gameBoard.blackChecked:
                self.gameBoard.boardState = -1
                self.loop = False
            self.gameBoard.turn *= -1
            self.gameBoard.turns = []
            self.gameBoard.notSelected = True
            self.timeOfLastTurn = dt.datetime.now()
            return True
        return False

    def standardLoop(self):
        if self.gameBoard.checkForMate() or self.gameBoard.checkForStalemate():
            self.loop = False
            return

        if self.mode[-5:] == "Timed" and self.runOutOfTime(): return

        for event in pg.event.get():
            ID_event = event.type

            if ID_event == pg.QUIT:
                exit()

            if ID_event == 1025:
                if self.gameBoard.notSelected:
                    x, y = event.pos
                    x = x // 80
                    y = y // 80
                    print(x + 1, 8 - y)
                    self.gameBoard.turns = self.gameBoard.selectPiece(x, y)
                    self.gameBoard.notSelected = not (len(self.gameBoard.turns[0]) or len(self.gameBoard.turns[1]))
                    if not self.gameBoard.notSelected:
                        self.selectedPiece = (x, y)
                else:
                    x, y = event.pos
                    click = (x // 80, y // 80)
                    if click in self.gameBoard.turns[0] or click in self.gameBoard.turns[1]:
                        if click in self.gameBoard.turns[0]:
                            pg.mixer.music.load(r"packageChess/sprites/move-self.mp3")
                        else:
                            pg.mixer.music.load(r"packageChess/sprites/move-check.mp3")
                        self.gameBoard.movePiece(self.selectedPiece[0], self.selectedPiece[1], click[0], click[1])
                        pg.mixer.music.play()
                        if self.gameBoard.checkCheck():
                            pg.mixer.music.load(r"packageChess/sprites/steam-message.mp3")
                            pg.mixer.music.play()
                        self.timeOfLastTurn = dt.datetime.now()
                        self.gameBoard.turn *= -1

                    self.gameBoard.turns = []
                    self.gameBoard.notSelected = True
            return True

    def secretLoop(self):

        if self.gameBoard.checkForStalemateSecret():
            self.loop = False
            return
        if self.gameBoard.board[self.secretWhite.y][self.secretWhite.x] != self.secretWhite:
            self.gameBoard.boardState = 1
            self.loop = False
            return
        if self.gameBoard.board[self.secretBlack.y][self.secretBlack.x] != self.secretBlack:
            self.gameBoard.boardState = -1
            self.loop = False
            return

        if self.mode[-5:] == "Timed" and self.runOutOfTime():
            return


        for event in pg.event.get():
            ID_event = event.type
            if ID_event == pg.QUIT:
                exit()

            if ID_event == 1025:
                if self.gameBoard.notSelected:
                    x, y = event.pos
                    x = x // 80
                    y = y // 80
                    print(x + 1, 8 - y)
                    self.gameBoard.turns = self.gameBoard.selectPieceSecret(x, y)
                    self.gameBoard.notSelected = not (self.gameBoard.turns[0] or self.gameBoard.turns[1])
                    if not self.gameBoard.notSelected:
                        self.selectedPiece = (x, y)
                else:
                    x, y = event.pos
                    click = (x // 80, y // 80)
                    if click in self.gameBoard.turns[0] or click in self.gameBoard.turns[1]:
                        if click in self.gameBoard.turns[0]:
                            pg.mixer.music.load(r"packageChess/sprites/move-self.mp3")
                        else:
                            pg.mixer.music.load(r"packageChess/sprites/move-check.mp3")
                        self.timeOfLastTurn = dt.datetime.now()
                        self.gameBoard.movePiece(self.selectedPiece[0], self.selectedPiece[1], click[0], click[1])
                        pg.mixer.music.play()
                        self.gameBoard.turn *= -1

                    self.gameBoard.turns = []
                    self.gameBoard.notSelected = True

    def endOfGame(self):
        pg.font.init()
        font = pg.font.Font(None, 36)

        if self.gameBoard.boardState == -1:
            text = font.render("Победа Белых", True, (255, 0, 0))
        elif self.gameBoard.boardState == 1:
            text = font.render("Победа Чёрных", True, (255, 0, 0))
        else:
            text = font.render("Пат", True, (255, 255, 255))

        place = text.get_rect(center=(320, 320))
        self.screen.blit(text, place)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            pg.display.flip()
