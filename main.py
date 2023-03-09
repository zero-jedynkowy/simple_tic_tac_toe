from interface import Ui_MainWindow
import sys
import random
from PyQt5 import QtCore, QtGui, QtWidgets

class Game():
    def __init__(self) -> None:
        self.players = ["X", "O"]
        self.currentRound = random.choice(self.players)
    def resetGame(self):
        self.__init__()
    def nextTurn(self):
        if self.currentRound == self.players[0]:
            self.currentRound = self.players[1]
        else:
            self.currentRound = self.players[0]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        game = Game()
        template = "self.ui.board_{}{}.mousePressEvent = self.changeContent(i, j)"
        for i in range(1, 4, 1):
            for j in range(1, 4, 1):
                exec(template.format(i, j))   
    def changeContent(self, row, column):
        def clickedAction(self):
            nonlocal row
            nonlocal column
            print(row, column)
        return clickedAction
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())