from world import World
import cProfile
import matplotlib.pyplot as plt
import neural_net
import time
from setup import *

def main():
    neural_net.global_mutation_chance = global_mutation_chance

    for i in range(1, 2):
        print("Iteration " + str(i))

        world = World(board_size, pop_amount, pop_size, spread)
        average_fitness = []
        best_fitness = []
        highest_food = []


        while True:
            if world.make_moves():
                continue
            else:
                average_fitness.append(world.prev_average_fitness)
                best_fitness.append(world.prev_best_fitness)
                highest_food.append(world.prev_best_food)

                if world.generation >= 250:
                    fig, axs = plt.subplots(3)
                    axs[0].plot(highest_food)
                    axs[0].legend(["Food"])
                    axs[1].plot(average_fitness)
                    axs[1].legend(["Average fitness"])
                    axs[2].plot(best_fitness)
                    axs[2].legend(["Best fitness"])
                    fig.suptitle("Snake")
                    break

    #plt.legend([0.9 + i/100 for i in range(1, 11)])
    plt.show()

if __name__ == "__main__":
    #cProfile.run("main()", sort="cumulative time")

    main()