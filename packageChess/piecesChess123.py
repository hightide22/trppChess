class Piece:



    def __init__(self, color: int, x=0, y=0) -> None:
        self.strType = "o"
        self.exp = 0
        self.level = 1
        self.wasMoved = False

        self.x = x
        self.color = color
        self.y = y

    def __str__(self):
        return self.strType

    def __repr__(self):
        self.strType

    def move(self, x: int, y: int):
        self.x = x
        self.y = y

    def getDir(self) -> list:
        """
        :return: list of lists of moves in all directions:
                        up, down, left, right, upleft, upright, downleft, downright tuple(x: int, y: int)
        """
        return [[], [], [], [], [], [], [], []]

    def evolve(self) -> object:
        return self


class EmptySpace(Piece):
    def __init__(self, x, y) -> None:
        super().__init__(0, x, y)


class Pawn(Piece):
    isEnPassant = False

    def __init__(self, color: int, x: int, y: int) -> None:
        super().__init__(color, x, y)
        self.strType = str(color) + "p"


class PawnWhite(Pawn):
    def __init__(self, x, y) -> None:
        super().__init__(1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        result[0].append((self.x, self.y - 1))  # up
        if self.y == 6:
            result[0].append((self.x, self.y - 2))
        result[4].append((self.x - 1, self.y - 1))
        result[5].append((self.x + 1, self.y - 1))
        return result

    def evolve(self) -> object:
        return PawnTwoWhite(self.x, self.y)


class PawnBlack(Pawn):
    def __init__(self, x, y) -> None:
        super().__init__(-1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        result[1].append((self.x, self.y + 1))  # down
        if self.y == 1:
            result[1].append((self.x, self.y + 2))
        result[6].append((self.x - 1, self.y + 1))
        result[7].append((self.x + 1, self.y + 1))
        return result

    def evolve(self) -> object:
        return PawnTwoBlack(self.x, self.y)


class King(Piece):
    wasMoved = False

    def __init__(self, color: int, x: int, y: int) -> None:
        super().__init__(color, x, y)
        self.strType = str(color) + "King"

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        for i in range(1, 2):
            result[0].append((self.x, self.y - i))  # up
            result[1].append((self.x, self.y + i))  # down
            result[2].append((self.x - i, self.y))  # left
            result[3].append((self.x + i, self.y))  # right
            result[4].append((self.x - i, self.y - i))  # upleft
            result[5].append((self.x + i, self.y - i))  # upright
            result[6].append((self.x - i, self.y + i))  # downleft
            result[7].append((self.x + i, self.y + i))  # downright
        if not self.wasMoved:
            result[2].append((self.x - 2, self.y))  # left
            result[3].append((self.x + 2, self.y))  # right
        return result


class KingWhite(King):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)

    def evolve(self) -> object:
        return KingTwoWhite(self.x, self.y)


class KingBlack(King):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)

    def evolve(self) -> object:
        return KingTwoBlack(self.x, self.y)


class Queen(Piece):
    def __init__(self, color: int, x: int, y: int) -> None:
        super().__init__(color, x, y)
        self.strType = str(color) + "q"

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        for i in range(1, 8):
            result[0].append((self.x, self.y - i))  # up
            result[1].append((self.x, self.y + i))  # down
            result[2].append((self.x - i, self.y))  # left
            result[3].append((self.x + i, self.y))  # right
            result[4].append((self.x - i, self.y - i))  # upleft
            result[5].append((self.x + i, self.y - i))  # upright
            result[6].append((self.x - i, self.y + i))  # downleft
            result[7].append((self.x + i, self.y + i))  # downright
        return result


class QueenWhite(Queen):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)

    def evolve(self) -> object:
        return QueenTwoWhite(self.x, self.y)


class QueenBlack(Queen):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)

    def evolve(self) -> object:
        return QueenTwoBlack(self.x, self.y)


class Bishop(Piece):
    def __init__(self, color, x: int, y: int) -> None:
        super().__init__(color, x, y)
        self.strType = str(color) + "b"

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        for i in range(1, 8):
            result[4].append((self.x - i, self.y - i))  # upleft
            result[5].append((self.x + i, self.y - i))  # upright
            result[6].append((self.x - i, self.y + i))  # downleft
            result[7].append((self.x + i, self.y + i))  # downright
        return result


class BishopWhite(Bishop):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)

    def evolve(self) -> object:
        return BishopTwoWhite(self.x, self.y)


class BishopBlack(Bishop):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)

    def evolve(self) -> object:
        return BishopTwoBlack(self.x, self.y)


class Rook(Piece):
    def __init__(self, color: int, x: int, y: int) -> None:
        super().__init__(color, x, y)
        self.strType = str(color) + "r"

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        for i in range(1, 8):
            result[0].append((self.x, self.y - i))  # up
            result[1].append((self.x, self.y + i))  # down
            result[2].append((self.x - i, self.y))  # left
            result[3].append((self.x + i, self.y))  # right
        return result


class RookWhite(Rook):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)
        pass

    def evolve(self) -> object:
        return RookTwoWhite(self.x, self.y)


class RookBlack(Rook):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)

    def evolve(self) -> object:
        return RookTwoBlack(self.x, self.y)


class Knight(Piece):
    def __init__(self, color: int, x: int, y: int) -> None:
        super().__init__(color, x, y)
        self.strType = str(color) + "k"

    def getDir(self) -> list:
        return [[(self.x + 2, self.y + 1)], [(self.x + 2, self.y - 1)], [(self.x - 2, self.y + 1)],
                [(self.x - 2, self.y - 1)],
                [(self.x + 1, self.y + 2)], [(self.x + 1, self.y - 2)
                                             ], [(self.x - 1, self.y + 2)],
                [(self.x - 1, self.y - 2)]]


class KnightWhite(Knight):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)

    def evolve(self) -> object:
        return KnightTwoWhite(self.x, self.y)


class KnightBlack(Knight):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)

    def evolve(self) -> object:
        return KnightTwoBlack(self.x, self.y)


class PawnTwoWhite(Pawn):


    def __init__(self, x, y) -> None:
        self.level = 2
        super().__init__(1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        result[0].append((self.x, self.y - 1))  # up
        result[0].append((self.x, self.y - 2))
        result[4].append((self.x - 1, self.y - 1))
        result[5].append((self.x + 1, self.y - 1))
        return result

    def evolve(self) -> Piece:
        return PawnThreeWhite(self.x, self.y)


class PawnTwoBlack(Pawn):
    def __init__(self, x, y) -> None:
        self.level = 2
        super().__init__(-1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        result[1].append((self.x, self.y + 1))  # up
        result[1].append((self.x, self.y + 2))
        result[6].append((self.x - 1, self.y + 1))
        result[7].append((self.x + 1, self.y + 1))
        return result

    def evolve(self) -> Piece:
        return PawnThreeBlack(self.x, self.y)


class PawnThreeWhite(Pawn):
    def __init__(self, x, y) -> None:
        self.level = 3
        super().__init__(1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        result[0].append((self.x, self.y - 1))  # up
        result[0].append((self.x, self.y - 2))
        result[4].append((self.x - 1, self.y - 1))
        result[5].append((self.x + 1, self.y - 1))
        result[1].append((self.x, self.y + 1))  # down
        result[1].append((self.x, self.y + 2))
        result[6].append((self.x - 1, self.y + 1))
        result[7].append((self.x + 1, self.y + 1))
        return result


class PawnThreeBlack(Pawn):

    def __init__(self, x, y) -> None:
        self.level = 3
        super().__init__(-1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        result[0].append((self.x, self.y - 1))  # up
        result[0].append((self.x, self.y - 2))
        result[4].append((self.x - 1, self.y - 1))
        result[5].append((self.x + 1, self.y - 1))
        result[1].append((self.x, self.y + 1))  # down
        result[1].append((self.x, self.y + 2))
        result[6].append((self.x - 1, self.y + 1))
        result[7].append((self.x + 1, self.y + 1))
        return result


class RookTwoWhite(Rook):

    def __init__(self, x: int, y: int) -> None:
        self.level = 2
        super().__init__(1, x, y)


    def evolve(self) -> object:
        return RookThreeWhite(self.x, self.y)


class RookTwoBlack(Rook):

    def __init__(self, x: int, y: int) -> None:
        self.level = 2
        super().__init__(-1, x, y)

    def evolve(self) -> object:
        return RookThreeBlack(self.x, self.y)


class RookThreeWhite(Rook):

    def __init__(self, x: int, y: int) -> None:
        self.level = 3
        super().__init__(1, x, y)


class RookThreeBlack(Rook):

    def __init__(self, x: int, y: int) -> None:
        self.level = 3
        super().__init__(-1, x, y)


class KnightTwoWhite(Knight):

    def __init__(self, x: int, y: int) -> None:
        self.level = 2
        super().__init__(1, x, y)

    def getDir(self) -> list:
        return [[(self.x + 2, self.y + 1), (self.x, self.y + 2)], [(self.x + 2, self.y - 1), (self.x, self.y - 2)],
                [(self.x - 2, self.y + 1), (self.x + 2, self.y)],
                [(self.x - 2, self.y - 1), (self.x - 2, self.y)],
                [(self.x + 1, self.y + 2)], [(self.x + 1, self.y - 2)
                                             ], [(self.x - 1, self.y + 2)],
                [(self.x - 1, self.y - 2)]]

    def evolve(self) -> object:
        return KnightThreeWhite(self.x, self.y)


class KnightTwoBlack(Knight):

    def __init__(self, x: int, y: int) -> None:
        self.level = 2
        super().__init__(-1, x, y)

    def getDir(self) -> list:
        return [[(self.x + 2, self.y + 1), (self.x, self.y + 2)], [(self.x + 2, self.y - 1), (self.x, self.y - 2)],
                [(self.x - 2, self.y + 1), (self.x + 2, self.y)],
                [(self.x - 2, self.y - 1), (self.x - 2, self.y)],
                [(self.x + 1, self.y + 2)], [(self.x + 1, self.y - 2)
                                             ], [(self.x - 1, self.y + 2)],
                [(self.x - 1, self.y - 2)]]

    def evolve(self) -> object:
        return KnightThreeBlack(self.x, self.y)


class KnightThreeWhite(Knight):
    level = 3

    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)

    def getDir(self) -> list:
        return [[(self.x + 2, self.y + 1), (self.x, self.y + 2)], [(self.x + 2, self.y - 1), (self.x, self.y - 2)],
                [(self.x - 2, self.y + 1), (self.x + 2, self.y)],
                [(self.x - 2, self.y - 1), (self.x - 2, self.y)],
                [(self.x + 1, self.y + 2), (self.x + 2, self.y + 2),
                 (self.x + 2, self.y + 2 + 1), (self.x + 2 + 1, self.y + 2)],
                [(self.x + 1, self.y - 2), (self.x - 2, self.y + 2),
                 (self.x - 2 - 1, self.y + 2), (self.x - 2, self.y + 2 + 1)],
                [(self.x - 1, self.y + 2), (self.x - 2, self.y - 2),
                 (self.x - 2 - 1, self.y - 2), (self.x - 2, self.y - 2 - 1)],
                [(self.x - 1, self.y - 2), (self.x + 2, self.y - 2),
                 (self.x + 2 + 1, self.y - 2), (self.x + 2, self.y - 2 - 1)]]


class KnightThreeBlack(Knight):
    level = 3

    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)

    def getDir(self) -> list:
        return [[(self.x + 2, self.y + 1), (self.x, self.y + 2)], [(self.x + 2, self.y - 1), (self.x, self.y - 2)],
                [(self.x - 2, self.y + 1), (self.x + 2, self.y)],
                [(self.x - 2, self.y - 1), (self.x - 2, self.y)],
                [(self.x + 1, self.y + 2), (self.x + 2, self.y + 2),
                 (self.x + 2, self.y + 2 + 1), (self.x + 2 + 1, self.y + 2)],
                [(self.x + 1, self.y - 2), (self.x - 2, self.y + 2),
                 (self.x - 2 - 1, self.y + 2), (self.x - 2, self.y + 2 + 1)],
                [(self.x - 1, self.y + 2), (self.x - 2, self.y - 2),
                 (self.x - 2 - 1, self.y - 2), (self.x - 2, self.y - 2 - 1)],
                [(self.x - 1, self.y - 2), (self.x + 2, self.y - 2),
                 (self.x + 2 + 1, self.y - 2), (self.x + 2, self.y - 2 - 1)]]


class BishopTwoWhite(Bishop):
    level = 2

    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        for i in range(1, 8):
            result[4].append((self.x - i, self.y - i))  # upleft
            result[5].append((self.x + i, self.y - i))  # upright
            result[6].append((self.x - i, self.y + i))  # downleft
            result[7].append((self.x + i, self.y + i))  # downright
        result[0].append((self.x, self.y - 1))
        result[1].append((self.x, self.y + 1))
        result[2].append((self.x - 1, self.y))
        result[3].append((self.x + 1, self.y))
        return result

    def evolve(self) -> object:
        return BishopThreeWhite(self.x, self.y)


class BishopTwoBlack(Bishop):
    level = 2

    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        for i in range(1, 8):
            result[4].append((self.x - i, self.y - i))  # upleft
            result[5].append((self.x + i, self.y - i))  # upright
            result[6].append((self.x - i, self.y + i))  # downleft
            result[7].append((self.x + i, self.y + i))  # downright
        result[0].append((self.x, self.y - 1))
        result[1].append((self.x, self.y + 1))
        result[2].append((self.x - 1, self.y))
        result[3].append((self.x + 1, self.y))
        return result

    def evolve(self) -> object:
        return BishopThreeBlack(self.x, self.y)


class BishopThreeWhite(Bishop):
    level = 3

    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        for i in range(1, 8):
            result[4].append((self.x - i, self.y - i))  # upleft
            result[5].append((self.x + i, self.y - i))  # upright
            result[6].append((self.x - i, self.y + i))  # downleft
            result[7].append((self.x + i, self.y + i))  # downright
            result[0].append((self.x - i, self.y + i))
            result[1].append((self.x - i, self.y - i))
            result[2].append((self.x + i, self.y - i))
            result[3].append((self.x + i, self.y + i))
        return result


class BishopThreeBlack(Bishop):
    level = 3

    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        for i in range(1, 8):
            result[4].append((self.x - i, self.y - i))  # upleft
            result[5].append((self.x + i, self.y - i))  # upright
            result[6].append((self.x - i, self.y + i))  # downleft
            result[7].append((self.x + i, self.y + i))  # downright
            result[0].append((self.x - i, self.y + 1 + i))
            result[1].append((self.x - i - 1, self.y - i))
            result[2].append((self.x - 1 + i, self.y - 1 - i))
            result[3].append((self.x + 1 + i, self.y + i))
        return result


class KingTwoWhite(King):
    level = 2

    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        for i in range(1, 3):
            result[0].append((self.x, self.y - i))  # up
            result[1].append((self.x, self.y + i))  # down
            result[2].append((self.x - i, self.y))  # left
            result[3].append((self.x + i, self.y))  # right
            result[4].append((self.x - i, self.y - i))  # upleft
            result[5].append((self.x + i, self.y - i))  # upright
            result[6].append((self.x - i, self.y + i))  # downleft
            result[7].append((self.x + i, self.y + i))  # downright
        if not self.wasMoved:
            result[2].append((self.x - 2, self.y))  # left
            result[3].append((self.x + 2, self.y))  # right
        return result

    def evolve(self) -> object:
        return KingThreeWhite(self.x, self.y)


class KingTwoBlack(King):
    level = 2

    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        for i in range(1, 3):
            result[0].append((self.x, self.y - i))  # up
            result[1].append((self.x, self.y + i))  # down
            result[2].append((self.x - i, self.y))  # left
            result[3].append((self.x + i, self.y))  # right
            result[4].append((self.x - i, self.y - i))  # upleft
            result[5].append((self.x + i, self.y - i))  # upright
            result[6].append((self.x - i, self.y + i))  # downleft
            result[7].append((self.x + i, self.y + i))  # downright
        if not self.wasMoved:
            result[2].append((self.x - 2, self.y))  # left
            result[3].append((self.x + 2, self.y))  # right
        return result

    def evolve(self) -> object:
        return KingThreeBlack(self.x, self.y)


class KingThreeWhite(King):
    level = 3

    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        for i in range(1, 8):
            result[0].append((self.x, self.y - i))  # up
            result[1].append((self.x, self.y + i))  # down
            result[2].append((self.x - i, self.y))  # left
            result[3].append((self.x + i, self.y))  # right
            result[4].append((self.x - i, self.y - i))  # upleft
            result[5].append((self.x + i, self.y - i))  # upright
            result[6].append((self.x - i, self.y + i))  # downleft
            result[7].append((self.x + i, self.y + i))  # downright
        return result


class KingThreeBlack(King):
    level = 3

    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)

    def getDir(self) -> list:
        result = [[], [], [], [], [], [], [], []]
        for i in range(1, 8):
            result[0].append((self.x, self.y - i))  # up
            result[1].append((self.x, self.y + i))  # down
            result[2].append((self.x - i, self.y))  # left
            result[3].append((self.x + i, self.y))  # right
            result[4].append((self.x - i, self.y - i))  # upleft
            result[5].append((self.x + i, self.y - i))  # upright
            result[6].append((self.x - i, self.y + i))  # downleft
            result[7].append((self.x + i, self.y + i))  # downright
        return result


class QueenTwoWhite(Queen):
    level = 2

    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)

    def evolve(self) -> object:
        return QueenThreeWhite(self.x, self.y)


class QueenTwoBlack(Queen):
    level = 2

    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)

    def evolve(self) -> object:
        return QueenThreeBlack(self.x, self.y)


class QueenThreeWhite(Queen):
    level = 3

    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)


class QueenThreeBlack(Queen):
    level = 3

    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)
