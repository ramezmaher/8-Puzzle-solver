from queue import Queue
import copy


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


def bfs(current):
    final = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    row, col = search_zero(current)
    _queue = Queue()
    _queue.put((current, row, col))
    visited = set()
    visited.add(array_to_string(current))
    counter = 0
    while not _queue.empty():
        counter += 1
        current, row, col = _queue.get()
        print(current)
        if current == final:
            return counter
        for neighbor_row, neighbor_col in get_neighbors(row, col):
            current[row][col], current[neighbor_row][neighbor_col] = current[neighbor_row][neighbor_col], current[row][col]
            new_array = array_to_string(current)
            if new_array not in visited:
                visited.add(new_array)
                _queue.put((copy.deepcopy(current), neighbor_row, neighbor_col))
            current[row][col], current[neighbor_row][neighbor_col] = current[neighbor_row][neighbor_col], current[row][col]
    else:
        print('No valid Answer')
        return