from queue import Queue
from queue import PriorityQueue
import math
import copy

TARGET_STATE = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

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


def manhattan_distance(x, y, val):
    target_x = int(val/3)
    target_y = val%3
    return (abs(x-target_x)+abs(y-target_y))

def euclidean_distance(x, y, val):
    target_x = int(val/3)
    target_y = val%3
    return math.sqrt((x-target_x)**2 + (y-target_y) ** 2)

def total_heuristics_distance(current_state, heuristics_func):
    total_distance = 0
    for i in range(3):
        for j in range(3):
            total_distance+= heuristics_func(i, j, current_state[i][j]) 
    return total_distance


def a_star_search(start_state, heuristics_func):
    fringe = PriorityQueue()
    distance_travelled = 0
    fringe.put((total_heuristics_distance(start_state, heuristics_func), start_state))
    while not fringe.empty():
        current_state = fringe.get()
        if current_state == TARGET_STATE:
            print('Found')
            print_state(current_state)
            break



    return 

#bfs([[1, 2, 5], [3, 4, 0], [6, 7, 8]])
print(total_heuristics_distance(array_to_string([[1, 2, 5], [3, 4, 0], [6, 7, 8]]), manhattan_distance))
