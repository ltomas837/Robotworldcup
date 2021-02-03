from solvers.modelisation.Graph import Graph
import itertools

def sort_by_values_len(dict):
    dict_len = {key: len(value) for key, value in dict.items()}
    import operator
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)

    dico = {}
    for item in sorted_key_list:
        dico[item[0]] = dict[item [0]]

    return dico

def run(problem):
    graph = Graph(problem)
    adjacency_list = graph.adjacency_list_from_positions
    positions = graph.positions

    listOfDefenders = []
    for i in range(len(adjacency_list)):
        if adjacency_list[i] != []:
            listOfDefenders.append(i)

    setOfDefenders = []
    shootList = [ z for z in range(graph.adjacency_list_from_attempts.size)]

    shootListForDefender = []
    for index in listOfDefenders[:]:
        shootListForDefender.append(adjacency_list[index])

    dico = dict(zip([n for n in listOfDefenders], shootListForDefender))
    dico = sort_by_values_len(dico)

    isFinished = False
    shot_covered = []

    while not isFinished:
        for defender, shots in dico.items():
            for shot in shots:
                if shot not in shot_covered:
                    shot_covered.append(shot)

                    if defender not in setOfDefenders:
                        setOfDefenders.append(defender)

        if len(shot_covered) == len(shootList):
            isFinished = True
            break

    isFinished = False

    set_size = 1
    solution = []

    while not isFinished :
        minimalSetOfDefenders = list(itertools.combinations(range(len(setOfDefenders)), set_size))
        for defenders in minimalSetOfDefenders:
            shot_covered = []
            for defender in defenders :
                for shoot in dico[setOfDefenders[defender]]:
                    if shoot not in shot_covered:
                        shot_covered.append(shoot)
            if len(shot_covered) == len(shootList):
                isFinished = True
                for index in defenders:
                    solution.append(setOfDefenders[index])
                break

        if set_size < len(setOfDefenders):
            set_size += 1
        else :
            isFinished = True

    # Dump data in JSON file
    defenderPos = { "defenders": [] }
    for index in solution:
        defenderPos.get("defenders", []).append(positions[index])

    return defenderPos
