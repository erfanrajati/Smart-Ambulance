from astar import *
from multiprocessing import Pool
import numpy as np


POPULATION_COUNT = 20
MUTATION_SHARE = 0.1 # percentage of the genes to mutate (1 means mutate all genes)
MUTATION_CHANCE = 0.1 # chance for each individual to be mutated (1 means mutate all genes)
DEATH_RATE = 0.3 # percentage of the population who die on each selection

def compute_fitness(c):
    return c, c.fitness()


class Chromosome:
    def __init__(self, city: CityMap, solution: list):
        self.city = city
        self.width = len(self.city.goal_states)
        self.height = len(self.city.init_states)
        self.adj_matrix = [
            [0 for _ in range(self.width)]
            for _ in range(self.height)
        ]
        for i, j in solution:
            self.adj_matrix[i][j] = 1
    
    def mutate(self):
        genes_to_mutate = set(random.sample(range(self.width), round(self.width * MUTATION_SHARE)))
        for gene in genes_to_mutate:
            old_help = [row[gene] for row in self.adj_matrix].index(1)
            new_help = random.randrange(self.height)
            self.adj_matrix[old_help][gene] = 0
            self.adj_matrix[new_help][gene] = 1

    def fitness(self):
        # generate a city map that only includes start and goal for one gene
        # calculate the final cost of that gene
        # return the worst cost of all genes
        all_genes_fitnesses = []
        for i in range(self.width):
            gene = list(map(lambda row: row[i], self.adj_matrix))

            init_node_id = self.city.init_states[gene.index(1)] # reminder: only one item is 1 in each gene
            init_node = self.city.node_index[init_node_id]
            init_coords = (init_node.x, init_node.y)

            goal_node_id = self.city.goal_states[i]
            goal_node = self.city.node_index[goal_node_id]
            goal_coords = (goal_node.x, goal_node.y)

            new_city = copy.deepcopy(self.city)
            new_city.polish_map(init_coords, goal_coords)

            # run A-STAR on new map
            all_genes_fitnesses.append(
                A_STAR(new_city, start=init_coords).cost
            )

            del new_city
        
        return max(all_genes_fitnesses)


    def reproduce(self, other):
        get_from_self = set(random.sample(range(self.width), self.width * 2 // 3)) # get random genes from parent 1, can be 2/3rd of all the genes at most
        get_from_other = set([i for i in range(self.width) if i not in get_from_self]) # rest of the genes from parent 2
        new_solution = []

        for gene in get_from_self:
            targe_help = [row[gene] for row in self.adj_matrix].index(1)
            new_solution.append((targe_help, gene))

        for gene in get_from_other:
            targe_help = [row[gene] for row in other.adj_matrix].index(1)
            new_solution.append((targe_help, gene))
        
        return Chromosome(self.city, new_solution)
    
    def __repr__(self):
        result = '\n'.join(' '.join(str(c) for c in row) for row in self.adj_matrix)
        return result
    

class Population:
    def __init__(self, city: CityMap):
        self.city = city
        self.individuals: list[Chromosome] = []
        for _ in range(POPULATION_COUNT):
            solution = []
            for j in range(len(self.city.goal_states)):
                choice = random.randrange(len(self.city.init_states)) # random help for each incident
                solution.append((choice, j))

            self.individuals.append(
                Chromosome(self.city, solution)
            )
    
    def _normal_sort(self):
        return sorted(self.individuals, key=lambda c: c.fitness(), reverse=True)

    def _parallel_fitness_calc(self):
        with Pool() as pool:
            fitnesses = pool.map(compute_fitness, self.individuals)
        
        return fitnesses
    
    def sort(self):
        fitnesses = self._parallel_fitness_calc()
        fitnesses.sort(key=lambda x: x[1])
        return [c for c, f in fitnesses[::-1]]

    def select(self):
        # sorted_population = self._normal_sort()
        sorted_population = self.sort()

        l = len(sorted_population)
        return sorted_population[round(l * DEATH_RATE) : ]
    
    def new_generation(self):
        selected_population = self.select()

        new_count = len(self.individuals) - len(selected_population) # how many new individuals should be created
        children = []
        for _ in range(new_count):
            parent1, parent2 = random.sample(selected_population, 2)
            child = parent1.reproduce(parent2)

            mutation = random.uniform(0.0, 1.0) < MUTATION_CHANCE
            if mutation:
                child.mutate()

            children.append(child)
        
        return selected_population + children
    
    def variance(self):
        with Pool() as pool:
            fitnesses = pool.map(compute_fitness, self.individuals)
        
        fitnesses = [f[1] for f in fitnesses]
        return float(np.var(fitnesses))

