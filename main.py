from queue import Queue
from heapdict import heapdict
from termcolor import colored, cprint
from time import sleep
import os
import math
import copy

########## GENERAL HELPERS #################

TARGET_STATE = "012345678"

def search_zero(array):
    for row in range(len(array)):
        for col in range(len(array[row])):
            if array[row][col] == 0:
                return row, col


def get_neighbors(row, col):
    answer = []
    if row - 1 >= 0:
        answer.append((row - 1, col))
    if col - 1 >= 0:
        answer.append((row, col - 1))
    if row + 1 < 3:
        answer.append((row + 1, col))
    if col + 1 < 3:
        answer.append((row, col + 1))
    return answer


def array_to_string(array):
    return ''.join([''.join(map(str, x)) for x in array])


def print_format(phase_number, array):
    print('Phase no.'+str(phase_number))
    for i in range(3):
        arr = [x[i] for x in array]
        for row in range(len(arr)):
            print(' '.join(map(str, arr[row])), end='')
            if row < len(arr) - 1:
                print('-----', end='')
        print()

def print_state(state):
    #to do
    return

def get_states(current_state, z_row, z_col):
    next_states = []
    for row, col in get_neighbors(z_row, z_col):
        state = copy.deepcopy(current_state)
        state[z_row][z_col] = state[row][col]
        state[row][col] = 0
        next_states.append(state)
    return next_states

def str_to_array(str):
    board = []
    k = 0
    for i in range(3):
        arr = []
        for j in range(3):
            arr.append(ord(str[k])-ord('0'))
            k+=1
        board.append(arr)
    return board

#############/////////////////////####################
#############//////...BFS.../////#####################

def bfs(current):
    final = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    row, col = search_zero(current)
    _queue = Queue()
    _queue.put((current, row, col))
    _queue.put((-1, -1, -1))
    visited = set()
    visited.add(array_to_string(current))
    counter = 0
    history = []
    phase = 0
    while not _queue.empty():
        counter += 1
        current, row, col = _queue.get()
        if current != -1:
            history.append(current)
        else:
            phase += 1
            print_format(phase, history)
            history = []
            counter -= 1
            continue
        if current == final:
            phase += 1
            print_format(phase, history)
            print("Expanded " + str(counter) + " times")
            return counter
        for neighbor_row, neighbor_col in get_neighbors(row, col):
            current[row][col], current[neighbor_row][neighbor_col] = current[neighbor_row][neighbor_col], current[row][
                col]
            new_array = array_to_string(current)
            if new_array not in visited:
                visited.add(new_array)
                _queue.put((copy.deepcopy(current), neighbor_row, neighbor_col))
            current[row][col], current[neighbor_row][neighbor_col] = current[neighbor_row][neighbor_col], current[row][
                col]
        _queue.put((-1, -1, -1))
    else:
        print('No valid Answer')
        return

#####################//////////////////#########################
#####################/////...A*.../////#########################

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

def a_star_search(start_state, heuristics_func):
    fringe = heapdict()
    explored = set()
    fringe[array_to_string(start_state)] = total_heuristics_distance(start_state, heuristics_func)
    nodes_expanded = 0
    while len(fringe) > 0:
        nodes_expanded+=1
        current_state_str, priority = fringe.popitem()
        explored.add(current_state_str)
        current_state = str_to_array(current_state_str)
        distance_travelled = priority - total_heuristics_distance(current_state, heuristics_func)
        if current_state_str == TARGET_STATE:
            print(current_state_str)
            print('Found!! Nodes expanded = '+str(nodes_expanded)) 
            print('Optimal number of moves: '+str(distance_travelled))
            return
        distance_travelled+= 1
        z_row, z_col = search_zero(current_state)
        #print(current_state_str)
        next_states = get_states(current_state, z_row, z_col)
        for state in next_states:
            state_str = array_to_string(state)
            if state_str not in explored:
                value = total_heuristics_distance(state, heuristics_func)+distance_travelled
                if state_str not in fringe.keys(): 
                    fringe[state_str] = value
                else:
                    fringe[state_str] = min(fringe[state_str], value)
    print('Nodes expanded = '+str(nodes_expanded)) 
    print('No solution')
    return 

#######################/////////////////////########################
######################//////...TEST...//////########################

v = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]
f = [[1, 2, 7], [3, 4, 6], [0, 5, 8]]
s = [[1, 2, 0], [3, 4, 6], [7, 5, 8]]
#bfs(s)
a_star_search(s, euclidean_distance)
a_star_search(s, manhattan_distance)


def screen_clear():
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      _ = os.system('cls')

def print_board(arr):
    os.system('clear')
    for i in range(3):
        for j in range(3):
            if arr[i][j] == 0:
                print(colored('0', 'red', attrs=['bold']), end=" "),
            else:
                print(arr[i][j], end=" "),
        print("")
    sleep(1)


def dfs(current):
    final = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    row, col = search_zero(current)

    def dfs_helper(current_graph, zero_row, zero_col, goal):
        nonlocal counter
        counter += 1
        print(current_graph)
        if current_graph == goal:
            return counter
        if zero_row > 0:
            current_graph[zero_row][zero_col], current_graph[zero_row - 1][zero_col] = current_graph[zero_row - 1][
                                                                                           zero_col], \
                                                                                       current_graph[zero_row][zero_col]
            if array_to_string(current_graph) not in visited:
                visited.add(array_to_string(current_graph))
                returned_code = dfs_helper(current_graph, zero_row - 1, zero_col, goal)
                if returned_code != -1:
                    return returned_code
            current_graph[zero_row][zero_col], current_graph[zero_row - 1][zero_col] = current_graph[zero_row - 1][
                                                                                           zero_col], \
                                                                                       current_graph[zero_row][zero_col]
        if zero_row < 2:
            current_graph[zero_row][zero_col], current_graph[zero_row + 1][zero_col] = current_graph[zero_row + 1][
                                                                                           zero_col], \
                                                                                       current_graph[zero_row][zero_col]
            if array_to_string(current_graph) not in visited:
                visited.add(array_to_string(current_graph))
                returned_code = dfs_helper(current_graph, zero_row + 1, zero_col, goal)
                if returned_code != -1:
                    return returned_code
            current_graph[zero_row][zero_col], current_graph[zero_row + 1][zero_col] = current_graph[zero_row + 1][
                                                                                           zero_col], \
                                                                                       current_graph[zero_row][zero_col]
        if zero_col > 0:
            current_graph[zero_row][zero_col], current_graph[zero_row][zero_col - 1] = current_graph[zero_row][
                                                                                           zero_col - 1], \
                                                                                       current_graph[zero_row][zero_col]
            if array_to_string(current_graph) not in visited:
                visited.add(array_to_string(current_graph))
                returned_code = dfs_helper(current_graph, zero_row, zero_col - 1, goal)
                if returned_code != -1:
                    return returned_code
            current_graph[zero_row][zero_col], current_graph[zero_row][zero_col - 1] = current_graph[zero_row][
                                                                                           zero_col - 1], \
                                                                                       current_graph[zero_row][zero_col]
        if zero_col < 2:
            current_graph[zero_row][zero_col], current_graph[zero_row][zero_col + 1] = current_graph[zero_row][
                                                                                           zero_col + 1], \
                                                                                       current_graph[zero_row][zero_col]
            if array_to_string(current_graph) not in visited:
                visited.add(array_to_string(current_graph))
                returned_code = dfs_helper(current_graph, zero_row, zero_col + 1, goal)
                if returned_code != -1:
                    return returned_code
            current_graph[zero_row][zero_col], current_graph[zero_row][zero_col + 1] = current_graph[zero_row][
                                                                                           zero_col + 1], \
                                                                                       current_graph[zero_row][zero_col]
        return -1

    visited = set()
    visited.add(array_to_string(current))
    counter = 0
    dfs_helper(current, row, col, final)
