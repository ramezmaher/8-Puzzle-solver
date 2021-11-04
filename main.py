from math import fabs
from A_star import a_star_search, manhattan_distance, euclidean_distance
from time import sleep
from helpers import *
from tkinter import *
from BFS import bfs
from DFS import dfs
import pygame


WINDOW_WIDTH = 700
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
START = 50

global valid_input, initial, a, op_lock
global path, nodes, distance
valid_input = False
initial = ''
a = False
op_lock = True

def p():
    global valid_input, op_lock
    global initial
    if check_valid_board_str(e1.get()):
        valid_input = True
        initial = e1.get()
        op_lock = False
        return True, e1.get()

def bfsCall():
    global path, nodes, distance, op_lock
    if valid_input and not op_lock:
        op_lock = True
        path, nodes, distance = bfs(initial)
        root.destroy()

def dfsCall():
    global path, nodes, distance, op_lock
    if valid_input and not op_lock:
        op_lock = True
        path, nodes, distance = dfs(initial)
        root.destroy()

def a_starCall():
    global a
    if valid_input:
        a = True

def manhattanCall():
    global a, op_lock
    global path, nodes, distance
    if a and valid_input and not op_lock:
        op_lock = True
        path, nodes, distance = a_star_search(initial, manhattan_distance)
        a = False
        root.destroy()

def euclideanCall():
    global a, op_lock
    global path, nodes, distance
    if a and valid_input and not op_lock:
        op_lock = True
        path, nodes, distance = a_star_search(initial, euclidean_distance)
        a = False
        root.destroy() 

root = Tk()
root.geometry('800x500+100+200')
root.title('8-Puzzle Solver')
Label(root, text='Enter initial state like a string (final state is 012345678) :').pack()
e1 = Entry(root)
e1.pack()
Label(root, text='').pack()

def draw_menu():
    solveButton = Button(root, text='Insert Input', width=13, height=1, command=p)
    solveButton.pack()
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

draw_menu()

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
                pygame.draw.rect(window, BLACK, (iloc, jloc, 200, 200))

    for i in range(3):
        iloc = START+(i*200)
        pygame.draw.line(window, BLACK, (50, iloc), (650, iloc), 3)
        pygame.draw.line(window, BLACK, (iloc, 50), (iloc, 650), 3)
    pygame.draw.line(window, BLACK, (650, 50), (650, 650), 3)
    pygame.draw.line(window, BLACK, (50, 650), (650, 650), 3)

def show_failure(grid):
    draw(grid)
    pygame.display.update()
    text1 = font2.render("No Solution :( !! Number of nodes expanded = "+str(nodes), 1, BLACK)
    window.blit(text1, (50 , 660))
    
def show_game():
    if distance < 0 or path == None:
        return
    grids = minimized_path(path)
    g_len = len(grids)
    counter = 0
    for i in range(g_len):
        draw(str_to_array(grids[g_len-1-i]))
        text1 = font2.render("Number of moves: "+str(counter), 1, BLACK)
        window.blit(text1, (50 , 660))
        pygame.display.update()
        window.fill(GREY)
        counter+=1
        sleep(1)
    draw(str_to_array(TARGET_STATE))
    text1 = font2.render("Found :) !! Number of nodes expanded = "+str(nodes)+" . Optimal path length = "+str(distance), 1, BLACK)
    window.blit(text1, (50 , 660))


t1 = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]
t2 = [[1, 2, 7], [3, 4, 6], [0, 5, 8]]
t3 = [[1, 2, 0], [3, 4, 6], [7, 5, 8]]
t4 = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]

running = True
flag = False
grid = str_to_array(initial)


while running:
    window.fill(GREY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False
    if not flag:
        draw(grid)
        pygame.display.update()

        if distance < 0:
            show_failure(grid) 
        else:
            show_game()
        pygame.display.update()
        flag = True

pygame.quit()