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
            
print build_random_function