# 📘 Genetic Algorithm for Pathfinding with Parallel Fitness Evaluation

This project implements a **Genetic Algorithm (GA)** to optimize paths between multiple start and goal locations on a grid-based city map. It integrates **A*** search as a fitness evaluation method and supports **parallel computation** for faster processing of large populations.

---

# 1. Project Overview

The project contains four files:

| File          | Description                                                                                     |
| ------------- | ----------------------------------------------------------------------------------------------- |
| `astar.py`    | Core pathfinding structures and **A*** search algorithm                                         |
| `classes.py`  | Genetic Algorithm data structures (`Chromosome`, `Population`) with parallel fitness evaluation |
| `main.py`     | GA runner                                                                                       |
| `plotting.py` | Live plotting for monitoring GA progress                                                        |

Key features:

* Supports **parallel processing** for independent fitness evaluations
* Handles dynamic traffic light penalties
* Optimizes multiple start-goal pairs
* Tracks population variance to determine convergence
* Modular, Object-Oriented design

---

# 2. File Details

## 🔹 2.1 `astar.py`

Contains the core pathfinding classes:

### Node

Represents a cell on the grid.

* Attributes:

  * `x, y`: coordinates
  * `id`: unique string
  * `cost`: base movement cost
  * `value`: S (start), G (goal), L (traffic light), or numeric cost
* Methods:

  * `get_cost(light_state)`: returns cost based on traffic light status
  * `__sub__(other)`: Manhattan distance (used in heuristic)
  * `__repr__`: human-readable representation

### CityMap

Represents the city grid.

* Stores nodes, initial positions, and goal positions.
* Methods:

  * `expand_node(x, y)`: returns neighbors (N, E, S, W)
  * `polish_map(new_init, new_goal)`: remaps start/goal for fitness calculation
  * `print_marked_path(path)`: prints a visual representation of the path

### Path

Represents a candidate path for a single start-goal pair.

* Attributes:

  * `nodes`: list of visited nodes
  * `cost`: total movement cost (g(n))
  * `f`: total A* evaluation (`g + h`)
  * `goals_reached`: goals already visited
* Methods:

  * `add_node(node)`: adds a node to the path with cost update
  * `expand_latest()`: generates new candidate paths from the last node
  * `huristic()`: heuristic for A*, based on Manhattan distance to unvisited goals
  * `print_nodes()`: prints path nodes
  * `__repr__`: prints detailed path info with cost, f-value, and marked path

### Frontier

Manages active paths for A* search.

* Methods:

  * `get_best_informed()`: returns path with lowest `f(n)`
  * `add_new_paths(paths)`: adds new paths to frontier

### A_STAR

Performs the A* search:

* Inputs: `city` (CityMap), `start` coordinates
* Returns: `Path` object with optimal path to all goals
* Expands paths iteratively until all goals are reached

---

## 🔹 2.2 `classes.py` (Genetic Algorithm)

Implements the GA and integrates **parallel fitness computation**.

### Chromosome

Represents one solution in the population.

* Attributes:

  * `city`: reference to `CityMap`
  * `adj_matrix`: assignment of starts to goals
* Methods:

  * `fitness()`: computes the cost of the worst start-goal pair using **A***. Can run in parallel across genes.
  * `mutate()`: randomly swaps start-goal assignments
  * `reproduce(other)`: creates a child by combining genes from two parents
  * `__repr__()`: prints adjacency matrix

### Population

Represents a population of `Chromosome` objects.

* Attributes:

  * `individuals`: list of `Chromosome`
* Methods:

  * `_parallel_fitness_calc()`: uses `multiprocessing.Pool` to evaluate fitness in parallel
  * `sort()`: sorts population based on fitness (uses parallel evaluation)
  * `select()`: selects the top individuals according to DEATH_RATE
  * `new_generation()`: creates next generation with selection, crossover, and mutation
  * `variance()`: computes population fitness variance using parallel evaluation

### Parallel Processing

* `compute_fitness(c)` is a standalone function for `pool.map`
* Parallelism allows **independent chromosome fitness evaluations** to run concurrently, improving performance on large populations

---

## 🔹 2.3 `main.py`

Runs the Genetic Algorithm.

1. Initializes a `CityMap` from user input.
2. Creates initial population:

   ```python
   initial_population = Population(city)
   ```
3. Iteratively runs GA until **population variance converges**:

   ```python
   while not -1 < variance < 1:
       population.individuals = population.new_generation()
       variance = population.variance()
   ```
4. Prints final fitness, variance, and best chromosome.

Supports logging, easy integration with plotting.

---

## 🔹 2.4 `plotting.py` (LivePlot)

Provides **live plotting** of population variance or other metrics.

* Class `LivePlot`:

  * `update(value)`: add a new data point and refresh plot
  * `finish()`: finalize plot at the end
* Notes:

  * Cannot be used directly with multiprocessing due to GUI thread restrictions
  * Best used when fitness evaluation is **not parallelized**, or values are gathered after parallel computation

---

# 3. Algorithm Overview

### Genetic Algorithm Flow

1. Generate initial population
2. Evaluate fitness for all individuals (**parallelized**)
3. Sort population by fitness
4. Selection: keep top individuals
5. Reproduction: combine genes from parents
6. Mutation: probabilistically modify genes
7. Repeat until population variance is low

### Fitness Evaluation (A* Integration)

* Each chromosome evaluates each gene:

  * Creates a temporary city map
  * Runs **A*** from start to goal
  * Returns the cost of the worst path (max of all genes)
* Fitness evaluation is **completely independent per gene**, enabling parallelization

---

# 4. Parallel Processing Highlights

* `multiprocessing.Pool` is used in:

  * `Population._parallel_fitness_calc()`
  * `Population.variance()`
* Benefits:

  * Significantly speeds up evaluation for large populations or maps
  * Each CPU core computes a subset of chromosomes independently
* Important:

  * Functions passed to `pool.map` must be **top-level** (`compute_fitness`)
  * Local lambdas cannot be pickled (common Python multiprocessing limitation)

---

# 5. Configuration Parameters

| Parameter          | Description                                    | Default |
| ------------------ | ---------------------------------------------- | ------- |
| `POPULATION_COUNT` | Number of individuals                          | 12      |
| `MUTATION_SHARE`   | Fraction of genes mutated                      | 0.1     |
| `MUTATION_CHANCE`  | Probability of mutation per child              | 0.1     |
| `DEATH_RATE`       | Fraction of population removed each generation | 0.2     |

---

# 6. Usage Example

```bash
python main.py
```

Sample input for `CityMap`:

```
5 7
S0012G0
010L100
...
```

Sample output:

```
Generation: 0 | Variance: 12.3
Generation: 1 | Variance: 8.7
...
Final Fitness: 15
Population Variance: 0.5
Chromosome:
0 1 0
1 0 0
...
```

---

# 7. Limitations and Notes

* LivePlot **cannot** directly plot during parallel evaluation due to GUI and multiprocessing conflicts
* Deep copies of `CityMap` are required per chromosome → memory-heavy for large maps
* Current crossover strategy is **2/3 from parent1, 1/3 from parent2**
* Traffic light timing simulated as `cost = 10` during red cycles

---

# 8. Potential Improvements

* Replace deep copies with **parent pointers**
* Optimize A* for repeated start-goal evaluation
* Add **multi-threaded or GPU-based** path evaluation
* Implement **diagonal movement** or more realistic traffic models
* Integrate **live plotting** with post-evaluation data collection

---

# 9. Conclusion

This GA project:

* Efficiently optimizes multiple start-goal paths using **parallel processing**
* Uses A* search for precise fitness evaluation
* Supports modular map input, mutation, and crossover strategies
* Is easily extensible for research or coursework

