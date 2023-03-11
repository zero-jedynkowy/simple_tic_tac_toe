from interface import Ui_MainWindow
from win_message import Ui_Dialog
import sys
import random
from PyQt5 import QtCore, QtGui, QtWidgets

class Game():
    
    def __init__(self):
        self.players = ["x", "o"]
        self.board = [['blank', 'blank', 'blank'] for _ in range(3)]
        self.currentRound = random.choice(self.players)

    def resetGame(self):
        self.__init__()

    def nextTurn(self):
        if self.currentRound == self.players[0]:
            self.currentRound = self.players[1]
        else:
            self.currentRound = self.players[0]

    def changeField(self, row, column):
        row -= 1
        column -= 1
        if self.board[row][column] == 'blank':
            self.board[row][column] = self.currentRound
            return True
        return False
    
    def checkWin(self):
        for i in range(3):
            temporary1 = ''.join(self.board[i])
            if  temporary1 == 'xxx' or temporary1 == 'ooo':
                return True
            temporary1 = ''.join([self.board[x][i] for x in range(3)])
            if  temporary1 == 'xxx' or temporary1 == 'ooo':
                return True
        temporary2 = ''.join([self.board[a][b] for (a, b) in [(0, 0), (1, 1), (2, 2)]])
        if  temporary2 == 'xxx' or temporary2 == 'ooo':
            return True
        temporary2 = ''.join([self.board[a][b] for (a, b) in [(0, 2), (1, 1), (2, 0)]])
        if  temporary2 == 'xxx' or temporary2 == 'ooo':
            return True
        return False

class WinMessageBox(QtWidgets.QDialog):
    def __init__(self, parent):
        super(WinMessageBox, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.game = Game()
        template = "self.ui.board_{}{}.mousePressEvent = self.changeContent(i, j)"
        for i in range(1, 4, 1):
            for j in range(1, 4, 1):
                exec(template.format(i, j))
        self.changePixMapFieldBoard('current_turn', '{}_template.png'.format(self.game.currentRound))
    
    def changeContent(self, row, column):
        def clickedAction(event):
            nonlocal row
            nonlocal column
            nonlocal self
            if self.game.changeField(row, column):
                self.changePixMapFieldBoard('board_{}{}'.format(row, column), '{}_template.png'.format(self.game.currentRound))
                if self.game.checkWin():
                    winDialog = WinMessageBox(self)
                    winDialog.ui.label.setText(winDialog.ui.label.text().format(self.game.currentRound.upper()))
                    winDialog.ui.pushButton.clicked.connect(winDialog.close)
                    winDialog.show()
                    winDialog.exec()
                    self.game.resetGame()
                    for i in range(1, 4, 1):
                        for j in range(1, 4, 1):
                            self.changePixMapFieldBoard('board_{}{}'.format(i, j), 'blank_template.png')
                self.game.nextTurn()
                self.changePixMapFieldBoard('current_turn', '{}_template.png'.format(self.game.currentRound))
        return clickedAction
    
    def changePixMapFieldBoard(self, name, newContent):
        template = 'self.ui.{}.setPixmap(QtGui.QPixmap("{}"))'
        exec(template.format(name, newContent))
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())