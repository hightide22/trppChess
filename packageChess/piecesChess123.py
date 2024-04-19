import boardChess123

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
    
    def move(self):
        pass
    
    
class EmptySpace(Piece):
    def __init__(self, x, y) -> None:
        super().__init__(0, x, y)
        
     
     
class Pawn(Piece):
    
    def __init__(self, color, x, y) -> None:
        super().__init__(color, x, y)
        self.strType = "p"
    def move(self):
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
        self.strType = "K"
    def move(self): ...
    
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
        self.strType = "q"
    def move(self): ...

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
        self.strType = "b"
    def move(self): ...
        
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
        self.strType = "r"
    def move(self): ...
        
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
        self.strType = "k"
    def move(self): ...

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



























