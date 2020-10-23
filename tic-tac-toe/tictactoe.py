import numpy as np
from neural_net import NeuralNetwork, NeuralLayer

class Game:
    def __init__(self, board, brain=None):
        self.board = np.array(board)
        if brain == None:
            inputNodes = 9
            hiddenNodes = 7
            outputNodes = 9
            self.brain = NeuralNetwork([inputNodes, hiddenNodes, outputNodes])
        else:
            self.brain = brain

    def place(self, marker, position):
        self.board[position[0]][position[1]] = marker

    def hasWon(self):
        for row in self.board:
            if all ([i == 1 for i in row]) or all ([i == 2 for i in row]):
                return row[0]
        for col in self.board.T:
            if all ([i == 1 for i in col]) or all ([i == 2 for i in col]):
                return col[0]
        rightDiagonal = [board[0,0], board[1,1], board[2,2]]
        leftDiagonal = [board[0,2], board[1,1], board[2,0]]
        if all ([i == 1 in rightDiagonal]) or all ([i == 2 in rightDiagonal]):
            return rieghtDiagonal[0]
        if all ([i == 1 in leftDiagonal]) or all ([i == 2 in leftDiagonal]):
            return leftDiagonal[0]
        return 0
    
    def think(self):
        outputs = self.brain.think(self.board.flatten().toList())
        
        while True:
            if len(outputs) > 0:
                output = self.board[outputs.index(max(outputs))//len(self.board)][outputs.index(max(outputs))%len(self.board)]
                if output != 0:
                    del outputs[outputs.index(max(outputs))]
                else:
                    return output
            else:
                return "oh noes something went wrong!!!??!?!?!1!!!!11111!?!?!?"