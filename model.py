from abc import ABC
from abc import abstractmethod

class Game:
    def __init__(self, board, playerOne, playerTwo):
        self.board = board
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.winner = None
        #! may need to change it from being a player object to being an int
        self.turn = playerOne

    def movePiece(self, pos1, pos2):
        pass
    
    def canCapture(self, pos1, pos2):
        pass
    
    def switchTurn(self):
        if self.turn == playerOne:
            self.turn = playerTwo
        else:
            self.turn = playerOne
    
    def checkedPinned(self, pos):
        pass
    
    def isCheckingEnemy(self, player):
        colour = player.colour
        kingPos = None
        if colour == 1:
            kingPos = self.board.getBlackKingPos()
        elif colour == 0:
            kingPos = self.board.getWhiteKingPos()

        for pos in self.board.gameBoard:
            if self.board.gameBoard[pos] is not None and self.board.gameBoard[pos].colour == colour:
                if kingPos in self.board.gameBoard[pos].validMoves(self.board.gameBoard):
                    return True
        return False
    
    def getPiecesCheckingEnemy(self):
        pass
    
    def isKingSafe(self, tmpBoard, kingPos):
        pass

    def checkPromotion(self, pos):
        if self.board.gameBoard[pos].promote():
            colour = self.board.gameBoard[pos].colour
            self.board.removePiece(pos)
            self.board.gameBoard[pos] = Queen(pos,colour)

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

    def removePiece(self, pos):
        if (pos[0],pos[1]) in self.gameBoard:
            self.gameBoard[pos] = None

    #! under the assumption the Game class made sure the move was possible
    def movePiece(self,pos1, pos2):
        self.gameBoard[pos2] = self.gameBoard[pos1]
        self.gameBoard[pos1] = None
        self.gameBoard[pos2].pos = pos2

    def getWhiteKingPos(self):
        for pos in self.gameBoard:
            if isinstance(self.gameBoard[pos],King) and self.gameBoard[pos].colour == 1:
                return pos

    def getBlackKingPos(self):
        for pos in self.gameBoard:
            if isinstance(self.gameBoard[pos],King) and self.gameBoard[pos].colour == 0:
                return pos

class Player:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.draw = False
        self.capturedPieces = []


    def declareDraw(self):
        self.draw = True


############ PIECES ############
class Piece(ABC):
    def __init__(self, pos, colour):
        self.pos = pos
        self.colour = colour
        self.isCaptured = False
        self.isPinned = False
    
    @abstractmethod
    def validMoves(self, board):
        moveList = []
        return moveList


class Rook(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.hasMoved = False
        self.symbol = "R" if colour else "r"

    def validMoves(self, board):
        moveList = []
        posx, posy = self.pos[0], self.pos[1]
        
        validList = [
            (-1,  0), # up
            (1 ,  0), # down
            (0 , -1), # left
            (0 ,  1), # right
        ]

        # loop over each direction
        for i in range(4):
            posx, posy = self.pos[0], self.pos[1]
            while True:
                posx += validList[i][0] 
                posy += validList[i][1]

                # if we go off the board
                if (posx, posy) not in board:
                    break
                # if we run into another piece
                elif board[(posx, posy)] is not None:
                    # enemy piece
                    if board[(posx,posy)].colour != self.colour:
                        moveList.append((posx,posy))
                    break
                moveList.append((posx,posy))
                
        return moveList

class Knight(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.symbol = "N" if colour else "n"


    def validMoves(self, board):
        moveList = []
        # posx, posy = self.pos[0], self.pos[1]
        validList = [
            (-2, 1),  # up-up-right
            (-1, 2),  # up-right-right
            (-2, -1), # up-up-left
            (-1, -2), # up-left-left

            (2, 1),   # down-down-right
            (1, 2),   # down-right-right
            (2, -1),  # down-down-left
            (1, -2)   # down-left-left
        ]
        # loop over the each direction (up, down)
        for i in range(8):
            posx, posy = self.pos[0], self.pos[1]
            posx += validList[i][0]
            posy += validList[i][1]

        # if we go off the board
            if (posx, posy) not in board:
                continue

            # if we run into another piece
            if board[(posx, posy)] is not None:
                # enemy piece
                if board[(posx,posy)].colour != self.colour:
                    moveList.append((posx,posy))

            else:
                moveList.append((posx,posy))

        return moveList


class Bishop(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.symbol = "B" if colour else "b"

    def validMoves(self, board):
        moveList = []
        validList = [
            (-1, 1),  # up-right
            (-1, -1), # up-left
            (1, 1),   # down-right
            (1, -1)   # down-left
        ]

        for i in range(4):
            posx, posy = self.pos[0], self.pos[1]
            while True:
                posx += validList[i][0]
                posy += validList[i][1]

                # if the position is outside the board
                if (posx, posy) not in board:
                    break

                # if there is a piece at that position
                if board[(posx,posy)] is not None:
                    if board[(posx,posy)].colour != self.colour:
                        moveList.append((posx,posy))

                    break
                
                else:
                    moveList.append((posx,posy))

        return moveList

class Queen(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.symbol = "Q" if colour else "q"

    def validMoves(self, board):
        moveList = []
        validList = [
            (-1,  0), # up
            (1 ,  0), # down
            (0 , -1), # left
            (0 ,  1), # right
            (-1, 1),  # up-right
            (-1, -1), # up-left
            (1, 1),   # down-right
            (1, -1)   # down-left
        ]

        for i in range(8):
            posx, posy = self.pos[0], self.pos[1]
            while True:
                posx += validList[i][0]
                posy += validList[i][1]

                # if we go off the board
                if (posx, posy) not in board:
                    break
                # if we run into another piece
                elif board[(posx, posy)] is not None:
                    # enemy piece
                    if board[(posx,posy)].colour != self.colour:
                        moveList.append((posx,posy))
                    break
                moveList.append((posx,posy))
        return moveList

    """ another way to check Queen's moves
        bishopMoves = Bishop.validMoves(self,board)
        rookMoves = Rook.validMoves(self,board)
        return rookMoves + bishopMoves 
    """

#TODO
class King(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.hasMoved = False
        self.symbol = "K" if colour else "k"

    def validMoves(self, board):
        validList = [
            (-1, 0), # up
            (1, 0),  # down
            (0, 1),  # right
            (0, -1), # left

            (-1, 1),  # up-right
            (-1, -1), # up-left
            (1, 1),   # down-right
            (1, -1)   # down-left
        ]

        for i in range(8):
            posx, posy = self.pos[0], self.pos[1]
            posx += validList[i][0]
            posy += validList[i][1]

            if (posx, posy) not in board:
                continue
             
            #! Need to be able to move to a spot that prevents the King from being in check
            #Todo: Need to come back to this
            # if self.gameBoard((posx, posy)) is not None:
                # if 
        moveList = []
        return moveList



class Pawn(Piece):
    def __init__(self, pos, colour):
        super().__init__(pos,colour)
        self.isPromoted = False
        self.hasMoved = False
        self.symbol = "P" if colour else "p"

    def validMoves(self, board):
        validList = []
        posx, posy = self.pos[0], self.pos[1]

        # black
        if self.colour == 0:
            # first move
            if self.hasMoved == False and ((posx + 1, posy)) in board and board[(posx+  1, posy)] is None:
                validList.append((posx + 2,posy))
            
            #capture down-right
            if ((posx + 1, posy + 1)) in board and board[(posx+  1, posy + 1)] is not None:
                if board[(posx + 1,posy + 1)].colour != self.colour:
                        validList.append((posx + 1,posy + 1))
            
            #capture down-left
            if ((posx + 1, posy - 1)) in board and board[(posx+  1, posy - 1)] is not None:
                if board[(posx + 1,posy - 1)].colour != self.colour:
                        validList.append((posx + 1,posy - 1))

            # if stepped out of bounds
            if (posx + 1, posy) not in board:
                return validList
            # if there is a piece in front of the pawn
            if ((posx + 1, posy)) in board and board[(posx+  1, posy)] is not None:
                return validList
            validList.append((posx + 1, posy))

        else:
            # first move
            if self.hasMoved == False and ((posx - 1, posy)) in board and board[(posx -  1, posy)] is None:
                validList.append((posx -2,posy))
            
            #capture up-right
            if ((posx - 1, posy + 1)) in board and board[(posx -  1, posy + 1)] is not None:
                if board[(posx - 1,posy + 1)].colour != self.colour:
                        validList.append((posx - 1,posy + 1))
            
            #capture up-left
            if ((posx -1, posy -1)) in board and board[(posx -  1, posy - 1)] is not None:
                if board[(posx - 1,posy - 1)].colour != self.colour:
                        validList.append((posx - 1,posy - 1))

            # if stepped out of bounds
            if (posx - 1, posy) not in board:
                return validList
            # if there is a piece in front of the pawn
            if ((posx - 1, posy)) in board and board[(posx -  1, posy)] is not None:
                return validList
            validList.append((posx - 1, posy))
        return validList
    
    def promote(self):
        #black
        if self.colour == 0:
            if self.pos[0] == 7:
                return True
            else:
                return False
        
        #white
        elif self.colour == 1:
            if self.pos[0] == 0:
                return True
            else:
                return False
