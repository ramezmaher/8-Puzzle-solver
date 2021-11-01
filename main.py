from heapdict import heapdict
from helpers import *
from tkinter import *
import pygame
import time
from queue import Queue
from termcolor import colored, cprint
from time import sleep
import os
import math
import copy

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

 
def a_star_search(start_state, heuristics_func):
    fringe = heapdict()
    explored = set()
    fringe[array_to_string(start_state)] = total_heuristics_distance(start_state, heuristics_func)
    nodes_expanded = 0
    while len(fringe) > 0:
        nodes_expanded+=1
        current_state_str, priority = fringe.popitem()
        explored.add(current_state_str)
        current_state = str_to_array(current_state_str)
        distance_travelled = priority - total_heuristics_distance(current_state, heuristics_func)
        if current_state_str == "012345678":
            draw(current_state)
            pygame.display.update()
            print('Found!! Nodes expanded = '+str(nodes_expanded)) 
            print('Optimal number of moves: '+str(distance_travelled))
            return
        distance_travelled+= 1
        z_row, z_col = search_zero(current_state)
        draw(current_state)
        pygame.display.update()
        #time.sleep(1)
        next_states = get_states(current_state, z_row, z_col)
        for state in next_states:
            state_str = array_to_string(state)
            if state_str not in explored:
                value = total_heuristics_distance(state, heuristics_func)+distance_travelled
                if state_str not in fringe.keys(): 
                    fringe[state_str] = value
                else:
                    fringe[state_str] = min(fringe[state_str], value)
    print('Nodes expanded = '+str(nodes_expanded)) 
    print('No solution')
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


t1 = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]
t2 = [[1, 2, 7], [3, 4, 6], [0, 5, 8]]
t3 = [[1, 2, 0], [3, 4, 6], [7, 5, 8]]

running = True
flag = False

while running:
    window.fill(GREY)
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
           running = False
    if not flag:

        a_star_search(t3, manhattan_distance)
        flag = True

pygame.quit()

def screen_clear():
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      _ = os.system('cls')

def print_board(arr):
    os.system('clear')
    for i in range(3):
        for j in range(3):
            if arr[i][j] == 0:
                print(colored('0', 'red', attrs=['bold']), end=" "),
            else:
                print(arr[i][j], end=" "),
        print("")
    sleep(1)
    
def dfs(current):
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
