from solvers.modelisation.Graph import Graph
import itertools

def run(problem):
    graph = Graph(problem)
    adjacency_list = graph.adjacency_list_from_positions

    shootList = [ z for z in range(graph.adjacency_list_from_attempts.size)]
    isFinished = False

    set_size = 1
    solution = []
     
    while not isFinished :
        setOfDefenders = list(itertools.combinations(range(len(adjacency_list)), set_size))
        for defenders in setOfDefenders:
            shot_covered = []
            for defender in defenders :
                for shoot in adjacency_list[defender]:
                    if shoot not in shot_covered:
                        shot_covered.append(shoot)
            
            if len(shot_covered) == len(shootList):
                isFinished = True
                solution = defenders
                break
        
        if set_size < len(adjacency_list):
            set_size += 1
        else :
            isFinished = True

    defenderPos = {"defenders": []}

    for position in solution:
        defenderPos.get("defenders", []).append(graph.positions[position])
    
    return defenderPos

