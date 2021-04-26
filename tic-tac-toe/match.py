import numpy as np

class Match:
    def __init__(self, players):
        self.board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.players = players
        self.players[0].marker = 1
        self.players[1].marker = 2

        self.is_done = False

    def place(self, marker, position):
        self.board[position[0], position[1]] = marker

    def has_won(self):
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
            # No one has won and there are moves left
            return "NO_WINNER"
        else:
            # No moves left and no one has won
            return "DRAW"

    def play(self):
        while not self.is_done:
            for player in self.players:
                
                position_to_place = player.think(self.board)
                self.place(player.marker, position_to_place)

                if self.has_won() == player.marker:
                    player.fitness += 1
                    player.wins += 1
                    self.is_done = True
                    break

                elif self.has_won() == "DRAW":
                    player.draws += 1
                    player.fitness += 0.5
                    self.is_done = True
                    break
