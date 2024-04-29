import copy

import trppChess.packageChess.piecesChess123 as pieces
import random as rn


class Board:
    boardState = 0
    height = 8
    width = 8

    blackChecked = False
    whiteChecked = False

    kingWhite = None
    kingBlack = None

    enPassant = ()

    turn = 1

    space = type(pieces.EmptySpace(0, 0))

    board = []

    turns = []
    notSelected = True

    def __init__(self):
        self.board = [[0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7],
                      [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7],
                      [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7]]
        for i in range(8):
            for j in range(8):
                self.board[i][j] = pieces.EmptySpace(i, j)

    def isStepOkay(self, x, y) -> True | False:
        if x >= self.height or y >= self.width or x < 0 or y < 0:
            return False
        if type(self.board[y][x]) == self.space:
            return True
            print((x, y))
        return False

    def isKillOkay(self, x, y, piece) -> True | False:
        if x >= self.height or y >= self.width or x < 0 or y < 0: return False
        pieceT = self.board[y][x]
        if isinstance(piece, pieces.Pawn) and len(self.enPassant) != 0:
            if x == self.enPassant[0] and y == self.enPassant[1] and piece.color == self.enPassant[2] * -1:
                return True
        if piece.color == pieceT.color * -1: return True
        return False

    def movePiece(self, xStart, yStart, xEnd, yEnd):
        piece = self.board[yStart][xStart]
        pieceT = self.board[yEnd][xEnd]
        self.board[yStart][xStart] = pieces.EmptySpace(xStart, yStart)
        self.board[yEnd][xEnd] = piece
        piece.move(xEnd, yEnd)
        piece.wasMoved = True
        if isinstance(piece, pieces.Pawn):
            if isinstance(pieceT, self.space):
                self.board[yStart][xEnd] = pieces.EmptySpace(xEnd, yStart)
            if abs(yStart - yEnd) == 2:
                self.enPassant = ((xStart + xEnd) / 2, (yStart + yEnd) / 2, piece.color)
            else:
                self.enPassant = ()
        else:
            self.enPassant = ()
        if isinstance(piece, pieces.King) and abs(xStart - xEnd) > 1:
            if self.turn == 1:
                self.board[yStart][int((xStart + xEnd) / 2)] = pieces.RookWhite(int((xStart + xEnd) / 2), yStart)
            else:
                self.board[yStart][int((xStart + xEnd) / 2)] = pieces.RookBlack(int((xStart + xEnd) / 2), yStart)
            if xStart > xEnd:
                self.board[yStart][0] = pieces.EmptySpace(0, yStart)
            else:
                self.board[yStart][7] = pieces.EmptySpace(7, yStart)
    def selectPiece(self, x, y) -> [[], []]:
        result = [[], []]
        if self.turn != self.board[y][x].color: return result
        return self.transformDir(x, y)



    def selectPieceSecret(self, x, y) -> [[], []]:
        result = [[], []]
        if self.turn != self.board[y][x].color: return result
        return self.transformDirForCheck(x, y)
    def checkForStalemateSecret(self) -> True | False:
        if self.whiteChecked or self.blackChecked:
            return False
        if self.turn == 1:
            for line in self.board:
                for piece in line:
                    if piece.color == -1 or piece.color == 0:
                        continue
                    else:
                        if len(self.transformDirForCheck(piece.x, piece.y)[0]) > 0 or len(self.transformDirForCheck(piece.x, piece.y)[1]) > 0:
                            return False
            return True
        else:
            for i in range(8):
                for j in range(8):
                    piece = self.board[i][j]
                    if piece.color == 1 or piece.color == 0: continue
                    else:
                        if len(self.transformDirForCheck(piece.x, piece.y)[0]) > 0 or len(self.transformDirForCheck(piece.x, piece.y)[1]) > 0:
                            return False
            return True




    def transformDirForCheck(self, x, y):
        result = [[], []]
        piece = self.board[y][x]
        dirs = piece.getDir()
        if isinstance(piece, pieces.Knight):
            for move in dirs:
                if self.isStepOkay(move[0], move[1]):
                    result[0].append(move)
                elif self.isKillOkay(move[0], move[1], piece):
                    result[1].append(move)
            return result
        if isinstance(piece, pieces.Pawn):
            for i in range(8):
                for move in dirs[i]:
                    if self.isStepOkay(move[0], move[1]) and i < 4:
                        result[0].append(move)
                    if self.isKillOkay(move[0], move[1], piece) and i > 3:
                        result[1].append(move)
            return result
        if isinstance(piece, pieces.King):
            if (len(dirs[2]) > 1 or len((dirs[3])) > 1) and not (self.blackChecked or self.whiteChecked):
                if isinstance(self.board[y][0], pieces.Rook) and not self.board[y][0].wasMoved:
                    if isinstance(self.board[y][1], self.space) and isinstance(self.board[y][2],
                                                                               self.space) and isinstance(
                        self.board[y][3], self.space):
                        result[0].append(dirs[2][1])
                if isinstance(self.board[y][7], pieces.Rook) and not self.board[y][7].wasMoved:
                    if isinstance(self.board[y][5], self.space) and isinstance(self.board[y][6], self.space):
                        result[0].append(dirs[3][1])
            for line in dirs:
                if self.isStepOkay(line[0][0], line[0][1]):
                    result[0].append(line[0])
                elif self.isKillOkay(line[0][0], line[0][1], piece):
                    result[1].append(line[0])
            return result

        # [[][][][][][][]]
        for line in dirs:
            for move in line:
                if self.isStepOkay(move[0], move[1]):
                    result[0].append(move)
                elif self.isKillOkay(move[0], move[1], piece):
                    result[1].append(move)
                    break
                else:
                    break
        return result
    def transformDir(self, x, y) -> [[], []]:
        result = [[], []]
        piece = self.board[y][x]
        dirs = piece.getDir()
        r1 = []
        r2 = []
        if isinstance(piece, pieces.Knight):
            for move in dirs:
                if self.isStepOkay(move[0], move[1]):
                    result[0].append(move)
                elif self.isKillOkay(move[0], move[1], piece):
                    result[1].append(move)
            for m in result[0]:
                if self.createNewTable(x, y, m[0], m[1]):
                    r1.append(m)
            for m in result[1]:
                if self.createNewTable(x, y, m[0], m[1]):
                    r2.append(m)
            result = [r1, r2]
            return result
        if isinstance(piece, pieces.Pawn):
            for i in range(8):
                for move in dirs[i]:
                    if self.isStepOkay(move[0], move[1]) and i < 4:
                        if abs(move[1] - y) == 1:
                            result[0].append(move)
                        else:
                            if isinstance(self.board[int((move[1] + y)/2)][x], pieces.EmptySpace):
                                result[0].append(move)
                    if self.isKillOkay(move[0], move[1], piece) and i > 3:
                        result[1].append(move)
            for m in result[0]:
                if self.createNewTable(x, y, m[0], m[1]):
                    r1.append(m)
            for m in result[1]:
                if self.createNewTable(x, y, m[0], m[1]):
                    r2.append(m)
            result = [r1, r2]
            return result
        if isinstance(piece, pieces.King):
            if (len(dirs[2]) > 1 or len((dirs[3])) > 1) and not (self.blackChecked or self.whiteChecked):
                if isinstance(self.board[y][0], pieces.Rook) and not self.board[y][0].wasMoved:
                    if isinstance(self.board[y][1], self.space) and isinstance(self.board[y][2],
                                                                               self.space) and isinstance(
                        self.board[y][3], self.space):
                        result[0].append(dirs[2][1])
                if isinstance(self.board[y][7], pieces.Rook) and not self.board[y][7].wasMoved:
                    if isinstance(self.board[y][5], self.space) and isinstance(self.board[y][6], self.space):
                        result[0].append(dirs[3][1])
            for line in dirs:
                if self.isStepOkay(line[0][0], line[0][1]):
                    result[0].append(line[0])
                elif self.isKillOkay(line[0][0], line[0][1], piece):
                    result[1].append(line[0])

            for m in result[0]:
                if self.createNewTable(x, y, m[0], m[1]):
                    r1.append(m)
            for k in result[1]:
                if self.createNewTable(x, y, k[0], k[1]):
                    r2.append(k)
            result = [r1, r2]
            return result

        # [[][][][][][][]]
        for line in dirs:
            for move in line:
                if self.isStepOkay(move[0], move[1]):
                    result[0].append(move)
                elif self.isKillOkay(move[0], move[1], piece):
                    result[1].append(move)
                    break
                else:
                    break
        for m in result[0]:
            if self.createNewTable(x, y, m[0], m[1]):
                r1.append(m)
        for k in result[1]:
            if self.createNewTable(x, y, k[0], k[1]):
                r2.append(k)
        result = [r1, r2]
        return result
    def checkCheck(self) -> True | False:
        whiteCords = (self.kingWhite.x, self.kingWhite.y)
        blackCords = (self.kingBlack.x, self.kingBlack.y)
        isChecked = False
        w, b = False, False
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                turns = self.transformDirForCheck(j, i)
                if whiteCords in turns[1]:
                    self.whiteChecked = True
                    w = True
                if blackCords in turns[1]:
                    self.blackChecked = True
                    b = True
        if not b:
            self.blackChecked = False
        if not w:
            self.whiteChecked = False
        return w or b
    def createNewTable(self, xStart, yStart, xEnd, yEnd) -> True | False:
        newBoard = Board()
        newBoard.board = copy.deepcopy(self.board)
        newBoard.movePiece(xStart, yStart, xEnd, yEnd)
        newBoard.turn = self.turn
        newBoard.kingWhite, newBoard.kingBlack = newBoard.getKingsCords()
        if newBoard.kingWhite is None or newBoard.kingBlack is None:
            print(1)
            return False
        newBoard.whiteChecked = self.whiteChecked
        newBoard.blackChecked = self.blackChecked
        ch = newBoard.checkCheck()
        if ch:
            if newBoard.turn == 1 and newBoard.whiteChecked:
                return False
            if newBoard.turn == -1 and newBoard.blackChecked:
                return False
        return True








    def checkForKings(self):
        cnt = 0
        for a in self.board:
            for b in a:
                if isinstance(b, pieces.King): cnt += 1
        if cnt < 2: exit(1)
    def checkPawn(self):
        for piece in self.board[0]:
            if isinstance(piece, pieces.PawnWhite):
                return (piece.x, piece.y)
        for piece in self.board[7]:
            if isinstance(piece, pieces.PawnBlack):
                return (piece.x, piece.y)
        return ()
    def transformPawn(self, pawn, a):
        pawn = self.checkPawn()
        if len(pawn) == 0: return
        x, y = pawn

        if a == "1q":
            self.board[y][x] = pieces.QueenWhite(x, y)
        if a == "-1q":
            self.board[y][x] = pieces.QueenBlack(x, y)

        if a == "1r":
            self.board[y][x] = pieces.RookWhite(x, y)
        if a == "-1r":
            self.board[y][x] = pieces.RookBlack(x, y)
        if a == "1k":
            self.board[y][x] = pieces.KnightWhiteWhite(x, y)
        if a == "-1k":
            self.board[y][x] = pieces.KnightBlackBlack(x, y)
        if a == "1b":
            self.board[y][x] = pieces.BishopWhiteWhite(x, y)
        if a == "-1b":
            self.board[y][x] = pieces.BishopBlack(x, y)
    def setStandardBoard(self):
        for i in range(8):
            for j in range(8):
                self.board[i][j] = pieces.EmptySpace(i, j)

        if self.width != 8 or self.height != 8:
            return
        self.board[0][0] = pieces.RookBlack(0, 0)
        self.board[0][1] = pieces.KnightBlack(1, 0)
        self.board[0][2] = pieces.BishopBlack(2, 0)
        self.board[0][3] = pieces.QueenBlack(3, 0)

        self.board[0][4] = pieces.KingBlack(4, 0)
        self.kingBlack = self.board[0][4]

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
        self.kingWhite = self.board[7][4]

        self.board[7][5] = pieces.BishopWhite(5, 7)
        self.board[7][6] = pieces.KnightWhite(6, 7)
        self.board[7][7] = pieces.RookWhite(7, 7)
        for i in range(8):
            self.board[6][i] = pieces.PawnWhite(i, 6)





    def setRandomBoard(self):
        c = True
        self.turn = rn.choice((1, -1))
        while c:
            self.whiteChecked = False
            self.blackChecked = False
            self.setStandardBoard()
            bufArr = []
            for i in self.board:
                for j in i:
                    bufArr.append(j)
            rn.shuffle(bufArr)
            for i in range(8):
                for j in range(8):
                    self.board[i][j] = bufArr[i * 8 + j]
                    self.board[i][j].move(j, i)
                    if isinstance(self.board[i][j], pieces.KingWhite): self.kingWhite = self.board[i][j]
                    if isinstance(self.board[i][j], pieces.KingBlack): self.kingBlack = self.board[i][j]
            self.randomTransform()
            c = self.checkCheck()
    def getRandomPice(self, color) -> pieces.Piece:
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
    def randomTransform(self):
        for j in range(8):
            if isinstance(self.board[0][j], pieces.PawnWhite):
                self.board[0][j] = self.getRandomPice(1)
                self.board[0][j].move(j, 0)
            if isinstance(self.board[7][j], pieces.PawnBlack):
                self.board[7][j] = self.getRandomPice(-1)
                self.board[7][j].move(j, 7)




    def getKingsCords(self):
        w = None
        b = None
        for line in self.board:
            for piece in line:
                if isinstance(piece, pieces.KingWhite): w = piece
                if isinstance(piece, pieces.KingBlack): b = piece
        return w, b


    def checkForMate(self) -> True | False:
        if not (self.whiteChecked or self.blackChecked):
            return False
        if self.whiteChecked:
            for line in self.board:
                for piece in line:
                    if piece.color == -1:
                        continue
                    else:
                        if len(self.transformDir(piece.x, piece.y)[0]) > 0 or len(self.transformDir(piece.x, piece.y)[1]) > 0:
                            return False
            self.boardState = 1
            return True
        else:
            for line in self.board:
                for piece in line:
                    if piece.color == 1: continue
                    else:
                        if len(self.transformDir(piece.x, piece.y)[0]) > 0 or len(self.transformDir(piece.x, piece.y)[1]) > 0:
                            return False
            self.boardState = -1
            return True

    def checkForStalemate(self) -> True | False:
        if self.whiteChecked or self.blackChecked:
            return False
        if self.turn == 1:
            for line in self.board:
                for piece in line:
                    if piece.color == -1 or piece.color == 0:
                        continue
                    else:
                        if len(self.transformDir(piece.x, piece.y)[0]) > 0 or len(self.transformDir(piece.x, piece.y)[1]) > 0:
                            return False
            return True
        else:
            for i in range(8):
                for j in range(8):
                    piece = self.board[i][j]
                    if piece.color == 1 or piece.color == 0: continue
                    else:
                        if len(self.transformDir(piece.x, piece.y)[0]) > 0 or len(self.transformDir(piece.x, piece.y)[1]) > 0:
                            return False
            return True
