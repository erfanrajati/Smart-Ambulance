# 📘 Project Documentation: UCS & A-Star Pathfinding Framework

This project implements **Uniform Cost Search (UCS)** and **A*** search using a grid-based city map with obstacles, weighted nodes, and dynamic traffic light penalties. The framework is modular, Object-Oriented, and suitable for experimentation with informed vs uninformed search.

---

# 1. Overview

The project consists of two main files:

* **`classes.py`** — Core data structures

  * `Node` — cells in the map
  * `CityMap` — grid containing nodes
  * `Path` — a candidate path used by the search
  * `Frontier` — priority queue for UCS or A*

* **`main.py`** — Search algorithm runner

  * Handles input processing
  * Executes UCS or A* based on user choice
  * Logs steps to file

The implementation supports:

### ✔ Uniform Cost Search (UCS)

Uses **path cost `g(n)`** to choose next node.

### ✔ A* Search

Uses evaluation function
[
f(n) = g(n) + h(n)
]
where `h(n)` is based on the Manhattan distance to the nearest unvisited goal.

---

# 2. Class Documentation (`classes.py`)

---

## 🔹 2.1 `Node` Class

Represents a single cell on the map.

### Attributes

| Attribute | Description                                                 |
| --------- | ----------------------------------------------------------- |
| `x, y`    | Grid coordinates                                            |
| `id`      | Unique random identifier                                    |
| `cost`    | Base movement cost (1 for S, G, L; numeric for digit cells) |
| `value`   | Character or cost (S, G, L, or number)                      |

### Dynamic traffic lights

The cost of traversing a light `'L'` depends on simulated traffic cycles:

```python
light_state = (self.cost % 20) < 10
```

* First 10 time units → **green**
* Next 10 → **red (cost = 10)**

### Overloaded operators

* `__sub__`: Manhattan distance between two nodes.
  Used by the A* heuristic.

---

## 🔹 2.2 `CityMap` Class

Parses input and constructs a 2D grid of `Node` objects.

### Initialization

The constructor receives:

* `height`, `width`
* `start` → `(i, j)` coordinate of S
* `matrix` → raw textual map input

It builds:

| Field         | Description                 |
| ------------- | --------------------------- |
| `map`         | 2D list of `Node` objects   |
| `goal_states` | IDs of all goal nodes (`G`) |
| `node_index`  | ID → Node lookup            |
| `h`, `w`      | Grid size                   |
| `start`       | Start coordinate            |

### Neighbor expansion

```python
expand_node(x, y)
```

Generates neighbors in 4 directions (N, E, S, W).
Rejects out-of-bounds indices safely.

---

## 🔹 2.3 `Path` Class

Represents a **sequence of nodes** explored by the algorithm.

### Fields

| Field           | Purpose                       |
| --------------- | ----------------------------- |
| `nodes`         | Ordered list of visited nodes |
| `cost`          | Total actual path cost (g(n)) |
| `f`             | A* evaluation function        |
| `city`          | Map reference                 |
| `goals_reached` | Keeps track of visited goals  |

### Adding nodes

`add_node(node)` updates:

* Reached goals
* Traffic light penalties
* Cost from movement (including STAY option)
* Updates `f = g + h`

### Expanding the latest node

```python
expand_latest()
```

Returns all possible new paths by branching toward neighbors (including a “stay” action).

A deep copy (`copy.deepcopy`) ensures each new path is independent.

---

## 🔹 2.4 Heuristic Function

```python
huristic()
```

The heuristic for A* estimates remaining cost as:

* Count of goals not yet reached: `len(unreached_goals)`
* Multiply by **minimum Manhattan distance** to one of them

Formula:
[
h(n) = |\text{unreached goals}| \times \min(\text{Manhattan distance})
]

Properties:

* Consistent / admissible
* Scales with number of goal states

---

## 🔹 2.5 Frontier Class

Manages all active paths (the open set in graph search).

### Methods:

* `add_new_paths` → inserts new candidates
* `get_best_uninformed` → UCS priority: lowest `cost`
* `get_best_informed` → A*: lowest `f`

Frontier is essentially a manually-maintained priority queue.

---

# 3. Algorithm Documentation (`main.py`)

---

## 🔹 3.1 `ALGORITHM(city, style)`

This function implements both **Uniform Cost Search** and **A*** depending on `style`.

### Step-by-step:

1. **Initialize starting path**

   ```python
   start_path = Path(... starting node ...)
   frontier = Frontier([start_path])
   ```

2. **Main loop**
   For each iteration:

   * Pick the best path:

     ```python
     if style == 'UNINFORMED':
         best_path = frontier.get_best_uninformed()   # UCS
     elif style == 'INFORMED':
         best_path = frontier.get_best_informed()     # A*
     ```

   * Check for goal completion:

     ```python
     if len(best_path.goals_reached) == len(city.goal_states):
         return best_path
     ```

   * Expand into child paths

     ```python
     new_paths = best_path.expand_latest()
     ```

   * Add children to frontier

     ```python
     frontier.add_new_paths(new_paths)
     ```

   * Remove expanded path from frontier

     ```python
     frontier.paths.remove(best_path)
     ```

Loop continues until goals are reached.

---

## 🔹 3.2 `main()`

Handles:

* Input parsing
* Constructing the `CityMap`
* Running UCS or A*
* Redirecting logs to file
* Printing final result

A typical input map looks like:

```
6 6
GL3456
LL38S8
G2949L
LLLLLL
LL6LLG
LL44LG
```

---

# 4. Search Behavior

### ✔ Uniform Cost Search

* No heuristic
* Expands strictly based on **lowest g(n)**
* Guaranteed optimal for positive costs
* Slow for large maps

### ✔ A*

* Uses `f(n) = g(n) + h(n)`
* Much more efficient
* Still guarantees optimal path due to admissible heuristic

---

# 5. Example Output

The `Path.__repr__()` method prints:

```
------------------------
Total Cost: 16

f(n): 24

Goals Achieved: 0 | []

Marked Path: 
G L # # # 6 
L L 3 8 # 8 
G 2 9 4 9 L 
L L L L L L 
L L 6 L L G 
L L 4 4 L G 

Nodes:
((1, 4), 'S') --> ((1, 4), 'S') --> ((1, 4), 'S') --> ((0, 4), '5') --> ((0, 3), '4') --> ((0, 2), '3') --> ((0, 2), '3')
------------------------
```

This includes:

* Total cost
* Heuristic value
* Path visualization
* Node list

---

# 6. Complexity Analysis

Let:

* `b` = branching factor (up to 5 with “stay”)
* `d` = depth of optimal solution

### UCS:

[
O(b^d)
]

### A*:

[
O(b^d) \text{ in worst case}
]

But practically much faster due to heuristic pruning.

Memory usage grows with number of active paths in the frontier.

---

# 7. Potential Improvements

* Replace list-based frontier with `heapq` priority queue
* Use node-level visited set instead of full path comparison
* Avoid deep copies (use parent pointers)
* Optimize heuristic for multi-goal search
* Add diagonal movement

I can implement any of these if you want.

---

# 8. Conclusion

This project provides a fully functional grid-based search framework capable of:

* Running **Uniform Cost Search**
* Running **A-Star**
* Handling dynamic traffic light penalties
* Supporting multi-goal objectives
* Visualizing path progress

It is highly extensible for AI coursework, experimentation, or research.
