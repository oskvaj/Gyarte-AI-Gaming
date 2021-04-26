import numpy as np
from neural_net import NeuralNetwork, NeuralLayer

class Player:
    def __init__(self, brain=None):
        self.marker = None

        self.fitness = 0
        if brain == None:
            inputNodes = 9
            hiddenNodes = 7
            outputNodes = 9
            self.brain = NeuralNetwork([inputNodes, hiddenNodes, outputNodes])
        else:
            self.brain = brain

        self.wins = 0
        self.draws = 0
        self.total_matches = 0
    
    def think(self, board):
        outputs = self.brain.think(board.flatten().reshape(1, -1))

        sorted_outputs = sorted(outputs[0], reverse=True)

        outputs = outputs.reshape(3, 3)
        tried_positions = []

        for output in sorted_outputs:
            
            indexes_of_highest_value = np.asarray(np.where(outputs==output)).T
            index = indexes_of_highest_value[0]

            indexes_tried = 0
            if len(tried_positions) > 0:
                for pos in tried_positions:
                    if all(index == pos):
                        index = indexes_of_highest_value[indexes_tried+1]
                        indexes_tried += 1

            marker_on_position = board[index[0], index[1]]

            if marker_on_position != 0:
                # Spot is already occupied
                # Check next highest choice
                tried_positions.append(index)
                continue
            else:
                # Return the index of the highest value adjusted for the board shape
                return index
            
        # If there are no legal moves left, return None
        # The script should never reach this point due to the order in which draws are checked.
        if len(tried_positions) >= board.size:
            return None


    def mutate(self):
        self.brain.mutate()
        
    def crossover(self, other_parent):

        # Create 2 children
        children_brains = self.brain.crossover(other_parent.brain)
        children = []
        
        for child_brain in children_brains:
            children.append(Player(child_brain))
        
        return children
