import random

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