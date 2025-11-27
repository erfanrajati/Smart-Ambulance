import copy
import random
import string


class Node:
    def __init__(self, x, y, cost, value):
        def random_string(length=12):
            chars = string.ascii_letters + string.digits
            return ''.join(random.choice(chars) for _ in range(length))
        
        self.x = x
        self.y = y
        self.id = random_string()
        self.cost = cost
        self.value = value

    def get_cost(self, light_state):
        if self.value == 'L' and not light_state: # if the node is a traffic light and the light is red
            return 10
        else:
            return self.cost # already set 1 for G and S locations

    def __repr__(self):
        return str(((self.x, self.y), str(self.value)))

    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
        

class CityMap:
    def __init__(self):
        self.goal_states = []
        self.init_states = []
        self.node_index: dict[str, Node] = dict()
        # self.start = start
        x, y = map(int, input().split())
        self.h = x
        self.w = y
        self.map: list[list[Node]] = [
            [None for _ in range(y)] 
            for _ in range(x)
        ]
        for i in range(x):
            row = input()
            for j in range(y):
                cost = None
                value = None
                cell = row[j]
                try:
                    cost = int(cell)
                    value = cost
                except:
                    if cell in ('S', 'G', 'L'):
                        cost = 1
                        value = cell
                finally:
                    new_node = Node(i, j, cost, value)
                    self.map[i][j] = new_node
                    if cell == 'G':
                        self.goal_states.append(new_node.id)
                    elif cell == 'S':
                        self.init_states.append(new_node.id)

                    self.node_index[new_node.id] = new_node
    
    def expand_node(self, x, y):
        dirs = [(x-1, y), (x, y+1), (x+1, y), (x, y-1)]
        children: list[Node] = []
        for i, j in dirs:
            if i < 0 or j < 0: # Bypass Python's reverse indexing feature
                continue
            try: 
                children.append(self.map[i][j])
            except IndexError: # Skip out or range indices
                continue
        return children

    def polish_map(self, new_init: tuple[int, int], new_goal: tuple[int, int]):
        for i in range(self.h):
            for j in range(self.w):
                value = self.map[i][j].value
                if value == 'S':
                    if i == new_init[0] and j == new_init[1]:
                        continue
                    else:
                        self.map[i][j].value = 1
                elif value == 'G':
                    if i == new_goal[1] and j == new_goal[1]:
                        continue
                    else:
                        self.map[i][j].value = 1

        self.init_states = [self.map[new_init[0]][new_init[1]].id]
        self.goal_states = [self.map[new_goal[0]][new_goal[1]].id]


    def __repr__(self):
        for row in self.map:
            for node in row:
                print(node.value, end = ' ')
            print()

        return ''
    
    def print_marked_path(self, path):
        for i, row in enumerate(self.map):
            for j, node in enumerate(row):
                if (i, j) in path:
                    print('#', end=' ')
                else:
                    print(node.value, end = ' ')
            print()

        return ''


class Path:
    def __init__(self, city: CityMap, nodes: list[Node] = None, cost = 0):
        self.nodes:list[Node] = nodes if nodes is not None else []
        self.cost = cost
        self.f = 10e16
        self.city = city
        self.goals_reached = []

    def add_node(self, node: Node):
        if node.value == 'G' and node.id not in [n.id for n in self.nodes]: # Do not count a goal state twice
            self.goals_reached.append(node.id)
        
        if self.nodes and node.id == self.nodes[-1].id: # In case of STAY
            self.cost += 1
        else:
            light_state = (self.cost % 20) < 10 # True means green and False means red
            self.cost += node.get_cost(light_state)
        
        self.f = self.cost + self.huristic() # f(n) = g(n) + h(n)
        self.nodes.append(node)
    
    def expand_latest(self):
        latest = self.nodes[-1]
        children = self.city.expand_node(latest.x, latest.y)
        children.append(latest)
        new_paths = []
        for node in children:
            if node.id == latest.id: # STAY should be considered
                pass
            elif node.id in [n.id for n in self.nodes]: # Do not consider nodes that are already visited,
            # if node.id in [n.id for n in self.nodes]: # Do not consider nodes that are already visited,
                continue

            new_path = copy.deepcopy(self)
            new_path.add_node(node)
            new_paths.append(new_path)
        
        return new_paths
    
    def huristic(self):
        not_reached_goals = [self.city.node_index[s] for s in self.city.goal_states if s not in self.goals_reached]
        if not not_reached_goals:
            return 0
        return len(not_reached_goals) * min(map(lambda s: self.nodes[-1] - s, not_reached_goals)) # subtraction is overloaded in Node class to calculate Manhatan Distance
        
    def print_nodes(self):
        print(*self.nodes, sep=' --> ')
    
    def __repr__(self):
        print()
        print("------------------------")
        print(f"Total Cost: {self.cost}")
        print()
        print(f"f(n): {self.f}")
        print()
        print(f"Goals Achieved: {len(self.goals_reached)} | {[self.city.node_index[s] for s in self.goals_reached]}")
        print()
        print('Marked Path: ')
        self.city.print_marked_path(
            path=[(n.x, n.y) for n in self.nodes]
        )
        print()
        print("Nodes:")
        self.print_nodes()
        print("------------------------")

        return ''


class Frontier:
    def __init__(self, paths: list[Path] = None):
        self.paths = paths if paths is not None else []
    
    def get_best_informed(self):
        best = min(self.paths, key=lambda p: p.f)
        # print(best)
        return best
    
    def add_new_paths(self, paths: list[Path]):
        for p in paths:
            self.paths.append(p)


def A_STAR(city, start):
    i, j = start
# start from i, j
    start_path = Path(city=city, nodes=[city.map[i][j]], cost=1)

    # update frontier
    frontier = Frontier()
    frontier.add_new_paths(paths=[start_path])

    i = 0
    while True:
        i += 1
        
        # choose best path
        best_path = frontier.get_best_informed()
        
        # check if the goal is achieved
        if len(best_path.goals_reached) == len(city.goal_states):
            return best_path
        
        # expand best path
        new_paths = best_path.expand_latest()

        # update frontier
        frontier.add_new_paths(paths=new_paths)

        # remove old path
        frontier.paths.remove(best_path)