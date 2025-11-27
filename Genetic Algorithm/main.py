from classes import *

POPULATION_COUNT = 5
MUTATION_SHARE = 0.3 # percentage of the genes to mutate (1 means mutate all genes)
MUTATION_RATE = 0.1 # percentage of the population to mutate (1 means mutate all genes)

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
        pass

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
        self.individuals: list[Chromosome]
        for _ in range(POPULATION_COUNT):
            solution = []
            for j in range(len(self.city.goal_states)):
                choice = random.randrange(len(self.city.init_states)) # random help for each incident
                solution.append((choice, j))

            self.individuals.append(
                Chromosome(self.city, solution)
            )
            



city = CityMap()

gene = Chromosome(city=city, solution=[(0, 1), (1, 0)])

print(gene)