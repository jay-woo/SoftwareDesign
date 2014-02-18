from functions import *
from random import *

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
    elif max_depth == min_depth:
        """Selects a function to nest into the equation"""
        if min_depth > 1: #Selects a random function
            random_function = functions[randint(0,4)]
            if random_function in functions_a:
                return [random_function, build_random_function(min_depth-1, max_depth-1)]
            elif random_function in functions_ab:
                return [random_function, build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
        elif min_depth == 1: #Base case
            random_function = parameters[randint(0,1)]
            return [random_function]
            
print build_random_function(3, 5)