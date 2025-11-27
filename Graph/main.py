from classes import *
import sys

def ALGORITHM(city: CityMap, style):
    i, j = city.start

    # start from i, j
    start_path = Path(city=city, nodes=[city.map[i][j]], cost=1)

    # update frontier
    frontier = Frontier()
    frontier.add_new_paths(paths=[start_path])

    i = 0
    while True:
        i += 1
        print(f"\n\n########-------- iteration {i} --------########\n\n")
        
        # choose best path
        if style == 'UNINFORMED':
            best_path = frontier.get_best_uninformed()
        elif style == 'INFORMED':
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


def main():
    h, w, s, city = CityMap.get_input()
    city = CityMap(h, w, s, city)

    sys.stdout = open('./UCS.log', 'w')
    result_ucs = ALGORITHM(city, 'UNINFORMED')

    print()
    print("###############################      UCS")
    print(result_ucs)

    sys.stdout = open('./A-Star.log', 'w')
    result_astar = ALGORITHM(city, 'INFORMED')

    print()
    print("###############################       A*")
    print(result_astar)
    
    # path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (1, 3)]
    # nodes = []
    # for x, y in path:
    #     nodes.append(city.map[x][y])
    
    # path = Path(city, nodes)
    # print(path)



if __name__ == "__main__":
    main()
