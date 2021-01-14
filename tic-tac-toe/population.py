from tictactoe import Player
from match import Match
from numpy import random, array
generator = random.default_rng()

class population():
    def __init__(self, popSize, spread, size):
        self.popSize = popSize
        self.count = 0
        self.spread = spread

        self.population = [Match([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [Player(), Player()]) for i in range(popSize)]
        self.popFitness =1 

    def Natural_selection(self):
        new_players = []

        # First child of new array is the best player of previous generation without mutation
        best_player = self.select_best_player()

        # Create new player with previous players brain to remove move history and such
        new_best_player = Player(best_player.brain)

        new_players.append(new_best_player)
        
        crossing_players = True

        parents = self.select_mating_pool(int(len(self.population)) +1)
        index = 0
        while crossing_players:
            parent1 = parents[index]
            index += 1

            parent2 = parents[index]
            index += 1

            children = parent1.crossover(parent2)
            for child in children:
                if len(new_players) < self.popSize:
                    child.mutate()
                    new_players.append(child)    
                else:
                    crossing_players = False
                    break
            
            self.population = new_players

        
    def calc_fitness(self):
        self.popFitness = 0
        for player in self.population:
            if player.alive:
                return True
        return False    

    def select_mating_pool(self, num_of_parents):
        
         # Select a random snake with higher probability for snakes with high fitness

        self.population.sort(key=lambda x:x.fitness, reverse=True)

        probabilities = []
        for index, _ in enumerate(self.population):
            probabilities.append((self.spread**index))

        probabilities = array(probabilities)/sum(probabilities)

        return random.choice(self.population, num_of_parents, p=probabilities)
        


    def select_player(self):



        # Select a random plaeyr from the amount of fitness from each player
        # Since fitness is exponential it will pick the ones with higher fitness more often than not
        # Creates genetic diversity

        rand = random.randint(0, self.popFitness)

        runningSum = 0

        for player in self.population:
            runningSum += player.fitness
            if rand <=runningSum:
                return player
        

    def get_random_player(self):
        return self.population[random.randint(0, len(self.population))]
    
    def select_best_player(self):
        best_player = self.population[0]

        for player in self.population:
            if player.fitness > best_player.fitness:
                best_player = player
        return best_player
    
    def average_fitness(self):
        total = 0
        for player in self.population:
            total += player.fitness

        total /= len(self.population)
        return total