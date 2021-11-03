from heapdict import heapdict
from helpers import *
import pygame
from tkinter import *
from queue import Queue
from time import sleep

WINDOW_WIDTH = 700
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
START = 50


pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
pygame.display.set_caption("8 Puzzle Solver")
font = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 15)

def draw(grid):
    for j in range(3):
        for i in range(3):
            iloc = START+(i*200)
            jloc = START+(j*200)
            if grid[j][i] != 0:
                pygame.draw.rect(window, WHITE, (iloc, jloc, 200, 200))
                text1 = font.render(str(grid[j][i]), 20, BLACK)
                window.blit(text1, (iloc+76, jloc+76))
            else:
                pygame.draw.rect(window, RED, (iloc, jloc, 200, 200))

    for i in range(3):
        iloc = START+(i*200)
        pygame.draw.line(window, BLACK, (50, iloc), (650, iloc), 3)
        pygame.draw.line(window, BLACK, (iloc, 50), (iloc, 650), 3)
    pygame.draw.line(window, BLACK, (650, 50), (650, 650), 3)
    pygame.draw.line(window, BLACK, (50, 650), (650, 650), 3)

def a_star_search(start_state_str, heuristics_func):
    root.destroy()
    fringe = heapdict()
    explored = set()
    start_state = str_to_array(start_state_str)
    fringe[start_state_str] = total_heuristics_distance(start_state, heuristics_func)
    nodes_expanded = 0
    path_history = dict()
    path_history[start_state_str] = None
    while len(fringe) > 0:
        nodes_expanded += 1
        current_state_str, priority = fringe.popitem()
        explored.add(current_state_str)
        current_state = str_to_array(current_state_str)
        distance_travelled = priority - total_heuristics_distance(current_state, heuristics_func)
        if current_state_str == TARGET_STATE:
            return (path_history, nodes_expanded, distance_travelled)
        distance_travelled += 1
        z_row, z_col = search_zero(current_state)
        next_states = get_states(current_state, z_row, z_col)
        for state in next_states:
            state_str = array_to_string(state)
            if state_str not in explored:
                path_history[state_str] = current_state_str
                value = total_heuristics_distance(state, heuristics_func) + distance_travelled
                if state_str not in fringe.keys():
                    fringe[state_str] = value
                else:
                    fringe[state_str] = min(fringe[state_str], value)
    return (None, nodes_expanded, -1)

def bfs(current):
    root.destroy()
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
            print_format(phase, history)
            history = []
            counter -= 1
            continue
        if current == final:
            phase += 1
            print_format(phase, history)
            print("Expanded " + str(counter) + " times")
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
        print('No valid Answer')
        return

def dfs(current):
    root.destroy()
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




t1 = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]
t2 = [[1, 2, 7], [3, 4, 6], [0, 5, 8]]
t3 = [[1, 2, 0], [3, 4, 6], [7, 5, 8]]
t4 = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
#print(bfs(t1))
running = True
flag = False

# to do: Take input from user { 1-board: String representing the board (fih function to check if input board valid fel helpers), 
    #                               2-int representing the algorithm
    # 

grid = t4

global valid_input, initial, a
valid_input = False
initial = ''
a = False
def p():
    global valid_input
    global initial
    if check_valid_board_str(e1.get()):
        valid_input = True
        initial = e1.get()
        return True, e1.get()

def bfsCall():
    if valid_input:
        bfs(initial)
def dfsCall():
    if valid_input:
        dfs(initial)
def a_starCall():
    global a
    if valid_input:
        a = True
        dfs(initial)
def manhattanCall():
    global a
    if a and valid_input:
        a_star_search(initial, manhattan_distance)
def euclideanCall():
    global a
    if a and valid_input:
        a_star_search(initial, euclidean_distance)

while running:
    window.fill(GREY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False
    if not flag:
        draw(grid)
        pygame.display.update()
        # To do: Pick one algorithm, all of them should have same API
        # switch on algorithm type 
        # a* with manhattan

        root = Tk()
        root.geometry('800x500+100+200')
        root.title('8-Puzzle Solver')
        Label(root, text='Enter initial state like a string (final state is 012345678) :').pack()
        e1 = Entry(root)
        e1.pack()
        Label(root, text='').pack()

        while True:
            solveButton = Button(root, text='Solve Puzzle', width=13, height=1, command=p).pack()
            Label(root, text='').pack()
            Label(root, text='').pack()
            Label(root, text='').pack()
            frame = Frame(root)
            frame.pack()
            bfsButton = Button(frame, text='BFS', width=25, height=4, fg='red', command=bfsCall)
            bfsButton.pack(side=LEFT)
            dfsButton = Button(frame, text='DFS', width=25, height=4, fg='green', command=dfsCall)
            dfsButton.pack(side=LEFT)
            a_starButton = Button(frame, text='A*', width=25, height=4, fg='blue', command=a_starCall)
            a_starButton.pack(side=LEFT)
            Label(root, text='').pack()
            Label(root, text='').pack()
            Label(root, text='').pack()
            Label(root, text='If you chose A*, choose the heuristic:').pack()
            f = Frame(root)
            f.pack()
            manhattanButton = Button(f, text='Manhattan', width=25, height=4, command=manhattanCall)
            manhattanButton.pack(side=LEFT)
            euclideanButton = Button(f, text='Euclidean', width=25, height=4, command=euclideanCall)
            euclideanButton.pack(side=LEFT)
            root.mainloop()
            if valid_input:
                break

        path, nodes, dist = a_star_search(grid, manhattan_distance)
        # a* with euclidean
        # //////.......//////
        # BFS
        # /////......///////
        # DFS
        # /////......///////

        if dist < 0: 
            draw(grid)
            pygame.display.update()
            text1 = font2.render("No Solution :( !! Number of nodes expanded = "+str(nodes), 1, BLACK)
            window.blit(text1, (50 , 660))
        else:
            grids = minimized_path(path)
            g_len = len(grids)
            for i in range(g_len):
                draw(str_to_array(grids[g_len-1-i]))
                pygame.display.update()
                sleep(1)
            text1 = font2.render("Found :) !! Number of nodes expanded = "+str(nodes)+" . Optimal path length = "+str(dist), 1, BLACK)
            window.blit(text1, (50 , 660))
        pygame.display.update()
        flag = True

pygame.quit()