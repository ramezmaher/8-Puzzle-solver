from helpers import *
from heapdict import heapdict

def manhattan_distance(x, y, val):
    target_x = int(val/3)
    target_y = val%3
    return (abs(x-target_x)+abs(y-target_y))

def euclidean_distance(x, y, val):
    target_x = int(val/3)
    target_y = val%3
    return int(math.sqrt((x-target_x)**2 + (y-target_y) ** 2))

def total_heuristics_distance(current_state, heuristics_func):
    total_distance = 0
    for i in range(3):
        for j in range(3):
            total_distance+= heuristics_func(i, j, current_state[i][j]) 
    return total_distance


def a_star_search(start_state_str, heuristics_func):
    fringe = heapdict()
    explored = set()
    start_state = str_to_array(start_state_str)
    fringe[start_state_str] = total_heuristics_distance(start_state, heuristics_func)
    nodes_expanded = 0
    path_history = dict()
    path_history[start_state_str] = None
    while len(fringe) > 0:
        nodes_expanded += 1
        current_state_str, priority = fringe.popitem()
        explored.add(current_state_str)
        current_state = str_to_array(current_state_str)
        distance_travelled = priority - total_heuristics_distance(current_state, heuristics_func)
        if current_state_str == TARGET_STATE:
            return (path_history, nodes_expanded, distance_travelled)
        distance_travelled += 1
        z_row, z_col = search_zero(current_state)
        next_states = get_states(current_state, z_row, z_col)
        for state in next_states:
            state_str = array_to_string(state)
            if state_str not in explored:
                path_history[state_str] = current_state_str
                value = total_heuristics_distance(state, heuristics_func) + distance_travelled
                if state_str not in fringe.keys():
                    fringe[state_str] = value
                else:
                    fringe[state_str] = min(fringe[state_str], value)
    return (None, nodes_expanded, -1)
