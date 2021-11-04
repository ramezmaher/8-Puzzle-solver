from helpers import *
from queue import Queue


def bfs(current):
    current = str_to_array(current)
    final = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    row, col = search_zero(current)
    _queue = Queue()
    _queue.put((current, row, col))
    visited = set()
    visited.add(array_to_string(current))
    phase = 0
    path_history = dict()
    path_history[array_to_string(current)] = None
    while not _queue.empty():
        current, row, col = _queue.get()
        if current == final:
            return path_history, phase, len(path_history.keys())
        new_one = False
        for neighbor_row, neighbor_col in get_neighbors(row, col):
            current[row][col], current[neighbor_row][neighbor_col] = current[neighbor_row][neighbor_col], current[row][
                col]
            new_array = array_to_string(current)
            if new_array not in visited:
                new_one = True
                visited.add(new_array)
                phase += 1
                _queue.put((copy.deepcopy(current), neighbor_row, neighbor_col))
            current[row][col], current[neighbor_row][neighbor_col] = current[neighbor_row][neighbor_col], current[row][
                col]
            if new_one:
                path_history[new_array] = array_to_string(current)
                new_one = False
    else:
        return None, phase, -1
