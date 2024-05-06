import copy
import trppChess.packageChess.piecesChess123 as pieces
import random as rn

from trppChess.packageChess.piecesChess123 import KingWhite, KingBlack


class Board:
    board_state = 0
    height = 8
    width = 8

    black_checked = False
    white_checked = False

    king_white = None
    king_black = None

    enPassant = ()

    turn = 1

    space = type(pieces.EmptySpace(0, 0))

    board = []

    turns = []
    notSelected = True

    def __init__(self):
        self.board = [[pieces.EmptySpace(0, 0)] * 8, [pieces.EmptySpace(0, 0)] * 8,
                      [pieces.EmptySpace(0, 0)] *
                      8, [pieces.EmptySpace(0, 0)] * 8,
                      [pieces.EmptySpace(0, 0)] *
                      8, [pieces.EmptySpace(0, 0)] * 8,
                      [pieces.EmptySpace(0, 0)] * 8, [pieces.EmptySpace(0, 0)] * 8]
        for i in range(8):
            for j in range(8):
                self.board[i][j] = pieces.EmptySpace(i, j)

    def is_step_okay(self, x: int, y: int) -> bool:
        if x >= self.height or y >= self.width or x < 0 or y < 0:
            return False
        if type(self.board[y][x]) == self.space:
            return True
        return False

    def is_kill_okay(self, x: int, y: int, piece: pieces.Piece) -> bool:
        if x >= self.height or y >= self.width or x < 0 or y < 0:
            return False
        pieceT = self.board[y][x]
        if isinstance(piece, pieces.Pawn) and len(self.enPassant) != 0:
            if x == self.enPassant[0] and y == self.enPassant[1] and piece.color == self.enPassant[2] * -1:
                return True
        if piece.color == pieceT.color * -1:
            return True
        return False



    def check_check_levelup(self) -> bool:
        whiteCords = (self.king_white.x, self.king_white.y)
        blackCords = (self.king_black.x, self.king_black.y)
        w, b = False, False
        for i in range(8):
            for j in range(8):
                turns = self.transform_dir_for_check_levelup(j, i)
                if whiteCords in turns[1]:
                    self.white_checked = True
                    w = True
                if blackCords in turns[1]:
                    self.black_checked = True
                    b = True
        if not b:
            self.black_checked = False
        if not w:
            self.white_checked = False
        return w or b
    def move_piece_levelup(self, xStart: int, yStart: int, xEnd: int, yEnd: int) -> None:
        piece = self.board[yStart][xStart]
        pieceT = self.board[yEnd][xEnd]
        self.board[yStart][xStart] = pieces.EmptySpace(xStart, yStart)
        self.board[yEnd][xEnd] = piece
        piece.move(xEnd, yEnd)
        if not isinstance(pieceT, pieces.EmptySpace) and piece.color != pieceT.color:
            self.board[yEnd][xEnd] = piece.evolve()
        if isinstance(piece, pieces.PawnWhite) or isinstance(piece, pieces.PawnBlack):
            if isinstance(pieceT, self.space):
                self.board[yStart][xEnd] = pieces.EmptySpace(xEnd, yStart)
            if abs(yStart - yEnd) == 2:
                self.enPassant = ((xStart + xEnd) / 2,
                                  (yStart + yEnd) / 2, piece.color)
            else:
                self.enPassant = ()
        else:
            self.enPassant = ()
        if isinstance(piece, pieces.King) and abs(xStart - xEnd) > 1 and ((yStart == 0 or yStart == 7) and xStart == 4):
            if self.turn == 1:
                self.board[yStart][(
                                           xStart + xEnd) // 2] = pieces.RookWhite((xStart + xEnd) // 2, yStart)
            else:
                self.board[yStart][(
                                           xStart + xEnd) // 2] = pieces.RookBlack((xStart + xEnd) // 2, yStart)
            if xStart > xEnd:
                self.board[yStart][0] = pieces.EmptySpace(0, yStart)
            else:
                self.board[yStart][7] = pieces.EmptySpace(7, yStart)
        piece.wasMoved = True


    def transform_dir_levelup(self, x: int, y: int) -> list[list[tuple[int]]]:
        """
        :param x: position x
        :param y: position y
        :return: [list of normal moves, list of attack moves]
        """
        result = self.transform_dir_for_check_levelup(x, y)

        r1 = [p for p in result[0] if self.create_new_table_levelup(x, y, p[0], p[1])]
        r2 = [p for p in result[1] if self.create_new_table_levelup(x, y, p[0], p[1])]
        return [r1, r2]

    def transform_dir_for_check_levelup(self, x: int, y: int) -> list[list[tuple[int]]]:
        """
        Doesn't check if your king can move to attacked position.
        :param x: position x
        :param y: position y
        :return: [list of normal moves, list of attack moves]
        """
        result = [[], []]
        piece = self.board[y][x]
        dirs = piece.getDir()
        if isinstance(piece, pieces.PawnWhite) or isinstance(piece, pieces.PawnBlack):
            for i in range(8):
                for move in dirs[i]:
                    if self.is_step_okay(move[0], move[1]) and i < 4:
                        if abs(move[1] - y) == 1:
                            result[0].append(move)
                        else:
                            if isinstance(self.board[int((move[1] + y) / 2)][x], pieces.EmptySpace):
                                result[0].append(move)
                    if self.is_kill_okay(move[0], move[1], piece) and i > 3:
                        result[1].append(move)
        elif isinstance(piece, pieces.King):
            if (len(dirs[2]) > 1 or len((dirs[3])) > 1) and\
                    not (self.black_checked or self.white_checked) and \
                    ((y == 0 or y == 7) and x == 4) :
                if isinstance(self.board[y][0], pieces.Rook) and not self.board[y][0].wasMoved:
                    if isinstance(self.board[y][1], self.space) and isinstance(self.board[y][2],
                                                                               self.space) and isinstance(
                            self.board[y][3], self.space):
                        result[0].append(dirs[2][1])
                if isinstance(self.board[y][7], pieces.Rook) and not self.board[y][7].wasMoved:
                    if isinstance(self.board[y][5], self.space) and isinstance(self.board[y][6], self.space):
                        result[0].append(dirs[3][1])
            for line in dirs:
                for move in line:
                    if self.is_step_okay(move[0], move[1]):
                        result[0].append(move)
                    elif self.is_kill_okay(move[0], move[1], piece):
                        result[1].append(move)
                        break
                    else:
                        break
        elif isinstance(piece, pieces.Rook) and piece.level > 1:
            result = self.transform_dir_rook(piece)

        # [[][][][][][][]]
        else:
            for line in dirs:
                for move in line:
                    if self.is_step_okay(move[0], move[1]):
                        result[0].append(move)
                    elif self.is_kill_okay(move[0], move[1], piece):
                        result[1].append(move)
                        break
                    else:
                        break

        return result

    def create_new_table_levelup(self, xStart: int, yStart: int, xEnd: int, yEnd: int) -> bool:
        """
        Will your king be not checked after move
        :param xStart: from x
        :param yStart: from y
        :param xEnd: to x
        :param yEnd: to y
        :return: True if turn okay
        """
        newBoard = Board()
        newBoard.board = copy.deepcopy(self.board)
        newBoard.turn = self.turn
        newBoard.move_piece_levelup(xStart, yStart, xEnd, yEnd)
        newBoard.king_white, newBoard.king_black = newBoard.get_kings_cords()
        if newBoard.king_white is None or newBoard.king_black is None:
            return False
        newBoard.white_checked = self.white_checked
        newBoard.black_checked = self.black_checked
        ch = newBoard.check_check_levelup()
        if ch:
            if newBoard.turn == 1 and newBoard.white_checked:
                return False
            if newBoard.turn == -1 and newBoard.black_checked:
                return False
        return True

    def transform_dir_rook(self, piece) -> list:
        result = [[], []]
        dirs = piece.getDir()
        if piece.level == 1:
            for line in dirs:
                for move in line:
                    if self.is_step_okay(move[0], move[1]):
                        result[0].append(move)
                    elif self.is_kill_okay(move[0], move[1], piece):
                        result[1].append(move)
                        break
                    else:
                        break
        elif piece.level == 2:
            for line in dirs:
                for move in line:
                    if self.is_step_okay(move[0], move[1]):
                        result[0].append(move)
                        continue
                    elif self.is_kill_okay(move[0], move[1], piece):
                        result[1].append(move)
                    if self.is_step_okay(move[0] + 1, move[1]):
                        result[0].append((move[0] + 1, move[1]))
                    elif self.is_kill_okay(move[0] + 1, move[1], piece):
                        result[1].append((move[0] + 1, move[1]))
                    if self.is_step_okay(move[0] - 1, move[1]):
                        result[0].append((move[0] - 1, move[1]))
                    elif self.is_kill_okay(move[0] - 1, move[1], piece):
                        result[1].append((move[0] - 1, move[1]))
                    if self.is_step_okay(move[0] + 1, move[1] + 1):
                        result[0].append((move[0] + 1, move[1] + 1))
                    elif self.is_kill_okay(move[0] + 1, move[1] + 1, piece):
                        result[1].append((move[0] + 1, move[1] + 1))
                    if self.is_step_okay(move[0] + 1, move[1] - 1):
                        result[0].append((move[0] + 1, move[1] - 1))
                    elif self.is_kill_okay(move[0] + 1, move[1] - 1, piece):
                        result[1].append((move[0] + 1, move[1] - 1))
                    break
        else:
            for line in dirs:
                for move in line:
                    if self.is_step_okay(move[0], move[1]):
                        result[0].append(move)
                    elif self.is_kill_okay(move[0], move[1], piece):
                        result[1].append(move)
                        break
                    else:
                        if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                            if self.board[move[1]][move[0]].color == piece.color:
                                result.append(move)
                        break
        return result

    def select_piece_levelup(self, x: int, y: int) -> list[list[tuple[int]]]:
        """
        :param x: position x
        :param y: position y
        :return: [list of normal moves, list of attack moves]
        """
        result = [[], []]
        if self.turn != self.board[y][x].color:
            return result
        return self.transform_dir_levelup(x, y)

    def check_for_mate_levelup(self) -> bool:
        if not (self.white_checked or self.black_checked):
            return False
        if self.white_checked:
            for line in self.board:
                for piece in line:
                    if piece.color == -1:
                        continue
                    else:
                        if self.transform_dir_levelup(piece.x, piece.y)[0] or\
                                self.transform_dir_levelup(piece.x, piece.y)[1]:
                            return False
            self.board_state = 1
            return True
        else:
            for line in self.board:
                for piece in line:
                    if piece.color == 1:
                        continue
                    else:
                        if self.transform_dir_levelup(piece.x, piece.y)[0] or\
                                self.transform_dir_levelup(piece.x, piece.y)[1]:
                            return False
            self.board_state = -1
            return True

    def check_for_stalemate_levelup(self) -> bool:
        if self.white_checked or self.black_checked:
            return False
        if self.turn == 1:
            for line in self.board:
                for piece in line:
                    if piece.color == -1 or piece.color == 0:
                        continue
                    else:
                        if self.transform_dir_levelup(piece.x, piece.y)[0] or\
                                self.transform_dir_levelup(piece.x, piece.y)[1]:
                            return False
            return True
        else:
            for i in range(8):
                for j in range(8):
                    piece = self.board[i][j]
                    if piece.color == 1 or piece.color == 0:
                        continue
                    else:
                        if self.transform_dir_levelup(piece.x, piece.y)[0] or\
                                self.transform_dir_levelup(piece.x, piece.y)[1]:
                            return False
            return True




    def move_piece(self, xStart: int, yStart: int, xEnd: int, yEnd: int) -> None:
        piece = self.board[yStart][xStart]
        pieceT = self.board[yEnd][xEnd]
        self.board[yStart][xStart] = pieces.EmptySpace(xStart, yStart)
        self.board[yEnd][xEnd] = piece
        piece.move(xEnd, yEnd)
        piece.wasMoved = True

        if isinstance(piece, pieces.PawnWhite) or isinstance(piece, pieces.PawnBlack):
            if isinstance(pieceT, self.space):
                self.board[yStart][xEnd] = pieces.EmptySpace(xEnd, yStart)
            if abs(yStart - yEnd) == 2:
                self.enPassant = ((xStart + xEnd) / 2,
                                  (yStart + yEnd) / 2, piece.color)
            else:
                self.enPassant = ()
        else:
            self.enPassant = ()
        if isinstance(piece, pieces.King) and abs(xStart - xEnd) > 1:
            if self.turn == 1:
                self.board[yStart][(
                                           xStart + xEnd) // 2] = pieces.RookWhite((xStart + xEnd) // 2, yStart)
            else:
                self.board[yStart][(
                                           xStart + xEnd) // 2] = pieces.RookBlack((xStart + xEnd) // 2, yStart)
            if xStart > xEnd:
                self.board[yStart][0] = pieces.EmptySpace(0, yStart)
            else:
                self.board[yStart][7] = pieces.EmptySpace(7, yStart)
        if isinstance(piece, pieces.Rook) and piece.level == 3 and piece.color == pieceT.color:
            self.board[yStart][xStart] = pieceT
    def select_piece(self, x: int, y: int) -> list[list[tuple[int]]]:
        """
        :param x: position x
        :param y: position y
        :return: [list of normal moves, list of attack moves]
        """
        result = [[], []]
        if self.turn != self.board[y][x].color:
            return result
        return self.transform_dir(x, y)

    def select_piece_secret(self, x: int, y: int) -> list[list[tuple[int]]]:
        """
        :param x: position x
        :param y: position y
        :return: [list of normal moves, list of attack moves]
        """
        result = [[], []]
        if self.turn != self.board[y][x].color:
            return result
        return self.transform_dir_for_check(x, y)

    def check_for_stalemate_secret(self) -> bool:
        if self.white_checked or self.black_checked:
            return False
        if self.turn == 1:
            for line in self.board:
                for piece in line:
                    if piece.color == -1 or piece.color == 0:
                        continue
                    else:
                        if len(self.transform_dir_for_check(piece.x, piece.y)[0]) > 0 or len(
                                self.transform_dir_for_check(piece.x, piece.y)[1]) > 0:
                            return False
            return True
        else:
            for i in range(8):
                for j in range(8):
                    piece = self.board[i][j]
                    if piece.color == 1 or piece.color == 0:
                        continue
                    else:
                        if len(self.transform_dir_for_check(piece.x, piece.y)[0]) > 0 or len(
                                self.transform_dir_for_check(piece.x, piece.y)[1]) > 0:
                            return False
            return True

    def transform_dir_for_check(self, x: int, y: int) -> list[list[tuple[int]]]:
        """
        Doesn't check if your king can move to attacked position.
        :param x: position x
        :param y: position y
        :return: [list of normal moves, list of attack moves]
        """
        result = [[], []]
        piece = self.board[y][x]
        dirs = piece.getDir()
        if isinstance(piece, pieces.PawnWhite) or isinstance(piece, pieces.PawnBlack):
            for i in range(8):
                for move in dirs[i]:
                    if self.is_step_okay(move[0], move[1]) and i < 4:
                        if abs(move[1] - y) == 1:
                            result[0].append(move)
                        else:
                            if isinstance(self.board[int((move[1] + y) / 2)][x], pieces.EmptySpace):
                                result[0].append(move)
                    if self.is_kill_okay(move[0], move[1], piece) and i > 3:
                        result[1].append(move)
        elif isinstance(piece, pieces.King):
            if (len(dirs[2]) > 1 or len((dirs[3])) > 1) and not (self.black_checked or self.white_checked):
                if isinstance(self.board[y][0], pieces.Rook) and not self.board[y][0].wasMoved:
                    if isinstance(self.board[y][1], self.space) and isinstance(self.board[y][2],
                                                                               self.space) and isinstance(
                            self.board[y][3], self.space):
                        result[0].append(dirs[2][1])
                if isinstance(self.board[y][7], pieces.Rook) and not self.board[y][7].wasMoved:
                    if isinstance(self.board[y][5], self.space) and isinstance(self.board[y][6], self.space):
                        result[0].append(dirs[3][1])

            for line in dirs:
                if self.is_step_okay(line[0][0], line[0][1]):
                    result[0].append(line[0])
                elif self.is_kill_okay(line[0][0], line[0][1], piece):
                    result[1].append(line[0])

        # [[][][][][][][]]
        else:
            for line in dirs:
                for move in line:
                    if self.is_step_okay(move[0], move[1]):
                        result[0].append(move)
                    elif self.is_kill_okay(move[0], move[1], piece):
                        result[1].append(move)
                        break
                    else:
                        break

        return result

    def transform_dir(self, x: int, y: int) -> list[list[tuple[int]]]:
        """
        :param x: position x
        :param y: position y
        :return: [list of normal moves, list of attack moves]
        """
        result = self.transform_dir_for_check(x, y)

        r1 = [p for p in result[0] if self.create_new_table(x, y, p[0], p[1])]
        r2 = [p for p in result[1] if self.create_new_table(x, y, p[0], p[1])]
        return [r1, r2]


    def check_check(self) -> bool:
        whiteCords = (self.king_white.x, self.king_white.y)
        blackCords = (self.king_black.x, self.king_black.y)
        w, b = False, False
        for i in range(8):
            for j in range(8):
                turns = self.transform_dir_for_check(j, i)
                if whiteCords in turns[1]:
                    self.white_checked = True
                    w = True
                if blackCords in turns[1]:
                    self.black_checked = True
                    b = True
        if not b:
            self.black_checked = False
        if not w:
            self.white_checked = False
        return w or b

    def create_new_table(self, xStart: int, yStart: int, xEnd: int, yEnd: int) -> bool:
        """
        Will your king be not checked after move
        :param xStart: from x
        :param yStart: from y
        :param xEnd: to x
        :param yEnd: to y
        :return: True if turn okay
        """
        newBoard = Board()
        newBoard.board = copy.deepcopy(self.board)
        newBoard.turn = self.turn
        newBoard.move_piece(xStart, yStart, xEnd, yEnd)
        newBoard.king_white, newBoard.king_black = newBoard.get_kings_cords()
        if newBoard.king_white is None or newBoard.king_black is None:
            return False
        newBoard.white_checked = self.white_checked
        newBoard.black_checked = self.black_checked
        ch = newBoard.check_check()
        if ch:
            if newBoard.turn == 1 and newBoard.white_checked:
                return False
            if newBoard.turn == -1 and newBoard.black_checked:
                return False
        return True

    def check_pawn(self) -> tuple:
        """
        :return: cords of pawn to transform (x, y) | empty tuple
        """
        for piece in self.board[0]:
            if isinstance(piece, pieces.PawnWhite):
                return piece.x, piece.y
        for piece in self.board[7]:
            if isinstance(piece, pieces.PawnBlack):
                return piece.x, piece.y
        return ()

    def transform_pawn(self, piece: str) -> None:
        """
        :param piece: string representation of piece
        """
        pawn = self.check_pawn()
        if len(pawn) == 0:
            return
        x, y = pawn

        if piece == "1q":
            self.board[y][x] = pieces.QueenWhite(x, y)
        elif piece == "-1q":
            self.board[y][x] = pieces.QueenBlack(x, y)
        elif piece == "1r":
            self.board[y][x] = pieces.RookWhite(x, y)
        elif piece == "-1r":
            self.board[y][x] = pieces.RookBlack(x, y)
        elif piece == "1k":
            self.board[y][x] = pieces.KnightWhite(x, y)
        elif piece == "-1k":
            self.board[y][x] = pieces.KnightBlack(x, y)
        elif piece == "1b":
            self.board[y][x] = pieces.BishopWhite(x, y)
        elif piece == "-1b":
            self.board[y][x] = pieces.BishopBlack(x, y)

    def set_standard_board(self) -> None:
        for i in range(2, 6):
            for j in range(8):
                self.board[i][j] = pieces.EmptySpace(i, j)

        if self.width != 8 or self.height != 8:
            return
        self.board[0][0] = pieces.RookBlack(0, 0)
        self.board[0][1] = pieces.KnightBlack(1, 0)
        self.board[0][2] = pieces.BishopBlack(2, 0)
        self.board[0][3] = pieces.QueenBlack(3, 0)

        self.board[0][4] = pieces.KingBlack(4, 0)
        self.king_black = self.board[0][4]

        self.board[0][5] = pieces.BishopBlack(5, 0)
        self.board[0][6] = pieces.KnightBlack(6, 0)
        self.board[0][7] = pieces.RookBlack(7, 0)
        for i in range(8):
            self.board[1][i] = pieces.PawnBlack(i, 1)

        self.board[7][0] = pieces.RookWhite(0, 7)
        self.board[7][1] = pieces.KnightWhite(1, 7)
        self.board[7][2] = pieces.BishopWhite(2, 7)
        self.board[7][3] = pieces.QueenWhite(3, 7)

        self.board[7][4] = pieces.KingWhite(4, 7)
        self.king_white = self.board[7][4]

        self.board[7][5] = pieces.BishopWhite(5, 7)
        self.board[7][6] = pieces.KnightWhite(6, 7)
        self.board[7][7] = pieces.RookWhite(7, 7)
        for i in range(8):
            self.board[6][i] = pieces.PawnWhite(i, 6)

    def set_random_board(self) -> None:
        """
        Set random cords of standard set of pieces, transform pawns, repeat until kings are not checked
        """
        c = True
        self.turn = rn.choice((1, -1))
        while c:
            self.white_checked = False
            self.black_checked = False
            self.set_standard_board()
            bufArr = []
            for i in self.board:
                for j in i:
                    bufArr.append(j)
            rn.shuffle(bufArr)
            for i in range(8):
                for j in range(8):
                    self.board[i][j] = bufArr[i * 8 + j]
                    self.board[i][j].move(j, i)
                    if isinstance(self.board[i][j], pieces.KingWhite):
                        self.king_white = self.board[i][j]
                    if isinstance(self.board[i][j], pieces.KingBlack):
                        self.king_black = self.board[i][j]
            self.random_transform()
            c = self.check_check()

    def get_random_piece(self, color: int) -> pieces.Piece:
        """
        :param color: color of piece
        :return: Knight, Rook, Bishop or Queen piece object for pawn transformation
        """
        c = rn.randint(1, 4)
        if c == 4:
            if color == 1:
                return pieces.RookWhite(0, 0)
            else:
                return pieces.RookBlack(0, 0)
        elif c == 1:
            if color == 1:
                return pieces.KnightWhite(0, 0)
            else:
                return pieces.KnightBlack(0, 0)
        elif c == 2:
            if color == 1:
                return pieces.BishopWhite(0, 0)
            else:
                return pieces.BishopBlack(0, 0)
        elif c == 3:
            if color == 1:
                return pieces.QueenWhite(0, 0)
            else:
                return pieces.QueenBlack(0, 0)

    def random_transform(self) -> None:
        for j in range(8):
            if isinstance(self.board[0][j], pieces.PawnWhite):
                self.board[0][j] = self.get_random_piece(1)
                self.board[0][j].move(j, 0)
            if isinstance(self.board[7][j], pieces.PawnBlack):
                self.board[7][j] = self.get_random_piece(-1)
                self.board[7][j].move(j, 7)

    def get_kings_cords(self) -> tuple[KingWhite | None, KingBlack | None]:
        """
        :return: tuple(white king object, black king object)
        """
        w = None
        b = None
        for line in self.board:
            for piece in line:
                if isinstance(piece, pieces.King):
                    if piece.color == 1:
                        w = piece
                    else:
                        b = piece
        return w, b

    def check_for_mate(self) -> bool:
        if not (self.white_checked or self.black_checked):
            return False
        if self.white_checked:
            for line in self.board:
                for piece in line:
                    if piece.color == -1:
                        continue
                    else:
                        if len(self.transform_dir(piece.x, piece.y)[0]) > 0 or len(
                                self.transform_dir(piece.x, piece.y)[1]) > 0:
                            return False
            self.board_state = 1
            return True
        else:
            for line in self.board:
                for piece in line:
                    if piece.color == 1:
                        continue
                    else:
                        if len(self.transform_dir(piece.x, piece.y)[0]) > 0 or len(
                                self.transform_dir(piece.x, piece.y)[1]) > 0:
                            return False
            self.board_state = -1
            return True

    def check_for_stalemate(self) -> bool:
        if self.white_checked or self.black_checked:
            return False
        if self.turn == 1:
            for line in self.board:
                for piece in line:
                    if piece.color == -1 or piece.color == 0:
                        continue
                    else:
                        if len(self.transform_dir(piece.x, piece.y)[0]) > 0 or len(
                                self.transform_dir(piece.x, piece.y)[1]) > 0:
                            return False
            return True
        else:
            for i in range(8):
                for j in range(8):
                    piece = self.board[i][j]
                    if piece.color == 1 or piece.color == 0:
                        continue
                    else:
                        if len(self.transform_dir(piece.x, piece.y)[0]) > 0 or len(
                                self.transform_dir(piece.x, piece.y)[1]) > 0:
                            return False
            return True
