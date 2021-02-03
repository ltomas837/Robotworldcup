from solvers.modelisation.Graph import Graph

def calculate_position_cost_for_index(index, iList, adjacency_list):
    cost = 1
    pos_cost = 1
    newly_added = 0
    for i in adjacency_list[index] :
        isInIList = False
        for j in iList :
            if(j == i):
                isInIList = True
        if(not isInIList) :
            newly_added = newly_added+1
    if(newly_added == 0):
        return -1

    return pos_cost/newly_added



def run(problem):
    graph = Graph(problem)
    adjacency_list = graph.adjacency_list_from_positions
    positions = graph.positions
    shootList = [ z for z in range(graph.adjacency_list_from_attempts.size)] #U
    I = []
    minimalSetOfDefenders = []
    indexCal = 0

    while(len(I) != len(shootList)):

        while((calculate_position_cost_for_index(indexCal,I,adjacency_list) == -1)):

            indexCal = indexCal + 1
        min_value = calculate_position_cost_for_index(indexCal,I,adjacency_list)
        min_value_index = indexCal
        for posIndex in range(1,len(adjacency_list)):
            pos_cost = calculate_position_cost_for_index(posIndex,I,adjacency_list)
            if(pos_cost != -1 and pos_cost < min_value):

                min_value = pos_cost
                min_value_index = posIndex

        for i in adjacency_list[min_value_index]:
            isInI = False
            for j in I :
                if i== j:
                    isInI = True
            if(not isInI):
                I.append(i)
        minimalSetOfDefenders.append(min_value_index)

    # Dump data in JSON file
    defenderPos = { "defenders": [] }
    for index in minimalSetOfDefenders:
        defenderPos.get("defenders", []).append(positions[index])

    return defenderPos
