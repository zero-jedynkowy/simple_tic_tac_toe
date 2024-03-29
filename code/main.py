import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QPushButton, QDialog
from PySide6.QtCore import QRegularExpression
import random

class Game():

    players = ["x", "o"]
    board = [['blank', 'blank', 'blank'] for _ in range(3)]
    currentRound = random.choice(players)
    counterAvailableFields = 9

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
    def changeField(row, column):
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

class Program:
    
    window = 0
    aboutWindow = 0
    winWindow = 0
    drawWindow = 0
    winDefaultString = 0

    @staticmethod
    def positionWindowCentering(window):
        screenSize = QApplication.primaryScreen().size()
        screenSizeList = [screenSize.width() - window.minimumWidth(), screenSize.height() - window.minimumHeight()]
        screenSizeList = [int(i/2) for i in screenSizeList]
        screenSizeList.append(window.minimumWidth())
        screenSizeList.append(window.minimumHeight())
        window.setGeometry(*screenSizeList)

    @staticmethod
    def loadWindow(path):
        ui_file_name = path
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        window = loader.load(ui_file)
        ui_file.close()
        if not window:
            print(loader.errorString())
            sys.exit(-1)
        return window

    @staticmethod
    def setDefaultFields():
        loadedPixMap = QPixmap("content/blank_template.png")
        boardList = Program.window.findChildren(QPushButton, QRegularExpression("board*"))
        for i in boardList:
            i.setIcon(loadedPixMap)
        loadedPixMap = QPixmap("content/{}_template.png".format(Game.currentRound))
        Program.window.currentTurn.setPixmap(loadedPixMap)

    @staticmethod 
    def generateAction(x):
        number = x.objectName()
        number = number[number.find("_") + 1:]
        cords = list(number)
        cords = [int(i) for i in cords]
        def y():
            nonlocal x
            nonlocal cords
            if Game.changeField(*cords):
                loadedPixMap = QPixmap("content/{}_template.png".format(Game.currentRound))
                x.setIcon(loadedPixMap)
                if Game.checkWin():
                    QDialog.setModal(Program.winWindow, True)
                    newWinner = Program.winDefaultString.format(Game.currentRound.upper())
                    Program.winWindow.label.setText(newWinner)
                    Program.winWindow.setWindowTitle(newWinner)
                    Program.positionWindowCentering(Program.winWindow)
                    Program.winWindow.show()
                    Program.winWindow.exec()
                    Game.setDefault()
                    Program.setDefaultFields()
                elif Game.counterAvailableFields == 1:
                    QDialog.setModal(Program.drawWindow, True)
                    Program.drawWindow.show()
                    Program.drawWindow.exec()
                    Program.positionWindowCentering(Program.drawWindow)
                    Game.setDefault()
                    Program.setDefaultFields()
                else:
                    Game.nextTurn()
                    loadedPixMap = QPixmap("content/{}_template.png".format(Game.currentRound))
                    Program.window.currentTurn.setPixmap(loadedPixMap)
        return y

    @staticmethod
    def aboutMessageButtonAction():
        QDialog.setModal(Program.aboutWindow, True)
        Program.positionWindowCentering(Program.aboutWindow)
        Program.aboutWindow.show()

    @staticmethod
    def setActions():
        boardList = Program.window.findChildren(QPushButton, QRegularExpression("board*"))
        for i in boardList:
            i.clicked.connect(Program.generateAction(i))
        Program.window.aboutProgramme.clicked.connect(Program.aboutMessageButtonAction)
        Program.winWindow.pushButton.clicked.connect(Program.winWindow.close)
        Program.drawWindow.pushButton.clicked.connect(Program.drawWindow.close)

if __name__ == "__main__":
   
    app = QApplication(sys.argv)
    
    Program.window = Program.loadWindow("content/mainWindow.ui")
    Program.winWindow = Program.loadWindow("content/winMessage.ui")
    Program.drawWindow = Program.loadWindow("content/drawMessage.ui")
    Program.aboutWindow = Program.loadWindow("content/aboutMessage.ui")
    Program.positionWindowCentering(Program.window)
    Program.winDefaultString = Program.winWindow.label.text()

    Program.setDefaultFields()
    Program.setActions()
    
    Program.window.show()
    sys.exit(app.exec())