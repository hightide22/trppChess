import pygame as pg
import trppChess.packageChess.boardChess123 as boardChess
import trppChess.packageChess.contextMenus as menu
import datetime as dt


class Gui:

    def __init__(self):
        self.screen = pg.display.set_mode((640, 640))

        self.loop = True

        self.mode = "standard"

        self.game_board = None

        self.secret_white = None
        self.secret_black = None

        self.timeOfLastTurn = None
        self.time_limit = 15
        self.boardIMG = pg.image.load(r"packageChess/sprites/chessBoard.jpg")
        self.boardRect = self.boardIMG.get_rect(bottomright=(640, 640))

        self.selected_piece = None

    def select_secret_pieces(self) -> None:
        """
        Whites and Blacks each-one select a piece, losing in results in game-lose
        :return: None
        """
        while self.secret_white is None:
            pg.display.flip()
            for event in pg.event.get():
                ID_event = event.type
                if ID_event == pg.QUIT:
                    exit()
                if ID_event == 1025:
                    x, y = event.pos
                    x = x // 80
                    y = y // 80
                    piece = self.game_board.board[y][x]
                    if piece.color == 1:
                        self.secret_white = piece
                        pg.mixer.music.load(
                            r"packageChess/sprites/steam-message.mp3")
                        pg.mixer.music.play()
        while self.secret_black is None:
            pg.display.flip()
            for event in pg.event.get():
                ID_event = event.type
                if ID_event == pg.QUIT:
                    exit()
                if ID_event == 1025:
                    x, y = event.pos
                    x = x // 80
                    y = y // 80
                    piece = self.game_board.board[y][x]
                    if piece.color == -1:
                        self.secret_black = piece
                        pg.mixer.music.load(
                            r"packageChess/sprites/steam-message.mp3")
                        pg.mixer.music.play()

    def set_start(self) -> None:
        """
        Mode, secret piece window initiation
        """
        self.mode = menu.start_menu()

        self.screen.fill("white")
        pg.display.set_caption("Chess")
        self.screen.blit(self.boardIMG, self.boardRect)

        pg.init()
        pg.mixer.music.load(r"packageChess/sprites/move-self.mp3")

        self.game_board = boardChess.Board()
        self.screen = pg.display.set_mode((640, 640))

        if self.mode == "random" or self.mode == "randomTimed":
            self.game_board.set_random_board()
        else:
            self.game_board.set_standard_board()

        if self.mode == "secret" or self.mode == "secretTimed":
            self.update_standard_desk()
            self.select_secret_pieces()

        self.timeOfLastTurn = dt.datetime.now()

    def pawn_transformation(self) -> None:
        if self.game_board.check_pawn():
            p = self.game_board.check_pawn()
            if p[1] == 0:
                self.game_board.transform_pawn(
                    menu.pawn_transformation_white())
            else:
                self.game_board.transform_pawn(
                    menu.pawn_transformation_black())
            self.screen = pg.display.set_mode((640, 640))
            self.screen.fill("white")
            pg.display.set_caption("Chess")

    def run(self) -> None:
        """
        main method of Object
        """
        print(1)
        self.set_start()
        al = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        while self.loop:
            self.pawn_transformation()
            self.update_standard_desk()
            if self.mode == "secretTimed" or self.mode == "secret":

                if self.game_board.check_for_stalemate_secret():
                    self.loop = False
                    continue
                if self.game_board.board[self.secret_white.y][self.secret_white.x] != self.secret_white:
                    self.game_board.board_state = 1
                    self.loop = False
                    continue
                if self.game_board.board[self.secret_black.y][self.secret_black.x] != self.secret_black:
                    self.game_board.board_state = -1
                    self.loop = False
                    continue

                if self.mode[-5:] == "Timed" and self.run_out_of_time():
                    continue

                for event in pg.event.get():
                    ID_event = event.type
                    if ID_event == pg.QUIT:
                        exit()

                    if ID_event == 1025:
                        if self.game_board.notSelected:
                            x, y = event.pos
                            x = x // 80
                            y = y // 80
                            self.game_board.turns = self.game_board.select_piece_secret(
                                x, y)
                            self.game_board.notSelected = not (
                                    self.game_board.turns[0] or self.game_board.turns[1])
                            if not self.game_board.notSelected:
                                self.selected_piece = (x, y)
                        else:
                            x, y = event.pos
                            click = (x // 80, y // 80)
                            if click in self.game_board.turns[0] or click in self.game_board.turns[1]:
                                if click in self.game_board.turns[0]:
                                    pg.mixer.music.load(
                                        r"packageChess/sprites/move-self.mp3")
                                else:
                                    pg.mixer.music.load(
                                        r"packageChess/sprites/move-check.mp3")
                                self.timeOfLastTurn = dt.datetime.now()
                                self.game_board.move_piece(self.selected_piece[0], self.selected_piece[1], click[0],
                                                           click[1])
                                pg.mixer.music.play()
                                self.game_board.turn *= -1
                                print(al[self.selected_piece[0]], 8 -
                                      self.selected_piece[1], "-->", al[x], 8 - y, )
                            self.game_board.turns = []
                            self.game_board.notSelected = True
            else:
                if (self.mode[:7] != "levelup") and (self.game_board.check_for_mate()
                                                     or self.game_board.check_for_stalemate()):
                    self.loop = False
                    print(1)
                    break
                if (self.mode[:7] == "levelup") and (self.game_board.check_for_mate_levelup()
                                                     or self.game_board.check_for_stalemate_levelup()):
                    self.loop = False
                    print(1)
                    break

                if self.mode[-5:] == "Timed" and self.run_out_of_time():
                    continue

                for event in pg.event.get():
                    ID_event = event.type

                    if ID_event == pg.QUIT:
                        exit()

                    if ID_event == 1025:
                        if self.game_board.notSelected:
                            x, y = event.pos
                            x //= 80
                            y //= 80
                            if self.mode == "levelup" or self.mode == "levelupTimed":
                                self.game_board.turns = self.game_board.select_piece_levelup(
                                    x, y)
                            else:
                                self.game_board.turns = self.game_board.select_piece(
                                    x, y)
                            self.game_board.notSelected = not (
                                    len(self.game_board.turns[0]) or len(self.game_board.turns[1]))
                            if not self.game_board.notSelected:
                                self.selected_piece = (x, y)
                        else:
                            x, y = event.pos
                            click = (x // 80, y // 80)
                            if click in self.game_board.turns[0] or click in self.game_board.turns[1]:
                                if click in self.game_board.turns[0]:
                                    pg.mixer.music.load(
                                        r"packageChess/sprites/move-self.mp3")
                                else:
                                    pg.mixer.music.load(
                                        r"packageChess/sprites/move-check.mp3")
                                if self.mode == "levelup" or self.mode == "levelupTimed":
                                    self.game_board.move_piece_levelup(self.selected_piece[0],
                                                                       self.selected_piece[1], click[0], click[1])
                                else:
                                    self.game_board.move_piece(self.selected_piece[0], self.selected_piece[1], click[0],
                                                               click[1])
                                pg.mixer.music.play()
                                if self.game_board.check_check():
                                    pg.mixer.music.load(
                                        r"packageChess/sprites/steam-message.mp3")
                                    pg.mixer.music.play()
                                print(
                                    al[self.selected_piece[0]], 8 - self.selected_piece[1],
                                    "-->", al[x // 80], 8 - y // 80, )
                                self.timeOfLastTurn = dt.datetime.now()
                                self.game_board.turn *= -1

                            self.game_board.turns = []
                            self.game_board.notSelected = True

            pg.display.flip()
        self.end_of_game()

    def update_standard_desk(self) -> None:
        """
        Draw board, pieces, move squares
        :return:
        """
        self.screen.blit(self.boardIMG, self.boardRect)
        for i in range(8):
            for j in range(8):
                pieceIMG = pg.image.load(
                    r"packageChess/sprites/" + str(self.game_board.board[i][j]) + ".png")
                pieceRect = pieceIMG.get_rect(
                    center=(40 + 80 * j, 40 + 80 * i))
                self.screen.blit(pieceIMG, pieceRect)
                if self.game_board.board[i][j].level == 2:
                    pieceIMG = pg.image.load(
                        r"packageChess/sprites/" + "level2" + ".png")
                    pieceRect = pieceIMG.get_rect(
                        center=(40 + 80 * j, 40 + 80 * i))
                    self.screen.blit(pieceIMG, pieceRect)
                elif self.game_board.board[i][j].level == 3:
                    pieceIMG = pg.image.load(
                        r"packageChess/sprites/" + "level3" + ".png")
                    pieceRect = pieceIMG.get_rect(
                        center=(40 + 80 * j, 40 + 80 * i))
                    self.screen.blit(pieceIMG, pieceRect)
        if len(self.game_board.turns):
            for i in self.game_board.turns[0]:
                webImg = pg.image.load(r"packageChess/sprites/pos.png")
                webRec = webImg.get_rect(
                    center=(40 + 80 * i[0], 40 + 80 * i[1]))
                self.screen.blit(webImg, webRec)
            for i in self.game_board.turns[1]:
                webImg = pg.image.load(r"packageChess/sprites/kill.png")
                webRec = webImg.get_rect(
                    center=(40 + 80 * i[0], 40 + 80 * i[1]))
                self.screen.blit(webImg, webRec)

    def run_out_of_time(self) -> bool:
        """
        Switch turn, empty possible moves, mate uf checked
        :return: True if run of time
        """
        curTime = dt.datetime.now()
        if (curTime - self.timeOfLastTurn).total_seconds() > self.time_limit:
            pg.mixer.music.load(r"packageChess/sprites/clock.mp3")
            pg.mixer.music.play()
            if self.game_board.turn == 1 and self.game_board.white_checked:
                self.game_board.board_state = 1
                self.loop = False
            elif self.game_board.turn == -1 and self.game_board.black_checked:
                self.game_board.board_state = -1
                self.loop = False
            self.game_board.turn *= -1
            self.game_board.turns = []
            self.game_board.notSelected = True
            self.timeOfLastTurn = dt.datetime.now()
            return True
        return False

    def end_of_game(self) -> None:
        pg.font.init()
        font = pg.font.Font(None, 36)

        if self.game_board.board_state == -1:
            text = font.render("Победа Белых", True, (255, 0, 0))
        elif self.game_board.board_state == 1:
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
