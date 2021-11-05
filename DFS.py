from helpers import *
 
def dfs(current):
    current = str_to_array(current)
    final = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    zero_row, zero_col = search_zero(current)
    stack = []
    stack.append((array_to_string(current), zero_row, zero_col, [0]))
    visited = set()
    visited.add(array_to_string(current))
    while len(stack) != 0:
        if stack[-1][0] == array_to_string(final):
            break
        if stack[-1][-1][0] == 0:
            zero_row, zero_col = stack[-1][1], stack[-1][2]
            arr = str_to_array(stack[-1][0])
            if stack[-1][1] > 0:
                arr[zero_row][zero_col], arr[zero_row - 1][zero_col] = arr[zero_row - 1][zero_col], arr[zero_row][
                    zero_col]
            stack[-1][-1][0] += 1
            if array_to_string(arr) not in visited:
                visited.add(array_to_string(arr))
                stack.append((array_to_string(arr), zero_row - 1, zero_col, [0]))
        elif stack[-1][-1][0] == 1:
            zero_row, zero_col = stack[-1][1], stack[-1][2]
            arr = str_to_array(stack[-1][0])
            if stack[-1][1] < 2:
                arr[zero_row][zero_col], arr[zero_row + 1][zero_col] = arr[zero_row + 1][zero_col], arr[zero_row][
                    zero_col]
            stack[-1][-1][0] += 1
            if array_to_string(arr) not in visited:
                visited.add(array_to_string(arr))
                stack.append((array_to_string(arr), zero_row + 1, zero_col, [0]))
        elif stack[-1][-1][0] == 2:
            zero_row, zero_col = stack[-1][1], stack[-1][2]
            arr = str_to_array(stack[-1][0])
            if stack[-1][2] > 0:
                arr[zero_row][zero_col], arr[zero_row][zero_col - 1] = arr[zero_row][zero_col - 1], arr[zero_row][
                    zero_col]
            stack[-1][-1][0] += 1
            if array_to_string(arr) not in visited:
                visited.add(array_to_string(arr))
                stack.append((array_to_string(arr), zero_row, zero_col - 1, [0]))
        elif stack[-1][-1][0] == 3:
            zero_row, zero_col = stack[-1][1], stack[-1][2]
            arr = str_to_array(stack[-1][0])
            if stack[-1][2] < 2:
                arr[zero_row][zero_col], arr[zero_row][zero_col + 1] = arr[zero_row][zero_col + 1], arr[zero_row][
                    zero_col]
            stack[-1][-1][0] += 1
            if array_to_string(arr) not in visited:
                visited.add(array_to_string(arr))
                stack.append((array_to_string(arr), zero_row, zero_col + 1, [0]))
        else:
            stack.pop()
 
    path_history = dict()
    path_history[array_to_string(current)] = None
    for i in range(len(stack) - 1, 0, -1):
        path_history[stack[i][0]] = stack[i - 1][0]
 
    if '012345678' in visited:
        return path_history, len(visited), len(stack)-1
    else:
        return None, len(visited), -1
 