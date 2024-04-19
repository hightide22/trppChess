import pieces 

class Board:
    hight = 8
    width = 8
    
    emptySpace = type(pieces.EmptySpace(0, 0))
    
    board = [["-"] * width] * hight
    
    def isStepOkay(x, y):
        if x >= Board.hight or y >= Board.width or x < 0 or y < 0: return False
        if type( Board.board[y][x]) == Board.emptySpace:
            return True
        return False
    
    def isKillOkay(x, y, color):
        if x >= Board.hight or y >= Board.width or x < 0 or y < 0: return False


    def setStandartBoard():
        if Board.width != 8 or Board.hight != 8: return
        Board.board[0][0] = pieces.RookBlack(0, 0)
        Board.board[0][1] = pieces.KnightBlack(0, 1)
        Board.board[0][2] = pieces.BishopBlack(0, 2)
        Board.board[0][3] = pieces.QueenBlack(0, 3)
        Board.board[0][4] = pieces.KingBlack(0, 4)
        Board.board[0][5] = pieces.BishopBlack(0, 5)
        Board.board[0][6] = pieces.KnightBlack(0, 6)
        Board.board[0][7] = pieces.RookBlack(0, 7)
        for i in range(8): Board.board[1][i] = pieces.PawnBlack(1, i)
        
        for i in range(4):
            for j in range(8): Board.board[2 + i][j] = pieces.EmptySpace(2+i, j)
            
        Board.board[7][0] = pieces.RookWhite(7, 0)
        Board.board[7][1] = pieces.KnightWhite(7, 1)
        Board.board[7][2] = pieces.BishopWhite(7, 2)
        Board.board[7][3] = pieces.QueenWhite(7, 3)
        Board.board[7][4] = pieces.KingWhite(7, 4)
        Board.board[7][5] = pieces.BishopWhite(7, 5)
        Board.board[7][6] = pieces.KnightWhite(7, 6)
        Board.board[7][7] = pieces.RookWhite(7, 7)    
        for i in range(8): Board.board[6][i] = pieces.PawnWhite(6, i)
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            