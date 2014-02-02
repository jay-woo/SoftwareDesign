def check_fermat(a, b, c, n):
    if a**n + b**n == c**n:
        print "Holy smokes, Fermat was wrong!"
    else:
        print "No, that doesn't work"
        
def input_fermat():
    a = int(raw_input("What is a? "))
    b = int(raw_input("What is b? "))
    c = int(raw_input("What is c? "))
    n = int(raw_input("What is n? "))        
    
    check_fermat(a, b, c, n)
    
check_fermat(1, 2, 3, 5)