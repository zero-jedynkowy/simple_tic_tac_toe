import tictactoe.mainWindow as mainWindow
import tictactoe.draw_message as draw_message
import tictactoe.win_message as win_message
import tictactoe.about_message as about_message
import sys
import random
from PyQt5 import QtCore, QtGui, QtWidgets

class Game():
    
    def __init__(self):
        self.players = ["x", "o"]
        self.board = [['blank', 'blank', 'blank'] for _ in range(3)]
        self.currentRound = random.choice(self.players)
        self.counterAvailableFields = 9

    def resetGame(self):
        self.__init__()

    def nextTurn(self):
        if self.currentRound == self.players[0]:
            self.currentRound = self.players[1]
        else:
            self.currentRound = self.players[0]
        self.counterAvailableFields -= 1

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

class AboutMessageBox(QtWidgets.QDialog):
    counterInstances = 0
    def __init__(self, parent):
        super(AboutMessageBox, self).__init__(parent)
        self.ui = about_message.Ui_Dialog()
        self.ui.setupUi(self)
        AboutMessageBox.counterInstances += 1
        self.ui.label.mouseDoubleClickEvent = self.openSite()

    def openSite(self):
        def fun(event):
            QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://google.com'))
        return fun
        
    def show(self) -> None:
        if AboutMessageBox.counterInstances == 1:
            return super().show()

    def exec(self) -> int:
        if AboutMessageBox.counterInstances == 1:
            return super().exec()
        self.done(0)

    def done(self, a0: int) -> None:
        AboutMessageBox.counterInstances -= 1
        super().done(a0)

class WinMessageBox(QtWidgets.QDialog):
    counterInstances = 0
    def __init__(self, parent, wonPlayer):
        super(WinMessageBox, self).__init__(parent)
        self.ui = win_message.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.label.setText(self.ui.label.text().format(wonPlayer))
        self.ui.pushButton.clicked.connect(self.close)
        self.setWindowTitle(self.windowTitle().format(wonPlayer))
        WinMessageBox.counterInstances += 1
    
    def show(self) -> None:
        if WinMessageBox.counterInstances == 1:
            return super().show()

    def exec(self) -> int:
        if WinMessageBox.counterInstances == 1:
            return super().exec()
        self.done(0)

    def done(self, a0: int) -> None:
        WinMessageBox.counterInstances -= 1
        super().done(a0)

class DrawMessageBox(QtWidgets.QDialog):
    counterInstances = 0
    def __init__(self, parent):
        super(DrawMessageBox, self).__init__(parent)
        self.ui = draw_message.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)
        DrawMessageBox.counterInstances += 1

    def show(self) -> None:
        if DrawMessageBox.counterInstances == 1:
            return super().show()

    def exec(self) -> int:
        if DrawMessageBox.counterInstances == 1:
            return super().exec()
        self.done(0)

    def done(self, a0: int) -> None:
        DrawMessageBox.counterInstances -= 1
        super().done(a0)

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.game = Game()
        screenSize = QtWidgets.QApplication.primaryScreen().size()
        screenSizeList = [screenSize.width() - self.minimumWidth(), screenSize.height() - self.minimumHeight()]
        screenSizeList = [int(i/2) for i in screenSizeList]
        screenSizeList.append(self.minimumWidth())
        screenSizeList.append(self.minimumHeight())
        self.setGeometry(*screenSizeList)
        template = "self.ui.board_{}{}.mousePressEvent = self.changeContent(i, j)"
        for i in range(1, 4, 1):
            for j in range(1, 4, 1):
                exec(template.format(i, j))
        self.changePixMapFieldBoard('current_turn', '{}_template.png'.format(self.game.currentRound))
        self.ui.menuUstawienia.mousePressEvent = self.aboutTheProgramme()
    
    def aboutTheProgramme(self):
        def fun(event):
            aboutDialog = AboutMessageBox(self)
            aboutDialog.show()
            aboutDialog.exec()
        return fun
    
    def changeContent(self, row, column):
        def clickedAction(event):
            nonlocal row
            nonlocal column
            nonlocal self
            if self.game.changeField(row, column):
                self.changePixMapFieldBoard('board_{}{}'.format(row, column), '{}_template.png'.format(self.game.currentRound))
                if self.game.checkWin():
                    winDialog = WinMessageBox(self, self.game.currentRound.upper())
                    winDialog.show()
                    winDialog.exec()
                    self.game.resetGame()
                    for i in range(1, 4, 1):
                        for j in range(1, 4, 1):
                            self.changePixMapFieldBoard('board_{}{}'.format(i, j), 'blank_template.png')
                self.game.nextTurn()
                self.changePixMapFieldBoard('current_turn', '{}_template.png'.format(self.game.currentRound))
            if self.game.counterAvailableFields == 0:
                drawDialog = DrawMessageBox(self)
                drawDialog.show()
                drawDialog.exec()
                self.game.resetGame()
                for i in range(1, 4, 1):
                    for j in range(1, 4, 1):
                        self.changePixMapFieldBoard('board_{}{}'.format(i, j), 'blank_template.png')
        return clickedAction
    
    def changePixMapFieldBoard(self, name, newContent):
        template = 'self.ui.{}.setPixmap(QtGui.QPixmap("{}"))'
        exec(template.format(name, newContent))
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())