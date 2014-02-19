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
    
    if max_depth > min_depth: #Selects a random depth
        random_depth = randint(min_depth, max_depth)
        return build_random_function(random_depth, random_depth)
    else: #Creates a random function with the selected random depth
        if min_depth == 1: #Base case
            return list(parameters[randint(0,1)])
        else:
            random_function = functions[randint(0,4)]
            if random_function in functions_a: #If there is one parameter
                return [random_function, build_random_function(min_depth-1, max_depth-1)]
            elif random_function in functions_ab: #If there are two parameters
                return [random_function, build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
                
def evaluate_random_function(f, x, y):
    """ Evaluates the function f using the given values x and y
    
        Input:
            f - a composition of functions
        Output:
            The result of plugging in x and y into the function
    """

        
    if f[0] in parameters: #Base case
        if f[0] == "x":
            return x
        else:
            return y
    else: #Evaluates all of the functions
        if f[0] == "sin_pi":
            return sin(pi*evaluate_random_function(f[1], x, y))
        elif f[0] == "cos_pi":
            return cos(pi*evaluate_random_function(f[1], x, y))
        elif f[0] == "square":
            return (evaluate_random_function(f[1], x, y))**2
        elif f[0] == "prod":
            return (evaluate_random_function(f[1], x, y)) * (evaluate_random_function(f[2], x, y))
        elif f[0] == "avg":
            return ((evaluate_random_function(f[1], x, y)) + (evaluate_random_function(f[2], x, y))) / 2
   
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