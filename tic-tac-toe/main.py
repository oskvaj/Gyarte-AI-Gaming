from world import World
from setup import *
import matplotlib.pyplot as plt

def main():
    best_fitness = []
    world = World(pop_amount, pop_size, spread)
    for i in range(25):
        world.run_generation()
        best_fitness.append(world.previous_best_fitness)
    plt.plot(best_fitness)
    plt.show()


if __name__ == "__main__":
    main()
