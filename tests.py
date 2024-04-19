from packageChess import boardChess123 as boardChess
from packageChess import piecesChess123 as piecesChess

gameBoard = boardChess.Board()
gameBoard.setStandartBoard()
gameBoard
print((gameBoard.board))

b = piecesChess.BishopBlack(1, 1)
k = piecesChess.KnightBlack(0, 0)

print(isinstance(b , piecesChess.Knight))