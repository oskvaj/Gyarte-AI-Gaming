from food import Food
from neural_net import NeuralNetwork, NeuralLayer
from math import sqrt
import numpy as np
import math
import world
from setup import hidden_layers

class Snake():
    def __init__(self, board_size, brain=None):
        if brain == None:
            _input_nodes = 5
            _output_nodes = 4
            self.brain = NeuralNetwork([_input_nodes] + hidden_layers + [_output_nodes])
        else:
            self.brain = brain

        self.direction = "up"

        self.growcount = 1

        self.death_cause = "None"

        self.board_size = board_size
        self.x = self.board_size//2
        self.y = self.board_size//2

        self.alive = True

        self.length = 5
        self.food = Food(self.board_size)

        self.lifetime = 0
        self.fitness = 0

        self.tail = [
            [self.x, self.y - 4],
            [self.x, self.y - 3],
            [self.x, self.y - 2],
            [self.x, self.y - 1]
            ]

        self.vector = []

        self.left_to_live_start = 200
        self.left_to_live = self.left_to_live_start

        self.parts = [
            [self.x, self.y - 4],
            [self.x, self.y - 3],
            [self.x, self.y - 2],
            [self.x, self.y - 1],
            [self.x, self.y]
            ]

        # Add food positions and lengths for each move
        self.move_history = {"fitness":self.fitness, "moves":self.parts, "food_position":[[self.food.x, self.food.y] for i in range(len(self.parts))], "length":[self.length for i in range(len(self.parts))] }

    
    def think(self):
        outputs = self.brain.think(self.look()).flatten().tolist()
        self.direction = ["up", "down", "left", "right"][outputs.index(max(outputs))]

    def move(self):
        #vector = [delta_x, delta_y]
        self.lifetime += 1
        
        self.left_to_live -= 1

        if self.left_to_live <= 0:
            self.alive = False
            self.death_cause = "timeout"
            world.timeout += 1

        if self.direction == "up":
            self.vector = [0, -1]

        elif self.direction == "down":
            self.vector = [0, 1]
        
        elif self.direction == "left":
            self.vector = [-1, 0]
        
        elif self.direction == "right":
            self.vector = [1, 0]

        if self.x == self.food.x and self.y == self.food.y:
            self.eat()
            while([self.food.x, self.food.y] in self.tail):
                self.food.respawn()

        if [self.x, self.y] in self.tail:
            self.alive = False
            self.death_cause = "ranIntoSelf"
            world.ranIntoSelf += 1

        if self.x >= self.board_size or self.y >= self.board_size or self.x < 0 or self.y < 0:
            self.alive = False
            self.death_cause = "wallCrash"
            world.wallCrash += 1

        if self.alive:
            #Add new part
            self.tail.insert(0, [self.x, self.y])

            #Remove last tail part
            self.tail.pop()

            self.x += self.vector[0]
            self.y += self.vector[1]

            self.move_history["moves"].append([self.x, self.y])
            self.move_history["food_position"].append([self.food.x, self.food.y])
            self.move_history["length"].append(self.length)



    def eat(self):
        for _ in range(self.growcount):
            
            self.length += 1
            #Append tail so this part is removed instead of actual tail
            self.tail.append([-1,-1])

        self.left_to_live = self.left_to_live_start
        self.food.respawn()
    
    def calc_fitness(self):
        self.fitness = self.lifetime * self.lifetime * 2**math.floor(self.length)
        self.fitness = self.lifetime + (2**(self.length-5) + ((self.length-5)**2.1)*500) - (((self.length-5)**1.2)*((0.25*self.lifetime)**1.3))
        self.move_history["fitness"] = self.fitness
        
        return self.fitness

        
    def look(self):

        #Left, right, up, food
        inputs = [0, 0, 0, 0, 0]
        if [self.x-1, self.y] in self.tail:
            inputs[0] = 1
        
        if [self.x+1, self.y] in self.tail:
            inputs[1] = 1

        if [self.x, self.y-1] in self.tail:
            inputs[2] = 1

        if [self.x, self.y+1] in self.tail:
            inputs[3] = 1
        inputs[4] = np.arctan2((self.x - self.food.x), (self.y - self.food.y))/360


        
        """
        base_value = 0

        distances = [
            [base_value, base_value, base_value, base_value, base_value, base_value, base_value, base_value],
            [base_value, base_value, base_value, base_value, base_value, base_value, base_value, base_value],
            [base_value, base_value, base_value, base_value, base_value, base_value, base_value, base_value]
        ]


        ###### DEPRECATED ######### Wall and Tail combined into one
        # Check distance to the walls
        # These are the first 8 distances

        # UP
        # Top wall position is 0, so the y postion should be the distance
        #distances[0][0] = self.y

        # DOWN
        # Bottom wall position is the board size, so the distance should be board size - current position
        #distances[0][1] = self.board_size - self.y

        # LEFT
        # Left wall is 0, so the x postion should be the distance
        #distances[0][2] = self.x

        # RIGHT
        # Right wall is board size, so the distance should be board size - current position
        #distances[0][3] = self.board_size - self.x
        ###### DEPRECATED #########

        # DOWN-LEFT
        #TEST, SHOW DIRECTION OF FOOD

        # self.x < food_x = food is to the right
        # self.x > food_x = food is left
        # self.y < food_y = food is below
        # self.y > food_y = food is above
        if self.x < self.food.x and self.y < self.food.y:
            distances[0] = [2 for i in range(len(distances[0]))]

        if self.x > self.food.x and self.y < self.food.y:
            distances[0] = [4 for i in range(len(distances[0]))]

        if self.x < self.food.x and self.y > self.food.y:
            distances[0] = [8 for i in range(len(distances[0]))]

        if self.x > self.food.x and self.y > self.food.y:
            distances[0] = [10 for i in range(len(distances[0]))]
        # DOWN-RIGHT

        # UP-LEFT

        # UP-RIGHT


        # Check distance to an obstacle (Wall and Tail)
        # These are the second 8 distances

        # UP
        # Find the closest distance of the parts that is above the current y position and is on the same x pos
        distances[1][0] = min([self.y - part[1] for part in self.tail if self.y > part[1] and self.x == part[0]] + [base_value])

        # Wall
        distances[1][0] = min(self.y, distances[1][0])

        # DOWN
        # Find the closest part that is below the current y position and is on the same x pos

        distances[1][1] = min([part[1] - self.y for part in self.tail if self.y < part[1] and self.x == part[0]] + [base_value])
         # Wall
        distances[1][1] = min(self.board_size - self.y, distances[1][1])


        # LEFT
        # Find the closest part that is to the left of the current x pos and on the same y pos

        distances[1][2] = min([self.x - part[0] for part in self.tail if self.x > part[0] and self.y == part[1]] + [base_value])
        # Wall
        distances[1][2] = min(self.x, distances[1][2])

        # RIGHT
        # Find the closest part that is to the right of the current x pos and on the same y pos

        distances[1][3] = min([part[0] - self.x for part in self.tail if self.x < part[0] and self.y == part[1]] + [base_value])
        # Wall
        distances[1][3] = min(self.board_size - self.x, distances[1][3])



        # Diagonals
        if (any([abs(part[0] - self.x) == abs(part[1] - self.y) for part in self.tail])):
            # DOWN-LEFT
            distances[1][4] = min([(abs(part[0] - self.x) + abs(part[1] - self.y)) if part[0] > self.x and part[1] < self.y else base_value for part in self.tail])

            # DOWN-RIGHT
            distances[1][5] = min([(abs(part[0] - self.x) + abs(part[1] - self.y)) if part[0] > self.x and part[1] > self.y else base_value for part in self.tail])

            # UP-LEFT
            distances[1][6] = min([(abs(part[0] - self.x) + abs(part[1] - self.y)) if part[0] < self.x and part[1] < self.y else base_value for part in self.tail])

            # UP-RIGHT
            distances[1][7] = min([(abs(part[0] - self.x) + abs(part[1] - self.y)) if part[0] < self.x and part[1] > self.y else base_value for part in self.tail])


        # Check distances to food
        # These are the third 8 distances

        # UP
        # Check if the food is at the same x then if it is upwards then assign the distance otherwise assign the base value
        distances[2][0] = (self.y - self.food.y) if self.food.x == self.x and self.y > self.food.y else base_value 

        # DOWN
        # Check if the food is at the same x then if it is downards the assign the distance otherwise assign the base value
        distances[2][1] = (self.food.y - self.y) if self.food.x == self.x and self.y < self.food.y else base_value

        # LEFT
        # Check if the food is at the same y then if it is to the left assign the distance otherwise assign the base value
        distances[2][2] = (self.x - self.food.x) if self.food.y == self.y and self.x > self.food.x else base_value

        # RIGHT
        # Check if the food is at the same y then if it is to the right assign the distance otherwise assign the base value
        distances[2][3] = ( self.food.x - self.x) if self.food.y == self.y and self.x < self.food.x else base_value
        
        if abs(self.food.x - self.x) == abs(self.food.y - self.y):
        
            # DOWN-LEFT
            if (self.food.x > self.x and self.food.y < self.y):
                distances[2][4] = abs(self.food.x - self.x) + abs(self.food.y - self.y)

            # DOWN-RIGHT
            if (self.food.x > self.x and self.food.y > self.y):
                distances[2][5] = abs(self.food.x - self.x) + abs(self.food.y - self.y)

            # UP-LEFT
            if (self.food.x < self.x and self.food.y < self.y):
                distances[2][6] = abs(self.food.x - self.x) + abs(self.food.y - self.y)

            # UP-RIGHT
            if (self.food.x < self.x and self.food.y > self.y):
                distances[2][7] = abs(self.food.x - self.x) + abs(self.food.y - self.y)


        # Distances is 3x8 dimensional matrix
        # Make it into a column vector instead
        distances = np.array(distances).reshape(1, -1) 
        print(distances)
        assert(distances.shape == (1, 24))
        """
        inputs = np.array(inputs).reshape(1, -1)
        return inputs

    def mutate(self):
        self.brain.mutate()
    
    def crossover(self, other_parent):

        # Create 2 children
        children_brains = self.brain.crossover(other_parent.brain)
        children = []
        
        for child_brain in children_brains:
            children.append(Snake(self.board_size, child_brain))
        
        return children
