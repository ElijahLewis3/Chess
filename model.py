from abc import ABC

class Game:
    pass

class Board:
    pass

class Player:
    pass


############ PIECES ############
class Piece(ABC):
    def __init__(self, pos, colour):
        self.pos = pos
        self.colour = colour
        self.isCaptured = False
        self.isPinned = False
    
    @abstractmethod
    def validMoves(self):
        moveList = []
        return moveList

    @abstractmethod
    def canCheck(self, kingPos):
        return True if kingPos in self.validMoves() else False


class Rook(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.hasMoved = False

class Knight(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)


class Bishop(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)

class Queen(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)


class King(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.hasMoved = False


class Pawn(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.isPromoted = False