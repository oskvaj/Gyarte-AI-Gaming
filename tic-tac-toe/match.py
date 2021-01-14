import numpy as np

class Match:
    def __init__(self, board, players):
        self.board = np.array(board)
        self.players = players
        self.matchIsOver = False

    def place(self, marker, position):
        self.board[position[0]][position[1]] = marker

    def hasWon(self):
        for row in self.board:
            if all ([i == 1 for i in row]) or all ([i == 2 for i in row]):
                return row[0]
        for col in self.board.T:
            if all ([i == 1 for i in col]) or all ([i == 2 for i in col]):
                return col[0]
        rightDiagonal = [self.board[0,0], self.board[1,1], self.board[2,2]]
        leftDiagonal = [self.board[0,2], self.board[1,1], self.board[2,0]]
        if all ([i == 1 for i in rightDiagonal]) or all ([i == 2 for i in rightDiagonal]):
            return rightDiagonal[0]
        if all ([i == 1 for i in leftDiagonal]) or all ([i == 2 for i in leftDiagonal]):
            return leftDiagonal[0]
        if 0 in self.board:
            return 0
        else:
            return 1
        return 0

    def play(self):
        while not self.matchIsOver:
            for player in self.players:
                self.place(player.marker, player.think())
                if self.hasWon() == player.marker:
                    #player has won
                    player.fitness +=1
                    self.matchIsOver = True
                    break
                elif self.hasWon == 0:
                    self.matchIsOver = True