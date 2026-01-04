from model import Board
from view import GameView
if __name__ == "__main__":
    newBoard = Board()
    gui = GameView()
    
    gui.displayBoard(newBoard.printBoard())


