import numpy as np
import matplotlib.pyplot as plt
import random

def my_function(x):
    return -x**4 + 2 * x**3 + 2 * x**2 - x

def derivative(x):
    return (-4 * x**3) + (6 * x**2) + (4 * x) - 1

def gradient_ascent(start_x):
    gamma = 0.01
    x = start_x
    dx = gamma * derivative(x) 

    while abs(dx) > 0.001:
        y = my_function(x)
        plt.plot(x,y, color="blue", marker="s", markersize=6)
        x += dx
        dx = gamma * derivative(x)
    return x, my_function(x)

def exhaustive_search(start_x, end_x):
    step = 0.5
    cur_x = start_x
    max_x = cur_x
    max_y = my_function(cur_x)

    while cur_x < end_x:
        y = my_function(cur_x)
        if y > max_y:
            max_x = cur_x
            max_y = y
        cur_x += step

    return max_x, max_y

def plot():
    start = -2
    stop = 3
    steps = 100
    ran = np.linspace(start, stop, steps)
    y_values = map(my_function, ran)
    y_derivatives = map(derivative, ran)
    plt.plot(ran, y_values, 'b')
    plt.plot(ran, y_derivatives, 'r')
    
    randx = random.uniform(start,stop)
    max_ga = gradient_ascent(randx)
    plt.plot(max_ga[0],max_ga[1], color="yellow", marker="*", markersize=16)

    max_es = exhaustive_search(start, stop)
    plt.plot(max_es[0],max_es[1], color="green", marker="*", markersize=16)
    
    print('ga x ' + str(max_ga[0]) + ' y ' + str(max_ga[1]))
    print('es x ' + str(max_es[0]) + ' y ' + str(max_es[1]))
    plt.show()

plot()