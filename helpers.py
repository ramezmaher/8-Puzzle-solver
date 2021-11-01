import copy
import math

def  char_to_int(c):
    return ord(c)-ord('0')

def str_to_array(str):
    board = []
    k = 0
    for i in range(3):
        arr = []
        for j in range(3):
            arr.append(char_to_int(str[k]))
            k+=1
        board.append(arr)
    return board

def array_to_string(array):
    return ''.join([''.join(map(str, x)) for x in array])

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

def check_valid_board_str(str):
    if str == None or len(str) != 9:
        return False
    s = set()
    for i in range(9):
        n = char_to_int(str[i])
        if n >= 9 or n < 0 or n in s:
            return False
        s.add(n)
    return True

def print_format(phase_number, array):
    print('Phase no.'+str(phase_number))
    for i in range(3):
        arr = [x[i] for x in array]
        for row in range(len(arr)):
            print(' '.join(map(str, arr[row])), end='')
            if row < len(arr) - 1:
                print('-----', end='')
        print()

def get_states(current_state, z_row, z_col):
    next_states = []
    for row, col in get_neighbors(z_row, z_col):
        state = copy.deepcopy(current_state)
        state[z_row][z_col] = state[row][col]
        state[row][col] = 0
        next_states.append(state)
    return next_states

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