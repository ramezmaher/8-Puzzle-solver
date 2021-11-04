from helpers import *

def dfs(current):
    current = str_to_array(current)
    final = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    row, col = search_zero(current)
    path_history = dict()
    path_history[array_to_string(current)] = None

    def dfs_helper(current_graph, zero_row, zero_col, goal):
        nonlocal counter
        counter += 1
        if current_graph == goal:
            return path_history, counter, len(path_history.keys())
        if zero_row > 0:
            backup = array_to_string(current_graph)
            current_graph[zero_row][zero_col], current_graph[zero_row - 1][zero_col] = current_graph[zero_row - 1][
                                                                                           zero_col], \
                                                                                       current_graph[zero_row][zero_col]
            if array_to_string(current_graph) not in visited:
                path_history[array_to_string(current_graph)] = backup
                visited.add(array_to_string(current_graph))
                returned_code = dfs_helper(current_graph, zero_row - 1, zero_col, goal)[1]
                if returned_code != -1:
                    return path_history, returned_code, len(path_history.keys())
            current_graph[zero_row][zero_col], current_graph[zero_row - 1][zero_col] = current_graph[zero_row - 1][
                                                                                           zero_col], \
                                                                                       current_graph[zero_row][zero_col]
        if zero_row < 2:
            backup = array_to_string(current_graph)
            current_graph[zero_row][zero_col], current_graph[zero_row + 1][zero_col] = current_graph[zero_row + 1][
                                                                                           zero_col], \
                                                                                       current_graph[zero_row][zero_col]
            if array_to_string(current_graph) not in visited:
                path_history[array_to_string(current_graph)] = backup
                visited.add(array_to_string(current_graph))
                returned_code = dfs_helper(current_graph, zero_row + 1, zero_col, goal)[1]
                if returned_code != -1:
                    return path_history, returned_code, len(path_history.keys())
            current_graph[zero_row][zero_col], current_graph[zero_row + 1][zero_col] = current_graph[zero_row + 1][
                                                                                           zero_col], \
                                                                                       current_graph[zero_row][zero_col]
        if zero_col > 0:
            backup = array_to_string(current_graph)
            current_graph[zero_row][zero_col], current_graph[zero_row][zero_col - 1] = current_graph[zero_row][
                                                                                           zero_col - 1], \
                                                                                       current_graph[zero_row][zero_col]
            if array_to_string(current_graph) not in visited:
                path_history[array_to_string(current_graph)] = backup
                visited.add(array_to_string(current_graph))
                returned_code = dfs_helper(current_graph, zero_row, zero_col - 1, goal)[1]
                if returned_code != -1:
                    return path_history, returned_code, len(path_history.keys())
            current_graph[zero_row][zero_col], current_graph[zero_row][zero_col - 1] = current_graph[zero_row][
                                                                                           zero_col - 1], \
                                                                                       current_graph[zero_row][zero_col]
        if zero_col < 2:
            backup = array_to_string(current_graph)
            current_graph[zero_row][zero_col], current_graph[zero_row][zero_col + 1] = current_graph[zero_row][
                                                                                           zero_col + 1], \
                                                                                       current_graph[zero_row][zero_col]
            if array_to_string(current_graph) not in visited:
                path_history[array_to_string(current_graph)] = backup
                visited.add(array_to_string(current_graph))
                returned_code = dfs_helper(current_graph, zero_row, zero_col + 1, goal)[1]
                if returned_code != -1:
                    return path_history, returned_code, len(path_history.keys())
            current_graph[zero_row][zero_col], current_graph[zero_row][zero_col + 1] = current_graph[zero_row][
                                                                                           zero_col + 1], \
                                                                                       current_graph[zero_row][zero_col]
        return None, counter, -1

    if current == final:
        return path_history, 0, 0
    visited = set()
    visited.add(array_to_string(current))
    counter = 0
    return dfs_helper(current, row, col, final)
