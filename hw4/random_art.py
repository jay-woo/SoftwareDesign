# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:34:57 2014

@author: pruvolo
"""

# you do not have to use these particular modules, but they may help
from random import randint
from functions import *
from math import *
from PIL import Image

def build_random_function(min_depth, max_depth):
    """ Recursively generates a random function whose depth can be any
        number within the range min_depth to max_depth.
    
        Input:
            min_depth - the minimum depth of the generated function
            max_depth - the maximum depth of the generated function
        Output:
            A composition of functions represented as a list of strings
                ex. ['sin_pi', ['prod', ['x'], ['y']]]
    """
    
    """Recursively generates a function"""
    if max_depth > min_depth:
        random_depth = randint(min_depth, max_depth)
        return build_random_function(random_depth, random_depth)
    elif min_depth >= 1:
        """Selects a function to nest into the equation"""
        if min_depth > 2:
            random_function = functions[randint(0,4)] #Selects a random function
        elif min_depth > 1:
            random_function = functions_a[randint(0,2)] #Selects a function w/ one parameter, if the current depth is too small
        elif min_depth == 1: #Base case
            random_function = parameters[randint(0,1)]
            return [random_function]
        
        """Figures out how to nest the functions together depending on how many parameters there are"""
        if random_function in functions_a: #One parameter
            return [random_function, build_random_function(min_depth-1, max_depth-1)]
        elif random_function in functions_ab: #Two parameters
            n = randint(1, min_depth-2)   #Randomly distributes the depth
            m = min_depth - n - 1         #between the two nested functions
            return [random_function, build_random_function(n, n), build_random_function(m, m)]


def evaluate_random_function(f, x, y):
    """ Evaluates the function f using the given values x and y
    
        Input:
            f - a composition of functions
        Output:
            The result of plugging in x and y into the function
    """

    func1 = f[0]
    func2 = f[1]
    
    """Calculates the first inner function"""
    if func2[0] in parameters:
        if func2[0] == "x":
            res = x
        elif func2[0] == "y":
            res = y
    else:
        res = evaluate_random_function(func2, x, y)
        
    """Calculates the second inner function (if one exists)"""
    if func1 in functions_ab:
        func3 = f[2]
        if func3[0] in parameters:
            if func3[0] == "x":
                res2 = x
            elif func3[0] == "y":
                res2 = y
        else:
            res2 = evaluate_random_function(func3, x, y)

    if func1 in functions_a:
        """Calculates the outer function (one parameter)"""
        if func1 == "sin_pi":
            return sin(pi*res)
        elif func1 == "cos_pi":
            return cos(pi*res)
        elif func1 =="square":
            return res**2
    
    elif func1 in functions_ab:
        """Calculates the outer function (two parameters)"""
        if func1 == "prod":
            return res * res2
        elif func1 == "avg":
            return (res + res2) / 2
    
def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Maps the input value that is in the interval [input_interval_start, input_interval_end]
        to the output interval [output_interval_start, output_interval_end].  The mapping
        is an affine one (i.e. output = input*c + b).
    
        TODO: please fill out the rest of this docstring
    """
    
    c = float(output_interval_end - output_interval_start) / (input_interval_end - input_interval_start)
    b = c*(output_interval_start - input_interval_start)
    
    return val*c + b
    
def main():
    x = 350
    y = 350

    red = build_random_function(10, 20)    
    green = build_random_function(10, 20)
    blue = build_random_function(10, 20)
    
    im = Image.new("RGB", (x,y))
    pixels = im.load()

    for i in range(x):
        for j in range(y):
            x_coord = remap_interval(i, 0, x, -1, 1)
            y_coord = remap_interval(j, 0, y, -1, 1)
            
            red_px = evaluate_random_function(red, x_coord, y_coord)
            green_px = evaluate_random_function(green, x_coord, y_coord)
            blue_px = evaluate_random_function(blue, x_coord, y_coord)
            
            red_px = int(remap_interval(red_px, -1, 1, 0, 256))
            green_px = int(remap_interval(green_px, -1, 1, 0, 256))
            blue_px = int(remap_interval(blue_px, -1, 1, 0, 256))
            
            pixels[i, j] = (red_px, green_px, blue_px)
    im.format = "PNG"
    im.save('example.png')
            
main()