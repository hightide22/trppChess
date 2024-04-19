import pack.board 

class Piece:
    x = 0
    y = 0
    color = 0
    strType = "o"
    
    def __init__(self, color, x, y) -> None:
        self.x = x
        self.color = color
        self.y = y
    def __str__(self):
        return self.strType
    
    def move():
        pass
    
    
class EmptySpace(Piece):
    def __init__(self, x, y) -> None:
        super().__init__(0, x, y)
        
     
     
class Pawn(Piece):
    
    def __init__(self, color, x, y) -> None:
        super().__init__(color, x, y)
        super().strType = "p"       
    def move():
        ...    
               
class PawnWhite(Pawn):
    def __init__(self, x, y) -> None:
        super().__init__(1, x, y)  
    def move(x, y):
        pass   
class PawnBlack(Pawn):
    def __init__(self, x, y) -> None:
        super().__init__(-1, x, y)
        
    def move(x, y):
        pass
 


class King(Piece):
    def __init__(self, color, x, y) -> None:
        super().__init__(color, x, y)
        super().strType = "K"       
    def move(): ...    
    
class KingWhite(King):
    def __init__(self, x, y) -> None:
        super().__init__(1, x, y)       
    def move(x, y):
        pass
class KingBlack(King):
    def __init__(self, x, y) -> None:
        super().__init__(-1, x, y)
    def move(x, y):
        pass



class Queen(Piece):
    def __init__(self, color, x, y) -> None:
        super().__init__(color, x, y)
        super().strType = "q"       
    def move(): ...       

class QueenWhite(Queen):
    def __init__(self, x, y) -> None:
        super().__init__(1, x, y)
    def move(x, y):
        pass
class QueenBlack(Queen):
    def __init__(self, x, y) -> None:
        super().__init__(-1, x, y)
      
    def move(x, y):
        pass



class Bishop(Piece):
    def __init__(self, color, x, y) -> None:
        super().__init__(color, x, y)
        super().strType = "b"       
    def move(): ...  
        
class BishopWhite(Bishop):
    def __init__(self, x, y) -> None:
        super().__init__(1, x, y)
       
    def move(x, y):
        pass
class BishopBlack(Bishop):
    def __init__(self, x, y) -> None:
        super().__init__(-1, x, y)
        
    def move(x, y):
        pass



class Rook(Piece):
    def __init__(self, color, x, y) -> None:
        super().__init__(color, x, y)
        super().strType = "r"       
    def move(): ...  
        
class RookWhite(Rook):
    def __init__(self, x, y) -> None:
        super().__init__(1, x, y)        
    def move(x, y):
        pass
class RookBlack(Rook):
    def __init__(self, x, y) -> None:
        super().__init__(-1, x, y)        
    def move(x, y):
        pass



class Knight(Piece):
    def __init__(self, color, x, y) -> None:
        super().__init__(color, x, y)
        super().strType = "k"       
    def move(): ...  

class KnightWhite(Knight):
    def __init__(self, x, y) -> None:
        super().__init__(1, x, y)
      
    def move(x, y):
        pass
class KnightBlack(Knight):
    def __init__(self, x, y) -> None:
        super().__init__(-1, x, y)
        
    def move(x, y):
        pass



























