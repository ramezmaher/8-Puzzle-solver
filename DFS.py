from helpers import *

def dfs(current):
    current = str_to_array(current)
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
