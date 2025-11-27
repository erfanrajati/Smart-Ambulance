from astar import CityMap
from classes import Population

def GENETIC_ALGORITHM():
    city = CityMap()
    initial_population = Population(city)
    variance = initial_population.variance()
    
    population = initial_population
    while not -1 < variance < 1:
        print(variance)
        population.individuals = population.new_generation() # selection, mutation, death rate consideration
        variance = population.variance()
    
    result = population._normal_sort()[0]

    print("Final Fitness:", result.fitness())
    print("Population Variance:", variance)
    print(result)


if __name__ == "__main__":
    GENETIC_ALGORITHM()