#!/usr/bin/python3
from trackbeebot import BeeBot
import matplotlib.pyplot as plt 
from matplotlib.patches import Polygon
import numpy as np
import math
import json

class MyBeeBot(BeeBot):
    a_i = []
    def __init__(self,a_i):
        super().__init__(a_i)
        self.a_i = a_i
    # a_i is initial position
    # c is command {'0'->stop, '1'->forward, '2'->backward, '3'->turn right, '4'->turn left}
    # o is obstacle
    
    def trackBeeBot(self, com, W):
        # pass
        # a_i is initial position
        # com is command {'0'->stop, '1'->forward, '2'->backward, '3'->turn right, '4'->turn left}
        # W is wall
        
        # add your code here

        variable_p = np.array([[math.sqrt(3) * math.cos(math.radians((30))), math.sqrt(3) * math.cos(math.radians((150)))], 
                            [math.sqrt(3) * math.sin(math.radians((30))), math.sqrt(3) * math.sin(math.radians((150)))]])
        variable_a = np.linalg.inv(variable_p)
        conv_to_p = np.matmul(variable_p, a_i)
        conv_to_a = np.matmul(variable_a, conv_to_p)
        # output ----------------------------------------------------
        matrix_p = (conv_to_p)
        matrix_a = (conv_to_a)
        # homogenous ------------------------------------------------
        theta = 0
        update  = [[1,  0,  0], 
                [0,   1,  0],
                [0,   0,  1]]
        update[0][2] = np.sum(conv_to_p[0])
        update[1][2] = np.sum(conv_to_p[1])
        save = update
        ident = np.identity(3)
        turn_left =  [[math.cos(math.radians(60)),   -math.sin(math.radians(60)),   0], 
                    [math.sin(math.radians(60)),    math.cos(math.radians(60)),   0],
                    [0,                             0,                            1]]
        turn_right = [[math.cos(math.radians(-60)),  -math.sin(math.radians(-60)),  0], 
                    [math.sin(math.radians(-60)),   math.cos(math.radians(-60)),  0],
                    [0,                             0,                            1]]
        # command ------------------------------------------------
        for i in range(len(com)): #len(com)
            if com[i] == "1":
                ident[0][2] = 0
                ident[1][2] = math.sqrt(3)
                save = np.copy(update)
                update_new = np.matmul(update, ident)
                conv_to_p = np.array([[update_new[0][2]], [update_new[1][2]]])
                # conv_to_p[0] = np.sum(update_new[0])
                # conv_to_p[1] = np.sum(update_new[1])
                conv_to_a = np.matmul(variable_a, conv_to_p)
                conv_to_a = np.round(conv_to_a).astype('int')
                # conv_to_a[0] = np.round(conv_to_a[0])
                # conv_to_a[1] = np.round(conv_to_a[1])
                print(np.any(np.bitwise_and(np.isin(W[0], conv_to_a[0]), np.isin(W[1], conv_to_a[1]))))
                if np.any(np.bitwise_and(np.isin(W[0], conv_to_a[0]), np.isin(W[1], conv_to_a[1]))):
                    # conv_to_p[0] = np.sum(save[0][2])
                    # conv_to_p[1] = np.sum(save[1][2])
                    conv_to_p = [[save[0][2]], [save[1][2]]]
                    conv_to_a = np.matmul(variable_a, conv_to_p)
                    conv_to_a = np.round(conv_to_a).astype('int')
                    # conv_to_a[0] = np.round(conv_to_a[0])
                    # conv_to_a[1] = np.round(conv_to_a[1])
                    update = np.copy(save)
                else:
                    matrix_p = np.append(matrix_p, conv_to_p, axis = 1)
                    matrix_a = np.append(matrix_a, conv_to_a, axis = 1)
                    print(1)
                    update = update_new
            elif com[i] == "2":
                ident[0][2] = 0
                ident[1][2] = -math.sqrt(3)
                save = np.copy(update)
                update_new = np.matmul(update, ident)
                conv_to_p = np.array([[update_new[0][2]], [update_new[1][2]]])
                # conv_to_p[0] = np.sum(update_new[0])
                # conv_to_p[1] = np.sum(update_new[1])
                conv_to_a = np.matmul(variable_a, conv_to_p)
                conv_to_a = np.round(conv_to_a).astype('int')
                # conv_to_a[0] = np.round(conv_to_a[0])
                # conv_to_a[1] = np.round(conv_to_a[1])

                if np.any(np.bitwise_and(np.isin(W[0], conv_to_a[0]), np.isin(W[1], conv_to_a[1]))):
                    conv_to_p = [[save[0][2]], [save[1][2]]]
                    conv_to_a = np.matmul(variable_a, conv_to_p)
                    conv_to_a = np.round(conv_to_a).astype('int')
                    update = np.copy(save)
                else:
                    matrix_p = np.append(matrix_p, conv_to_p, axis = 1)
                    matrix_a = np.append(matrix_a, conv_to_a, axis = 1)
                    update = update_new
            elif com[i] == "3":
                theta = math.radians(-60)
                update_new = np.matmul(update, turn_left)
                update = update_new
            elif com[i] == "4":
                theta = math.radians(60)
                update_new = np.matmul(update, turn_right)
                update = update_new

        return (matrix_a, matrix_p)