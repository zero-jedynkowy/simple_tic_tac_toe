import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QRegularExpression
import random

class Program:
    window = 0

    @staticmethod
    def setDefaultFields():
        loadedPixMap = QPixmap("content/blank_template.png")
        boardList = Program.window.findChildren(QLabel, QRegularExpression("board*"))
        for i in boardList:
            i.setPixmap(loadedPixMap)
        Program.window.currentTurn.setPixmap(loadedPixMap)

class Game():

    def setDefault():
        Game.players = ["x", "o"]
        Game.board = [['blank', 'blank', 'blank'] for _ in range(3)]
        Game.currentRound = random.choice(Game.players)
        Game.counterAvailableFields = 9

    @staticmethod
    def resetGame():
        Game.setDefault()

    @staticmethod
    def nextTurn():
        if Game.currentRound == Game.players[0]:
            Game.currentRound = Game.players[1]
        else:
            Game.currentRound = Game.players[0]
        Game.counterAvailableFields -= 1

    @staticmethod
    def changeField(self, row, column):
        row -= 1
        column -= 1
        if Game.board[row][column] == 'blank':
            Game.board[row][column] = Game.currentRound
            return True
        return False
    
    @staticmethod
    def checkWin():
        for i in range(3):
            temporary1 = ''.join(Game.board[i])
            if  temporary1 == 'xxx' or temporary1 == 'ooo':
                return True
            temporary1 = ''.join([Game.board[x][i] for x in range(3)])
            if  temporary1 == 'xxx' or temporary1 == 'ooo':
                return True
        temporary2 = ''.join([Game.board[a][b] for (a, b) in [(0, 0), (1, 1), (2, 2)]])
        if  temporary2 == 'xxx' or temporary2 == 'ooo':
            return True
        temporary2 = ''.join([Game.board[a][b] for (a, b) in [(0, 2), (1, 1), (2, 0)]])
        if  temporary2 == 'xxx' or temporary2 == 'ooo':
            return True
        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_file_name = "content/mainWindow.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    Program.window = loader.load(ui_file)
    ui_file.close()
    if not Program.window:
        print(loader.errorString())
        sys.exit(-1)

    Program.setDefaultFields()
    Program.window.show()

    sys.exit(app.exec())