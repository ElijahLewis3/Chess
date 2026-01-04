from abc import ABC
from abc import abstractmethod

class Game:
    pass

class Board:
    def __init__(self):
        self.gameBoard = {}
        self.setupBoard()

    def setupBoard(self):
        for row in range(8):
            for col in range(8):
                self.gameBoard[(row,col)] = None

        ############### BLACK ###############
        self.gameBoard[(0,0)] = Rook((0,0),0)
        self.gameBoard[(0,7)] = Rook((0,7),0)

        self.gameBoard[(0,1)] = Knight((0,1),0)
        self.gameBoard[(0,6)] = Knight((0,6),0)

        self.gameBoard[(0,2)] = Bishop((0,2),0)
        self.gameBoard[(0,5)] = Bishop((0,5),0)

        self.gameBoard[(0,3)] = Queen((0,3),0)
        self.gameBoard[(0,4)] = King((0,4),0)

        for i in range(8):
            self.gameBoard[(1,i)] = Pawn((1,i),0)

        ############### WHITE ###############
        self.gameBoard[(7,0)] = Rook((7,0),1)
        self.gameBoard[(7,7)] = Rook((7,7),1)

        self.gameBoard[(7,1)] = Knight((7,1),1)
        self.gameBoard[(7,6)] = Knight((7,6),1)

        self.gameBoard[(7,2)] = Bishop((7,2),1)
        self.gameBoard[(7,5)] = Bishop((7,5),1)

        self.gameBoard[(7,3)] = Queen((7,3),1)
        self.gameBoard[(7,4)] = King((7,4),1)

        for i in range(8):
            self.gameBoard[(6,i)] = Pawn((6,i),1)


    def updateBoard(self, newBoard):
        self.gameBoard = newBoard

    def printBoard(self):
        finalString = "\ta\tb\tc\td\te\tf\tg\th\n\n"
        for row in range(0,8):
            finalString += str(row)
            for col in range(0,8):
                if self.gameBoard[(row,col)]:
                    finalString += "\t"
                    finalString += self.gameBoard[(row,col)].symbol
                    finalString += "  "
                else:
                    finalString += "\t   "
            finalString += "    " + str(row)
            finalString += "\n\n"

        finalString += "\ta\tb\tc\td\te\tf\tg\th\n\n"
        return finalString


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

    def canCheck(self, kingPos):
        return True if kingPos in self.validMoves() else False


class Rook(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.hasMoved = False
        self.symbol = "R" if colour else "r"

    def validMoves(self):
        moveList = []
        return moveList

class Knight(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.symbol = "N" if colour else "n"


    def validMoves(self):
        moveList = []
        return moveList


class Bishop(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.symbol = "B" if colour else "b"

    def validMoves(self):
        moveList = []
        return moveList

class Queen(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.symbol = "Q" if colour else "q"

    def validMoves(self):
        moveList = []
        return moveList


class King(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.hasMoved = False
        self.symbol = "K" if colour else "k"

    def validMoves(self):
        moveList = []
        return moveList


class Pawn(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.isPromoted = False
        self.symbol = "P" if colour else "p"

    def validMoves(self):
        moveList = []
        return moveList