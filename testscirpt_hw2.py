# from trackbeebot import BeeBot
# import matplotlib.pyplot as plt 
# from matplotlib.patches import Polygon
import numpy as np
import math
# import jsonpip install numpy

# Given -----------------------------------------------------------------------------------------------------------------------------------------
a_i = [[-4], [-1]]
com = "10004031304133412113203401202434122434340313312420340143230302444311410144134242324403414413032441433"
W = [[-1, 0, -2, 0, -4, 2, 5, -2, 2, 1, 4, 2, -2, -4], [1, 0, -1, 5, 2, 2, 1, -4, -5, 1, -5, -1, 4, 0]]
# transform frame A to frame P using the equation P = M + N (vector) and then apply a matrix multiplication--------------------------------------
# additionally, find the inverse transformation from frame P to frame A
variable_p = np.array([[math.sqrt(3) * math.cos(math.radians((30))), math.sqrt(3) * math.cos(math.radians((150)))], 
                       [math.sqrt(3) * math.sin(math.radians((30))), math.sqrt(3) * math.sin(math.radians((150)))]])
variable_a = np.linalg.inv(variable_p)
conv_to_p = np.matmul(variable_p, a_i) # converted to matrix P
conv_to_a = np.matmul(variable_a, conv_to_p) # converted to matrix A
# define variables for displaying frame P and frame A --------------------------------------------------------------------------------------------
matrix_a = (conv_to_a)
matrix_a = matrix_a.astype('int')
matrix_p = (conv_to_p)
# ------------------------------------------------------------------------------------------------------------------------------------------------
update = np.identity(3) # initialize a matrix for the purpose of updating its values 
update[0][2] = np.sum(conv_to_p[0])
update[1][2] = np.sum(conv_to_p[1])
save = update  # variable for storing the current value before making any updates
ident = np.identity(3) # translation matrix
turn_left =  [[math.cos(math.radians(60)),   -math.sin(math.radians(60)),   0], # rotation matrix around z-axis (left)
              [math.sin(math.radians(60)),    math.cos(math.radians(60)),   0],
              [0,                             0,                            1]]
turn_right = [[math.cos(math.radians(-60)),  -math.sin(math.radians(-60)),  0], # rotation matrix around z-axis (right)
              [math.sin(math.radians(-60)),   math.cos(math.radians(-60)),  0],
              [0,                             0,                            1]]
# conditions under which a command is executed ----------------------------------------------------------------------------------------------------
for i in range(len(com)):
    if com[i] == "1": # forward
        ident[0][2] = 0 # assign value (x, y)
        ident[1][2] = math.sqrt(3)
        save = np.copy(update) # store the current value
        update_new = np.matmul(update, ident) # apply a matrix multiplication
        conv_to_p = np.array([[update_new[0][2]], [update_new[1][2]]]) # update value
        conv_to_a = np.matmul(variable_a, conv_to_p) # converted to matrix P
        conv_to_a = np.round(conv_to_a).astype('int') # round numbers, change type of frame A to int
        if np.any(np.bitwise_and(np.isin(W[0], conv_to_a[0]), np.isin(W[1], conv_to_a[1]))): # check wall if it available
            conv_to_p = [[save[0][2]], [save[1][2]]] # re-store last value
            conv_to_a = np.matmul(variable_a, conv_to_p) # converted to matrix P
            conv_to_a = np.round(conv_to_a).astype('int') # round numbers, change type of frame A to int
            update = np.copy(save) # re-store last matrix
        else: # else wall is unavailable
            matrix_p = np.append(matrix_p, conv_to_p, axis = 1) # add path of frame P to matrix P
            matrix_a = np.append(matrix_a, conv_to_a, axis = 1) # add path of frame A to matrix A
            update = update_new # update current matrix

    elif com[i] == "2": # backward
        ident[0][2] = 0 # assign value (x, -y)
        ident[1][2] = -math.sqrt(3)
        save = np.copy(update) # store the current value
        update_new = np.matmul(update, ident) # apply a matrix multiplication
        conv_to_p = np.array([[update_new[0][2]], [update_new[1][2]]]) # update value
        conv_to_a = np.matmul(variable_a, conv_to_p) # converted to matrix P
        conv_to_a = np.round(conv_to_a).astype('int') # round numbers, change type of frame A to int
        if np.any(np.bitwise_and(np.isin(W[0], conv_to_a[0]), np.isin(W[1], conv_to_a[1]))): # check wall if it available
            conv_to_p = [[save[0][2]], [save[1][2]]] # re-store last value
            conv_to_a = np.matmul(variable_a, conv_to_p) # converted to matrix P
            conv_to_a = np.round(conv_to_a).astype('int') # round numbers, change type of frame A to int
            update = np.copy(save) # re-store last matrix
        else: # else wall is unavailable
            matrix_p = np.append(matrix_p, conv_to_p, axis = 1) # add path of frame P to matrix P
            matrix_a = np.append(matrix_a, conv_to_a, axis = 1) # add path of frame A to matrix A
            update = update_new # update current matrix
    elif com[i] == "3": # turn left
        update_new = np.matmul(update, turn_left) # apply a matrix multiplication
        update = update_new # update current matrix
    elif com[i] == "4": # turn right
        update_new = np.matmul(update, turn_right) # apply a matrix multiplication
        update = update_new # update current matrix

print(matrix_a)
print(matrix_p)