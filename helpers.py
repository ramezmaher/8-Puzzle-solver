import copy
import math

TARGET_STATE = "012345678"

def  char_to_int(c):
    return ord(c)-ord('0')

def str_to_array(str):
    if str == None or len(str) == 0:
        return
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


def get_states(current_state, z_row, z_col):
    next_states = []
    for row, col in get_neighbors(z_row, z_col):
        state = copy.deepcopy(current_state)
        state[z_row][z_col] = state[row][col]
        state[row][col] = 0
        next_states.append(state)
    return next_states

def minimized_path(history):
    current = TARGET_STATE
    answer = []
    while current != None:
        answer.append(current)
        current = history[current]
    return answer