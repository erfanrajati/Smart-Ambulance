# 📂 Pathfinding & Genetic Algorithm Repository

This repository contains two main projects related to **graph search** and **genetic algorithms**:

```
root/
│
├── GeneticAlgorithm/
│   ├── astar.py          # Core A* search and city map structure
│   ├── classes.py        # GA data structures (Chromosome, Population) with parallel fitness
│   ├── main.py           # GA runner script
│   ├── plotting.py       # Live plotting for monitoring GA evolution
│   └── README.md         # Detailed documentation for Genetic Algorithm
│
└── Graph/
    ├── classes.py        # Data structures (Node, CityMap, Path, Frontier)
    ├── main.py           # UCS and A* runner
    └── README.md         # Detailed documentation for Graph search algorithms

```

---

## 1. **Genetic Algorithm**

This folder contains a **Genetic Algorithm (GA)** implementation for optimizing multiple start-to-goal paths on a grid-based city map.

**Key Features:**

* Uses **A*** search for fitness evaluation
* Supports **parallel processing** to speed up evaluation of large populations
* Implements mutation, crossover, and selection strategies
* Tracks population variance to detect convergence
* Optional live plotting of variance trends (non-parallel mode)

**Contents:**

* `astar.py` – core A* search and city map structure
* `classes.py` – GA data structures (`Chromosome`, `Population`) with parallel fitness support
* `main.py` – GA runner
* `plotting.py` – live plotting for monitoring GA evolution

**Reference Documentation:**
For detailed explanation of the GA, parallel processing, and how each class works, see:
[Genetic Algorithm/README.md](GeneticAlgorithm/README.md)

---

## 2. **Graph**

This folder contains **graph search algorithms** for finding optimal paths on a grid-based map.

**Key Features:**

* Implements **Uniform Cost Search (UCS)** and **A*** search
* Handles multiple goal nodes and traffic light penalties
* Supports visualizing the marked path on the grid
* Object-Oriented design for nodes, paths, and frontier management

**Contents:**

* `classes.py` – data structures (`Node`, `CityMap`, `Path`, `Frontier`)
* `main.py` – UCS and A* runner

**Reference Documentation:**
For a detailed guide, class descriptions, and examples of running UCS or A*, see:
[Graph/README.md](Graph/README.md)

---

## 3. **Usage**

1. Navigate into the relevant folder:

```bash
cd GeneticAlgorithm
python main.py
```

or

```bash
cd Graph
python main.py
```

2. Each folder contains its own `README.md` with **detailed instructions, sample inputs, and expected outputs**.

---

## 4. **Repository Structure Summary**

| Folder             | Purpose                                                     | Key Features                                                                |
| ------------------ | ----------------------------------------------------------- | --------------------------------------------------------------------------- |
| `GeneticAlgorithm` | Genetic Algorithm optimization of multiple start-goal paths | Parallelized fitness, A* integration, mutation & crossover, live plotting   |
| `Graph`            | Graph search algorithms                                     | UCS & A* search, multiple goals, traffic light modeling, visual path output |

---

This setup allows users to **quickly explore either project** without confusion and provides direct links to the detailed documentation for each module.
