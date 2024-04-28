from packageChess import boardChess123 as boardChess
from packageChess import piecesChess123 as piecesChess

# gameBoard = boardChess.Board()
# gameBoard.setStandartBoard()
# gameBoard
# print((gameBoard.board))
#
# b = piecesChess.BishopBlack(1, 1)
# k = piecesChess.KnightBlack(0, 0)
#
# print(isinstance(b , piecesChess.Knight))

from random import shuffle
a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
foo = []
for i in a:
    for j in i:
        foo.append(j)
shuffle(foo)
for i in range(3):
    for j in range(3):
        a[i][j] = foo[i*3 + j]

print (a)