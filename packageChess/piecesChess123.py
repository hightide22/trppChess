class Piece:
    x = 0
    y = 0
    color = 0
    strType = "o"
    wasMoved = False

    def __init__(self, color: int, x=0, y=0) -> None:
        self.x = x
        self.color = color
        self.y = y

    def __str__(self):
        return self.strType

    def __repr__(self):
        return self.strType

    def move(self, x: int, y: int):
        self.x = x
        self.y = y

    def getDir(self) -> list:
        """
        :return: list of lists of moves in all directions:
                        up, down, left, right, upleft, upright, downleft, downright tuple(x: int, y: int)
        """
        return [[], [], [], [], [], [], [], []]


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


class King(Piece):
    moved = False

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
        if not self.moved:
            result[2].append((self.x - 2, self.y))  # left
            result[3].append((self.x + 2, self.y))  # right
        return result


class KingWhite(King):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(1, x, y)


class KingBlack(King):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)


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


class QueenBlack(Queen):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)


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


class BishopBlack(Bishop):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)


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


class RookBlack(Rook):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)


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


class KnightBlack(Knight):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(-1, x, y)
