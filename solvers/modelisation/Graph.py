from viewer.geometry import *
from math import sqrt

class Graph:
    theta_print = 0

    def __init__(self, problem):
        '''
        Creates the bipartite graph from a problem. First computes the available positions, then the attemps on target
        and finally computes the adjacency matrix between these two ensembles of vertices when an attempt on target
        intersects a position (+/- robot_radius).
        :param problem: A Problem from the viewer
        '''

        self.adjacency_list_from_attempts, \
        self.adjacency_list_from_positions, \
        self.attemps_on_target, \
        self.positions = self.create_graph_from_problem(problem)



    def create_graph_from_problem(self, problem):
        positions = self.get_defenders_available_positions(problem)
        attempts_on_target = self.get_attempts_on_target(problem)
        adjacency_list_from_attempts, adjacency_list_from_positions, new_positions = \
            self.calculate_adjacency(problem, positions, attempts_on_target)

        return adjacency_list_from_attempts, \
               adjacency_list_from_positions, \
               attempts_on_target, \
               new_positions

    def get_distances_from_groal(self, goal, attempt):
        x1 = goal.posts[0, 0]
        y1 = goal.posts[1, 0]
        x2 = goal.posts[0, 1]
        y2 = goal.posts[1, 1]
        x_shot = attempt[0]
        y_shot = attempt[1]

        if (x1 == x2):
            a = abs(y2 - y1) / math.pow(10, -15)
        else:
            a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        distance = abs(y_shot - a * x_shot - b) / sqrt(1 + a ** 2)

        return [sqrt((x1-x_shot)**2 + (y1-y_shot)**2),
                sqrt((x2-x_shot)**2 + (y2-y_shot)**2)], distance

    def get_attempts_on_target(self, problem):
        theta_step = problem.theta_step
        nb_opponents = problem.getNbOpponents()
        result = []

        for i in range (0, nb_opponents):
            theta = 0
            while (theta < 2*np.pi):

                attempt = []
                attempt.append(self.get_opponents_positions(problem)[i][0])
                attempt.append(self.get_opponents_positions(problem)[i][1])
                theta += theta_step

                isOnGoal = False

                for goal in problem.goals:
                    # Check if the angle is enough to score, meaning not kicking from the side of the goal
                    distances_from_posts, distance = self.get_distances_from_groal(goal, attempt)
                    nearest = min(distances_from_posts)

                    if((distance > nearest*math.sin(theta_step)) and (goal.kickResult(attempt, theta) is not None)):
                        farthest = max(distances_from_posts)
                        isOnGoal = True
                        break

                attempt.append(theta)
                if(isOnGoal):
                    attempt.append(farthest)
                    result.append(attempt)

        return result


    def get_opponents_positions(self,problem):
        return problem.opponents.transpose()

    def is_position_allowed(self, x, y, problem):
        # collision with goal (OK as long as the robot, at +/- robot_radius, doesn't touch the goalpost)
        for goal in problem.goals:
            if np.linalg.norm(np.array([x,y]) - goal.posts[:, 0]) < problem.robot_radius or \
               np.linalg.norm(np.array([x, y]) - goal.posts[:, 1]) < problem.robot_radius :
                return False

        # collision with opponents
        for opponent in self.get_opponents_positions(problem):
            if np.linalg.norm(np.array([x, y]) - opponent) < problem.robot_radius * 2:
                return False

        return True

    def get_distance_to_allow_between_defenders(self, problem):
        return problem.pos_step

    def get_defenders_available_positions(self, problem):
        range_step = self.get_distance_to_allow_between_defenders(problem)

        horizontal_pos_range = np.arange(problem.field_limits[0,0],
                                         problem.field_limits[0,1], range_step)
        vertical_pos_range = np.arange(problem.field_limits[1,0],
                                       problem.field_limits[1,1], range_step)
        return [[i, j] for j in np.round(vertical_pos_range, 2) for i in np.round(horizontal_pos_range, 2) if self.is_position_allowed(i, j, problem)]


    def calculate_adjacency(self, problem, positions, attempts):
        adjacency_list_from_attempts = [np.array([], dtype=int) for _ in attempts]
        adjacency_list_from_positions = [np.array([], dtype=int) for _ in positions]

        for t in range (0, len(attempts)):
            theta = attempts[t][2]
            x1_shot = attempts[t][0]
            y1_shot = attempts[t][1]
            cos = np.cos(theta)
            sin = np.sin(theta)

            for p in range (0, len(positions)):
                x_p = positions[p][0]
                y_p = positions[p][1]

                segment_length = sqrt((x_p-x1_shot)**2 + (y_p-y1_shot)**2)

                if (segment_length < attempts[t][3]):
                    if (cos >= 0):
                        if (sin >= 0):
                            x2_shot = x1_shot+(segment_length*cos)
                            y2_shot = y1_shot+(segment_length*sin)
                        else:
                            x2_shot = x1_shot +(segment_length*np.sin(theta - 3*np.pi/2))
                            y2_shot = y1_shot -(segment_length*np.cos(theta - 3*np.pi/2))
                    else:
                        if (sin >= 0):
                            x2_shot = x1_shot -(segment_length*np.sin(theta - np.pi/2)) # +
                            y2_shot = y1_shot +(segment_length*np.cos(theta - np.pi/2)) # -
                        else:
                            x2_shot = x1_shot+(segment_length*np.cos(theta - np.pi))
                            y2_shot = y1_shot+(segment_length*np.sin(theta - np.pi))

                    shot_point_1 = np.array([x1_shot,y1_shot])
                    shot_point_2 = np.array([x2_shot,y2_shot])

                    position = np.array([x_p,y_p])

                    if (segmentCircleIntersection(shot_point_1,shot_point_2, position, problem.robot_radius) is not None):
                        adjacency_list_from_attempts[t] = np.append(adjacency_list_from_attempts[t], np.array([p], dtype=int))
                        adjacency_list_from_positions[p] = np.append(adjacency_list_from_positions[p], np.array([t], dtype=int))


        # Cleaning
        adjacency_list_from_attempts = [arr for arr in adjacency_list_from_attempts if arr.size > 0]
        positions_to_keep = [i for i in range(len(adjacency_list_from_positions)) if adjacency_list_from_positions[i].size > 0]
        new_positions = np.array(positions)[positions_to_keep]
        return np.array(adjacency_list_from_attempts), \
               np.array(adjacency_list_from_positions)[positions_to_keep], \
               new_positions.tolist()
