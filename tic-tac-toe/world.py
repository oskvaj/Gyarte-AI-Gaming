from population import Population

class World():
    def __init__(self, amount_of_populations, population_size, spread):
        self.amount_of_populations = amount_of_populations
        self.population_size = population_size
        self.spread = spread
        self.species = [Population(population_size, spread) for i in range(amount_of_populations)]
        self.previous_best_fitness = 0

    def run_generation(self):
        for population in self.species:
            population.play()

        best_player = self.best_player()
        print(f"The best fitness was: {best_player.fitness} (W:{best_player.wins} D:{best_player.draws} L:{(best_player.total_matches - best_player.draws - best_player.wins)} TOTAL:{best_player.total_matches})")
        self.previous_best_fitness = best_player.fitness
        print("Commencing Natural Selection")
        self.natural_selection()
    
    def natural_selection(self):
        for population in self.species:
            population.natural_selection()

    def is_done(self):
        for population in self.species:
            if not population.is_done():
                return False
        return True
    
    def average_fitness(self):
        total = 0
        for pop in self.species:
            total += pop.average_fitness()
        total /= len(self.species)
        return total
    
    def best_player(self):
        best_player = self.species[0].get_random_player()

        for pop in self.species:
            new_player = pop.select_best_player()
            if new_player.fitness > best_player.fitness:
                best_player = new_player
        return best_player
