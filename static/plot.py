import numpy as np
import matplotlib.pyplot as plt
import data_processing as dp

def add_func_plot(func, xmin, xmax, number_of_steps, style = {}):
    '''Add the plot of the function using linspace'''
    tau = np.linspace(xmin, xmax, number_of_steps)
    plt.plot(tau, func(tau), **style)

def add_errors_plot(time_between_errors, style = {}):
    '''Add the plot of real errors '''
    numbers_of_errors = [i + 1 for i in range(0, len(time_between_errors))]
    times_of_errors = dp.convert_time_between_errors_to_time_of_errors(time_between_errors)
    plt.plot(times_of_errors, numbers_of_errors, **style)

def add_xy_plot(x_array, y_array):
    '''Plot data by x and y values'''
    plt.plot(x_array, y_array)

def xlabel(label):
    plt.xlabel(label)

def ylabel(label):
    plt.ylabel(label)

def grid():
    plt.grid()

def show():
    plt.show()

def legend():
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
       fancybox=True, shadow=True, ncol=5)