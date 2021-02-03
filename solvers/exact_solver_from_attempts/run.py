from solvers.modelisation.Graph import Graph
import numpy as np

def nullCounter(counter, length):
    for c in range(length):
        if counter[length-1-c] != 0:
            return False
    return True

def decreaseCounter(counter, baseCounter, length):
    index = length-1
    changedIndex = np.empty(0, dtype=int)
    while (index != 0):
        if counter[index] == 0:
            counter[index] = baseCounter[index]
            changedIndex = np.append(changedIndex, index)
        else:
            break
        index -= 1
    counter[index] -=1
    changedIndex = np.append(changedIndex, index)
    return changedIndex


def notIn(element, list):
    for i in range(list.size):
        if (list[i][1] == element):
            return True;
    return False;

def copy(list, exeptions):
    size = list.size
    result = np.empty(0, dtype=int)
    for i in range(list.size):
        if list[i][0] not in exeptions:
            result = np.append(result, list[i])
    return result




def run(problem):
    graph = Graph(problem)
    adjacency_list = graph.adjacency_list_from_attempts
    nbShoots = adjacency_list.size
    edges = np.empty(0, dtype=int)
    counterOfEdges = np.empty(nbShoots, dtype=int)
    unchangedCounterOfEdges = np.empty(nbShoots, dtype=int)


    for shoot in range(nbShoots):
        counterOfSuitablePos = adjacency_list[shoot].size-1
        suitablePos = adjacency_list[shoot][counterOfSuitablePos]
        if notIn(suitablePos, edges):
            edges = np.append(edges, [shoot, suitablePos])
        counterOfEdges[shoot] = counterOfSuitablePos
        unchangedCounterOfEdges[shoot] = counterOfSuitablePos



    changedIndex = decreaseCounter(counterOfEdges, unchangedCounterOfEdges, nbShoots)



    while ( not(nullCounter(counterOfEdges, nbShoots)) ):
        tmpEdges = copy(edges, changedIndex)

        for shoot in changedIndex:
            suitablePos = adjacency_list[shoot][counterOfEdges[shoot]]
            if notIn(suitablePos, tmpEdges):
                tmpEdges = np.append(tmpEdges, [shoot, suitablePos])

        if (tmpEdges.size < edges.size):
            edges = tmpEdges
            print("Current best set size : " + str(edges.size))

        changedIndex = decreaseCounter(counterOfEdges, unchangedCounterOfEdges, nbShoots)


    defenderPos = { "defenders": [] }

    for position in range(edges.size):
        defenderPos.get("defenders", []).append(graph.positions[edges[position][1]])


    return defenderPos
