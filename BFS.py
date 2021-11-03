from helpers import *
from queue import Queue

def bfs(current):
    current = str_to_array(current)
    final = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    original = current
    row, col = search_zero(current)
    _queue = Queue()
    _queue.put((current, row, col))
    _queue.put((-1, -1, -1))
    visited = set()
    visited.add(array_to_string(current))
    counter = 0
    history = []
    phase = 0
    path_history = dict()
    while not _queue.empty():
        counter += 1
        current, row, col = _queue.get()
        if current != -1:
            history.append(current)
        else:
            phase += 1
            history = []
            counter -= 1
            continue
        if current == final:
            phase += 1
            return minimized_path(path_history, original)
        new_one = False
        for neighbor_row, neighbor_col in get_neighbors(row, col):
            current[row][col], current[neighbor_row][neighbor_col] = current[neighbor_row][neighbor_col], current[row][
                col]
            new_array = array_to_string(current)
            if new_array not in visited:
                new_one = True
                visited.add(new_array)
                _queue.put((copy.deepcopy(current), neighbor_row, neighbor_col))
            current[row][col], current[neighbor_row][neighbor_col] = current[neighbor_row][neighbor_col], current[row][
                col]
            if new_one:
                path_history[new_array] = copy.deepcopy(current)
                new_one = False
        _queue.put((-1, -1, -1))
    else:
        return
