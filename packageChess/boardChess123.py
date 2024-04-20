import trppChess.packageChess.piecesChess123 as pieces


class Board:
    height = 8
    width = 8

    blackChecked = False
    whiteChecked = False

    kingWhite = None
    kingBlack = None

    turn = 1

    space = type(pieces.EmptySpace(0, 0))

    board = []

    def __init__(self):
        self.board = [[0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7]]
        for i in range(8):
           for j in range(8):
               self.board[i][j] = pieces.EmptySpace(i, j)
    def isStepOkay(self, x, y) -> True | False:
        if x >= self.height or y >= self.width or x < 0 or y < 0: return False
        if type(self.board[y][x]) == self.space:
            return True
        return False

    def isKillOkay(self, x, y, color) -> True | False:
        if x >= self.height or y >= self.width or x < 0 or y < 0: return False
        if self.board[y][x].color == color*-1: return True
        return False

    def movePiece(self, xStart, yStart, xEnd, yEnd ):
        piece = self.board[yStart][xStart]
        piece.move(xEnd, yEnd)
        self.board[yStart][xStart] = pieces.EmptySpace(xStart, yStart)
        self.board[yEnd][xEnd] = piece
        piece.x = xEnd
        piece.y = yEnd
    def transformDir(self, x, y) -> [[],[]]:
        result = [[], []]
        piece = self.board[y][x]
        dirs = piece.getDir()
        if isinstance(piece, pieces.Knight):
            for move in dirs:
                if self.isStepOkay(move[0], move[1]):
                    result[0].append(move)
                elif self.isKillOkay(move[0], move[1], piece.color):
                    result[1].append(move)
            return result
        if isinstance(piece, pieces.Pawn):
            for i in range(8):
                for move in dirs[i]:
                    if self.isStepOkay(move[0], move[1]) and i < 4:
                        result[0].append(move)
                    if self.isKillOkay(move[0], move[1], piece.color) and i > 3:
                        result[1].append(move)
            return result
        #[[][][][][][][]]
        for line in dirs:
            for move in line:
                if self.isStepOkay(move[0], move[1]):
                    result[0].append(move)
                elif self.isKillOkay(move[0], move[1], piece.color):
                    result[1].append(move)
                    break
                else:
                    break
        return result
    def selectPiece(self, x, y)-> [[],[]]:
        result = [[], []]
        if self.turn != self.board[y][x].color: return result
        return self.transformDir(x, y)

    def checkCheck(self) -> True | False:
        whiteCords = (self.kingWhite.x, self.kingWhite.y)
        blackCords = (self.kingBlack.x, self.kingBlack.y)
        isChecked = False
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                turns = self.transformDir(i, j)
                if whiteCords in turns[1]:
                    if self.whiteChecked:
                        print("Победили Черные!")
                        exit(0)
                    self.whiteChecked = True
                    print("Шах!")
                    isChecked = True
                if blackCords in turns[1]:
                    if self.blackChecked:
                        print("Победили Белые!")
                        exit(0)
                    self.blackChecked = True
                    print("Шах!")
                    isChecked = True
        if not isChecked:
            self.blackChecked = False
            self.whiteChecked = False
        return isChecked


    def checkCheckmate(self):
        ...


    def checkPawn(self):
        for piece in self.board[0]:
            if isinstance( piece, pieces.PawnWhite):
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




    def setStandartBoard(self):
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
