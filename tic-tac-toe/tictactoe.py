import numpy as np
from neural_net import NeuralNetwork, NeuralLayer

class Player:
    def __init__(self, brain=None):
        self.marker = "X"
        self.fitness = 0
        if brain == None:
            inputNodes = 9
            hiddenNodes = 7
            outputNodes = 9
            self.brain = NeuralNetwork([inputNodes, hiddenNodes, outputNodes])
        else:
            self.brain = brain
    
    def think(self):
        outputs = self.brain.think(self.board.flatten().tolist())

        while True:
            if len(outputs) > 0:
                #Output gives the marker on position
                output = self.board[outputs.index(max(outputs))//len(self.board)][outputs.index(max(outputs))%len(self.board)]
                if output != 0:
                    del outputs[outputs.index(max(outputs))]
                else:
                    return [outputs.index(max(outputs))//len(self.board), outputs.index(max(outputs))%len(self.board)]
            else:
                return "oh noes something went wrong!!!??!?!?!1!!!!11111!?!?!?"

    def calc_fitness(self):
            #TODO: implement fittness to be if the ai won or not and in how many moves it won?
            self.fitness = self.lifetime * self.lifetime * 2**math.floor(self.length)
            self.fitness = self.lifetime + (2**(self.length-5) + ((self.length-5)**2.1)*500) - (((self.length-5)**1.2)*((0.25*self.lifetime)**1.3))
            self.move_history["fitness"] = self.fitness
            
            return self.fitness

    def mutate(self):
            self.brain.mutate()
        
    def crossover(self, other_parent):

        # Create 2 children
        children_brains = self.brain.crossover(other_parent.brain)
        children = []
        
        for child_brain in children_brains:
            children.append(Snake(self.board_size, child_brain))
        
        return children
